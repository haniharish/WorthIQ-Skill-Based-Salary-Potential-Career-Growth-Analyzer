from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.db.models import Q
from .models import UserProfile, Skill
from .serializers import UserProfileSerializer, SkillSerializer

# Default skills to seed if DB is fresh
DEFAULT_SKILLS = [
    'Python', 'Django', 'React.js', 'JavaScript', 'TypeScript', 'Node.js',
    'PostgreSQL', 'Docker', 'AWS', 'Git', 'REST APIs', 'SQL',
    'Tailwind CSS', 'Next.js', 'MongoDB', 'Redis', 'Machine Learning',
    'Data Analysis', 'HTML5', 'CSS3', 'Linux', 'GraphQL', 'Kubernetes',
    'FastAPI', 'Pandas', 'NumPy', 'Scikit-Learn', 'Java', 'Spring Boot',
    'C++', 'Go', 'Flutter', 'Express.js', 'CI/CD', 'Microservices'
]

class UserProfileView(APIView):
    """
    User Profile Management:
    GET: Retrieve current user's profile.
    POST: Create profile for current user.
    PUT: Full update of profile.
    PATCH: Partial update of profile.
    Users cannot access or modify other users' profiles.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, user):
        try:
            return user.profile
        except UserProfile.DoesNotExist:
            return None

    def get(self, request):
        profile = self.get_object(request.user)
        if not profile:
            return Response(
                {
                    'detail': 'Profile not found. Please complete profile setup.',
                    'has_profile': False
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = UserProfileSerializer(profile, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if self.get_object(request.user):
            return Response(
                {'detail': 'Profile already exists. Use PUT or PATCH to update.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = UserProfileSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            profile = serializer.save()
            return Response(
                UserProfileSerializer(profile, context={'request': request}).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        profile = self.get_object(request.user)
        if not profile:
            return Response(
                {'detail': 'Profile not found. Please create a profile first.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = UserProfileSerializer(profile, data=request.data, context={'request': request})
        if serializer.is_valid():
            updated_profile = serializer.save()
            return Response(
                UserProfileSerializer(updated_profile, context={'request': request}).data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        profile = self.get_object(request.user)
        if not profile:
            return Response(
                {'detail': 'Profile not found. Please create a profile first.'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = UserProfileSerializer(profile, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            updated_profile = serializer.save()
            return Response(
                UserProfileSerializer(updated_profile, context={'request': request}).data,
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SkillListView(APIView):
    """
    Skill catalog endpoint:
    GET: Returns list of skills with optional ?search= parameter.
    Seeds default common tech skills on first access if table is empty.
    """
    permission_classes = [AllowAny]

    def get(self, request):
        # Auto-seed if skills table is empty
        if not Skill.objects.exists():
            for name in DEFAULT_SKILLS:
                Skill.objects.get_or_create(name=name)

        search_query = request.query_params.get('search', '').strip()
        if search_query:
            skills = Skill.objects.filter(name__icontains=search_query)[:30]
        else:
            skills = Skill.objects.all()[:100]

        serializer = SkillSerializer(skills, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
