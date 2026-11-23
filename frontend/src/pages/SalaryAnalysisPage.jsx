import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  TrendingUp,
  Sparkles,
  Award,
  AlertCircle,
  CheckCircle2,
  HelpCircle,
  ArrowRight,
  RefreshCw,
  Plus,
  X,
  UserCheck,
  ChevronDown,
  ChevronUp,
  Briefcase,
  MapPin,
  GraduationCap,
  Clock,
  BarChart3,
  Layers,
  Zap,
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell,
  ReferenceLine,
  CartesianGrid,
} from 'recharts';
import { Card, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Input } from '../components/ui/Input';
import { useAuth } from '../context/AuthContext';
import { predictionService } from '../services/predictionService';

const SUPPORTED_ROLES = [
  'Software Developer',
  'Full Stack Developer',
  'Backend Developer',
  'Frontend Developer',
  'Data Scientist',
  'Data Analyst',
  'DevOps Engineer',
  'Machine Learning Engineer',
];

const SUPPORTED_LOCATIONS = [
  'Bengaluru',
  'Hyderabad',
  'Pune',
  'Chennai',
  'Mumbai',
  'Delhi NCR',
  'Remote',
  'Other',
];

const SUPPORTED_EDUCATIONS = [
  "Bachelor's Degree",
  "Master's Degree",
  'PhD',
  'Diploma',
  'Other',
];

const POPULAR_SKILLS = [
  'Python',
  'JavaScript',
  'React.js',
  'Node.js',
  'SQL',
  'Docker',
  'AWS',
  'Django',
  'TypeScript',
  'Java',
  'Git',
  'Kubernetes',
  'MongoDB',
  'PostgreSQL',
  'Machine Learning',
  'Scikit-learn',
  'Pandas',
  'FastAPI',
  'Next.js',
  'Redis',
  'Linux',
  'Spring Boot',
  'Tailwind CSS',
  'Microservices',
];

export const SalaryAnalysisPage = () => {
  const { profile } = useAuth();

  // Form State
  const [formData, setFormData] = useState({
    job_role: 'Full Stack Developer',
    years_of_experience: '3',
    location: 'Bengaluru',
    education: "Bachelor's Degree",
    skills: ['JavaScript', 'React.js', 'Node.js', 'PostgreSQL', 'Git'],
  });

  const [skillInput, setSkillInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [predictionResult, setPredictionResult] = useState(null);
  const [showConfidenceDetails, setShowConfidenceDetails] = useState(false);
  const [prefilledFromProfile, setPrefilledFromProfile] = useState(false);

  // Auto-prefill if profile is available
  useEffect(() => {
    if (profile && !prefilledFromProfile) {
      prefillWithProfile();
    }
  }, [profile]);

  const prefillWithProfile = () => {
    if (!profile) return;
    const profileSkills = Array.isArray(profile.skills)
      ? profile.skills.map((s) => (typeof s === 'string' ? s : s.name))
      : [];

    setFormData((prev) => ({
      ...prev,
      job_role: profile.job_role || prev.job_role,
      years_of_experience:
        profile.years_of_experience !== undefined && profile.years_of_experience !== null
          ? String(profile.years_of_experience)
          : prev.years_of_experience,
      location: profile.location || prev.location,
      education: profile.education || prev.education,
      skills: profileSkills.length > 0 ? profileSkills : prev.skills,
    }));
    setPrefilledFromProfile(true);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const handleAddSkill = (skillToAdd) => {
    const trimmed = (skillToAdd || skillInput).trim();
    if (!trimmed) return;
    if (formData.skills.some((s) => s.toLowerCase() === trimmed.toLowerCase())) {
      setSkillInput('');
      return;
    }
    setFormData((prev) => ({
      ...prev,
      skills: [...prev.skills, trimmed],
    }));
    setSkillInput('');
  };

  const handleRemoveSkill = (skillToRemove) => {
    setFormData((prev) => ({
      ...prev,
      skills: prev.skills.filter((s) => s !== skillToRemove),
    }));
  };

  const handleKeyDownSkill = (e) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddSkill();
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    const expNum = parseFloat(formData.years_of_experience);
    if (isNaN(expNum) || expNum < 0 || expNum > 45) {
      setError('Please provide a valid years of experience between 0 and 45.');
      return;
    }

    setLoading(true);
    try {
      const payload = {
        job_role: formData.job_role,
        years_of_experience: expNum,
        location: formData.location,
        education: formData.education,
        skills: formData.skills,
      };

      const result = await predictionService.createSalaryPrediction(payload);
      setPredictionResult(result);

      // Scroll to results
      setTimeout(() => {
        const el = document.getElementById('prediction-results-section');
        if (el) el.scrollIntoView({ behavior: 'smooth' });
      }, 100);
    } catch (err) {
      console.error('Prediction failed:', err);
      const serverMsg =
        err.response?.data?.detail ||
        (err.response?.data && typeof err.response.data === 'object'
          ? Object.values(err.response.data).flat().join(', ')
          : null);
      setError(serverMsg || 'Failed to generate salary prediction. Please check your inputs and try again.');
    } finally {
      setLoading(false);
    }
  };

  // Recharts Chart Data preparation
  const chartData = predictionResult
    ? [
        {
          name: 'Conservative (P10)',
          salary: Math.round(predictionResult.salary_range.p10_annual / 1000) * 1000,
          lpa: predictionResult.salary_range.p10_lpa,
          fill: '#94a3b8',
        },
        {
          name: 'Target Median (P50)',
          salary: Math.round(predictionResult.predicted_salary_annual / 1000) * 1000,
          lpa: predictionResult.predicted_salary_lpa,
          fill: '#4f46e5',
        },
        {
          name: 'Top Tier (P90)',
          salary: Math.round(predictionResult.salary_range.p90_annual / 1000) * 1000,
          lpa: predictionResult.salary_range.p90_lpa,
          fill: '#10b981',
        },
      ]
    : [];

  const getConfidenceBadgeColor = (level) => {
    switch (level?.toLowerCase()) {
      case 'high':
        return 'emerald';
      case 'medium':
        return 'indigo';
      case 'low':
      default:
        return 'amber';
    }
  };

  return (
    <div className="space-y-8 max-w-6xl mx-auto pb-12">
      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-2 border-b border-slate-200">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-slate-900">
              Salary Potential Prediction Engine
            </h1>
            <Badge variant="emerald" size="xs" dot>
              ML Model v2.0
            </Badge>
          </div>
          <p className="text-sm text-slate-600">
            Multi-variable quantile regression trained on 20,265 verified Indian technology compensation records.
          </p>
        </div>

        <div className="flex items-center gap-3">
          {profile && (
            <Button
              variant="outline"
              size="sm"
              icon={UserCheck}
              onClick={prefillWithProfile}
              className="text-xs"
            >
              Sync Profile Data
            </Button>
          )}
          <Link to="/saved-reports">
            <Button variant="ghost" size="sm" icon={Layers} className="text-xs">
              View History
            </Button>
          </Link>
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-sm flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
          <div className="flex-1">
            <p className="font-semibold">Prediction Error</p>
            <p className="text-rose-700 text-xs mt-0.5">{error}</p>
          </div>
        </div>
      )}

      {/* Main Grid: Input Form & Quick Tips */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Form Column (Span 2) */}
        <div className="lg:col-span-2 space-y-6">
          <Card className="p-6">
            <CardHeader
              title="Career Parameters & Skill Profile"
              subtitle="Configure your target role, experience, and technical skill set to generate salary predictions."
              icon={TrendingUp}
            />

            <form onSubmit={handleSubmit} className="space-y-5">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Job Role */}
                <div>
                  <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
                    Target Job Role <span className="text-rose-500">*</span>
                  </label>
                  <div className="relative">
                    <select
                      name="job_role"
                      value={formData.job_role}
                      onChange={handleInputChange}
                      className="w-full rounded-lg text-sm text-slate-900 bg-white border border-slate-300 py-2.5 px-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                    >
                      {SUPPORTED_ROLES.map((role) => (
                        <option key={role} value={role}>
                          {role}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                {/* Years of Experience */}
                <div>
                  <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
                    Years of Experience <span className="text-rose-500">*</span>
                  </label>
                  <div className="relative">
                    <input
                      type="number"
                      step="0.5"
                      min="0"
                      max="45"
                      name="years_of_experience"
                      value={formData.years_of_experience}
                      onChange={handleInputChange}
                      placeholder="e.g. 3.5"
                      className="w-full rounded-lg text-sm text-slate-900 bg-white border border-slate-300 py-2 px-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                      required
                    />
                  </div>
                  <span className="text-[11px] text-slate-500 mt-1 block">
                    Use 0 for fresh graduates / entry-level roles.
                  </span>
                </div>

                {/* Location */}
                <div>
                  <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
                    Job Location <span className="text-rose-500">*</span>
                  </label>
                  <select
                    name="location"
                    value={formData.location}
                    onChange={handleInputChange}
                    className="w-full rounded-lg text-sm text-slate-900 bg-white border border-slate-300 py-2.5 px-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  >
                    {SUPPORTED_LOCATIONS.map((loc) => (
                      <option key={loc} value={loc}>
                        {loc}
                      </option>
                    ))}
                  </select>
                </div>

                {/* Education */}
                <div>
                  <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-1.5">
                    Highest Education
                  </label>
                  <select
                    name="education"
                    value={formData.education}
                    onChange={handleInputChange}
                    className="w-full rounded-lg text-sm text-slate-900 bg-white border border-slate-300 py-2.5 px-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                  >
                    {SUPPORTED_EDUCATIONS.map((edu) => (
                      <option key={edu} value={edu}>
                        {edu}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              {/* Skills Multi-Select / Tag Selector */}
              <div>
                <div className="flex items-center justify-between mb-1.5">
                  <label className="text-xs font-semibold text-slate-700 uppercase tracking-wider">
                    Technical Skills ({formData.skills.length} selected)
                  </label>
                  <span className="text-xs text-indigo-600 font-medium">
                    Skills directly boost prediction accuracy
                  </span>
                </div>

                {/* Selected Skill Chips */}
                <div className="flex flex-wrap gap-2 p-3 rounded-lg border border-slate-200 bg-slate-50/50 min-h-[48px] mb-3">
                  {formData.skills.length === 0 ? (
                    <span className="text-xs text-slate-400 italic py-1">
                      No skills added yet. Pick from the suggestions below or type your own.
                    </span>
                  ) : (
                    formData.skills.map((skill) => (
                      <span
                        key={skill}
                        className="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-xs font-medium bg-indigo-50 text-indigo-700 border border-indigo-200/80 shadow-2xs group"
                      >
                        {skill}
                        <button
                          type="button"
                          onClick={() => handleRemoveSkill(skill)}
                          className="text-indigo-400 hover:text-indigo-700 rounded transition-colors"
                        >
                          <X className="w-3 h-3" />
                        </button>
                      </span>
                    ))
                  )}
                </div>

                {/* Custom Skill Input */}
                <div className="flex gap-2 mb-3">
                  <input
                    type="text"
                    value={skillInput}
                    onChange={(e) => setSkillInput(e.target.value)}
                    onKeyDown={handleKeyDownSkill}
                    placeholder="Type a skill (e.g. FastAPI, Kubernetes, GraphQL) and press Enter..."
                    className="flex-1 rounded-lg text-sm text-slate-900 bg-white border border-slate-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                  <Button
                    type="button"
                    variant="secondary"
                    size="md"
                    icon={Plus}
                    onClick={() => handleAddSkill()}
                  >
                    Add
                  </Button>
                </div>

                {/* Suggested Quick Add Chips */}
                <div>
                  <p className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider mb-2">
                    Popular In-Demand Skills (Click to add):
                  </p>
                  <div className="flex flex-wrap gap-1.5">
                    {POPULAR_SKILLS.filter(
                      (ps) => !formData.skills.some((s) => s.toLowerCase() === ps.toLowerCase())
                    ).map((skill) => (
                      <button
                        key={skill}
                        type="button"
                        onClick={() => handleAddSkill(skill)}
                        className="text-xs px-2.5 py-1 rounded-full bg-white text-slate-600 border border-slate-200 hover:border-indigo-300 hover:bg-indigo-50 hover:text-indigo-600 transition-colors cursor-pointer"
                      >
                        + {skill}
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              {/* Action Submit */}
              <div className="pt-4 border-t border-slate-100 flex items-center justify-between">
                <p className="text-xs text-slate-500 flex items-center gap-1.5">
                  <Sparkles className="w-4 h-4 text-indigo-500" />
                  Instant ML evaluation with P10, P50, and P90 quantiles
                </p>

                <Button
                  type="submit"
                  variant="primary"
                  size="lg"
                  isLoading={loading}
                  icon={TrendingUp}
                  className="px-6"
                >
                  {loading ? 'Evaluating Model...' : 'Predict Salary Potential'}
                </Button>
              </div>
            </form>
          </Card>
        </div>

        {/* Sidebar Info Column */}
        <div className="space-y-6">
          <Card className="p-6 bg-gradient-to-br from-indigo-900 to-slate-900 text-white border-indigo-950">
            <div className="flex items-center gap-2 mb-3">
              <div className="p-2 rounded-lg bg-indigo-500/20 text-indigo-300">
                <Award className="w-5 h-5" />
              </div>
              <h3 className="font-semibold text-white text-base">Model Architecture</h3>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed mb-4">
              WorthIQ utilizes a Random Forest Regressor calibrated with quantile loss models for compensation estimation.
            </p>

            <div className="space-y-3 pt-3 border-t border-slate-800 text-xs text-slate-300">
              <div className="flex justify-between">
                <span className="text-slate-400">Trained Samples:</span>
                <span className="font-medium text-white">20,265 Tech Profiles</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Features Vector:</span>
                <span className="font-medium text-white">55 Engineered Dimensions</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Cross-Validation MAE:</span>
                <span className="font-medium text-emerald-400">₹3.35 Lakhs</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-400">Quantile Spread:</span>
                <span className="font-medium text-indigo-300">P10, P50, P90</span>
              </div>
            </div>
          </Card>

          <Card className="p-5">
            <h4 className="text-xs font-semibold text-slate-900 uppercase tracking-wider mb-2 flex items-center gap-1.5">
              <Zap className="w-4 h-4 text-amber-500" />
              Tips for Higher Accuracy
            </h4>
            <ul className="text-xs text-slate-600 space-y-2">
              <li className="flex items-start gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 shrink-0 mt-0.5" />
                <span>Specify at least 4–6 verified technical skills to maximize confidence.</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 shrink-0 mt-0.5" />
                <span>Ensure your experience matches full-time industry tenure.</span>
              </li>
              <li className="flex items-start gap-2">
                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-500 shrink-0 mt-0.5" />
                <span>Select Tier-1 tech hubs (Bengaluru, Hyderabad, Pune) for localized cost indexes.</span>
              </li>
            </ul>
          </Card>
        </div>
      </div>

      {/* Prediction Results Section */}
      {predictionResult && (
        <div id="prediction-results-section" className="space-y-6 pt-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <h2 className="text-xl sm:text-2xl font-bold text-slate-900">
                Salary Prediction Results
              </h2>
              <Badge variant={getConfidenceBadgeColor(predictionResult.confidence_level)} dot>
                {predictionResult.confidence_level} Confidence ({predictionResult.confidence_score}%)
              </Badge>
            </div>

            <div className="text-xs text-slate-500">
              Evaluated on {new Date(predictionResult.created_at).toLocaleDateString('en-IN', {
                day: 'numeric',
                month: 'short',
                year: 'numeric',
              })}
            </div>
          </div>

          {/* Headline Metric Card */}
          <Card className="p-6 sm:p-8 bg-gradient-to-r from-indigo-50 via-white to-slate-50 border-indigo-200">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-center">
              {/* Primary Median */}
              <div className="lg:col-span-2 space-y-2">
                <span className="text-xs font-bold text-indigo-600 uppercase tracking-wider">
                  Target Market Compensation (Median P50)
                </span>
                <div className="flex flex-wrap items-baseline gap-3">
                  <span className="text-4xl sm:text-5xl font-extrabold text-slate-900 tracking-tight">
                    {predictionResult.predicted_salary_formatted}
                  </span>
                  <span className="text-2xl font-semibold text-indigo-600">
                    ({predictionResult.predicted_salary_lpa} LPA)
                  </span>
                </div>
                <p className="text-sm text-slate-600 pt-1">
                  Estimated monthly gross:{' '}
                  <span className="font-semibold text-slate-900">
                    ₹{Math.round(predictionResult.predicted_salary_annual / 12).toLocaleString('en-IN')}{' '}
                    / month
                  </span>
                </p>
              </div>

              {/* Confidence Meter Box */}
              <div className="p-4 rounded-xl bg-white border border-slate-200/80 shadow-xs">
                <div className="flex items-center justify-between mb-2">
                  <span className="text-xs font-semibold text-slate-700">Model Reliability</span>
                  <Badge variant={getConfidenceBadgeColor(predictionResult.confidence_level)}>
                    {predictionResult.confidence_level}
                  </Badge>
                </div>
                <div className="w-full bg-slate-100 rounded-full h-2.5 mb-2 overflow-hidden">
                  <div
                    className={`h-2.5 rounded-full ${
                      predictionResult.confidence_level === 'High'
                        ? 'bg-emerald-500'
                        : predictionResult.confidence_level === 'Medium'
                        ? 'bg-indigo-500'
                        : 'bg-amber-500'
                    }`}
                    style={{ width: `${predictionResult.confidence_score}%` }}
                  />
                </div>
                <button
                  type="button"
                  onClick={() => setShowConfidenceDetails(!showConfidenceDetails)}
                  className="text-xs text-indigo-600 hover:text-indigo-800 flex items-center gap-1 font-medium cursor-pointer"
                >
                  {showConfidenceDetails ? 'Hide confidence factors' : 'Why this score?'}
                  {showConfidenceDetails ? (
                    <ChevronUp className="w-3.5 h-3.5" />
                  ) : (
                    <ChevronDown className="w-3.5 h-3.5" />
                  )}
                </button>
              </div>
            </div>

            {/* Expandable Confidence Factors */}
            {showConfidenceDetails && predictionResult.confidence_factors && (
              <div className="mt-6 pt-6 border-t border-slate-200 text-xs">
                <h4 className="font-semibold text-slate-800 mb-3 uppercase tracking-wider">
                  Confidence Evaluation Breakdown
                </h4>
                <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3">
                  {Object.entries(predictionResult.confidence_factors).map(([key, val]) => (
                    <div key={key} className="p-3 rounded-lg bg-slate-50 border border-slate-200">
                      <span className="text-[11px] text-slate-500 uppercase block capitalize">
                        {key.replace(/_/g, ' ')}
                      </span>
                      <span className="font-semibold text-slate-800 mt-0.5 block">{String(val)}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </Card>

          {/* Quantile Triad Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            {/* Conservative P10 */}
            <Card className="p-5 border-slate-200 bg-white">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">
                  10th Percentile (Floor)
                </span>
                <span className="text-xs px-2 py-0.5 rounded bg-slate-100 text-slate-600 font-medium">
                  Entry / Baseline
                </span>
              </div>
              <div className="text-2xl font-bold text-slate-800">
                {predictionResult.salary_range.p10_formatted}
              </div>
              <div className="text-sm font-semibold text-slate-500 mt-0.5">
                {predictionResult.salary_range.p10_lpa} LPA
              </div>
              <p className="text-xs text-slate-500 mt-3 pt-3 border-t border-slate-100">
                90% of peer professionals in this bracket earn above this compensation floor.
              </p>
            </Card>

            {/* Median P50 */}
            <Card className="p-5 border-indigo-300 bg-indigo-50/30 ring-2 ring-indigo-500/20">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-bold text-indigo-700 uppercase tracking-wider">
                  50th Percentile (Median)
                </span>
                <span className="text-xs px-2 py-0.5 rounded bg-indigo-100 text-indigo-700 font-semibold">
                  Market Target
                </span>
              </div>
              <div className="text-2xl font-bold text-indigo-900">
                {predictionResult.predicted_salary_formatted}
              </div>
              <div className="text-sm font-semibold text-indigo-600 mt-0.5">
                {predictionResult.predicted_salary_lpa} LPA
              </div>
              <p className="text-xs text-indigo-700/80 mt-3 pt-3 border-t border-indigo-100">
                Represents the exact central tendency of compensation for matching attributes.
              </p>
            </Card>

            {/* Optimistic P90 */}
            <Card className="p-5 border-emerald-200 bg-emerald-50/20">
              <div className="flex items-center justify-between mb-2">
                <span className="text-xs font-semibold text-emerald-800 uppercase tracking-wider">
                  90th Percentile (Ceiling)
                </span>
                <span className="text-xs px-2 py-0.5 rounded bg-emerald-100 text-emerald-700 font-medium">
                  Top Tier
                </span>
              </div>
              <div className="text-2xl font-bold text-emerald-950">
                {predictionResult.salary_range.p90_formatted}
              </div>
              <div className="text-sm font-semibold text-emerald-700 mt-0.5">
                {predictionResult.salary_range.p90_lpa} LPA
              </div>
              <p className="text-xs text-slate-500 mt-3 pt-3 border-t border-slate-100">
                Top 10% highest compensated candidates with elite product companies or niche skill depth.
              </p>
            </Card>
          </div>

          {/* Visual Range Chart with Recharts */}
          <Card className="p-6">
            <CardHeader
              title="Compensation Distribution & Percentile Spread"
              subtitle="Comparison of empirical compensation quantiles (P10, P50, P90) in INR Lakhs."
              icon={BarChart3}
            />

            <div className="h-64 w-full pt-4">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={chartData}
                  layout="vertical"
                  margin={{ top: 10, right: 30, left: 40, bottom: 10 }}
                >
                  <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#e2e8f0" />
                  <XAxis
                    type="number"
                    tickFormatter={(val) => `₹${(val / 100000).toFixed(1)}L`}
                    stroke="#64748b"
                    fontSize={12}
                  />
                  <YAxis
                    type="category"
                    dataKey="name"
                    stroke="#64748b"
                    fontSize={12}
                    width={140}
                  />
                  <Tooltip
                    formatter={(value) => [
                      `₹${(value / 100000).toFixed(2)} LPA (₹${Number(value).toLocaleString('en-IN')})`,
                      'Annual Salary',
                    ]}
                    contentStyle={{
                      backgroundColor: '#1e293b',
                      borderRadius: '8px',
                      color: '#fff',
                      fontSize: '12px',
                    }}
                  />
                  <Bar dataKey="salary" radius={[0, 6, 6, 0]} barSize={26}>
                    {chartData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.fill} />
                    ))}
                  </Bar>
                </BarChart>
              </ResponsiveContainer>
            </div>

            <div className="mt-4 pt-4 border-t border-slate-100 flex flex-wrap items-center justify-between text-xs text-slate-500 gap-2">
              <div className="flex items-center gap-4">
                <span className="flex items-center gap-1.5">
                  <span className="w-2.5 h-2.5 rounded-full bg-slate-400" /> P10 Conservative
                </span>
                <span className="flex items-center gap-1.5">
                  <span className="w-2.5 h-2.5 rounded-full bg-indigo-600" /> P50 Median Target
                </span>
                <span className="flex items-center gap-1.5">
                  <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" /> P90 Top Tier
                </span>
              </div>
              <div>
                Total Variance Range:{' '}
                <span className="font-semibold text-slate-700">
                  ₹{(
                    (predictionResult.salary_range.p90_annual -
                      predictionResult.salary_range.p10_annual) /
                    100000
                  ).toFixed(2)}{' '}
                  Lakhs
                </span>
              </div>
            </div>
          </Card>

          {/* Skill Attribution & Recommendations */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Current Contributing Skills */}
            <Card className="p-6">
              <div className="flex items-center gap-2 mb-3">
                <div className="p-2 rounded-lg bg-emerald-50 text-emerald-600">
                  <CheckCircle2 className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-semibold text-slate-900 text-sm">
                    Skills Powering Your Evaluation
                  </h3>
                  <p className="text-xs text-slate-500">
                    Recognized by the ML model with positive coefficient weights.
                  </p>
                </div>
              </div>

              <div className="flex flex-wrap gap-2 pt-2">
                {formData.skills.map((skill) => (
                  <span
                    key={skill}
                    className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200"
                  >
                    <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />
                    {skill}
                  </span>
                ))}
              </div>
            </Card>

            {/* Recommended High-Value Upskilling Skills */}
            <Card className="p-6">
              <div className="flex items-center gap-2 mb-3">
                <div className="p-2 rounded-lg bg-indigo-50 text-indigo-600">
                  <Sparkles className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-semibold text-slate-900 text-sm">
                    High-Value Target Skills to Acquire
                  </h3>
                  <p className="text-xs text-slate-500">
                    Highest marginal market premium for {formData.job_role}.
                  </p>
                </div>
              </div>

              <div className="flex flex-wrap gap-2 pt-2">
                {predictionResult.top_recommended_skills &&
                predictionResult.top_recommended_skills.length > 0 ? (
                  predictionResult.top_recommended_skills.map((recSkill) => (
                    <span
                      key={recSkill}
                      className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-indigo-50 text-indigo-800 border border-indigo-200"
                    >
                      <Plus className="w-3 h-3 text-indigo-600" />
                      {recSkill}
                      <span className="text-[10px] text-indigo-500 font-normal">
                        (+Premium)
                      </span>
                    </span>
                  ))
                ) : (
                  ['Docker', 'Kubernetes', 'AWS', 'System Design'].map((s) => (
                    <span
                      key={s}
                      className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-indigo-50 text-indigo-800 border border-indigo-200"
                    >
                      <Plus className="w-3 h-3 text-indigo-600" />
                      {s}
                    </span>
                  ))
                )}
              </div>
            </Card>
          </div>

          {/* Model Governance Footer & Disclaimer */}
          <div className="p-5 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-600 space-y-2">
            <div className="flex flex-wrap items-center justify-between gap-2 font-medium text-slate-700">
              <span className="flex items-center gap-1.5">
                <BarChart3 className="w-4 h-4 text-indigo-600" />
                Trained on 20,265 real Indian tech compensation profiles (Random Forest Regressor)
              </span>
              <span>Model ID: {predictionResult.model_version || '2.0.0'}</span>
            </div>
            <p className="text-slate-500 text-[11px] leading-relaxed">
              <strong className="text-slate-700">Methodological Disclaimer:</strong> Predictions
              represent parametric and non-parametric statistical expectations derived from industry compensation
              data. Individual offers may vary based on company tier, individual negotiation, interview performance,
              and equity components.
            </p>
            <div className="pt-2 flex flex-wrap items-center justify-between gap-3">
              <Link
                to={`/explanations/${predictionResult.id || predictionResult.prediction_id}`}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-indigo-600 text-white font-semibold text-xs hover:bg-indigo-700 transition-colors shadow-2xs"
              >
                <Sparkles className="w-3.5 h-3.5" /> View SHAP Explainability & Feature Impact
              </Link>
              <Link to="/saved-reports" className="text-indigo-600 hover:text-indigo-800 font-semibold inline-flex items-center gap-1">
                View all past predictions in Saved Reports <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SalaryAnalysisPage;
