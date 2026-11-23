import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  BookmarkCheck,
  Calendar,
  Briefcase,
  MapPin,
  TrendingUp,
  Eye,
  X,
  ChevronLeft,
  ChevronRight,
  AlertCircle,
  Clock,
  Sparkles,
  ArrowRight,
  Layers,
  Award,
  RefreshCw,
} from 'lucide-react';
import { Card, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { predictionService } from '../services/predictionService';

export const SavedReportsPage = () => {
  const [historyData, setHistoryData] = useState({
    count: 0,
    next: null,
    previous: null,
    results: [],
  });
  const [currentPage, setCurrentPage] = useState(1);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedReport, setSelectedReport] = useState(null);
  const [modalLoading, setModalLoading] = useState(false);

  const fetchHistory = async (page = 1) => {
    setLoading(true);
    setError(null);
    try {
      const data = await predictionService.getPredictionHistory(page);
      setHistoryData(data);
      setCurrentPage(page);
    } catch (err) {
      console.error('Failed to fetch prediction history:', err);
      setError('Unable to load prediction history. Please verify your connection and try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory(1);
  }, []);

  const handleOpenDetail = async (reportId) => {
    setModalLoading(true);
    try {
      const detail = await predictionService.getPredictionDetail(reportId);
      setSelectedReport(detail);
    } catch (err) {
      console.error('Failed to load prediction details:', err);
      // Fallback to item in results if detail fails
      const fallback = historyData.results.find((r) => r.id === reportId);
      setSelectedReport(fallback || null);
    } finally {
      setModalLoading(false);
    }
  };

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

  const totalPages = Math.ceil((historyData.count || 0) / 10) || 1;

  return (
    <div className="space-y-6 max-w-6xl mx-auto pb-12">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-2 border-b border-slate-200">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <h1 className="text-2xl sm:text-3xl font-bold tracking-tight text-slate-900">
              Saved Reports & History
            </h1>
            <Badge variant="indigo" size="xs">
              {historyData.count} Evaluations
            </Badge>
          </div>
          <p className="text-sm text-slate-600">
            Historical log of your salary predictions, quantile spreads, and career milestone assessments.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <Button
            variant="outline"
            size="sm"
            icon={RefreshCw}
            onClick={() => fetchHistory(currentPage)}
            disabled={loading}
            className="text-xs"
          >
            Refresh
          </Button>
          <Link to="/salary-analysis">
            <Button variant="primary" size="sm" icon={TrendingUp} className="text-xs">
              New Prediction
            </Button>
          </Link>
        </div>
      </div>

      {/* Error Notice */}
      {error && (
        <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-sm flex items-start justify-between gap-3">
          <div className="flex items-start gap-2.5">
            <AlertCircle className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold">Failed to Load Reports</p>
              <p className="text-rose-700 text-xs mt-0.5">{error}</p>
            </div>
          </div>
          <Button variant="outline" size="sm" onClick={() => fetchHistory(currentPage)}>
            Retry
          </Button>
        </div>
      )}

      {/* Main Content Area */}
      {loading ? (
        // Loading Skeletons
        <div className="space-y-3">
          {[1, 2, 3, 4].map((i) => (
            <div
              key={i}
              className="p-5 rounded-xl border border-slate-200 bg-white animate-pulse flex flex-col sm:flex-row sm:items-center justify-between gap-4"
            >
              <div className="space-y-2 flex-1">
                <div className="h-4 bg-slate-200 rounded w-1/4" />
                <div className="h-3 bg-slate-100 rounded w-1/2" />
                <div className="h-3 bg-slate-100 rounded w-1/3" />
              </div>
              <div className="h-8 bg-slate-200 rounded w-24" />
            </div>
          ))}
        </div>
      ) : historyData.results.length === 0 ? (
        // Empty State
        <Card className="p-12 text-center border-dashed border-2 border-slate-200 bg-slate-50/50">
          <div className="w-14 h-14 rounded-2xl bg-indigo-100 text-indigo-600 flex items-center justify-center mx-auto mb-4 shadow-xs">
            <BookmarkCheck className="w-7 h-7" />
          </div>
          <h3 className="text-lg font-bold text-slate-900 mb-1">
            No Salary Predictions Yet
          </h3>
          <p className="text-sm text-slate-500 max-w-md mx-auto mb-6">
            Run a salary evaluation on your technical skills and experience to save benchmark reports, track salary milestones, and compare market percentiles.
          </p>
          <Link to="/salary-analysis">
            <Button variant="primary" size="md" icon={TrendingUp}>
              Evaluate Salary Potential Now
            </Button>
          </Link>
        </Card>
      ) : (
        // History List / Table
        <div className="space-y-4">
          <div className="overflow-hidden bg-white rounded-xl border border-slate-200/90 shadow-xs">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="bg-slate-50/75 border-b border-slate-200 text-xs font-semibold uppercase tracking-wider text-slate-500">
                  <tr>
                    <th scope="col" className="px-5 py-3.5">
                      Date & Evaluation
                    </th>
                    <th scope="col" className="px-5 py-3.5">
                      Role & Exp
                    </th>
                    <th scope="col" className="px-5 py-3.5">
                      Location
                    </th>
                    <th scope="col" className="px-5 py-3.5">
                      Median Salary
                    </th>
                    <th scope="col" className="px-5 py-3.5">
                      P10–P90 Range
                    </th>
                    <th scope="col" className="px-5 py-3.5">
                      Confidence
                    </th>
                    <th scope="col" className="px-5 py-3.5 text-right">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 text-slate-700">
                  {historyData.results.map((item) => (
                    <tr
                      key={item.id}
                      className="hover:bg-slate-50/80 transition-colors"
                    >
                      {/* Date */}
                      <td className="px-5 py-4 whitespace-nowrap">
                        <div className="font-semibold text-slate-900">
                          {new Date(item.created_at).toLocaleDateString('en-IN', {
                            day: 'numeric',
                            month: 'short',
                            year: 'numeric',
                          })}
                        </div>
                        <div className="text-xs text-slate-400">
                          {new Date(item.created_at).toLocaleTimeString('en-IN', {
                            hour: '2-digit',
                            minute: '2-digit',
                          })}
                        </div>
                      </td>

                      {/* Role & Experience */}
                      <td className="px-5 py-4">
                        <div className="font-semibold text-slate-900">{item.job_role}</div>
                        <div className="text-xs text-slate-500 flex items-center gap-1 mt-0.5">
                          <Clock className="w-3 h-3 text-slate-400" />
                          {item.years_of_experience} yrs exp
                        </div>
                      </td>

                      {/* Location */}
                      <td className="px-5 py-4 whitespace-nowrap">
                        <div className="text-slate-800 flex items-center gap-1.5 text-xs font-medium">
                          <MapPin className="w-3.5 h-3.5 text-slate-400" />
                          {item.location}
                        </div>
                        <div className="text-[11px] text-slate-400 mt-0.5">
                          {item.education || "Bachelor's Degree"}
                        </div>
                      </td>

                      {/* Median Salary */}
                      <td className="px-5 py-4 whitespace-nowrap">
                        <div className="font-bold text-slate-900 text-base">
                          {item.predicted_salary_formatted}
                        </div>
                        <div className="text-xs font-semibold text-indigo-600">
                          {item.predicted_salary_lpa} LPA
                        </div>
                      </td>

                      {/* P10 - P90 Range */}
                      <td className="px-5 py-4 whitespace-nowrap">
                        <div className="text-xs text-slate-600 font-medium">
                          {item.salary_range?.p10_lpa}L – {item.salary_range?.p90_lpa}L
                        </div>
                        <div className="text-[10px] text-slate-400">
                          Conservative to Top Tier
                        </div>
                      </td>

                      {/* Confidence */}
                      <td className="px-5 py-4 whitespace-nowrap">
                        <Badge variant={getConfidenceBadgeColor(item.confidence_level)} size="xs" dot>
                          {item.confidence_level} ({item.confidence_score}%)
                        </Badge>
                      </td>

                      {/* Actions */}
                      <td className="px-5 py-4 whitespace-nowrap text-right">
                        <div className="flex items-center justify-end gap-1.5">
                          <Link
                            to={`/explanations/${item.id}`}
                            className="inline-flex items-center gap-1 px-2.5 py-1.5 rounded-lg text-xs font-medium text-indigo-700 bg-indigo-50 hover:bg-indigo-100 border border-indigo-200 transition-colors"
                            title="View SHAP Explainability"
                          >
                            <Sparkles className="w-3.5 h-3.5 text-indigo-600" />
                            SHAP
                          </Link>
                          <Button
                            variant="outline"
                            size="sm"
                            icon={Eye}
                            onClick={() => handleOpenDetail(item.id)}
                            className="text-xs"
                          >
                            Details
                          </Button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Pagination Toolbar */}
            <div className="px-5 py-3.5 border-t border-slate-200 bg-slate-50/50 flex items-center justify-between text-xs text-slate-600">
              <div>
                Showing{' '}
                <span className="font-semibold text-slate-800">
                  {(currentPage - 1) * 10 + 1}
                </span>{' '}
                to{' '}
                <span className="font-semibold text-slate-800">
                  {Math.min(currentPage * 10, historyData.count)}
                </span>{' '}
                of <span className="font-semibold text-slate-800">{historyData.count}</span> evaluations
              </div>

              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  icon={ChevronLeft}
                  onClick={() => fetchHistory(currentPage - 1)}
                  disabled={!historyData.previous || loading}
                  className="px-2 py-1"
                >
                  Prev
                </Button>
                <span className="px-2 text-xs font-medium text-slate-700">
                  Page {currentPage} of {totalPages}
                </span>
                <Button
                  variant="outline"
                  size="sm"
                  iconRight={ChevronRight}
                  onClick={() => fetchHistory(currentPage + 1)}
                  disabled={!historyData.next || loading}
                  className="px-2 py-1"
                >
                  Next
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Detail Modal */}
      {selectedReport && (
        <div className="fixed inset-0 z-50 overflow-y-auto bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
          <div className="relative bg-white rounded-2xl max-w-2xl w-full p-6 sm:p-8 shadow-xl border border-slate-200 animate-in fade-in zoom-in-95 duration-150">
            {/* Modal Header */}
            <div className="flex items-start justify-between pb-4 border-b border-slate-200">
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <h3 className="text-xl font-bold text-slate-900">
                    Evaluation Details #{selectedReport.id}
                  </h3>
                  <Badge variant={getConfidenceBadgeColor(selectedReport.confidence_level)} dot>
                    {selectedReport.confidence_level} Confidence
                  </Badge>
                </div>
                <p className="text-xs text-slate-500">
                  Recorded on{' '}
                  {new Date(selectedReport.created_at).toLocaleString('en-IN', {
                    dateStyle: 'medium',
                    timeStyle: 'short',
                  })}
                </p>
              </div>

              <button
                type="button"
                onClick={() => setSelectedReport(null)}
                className="p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Modal Body */}
            <div className="py-6 space-y-6">
              {/* Primary Output Display */}
              <div className="p-5 rounded-xl bg-gradient-to-r from-indigo-50 to-slate-50 border border-indigo-200 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div>
                  <span className="text-xs font-bold text-indigo-600 uppercase tracking-wider block">
                    Median Market Prediction (P50)
                  </span>
                  <div className="text-3xl font-extrabold text-slate-900 mt-1">
                    {selectedReport.predicted_salary_formatted}
                  </div>
                  <div className="text-sm font-semibold text-indigo-700 mt-0.5">
                    {selectedReport.predicted_salary_lpa} LPA
                  </div>
                </div>

                <div className="text-right sm:border-l sm:border-indigo-200 sm:pl-6">
                  <span className="text-xs text-slate-500 block">Monthly Equivalent</span>
                  <div className="text-lg font-bold text-slate-800 mt-1">
                    ₹{Math.round(selectedReport.predicted_salary_annual / 12).toLocaleString('en-IN')}{' '}
                    / mo
                  </div>
                  <span className="text-[11px] text-slate-400">Pre-tax gross estimate</span>
                </div>
              </div>

              {/* Quantile Breakdown */}
              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">
                  Quantile Spread (P10 - P50 - P90)
                </h4>
                <div className="grid grid-cols-3 gap-3">
                  <div className="p-3 rounded-lg bg-slate-50 border border-slate-200">
                    <span className="text-[11px] text-slate-400 block uppercase">10th Percentile</span>
                    <span className="text-sm font-bold text-slate-800 mt-0.5 block">
                      {selectedReport.salary_range?.p10_formatted}
                    </span>
                    <span className="text-xs text-slate-500 font-medium">
                      {selectedReport.salary_range?.p10_lpa} LPA
                    </span>
                  </div>

                  <div className="p-3 rounded-lg bg-indigo-50/50 border border-indigo-200">
                    <span className="text-[11px] text-indigo-500 block uppercase font-medium">Median Target</span>
                    <span className="text-sm font-bold text-indigo-900 mt-0.5 block">
                      {selectedReport.predicted_salary_formatted}
                    </span>
                    <span className="text-xs text-indigo-600 font-medium">
                      {selectedReport.predicted_salary_lpa} LPA
                    </span>
                  </div>

                  <div className="p-3 rounded-lg bg-emerald-50/50 border border-emerald-200">
                    <span className="text-[11px] text-emerald-600 block uppercase">90th Percentile</span>
                    <span className="text-sm font-bold text-emerald-950 mt-0.5 block">
                      {selectedReport.salary_range?.p90_formatted}
                    </span>
                    <span className="text-xs text-emerald-700 font-medium">
                      {selectedReport.salary_range?.p90_lpa} LPA
                    </span>
                  </div>
                </div>
              </div>

              {/* Profile Inputs Evaluated */}
              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">
                  Candidate Parameters Evaluated
                </h4>
                <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs">
                  <div className="p-3 rounded-lg bg-slate-50 border border-slate-200">
                    <span className="text-slate-400 block text-[11px]">Role</span>
                    <span className="font-semibold text-slate-900 mt-0.5 block">
                      {selectedReport.job_role}
                    </span>
                  </div>
                  <div className="p-3 rounded-lg bg-slate-50 border border-slate-200">
                    <span className="text-slate-400 block text-[11px]">Experience</span>
                    <span className="font-semibold text-slate-900 mt-0.5 block">
                      {selectedReport.years_of_experience} Years
                    </span>
                  </div>
                  <div className="p-3 rounded-lg bg-slate-50 border border-slate-200">
                    <span className="text-slate-400 block text-[11px]">Location</span>
                    <span className="font-semibold text-slate-900 mt-0.5 block">
                      {selectedReport.location}
                    </span>
                  </div>
                  <div className="p-3 rounded-lg bg-slate-50 border border-slate-200">
                    <span className="text-slate-400 block text-[11px]">Education</span>
                    <span className="font-semibold text-slate-900 mt-0.5 block">
                      {selectedReport.education || "Bachelor's Degree"}
                    </span>
                  </div>
                </div>
              </div>

              {/* Evaluated Skills */}
              <div>
                <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">
                  Technical Skills Evaluated ({selectedReport.skills?.length || 0})
                </h4>
                <div className="flex flex-wrap gap-1.5 p-3 rounded-lg bg-slate-50 border border-slate-200">
                  {selectedReport.skills && selectedReport.skills.length > 0 ? (
                    selectedReport.skills.map((skill) => (
                      <span
                        key={skill}
                        className="px-2.5 py-1 rounded-md text-xs font-medium bg-white text-slate-700 border border-slate-200 shadow-2xs"
                      >
                        {skill}
                      </span>
                    ))
                  ) : (
                    <span className="text-xs text-slate-400 italic">No specific skills listed.</span>
                  )}
                </div>
              </div>

              {/* Confidence Factors */}
              {selectedReport.confidence_factors && (
                <div>
                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-500 mb-2">
                    Confidence Factor Scores
                  </h4>
                  <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
                    {Object.entries(selectedReport.confidence_factors).map(([factor, score]) => (
                      <div key={factor} className="p-2.5 rounded bg-slate-50 border border-slate-200 text-center">
                        <span className="text-[10px] text-slate-400 uppercase block">
                          {factor.replace(/_/g, ' ')}
                        </span>
                        <span className="font-semibold text-slate-800 text-xs mt-0.5 block">
                          {String(score)}
                        </span>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>

            {/* Modal Footer */}
            <div className="pt-4 border-t border-slate-200 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
              <span className="text-[11px] text-slate-400">
                Model: {selectedReport.model_version || '2.0.0 (Random Forest)'}
              </span>
              <div className="flex items-center gap-2">
                <Link
                  to={`/explanations/${selectedReport.id}`}
                  className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium text-white bg-indigo-600 hover:bg-indigo-700 shadow-2xs transition-colors"
                >
                  <Sparkles className="w-3.5 h-3.5" />
                  View SHAP Explanation
                </Link>
                <Button variant="secondary" size="sm" onClick={() => setSelectedReport(null)}>
                  Close
                </Button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SavedReportsPage;
