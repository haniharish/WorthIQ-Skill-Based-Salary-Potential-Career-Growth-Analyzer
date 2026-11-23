import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';
import { resumeService } from '../services/resumeService';
import { Card, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import {
  FileText,
  UploadCloud,
  CheckCircle2,
  AlertTriangle,
  Sparkles,
  ArrowRight,
  Trash2,
  Clock,
  User,
  Mail,
  Phone,
  Briefcase,
  GraduationCap,
  ShieldCheck,
  Search,
  Check,
  FileCheck,
  RefreshCw,
  ExternalLink,
} from 'lucide-react';

export const ResumeAnalysisPage = () => {
  const { profile, fetchProfile } = useAuth();
  const toast = useToast();
  const navigate = useNavigate();
  const fileInputRef = useRef(null);

  // Upload state
  const [selectedFile, setSelectedFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);

  // Resume lists and active extraction state
  const [resumes, setResumes] = useState([]);
  const [loadingResumes, setLoadingResumes] = useState(false);
  const [activeResumeId, setActiveResumeId] = useState(null);
  const [activeResults, setActiveResults] = useState(null);
  const [loadingResults, setLoadingResults] = useState(false);

  // Profile Sync Selection state
  const [selectedSkillsToApply, setSelectedSkillsToApply] = useState([]);
  const [applyExp, setApplyExp] = useState(false);
  const [applyEdu, setApplyEdu] = useState(false);
  const [applyRole, setApplyRole] = useState(false);
  const [showConfirmModal, setShowConfirmModal] = useState(false);
  const [applying, setApplying] = useState(false);

  // Fetch list of user's resumes
  const fetchResumesList = async () => {
    setLoadingResumes(true);
    try {
      const data = await resumeService.getResumes();
      const resumeList = Array.isArray(data) ? data : (data?.results || []);
      setResumes(resumeList);
      if (resumeList.length > 0 && !activeResumeId) {
        // Load the most recent one
        loadResumeResults(resumeList[0].id);
      }
    } catch (err) {
      console.warn('Could not load resumes', err);
    } finally {
      setLoadingResumes(false);
    }
  };

  useEffect(() => {
    fetchResumesList();
  }, []);

  // Load results of a specific resume
  const loadResumeResults = async (id) => {
    setActiveResumeId(id);
    setLoadingResults(true);
    try {
      const data = await resumeService.getResumeResults(id);
      setActiveResults(data);

      // Pre-select new skills by default
      const comparisonData = data?.comparison || {};
      const newSkills = Array.isArray(comparisonData.new_skills)
        ? comparisonData.new_skills
        : Array.isArray(comparisonData.new_skills_detected)
          ? comparisonData.new_skills_detected.map((s) => (typeof s === 'string' ? s : (s.canonical_name || s.name)))
          : [];

      setSelectedSkillsToApply(newSkills);
      setApplyExp(false);
      setApplyEdu(false);
      setApplyRole(false);
    } catch (err) {
      console.error('Failed to load resume results:', err);
      toast.error('Failed to load extraction details for this resume.');
    } finally {
      setLoadingResults(false);
    }
  };

  // Drag and drop handlers
  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setDragActive(true);
    } else if (e.type === 'dragleave') {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const validateAndSetFile = (file) => {
    const ext = file.name.split('.').pop().toLowerCase();
    if (!['pdf', 'docx'].includes(ext)) {
      toast.error('Only PDF and DOCX files are supported.');
      return;
    }
    if (file.size > 5 * 1024 * 1024) {
      toast.error('File size exceeds maximum limit of 5MB.');
      return;
    }
    setSelectedFile(file);
  };

  // Upload and parse resume
  const handleUpload = async () => {
    if (!selectedFile) return;
    setUploading(true);
    setUploadProgress(15);
    try {
      const result = await resumeService.uploadResume(selectedFile, (progressEvent) => {
        if (progressEvent.total) {
          const percent = Math.round((progressEvent.loaded * 100) / progressEvent.total);
          setUploadProgress(Math.min(percent, 95));
        }
      });
      toast.success('Resume parsed and skills extracted successfully!');
      setSelectedFile(null);
      if (fileInputRef.current) fileInputRef.current.value = '';
      await fetchResumesList();

      const docId = result?.document?.id || result?.resume?.id || result?.id;
      if (docId) {
        loadResumeResults(docId);
      }
    } catch (err) {
      console.error('Upload error:', err);
      const errMsg = err.response?.data?.file?.[0] || err.response?.data?.error || 'Failed to process resume.';
      toast.error(errMsg);
    } finally {
      setUploading(false);
      setUploadProgress(0);
    }
  };

  // Delete resume
  const handleDeleteResume = async (id, e) => {
    e.stopPropagation();
    if (!window.confirm('Delete this resume and its extracted intelligence?')) return;
    try {
      await resumeService.deleteResume(id);
      toast.success('Resume deleted.');
      if (activeResumeId === id) {
        setActiveResumeId(null);
        setActiveResults(null);
      }
      await fetchResumesList();
    } catch (err) {
      toast.error('Failed to delete resume.');
    }
  };

  // Toggle skill selection for profile sync
  const toggleSkillSelection = (skillName) => {
    setSelectedSkillsToApply((prev) =>
      prev.includes(skillName)
        ? prev.filter((s) => s !== skillName)
        : [...prev, skillName]
    );
  };

  // Select/Deselect all new skills
  const handleSelectAllNew = () => {
    if (newSkillsList.length === 0) return;
    if (selectedSkillsToApply.length === newSkillsList.length) {
      setSelectedSkillsToApply([]);
    } else {
      setSelectedSkillsToApply([...newSkillsList]);
    }
  };

  // Apply to profile handler
  const handleConfirmApply = async () => {
    if (!activeResumeId) return;
    setApplying(true);
    try {
      const payload = {
        confirmed_skills: selectedSkillsToApply,
        skills: selectedSkillsToApply,
        apply_experience: applyExp,
        apply_education: applyEdu,
        apply_job_role: applyRole,
      };
      const res = await resumeService.applyToProfile(activeResumeId, payload);
      toast.success(res.message || 'Profile successfully updated with verified skills!');
      setShowConfirmModal(false);
      if (fetchProfile) await fetchProfile();
      // Reload current extraction to update comparison state
      loadResumeResults(activeResumeId);
    } catch (err) {
      console.error('Apply error:', err);
      toast.error('Failed to update profile. Please try again.');
    } finally {
      setApplying(false);
    }
  };

  // Safely extract active document & extraction attributes
  const activeDoc = activeResults?.document || activeResults?.resume || {};
  const extraction = activeResults?.extraction || {};
  const candidateInfo = extraction?.candidate_info || {};

  const rawExtractedSkills = Array.isArray(extraction?.extracted_skills)
    ? extraction.extracted_skills
    : [];

  const extractedSkills = rawExtractedSkills.map((s) => ({
    name: s.canonical_name || s.name || (typeof s === 'string' ? s : 'Skill'),
    confidence: s.confidence != null ? Math.round(s.confidence <= 1 ? s.confidence * 100 : s.confidence) : 90,
    snippet: s.evidence_snippet || s.snippet || '',
    category: s.category || 'Technical Skill',
  }));

  const comparisonRaw = activeResults?.comparison || {};

  const newSkillsList = Array.isArray(comparisonRaw.new_skills)
    ? comparisonRaw.new_skills
    : Array.isArray(comparisonRaw.new_skills_detected)
      ? comparisonRaw.new_skills_detected.map((s) => (typeof s === 'string' ? s : (s.canonical_name || s.name)))
      : [];

  const existingSkillsList = Array.isArray(comparisonRaw.existing_skills)
    ? comparisonRaw.existing_skills
    : Array.isArray(comparisonRaw.existing_profile_skills)
      ? comparisonRaw.existing_profile_skills
      : Array.isArray(comparisonRaw.already_in_profile)
        ? comparisonRaw.already_in_profile.map((s) => (typeof s === 'string' ? s : (s.canonical_name || s.name)))
        : [];

  const expValue = candidateInfo.detected_experience_years != null
    ? candidateInfo.detected_experience_years
    : candidateInfo.years_of_experience;

  const expDisplay = expValue != null ? `${expValue} yrs` : 'Not detected';
  const eduDisplay = candidateInfo.education || candidateInfo.education_level || 'Not detected';
  const roleDisplay = candidateInfo.detected_role || candidateInfo.job_role || candidateInfo.role || 'Not detected';
  const emailDisplay = candidateInfo.email || 'Not detected';
  const phoneDisplay = candidateInfo.phone || 'Not detected';

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-16">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-200">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-slate-900">
              Resume Intelligence & Skill Extractor
            </h1>
            <Badge variant="primary" size="sm">NLP Engine</Badge>
          </div>
          <p className="text-xs sm:text-sm text-slate-600">
            Upload your resume (PDF or DOCX) to automatically discover verified technical competencies, extract experience, and sync to your profile.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            icon={Briefcase}
            onClick={() => navigate('/role-matching')}
          >
            Check Role Fit
          </Button>
          <Button
            variant="primary"
            size="sm"
            icon={Sparkles}
            onClick={() => navigate('/salary-analysis')}
          >
            Predict Salary
          </Button>
        </div>
      </div>

      {/* Main Grid: Upload & History on Left (5 cols), Analysis Results on Right (7 cols) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">

        {/* Left Column: Upload Zone & Document History */}
        <div className="lg:col-span-5 space-y-6">

          {/* Upload Card */}
          <Card className="border-indigo-100 shadow-sm">
            <CardHeader
              title="Upload Resume Document"
              subtitle="Supports PDF and DOCX formats up to 5MB"
              icon={UploadCloud}
            />

            <div className="pt-2 space-y-4">
              <div
                onDragEnter={handleDrag}
                onDragLeave={handleDrag}
                onDragOver={handleDrag}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
                className={`p-6 border-2 border-dashed rounded-xl flex flex-col items-center justify-center text-center cursor-pointer transition-all ${
                  dragActive
                    ? 'border-indigo-500 bg-indigo-50/70'
                    : 'border-slate-300 hover:border-indigo-400 bg-slate-50/50'
                }`}
              >
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                  onChange={handleFileChange}
                  className="hidden"
                />

                <FileText className="w-10 h-10 text-indigo-500 mb-2" />
                <p className="text-xs font-semibold text-slate-800">
                  {selectedFile ? selectedFile.name : 'Click to browse or drag and drop'}
                </p>
                <p className="text-[11px] text-slate-500 mt-0.5">
                  PDF or DOCX (Max 5MB)
                </p>
                {selectedFile && (
                  <span className="mt-2 text-[10px] bg-indigo-100 text-indigo-700 font-medium px-2 py-0.5 rounded-full">
                    {(selectedFile.size / 1024 / 1024).toFixed(2)} MB • Ready
                  </span>
                )}
              </div>

              {/* Progress bar during upload */}
              {uploading && (
                <div className="space-y-1">
                  <div className="flex justify-between text-xs text-slate-600">
                    <span>Extracting skills & metadata...</span>
                    <span>{uploadProgress}%</span>
                  </div>
                  <div className="w-full bg-slate-200 h-2 rounded-full overflow-hidden">
                    <div
                      className="bg-indigo-600 h-full transition-all duration-300"
                      style={{ width: `${uploadProgress}%` }}
                    />
                  </div>
                </div>
              )}

              <Button
                variant="primary"
                size="md"
                className="w-full"
                icon={UploadCloud}
                onClick={handleUpload}
                disabled={!selectedFile || uploading}
                isLoading={uploading}
              >
                {uploading ? 'Analyzing Document...' : 'Parse Resume & Extract Skills'}
              </Button>
            </div>
          </Card>

          {/* Uploaded Resumes History List */}
          <Card>
            <div className="flex items-center justify-between pb-3 border-b border-slate-200">
              <div className="flex items-center gap-2">
                <Clock className="w-4 h-4 text-indigo-600" />
                <h3 className="text-sm font-bold text-slate-800">Uploaded Documents</h3>
              </div>
              <span className="text-xs text-slate-500">{resumes.length} parsed</span>
            </div>

            <div className="pt-3 space-y-2 max-h-64 overflow-y-auto">
              {loadingResumes ? (
                <div className="py-4 text-center text-xs text-slate-400">Loading history...</div>
              ) : resumes.length === 0 ? (
                <div className="py-4 text-center text-xs text-slate-400 italic">
                  No resumes uploaded yet. Upload a resume above to analyze.
                </div>
              ) : (
                resumes.map((r) => {
                  const isActive = activeResumeId === r.id;
                  const dateStr = r.uploaded_at || r.created_at
                    ? new Date(r.uploaded_at || r.created_at).toLocaleDateString()
                    : 'Recent';
                  const fileType = (r.file_type || 'PDF').toUpperCase();
                  const fileSize = r.file_size_formatted || (r.file_size ? `${(r.file_size / 1024).toFixed(0)} KB` : 'N/A');
                  const countDisplay = r.extracted_skills_count != null ? `${r.extracted_skills_count} skills` : 'Analyzed';

                  return (
                    <div
                      key={r.id}
                      onClick={() => loadResumeResults(r.id)}
                      className={`p-3 rounded-lg border text-xs cursor-pointer transition-all ${
                        isActive
                          ? 'border-indigo-500 bg-indigo-50/60 shadow-sm'
                          : 'border-slate-200 hover:border-slate-300 bg-white'
                      }`}
                    >
                      <div className="flex items-start justify-between gap-2">
                        <div className="flex items-start gap-2 overflow-hidden">
                          <FileCheck className={`w-4 h-4 shrink-0 mt-0.5 ${isActive ? 'text-indigo-600' : 'text-slate-400'}`} />
                          <div className="truncate">
                            <div className="font-bold text-slate-900 truncate">
                              {r.original_filename}
                            </div>
                            <div className="text-[11px] text-slate-500">
                              {dateStr} • {fileType} • {fileSize}
                            </div>
                          </div>
                        </div>

                        <div className="flex items-center gap-1 shrink-0">
                          <Badge variant={r.processing_status === 'applied' || r.processing_status === 'extracted' ? 'success' : 'neutral'} size="sm">
                            {countDisplay}
                          </Badge>
                          <button
                            type="button"
                            onClick={(e) => handleDeleteResume(r.id, e)}
                            className="p-1 text-slate-400 hover:text-rose-600 rounded"
                            title="Delete"
                          >
                            <Trash2 className="w-3.5 h-3.5" />
                          </button>
                        </div>
                      </div>
                    </div>
                  );
                })
              )}
            </div>
          </Card>

          {/* Privacy & Zero-Auto-Sync Guarantee Notice */}
          <div className="p-4 bg-emerald-50/60 border border-emerald-200 rounded-xl flex items-start gap-3">
            <ShieldCheck className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
            <div className="text-xs text-emerald-800 space-y-1">
              <span className="font-bold">Strict Privacy & Confirmation Guarantee:</span>
              <p>
                WorthIQ will NEVER modify your candidate profile automatically. You retain full granular control to review every extracted skill and explicitly confirm synchronization.
              </p>
            </div>
          </div>

        </div>

        {/* Right Column: Extracted Intelligence & Profile Sync Panel */}
        <div className="lg:col-span-7 space-y-6">

          {loadingResults ? (
            <Card className="p-12 text-center text-slate-500 text-xs">
              <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2 text-indigo-600" />
              Loading extraction analytics...
            </Card>
          ) : !activeResults ? (
            <Card className="p-12 text-center text-slate-400 text-xs">
              <FileText className="w-10 h-10 mx-auto mb-2 text-slate-300" />
              Upload a resume or select one from the history to view extracted skills and profile comparison.
            </Card>
          ) : (
            <>
              {/* Candidate Metadata Summary Card */}
              <Card>
                <CardHeader
                  title="Candidate Metadata Extracted"
                  subtitle={`Derived from ${activeDoc.original_filename || 'Uploaded Document'}`}
                  icon={User}
                />
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 pt-2 text-xs">
                  <div className="p-2.5 bg-slate-50 rounded-lg">
                    <span className="text-[11px] text-slate-500 block mb-0.5 flex items-center gap-1">
                      <User className="w-3 h-3" /> Candidate Name
                    </span>
                    <span className="font-bold text-slate-800 truncate block">
                      {candidateInfo.name || candidateInfo.full_name || 'Not detected'}
                    </span>
                  </div>
                  <div className="p-2.5 bg-slate-50 rounded-lg">
                    <span className="text-[11px] text-slate-500 block mb-0.5 flex items-center gap-1">
                      <Mail className="w-3 h-3" /> Email
                    </span>
                    <span className="font-bold text-slate-800 truncate block">
                      {emailDisplay}
                    </span>
                  </div>
                  <div className="p-2.5 bg-slate-50 rounded-lg">
                    <span className="text-[11px] text-slate-500 block mb-0.5 flex items-center gap-1">
                      <Briefcase className="w-3 h-3" /> Detected Exp
                    </span>
                    <span className="font-bold text-slate-800 truncate block">
                      {expDisplay}
                    </span>
                  </div>
                  <div className="p-2.5 bg-slate-50 rounded-lg">
                    <span className="text-[11px] text-slate-500 block mb-0.5 flex items-center gap-1">
                      <GraduationCap className="w-3 h-3" /> Education
                    </span>
                    <span className="font-bold text-slate-800 truncate block">
                      {eduDisplay}
                    </span>
                  </div>
                </div>

                {roleDisplay !== 'Not detected' && (
                  <div className="mt-3 p-2 bg-indigo-50/50 rounded-lg border border-indigo-100 flex items-center justify-between text-xs">
                    <span className="text-slate-600 flex items-center gap-1.5">
                      <Briefcase className="w-3.5 h-3.5 text-indigo-600" />
                      Detected Target Role: <strong className="text-slate-900">{roleDisplay}</strong>
                    </span>
                    <span className="text-[10px] text-indigo-600 font-semibold bg-indigo-100/70 px-2 py-0.5 rounded">
                      Identified from experience
                    </span>
                  </div>
                )}
              </Card>

              {/* Skills Extraction & Profile Comparison Card */}
              <Card>
                <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-3 border-b border-slate-200 gap-2">
                  <div>
                    <h3 className="text-sm font-bold text-slate-900">
                      Discovered Technical Skills ({extractedSkills.length})
                    </h3>
                    <p className="text-xs text-slate-500">
                      {newSkillsList.length} new skills discovered • {existingSkillsList.length} already in profile
                    </p>
                  </div>

                  <div className="flex items-center gap-2">
                    {newSkillsList.length > 0 && (
                      <Button
                        variant="outline"
                        size="xs"
                        onClick={handleSelectAllNew}
                      >
                        {selectedSkillsToApply.length === newSkillsList.length
                          ? 'Deselect All'
                          : 'Select All New'}
                      </Button>
                    )}
                    <Button
                      variant="primary"
                      size="sm"
                      icon={CheckCircle2}
                      disabled={selectedSkillsToApply.length === 0}
                      onClick={() => setShowConfirmModal(true)}
                    >
                      Sync to Profile ({selectedSkillsToApply.length})
                    </Button>
                  </div>
                </div>

                {/* Skills Grid */}
                <div className="pt-3 space-y-4">
                  {/* Section 1: New Skills (Not in Profile) */}
                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                      <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider">
                        New Skills Discovered ({newSkillsList.length})
                      </h4>
                    </div>

                    {newSkillsList.length === 0 ? (
                      <p className="text-xs text-slate-400 italic">All skills in this resume are already added to your profile.</p>
                    ) : (
                      <div className="grid grid-cols-1 sm:grid-cols-2 gap-2">
                        {extractedSkills
                          .filter((s) => newSkillsList.includes(s.name))
                          .map((skill) => {
                            const isSelected = selectedSkillsToApply.includes(skill.name);
                            return (
                              <div
                                key={skill.name}
                                onClick={() => toggleSkillSelection(skill.name)}
                                className={`p-2.5 rounded-lg border text-xs cursor-pointer transition-all flex items-start gap-2.5 ${
                                  isSelected
                                    ? 'border-emerald-500 bg-emerald-50/50 shadow-sm'
                                    : 'border-slate-200 hover:border-slate-300 bg-white'
                                }`}
                              >
                                <input
                                  type="checkbox"
                                  checked={isSelected}
                                  onChange={() => {}}
                                  className="mt-0.5 h-3.5 w-3.5 text-emerald-600 rounded border-slate-300"
                                />
                                <div className="space-y-0.5 overflow-hidden">
                                  <div className="flex items-center gap-2">
                                    <span className="font-bold text-slate-900">{skill.name}</span>
                                    <span className="text-[10px] px-1.5 py-0.2 bg-emerald-100 text-emerald-700 font-semibold rounded">
                                      {skill.confidence}% match
                                    </span>
                                  </div>
                                  {skill.snippet && (
                                    <p className="text-[10px] text-slate-500 line-clamp-1 italic">
                                      "{skill.snippet}"
                                    </p>
                                  )}
                                </div>
                              </div>
                            );
                          })}
                      </div>
                    )}
                  </div>

                  {/* Section 2: Already in Profile */}
                  {existingSkillsList.length > 0 && (
                    <div className="pt-2 border-t border-slate-100">
                      <div className="flex items-center gap-2 mb-2">
                        <span className="w-2 h-2 rounded-full bg-slate-400"></span>
                        <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider">
                          Already in Profile ({existingSkillsList.length})
                        </h4>
                      </div>
                      <div className="flex flex-wrap gap-1.5">
                        {existingSkillsList.map((name) => (
                          <span
                            key={name}
                            className="text-xs px-2.5 py-1 bg-slate-100 text-slate-600 rounded-full border border-slate-200"
                          >
                            ✓ {name}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </Card>

              {/* Action Buttons to navigate to other features */}
              <div className="flex flex-col sm:flex-row items-center justify-between p-4 bg-indigo-50/50 border border-indigo-100 rounded-xl gap-3">
                <div className="text-xs text-indigo-950">
                  <span className="font-bold">Next Recommended Action:</span>
                  <p>Run a salary analysis or check role matching with your newly identified skills.</p>
                </div>
                <div className="flex items-center gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => navigate('/what-if-simulator')}
                  >
                    Simulate Salary
                  </Button>
                  <Button
                    variant="primary"
                    size="sm"
                    icon={ArrowRight}
                    onClick={() => navigate('/role-matching')}
                  >
                    View Matching Roles
                  </Button>
                </div>
              </div>
            </>
          )}

        </div>

      </div>

      {/* Profile Sync Confirmation Modal */}
      {showConfirmModal && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-4">
            <div className="flex items-center gap-2 border-b border-slate-100 pb-3">
              <ShieldCheck className="w-6 h-6 text-indigo-600" />
              <h3 className="text-base font-bold text-slate-900">
                Confirm Profile Synchronization
              </h3>
            </div>

            <p className="text-xs text-slate-600 leading-relaxed">
              You are about to add <strong className="text-slate-900">{selectedSkillsToApply.length} verified technical skills</strong> to your candidate profile.
            </p>

            <div className="max-h-32 overflow-y-auto p-2 bg-slate-50 rounded-lg border border-slate-200 flex flex-wrap gap-1">
              {selectedSkillsToApply.map((sk) => (
                <span key={sk} className="text-[11px] bg-white border border-slate-300 px-2 py-0.5 rounded text-slate-800">
                  {sk}
                </span>
              ))}
            </div>

            {/* Optional Metadata Updates */}
            <div className="space-y-2 pt-2 border-t border-slate-100">
              <span className="text-xs font-bold text-slate-800 block">
                Additional Profile Sync Options:
              </span>

              {expValue != null && (
                <label className="flex items-center gap-2 text-xs text-slate-700 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={applyExp}
                    onChange={(e) => setApplyExp(e.target.checked)}
                    className="rounded border-slate-300 text-indigo-600"
                  />
                  <span>
                    Update years of experience to <strong className="text-indigo-600">{expValue} yrs</strong> (current: {profile?.years_of_experience || '0'} yrs)
                  </span>
                </label>
              )}

              {candidateInfo.education && (
                <label className="flex items-center gap-2 text-xs text-slate-700 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={applyEdu}
                    onChange={(e) => setApplyEdu(e.target.checked)}
                    className="rounded border-slate-300 text-indigo-600"
                  />
                  <span>
                    Update education level to <strong className="text-indigo-600">{candidateInfo.education}</strong>
                  </span>
                </label>
              )}

              {candidateInfo.detected_role && (
                <label className="flex items-center gap-2 text-xs text-slate-700 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={applyRole}
                    onChange={(e) => setApplyRole(e.target.checked)}
                    className="rounded border-slate-300 text-indigo-600"
                  />
                  <span>
                    Update primary role to <strong className="text-indigo-600">{candidateInfo.detected_role}</strong>
                  </span>
                </label>
              )}
            </div>

            <div className="flex items-center justify-end gap-2 pt-4 border-t border-slate-100">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setShowConfirmModal(false)}
                disabled={applying}
              >
                Cancel
              </Button>
              <Button
                variant="primary"
                size="sm"
                icon={Check}
                onClick={handleConfirmApply}
                isLoading={applying}
              >
                Confirm & Update Profile
              </Button>
            </div>
          </div>
        </div>
      )}

    </div>
  );
};

export default ResumeAnalysisPage;
