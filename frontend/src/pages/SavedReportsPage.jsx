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
  Download,
  Trash2,
  Filter,
  FileText,
  Clock,
  Sparkles,
  ArrowRight,
  Layers,
  Award,
  RefreshCw,
  FileSpreadsheet,
  AlertCircle,
  ShieldCheck,
} from 'lucide-react';
import { Card, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { reportService } from '../services/reportService';
import { predictionService } from '../services/predictionService';
import { useToast } from '../context/ToastContext';

const REPORT_TABS = [
  { id: 'all', label: 'All Reports' },
  { id: 'salary_prediction', label: 'Salary Predictions' },
  { id: 'scenario_comparison', label: 'Scenario Comparisons' },
  { id: 'resume_analysis', label: 'Resume Intelligence' },
  { id: 'job_role_matching', label: 'Role Matches' },
  { id: 'career_roadmap', label: 'Career Roadmaps' },
];

export const SavedReportsPage = () => {
  const toast = useToast();
  const [activeTab, setActiveTab] = useState('all');
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedReport, setSelectedReport] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);
  const [downloadingId, setDownloadingId] = useState(null);
  const [exportingCsv, setExportingCsv] = useState(false);
  const [searchTerm, setSearchTerm] = useState('');

  // Fetch reports from backend
  const fetchReports = async (type = null) => {
    setLoading(true);
    setError(null);
    try {
      const filterType = type && type !== 'all' ? type : null;
      const data = await reportService.getReports(filterType);
      setReports(data || []);
    } catch (err) {
      console.error('Failed to fetch reports:', err);
      setError('Unable to load saved reports. Please verify your connection.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports(activeTab);
  }, [activeTab]);

  // Download PDF
  const handleDownloadPdf = async (report) => {
    setDownloadingId(report.id);
    try {
      await reportService.downloadReportPdf(report.id, report.title);
      toast.success(`Downloaded "${report.title}.pdf"`);
    } catch (err) {
      console.error('Download error:', err);
      toast.error('Failed to download PDF report.');
    } finally {
      setDownloadingId(null);
    }
  };

  // Export CSV
  const handleExportCsv = async (type) => {
    setExportingCsv(true);
    try {
      await reportService.exportCsv(type);
      toast.success(`Exported ${type} to CSV successfully.`);
    } catch (err) {
      console.error('Export CSV error:', err);
      toast.error(`Failed to export ${type} to CSV.`);
    } finally {
      setExportingCsv(false);
    }
  };

  // Delete Report
  const handleDeleteReport = async (id, title) => {
    if (!window.confirm(`Delete report "${title}"?`)) return;
    try {
      await reportService.deleteReport(id);
      toast.success('Report deleted.');
      setReports((prev) => prev.filter((r) => r.id !== id));
      if (selectedReport?.id === id) setModalOpen(false);
    } catch (err) {
      toast.error('Failed to delete report.');
    }
  };

  // Open inspection modal
  const handleViewReport = (report) => {
    setSelectedReport(report);
    setModalOpen(true);
  };

  // Filtered reports
  const filteredReports = reports.filter((r) => {
    const term = searchTerm.toLowerCase();
    const titleMatch = (r.title || '').toLowerCase().includes(term);
    const summaryMatch = (r.summary || '').toLowerCase().includes(term);
    return titleMatch || summaryMatch;
  });

  const getReportTypeBadge = (type) => {
    switch (type) {
      case 'salary_prediction':
        return <Badge variant="primary" size="sm">Salary Prediction</Badge>;
      case 'scenario_comparison':
        return <Badge variant="indigo" size="sm">What-If Comparison</Badge>;
      case 'resume_analysis':
        return <Badge variant="emerald" size="sm">Resume Intelligence</Badge>;
      case 'job_role_matching':
        return <Badge variant="violet" size="sm">Role Match</Badge>;
      case 'career_roadmap':
        return <Badge variant="amber" size="sm">Roadmap</Badge>;
      default:
        return <Badge variant="neutral" size="sm">{type}</Badge>;
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-16">
      {/* Page Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-4 border-b border-slate-200">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <h1 className="text-2xl sm:text-3xl font-extrabold tracking-tight text-slate-900">
              Advanced Career Reports & Archive
            </h1>
            <Badge variant="primary" size="sm">PDF & CSV</Badge>
          </div>
          <p className="text-xs sm:text-sm text-slate-600">
            Access, inspect, and export your formal salary assessments, scenario models, resume extractions, and career roadmaps.
          </p>
        </div>

        {/* CSV Export Quick Actions */}
        <div className="flex flex-wrap items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            icon={FileSpreadsheet}
            onClick={() => handleExportCsv('predictions')}
            disabled={exportingCsv}
          >
            Export Predictions (CSV)
          </Button>
          <Button
            variant="outline"
            size="sm"
            icon={FileSpreadsheet}
            onClick={() => handleExportCsv('scenarios')}
            disabled={exportingCsv}
          >
            Export Scenarios (CSV)
          </Button>
          <Button
            variant="primary"
            size="sm"
            icon={RefreshCw}
            onClick={() => fetchReports(activeTab)}
          >
            Refresh
          </Button>
        </div>
      </div>

      {/* Tabs & Search Filter Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        {/* Filter Tabs */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0 scrollbar-none">
          {REPORT_TABS.map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id)}
              className={`text-xs px-3 py-1.5 rounded-lg font-medium whitespace-nowrap transition-all ${
                activeTab === tab.id
                  ? 'bg-indigo-600 text-white shadow-sm'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Search Bar */}
        <div className="w-full sm:w-64">
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search reports..."
            className="w-full text-xs px-3 py-1.5 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>
      </div>

      {/* Reports Grid */}
      {loading ? (
        <Card className="p-12 text-center text-slate-500 text-xs">
          <RefreshCw className="w-6 h-6 animate-spin mx-auto mb-2 text-indigo-600" />
          Loading reports archive...
        </Card>
      ) : error ? (
        <Card className="p-8 text-center text-rose-600 text-xs">
          <AlertCircle className="w-6 h-6 mx-auto mb-2" />
          {error}
        </Card>
      ) : filteredReports.length === 0 ? (
        <Card className="p-12 text-center text-slate-400 space-y-3">
          <FileText className="w-12 h-12 mx-auto text-slate-300" />
          <div className="space-y-1">
            <h3 className="text-sm font-bold text-slate-700">No reports found</h3>
            <p className="text-xs text-slate-500 max-w-sm mx-auto">
              Run a salary analysis, create a What-If scenario, or upload your resume to generate archived reports.
            </p>
          </div>
          <div className="pt-2 flex justify-center gap-3">
            <Link to="/salary-analysis">
              <Button variant="primary" size="sm">
                Run Salary Analysis
              </Button>
            </Link>
            <Link to="/what-if-simulator">
              <Button variant="outline" size="sm">
                Open Simulator
              </Button>
            </Link>
          </div>
        </Card>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filteredReports.map((report) => (
            <Card
              key={report.id}
              className="hover:shadow-md transition-all border-slate-200 flex flex-col justify-between"
            >
              <div className="space-y-3">
                <div className="flex items-start justify-between gap-2">
                  <div className="space-y-1">
                    {getReportTypeBadge(report.report_type)}
                    <h3 className="text-sm font-bold text-slate-900 line-clamp-1 mt-1">
                      {report.title}
                    </h3>
                  </div>
                  <span className="text-[10px] text-slate-400 font-mono whitespace-nowrap">
                    #{report.id}
                  </span>
                </div>

                <p className="text-xs text-slate-600 line-clamp-2">
                  {report.summary || 'Comprehensive evaluation snapshot archived.'}
                </p>

                <div className="flex items-center gap-1.5 text-[11px] text-slate-400 pt-1 border-t border-slate-100">
                  <Clock className="w-3.5 h-3.5" />
                  <span>{new Date(report.created_at).toLocaleString()}</span>
                </div>
              </div>

              {/* Action Buttons */}
              <div className="pt-4 mt-3 border-t border-slate-100 flex items-center justify-between gap-2">
                <button
                  type="button"
                  onClick={() => handleViewReport(report)}
                  className="inline-flex items-center gap-1 text-xs text-indigo-600 hover:text-indigo-800 font-medium"
                >
                  <Eye className="w-3.5 h-3.5" />
                  Inspect Snapshot
                </button>

                <div className="flex items-center gap-1">
                  <Button
                    variant="outline"
                    size="xs"
                    icon={Download}
                    isLoading={downloadingId === report.id}
                    onClick={() => handleDownloadPdf(report)}
                    title="Download Official PDF Report"
                  >
                    PDF
                  </Button>
                  <button
                    type="button"
                    onClick={() => handleDeleteReport(report.id, report.title)}
                    className="p-1.5 text-slate-400 hover:text-rose-600 rounded"
                    title="Delete report"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      )}

      {/* Snapshot Inspection Modal */}
      {modalOpen && selectedReport && (
        <div className="fixed inset-0 z-50 bg-slate-900/50 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="bg-white rounded-2xl max-w-2xl w-full max-h-[85vh] flex flex-col shadow-2xl overflow-hidden">
            {/* Modal Header */}
            <div className="p-4 border-b border-slate-100 flex items-center justify-between">
              <div>
                <div className="flex items-center gap-2">
                  {getReportTypeBadge(selectedReport.report_type)}
                  <h3 className="text-base font-bold text-slate-900">
                    {selectedReport.title}
                  </h3>
                </div>
                <p className="text-xs text-slate-500 mt-0.5">
                  Archived on {new Date(selectedReport.created_at).toLocaleString()}
                </p>
              </div>
              <button
                type="button"
                onClick={() => setModalOpen(false)}
                className="p-1 text-slate-400 hover:text-slate-600 rounded-lg"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {/* Modal Content */}
            <div className="p-5 overflow-y-auto space-y-4 text-xs">
              <div className="p-3 bg-slate-50 rounded-lg border border-slate-200">
                <span className="font-bold text-slate-700 block mb-1">Executive Summary</span>
                <p className="text-slate-600 leading-relaxed">{selectedReport.summary}</p>
              </div>

              <div>
                <span className="font-bold text-slate-800 block mb-2">Evaluated Data Snapshot</span>
                <div className="p-3 bg-slate-900 text-slate-200 rounded-lg font-mono text-[11px] overflow-x-auto max-h-60">
                  <pre>{JSON.stringify(selectedReport.data_snapshot, null, 2)}</pre>
                </div>
              </div>

              <div className="p-3 bg-amber-50/70 border border-amber-200 rounded-lg flex items-start gap-2 text-amber-800 text-[11px]">
                <ShieldCheck className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                <p>
                  Official reports generated by WorthIQ are computed using Random Forest ML 2.0 based on market correlation benchmarks. Download the official PDF document for a formatted presentation.
                </p>
              </div>
            </div>

            {/* Modal Footer */}
            <div className="p-4 border-t border-slate-100 flex items-center justify-between">
              <button
                type="button"
                onClick={() => handleDeleteReport(selectedReport.id, selectedReport.title)}
                className="text-xs text-rose-600 hover:text-rose-800 font-medium inline-flex items-center gap-1"
              >
                <Trash2 className="w-3.5 h-3.5" /> Delete Report
              </button>

              <div className="flex items-center gap-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setModalOpen(false)}
                >
                  Close
                </Button>
                <Button
                  variant="primary"
                  size="sm"
                  icon={Download}
                  isLoading={downloadingId === selectedReport.id}
                  onClick={() => handleDownloadPdf(selectedReport)}
                >
                  Download PDF Report
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
