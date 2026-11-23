import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  TrendingUp,
  ArrowLeft,
  Sparkles,
  HelpCircle,
  CheckCircle2,
  AlertTriangle,
  Info,
  Clock,
  MapPin,
  Briefcase,
  Layers,
  ArrowUpRight,
  ArrowDownRight,
  BarChart3,
  ShieldCheck,
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
import { intelligenceService } from '../services/intelligenceService';

export const PredictionExplanationPage = () => {
  const { predictionId } = useParams();
  const [explanation, setExplanation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchExplanation = async () => {
      setLoading(true);
      setError(null);
      try {
        const data = await intelligenceService.getPredictionExplanation(predictionId);
        setExplanation(data);
      } catch (err) {
        console.error('Failed to fetch prediction explanation:', err);
        setError(
          err.response?.data?.detail ||
          'Failed to load SHAP explainability analysis. Ensure this prediction exists and belongs to you.'
        );
      } finally {
        setLoading(false);
      }
    };

    if (predictionId) {
      fetchExplanation();
    }
  }, [predictionId]);

  if (loading) {
    return (
      <div className="max-w-5xl mx-auto space-y-6 py-8">
        <div className="h-8 bg-slate-200 rounded w-1/3 animate-pulse" />
        <div className="h-40 bg-slate-100 rounded-xl animate-pulse" />
        <div className="h-64 bg-slate-100 rounded-xl animate-pulse" />
      </div>
    );
  }

  if (error || !explanation) {
    return (
      <div className="max-w-4xl mx-auto py-12 text-center space-y-4">
        <div className="w-12 h-12 rounded-full bg-rose-100 text-rose-600 flex items-center justify-center mx-auto">
          <AlertTriangle className="w-6 h-6" />
        </div>
        <h2 className="text-xl font-bold text-slate-900">Explainability Unavailable</h2>
        <p className="text-sm text-slate-500 max-w-md mx-auto">{error}</p>
        <Link to="/saved-reports">
          <Button variant="outline" size="sm" icon={ArrowLeft}>
            Back to Saved Reports
          </Button>
        </Link>
      </div>
    );
  }

  // Prepare chart data for SHAP waterfall / bar view
  const chartData = (explanation.feature_attributions || []).slice(0, 10).map((attr) => ({
    name: attr.display_name || attr.clean_name,
    shap_value: attr.shap_value,
    inr_impact: Math.round(attr.inr_impact),
    direction: attr.direction,
    percentage: attr.percentage_impact,
    fill: attr.direction === 'positive' ? '#10b981' : '#f59e0b',
  })).reverse();

  const deltaSign = explanation.total_delta_inr >= 0 ? '+' : '';

  return (
    <div className="space-y-8 max-w-5xl mx-auto pb-12">
      {/* Navigation & Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 pb-2 border-b border-slate-200">
        <div>
          <Link
            to="/saved-reports"
            className="text-xs font-semibold text-indigo-600 hover:text-indigo-800 flex items-center gap-1 mb-2"
          >
            <ArrowLeft className="w-3.5 h-3.5" /> Back to History & Reports
          </Link>
          <h1 className="text-2xl sm:text-3xl font-bold text-slate-900 tracking-tight mb-1">
            SHAP Prediction Explainability
          </h1>
          <p className="text-sm text-slate-600">
            Mathematical feature attribution breaking down how each parameter shifted your compensation from baseline.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Link to="/salary-analysis">
            <Button variant="outline" size="sm" icon={TrendingUp} className="text-xs">
              New Prediction
            </Button>
          </Link>
        </div>
      </div>

      {/* Prediction Overview Card */}
      <Card className="p-6 bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 text-white border-slate-800">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 items-center">
          {/* Target Output */}
          <div className="space-y-1 md:border-r md:border-slate-800 md:pr-6">
            <span className="text-[11px] font-bold uppercase tracking-wider text-indigo-300">
              Evaluated Salary Outcome
            </span>
            <div className="text-3xl font-black text-white">
              ₹{Number(explanation.predicted_value_inr).toLocaleString('en-IN')}
            </div>
            <div className="text-xs text-slate-400">
              Annual Predicted Median (₹{(explanation.predicted_value_inr / 100000).toFixed(2)} LPA)
            </div>
          </div>

          {/* Baseline Comparison */}
          <div className="space-y-1 md:border-r md:border-slate-800 md:pr-6">
            <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
              Dataset Base Expectation E[y]
            </span>
            <div className="text-2xl font-bold text-slate-300">
              ₹{Number(explanation.base_value_inr).toLocaleString('en-IN')}
            </div>
            <div className="text-xs text-slate-400">
              Central tendency of reference market
            </div>
          </div>

          {/* Net Attribution Delta */}
          <div className="space-y-1">
            <span className="text-[11px] font-bold uppercase tracking-wider text-slate-400">
              Net Model Shift (Σ Φ)
            </span>
            <div className={`text-2xl font-bold flex items-center gap-1.5 ${explanation.total_delta_inr >= 0 ? 'text-emerald-400' : 'text-amber-400'}`}>
              {explanation.total_delta_inr >= 0 ? <ArrowUpRight className="w-5 h-5" /> : <ArrowDownRight className="w-5 h-5" />}
              {deltaSign}₹{Number(explanation.total_delta_inr).toLocaleString('en-IN')}
            </div>
            <div className="text-xs text-slate-400">
              Combined impact of candidate features
            </div>
          </div>
        </div>

        {/* Narrative Banner */}
        <div className="mt-5 pt-4 border-t border-slate-800 text-xs text-slate-300 flex items-start gap-2.5">
          <Sparkles className="w-4 h-4 text-indigo-400 shrink-0 mt-0.5" />
          <p className="leading-relaxed">{explanation.summary_narrative}</p>
        </div>
      </Card>

      {/* SHAP Feature Impact Waterfall / Bar Chart */}
      <Card className="p-6">
        <CardHeader
          title="SHAP Feature Contribution Spectrum"
          subtitle="Top 10 features shifting compensation above (green) or below (amber) the baseline in log-salary space."
          icon={BarChart3}
        />

        <div className="h-80 w-full pt-2">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart
              data={chartData}
              layout="vertical"
              margin={{ top: 10, right: 30, left: 60, bottom: 10 }}
            >
              <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#e2e8f0" />
              <XAxis
                type="number"
                stroke="#64748b"
                fontSize={12}
                tickFormatter={(val) => `${val >= 0 ? '+' : ''}${val}`}
              />
              <YAxis
                type="category"
                dataKey="name"
                stroke="#64748b"
                fontSize={12}
                width={130}
              />
              <Tooltip
                formatter={(val, name, item) => [
                  `SHAP: ${val >= 0 ? '+' : ''}${val} (${item.payload.percentage >= 0 ? '+' : ''}${item.payload.percentage}% effect, ${item.payload.inr_impact >= 0 ? '+' : ''}₹${Number(item.payload.inr_impact).toLocaleString('en-IN')})`,
                  'Attribution',
                ]}
                contentStyle={{
                  backgroundColor: '#1e293b',
                  borderRadius: '8px',
                  color: '#fff',
                  fontSize: '12px',
                }}
              />
              <ReferenceLine x={0} stroke="#94a3b8" strokeWidth={1.5} />
              <Bar dataKey="shap_value" radius={[0, 4, 4, 0]} barSize={20}>
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.fill} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
          <div className="flex items-center gap-4">
            <span className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-emerald-500" /> Positive Salary Contributor
            </span>
            <span className="flex items-center gap-1.5">
              <span className="w-2.5 h-2.5 rounded-full bg-amber-500" /> Limiting / Dragging Factor
            </span>
          </div>
          <span>Exact SHAP TreeExplainer additive values</span>
        </div>
      </Card>

      {/* Positive vs Limiting Drivers Triad */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Positive Drivers */}
        <Card className="p-6 border-emerald-100 bg-emerald-50/20">
          <div className="flex items-center gap-2 mb-4">
            <div className="p-2 rounded-lg bg-emerald-100 text-emerald-700">
              <CheckCircle2 className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-semibold text-slate-900 text-base">Key Positive Drivers</h3>
              <p className="text-xs text-slate-500">Factors boosting your compensation offer</p>
            </div>
          </div>

          <div className="space-y-3">
            {(explanation.positive_contributors || []).slice(0, 5).map((pos, idx) => (
              <div
                key={idx}
                className="p-3 rounded-xl bg-white border border-emerald-200/80 shadow-2xs flex items-center justify-between gap-3 text-xs"
              >
                <div>
                  <div className="font-semibold text-slate-900">{pos.clean_name}</div>
                  <div className="text-slate-500 text-[11px]">{pos.category}</div>
                </div>
                <div className="text-right">
                  <div className="font-bold text-emerald-600">
                    +{pos.percentage_impact}%
                  </div>
                  <div className="text-[11px] text-slate-400">
                    +₹{Math.round(pos.inr_impact).toLocaleString('en-IN')}
                  </div>
                </div>
              </div>
            ))}
          </div>
        </Card>

        {/* Limiting Factors */}
        <Card className="p-6 border-amber-100 bg-amber-50/20">
          <div className="flex items-center gap-2 mb-4">
            <div className="p-2 rounded-lg bg-amber-100 text-amber-700">
              <AlertTriangle className="w-5 h-5" />
            </div>
            <div>
              <h3 className="font-semibold text-slate-900 text-base">Primary Limiting Factors</h3>
              <p className="text-xs text-slate-500">Attributes dragging down salary potential</p>
            </div>
          </div>

          <div className="space-y-3">
            {(explanation.negative_contributors || []).length === 0 ? (
              <div className="p-4 rounded-xl bg-white border border-slate-200 text-xs text-slate-500 text-center">
                Zero negative factors detected. All profile parameters exceed market baseline expectations.
              </div>
            ) : (
              (explanation.negative_contributors || []).slice(0, 5).map((neg, idx) => (
                <div
                  key={idx}
                  className="p-3 rounded-xl bg-white border border-amber-200/80 shadow-2xs flex items-center justify-between gap-3 text-xs"
                >
                  <div>
                    <div className="font-semibold text-slate-900">{neg.clean_name}</div>
                    <div className="text-slate-500 text-[11px]">{neg.category}</div>
                  </div>
                  <div className="text-right">
                    <div className="font-bold text-amber-600">
                      {neg.percentage_impact}%
                    </div>
                    <div className="text-[11px] text-slate-400">
                      -₹{Math.abs(Math.round(neg.inr_impact)).toLocaleString('en-IN')}
                    </div>
                  </div>
                </div>
              ))
            )}
          </div>
        </Card>
      </div>

      {/* Technical Skills Specific SHAP Attribution */}
      <Card className="p-6">
        <CardHeader
          title="Technical Skills Value Attribution"
          subtitle="Specific SHAP contribution of technical skills present in your evaluated profile."
          icon={Sparkles}
        />

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3 pt-2">
          {(explanation.skills_impact || []).map((skillAttr, idx) => (
            <div
              key={idx}
              className="p-3.5 rounded-xl border border-slate-200 bg-slate-50/60 flex items-center justify-between gap-2 text-xs"
            >
              <div>
                <span className="font-semibold text-slate-900 block">{skillAttr.display_name}</span>
                <span className="text-[11px] text-slate-500">SHAP: {skillAttr.shap_value}</span>
              </div>
              <div className="text-right">
                <span
                  className={`font-bold block ${
                    skillAttr.direction === 'positive' ? 'text-emerald-600' : 'text-amber-600'
                  }`}
                >
                  {skillAttr.direction === 'positive' ? '+' : ''}
                  {skillAttr.percentage_impact}%
                </span>
                <span className="text-[10px] text-slate-400">
                  {skillAttr.inr_impact >= 0 ? '+' : ''}₹{Math.round(skillAttr.inr_impact).toLocaleString('en-IN')}
                </span>
              </div>
            </div>
          ))}
        </div>
      </Card>

      {/* Explainability Methodology Disclaimer */}
      <div className="p-5 rounded-xl bg-slate-50 border border-slate-200 text-xs text-slate-600 space-y-2">
        <div className="flex items-center gap-2 font-semibold text-slate-800">
          <ShieldCheck className="w-4 h-4 text-indigo-600" />
          Mathematical Explainability Methodology (SHAP TreeExplainer)
        </div>
        <p className="text-[11px] leading-relaxed text-slate-500">
          WorthIQ utilizes exact tree-traversal algorithms via Lundberg et al.'s TreeSHAP algorithm to compute local
          feature attributions ($\phi_i$) satisfy efficiency, symmetry, and additivity:
          $\ln(1 + \hat{y}) = E[\ln(1 + y)] + \sum \phi_i$.
          The estimated rupee (₹) contributions represent proportional redistributions of the total salary variance
          and reflect statistical associations from the training dataset.
        </p>
      </div>
    </div>
  );
};

export default PredictionExplanationPage;
