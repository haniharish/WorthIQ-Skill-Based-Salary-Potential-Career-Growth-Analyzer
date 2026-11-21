import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { profileService } from '../services/profileService';
import { Logo } from '../components/common/Logo';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { Badge } from '../components/ui/Badge';
import {
  Briefcase,
  Clock,
  MapPin,
  GraduationCap,
  IndianRupee,
  Sparkles,
  Plus,
  X,
  AlertCircle,
  CheckCircle2,
  ArrowRight,
  Layers,
} from 'lucide-react';

const COMMON_ROLES = [
  'Full Stack Developer',
  'Frontend Developer',
  'Backend Developer',
  'Data Scientist',
  'Machine Learning Engineer',
  'DevOps Engineer',
  'Cloud Architect',
  'Mobile Developer',
  'Software Engineer',
];

const COMMON_EDUCATION = [
  'B.Tech / B.E. in Computer Science',
  'B.Tech / B.E. (Other Branch)',
  'M.Tech / M.E. in CS/IT',
  'MCA / M.Sc Computer Science',
  'BCA / B.Sc Computer Science',
  "Master's Degree",
  "Bachelor's Degree",
  'Self-Taught / Bootcamp',
];

const POPULAR_SKILLS = [
  'Python', 'Django', 'React.js', 'JavaScript', 'TypeScript',
  'Node.js', 'PostgreSQL', 'Docker', 'AWS', 'REST APIs',
  'Tailwind CSS', 'Git', 'MongoDB', 'Machine Learning', 'Linux',
  'FastAPI', 'GraphQL', 'Next.js', 'Redis', 'SQL'
];

export const ProfileSetupPage = () => {
  const { user, profile, refreshUserProfile } = useAuth();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    job_role: '',
    years_of_experience: '1',
    location: '',
    education: '',
    current_salary: '',
  });

  const [selectedSkills, setSelectedSkills] = useState([]);
  const [skillInput, setSkillInput] = useState('');
  const [availableSkills, setAvailableSkills] = useState([]);
  const [errors, setErrors] = useState({});
  const [serverError, setServerError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isFetching, setIsFetching] = useState(true);

  // Load existing profile or suggestions on mount
  useEffect(() => {
    const loadInitialData = async () => {
      try {
        // Fetch skill suggestions
        const skillsData = await profileService.getSkills();
        setAvailableSkills(skillsData.map((s) => s.name));

        // Check if user already has profile
        const existingProfile = await profileService.getProfile();
        if (existingProfile) {
          setFormData({
            job_role: existingProfile.job_role || '',
            years_of_experience: existingProfile.years_of_experience?.toString() || '0',
            location: existingProfile.location || '',
            education: existingProfile.education || '',
            current_salary: existingProfile.current_salary ? existingProfile.current_salary.toString() : '',
          });
          if (existingProfile.skills) {
            setSelectedSkills(existingProfile.skills.map((s) => s.name));
          }
        }
      } catch (err) {
        console.error('Error loading initial profile data:', err);
      } finally {
        setIsFetching(false);
      }
    };

    loadInitialData();
  }, []);

  const handleAddSkill = (skillName) => {
    const trimmed = skillName.trim();
    if (!trimmed) return;
    if (selectedSkills.some((s) => s.toLowerCase() === trimmed.toLowerCase())) {
      setSkillInput('');
      return;
    }
    setSelectedSkills([...selectedSkills, trimmed]);
    setSkillInput('');
    if (errors.skills) {
      setErrors((prev) => ({ ...prev, skills: '' }));
    }
  };

  const handleRemoveSkill = (skillToRemove) => {
    setSelectedSkills(selectedSkills.filter((s) => s !== skillToRemove));
  };

  const handleSkillInputKeyDown = (e) => {
    if (e.key === 'Enter' || e.key === ',') {
      e.preventDefault();
      handleAddSkill(skillInput);
    }
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.job_role.trim()) {
      newErrors.job_role = 'Target or current job role is required.';
    }

    const exp = parseFloat(formData.years_of_experience);
    if (isNaN(exp) || exp < 0) {
      newErrors.years_of_experience = 'Please enter a valid number of years (0 for freshers).';
    } else if (exp > 60) {
      newErrors.years_of_experience = 'Experience cannot exceed 60 years.';
    }

    if (formData.current_salary) {
      const salary = parseFloat(formData.current_salary);
      if (isNaN(salary) || salary < 0) {
        newErrors.current_salary = 'Salary must be a positive number or left blank.';
      }
    }

    if (selectedSkills.length === 0) {
      newErrors.skills = 'Please add at least one technical skill to calibrate salary modeling.';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    setIsLoading(true);
    setServerError('');
    setSuccessMessage('');

    const payload = {
      job_role: formData.job_role.trim(),
      years_of_experience: parseFloat(formData.years_of_experience),
      location: formData.location.trim(),
      education: formData.education.trim(),
      current_salary: formData.current_salary ? parseFloat(formData.current_salary) : null,
      skills_input: selectedSkills,
    };

    try {
      if (profile) {
        await profileService.updateProfile(payload);
      } else {
        await profileService.createProfile(payload);
      }

      await refreshUserProfile();
      setSuccessMessage('Profile saved successfully! Redirecting to your analytics dashboard...');
      setTimeout(() => {
        navigate('/dashboard');
      }, 1000);
    } catch (err) {
      console.error('Save profile error:', err);
      if (err.response?.data) {
        const data = err.response.data;
        if (typeof data === 'string') {
          setServerError(data);
        } else if (data.detail) {
          setServerError(data.detail);
        } else {
          setServerError('Could not save profile. Please review the highlighted fields.');
        }
      } else {
        setServerError('Network error connecting to backend server.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col py-10 px-4 sm:px-6 lg:px-8 antialiased">
      <div className="max-w-3xl mx-auto w-full">
        {/* Header */}
        <div className="text-center mb-8">
          <Logo size="md" to="/dashboard" />
          <h1 className="mt-4 text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Configure Your Career Profile
          </h1>
          <p className="mt-2 text-xs sm:text-sm text-slate-600 max-w-lg mx-auto">
            Provide your skill stack and professional background to unlock precise market valuation and career roadmaps.
          </p>
        </div>

        {/* Form Container */}
        <div className="bg-white rounded-2xl border border-slate-200/90 shadow-sm p-6 sm:p-10">
          {serverError && (
            <div className="mb-6 p-3.5 rounded-xl bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-start gap-2.5">
              <AlertCircle className="w-4 h-4 shrink-0 mt-0.5 text-rose-500" />
              <span>{serverError}</span>
            </div>
          )}

          {successMessage && (
            <div className="mb-6 p-3.5 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs flex items-start gap-2.5">
              <CheckCircle2 className="w-4 h-4 shrink-0 mt-0.5 text-emerald-600" />
              <span>{successMessage}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6" noValidate>
            {/* Job Role with Quick Presets */}
            <div>
              <Input
                label="Target or Current Job Role"
                name="job_role"
                type="text"
                placeholder="e.g. Full Stack Developer"
                icon={Briefcase}
                value={formData.job_role}
                onChange={(e) => setFormData({ ...formData, job_role: e.target.value })}
                error={errors.job_role}
                required
              />
              <div className="mt-2 flex flex-wrap items-center gap-1.5">
                <span className="text-[11px] text-slate-400 font-medium">Suggestions:</span>
                {COMMON_ROLES.slice(0, 5).map((role) => (
                  <button
                    key={role}
                    type="button"
                    onClick={() => setFormData({ ...formData, job_role: role })}
                    className="text-[11px] px-2 py-0.5 rounded-md bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium transition-colors cursor-pointer"
                  >
                    {role}
                  </button>
                ))}
              </div>
            </div>

            {/* Experience and Current Salary */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
              <div>
                <Input
                  label="Years of Experience"
                  name="years_of_experience"
                  type="number"
                  step="0.5"
                  min="0"
                  max="60"
                  placeholder="0 (Fresher) or years"
                  icon={Clock}
                  value={formData.years_of_experience}
                  onChange={(e) => setFormData({ ...formData, years_of_experience: e.target.value })}
                  error={errors.years_of_experience}
                  required
                />
                <div className="mt-2 flex items-center gap-1.5">
                  <span className="text-[11px] text-slate-400">Quick select:</span>
                  {['0', '1', '2', '3', '5', '8+'].map((yr) => (
                    <button
                      key={yr}
                      type="button"
                      onClick={() => setFormData({ ...formData, years_of_experience: yr.replace('+', '') })}
                      className={`text-[11px] px-2 py-0.5 rounded-md font-medium transition-colors cursor-pointer ${
                        formData.years_of_experience === yr.replace('+', '')
                          ? 'bg-indigo-600 text-white'
                          : 'bg-slate-100 hover:bg-slate-200 text-slate-700'
                      }`}
                    >
                      {yr} {yr === '0' ? '(Fresher)' : 'yrs'}
                    </button>
                  ))}
                </div>
              </div>

              <div>
                <Input
                  label="Current Salary (Optional, LPA)"
                  name="current_salary"
                  type="number"
                  step="0.1"
                  min="0"
                  placeholder="e.g. 6.5 (in Lakhs Per Annum)"
                  icon={IndianRupee}
                  value={formData.current_salary}
                  onChange={(e) => setFormData({ ...formData, current_salary: e.target.value })}
                  error={errors.current_salary}
                  helperText="Kept private; used for personal salary variance & growth calculation"
                />
              </div>
            </div>

            {/* Location & Education */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
              <Input
                label="Location / City"
                name="location"
                type="text"
                placeholder="e.g. Bengaluru, India or Remote"
                icon={MapPin}
                value={formData.location}
                onChange={(e) => setFormData({ ...formData, location: e.target.value })}
              />

              <div>
                <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
                  Education Background
                </label>
                <div className="relative">
                  <select
                    value={formData.education}
                    onChange={(e) => setFormData({ ...formData, education: e.target.value })}
                    className="w-full rounded-lg text-sm text-slate-900 bg-white border border-slate-300 py-2.5 px-3.5 focus:border-indigo-600 focus:ring-3 focus:ring-indigo-600/15 outline-none transition-all"
                  >
                    <option value="">Select qualification...</option>
                    {COMMON_EDUCATION.map((edu) => (
                      <option key={edu} value={edu}>
                        {edu}
                      </option>
                    ))}
                  </select>
                </div>
              </div>
            </div>

            {/* Technical Skills Section */}
            <div className="pt-2">
              <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
                Technical Skills <span className="text-rose-500">*</span>
              </label>
              <p className="text-xs text-slate-500 mb-3">
                Add the technologies, languages, frameworks and databases you work with.
              </p>

              {/* Skills Input Bar */}
              <div className="flex gap-2">
                <input
                  type="text"
                  placeholder="Type a skill (e.g. Python, React, PostgreSQL) and press Enter"
                  value={skillInput}
                  onChange={(e) => setSkillInput(e.target.value)}
                  onKeyDown={handleSkillInputKeyDown}
                  className="flex-1 rounded-lg text-sm text-slate-900 bg-white border border-slate-300 py-2 px-3.5 focus:border-indigo-600 focus:ring-3 focus:ring-indigo-600/15 outline-none transition-all"
                />
                <Button
                  type="button"
                  variant="secondary"
                  size="md"
                  icon={Plus}
                  onClick={() => handleAddSkill(skillInput)}
                >
                  Add
                </Button>
              </div>

              {errors.skills && (
                <p className="mt-1.5 text-xs text-rose-600 font-medium">{errors.skills}</p>
              )}

              {/* Selected Skills Chips */}
              <div className="mt-4 p-4 rounded-xl bg-slate-50 border border-slate-200/80 min-h-[80px]">
                <div className="flex items-center justify-between pb-2 mb-2 border-b border-slate-200/60">
                  <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider">
                    Selected Skills ({selectedSkills.length})
                  </span>
                  {selectedSkills.length > 0 && (
                    <button
                      type="button"
                      onClick={() => setSelectedSkills([])}
                      className="text-[11px] text-rose-600 hover:text-rose-700 font-medium"
                    >
                      Clear all
                    </button>
                  )}
                </div>

                {selectedSkills.length === 0 ? (
                  <p className="text-xs text-slate-400 italic py-2">
                    No skills added yet. Click on suggestions below or type custom skills above.
                  </p>
                ) : (
                  <div className="flex flex-wrap gap-2">
                    {selectedSkills.map((skill) => (
                      <span
                        key={skill}
                        className="inline-flex items-center gap-1.5 px-3 py-1 rounded-lg bg-indigo-50 border border-indigo-200 text-indigo-700 text-xs font-semibold shadow-2xs"
                      >
                        {skill}
                        <button
                          type="button"
                          onClick={() => handleRemoveSkill(skill)}
                          className="hover:text-indigo-900 cursor-pointer"
                        >
                          <X className="w-3.5 h-3.5" />
                        </button>
                      </span>
                    ))}
                  </div>
                )}
              </div>

              {/* Quick Add Suggestions */}
              <div className="mt-4">
                <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider mb-2">
                  Popular Technical Skills:
                </p>
                <div className="flex flex-wrap gap-1.5">
                  {POPULAR_SKILLS.map((skill) => {
                    const isSelected = selectedSkills.some((s) => s.toLowerCase() === skill.toLowerCase());
                    return (
                      <button
                        key={skill}
                        type="button"
                        disabled={isSelected}
                        onClick={() => handleAddSkill(skill)}
                        className={`text-xs px-2.5 py-1 rounded-lg font-medium transition-all ${
                          isSelected
                            ? 'bg-slate-100 text-slate-400 border border-slate-200 cursor-not-allowed'
                            : 'bg-white hover:bg-indigo-50 text-slate-700 hover:text-indigo-700 border border-slate-200 hover:border-indigo-300 cursor-pointer shadow-2xs'
                        }`}
                      >
                        + {skill}
                      </button>
                    );
                  })}
                </div>
              </div>
            </div>

            {/* Submit Action */}
            <div className="pt-6 border-t border-slate-200 flex flex-col sm:flex-row items-center justify-between gap-4">
              <p className="text-xs text-slate-500 text-center sm:text-left">
                Your profile updates the PostgreSQL database in real-time.
              </p>
              <div className="flex items-center gap-3 w-full sm:w-auto">
                <Button
                  type="submit"
                  variant="primary"
                  size="md"
                  className="w-full sm:w-auto"
                  isLoading={isLoading}
                  iconRight={ArrowRight}
                >
                  Save Profile & View Dashboard
                </Button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ProfileSetupPage;
