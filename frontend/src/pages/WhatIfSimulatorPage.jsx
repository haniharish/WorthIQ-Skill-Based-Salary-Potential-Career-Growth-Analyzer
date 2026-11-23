import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';
import { intelligenceService } from '../services/intelligenceService';
import { Card, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { SelectInput } from '../components/ui/SelectInput';
import { SkillTagInput } from '../components/ui/SkillTagInput';
import { StatCard } from '../components/ui/StatCard';
import {
  Sliders,
  Sparkles,
  TrendingUp,
  ArrowRight,
  Plus,
  Trash2,
  RefreshCw,
  Info,
  CheckCircle2,
  Briefcase,
  MapPin,
  Layers,
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Cell,
} from 'recharts';

const STANDARD_ROLES = [
  'Full Stack Developer',
  'Backend Developer',
  'Frontend Developer',
  'DevOps Engineer',
  'Data Scientist',
  'Machine Learning Engineer',
  'Data Analyst',
  'Software Developer',
];

const STANDARD_LOCATIONS = [
  'Bengaluru',
  'Hyderabad',
  'Pune',
  'Mumbai',
  'Delhi NCR',
  'Chennai',
];

const HIGH_LEVERAGE_SKILLS = [
  'Docker',
  'Kubernetes',
  'AWS',
  'FastAPI',
  'Next.js',
  'PostgreSQL',
  'Redis',
  'Microservices',
  'CI/CD',
  'Machine Learning',
  'TypeScript',
  'React.js',
  'Python',
  'Go',
];

export const WhatIfSimulatorPage = () => {
  const { profile } = useAuth();
  const toast = useToast();

  const [role, setRole] = useState('Backend Developer');
  const [exp, setExp] = useState(3.0);
  const [location, setLocation] = useState('Bengaluru');
  const [education, setEducation] = useState("Bachelor's Degree");
  const [baseSkills, setBaseSkills] = useState(['Python', 'PostgreSQL', 'Git']);
  const [addSkills, setAddSkills] = useState(['Docker', 'AWS']);
  const [removeSkills, setRemoveSkills] = useState([]);

  const [availableSkills, setAvailableSkills] = useState(HIGH_LEVERAGE_SKILLS);
  const [simulating, setSimulating] = useState(false);
  const [simulationResult, setSimulationResult] = useState(null);

  // Autofill from user profile on mount
  useEffect(() => {
    if (profile) {
      if (profile.job_role) setRole(profile.job_role);
      if (profile.years_of_experience) setExp(Number(profile.years_of_experience));
      if (profile.location) setLocation(profile.location);
      if (profile.education) setEducation(profile.education);
      if (profile.skills && profile.skills.length > 0) {
        setBaseSkills(profile.skills.map((s) => s.name));
      }
    }
  }, [profile]);

  // Load canonical skills suggestions
  useEffect(() => {
    const fetchTaxonomy = async () => {
      try {
        const res = await intelligenceService.getSkills();
        if (res?.skills) {
          setAvailableSkills(res.skills.map((s) => s.name));
        }
      } catch (err) {
        console.warn('Could not load skills taxonomy', err);
      }
    };
    fetchTaxonomy();
  }, []);

  const handleRunSimulation = async () => {
    setSimulating(true);
    try {
      const payload = {
        job_role: role,
        years_of_experience: Number(exp),
        location,
        education,
        skills: baseSkills,
        add_skills: addSkills,
        remove_skills: removeSkills,
      };

      const result = await intelligenceService.compareSkills(payload);
      setSimulationResult(result);
      toast.success('Simulation completed! Evaluated counterfactual salary outcome.');
    } catch (err) {
      console.error('Simulation error:', err);
      toast.error('Simulation failed. Please verify inputs and try again.');
    } finally {
      setSimulating(false);
    }
  };

  // Run initial simulation
  useEffect(() => {
    handleRunSimulation();
  }, []);

  const chartData = simulationResult
    ? [
        {
          name: 'Baseline Profile',
          lpa: simulationResult.original_salary_lpa,
          raw: simulationResult.original_salary_annual,
          color: '#94a3b8',
        },
        {
          name: 'Simulated Scenario',
          lpa: simulationResult.counterfactual_salary_lpa,
          raw: simulationResult.counterfactual_salary_annual,
          color: simulationResult.delta_annual >= 0 ? '#10b981' : '#f43f5e',
        },
      ]
    : [];

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-200">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-slate-900 mb-1">
            What-If Salary Simulation Lab
          </h1>
          <p className="text-xs sm:text-sm text-slate-600">
            Simulate the market compensation impact of acquiring new technical skills or modifying experience holding all other factors constant.
          </p>
        </div>

        <Button
          variant="primary"
          size="sm"
          icon={RefreshCw}
          onClick={handleRunSimulation}
          isLoading={simulating}
        >
          Recalculate Scenario
        </Button>
      </div>

      {/* Main Grid: Controls on left, Live Outcome on right */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Simulation Inputs */}
        <div className="lg:col-span-5 space-y-6">
          <Card>
            <CardHeader
              title="Baseline Candidate Profile"
              subtitle="Current baseline features for controlled comparison"
              icon={Briefcase}
            />

            <div className="space-y-4 pt-2">
              <SelectInput
                label="Target Job Role"
                value={role}
                onChange={(e) => setRole(e.target.value)}
                options={STANDARD_ROLES}
              />

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-semibold text-slate-700 tracking-wide mb-1">
                    Experience (Years): {exp}
                  </label>
                  <input
                    type="range"
                    min="0"
                    max="15"
                    step="0.5"
                    value={exp}
                    onChange={(e) => setExp(parseFloat(e.target.value))}
                    className="w-full accent-indigo-600 cursor-pointer"
                  />
                </div>

                <SelectInput
                  label="Location"
                  value={location}
                  onChange={(e) => setLocation(e.target.value)}
                  options={STANDARD_LOCATIONS}
                />
              </div>

              <SkillTagInput
                label="Base Technical Skills"
                skills={baseSkills}
                onChange={setBaseSkills}
                suggestions={availableSkills}
                placeholder="Add current skill..."
              />
            </div>
          </Card>

          {/* Counterfactual Adjustments Card */}
          <Card>
            <CardHeader
              title="Counterfactual Skills Action"
              subtitle="Hypothetical skills to acquire or ablate"
              icon={Sliders}
            />

            <div className="space-y-4 pt-2">
              <SkillTagInput
                label="Skills to Acquire (+ Gain)"
                skills={addSkills}
                onChange={setAddSkills}
                suggestions={availableSkills}
                placeholder="Add skill to learn..."
                helperText="Simulates market compensation if you master these technologies."
              />

              <SkillTagInput
                label="Skills to Drop / Exclude (- Ablate)"
                skills={removeSkills}
                onChange={setRemoveSkills}
                suggestions={baseSkills}
                placeholder="Add skill to remove..."
                helperText="Simulates compensation without these skills."
              />
            </div>
          </Card>
        </div>

        {/* Right Column: Live Outcome Visualization */}
        <div className="lg:col-span-7 space-y-6">
          {simulationResult ? (
            <>
              {/* Outcome KPI Banner */}
              <div
                className={`p-6 rounded-2xl border shadow-sm transition-all ${
                  simulationResult.delta_annual >= 0
                    ? 'bg-gradient-to-br from-emerald-50/80 via-white to-indigo-50/50 border-emerald-200'
                    : 'bg-rose-50/60 border-rose-200'
                }`}
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                  <div>
                    <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider block">
                      Estimated Net Impact
                    </span>
                    <p
                      className={`text-3xl font-black tracking-tight mt-1 ${
                        simulationResult.delta_annual >= 0 ? 'text-emerald-700' : 'text-rose-700'
                      }`}
                    >
                      {simulationResult.delta_annual >= 0 ? '+' : ''}
                      ₹{simulationResult.delta_annual.toLocaleString('en-IN')}{' '}
                      <span className="text-sm font-semibold">
                        ({simulationResult.percentage_change >= 0 ? '+' : ''}
                        {simulationResult.percentage_change}%)
                      </span>
                    </p>
                    <p className="text-xs text-slate-600 mt-1">
                      Net compensation shift from baseline {simulationResult.original_salary_lpa} LPA to{' '}
                      <span className="font-bold text-slate-900">
                        {simulationResult.counterfactual_salary_lpa} LPA
                      </span>
                    </p>
                  </div>

                  <div className="text-left sm:text-right shrink-0">
                    <Badge
                      variant={simulationResult.delta_annual >= 0 ? 'emerald' : 'rose'}
                      size="md"
                    >
                      {simulationResult.delta_annual >= 0 ? 'Positive ROI' : 'Negative ROI'}
                    </Badge>
                  </div>
                </div>
              </div>

              {/* Comparative Bar Chart */}
              <Card>
                <CardHeader
                  title="Scenario Comparison"
                  subtitle="Baseline vs Simulated Annual Compensation (LPA)"
                  icon={TrendingUp}
                />

                <div className="h-48 w-full mt-4">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart
                      data={chartData}
                      layout="vertical"
                      margin={{ top: 10, right: 30, left: 30, bottom: 5 }}
                    >
                      <XAxis type="number" unit="L" tick={{ fontSize: 11, fill: '#64748b' }} />
                      <YAxis
                        type="category"
                        dataKey="name"
                        tick={{ fontSize: 11, fill: '#1e293b', fontWeight: 600 }}
                        width={120}
                      />
                      <Tooltip
                        formatter={(val, name, item) => [
                          `₹${val} LPA (₹${item.payload.raw.toLocaleString('en-IN')})`,
                          'Salary Median',
                        ]}
                        contentStyle={{
                          borderRadius: '0.75rem',
                          border: '1px solid #e2e8f0',
                          fontSize: '12px',
                        }}
                      />
                      <Bar dataKey="lpa" radius={[0, 6, 6, 0]}>
                        {chartData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} />
                        ))}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </Card>

              {/* Added Skills Impact Breakdown */}
              <Card>
                <CardHeader
                  title="Simulated Skills Summary"
                  subtitle="Evaluated changes in technical capability"
                  icon={Layers}
                />

                <div className="space-y-4 pt-2">
                  <div>
                    <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block mb-1.5">
                      Skills Added ({addSkills.length})
                    </span>
                    <div className="flex flex-wrap gap-1.5">
                      {addSkills.length > 0 ? (
                        addSkills.map((s) => (
                          <span
                            key={s}
                            className="px-2.5 py-1 rounded-lg text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200"
                          >
                            + {s}
                          </span>
                        ))
                      ) : (
                        <span className="text-xs text-slate-400 italic">No skills added in this scenario.</span>
                      )}
                    </div>
                  </div>

                  {removeSkills.length > 0 && (
                    <div>
                      <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block mb-1.5">
                        Skills Removed ({removeSkills.length})
                      </span>
                      <div className="flex flex-wrap gap-1.5">
                        {removeSkills.map((s) => (
                          <span
                            key={s}
                            className="px-2.5 py-1 rounded-lg text-xs font-semibold bg-rose-50 text-rose-800 border border-rose-200"
                          >
                            - {s}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  <div className="p-3 rounded-xl bg-slate-50 border border-slate-100 flex items-start gap-2.5">
                    <Info className="w-4 h-4 text-slate-400 shrink-0 mt-0.5" />
                    <p className="text-[11px] text-slate-500 leading-relaxed">
                      {simulationResult.disclaimer}
                    </p>
                  </div>
                </div>
              </Card>
            </>
          ) : (
            <Card className="p-8 text-center">
              <p className="text-xs text-slate-500">Calculating initial simulation...</p>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
};

export default WhatIfSimulatorPage;
