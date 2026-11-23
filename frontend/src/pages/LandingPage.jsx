import React from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../components/layout/Navbar';
import Button from '../components/ui/Button';
import Card from '../components/ui/Card';
import Badge from '../components/ui/Badge';
import {
  TrendingUp,
  Sparkles,
  Briefcase,
  Sliders,
  Compass,
  LineChart,
  ShieldCheck,
  CheckCircle2,
  ArrowRight,
  Database,
  Layers,
  Code2,
  Lock,
  Cpu,
  BarChart3,
  HelpCircle,
  Award,
} from 'lucide-react';

export const LandingPage = () => {
  return (
    <div className="min-h-screen bg-[#F7F8FC] flex flex-col antialiased text-[#172033]">
      <Navbar />

      {/* 1. Hero Section */}
      <section className="relative overflow-hidden pt-12 pb-20 md:pt-20 md:pb-28">
        {/* Subtle background glow */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-indigo-500/10 blur-[130px] rounded-full pointer-events-none" />

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
          <div className="inline-flex items-center gap-2 px-3.5 py-1.5 rounded-full bg-indigo-50 border border-indigo-200/90 text-indigo-700 text-xs font-semibold mb-6 shadow-2xs">
            <Sparkles className="w-3.5 h-3.5 text-indigo-600" />
            <span>AI-Powered Career &amp; Compensation Intelligence</span>
          </div>

          <h1 className="text-4xl sm:text-5xl md:text-6xl font-black text-slate-900 tracking-tight leading-[1.12] max-w-4xl mx-auto">
            Know Your Worth.{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 via-violet-600 to-indigo-700">
              Build Your Future.
            </span>
          </h1>

          <p className="mt-6 text-base sm:text-lg md:text-xl text-slate-600 max-w-2xl mx-auto leading-relaxed">
            Discover your estimated market salary potential, analyze the exact Rupee contribution of your technical skills with SHAP explainability, and follow structured career roadmaps.
          </p>

          <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3 sm:gap-4">
            <Link to="/register" className="w-full sm:w-auto">
              <Button size="lg" variant="primary" iconRight={ArrowRight} className="w-full sm:w-auto shadow-md">
                Get Started Free
              </Button>
            </Link>
            <a href="#features" className="w-full sm:w-auto">
              <Button size="lg" variant="outline" className="w-full sm:w-auto">
                Explore Features
              </Button>
            </a>
          </div>

          {/* Interactive Live Preview Teaser Card */}
          <div className="mt-14 max-w-4xl mx-auto">
            <div className="rounded-2xl border border-slate-200/90 bg-white p-6 sm:p-8 shadow-xl shadow-slate-200/40 text-left">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-6 border-b border-slate-100 gap-4">
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="text-lg font-bold text-slate-900">Career Market Benchmark Preview</h3>
                    <Badge variant="emerald" dot={true}>
                      Machine Learning 2.0
                    </Badge>
                  </div>
                  <p className="text-xs text-slate-500 mt-1">
                    Multi-quantile bounds calculated using Random Forest trained on 25,332 tech records
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs text-slate-400">Sample Track:</span>
                  <span className="text-xs font-bold px-2.5 py-1 bg-indigo-50 text-indigo-700 rounded-md border border-indigo-200">
                    Full Stack Developer
                  </span>
                </div>
              </div>

              {/* Sample Analytics Grid */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-6">
                <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
                  <p className="text-xs font-semibold text-slate-500">Benchmark Median Salary</p>
                  <p className="text-2xl font-black text-slate-900 mt-1.5">
                    ₹12.4 LPA <span className="text-xs text-slate-400 font-normal">P50</span>
                  </p>
                  <p className="text-[11px] text-emerald-600 font-semibold mt-1 flex items-center gap-1">
                    <TrendingUp className="w-3.5 h-3.5" /> High Demand Tier
                  </p>
                </div>

                <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
                  <p className="text-xs font-semibold text-slate-500">Top High-Leverage Skills</p>
                  <div className="flex flex-wrap gap-1.5 mt-2">
                    {['React.js', 'Docker', 'PostgreSQL', 'AWS'].map((s) => (
                      <span
                        key={s}
                        className="px-2 py-0.5 text-[11px] font-semibold bg-white border border-slate-200 rounded text-slate-700 shadow-2xs"
                      >
                        {s}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
                  <p className="text-xs font-semibold text-slate-500">SHAP Explainability</p>
                  <p className="text-xs text-indigo-600 font-bold mt-1.5 flex items-center gap-1">
                    <Sparkles className="w-3.5 h-3.5" /> TreeSHAP Attribution
                  </p>
                  <p className="text-[11px] text-slate-500 mt-1">
                    Decomposes salary into positive and limiting factors in ₹ INR.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* 2. Features Grid Section */}
      <section id="features" className="py-20 bg-white border-y border-slate-200/90">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-xs font-bold text-indigo-600 uppercase tracking-widest">
              Core Intelligence Capabilities
            </h2>
            <p className="text-3xl font-extrabold text-slate-900 tracking-tight mt-2">
              Everything You Need to Navigate Your Tech Career
            </p>
            <p className="text-sm text-slate-600 mt-3">
              WorthIQ replaces guesswork with calibrated empirical data, game-theoretic explainability, and actionable roadmaps.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {/* Feature 1 */}
            <Card padding="p-6" className="space-y-3">
              <div className="w-10 h-10 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center font-bold">
                <TrendingUp className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-slate-900">Quantile Salary Prediction</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Supervised Random Forest regressor outputting Conservative (P10), Median (P50), and Top-Tier (P90) salary ranges tailored to your tech stack and experience.
              </p>
            </Card>

            {/* Feature 2 */}
            <Card padding="p-6" className="space-y-3">
              <div className="w-10 h-10 rounded-xl bg-violet-50 text-violet-600 flex items-center justify-center font-bold">
                <Sparkles className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-slate-900">Explainable AI (TreeSHAP)</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Understand the "why" behind your prediction. TreeSHAP additive feature attributions reveal exactly how much each skill and location raises or lowers your compensation in ₹ INR.
              </p>
            </Card>

            {/* Feature 3 */}
            <Card padding="p-6" className="space-y-3">
              <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center font-bold">
                <Layers className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-slate-900">Skill Intelligence &amp; Co-Occurrence</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Mined across 25,332 records to discover high-synergy technology pairings (e.g., Docker + Kubernetes) and calculate single-skill marginal compensation ROI.
              </p>
            </Card>

            {/* Feature 4 */}
            <Card padding="p-6" className="space-y-3">
              <div className="w-10 h-10 rounded-xl bg-sky-50 text-sky-600 flex items-center justify-center font-bold">
                <Briefcase className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-slate-900">AI Job Role Matching</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Multi-dimensional composite scoring evaluating 40% mandatory skill overlap, 15% preferred coverage, 25% TF-IDF cosine semantic similarity, and 20% experience fit across 9 roles.
              </p>
            </Card>

            {/* Feature 5 */}
            <Card padding="p-6" className="space-y-3">
              <div className="w-10 h-10 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center font-bold">
                <Compass className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-slate-900">Directed Career Roadmaps</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Non-circular Directed Acyclic Graph (DAG) learning stages that sequence your missing skills with real-world capstone software engineering project briefs.
              </p>
            </Card>

            {/* Feature 6 */}
            <Card padding="p-6" className="space-y-3">
              <div className="w-10 h-10 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center font-bold">
                <Sliders className="w-5 h-5" />
              </div>
              <h3 className="text-base font-bold text-slate-900">What-If Simulation Sandbox</h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                Interactive counterfactual laboratory allowing you to simulate acquiring new skills, adding years of experience, or relocating before making real-world career investments.
              </p>
            </Card>
          </div>
        </div>
      </section>

      {/* 3. How It Works Section */}
      <section className="py-20 bg-[#F7F8FC]">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-xs font-bold text-indigo-600 uppercase tracking-widest">
              Simple 5-Step Process
            </h2>
            <p className="text-3xl font-extrabold text-slate-900 tracking-tight mt-2">
              How WorthIQ Works
            </p>
            <p className="text-sm text-slate-600 mt-3">
              From profile setup to actionable career execution in minutes.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-5 gap-4 relative">
            {[
              {
                step: '01',
                title: 'Build Profile',
                desc: 'Add your job track, verified skills, experience, and location.',
              },
              {
                step: '02',
                title: 'Analyze Salary',
                desc: 'Run Random Forest ML inference to obtain P10–P90 estimates.',
              },
              {
                step: '03',
                title: 'Inspect SHAP',
                desc: 'See exact Rupee contributions from each skill and factor.',
              },
              {
                step: '04',
                title: 'Match Roles',
                desc: 'Discover roles aligned with your capabilities and identify skill gaps.',
              },
              {
                step: '05',
                title: 'Execute Roadmap',
                desc: 'Follow DAG prerequisite stages and build recommended capstones.',
              },
            ].map((st) => (
              <div
                key={st.step}
                className="bg-white p-5 rounded-2xl border border-slate-200/80 shadow-xs relative flex flex-col justify-between"
              >
                <div>
                  <span className="text-2xl font-black text-indigo-600 block mb-2">{st.step}</span>
                  <h4 className="text-sm font-bold text-slate-900">{st.title}</h4>
                  <p className="text-xs text-slate-500 mt-1 leading-relaxed">{st.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* 4. Trust & Methodology Section */}
      <section className="py-16 bg-white border-t border-slate-200/90">
        <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <div className="p-8 rounded-3xl bg-slate-50 border border-slate-200 space-y-4">
            <div className="w-12 h-12 rounded-2xl bg-indigo-100 text-indigo-700 flex items-center justify-center mx-auto">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-slate-900 tracking-tight">
              Rigorous Data Science &amp; Statistical Governance
            </h3>
            <p className="text-xs sm:text-sm text-slate-600 leading-relaxed max-w-3xl mx-auto">
              WorthIQ models are trained exclusively on authentic, cleaned tech compensation datasets spanning 25,332 records across major Indian technology hubs. Model predictions represent statistical conditional medians and quantile bounds calibrated to historical hiring trends. They reflect market valuation benchmarks rather than binding or guaranteed employment offers.
            </p>
            <div className="pt-2 flex flex-wrap items-center justify-center gap-6 text-xs font-semibold text-slate-600">
              <span className="flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" /> 25,332 Real Records
              </span>
              <span className="flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" /> Random Forest Regressor
              </span>
              <span className="flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" /> TreeSHAP Additive Math
              </span>
              <span className="flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" /> PostgreSQL Persistence
              </span>
            </div>
          </div>
        </div>
      </section>

      {/* 5. Footer */}
      <footer className="bg-slate-900 text-white py-12 border-t border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row sm:items-center justify-between gap-6">
          <div>
            <span className="text-lg font-black tracking-tight text-white">WorthIQ</span>
            <p className="text-xs text-slate-400 mt-1">
              Skill-Based Salary Potential &amp; Career Growth Analyzer &middot; Final-Year B.Tech Project
            </p>
          </div>
          <div className="flex flex-wrap items-center gap-6 text-xs text-slate-400">
            <Link to="/login" className="hover:text-white transition-colors">
              Sign In
            </Link>
            <Link to="/register" className="hover:text-white transition-colors">
              Register Free
            </Link>
            <a href="#features" className="hover:text-white transition-colors">
              Features
            </a>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
