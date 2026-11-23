"""
API Views for Resume Upload, Parsing, Skill Extraction, and Profile Sync.
"""

import os
import logging
from django.utils import timezone
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser

from .models import ResumeDocument, ResumeExtraction
from .serializers import (
    ResumeDocumentSerializer,
    ResumeExtractionSerializer,
    ApplyToProfileInputSerializer
)
from .services.parser import parse_resume_document, DocumentParsingError
from .services.extractor import extract_resume_intelligence
from .services.profile_sync import sync_confirmed_skills_to_profile

logger = logging.getLogger("resumes.views")

class ResumeUploadView(APIView):
    """
    POST /api/resumes/upload/
    Uploads a PDF or DOCX resume document (max 5MB) and executes text extraction.
    """
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        file_obj = request.FILES.get('file')
        if not file_obj:
            return Response({"error": "No resume file provided."}, status=status.HTTP_400_BAD_REQUEST)

        # 1. Size Validation (Max 5MB)
        max_size = getattr(settings, 'MAX_UPLOAD_SIZE', 5 * 1024 * 1024)
        if file_obj.size > max_size:
            return Response(
                {"error": f"File exceeds maximum allowed size of 5 MB ({round(file_obj.size / (1024*1024), 2)} MB)."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 2. Extension Validation
        ext = os.path.splitext(file_obj.name)[1].lower().replace('.', '')
        if ext not in ['pdf', 'docx', 'doc']:
            return Response(
                {"error": f"Unsupported file type '.{ext}'. Supported formats: PDF, DOCX."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 3. Create ResumeDocument
        resume_doc = ResumeDocument.objects.create(
            user=request.user,
            original_filename=file_obj.name,
            file=file_obj,
            file_size=file_obj.size,
            file_type=ext,
            processing_status='parsing'
        )

        # 4. Execute extraction immediately
        try:
            full_path = resume_doc.file.path
            raw_text, warnings = parse_resume_document(full_path, ext)
            intelligence = extract_resume_intelligence(raw_text)

            extraction = ResumeExtraction.objects.create(
                resume_document=resume_doc,
                extracted_skills=intelligence["extracted_skills"],
                candidate_info=intelligence["candidate_info"],
                raw_text_length=intelligence["raw_text_length"],
                warnings=warnings
            )

            resume_doc.processing_status = 'extracted'
            resume_doc.processed_at = timezone.now()
            resume_doc.save(update_fields=['processing_status', 'processed_at'])

            return Response({
                "document": ResumeDocumentSerializer(resume_doc).data,
                "extraction": ResumeExtractionSerializer(extraction).data,
                "message": "Resume uploaded and skills extracted successfully."
            }, status=status.HTTP_201_CREATED)

        except DocumentParsingError as e:
            logger.error(f"Document parsing failed for {file_obj.name}: {e}")
            resume_doc.processing_status = 'failed'
            resume_doc.error_message = str(e)
            resume_doc.save(update_fields=['processing_status', 'error_message'])
            return Response({
                "document": ResumeDocumentSerializer(resume_doc).data,
                "error": str(e)
            }, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except Exception as e:
            logger.exception(f"Unexpected extraction failure: {e}")
            resume_doc.processing_status = 'failed'
            resume_doc.error_message = "Unexpected document extraction error."
            resume_doc.save(update_fields=['processing_status', 'error_message'])
            return Response({
                "error": "Failed to extract information from uploaded document."
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ResumeListView(APIView):
    """
    GET /api/resumes/
    Lists all uploaded resumes for the authenticated user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        resumes = ResumeDocument.objects.filter(user=request.user)
        return Response(ResumeDocumentSerializer(resumes, many=True).data, status=status.HTTP_200_OK)


class ResumeDetailView(APIView):
    """
    GET /api/resumes/{id}/ - Retrieve document status
    DELETE /api/resumes/{id}/ - Delete file from disk and record from DB
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk, user):
        return get_object_or_404(ResumeDocument, pk=pk, user=user)

    def get(self, request, pk):
        resume = self.get_object(pk, request.user)
        return Response(ResumeDocumentSerializer(resume).data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        resume = self.get_object(pk, request.user)
        # Delete file from storage
        try:
            if resume.file and os.path.exists(resume.file.path):
                os.remove(resume.file.path)
        except Exception as e:
            logger.warning(f"Could not remove resume file from disk: {e}")

        resume.delete()
        return Response({"message": "Resume document deleted successfully."}, status=status.HTTP_204_NO_CONTENT)


class ResumeResultsView(APIView):
    """
    GET /api/resumes/{id}/results/
    Fetches structured extraction results and compares with active profile skills.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        resume = get_object_or_404(ResumeDocument, pk=pk, user=request.user)
        if not hasattr(resume, 'extraction'):
            return Response(
                {"error": "No extraction results available for this document.", "status": resume.processing_status},
                status=status.HTTP_404_NOT_FOUND
            )

        extraction = resume.extraction
        
        # Compare against current profile
        profile = getattr(request.user, 'profile', None)
        existing_skills = [s.name for s in profile.skills.all()] if profile else []
        existing_skills_lower = {s.lower() for s in existing_skills}

        extracted_skills = extraction.extracted_skills
        new_skills = []
        already_possessed = []

        for item in extracted_skills:
            if item["canonical_name"].lower() in existing_skills_lower:
                already_possessed.append(item)
            else:
                new_skills.append(item)

        return Response({
            "document": ResumeDocumentSerializer(resume).data,
            "extraction": ResumeExtractionSerializer(extraction).data,
            "comparison": {
                "existing_profile_skills": existing_skills,
                "new_skills_detected": new_skills,
                "already_in_profile": already_possessed,
                "total_extracted": len(extracted_skills),
                "total_new": len(new_skills)
            }
        }, status=status.HTTP_200_OK)


class ResumeApplyToProfileView(APIView):
    """
    POST /api/resumes/{id}/apply-to-profile/
    Applies user-confirmed skills and optional metadata to the authenticated user's profile.
    Mandatory explicit confirmation step.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        resume = get_object_or_404(ResumeDocument, pk=pk, user=request.user)
        serializer = ApplyToProfileInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        update_meta = {}
        if hasattr(resume, 'extraction'):
            candidate_info = resume.extraction.candidate_info
            if data.get("apply_job_role") and candidate_info.get("detected_role"):
                update_meta["job_role"] = candidate_info["detected_role"]
            if data.get("apply_experience") and candidate_info.get("detected_experience_years") is not None:
                update_meta["years_of_experience"] = candidate_info["detected_experience_years"]
            if data.get("apply_education") and candidate_info.get("education"):
                update_meta["education"] = candidate_info["education"]

        result = sync_confirmed_skills_to_profile(
            user=request.user,
            confirmed_skills=data["confirmed_skills"],
            update_meta_fields=update_meta
        )

        resume.processing_status = 'applied'
        resume.save(update_fields=['processing_status'])

        return Response({
            "message": f"Successfully synced {len(result['skills_added'])} new skills to your profile.",
            "details": result
        }, status=status.HTTP_200_OK)
