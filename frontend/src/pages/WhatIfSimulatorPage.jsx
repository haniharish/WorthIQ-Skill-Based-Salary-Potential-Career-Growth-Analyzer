import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';
import { scenarioService } from '../services/scenarioService';
import { reportService } from '../services/reportService';
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
  Copy,
  Save,
  Download,
  RefreshCw,
  Info,
  CheckCircle2,
  Briefcase,
  MapPin,
  Layers,
  GraduationCap,
  Calendar,
  AlertCircle,
  BarChart2,
  BookmarkCheck,
} from 'lucide-react';
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  Cell,
  CartesianGrid,
} from 'recharts';

const STANDARD_ROLES = [
  'Full Stack Developer',
  'Backend Developer',
  'Frontend Developer',
  'DevOps Engineer',
  'Data Scientist',
  'Machine Learning Engineer',
  'Data Analyst',
  'Cloud Architect',
  'Software Developer',
];

const STANDARD_LOCATIONS = [
  'Bengaluru',
  'Hyderabad',
  'Pune',
  'Mumbai',
  'Delhi NCR',
  'Chennai',
  'Kolkata',
  'Remote',
];

const STANDARD_EDUCATION = [
  "Bachelor's Degree",
  "Master's Degree",
  'B.Tech / B.E.',
  'M.Tech / M.E.',
  'MCA',
  'BCA / B.Sc',
  'Doctorate / Ph.D',
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
  'Kafka',
  'GraphQL',
];

export const WhatIfSimulatorPage = () => {
  const { profile } = useAuth();
  const toast = useToast();

  // Baseline Profile state
  const [baselineRole, setBaselineRole] = useState('Full Stack Developer');
  const [baselineExp, setBaselineExp] = useState(2.0);
  const [baselineLoc, setBaselineLoc] = useState('Delhi NCR');
  const [baselineEdu, setBaselineEdu] = useState("Bachelor's Degree");
  const [baselineSkills, setBaselineSkills] = useState(['Python', 'React.js', 'PostgreSQL']);

  // Active Simulation / Target Scenario state
  const [scenarioName, setScenarioName] = useState('Upskill & Relocate Scenario');
  const [targetRole, setTargetRole] = useState('Full Stack Developer');
  const [targetExp, setTargetExp] = useState(3.0);
  const [targetLoc, setTargetLoc] = useState('Bengaluru');
  const [targetEdu, setTargetEdu] = useState("Bachelor's Degree");
  const [targetSkills, setTargetSkills] = useState(['Python', 'React.js', 'PostgreSQL', 'Docker', 'AWS']);
  const [scenarioNotes, setScenarioNotes] = useState('');

  // Taxonomies and catalogs
  const [availableSkills, setAvailableSkills] = useState(HIGH_LEVERAGE_SKILLS);

  // Saved scenarios state
  const [savedScenarios, setSavedScenarios] = useState([]);
  const [selectedScenarioIds, setSelectedScenarioIds] = useState([]);
  const [loadingScenarios, setLoadingScenarios] = useState(false);

  // Simulation execution state
  const [simulating, setSimulating] = useState(false);
  const [comparisonResult, setComparisonResult] = useState(null);
  const [savingScenario, setSavingScenario] = useState(false);

  // Initialize from user profile
  useEffect(() => {
    if (profile) {
      const pRole = profile.job_role || 'Full Stack Developer';
      const pExp = profile.years_of_experience ? Number(profile.years_of_experience) : 2.0;
      const pLoc = profile.location || 'Delhi NCR';
      const pEdu = profile.education || "Bachelor's Degree";
      const pSkills = profile.skills && profile.skills.length > 0
        ? profile.skills.map((s) => (typeof s === 'string' ? s : s.name))
        : ['Python', 'React.js', 'PostgreSQL'];

      setBaselineRole(pRole);
      setBaselineExp(pExp);
      setBaselineLoc(pLoc);
      setBaselineEdu(pEdu);
      setBaselineSkills(pSkills);

      // Default target scenario starts as baseline + high-leverage skills
      setTargetRole(pRole);
      setTargetExp(pExp + 1);
      setTargetLoc(pLoc);
      setTargetEdu(pEdu);
      setTargetSkills(Array.from(new Set([...pSkills, 'Docker', 'AWS'])));
    }
  }, [profile]);

  // Load skills taxonomy
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

  // Fetch saved scenarios
  const fetchScenarios = async () => {
    setLoadingScenarios(true);
    try {
      const data = await scenarioService.getScenarios();
      setSavedScenarios(data || []);
    } catch (err) {
      console.warn('Could not fetch saved scenarios', err);
    } finally {
      setLoadingScenarios(false);
    }
  };

  useEffect(() => {
    fetchScenarios();
  }, []);

  // Run simulation comparison between Baseline and active target scenario
  const handleRunSimulation = async () => {
    setSimulating(true);
    try {
      const payload = {
        baseline: {
          job_role: baselineRole,
          years_of_experience: Number(baselineExp),
          location: baselineLoc,
          education: baselineEdu,
          skills: baselineSkills,
        },
        scenarios: [
          {
            name: scenarioName || 'Simulated Scenario',
            job_role: targetRole,
            years_of_experience: Number(targetExp),
            location: targetLoc,
            education: targetEdu,
            skills: targetSkills,
          },
        ],
        scenario_ids: selectedScenarioIds,
      };

      const result = await scenarioService.compareScenarios(payload);
      setComparisonResult(result);
      toast.success('Simulation updated successfully!');
    } catch (err) {
      console.error('Simulation comparison failed:', err);
      toast.error('Simulation calculation failed. Please check your inputs.');
    } finally {
      setSimulating(false);
    }
  };

  // Run initial simulation once baseline is populated
  useEffect(() => {
    handleRunSimulation();
  }, [baselineRole, baselineExp, baselineLoc]);

  // Save active scenario to PostgreSQL
  const handleSaveScenario = async () => {
    if (!scenarioName.trim()) {
      toast.error('Please enter a scenario name before saving.');
      return;
    }
    setSavingScenario(true);
    try {
      await scenarioService.createScenario({
        name: scenarioName,
        job_role: targetRole,
        years_of_experience: Number(targetExp),
        location: targetLoc,
        education: targetEdu,
        skills: targetSkills,
        notes: scenarioNotes,
      });
      toast.success(`Scenario "${scenarioName}" saved!`);
      await fetchScenarios();
    } catch (err) {
      console.error('Failed to save scenario:', err);
      toast.error('Could not save scenario. Please try again.');
    } finally {
      setSavingScenario(false);
    }
  };

  // Delete scenario
  const handleDeleteScenario = async (id, name) => {
    if (!window.confirm(`Delete scenario "${name}"?`)) return;
    try {
      await scenarioService.deleteScenario(id);
      toast.success('Scenario deleted.');
      setSelectedScenarioIds((prev) => prev.filter((item) => item !== id));
      await fetchScenarios();
    } catch (err) {
      toast.error('Failed to delete scenario.');
    }
  };

  // Duplicate scenario
  const handleDuplicateScenario = async (id) => {
    try {
      await scenarioService.duplicateScenario(id);
      toast.success('Scenario duplicated.');
      await fetchScenarios();
    } catch (err) {
      toast.error('Failed to duplicate scenario.');
    }
  };

  // Load a saved scenario into active editor
  const handleLoadScenario = (sc) => {
    setScenarioName(`${sc.name} (Copy)`);
    setTargetRole(sc.job_role);
    setTargetExp(sc.years_of_experience);
    setTargetLoc(sc.location);
    setTargetEdu(sc.education);
    setTargetSkills(sc.skills || []);
    setScenarioNotes(sc.notes || '');
    toast.info(`Loaded "${sc.name}" into editor.`);
  };

  // Toggle scenario inclusion in multi-comparison
  const toggleScenarioSelection = (id) => {
    setSelectedScenarioIds((prev) => {
      if (prev.includes(id)) {
        return prev.filter((item) => item !== id);
      }
      if (prev.length >= 3) {
        toast.warning('Maximum 3 saved scenarios can be compared simultaneously with baseline.');
        return prev;
      }
      return [...prev, id];
    });
  };

  // Re-run simulation when selected scenarios change
  useEffect(() => {
    if (selectedScenarioIds.length > 0) {
      handleRunSimulation();
    }
  }, [selectedScenarioIds]);

  // Export scenarios to CSV
  const handleExportCsv = async () => {
    try {
      await reportService.exportCsv('scenarios');
      toast.success('Scenarios exported to CSV.');
    } catch (err) {
      toast.error('Failed to export scenarios.');
    }
  };

  // Quick helper to add skill to target
  const handleAddQuickSkill = (skill) => {
    if (!targetSkills.includes(skill)) {
      setTargetSkills([...targetSkills, skill]);
    }
  };

  // Chart data extraction
  const baselineData = comparisonResult?.baseline;
  const scenariosData = comparisonResult?.scenarios || [];

  // Prepare Recharts bar data
  const chartData = [];
  if (baselineData) {
    chartData.push({
      name: 'Baseline Profile',
      p10: baselineData.prediction?.p10_lpa || 0,
      p50: baselineData.prediction?.p50_lpa || 0,
      p90: baselineData.prediction?.p90_lpa || 0,
      isBaseline: true,
    });
  }
  scenariosData.forEach((sc) => {
    chartData.push({
      name: sc.name.length > 18 ? sc.name.slice(0, 16) + '...' : sc.name,
      fullName: sc.name,
      p10: sc.prediction?.p10_lpa || 0,
      p50: sc.prediction?.p50_lpa || 0,
      p90: sc.prediction?.p90_lpa || 0,
      deltaP50: sc.delta_vs_baseline?.delta_p50_lpa || 0,
      isBaseline: false,
    });
  });

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-16">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-200">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-slate-900">
              What-If Salary Simulator
            </h1>
            <Badge variant="primary" size="sm">Advanced</Badge>
          </div>
          <p className="text-xs sm:text-sm text-slate-600">
            Simulate, compare, and save multi-variable career trajectories with quantile salary bounds (P10, P50, P90).
          </p>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            icon={Download}
            onClick={handleExportCsv}
          >
            Export CSV
          </Button>
          <Button
            variant="primary"
            size="sm"
            icon={RefreshCw}
            onClick={handleRunSimulation}
            isLoading={simulating}
          >
            Run Simulation
          </Button>
        </div>
      </div>

      {/* Main Grid: Left Controls & Saved Scenarios, Right Live Comparison */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Column (5 cols): Baseline Card & Scenario Editor */}
        <div className="lg:col-span-5 space-y-6">
          
          {/* Active Target Scenario Editor */}
          <Card className="border-indigo-100 shadow-sm">
            <CardHeader
              title="Scenario Simulation Lab"
              subtitle="Hypothesize new skills, roles, experience or relocation"
              icon={Sliders}
            />

            <div className="space-y-4 pt-2">
              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Scenario Name
                </label>
                <input
                  type="text"
                  value={scenarioName}
                  onChange={(e) => setScenarioName(e.target.value)}
                  placeholder="e.g. Senior DevOps + Kubernetes in Bengaluru"
                  className="w-full text-sm px-3 py-2 border border-slate-300 rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <SelectInput
                  label="Target Job Role"
                  value={targetRole}
                  onChange={(e) => setTargetRole(e.target.value)}
                  options={STANDARD_ROLES}
                />
                <SelectInput
                  label="Target Location"
                  value={targetLoc}
                  onChange={(e) => setTargetLoc(e.target.value)}
                  options={STANDARD_LOCATIONS}
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <div className="flex justify-between items-center mb-1">
                    <label className="text-xs font-semibold text-slate-700">
                      Experience: {targetExp} yrs
                    </label>
                    <span className="text-[10px] text-indigo-600 font-medium">
                      {targetExp > baselineExp ? `+${(targetExp - baselineExp).toFixed(1)} yrs` : ''}
                    </span>
                  </div>
                  <input
                    type="range"
                    min="0"
                    max="20"
                    step="0.5"
                    value={targetExp}
                    onChange={(e) => setTargetExp(parseFloat(e.target.value))}
                    className="w-full accent-indigo-600 cursor-pointer"
                  />
                </div>
                <SelectInput
                  label="Education Level"
                  value={targetEdu}
                  onChange={(e) => setTargetEdu(e.target.value)}
                  options={STANDARD_EDUCATION}
                />
              </div>

              <SkillTagInput
                label="Target Technical Skills"
                skills={targetSkills}
                onChange={setTargetSkills}
                suggestions={availableSkills}
                placeholder="Type and press enter..."
              />

              {/* Quick high-leverage skill recommendations */}
              <div>
                <label className="block text-[11px] font-semibold text-slate-500 uppercase tracking-wider mb-1.5">
                  Recommended High-Leverage Skills
                </label>
                <div className="flex flex-wrap gap-1.5">
                  {HIGH_LEVERAGE_SKILLS.slice(0, 8).map((sk) => {
                    const isSelected = targetSkills.includes(sk);
                    return (
                      <button
                        key={sk}
                        type="button"
                        onClick={() => handleAddQuickSkill(sk)}
                        disabled={isSelected}
                        className={`text-xs px-2.5 py-1 rounded-full border transition-all ${
                          isSelected
                            ? 'bg-slate-100 text-slate-400 border-slate-200 cursor-default'
                            : 'bg-indigo-50/50 text-indigo-700 border-indigo-200 hover:bg-indigo-100 hover:border-indigo-300'
                        }`}
                      >
                        {isSelected ? '✓ ' : '+ '}
                        {sk}
                      </button>
                    );
                  })}
                </div>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-700 mb-1">
                  Notes / Career Strategy (Optional)
                </label>
                <textarea
                  rows={2}
                  value={scenarioNotes}
                  onChange={(e) => setScenarioNotes(e.target.value)}
                  placeholder="e.g. Plan to take CKA certification and transition by Q3..."
                  className="w-full text-xs px-3 py-2 border border-slate-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>

              {/* Save & Run Buttons */}
              <div className="pt-2 flex items-center justify-between gap-3">
                <Button
                  variant="outline"
                  size="sm"
                  icon={Save}
                  onClick={handleSaveScenario}
                  isLoading={savingScenario}
                >
                  Save Scenario
                </Button>
                <Button
                  variant="primary"
                  size="sm"
                  icon={TrendingUp}
                  onClick={handleRunSimulation}
                  isLoading={simulating}
                >
                  Recalculate
                </Button>
              </div>
            </div>
          </Card>

          {/* Baseline Profile Summary Card */}
          <Card className="bg-slate-50/70 border-slate-200">
            <CardHeader
              title="Baseline Candidate Benchmark"
              subtitle="Current baseline profile anchor"
              icon={Briefcase}
            />
            <div className="text-xs text-slate-600 space-y-2 pt-1">
              <div className="flex justify-between py-1 border-b border-slate-200">
                <span className="font-medium text-slate-500">Current Role:</span>
                <span className="font-semibold text-slate-800">{baselineRole}</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-200">
                <span className="font-medium text-slate-500">Experience & Location:</span>
                <span className="font-semibold text-slate-800">{baselineExp} yrs • {baselineLoc}</span>
              </div>
              <div className="py-1">
                <span className="font-medium text-slate-500 block mb-1">Active Skills ({baselineSkills.length}):</span>
                <div className="flex flex-wrap gap-1">
                  {baselineSkills.map((s) => (
                    <span key={s} className="px-2 py-0.5 bg-white border border-slate-200 rounded text-[11px] text-slate-700">
                      {s}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          </Card>

          {/* Saved Scenarios Library */}
          <Card>
            <div className="flex items-center justify-between pb-3 border-b border-slate-200">
              <div className="flex items-center gap-2">
                <BookmarkCheck className="w-4 h-4 text-indigo-600" />
                <h3 className="text-sm font-bold text-slate-800">Saved Scenarios</h3>
              </div>
              <span className="text-xs text-slate-500">
                {savedScenarios.length} saved
              </span>
            </div>

            <div className="pt-3 space-y-2 max-h-64 overflow-y-auto">
              {savedScenarios.length === 0 ? (
                <p className="text-xs text-slate-400 italic py-2 text-center">
                  No saved scenarios yet. Configure a scenario above and click "Save Scenario".
                </p>
              ) : (
                savedScenarios.map((sc) => {
                  const isChecked = selectedScenarioIds.includes(sc.id);
                  return (
                    <div
                      key={sc.id}
                      className={`p-2.5 rounded-lg border text-xs transition-all ${
                        isChecked
                          ? 'border-indigo-400 bg-indigo-50/50'
                          : 'border-slate-200 hover:border-slate-300 bg-white'
                      }`}
                    >
                      <div className="flex items-start justify-between gap-2">
                        <div className="flex items-start gap-2">
                          <input
                            type="checkbox"
                            checked={isChecked}
                            onChange={() => toggleScenarioSelection(sc.id)}
                            className="mt-0.5 h-3.5 w-3.5 text-indigo-600 rounded border-slate-300"
                            title="Select to compare in chart"
                          />
                          <div>
                            <div className="font-bold text-slate-900">{sc.name}</div>
                            <div className="text-[11px] text-slate-500">
                              {sc.job_role} • {sc.years_of_experience} yrs • {sc.location}
                            </div>
                            <div className="text-[10px] text-slate-400 mt-0.5">
                              P50: ₹{sc.prediction_snapshot?.p50_lpa || '—'} LPA ({sc.skills?.length || 0} skills)
                            </div>
                          </div>
                        </div>

                        <div className="flex items-center gap-1 shrink-0">
                          <button
                            type="button"
                            onClick={() => handleLoadScenario(sc)}
                            title="Load into editor"
                            className="p-1 text-slate-400 hover:text-indigo-600 rounded"
                          >
                            <Sliders className="w-3.5 h-3.5" />
                          </button>
                          <button
                            type="button"
                            onClick={() => handleDuplicateScenario(sc.id)}
                            title="Duplicate scenario"
                            className="p-1 text-slate-400 hover:text-emerald-600 rounded"
                          >
                            <Copy className="w-3.5 h-3.5" />
                          </button>
                          <button
                            type="button"
                            onClick={() => handleDeleteScenario(sc.id, sc.name)}
                            title="Delete scenario"
                            className="p-1 text-slate-400 hover:text-rose-600 rounded"
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
            {savedScenarios.length > 0 && (
              <p className="text-[10px] text-slate-400 pt-2 border-t border-slate-100">
                Check boxes above to compare up to 3 saved scenarios side-by-side with your active simulation.
              </p>
            )}
          </Card>

        </div>

        {/* Right Column (7 cols): Comparative Analytics & Visualization */}
        <div className="lg:col-span-7 space-y-6">

          {/* Quick Metrics Cards */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <StatCard
              title="Baseline Market Median"
              value={`₹${baselineData?.prediction?.p50_lpa || '—'} LPA`}
              subtitle={`Conservative: ₹${baselineData?.prediction?.p10_lpa || '—'}L`}
              icon={Briefcase}
            />
            <StatCard
              title="Simulated Scenario (P50)"
              value={`₹${scenariosData[0]?.prediction?.p50_lpa || '—'} LPA`}
              subtitle={`Top Tier: ₹${scenariosData[0]?.prediction?.p90_lpa || '—'}L`}
              icon={TrendingUp}
            />
            <StatCard
              title="Potential Delta"
              value={`${(scenariosData[0]?.delta_vs_baseline?.delta_p50_lpa || 0) >= 0 ? '+' : ''}₹${scenariosData[0]?.delta_vs_baseline?.delta_p50_lpa || '0'} LPA`}
              subtitle={`${(scenariosData[0]?.delta_vs_baseline?.percentage_change || 0) >= 0 ? '+' : ''}${scenariosData[0]?.delta_vs_baseline?.percentage_change || 0}% change`}
              icon={Sparkles}
            />
          </div>

          {/* Recharts Quantile Comparison Chart */}
          <Card>
            <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-4 border-b border-slate-200 gap-2">
              <div>
                <h3 className="text-base font-bold text-slate-900">
                  Quantile Market Distribution Comparison
                </h3>
                <p className="text-xs text-slate-500">
                  Evaluating P10 (Conservative), P50 (Median), and P90 (Top Tier) bounds in LPA
                </p>
              </div>
              <Badge variant="outline" size="sm">
                Random Forest ML 2.0
              </Badge>
            </div>

            <div className="h-72 w-full pt-4">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={chartData}
                  margin={{ top: 10, right: 20, left: 0, bottom: 25 }}
                >
                  <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" vertical={false} />
                  <XAxis
                    dataKey="name"
                    tick={{ fill: '#64748b', fontSize: 11 }}
                    interval={0}
                  />
                  <YAxis
                    unit=" L"
                    tick={{ fill: '#64748b', fontSize: 11 }}
                    domain={[0, 'auto']}
                  />
                  <Tooltip
                    content={({ active, payload }) => {
                      if (!active || !payload || !payload.length) return null;
                      const d = payload[0].payload;
                      return (
                        <div className="bg-slate-900 text-white text-xs p-3 rounded-lg shadow-xl space-y-1">
                          <div className="font-bold text-indigo-300 pb-1 border-b border-slate-700">
                            {d.fullName || d.name}
                          </div>
                          <div>P10 (Conservative): <span className="font-mono text-emerald-400">₹{d.p10} LPA</span></div>
                          <div>P50 (Market Median): <span className="font-mono text-indigo-400 font-bold">₹{d.p50} LPA</span></div>
                          <div>P90 (Top Tier): <span className="font-mono text-amber-400">₹{d.p90} LPA</span></div>
                          {d.deltaP50 !== undefined && (
                            <div className="pt-1 text-[11px] text-slate-300 border-t border-slate-700">
                              Delta vs Baseline: <span className="font-bold">{d.deltaP50 >= 0 ? `+₹${d.deltaP50} LPA` : `-₹${Math.abs(d.deltaP50)} LPA`}</span>
                            </div>
                          )}
                        </div>
                      );
                    }}
                  />
                  <Legend
                    wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }}
                  />
                  <Bar dataKey="p10" name="P10 (Conservative)" fill="#94a3b8" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="p50" name="P50 (Median Market)" fill="#6366f1" radius={[4, 4, 0, 0]} />
                  <Bar dataKey="p90" name="P90 (Top Tier)" fill="#10b981" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </Card>

          {/* Scenario Comparison Breakdown Table */}
          <Card>
            <div className="flex items-center justify-between pb-3 border-b border-slate-200">
              <h3 className="text-sm font-bold text-slate-900">
                Detailed Trajectory Matrix
              </h3>
              <span className="text-xs text-slate-500">
                {scenariosData.length + 1} Profile Vectors Evaluated
              </span>
            </div>

            <div className="overflow-x-auto pt-2">
              <table className="w-full text-xs text-left">
                <thead>
                  <tr className="border-b border-slate-200 text-slate-500 font-semibold">
                    <th className="py-2 px-3">Profile / Scenario</th>
                    <th className="py-2 px-2">Role & Exp</th>
                    <th className="py-2 px-2">Location</th>
                    <th className="py-2 px-2 text-right">P10</th>
                    <th className="py-2 px-2 text-right">P50 (Median)</th>
                    <th className="py-2 px-2 text-right">P90</th>
                    <th className="py-2 px-3 text-right">Delta</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {/* Baseline Row */}
                  <tr className="bg-slate-50/50 font-medium">
                    <td className="py-2.5 px-3">
                      <span className="inline-flex items-center gap-1.5 font-bold text-slate-800">
                        <span className="w-2 h-2 rounded-full bg-slate-400"></span>
                        Baseline Profile
                      </span>
                    </td>
                    <td className="py-2.5 px-2 text-slate-600">{baselineRole} ({baselineExp}y)</td>
                    <td className="py-2.5 px-2 text-slate-600">{baselineLoc}</td>
                    <td className="py-2.5 px-2 text-right font-mono text-slate-600">₹{baselineData?.prediction?.p10_lpa || '—'}L</td>
                    <td className="py-2.5 px-2 text-right font-mono font-bold text-slate-900">₹{baselineData?.prediction?.p50_lpa || '—'}L</td>
                    <td className="py-2.5 px-2 text-right font-mono text-slate-600">₹{baselineData?.prediction?.p90_lpa || '—'}L</td>
                    <td className="py-2.5 px-3 text-right text-slate-400 font-mono">—</td>
                  </tr>

                  {/* Scenarios Rows */}
                  {scenariosData.map((sc, index) => {
                    const delta = sc.delta_vs_baseline?.delta_p50_lpa || 0;
                    const isPositive = delta >= 0;
                    return (
                      <tr key={index} className="hover:bg-indigo-50/30 transition-colors">
                        <td className="py-2.5 px-3">
                          <span className="inline-flex items-center gap-1.5 font-semibold text-slate-900">
                            <span className="w-2 h-2 rounded-full bg-indigo-600"></span>
                            {sc.name}
                          </span>
                        </td>
                        <td className="py-2.5 px-2 text-slate-600">{sc.profile?.job_role} ({sc.profile?.years_of_experience}y)</td>
                        <td className="py-2.5 px-2 text-slate-600">{sc.profile?.location}</td>
                        <td className="py-2.5 px-2 text-right font-mono text-slate-600">₹{sc.prediction?.p10_lpa}L</td>
                        <td className="py-2.5 px-2 text-right font-mono font-bold text-indigo-700">₹{sc.prediction?.p50_lpa}L</td>
                        <td className="py-2.5 px-2 text-right font-mono text-slate-600">₹{sc.prediction?.p90_lpa}L</td>
                        <td className="py-2.5 px-3 text-right font-mono font-bold">
                          <span className={isPositive ? 'text-emerald-600' : 'text-rose-600'}>
                            {isPositive ? '+' : ''}₹{delta}L
                          </span>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </Card>

          {/* Statistical Non-Causality Disclaimer Alert */}
          <div className="p-4 bg-amber-50/70 border border-amber-200 rounded-xl flex items-start gap-3">
            <Info className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
            <div className="text-xs text-amber-800 space-y-1">
              <span className="font-bold">Non-Causality & Methodology Notice:</span>
              <p>
                WorthIQ simulation models evaluate correlation patterns observed across 25,000+ technology employment records. Salary bounds are statistical estimates (P10 conservative, P50 median, P90 top-tier) and do not guarantee identical compensation offers from employers. Real offers depend on interview performance, company tier, negotiation, and economic conditions.
              </p>
            </div>
          </div>

        </div>

      </div>
    </div>
  );
};

export default WhatIfSimulatorPage;
