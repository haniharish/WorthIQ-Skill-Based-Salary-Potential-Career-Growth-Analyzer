import React, { useState, useEffect } from 'react';
import { useSearchParams, Link } from 'react-router-dom';
import {
  Compass,
  CheckCircle2,
  Circle,
  Clock,
  Briefcase,
  Layers,
  ArrowRight,
  Plus,
  Trash2,
  AlertCircle,
  Sparkles,
  Award,
  Code,
  FolderGit2,
  RefreshCw,
} from 'lucide-react';
import { Card, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { useAuth } from '../context/AuthContext';
import { intelligenceService } from '../services/intelligenceService';

export const CareerRoadmapPage = () => {
  const { profile } = useAuth();
  const [searchParams] = useSearchParams();

  const [roadmaps, setRoadmaps] = useState([]);
  const [activeRoadmap, setActiveRoadmap] = useState(null);
  const [rolesCatalog, setRolesCatalog] = useState([]);
  const [loading, setLoading] = useState(true);
  const [updatingSkillId, setUpdatingSkillId] = useState(null);
  const [error, setError] = useState(null);

  // New Roadmap Modal State
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [selectedTargetRole, setSelectedTargetRole] = useState('');
  const [creatingRoadmap, setCreatingRoadmap] = useState(false);

  const fetchRoadmapData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [rListRes, rolesRes] = await Promise.all([
        intelligenceService.getRoadmaps(),
        intelligenceService.getJobRoles(),
      ]);

      const savedList = rListRes.results || [];
      setRoadmaps(savedList);
      setRolesCatalog(rolesRes || []);

      // If role_id passed in URL query param, trigger generation or select
      const queryRoleId = searchParams.get('role_id');
      if (queryRoleId) {
        const foundExisting = savedList.find((r) => String(r.target_role) === String(queryRoleId));
        if (foundExisting) {
          const detail = await intelligenceService.getRoadmapDetail(foundExisting.id);
          setActiveRoadmap(detail);
        } else {
          // Auto-generate for this query role
          const newRm = await intelligenceService.generateRoadmap({
            target_role_id: parseInt(queryRoleId),
          });
          setActiveRoadmap(newRm);
          setRoadmaps((prev) => [newRm, ...prev]);
        }
      } else if (savedList.length > 0) {
        const detail = await intelligenceService.getRoadmapDetail(savedList[0].id);
        setActiveRoadmap(detail);
      }
    } catch (err) {
      console.error('Failed to load roadmap data:', err);
      setError('Unable to load career roadmaps. Please verify your connection.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRoadmapData();
  }, []);

  const handleSelectRoadmap = async (roadmapId) => {
    try {
      const detail = await intelligenceService.getRoadmapDetail(roadmapId);
      setActiveRoadmap(detail);
    } catch (err) {
      console.error('Failed to load roadmap details:', err);
    }
  };

  const handleToggleSkill = async (skillProgressId, currentCompleted) => {
    if (!activeRoadmap) return;
    setUpdatingSkillId(skillProgressId);
    try {
      const res = await intelligenceService.updateRoadmapProgress(activeRoadmap.id, {
        skill_progress_id: skillProgressId,
        is_completed: !currentCompleted,
      });

      if (res?.roadmap) {
        setActiveRoadmap(res.roadmap);
        // Update list overall %
        setRoadmaps((prev) =>
          prev.map((r) =>
            r.id === activeRoadmap.id
              ? { ...r, overall_progress_pct: res.overall_progress_pct }
              : r
          )
        );
      }
    } catch (err) {
      console.error('Failed to update skill progress:', err);
    } finally {
      setUpdatingSkillId(null);
    }
  };

  const handleCreateNewRoadmap = async (e) => {
    e.preventDefault();
    if (!selectedTargetRole) return;

    setCreatingRoadmap(true);
    try {
      const newRm = await intelligenceService.generateRoadmap({
        target_role_id: parseInt(selectedTargetRole),
      });
      setActiveRoadmap(newRm);
      setRoadmaps((prev) => [newRm, ...prev]);
      setShowCreateModal(false);
      setSelectedTargetRole('');
    } catch (err) {
      console.error('Failed to generate roadmap:', err);
      setError('Failed to generate career roadmap. Please try again.');
    } finally {
      setCreatingRoadmap(false);
    }
  };

  const handleDeleteRoadmap = async (roadmapId) => {
    if (!window.confirm('Are you sure you want to delete this career roadmap?')) return;
    try {
      await intelligenceService.deleteRoadmap(roadmapId);
      const remaining = roadmaps.filter((r) => r.id !== roadmapId);
      setRoadmaps(remaining);
      if (remaining.length > 0) {
        handleSelectRoadmap(remaining[0].id);
      } else {
        setActiveRoadmap(null);
      }
    } catch (err) {
      console.error('Failed to delete roadmap:', err);
    }
  };

  return (
    <div className="space-y-8 max-w-6xl mx-auto pb-12">
      {/* Header Banner */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-2 border-b border-slate-200">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-slate-900">
              Personalized Career Growth Roadmaps
            </h1>
            <Badge variant="indigo" size="xs" dot>
              DAG Learning Engine
            </Badge>
          </div>
          <p className="text-sm text-slate-600">
            Acyclic milestone learning paths, real-world project portfolios, and persistent skill mastery tracking.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Button
            variant="primary"
            size="sm"
            icon={Plus}
            onClick={() => setShowCreateModal(true)}
            className="text-xs"
          >
            New Target Roadmap
          </Button>
        </div>
      </div>

      {error && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-sm flex items-start gap-3">
          <AlertCircle className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
          <p className="text-xs">{error}</p>
        </div>
      )}

      {loading ? (
        <div className="space-y-6">
          <div className="h-28 bg-slate-100 rounded-xl animate-pulse" />
          <div className="h-64 bg-slate-100 rounded-xl animate-pulse" />
        </div>
      ) : roadmaps.length === 0 && !activeRoadmap ? (
        // Empty State
        <Card className="p-12 text-center border-dashed border-2 border-slate-200">
          <Compass className="w-12 h-12 text-indigo-500 mx-auto mb-3" />
          <h3 className="text-lg font-bold text-slate-900 mb-1">No Career Roadmaps Created Yet</h3>
          <p className="text-sm text-slate-500 max-w-md mx-auto mb-6">
            Choose a target engineering role to generate a multi-stage skill progression roadmap with practical capstone projects.
          </p>
          <Button
            variant="primary"
            size="md"
            icon={Plus}
            onClick={() => setShowCreateModal(true)}
          >
            Create Your First Roadmap
          </Button>
        </Card>
      ) : (
        <div className="space-y-6">
          {/* Saved Roadmaps Tabs / Pill Selector */}
          {roadmaps.length > 1 && (
            <div className="flex items-center gap-2 overflow-x-auto pb-2 border-b border-slate-100">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider shrink-0 mr-2">
                Your Roadmaps:
              </span>
              {roadmaps.map((r) => (
                <button
                  key={r.id}
                  type="button"
                  onClick={() => handleSelectRoadmap(r.id)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition-colors cursor-pointer flex items-center gap-2 ${
                    activeRoadmap?.id === r.id
                      ? 'bg-indigo-600 text-white shadow-xs'
                      : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                  }`}
                >
                  <span>{r.title}</span>
                  <span
                    className={`text-[10px] px-1.5 py-0.2 rounded-full ${
                      activeRoadmap?.id === r.id
                        ? 'bg-indigo-700 text-white'
                        : 'bg-slate-200 text-slate-700'
                    }`}
                  >
                    {r.overall_progress_pct}%
                  </span>
                </button>
              ))}
            </div>
          )}

          {activeRoadmap && (
            <>
              {/* Active Roadmap Hero Header Card */}
              <Card className="p-6 bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white border-slate-800">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                  <div>
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-xs font-bold text-indigo-300 uppercase tracking-wider">
                        Active Career Path
                      </span>
                      <Badge variant="indigo" size="xs">
                        {activeRoadmap.stages?.length || 4} Milestone Stages
                      </Badge>
                    </div>
                    <h2 className="text-2xl font-black text-white">
                      {activeRoadmap.title}
                    </h2>
                    <p className="text-xs text-slate-400 mt-1">
                      Current: {activeRoadmap.current_role || 'Software Engineer'} ({activeRoadmap.current_experience} yrs exp)
                      &nbsp;→&nbsp; Target: {activeRoadmap.target_role_title}
                    </p>
                  </div>

                  {/* Progress Ring / Percentage Box */}
                  <div className="flex items-center gap-4">
                    <div className="text-right">
                      <span className="text-xs text-slate-400 block">Overall Mastery</span>
                      <span className="text-3xl font-extrabold text-emerald-400">
                        {activeRoadmap.overall_progress_pct}%
                      </span>
                    </div>

                    <Button
                      variant="ghost"
                      size="sm"
                      icon={Trash2}
                      onClick={() => handleDeleteRoadmap(activeRoadmap.id)}
                      className="text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 text-xs"
                      title="Delete this roadmap"
                    />
                  </div>
                </div>

                {/* Progress Bar */}
                <div className="w-full bg-slate-800 rounded-full h-2.5 mt-5 overflow-hidden">
                  <div
                    className="h-2.5 rounded-full bg-gradient-to-r from-indigo-500 to-emerald-400 transition-all duration-300"
                    style={{ width: `${activeRoadmap.overall_progress_pct}%` }}
                  />
                </div>
              </Card>

              {/* Milestone Stages Timeline */}
              <div className="space-y-6">
                {(activeRoadmap.stages || []).map((stage) => {
                  const completedSkillsCount = (stage.skills_progress || []).filter(
                    (s) => s.is_completed
                  ).length;
                  const totalSkillsCount = (stage.skills_progress || []).length;
                  const stageAllDone = totalSkillsCount > 0 && completedSkillsCount === totalSkillsCount;

                  return (
                    <Card
                      key={stage.id}
                      className={`p-6 border transition-all duration-200 ${
                        stageAllDone
                          ? 'border-emerald-200 bg-emerald-50/15'
                          : 'border-slate-200 bg-white'
                      }`}
                    >
                      {/* Stage Header */}
                      <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3 pb-4 border-b border-slate-100">
                        <div className="flex items-start gap-3">
                          <div
                            className={`w-9 h-9 rounded-xl flex items-center justify-center font-bold text-sm shrink-0 ${
                              stageAllDone
                                ? 'bg-emerald-100 text-emerald-700'
                                : 'bg-indigo-100 text-indigo-700'
                            }`}
                          >
                            {stageAllDone ? <CheckCircle2 className="w-5 h-5" /> : stage.stage_number}
                          </div>
                          <div>
                            <div className="flex items-center gap-2">
                              <h3 className="text-base font-bold text-slate-900">{stage.title}</h3>
                              {stageAllDone && (
                                <Badge variant="emerald" size="xs">
                                  Stage Completed
                                </Badge>
                              )}
                            </div>
                            <p className="text-xs text-slate-500 mt-0.5">{stage.objective}</p>
                          </div>
                        </div>

                        <div className="text-xs text-slate-400 font-medium whitespace-nowrap">
                          {completedSkillsCount} / {totalSkillsCount} skills mastered
                        </div>
                      </div>

                      {/* Skills Checklist */}
                      <div className="py-4">
                        <span className="text-[11px] font-bold uppercase tracking-wider text-slate-500 block mb-2.5">
                          Target Skills in this Milestone:
                        </span>

                        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-2.5">
                          {(stage.skills_progress || []).map((skill) => (
                            <button
                              key={skill.id}
                              type="button"
                              onClick={() => handleToggleSkill(skill.id, skill.is_completed)}
                              disabled={updatingSkillId === skill.id}
                              className={`p-2.5 rounded-lg border text-left flex items-center justify-between gap-2 text-xs transition-all duration-150 cursor-pointer ${
                                skill.is_completed
                                  ? 'bg-emerald-50 text-emerald-900 border-emerald-200'
                                  : 'bg-slate-50/70 text-slate-700 border-slate-200 hover:border-indigo-300'
                              }`}
                            >
                              <div className="flex items-center gap-2">
                                {skill.is_completed ? (
                                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                                ) : (
                                  <Circle className="w-4 h-4 text-slate-300 shrink-0" />
                                )}
                                <span className={`font-semibold ${skill.is_completed ? 'line-through text-slate-400' : ''}`}>
                                  {skill.skill_name}
                                </span>
                              </div>

                              <span
                                className={`text-[10px] px-1.5 py-0.5 rounded font-medium ${
                                  skill.importance === 'Mandatory'
                                    ? 'bg-rose-100/60 text-rose-700'
                                    : 'bg-slate-200/60 text-slate-600'
                                }`}
                              >
                                {skill.importance}
                              </span>
                            </button>
                          ))}
                        </div>
                      </div>

                      {/* Practical Project Recommendation Box */}
                      {stage.project_suggestion && stage.project_suggestion.title && (
                        <div className="mt-2 p-4 rounded-xl bg-slate-50 border border-slate-200 text-xs space-y-2">
                          <div className="flex items-center gap-2 font-bold text-slate-800">
                            <Code className="w-4 h-4 text-indigo-600" />
                            <span>Recommended Capstone Project: {stage.project_suggestion.title}</span>
                          </div>
                          <div className="text-slate-600 leading-relaxed">
                            <strong className="text-slate-700">Tech Stack:</strong>{' '}
                            {stage.project_suggestion.stack}
                          </div>
                          <div className="text-slate-600 leading-relaxed">
                            <strong className="text-slate-700">Deliverables:</strong>{' '}
                            {stage.project_suggestion.deliverables}
                          </div>
                          <div className="text-emerald-700 leading-relaxed font-medium">
                            <strong>Completion Standard:</strong>{' '}
                            {stage.project_suggestion.completion_criteria}
                          </div>
                        </div>
                      )}
                    </Card>
                  );
                })}
              </div>
            </>
          )}
        </div>
      )}

      {/* New Roadmap Modal */}
      {showCreateModal && (
        <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="relative bg-white rounded-2xl max-w-md w-full p-6 shadow-xl border border-slate-200 animate-in fade-in zoom-in-95 duration-150">
            <h3 className="text-lg font-bold text-slate-900 mb-1">
              Create New Career Roadmap
            </h3>
            <p className="text-xs text-slate-500 mb-4">
              Select your desired target engineering role. The DAG engine will construct milestone stages and capstone projects based on your current skill profile.
            </p>

            <form onSubmit={handleCreateNewRoadmap} className="space-y-4">
              <div>
                <label className="text-xs font-semibold text-slate-700 uppercase tracking-wider block mb-1.5">
                  Target Technology Role
                </label>
                <select
                  value={selectedTargetRole}
                  onChange={(e) => setSelectedTargetRole(e.target.value)}
                  className="w-full rounded-lg text-sm bg-white border border-slate-300 py-2.5 px-3 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  required
                >
                  <option value="">-- Choose a Target Role --</option>
                  {rolesCatalog.map((role) => (
                    <option key={role.id} value={role.id}>
                      {role.title} (Median: ₹{(role.median_salary / 100000).toFixed(1)} LPA)
                    </option>
                  ))}
                </select>
              </div>

              <div className="pt-3 border-t border-slate-100 flex items-center justify-end gap-2">
                <Button
                  type="button"
                  variant="secondary"
                  size="sm"
                  onClick={() => setShowCreateModal(false)}
                >
                  Cancel
                </Button>
                <Button
                  type="submit"
                  variant="primary"
                  size="sm"
                  isLoading={creatingRoadmap}
                  disabled={!selectedTargetRole}
                >
                  Generate Roadmap
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default CareerRoadmapPage;
