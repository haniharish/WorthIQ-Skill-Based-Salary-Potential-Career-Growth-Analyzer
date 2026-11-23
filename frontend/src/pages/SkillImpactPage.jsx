import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Sparkles,
  TrendingUp,
  Layers,
  CheckCircle2,
  Plus,
  Trash2,
  RefreshCw,
  Zap,
  ArrowRight,
  ShieldCheck,
  AlertCircle,
  HelpCircle,
  BarChart3,
  Flame,
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell,
  CartesianGrid,
} from 'recharts';
import { Card, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { useAuth } from '../context/AuthContext';
import { intelligenceService } from '../services/intelligenceService';

export const SkillImpactPage = () => {
  const { profile } = useAuth();

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [impactData, setImpactData] = useState(null);
  const [cooccurrences, setCooccurrences] = useState([]);
  const [taxonomy, setTaxonomy] = useState(null);

  // Counterfactual What-If State
  const [simRole, setSimRole] = useState('Full Stack Developer');
  const [simExp, setSimExp] = useState(3.0);
  const [simCurrentSkills, setSimCurrentSkills] = useState(['JavaScript', 'React.js', 'Node.js', 'PostgreSQL', 'Git']);
  const [simAddSkill, setSimAddSkill] = useState('');
  const [simResult, setSimResult] = useState(null);
  const [simLoading, setSimLoading] = useState(false);

  const fetchSkillIntelligence = async () => {
    setLoading(true);
    setError(null);
    try {
      const [impactRes, coRes, taxRes] = await Promise.all([
        intelligenceService.getSkillImpact(),
        intelligenceService.getSkillCoOccurrence('', 15),
        intelligenceService.getSkills(),
      ]);

      setImpactData(impactRes);
      setCooccurrences(coRes.co_occurrences || []);
      setTaxonomy(taxRes);

      if (impactRes?.evaluated_profile) {
        setSimRole(impactRes.evaluated_profile.job_role || 'Full Stack Developer');
        setSimExp(impactRes.evaluated_profile.years_of_experience || 3.0);
        setSimCurrentSkills(impactRes.evaluated_profile.skills || ['JavaScript', 'React.js', 'Node.js', 'PostgreSQL', 'Git']);
      }
    } catch (err) {
      console.error('Failed to load skill intelligence:', err);
      setError('Unable to load skill valuation data. Please verify your connection.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSkillIntelligence();
  }, []);

  const handleRunCounterfactual = async (skillToEvaluate) => {
    const targetSkill = (skillToEvaluate || simAddSkill).trim();
    if (!targetSkill) return;

    setSimLoading(true);
    try {
      const res = await intelligenceService.compareSkills({
        job_role: simRole,
        years_of_experience: simExp,
        location: profile?.location || 'Bengaluru',
        education: profile?.education || "Bachelor's Degree",
        skills: simCurrentSkills,
        add_skills: [targetSkill],
      });
      setSimResult(res);
      setSimAddSkill('');
    } catch (err) {
      console.error('Counterfactual simulation failed:', err);
    } finally {
      setSimLoading(false);
    }
  };

  // Prepare chart data for top skill contributions
  const chartData = (impactData?.skill_impacts || []).slice(0, 8).map((item) => ({
    name: item.skill_name,
    contribution: Math.round(item.marginal_contribution_inr),
    lpa: (item.marginal_contribution_inr / 100000).toFixed(2),
    pct: item.percentage_impact,
  }));

  return (
    <div className="space-y-8 max-w-6xl mx-auto pb-12">
      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-2 border-b border-slate-200">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-slate-900">
              Skill Impact & Valuation Intelligence
            </h1>
            <Badge variant="indigo" size="xs" dot>
              AI Skill Engine
            </Badge>
          </div>
          <p className="text-sm text-slate-600">
            Deconstruct your technical portfolio to discover individual skill premiums, pairwise co-occurrence lift, and counterfactual ROI.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Button
            variant="outline"
            size="sm"
            icon={RefreshCw}
            onClick={fetchSkillIntelligence}
            disabled={loading}
            className="text-xs"
          >
            Refresh
          </Button>
          <Link to="/job-matching">
            <Button variant="primary" size="sm" icon={TrendingUp} className="text-xs">
              Match Roles
            </Button>
          </Link>
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-sm flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
          <div>
            <p className="font-semibold">Intelligence Error</p>
            <p className="text-rose-700 text-xs mt-0.5">{error}</p>
          </div>
        </div>
      )}

      {loading ? (
        <div className="space-y-6">
          <div className="h-28 bg-slate-100 rounded-xl animate-pulse" />
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="h-64 bg-slate-100 rounded-xl animate-pulse" />
            <div className="h-64 bg-slate-100 rounded-xl animate-pulse" />
          </div>
        </div>
      ) : (
        <>
          {/* Top Metric Cards */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
            {/* Evaluated Skills Count */}
            <Card className="p-5 border-slate-200 bg-white">
              <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block mb-1">
                Portfolio Skill Depth
              </span>
              <div className="text-3xl font-extrabold text-slate-900">
                {impactData?.evaluated_profile?.skills?.length || 0} Skills
              </div>
              <p className="text-xs text-slate-500 mt-2">
                Active technical proficiencies synchronized from your verified profile.
              </p>
            </Card>

            {/* Bundle Synergy Score */}
            <Card className="p-5 border-indigo-200 bg-indigo-50/25">
              <div className="flex items-center justify-between mb-1">
                <span className="text-xs font-bold text-indigo-700 uppercase tracking-wider block">
                  Tech Stack Synergy
                </span>
                <Badge variant="indigo" size="xs">
                  {impactData?.bundle_synergy?.synergy_label || 'Complementary Stack'}
                </Badge>
              </div>
              <div className="text-3xl font-extrabold text-indigo-900">
                {impactData?.bundle_synergy?.synergy_score || 78}%
              </div>
              <p className="text-xs text-indigo-700/80 mt-2">
                Calculated across {impactData?.bundle_synergy?.pair_count || 0} co-occurring high-affinity pairings.
              </p>
            </Card>

            {/* Top Contributing Skill */}
            <Card className="p-5 border-emerald-200 bg-emerald-50/20">
              <span className="text-xs font-semibold text-emerald-800 uppercase tracking-wider block mb-1">
                Highest Marginal Driver
              </span>
              <div className="text-2xl font-bold text-emerald-950 truncate">
                {impactData?.skill_impacts?.[0]?.skill_name || 'Docker'}
              </div>
              <div className="text-xs font-semibold text-emerald-700 mt-0.5">
                +{impactData?.skill_impacts?.[0]?.percentage_impact || 0}% Marginal Uplift
              </div>
              <p className="text-xs text-slate-500 mt-2">
                Estimated marginal premium through controlled ablation holding role constant.
              </p>
            </Card>
          </div>

          {/* Skill Valuation Chart & Table */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Visual Bar Chart (Span 2) */}
            <div className="lg:col-span-2">
              <Card className="p-6">
                <CardHeader
                  title="Individual Skill Marginal Contribution (₹ INR)"
                  subtitle="Ablation value representing predicted compensation loss if this specific skill were absent."
                  icon={BarChart3}
                />

                <div className="h-72 w-full pt-3">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={chartData}
                      layout="vertical"
                      margin={{ top: 10, right: 30, left: 30, bottom: 10 }}
                    >
                      <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#e2e8f0" />
                      <XAxis
                        type="number"
                        stroke="#64748b"
                        fontSize={12}
                        tickFormatter={(v) => `₹${(v / 1000).toFixed(0)}k`}
                      />
                      <YAxis
                        type="category"
                        dataKey="name"
                        stroke="#64748b"
                        fontSize={12}
                        width={90}
                      />
                      <Tooltip
                        formatter={(val, name, item) => [
                          `₹${Number(val).toLocaleString('en-IN')} (+${item.payload.pct}%)`,
                          'Marginal Premium',
                        ]}
                        contentStyle={{
                          backgroundColor: '#1e293b',
                          borderRadius: '8px',
                          color: '#fff',
                          fontSize: '12px',
                        }}
                      />
                      <Bar dataKey="contribution" fill="#4f46e5" radius={[0, 4, 4, 0]} barSize={20}>
                        {chartData.map((_, i) => (
                          <Cell key={`cell-${i}`} fill={i === 0 ? '#10b981' : '#4f46e5'} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </Card>
            </div>

            {/* Co-occurrence Highlights */}
            <div>
              <Card className="p-6 h-full flex flex-col justify-between">
                <div>
                  <div className="flex items-center gap-2 mb-3">
                    <div className="p-2 rounded-lg bg-indigo-50 text-indigo-600">
                      <Flame className="w-5 h-5" />
                    </div>
                    <div>
                      <h3 className="font-semibold text-slate-900 text-sm">
                        High-Synergy Skill Pairs
                      </h3>
                      <p className="text-xs text-slate-500">Mined from 25,332 records</p>
                    </div>
                  </div>

                  <div className="space-y-2.5 pt-2">
                    {cooccurrences.slice(0, 6).map((pair, idx) => (
                      <div
                        key={idx}
                        className="p-2.5 rounded-lg border border-slate-100 bg-slate-50/70 flex items-center justify-between text-xs"
                      >
                        <div>
                          <span className="font-semibold text-slate-800">
                            {pair.skill_a} + {pair.skill_b}
                          </span>
                          <span className="text-[10px] text-slate-400 block">
                            {pair.pair_count} co-occurrences (Lift: {pair.lift})
                          </span>
                        </div>
                        <div className="text-right font-medium text-indigo-600">
                          ₹{(pair.pair_median_salary / 100000).toFixed(1)}L
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <div className="mt-4 pt-3 border-t border-slate-100 text-[11px] text-slate-400">
                  Lift &gt; 1.0 indicates skills that appear together far more frequently than random chance.
                </div>
              </Card>
            </div>
          </div>

          {/* Interactive What-If Counterfactual Laboratory */}
          <Card className="p-6 bg-gradient-to-r from-slate-50 to-indigo-50/30 border-indigo-200">
            <CardHeader
              title="Interactive What-If Skill Counterfactual Laboratory"
              subtitle="Simulate the projected compensation impact of acquiring an in-demand skill holding all other attributes fixed."
              icon={Sparkles}
            />

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-start pt-2">
              {/* Form Controls */}
              <div className="space-y-4">
                <div>
                  <label className="text-xs font-semibold text-slate-700 uppercase tracking-wider block mb-1">
                    Select a Target Skill to Acquire
                  </label>
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={simAddSkill}
                      onChange={(e) => setSimAddSkill(e.target.value)}
                      placeholder="e.g. AWS, Docker, Kubernetes"
                      className="flex-1 rounded-lg text-sm bg-white border border-slate-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                    <Button
                      variant="primary"
                      size="sm"
                      onClick={() => handleRunCounterfactual()}
                      isLoading={simLoading}
                      disabled={!simAddSkill.trim()}
                    >
                      Simulate
                    </Button>
                  </div>
                </div>

                {/* Popular Quick Suggestions */}
                <div>
                  <span className="text-[11px] font-semibold text-slate-500 uppercase tracking-wider block mb-1.5">
                    Quick-Test High-Demand Skills:
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {['AWS', 'Kubernetes', 'Docker', 'Redis', 'TypeScript', 'FastAPI'].map((s) => (
                      <button
                        key={s}
                        type="button"
                        onClick={() => handleRunCounterfactual(s)}
                        className="text-xs px-2.5 py-1 rounded-md bg-white border border-slate-200 hover:border-indigo-300 hover:text-indigo-600 transition-colors cursor-pointer"
                      >
                        + {s}
                      </button>
                    ))}
                  </div>
                </div>
              </div>

              {/* Simulation Output Card (Span 2) */}
              <div className="md:col-span-2">
                {simResult ? (
                  <div className="p-5 rounded-xl bg-white border border-indigo-200 shadow-xs space-y-4">
                    <div className="flex items-center justify-between pb-3 border-b border-slate-100">
                      <div>
                        <span className="text-xs font-bold text-indigo-600 uppercase tracking-wider">
                          Simulation Results
                        </span>
                        <h4 className="text-sm font-semibold text-slate-900 mt-0.5">
                          Acquiring {simResult.added_skills.join(', ')}
                        </h4>
                      </div>
                      <Badge variant={simResult.delta_annual >= 0 ? 'emerald' : 'amber'}>
                        {simResult.delta_annual >= 0 ? '+' : ''}
                        {simResult.percentage_change}% Projected
                      </Badge>
                    </div>

                    <div className="grid grid-cols-3 gap-4 text-center">
                      <div className="p-3 rounded-lg bg-slate-50">
                        <span className="text-[11px] text-slate-400 block uppercase">Current Baseline</span>
                        <span className="text-lg font-bold text-slate-800">
                          ₹{simResult.original_salary_lpa} LPA
                        </span>
                      </div>
                      <div className="p-3 rounded-lg bg-indigo-50/60 border border-indigo-200">
                        <span className="text-[11px] text-indigo-500 block uppercase font-medium">With Target Skill</span>
                        <span className="text-lg font-extrabold text-indigo-900">
                          ₹{simResult.counterfactual_salary_lpa} LPA
                        </span>
                      </div>
                      <div className="p-3 rounded-lg bg-emerald-50/60 border border-emerald-200">
                        <span className="text-[11px] text-emerald-600 block uppercase font-medium">Estimated Premium</span>
                        <span className="text-lg font-bold text-emerald-800">
                          +{simResult.delta_lpa} LPA
                        </span>
                      </div>
                    </div>

                    <p className="text-[11px] text-slate-400 italic">
                      {simResult.disclaimer}
                    </p>
                  </div>
                ) : (
                  <div className="p-8 rounded-xl border border-dashed border-slate-200 bg-white/70 text-center text-xs text-slate-500">
                    <Sparkles className="w-6 h-6 text-indigo-400 mx-auto mb-2" />
                    Select or type a technical skill above to simulate its estimated compensation impact.
                  </div>
                )}
              </div>
            </div>
          </Card>
        </>
      )}
    </div>
  );
};

export default SkillImpactPage;
