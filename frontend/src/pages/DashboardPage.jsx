import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { dashboardService } from '../services/dashboardService';
import { Card, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { StatCard } from '../components/ui/StatCard';
import { EmptyState } from '../components/ui/EmptyState';
import { ConfidenceIndicator } from '../components/ui/ConfidenceIndicator';
import { CardSkeleton } from '../components/ui/LoadingSkeleton';
import {
  TrendingUp,
  Sparkles,
  Briefcase,
  Sliders,
  Compass,
  User,
  MapPin,
  Clock,
  Layers,
  ArrowRight,
  ChevronRight,
  AlertTriangle,
  Award,
  Zap,
  BookmarkCheck,
  CheckCircle2,
  Calendar,
  BarChart3,
  RefreshCw,
  ExternalLink,
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell,
  LineChart,
  Line,
  CartesianGrid,
} from 'recharts';

export const DashboardPage = () => {
  const { user } = useAuth();
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [data, setData] = useState({
    profile: null,
    latestPrediction: null,
    predictionHistory: [],
    matchedRoles: [],
    roadmaps: [],
    modelInfo: null,
    stats: {
      totalEvaluations: 0,
      skillCount: 0,
      matchedRoleCount: 0,
      roadmapProgressPct: 0,
    },
  });

  const loadData = async () => {
    setLoading(true);
    try {
      const res = await dashboardService.getDashboardData();
      setData(res);
    } catch (err) {
      console.error('Failed to load dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const { profile, latestPrediction, predictionHistory, matchedRoles, roadmaps } = data;

  // Profile completion score
  const userSkills = profile?.skills || [];
  const skillCount = userSkills.length;
  const completenessChecks = [
    Boolean(profile?.job_role),
    profile?.years_of_experience !== undefined && profile?.years_of_experience !== null,
    Boolean(profile?.location),
    Boolean(profile?.education),
    skillCount >= 3,
    skillCount >= 6,
  ];
  const completenessPercent = Math.round(
    (completenessChecks.filter(Boolean).length / completenessChecks.length) * 100
  );

  // Active roadmap
  const activeRoadmap = roadmaps && roadmaps.length > 0 ? roadmaps[0] : null;

  // Extract normalized salary fields safely from PredictionHistory or Prediction API
  const medianSalary = Number(
    latestPrediction?.predicted_median_salary ??
    latestPrediction?.predicted_salary ??
    (latestPrediction?.salary_lpa ? latestPrediction.salary_lpa * 100000 : 0)
  );

  const lowSalary = Number(
    latestPrediction?.predicted_low_salary ??
    latestPrediction?.salary_range?.low ??
    latestPrediction?.salary_range?.p10_salary ??
    (medianSalary > 0 ? Math.round(medianSalary * 0.7) : 0)
  );

  const highSalary = Number(
    latestPrediction?.predicted_high_salary ??
    latestPrediction?.salary_range?.high ??
    latestPrediction?.salary_range?.p90_salary ??
    (medianSalary > 0 ? Math.round(medianSalary * 1.35) : 0)
  );

  const medianLpa =
    latestPrediction?.salary_lpa ??
    latestPrediction?.predicted_salary_lpa ??
    (medianSalary > 0 ? (medianSalary / 100000).toFixed(1) : null);

  const lowLpa =
    latestPrediction?.salary_range?.p10_lpa ??
    (lowSalary > 0 ? (lowSalary / 100000).toFixed(1) : null);

  const highLpa =
    latestPrediction?.salary_range?.p90_lpa ??
    (highSalary > 0 ? (highSalary / 100000).toFixed(1) : null);

  // Prepare chart data for latest prediction range
  const rangeChartData =
    latestPrediction && medianSalary > 0
      ? [
          {
            name: 'Conservative (P10)',
            salary: lowLpa ? parseFloat(lowLpa) : 4.0,
            raw: lowSalary,
            color: '#94a3b8',
          },
          {
            name: 'Market Median (P50)',
            salary: medianLpa ? parseFloat(medianLpa) : 7.5,
            raw: medianSalary,
            color: '#6366f1',
          },
          {
            name: 'Top Tier (P90)',
            salary: highLpa ? parseFloat(highLpa) : 15.0,
            raw: highSalary,
            color: '#10b981',
          },
        ]
      : [];

  // Historical trend data (reversed to chronological)
  const historyChartData = (predictionHistory || [])
    .slice(0, 7)
    .reverse()
    .map((item) => {
      const med = Number(item.predicted_median_salary ?? item.predicted_salary ?? 0);
      const lpa = Number(item.salary_lpa ?? item.predicted_salary_lpa ?? (med > 0 ? med / 100000 : 0));
      return {
        name: new Date(item.created_at).toLocaleDateString('en-IN', {
          month: 'short',
          day: 'numeric',
        }),
        lpa: Number(lpa.toFixed(1)),
        role: item.job_role,
      };
    });

  return (
    <div className="space-y-6 sm:space-y-8 max-w-7xl mx-auto pb-12">
      {/* 1. Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-200/80">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Dashboard Overview
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Real-time compensation analytics, market valuation bounds, and career guidance.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Link to="/salary-analysis">
            <Button variant="primary" size="sm" icon={TrendingUp}>
              New Valuation
            </Button>
          </Link>
        </div>
      </div>

      {/* 2. Welcome Banner Card */}
      <div className="bg-white rounded-2xl border border-slate-200/90 p-6 sm:p-8 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <h2 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight mb-2">
            Welcome back, {user?.full_name || 'Engineer'}
          </h2>
          <p className="text-xs sm:text-sm text-slate-500 flex flex-wrap items-center gap-3">
            <span className="flex items-center gap-1.5 font-medium text-slate-700">
              <Briefcase className="w-3.5 h-3.5 text-indigo-600" />
              {profile?.job_role || 'Role not configured'}
            </span>
            <span className="text-slate-300">&bull;</span>
            <span className="flex items-center gap-1.5 font-medium text-slate-700">
              <Clock className="w-3.5 h-3.5 text-indigo-600" />
              {profile?.years_of_experience ?? 0} {profile?.years_of_experience === 1 ? 'Year' : 'Years'} Exp
            </span>
            {profile?.location && (
              <>
                <span className="text-slate-300">&bull;</span>
                <span className="flex items-center gap-1.5 font-medium text-slate-700">
                  <MapPin className="w-3.5 h-3.5 text-indigo-600" />
                  {profile.location}
                </span>
              </>
            )}
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-3">
          <Link to="/profile">
            <Button variant="outline" size="sm" icon={User}>
              View Profile
            </Button>
          </Link>
          <Link to="/salary-analysis">
            <Button variant="secondary" size="sm" icon={TrendingUp}>
              Analyze Salary
            </Button>
          </Link>
        </div>
      </div>

      {/* 2. Profile Completeness Progress (if < 100%) */}
      {completenessPercent < 100 && (
        <div className="bg-gradient-to-r from-indigo-50/80 via-white to-violet-50/80 rounded-2xl border border-indigo-100 p-5 shadow-2xs flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-start gap-3">
            <div className="p-2 rounded-xl bg-indigo-600 text-white shrink-0 shadow-xs">
              <Sparkles className="w-4 h-4" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-900">
                  Profile Completeness ({completenessPercent}%)
                </h4>
              </div>
              <p className="text-xs text-slate-600 mt-0.5">
                Add more verified technical skills to increase the precision of your ML salary prediction and job role matches.
              </p>
            </div>
          </div>
          <Link to="/profile/setup" className="shrink-0">
            <Button variant="outline" size="sm" iconRight={ArrowRight}>
              Complete Profile
            </Button>
          </Link>
        </div>
      )}

      {/* 3. KPI Overview Cards */}
      {loading ? (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          <CardSkeleton count={4} />
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {/* KPI 1: Estimated Salary */}
          <StatCard
            title="Estimated Salary (P50)"
            value={
              latestPrediction && medianLpa
                ? `₹${medianLpa} LPA`
                : 'Not Evaluated'
            }
            subtitle={
              latestPrediction && medianLpa
                ? `₹${medianLpa} LPA Annual Median`
                : 'Run your first evaluation'
            }
            icon={TrendingUp}
            badgeText={latestPrediction && medianLpa ? 'P50 Median' : null}
            badgeVariant="indigo"
            onClick={() => navigate(latestPrediction ? `/explanations/${latestPrediction.id}` : '/salary-analysis')}
          />

          {/* KPI 2: Salary Range */}
          <StatCard
            title="Estimated Range (P10–P90)"
            value={
              latestPrediction && lowLpa && highLpa
                ? `₹${lowLpa}L – ₹${highLpa}L`
                : '—'
            }
            subtitle={
              latestPrediction && lowLpa && highLpa
                ? 'Conservative to top-tier bounds'
                : 'Awaiting model inference'
            }
            icon={BarChart3}
            badgeText={
              typeof latestPrediction?.confidence === 'string'
                ? latestPrediction.confidence
                : latestPrediction?.confidence?.confidence_tier || latestPrediction?.confidence_level || 'Active'
            }
            badgeVariant={
              (latestPrediction?.confidence === 'High' || latestPrediction?.confidence?.confidence_tier === 'High')
                ? 'emerald'
                : 'indigo'
            }
            onClick={() => navigate('/salary-analysis')}
          />

          {/* KPI 3: Matched Job Roles */}
          <StatCard
            title="Compatible Roles"
            value={matchedRoles.length > 0 ? `${matchedRoles.length} Roles` : '9 Roles'}
            subtitle={
              matchedRoles.length > 0
                ? `Top: ${matchedRoles[0]?.title} (${matchedRoles[0]?.match_score}%)`
                : 'Catalog available'
            }
            icon={Briefcase}
            badgeText="Matched"
            badgeVariant="indigo"
            onClick={() => navigate('/job-matching')}
          />

          {/* KPI 4: Career Roadmap Progress */}
          <StatCard
            title="Roadmap Progress"
            value={
              activeRoadmap
                ? `${Math.round(activeRoadmap.overall_progress_pct || 0)}%`
                : 'No Active Goal'
            }
            subtitle={
              activeRoadmap
                ? `Target: ${activeRoadmap.target_role_title || 'Software Specialist'}`
                : 'Select role to start'
            }
            icon={Compass}
            progressPercent={activeRoadmap ? activeRoadmap.overall_progress_pct || 0 : 0}
            onClick={() => navigate('/career-roadmap')}
          />
        </div>
      )}

      {/* 4. Main Analytics Split: Salary Overview & Salary Prediction History */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left 7 Columns: Latest Salary Overview */}
        <div className="lg:col-span-7">
          <Card className="h-full flex flex-col justify-between">
            <div>
              <CardHeader
                title="Market Salary Valuation"
                subtitle="Quantile bounds derived from Random Forest Regressor 2.0"
                icon={TrendingUp}
                badge={
                  latestPrediction ? (
                    <Badge variant="indigo" size="xs">
                      Evaluated {new Date(latestPrediction.created_at).toLocaleDateString()}
                    </Badge>
                  ) : null
                }
              />

              {latestPrediction ? (
                <div className="mt-4 space-y-6">
                  {/* Top Stats Banner */}
                  <div className="p-4 rounded-xl bg-slate-50 border border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                    <div>
                      <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                        Evaluated Target Role
                      </span>
                      <p className="text-base font-bold text-slate-900 mt-0.5">
                        {latestPrediction.job_role} &middot; {latestPrediction.location}
                      </p>
                      <p className="text-xs text-slate-500 mt-0.5">
                        {latestPrediction.years_of_experience} yrs exp &middot; {latestPrediction.skills?.length || 0} skills evaluated
                      </p>
                    </div>

                    <div className="text-left sm:text-right">
                      <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider block">
                        Monthly Gross Equivalent
                      </span>
                      <p className="text-base font-bold text-indigo-600 mt-0.5">
                        ₹{medianSalary > 0 ? Math.round(medianSalary / 12).toLocaleString('en-IN') : '62,500'}{' '}
                        <span className="text-xs text-slate-400 font-normal">/ mo</span>
                      </p>
                    </div>
                  </div>

                  {/* Range Quantiles Chart */}
                  <div>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-xs font-bold uppercase tracking-wider text-slate-500">
                        Salary Distribution (LPA)
                      </span>
                      <span className="text-[11px] text-slate-400">P10 – P50 – P90</span>
                    </div>
                    <div className="h-44 w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart
                          data={rangeChartData}
                          layout="vertical"
                          margin={{ top: 5, right: 30, left: 40, bottom: 5 }}
                        >
                          <XAxis type="number" unit="L" tick={{ fontSize: 11, fill: '#64748b' }} />
                          <YAxis
                            type="category"
                            dataKey="name"
                            tick={{ fontSize: 11, fill: '#334155', fontWeight: 600 }}
                            width={110}
                          />
                          <Tooltip
                            formatter={(val, name, item) => [
                              `₹${val} LPA (₹${item.payload.raw.toLocaleString('en-IN')})`,
                              'Estimated Compensation',
                            ]}
                            contentStyle={{
                              borderRadius: '0.75rem',
                              border: '1px solid #e2e8f0',
                              fontSize: '12px',
                            }}
                          />
                          <Bar dataKey="salary" radius={[0, 6, 6, 0]}>
                            {rangeChartData.map((entry, index) => (
                              <Cell key={`cell-${index}`} fill={entry.color} />
                            ))}
                          </Bar>
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  {/* Confidence & Explainability Callout */}
                  <div className="p-4 rounded-xl bg-indigo-50/50 border border-indigo-100 flex items-center justify-between gap-4">
                    <div className="flex items-center gap-3">
                      <div className="p-2 rounded-lg bg-indigo-100 text-indigo-700 shrink-0">
                        <Sparkles className="w-4 h-4" />
                      </div>
                      <div>
                        <p className="text-xs font-bold text-slate-900">SHAP Explainability Available</p>
                        <p className="text-[11px] text-slate-500">
                          Inspect the exact Rupee contribution of your skills, experience, and location.
                        </p>
                      </div>
                    </div>
                    <Link to={`/explanations/${latestPrediction.id}`}>
                      <Button variant="primary" size="sm" iconRight={ArrowRight}>
                        Explain
                      </Button>
                    </Link>
                  </div>
                </div>
              ) : (
                <EmptyState
                  icon={TrendingUp}
                  title="No Salary Evaluations Yet"
                  description="Run an AI salary analysis to predict your market compensation range based on your current technical stack and experience."
                  actionLabel="Analyze Salary Now"
                  onAction={() => navigate('/salary-analysis')}
                  className="my-4"
                />
              )}
            </div>

            {latestPrediction && (
              <div className="pt-4 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
                <span>Model: Random Forest 2.0 (CV MAE: ₹3.35L)</span>
                <Link to="/saved-reports" className="text-indigo-600 font-semibold hover:underline flex items-center gap-1">
                  History ({data.stats.totalEvaluations}) <ChevronRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            )}
          </Card>
        </div>

        {/* Right 5 Columns: Historical Trend & Model Confidence */}
        <div className="lg:col-span-5 space-y-6">
          {/* Historical Trend Card */}
          <Card className="h-full flex flex-col justify-between">
            <div>
              <CardHeader
                title="Evaluation History"
                subtitle="Progression across recent salary analyses"
                icon={Calendar}
              />

              {historyChartData.length >= 2 ? (
                <div className="mt-4">
                  <div className="h-44 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                      <LineChart data={historyChartData} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
                        <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                        <XAxis dataKey="name" tick={{ fontSize: 10, fill: '#64748b' }} />
                        <YAxis tick={{ fontSize: 10, fill: '#64748b' }} unit="L" />
                        <Tooltip
                          formatter={(val, name, item) => [`${val} LPA`, item.payload.role]}
                          contentStyle={{
                            borderRadius: '0.75rem',
                            border: '1px solid #e2e8f0',
                            fontSize: '11px',
                          }}
                        />
                        <Line
                          type="monotone"
                          dataKey="lpa"
                          stroke="#6366f1"
                          strokeWidth={2.5}
                          dot={{ r: 4, fill: '#6366f1' }}
                          activeDot={{ r: 6 }}
                        />
                      </LineChart>
                    </ResponsiveContainer>
                  </div>
                  <p className="text-[11px] text-slate-400 text-center mt-2">
                    Median LPA plotted chronologically across your evaluations
                  </p>
                </div>
              ) : (
                <div className="py-8 text-center">
                  <p className="text-xs text-slate-500 max-w-xs mx-auto">
                    Evaluate your profile under different roles or after acquiring new skills to observe historical trajectory comparisons.
                  </p>
                  <Link to="/salary-analysis" className="inline-block mt-4">
                    <Button variant="outline" size="sm">
                      New Analysis
                    </Button>
                  </Link>
                </div>
              )}
            </div>

            {/* Quick Actions Footer */}
            <div className="pt-4 border-t border-slate-100">
              <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-2">
                Quick Shortcuts
              </span>
              <div className="grid grid-cols-2 sm:grid-cols-3 gap-2">
                <Link
                  to="/skill-impact"
                  className="flex items-center gap-2 p-2 rounded-xl bg-slate-50 hover:bg-indigo-50/70 border border-slate-100 text-xs font-semibold text-slate-700 hover:text-indigo-700 transition-colors"
                >
                  <Sparkles className="w-3.5 h-3.5 text-indigo-600 shrink-0" />
                  <span>Skill Intelligence</span>
                </Link>
                <Link
                  to="/job-matching"
                  className="flex items-center gap-2 p-2 rounded-xl bg-slate-50 hover:bg-indigo-50/70 border border-slate-100 text-xs font-semibold text-slate-700 hover:text-indigo-700 transition-colors"
                >
                  <Briefcase className="w-3.5 h-3.5 text-indigo-600 shrink-0" />
                  <span>Role Matching</span>
                </Link>
                <Link
                  to="/career-roadmap"
                  className="flex items-center gap-2 p-2 rounded-xl bg-slate-50 hover:bg-indigo-50/70 border border-slate-100 text-xs font-semibold text-slate-700 hover:text-indigo-700 transition-colors"
                >
                  <Compass className="w-3.5 h-3.5 text-indigo-600 shrink-0" />
                  <span>Roadmaps</span>
                </Link>
                <Link
                  to="/what-if-simulator"
                  className="flex items-center gap-2 p-2 rounded-xl bg-slate-50 hover:bg-indigo-50/70 border border-slate-100 text-xs font-semibold text-slate-700 hover:text-indigo-700 transition-colors"
                >
                  <Sliders className="w-3.5 h-3.5 text-indigo-600 shrink-0" />
                  <span>What-If Lab</span>
                </Link>
                <Link
                  to="/resume-analysis"
                  className="flex items-center gap-2 p-2 rounded-xl bg-slate-50 hover:bg-indigo-50/70 border border-slate-100 text-xs font-semibold text-slate-700 hover:text-indigo-700 transition-colors"
                >
                  <BookmarkCheck className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                  <span>Resume Intel</span>
                </Link>
                <Link
                  to="/saved-reports"
                  className="flex items-center gap-2 p-2 rounded-xl bg-slate-50 hover:bg-indigo-50/70 border border-slate-100 text-xs font-semibold text-slate-700 hover:text-indigo-700 transition-colors"
                >
                  <Calendar className="w-3.5 h-3.5 text-indigo-600 shrink-0" />
                  <span>All Reports</span>
                </Link>
              </div>
            </div>
          </Card>
        </div>
      </div>

      {/* 5. Second Grid: Job Role Matching Shortlist & Career Roadmap Progress */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left 6 Columns: Top Matching Roles */}
        <div className="lg:col-span-6">
          <Card className="h-full flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                <div>
                  <h3 className="text-sm font-bold text-slate-900 tracking-tight flex items-center gap-2">
                    <Briefcase className="w-4 h-4 text-indigo-600" />
                    Top Compatible Job Roles
                  </h3>
                  <p className="text-xs text-slate-500 mt-0.5">
                    Multi-factor match score based on skill overlap and experience fit
                  </p>
                </div>
                <Link to="/job-matching" className="text-xs font-semibold text-indigo-600 hover:underline">
                  View All ({matchedRoles.length})
                </Link>
              </div>

              {matchedRoles.length > 0 ? (
                <div className="divide-y divide-slate-100 mt-2">
                  {matchedRoles.slice(0, 3).map((role) => (
                    <div
                      key={role.id || role.title}
                      className="py-3.5 flex items-start justify-between gap-4 hover:bg-slate-50/70 px-2 rounded-xl transition-colors cursor-pointer"
                      onClick={() => navigate('/job-matching')}
                    >
                      <div className="space-y-1">
                        <div className="flex items-center gap-2">
                          <h4 className="text-xs font-bold text-slate-900">{role.title}</h4>
                          <Badge
                            variant={
                              role.match_score >= 80
                                ? 'emerald'
                                : role.match_score >= 65
                                ? 'indigo'
                                : 'sky'
                            }
                            size="xs"
                          >
                            {role.match_score}% Match
                          </Badge>
                        </div>
                        <p className="text-[11px] text-slate-500">
                          Median Market Salary: ₹{role.median_salary_lpa || '7.5'} LPA &middot; {role.min_exp}–{role.max_exp} yrs exp
                        </p>
                        <div className="flex flex-wrap gap-1 pt-1">
                          {(role.matched_required_skills || []).slice(0, 3).map((s) => (
                            <span
                              key={s}
                              className="px-1.5 py-0.5 text-[10px] font-medium bg-emerald-50 text-emerald-700 rounded border border-emerald-200"
                            >
                              ✓ {s}
                            </span>
                          ))}
                          {(role.missing_required_skills || []).slice(0, 2).map((s) => (
                            <span
                              key={s}
                              className="px-1.5 py-0.5 text-[10px] font-medium bg-rose-50 text-rose-700 rounded border border-rose-200"
                            >
                              Need: {s}
                            </span>
                          ))}
                        </div>
                      </div>

                      <ChevronRight className="w-4 h-4 text-slate-400 shrink-0 mt-2" />
                    </div>
                  ))}
                </div>
              ) : (
                <EmptyState
                  icon={Briefcase}
                  title="No Role Matches Available"
                  description="Complete your profile with your technical skills to receive automated candidate match evaluations."
                  actionLabel="Update Skills"
                  onAction={() => navigate('/profile/setup')}
                  className="my-4"
                />
              )}
            </div>

            <div className="pt-3 border-t border-slate-100 text-[11px] text-slate-400 flex items-center justify-between">
              <span>Calibrated across 9 technology tracks</span>
              <span className="italic">Not a hiring guarantee</span>
            </div>
          </Card>
        </div>

        {/* Right 6 Columns: Career Roadmap Overview */}
        <div className="lg:col-span-6">
          <Card className="h-full flex flex-col justify-between">
            <div>
              <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                <div>
                  <h3 className="text-sm font-bold text-slate-900 tracking-tight flex items-center gap-2">
                    <Compass className="w-4 h-4 text-indigo-600" />
                    Career Growth Roadmap
                  </h3>
                  <p className="text-xs text-slate-500 mt-0.5">
                    Targeted milestones, DAG prerequisite ordering &amp; capstone projects
                  </p>
                </div>
                <Link to="/career-roadmap" className="text-xs font-semibold text-indigo-600 hover:underline">
                  {activeRoadmap ? 'View Stages' : 'Create Roadmap'}
                </Link>
              </div>

              {activeRoadmap ? (
                <div className="mt-4 space-y-4">
                  <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
                    <div className="flex items-center justify-between">
                      <span className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">
                        Target Role Goal
                      </span>
                      <Badge variant="indigo" size="xs">
                        {Math.round(activeRoadmap.overall_progress_pct || 0)}% Completed
                      </Badge>
                    </div>
                    <p className="text-base font-bold text-slate-900 mt-1">
                      {activeRoadmap.target_role_title}
                    </p>
                    <p className="text-xs text-slate-500 mt-0.5 line-clamp-1">
                      {activeRoadmap.title || 'Personalized career advancement milestone track'}
                    </p>

                    <div className="w-full bg-slate-200 h-2 rounded-full mt-3 overflow-hidden">
                      <div
                        className="bg-indigo-600 h-2 rounded-full transition-all duration-500"
                        style={{ width: `${activeRoadmap.overall_progress_pct || 0}%` }}
                      />
                    </div>
                  </div>

                  {/* Stage Milestones Preview */}
                  <div className="space-y-2">
                    <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
                      Curated Stages ({activeRoadmap.stages_count || 3} Milestones)
                    </span>
                    <div className="grid grid-cols-3 gap-2 text-center text-xs">
                      <div className="p-2.5 rounded-lg bg-emerald-50 border border-emerald-100 text-emerald-900">
                        <span className="text-[10px] uppercase font-bold text-emerald-600 block">Stage 1</span>
                        <span className="font-semibold text-xs block truncate mt-0.5">Foundations</span>
                      </div>
                      <div className="p-2.5 rounded-lg bg-indigo-50 border border-indigo-100 text-indigo-900">
                        <span className="text-[10px] uppercase font-bold text-indigo-600 block">Stage 2</span>
                        <span className="font-semibold text-xs block truncate mt-0.5">Specialization</span>
                      </div>
                      <div className="p-2.5 rounded-lg bg-slate-50 border border-slate-100 text-slate-700">
                        <span className="text-[10px] uppercase font-bold text-slate-400 block">Stage 3</span>
                        <span className="font-semibold text-xs block truncate mt-0.5">Advanced Scale</span>
                      </div>
                    </div>
                  </div>
                </div>
              ) : (
                <EmptyState
                  icon={Compass}
                  title="No Active Roadmap"
                  description="Generate a personalized career roadmap for any technology role with structured prerequisite stages and project briefs."
                  actionLabel="Generate Roadmap"
                  onAction={() => navigate('/career-roadmap')}
                  className="my-4"
                />
              )}
            </div>

            <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
              <span className="text-slate-400">Non-circular DAG sequencing</span>
              <Link to="/career-roadmap" className="text-indigo-600 font-semibold hover:underline flex items-center gap-1">
                Go to Roadmap <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>
          </Card>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
