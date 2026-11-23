import React, { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import {
  Briefcase,
  TrendingUp,
  Compass,
  CheckCircle2,
  AlertCircle,
  XCircle,
  Clock,
  Sparkles,
  RefreshCw,
  ArrowRight,
  Filter,
  Search,
  Award,
} from 'lucide-react';
import { Card, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { useAuth } from '../context/AuthContext';
import { intelligenceService } from '../services/intelligenceService';

export const JobMatchingPage = () => {
  const { profile } = useAuth();
  const navigate = useNavigate();

  const [matches, setMatches] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filterCategory, setFilterCategory] = useState('All');
  const [searchQuery, setSearchQuery] = useState('');

  const fetchMatches = async () => {
    setLoading(true);
    setError(null);
    try {
      const userSkills = profile?.skills
        ? profile.skills.map((s) => (typeof s === 'string' ? s : s.name))
        : [];
      const skills = userSkills.length > 0 ? userSkills : ['Python', 'SQL', 'Git', 'REST APIs'];
      const exp = profile?.years_of_experience ? parseFloat(profile.years_of_experience) : 2.0;

      const data = await intelligenceService.matchJobRoles(skills, exp);
      setMatches(data.matches || []);
    } catch (err) {
      console.error('Failed to match roles:', err);
      setError('Unable to calculate role matches. Please check your connection.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMatches();
  }, [profile]);

  const handleGenerateRoadmap = (roleId, roleTitle) => {
    navigate(`/career-roadmap?role_id=${roleId}&title=${encodeURIComponent(roleTitle)}`);
  };

  const getScoreBadge = (score, category) => {
    if (score >= 80) return <Badge variant="emerald" dot>{category} ({score}%)</Badge>;
    if (score >= 65) return <Badge variant="indigo" dot>{category} ({score}%)</Badge>;
    if (score >= 50) return <Badge variant="sky" dot>{category} ({score}%)</Badge>;
    return <Badge variant="amber" dot>{category} ({score}%)</Badge>;
  };

  const filteredMatches = matches.filter((m) => {
    const matchesCat = filterCategory === 'All Roles' || filterCategory === 'All' || m.match_category === filterCategory;
    const matchesSearch =
      !searchQuery ||
      m.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      m.description.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesCat && matchesSearch;
  });

  return (
    <div className="space-y-8 max-w-6xl mx-auto pb-12">
      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-2 border-b border-slate-200">
        <div>
          <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-slate-900 mb-1">
            Job Role Matching &amp; Fit Engine
          </h1>
          <p className="text-sm text-slate-600">
            Compare your profile against verified technology tracks. Discover matching roles, skill gaps, and transition roadmaps.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Button
            variant="outline"
            size="sm"
            icon={RefreshCw}
            onClick={fetchMatches}
            disabled={loading}
            className="text-xs"
          >
            Re-evaluate
          </Button>
          <Link to="/career-roadmap">
            <Button variant="primary" size="sm" icon={Compass} className="text-xs">
              My Roadmaps
            </Button>
          </Link>
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-sm flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
          <div>
            <p className="font-semibold">Matching Error</p>
            <p className="text-rose-700 text-xs mt-0.5">{error}</p>
          </div>
        </div>
      )}

      {/* Filter and Search Bar */}
      <div className="flex flex-col sm:flex-row items-center justify-between gap-3 p-4 rounded-xl bg-slate-50 border border-slate-200">
        <div className="flex items-center gap-2 w-full sm:w-auto">
          <Search className="w-4 h-4 text-slate-400 shrink-0" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search roles (e.g. Backend, Data Scientist, DevOps)..."
            className="bg-transparent border-none text-xs text-slate-900 placeholder-slate-400 focus:outline-none w-full sm:w-64"
          />
        </div>

        <div className="flex items-center gap-1.5 overflow-x-auto w-full sm:w-auto">
          {['All Roles', 'Strong Match', 'Good Match', 'Moderate Match', 'Low Match'].map((cat) => (
            <button
              key={cat}
              type="button"
              onClick={() => setFilterCategory(cat)}
              className={`text-xs px-3 py-1.5 rounded-lg font-medium transition-colors cursor-pointer ${
                filterCategory === cat || (cat === 'All Roles' && filterCategory === 'All')
                  ? 'bg-indigo-600 text-white shadow-2xs'
                  : 'bg-white text-slate-600 border border-slate-200 hover:bg-slate-100'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Roles Grid */}
      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="h-64 rounded-xl border border-slate-200 bg-white animate-pulse p-6" />
          ))}
        </div>
      ) : filteredMatches.length === 0 ? (
        <Card className="p-12 text-center border-dashed border-2 border-slate-200">
          <Briefcase className="w-10 h-10 text-slate-400 mx-auto mb-3" />
          <h3 className="text-base font-bold text-slate-900">No Matching Roles Found</h3>
          <p className="text-xs text-slate-500 max-w-sm mx-auto mt-1">
            Try adjusting your search query or category filters.
          </p>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {filteredMatches.map((role) => (
            <Card
              key={role.id || role.title}
              className="p-6 flex flex-col justify-between border-slate-200 hover:border-indigo-300 hover:shadow-md transition-all duration-200"
            >
              <div className="space-y-4">
                {/* Role Header */}
                <div className="flex items-start justify-between gap-3">
                  <div>
                    <h3 className="text-lg font-bold text-slate-900 leading-snug">
                      {role.title}
                    </h3>
                    <div className="flex items-center gap-3 text-xs text-slate-500 mt-1">
                      <span className="flex items-center gap-1">
                        <Clock className="w-3.5 h-3.5 text-slate-400" />
                        {role.min_exp}–{role.max_exp} yrs exp
                      </span>
                      <span>•</span>
                      <span className="font-semibold text-slate-700">
                        Median: ₹{role.median_salary_lpa} LPA
                      </span>
                    </div>
                  </div>
                  <div>{getScoreBadge(role.match_score, role.match_category)}</div>
                </div>

                <p className="text-xs text-slate-600 line-clamp-2 leading-relaxed">
                  {role.description}
                </p>

                {/* Score Progress Bar */}
                <div>
                  <div className="flex items-center justify-between text-[11px] font-semibold text-slate-500 mb-1">
                    <span>Skill & Tenure Alignment</span>
                    <span className="text-slate-700 font-bold">{role.match_score}%</span>
                  </div>
                  <div className="w-full bg-slate-100 rounded-full h-2 overflow-hidden">
                    <div
                      className={`h-2 rounded-full ${
                        role.match_score >= 80
                          ? 'bg-emerald-500'
                          : role.match_score >= 65
                          ? 'bg-indigo-600'
                          : role.match_score >= 50
                          ? 'bg-sky-500'
                          : 'bg-amber-500'
                      }`}
                      style={{ width: `${role.match_score}%` }}
                    />
                  </div>
                </div>

                {/* Matched Skills */}
                <div>
                  <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500 block mb-1.5">
                    Matched Skills ({role.matched_skills.length})
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {role.matched_skills.length === 0 ? (
                      <span className="text-xs text-slate-400 italic">None matched yet</span>
                    ) : (
                      role.matched_skills.map((s) => (
                        <span
                          key={s}
                          className="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-md text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200"
                        >
                          <CheckCircle2 className="w-3 h-3 text-emerald-600" />
                          {s}
                        </span>
                      ))
                    )}
                  </div>
                </div>

                {/* Missing Required Skills */}
                {role.missing_required_skills.length > 0 && (
                  <div>
                    <span className="text-[11px] font-bold uppercase tracking-wider text-rose-500 block mb-1.5">
                      Missing Core Requirements ({role.missing_required_skills.length})
                    </span>
                    <div className="flex flex-wrap gap-1.5">
                      {role.missing_required_skills.map((s) => (
                        <span
                          key={s}
                          className="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-xs font-medium bg-rose-50 text-rose-700 border border-rose-200"
                        >
                          <XCircle className="w-3 h-3 text-rose-500" />
                          {s}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              {/* Card Footer Action */}
              <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between">
                <span className="text-xs text-slate-400">
                  Spread: {role.p10_salary_lpa}L – {role.p90_salary_lpa}L
                </span>
                <Button
                  variant="primary"
                  size="sm"
                  icon={Compass}
                  onClick={() => handleGenerateRoadmap(role.id, role.title)}
                  className="text-xs"
                >
                  Generate Roadmap
                </Button>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
};

export default JobMatchingPage;
