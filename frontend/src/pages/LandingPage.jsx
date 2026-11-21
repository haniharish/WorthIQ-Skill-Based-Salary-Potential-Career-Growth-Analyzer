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
} from 'lucide-react';

export const LandingPage = () => {
  return (
    <div className="min-h-screen bg-slate-50 flex flex-col">
      <Navbar />

      {/* Hero Section */}
      <section className="relative overflow-hidden pt-12 pb-20 md:pt-20 md:pb-28">
        {/* Subtle background glow */}
        <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[350px] bg-indigo-500/10 blur-[120px] rounded-full pointer-events-none" />

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10 text-center">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-indigo-50 border border-indigo-200/80 text-indigo-700 text-xs font-semibold mb-6">
            <Sparkles className="w-3.5 h-3.5 text-indigo-600" />
            <span>WorthIQ &middot; Phase 1 Foundation Live</span>
          </div>

          <h1 className="text-4xl sm:text-5xl md:text-6xl font-extrabold text-slate-900 tracking-tight leading-[1.15] max-w-4xl mx-auto">
            Know Your Worth.{' '}
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-indigo-600 to-violet-600">
              Build Your Future.
            </span>
          </h1>

          <p className="mt-6 text-lg sm:text-xl text-slate-600 max-w-2xl mx-auto leading-relaxed">
            Discover your salary potential, identify valuable skills and make smarter career decisions with data-driven insights.
          </p>

          <div className="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3 sm:gap-4">
            <Link to="/register" className="w-full sm:w-auto">
              <Button size="lg" variant="primary" iconRight={ArrowRight} className="w-full sm:w-auto shadow-md">
                Get Started Free
              </Button>
            </Link>
            <Link to="/login" className="w-full sm:w-auto">
              <Button size="lg" variant="outline" className="w-full sm:w-auto">
                Sign In to Account
              </Button>
            </Link>
          </div>

          {/* Live Teaser Card */}
          <div className="mt-14 max-w-4xl mx-auto">
            <div className="rounded-2xl border border-slate-200/90 bg-white p-6 sm:p-8 shadow-xl shadow-slate-200/50 text-left">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between pb-6 border-b border-slate-100 gap-4">
                <div>
                  <div className="flex items-center gap-2">
                    <h3 className="text-lg font-bold text-slate-900">Career Market Benchmark Preview</h3>
                    <Badge variant="emerald" dot={true}>Live Analyzer</Badge>
                  </div>
                  <p className="text-xs text-slate-500 mt-1">
                    Multi-factor benchmark combining technical skills, experience and market demand
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs text-slate-400">Target Role:</span>
                  <span className="text-xs font-semibold px-2.5 py-1 bg-slate-100 rounded-md text-slate-700">
                    Full Stack Developer
                  </span>
                </div>
              </div>

              {/* Sample Analytics Grid */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-6">
                <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
                  <p className="text-xs font-medium text-slate-500">Benchmark Salary Potential</p>
                  <p className="text-2xl font-extrabold text-slate-900 mt-1.5">₹12.4 LPA <span className="text-xs text-slate-400 font-normal">avg</span></p>
                  <p className="text-[11px] text-emerald-600 font-medium mt-1 flex items-center gap-1">
                    <TrendingUp className="w-3.5 h-3.5" /> +28% vs general market
                  </p>
                </div>

                <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
                  <p className="text-xs font-medium text-slate-500">Highest-Value Skill Stack</p>
                  <div className="flex flex-wrap gap-1.5 mt-2">
                    {['React.js', 'Django', 'PostgreSQL', 'Docker'].map((s) => (
                      <span key={s} className="px-2 py-0.5 text-[11px] font-semibold bg-white border border-slate-200 rounded text-slate-700">
                        {s}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="p-4 rounded-xl bg-slate-50 border border-slate-100">
                  <p className="text-xs font-medium text-slate-500">Profile Optimization Score</p>
                  <div className="flex items-end gap-2 mt-1.5">
                    <span className="text-2xl font-extrabold text-indigo-600">92/100</span>
                    <span className="text-xs text-slate-400 pb-0.5">Top 8% candidate</span>
                  </div>
                  <div className="w-full bg-slate-200 rounded-full h-1.5 mt-2">
                    <div className="bg-indigo-600 h-1.5 rounded-full w-[92%]"></div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section id="features" className="py-20 bg-white border-y border-slate-200/80">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-xs font-bold uppercase tracking-wider text-indigo-600">Core Capabilities</h2>
            <p className="mt-2 text-3xl font-extrabold text-slate-900 tracking-tight sm:text-4xl">
              Engineered for Transparent Career Intelligence
            </p>
            <p className="mt-4 text-base text-slate-600">
              WorthIQ replaces guesswork with concrete algorithmic salary modeling, gap analysis and growth roadmaps.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            <Card hover={true}>
              <div className="w-10 h-10 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center mb-4">
                <TrendingUp className="w-5 h-5" />
              </div>
              <h3 className="text-lg font-bold text-slate-900 mb-2">1. Salary Prediction</h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                Estimate market compensation ranges customized to your exact combination of skills, years of experience and target job role.
              </p>
            </Card>

            <Card hover={true}>
              <div className="w-10 h-10 rounded-xl bg-violet-50 text-violet-600 flex items-center justify-center mb-4">
                <Sparkles className="w-5 h-5" />
              </div>
              <h3 className="text-lg font-bold text-slate-900 mb-2">2. Skill Impact Analysis</h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                Determine the exact monetary contribution of each individual skill in your portfolio and identify high-ROI skills to learn next.
              </p>
            </Card>

            <Card hover={true}>
              <div className="w-10 h-10 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center mb-4">
                <Briefcase className="w-5 h-5" />
              </div>
              <h3 className="text-lg font-bold text-slate-900 mb-2">3. Job Role Matching</h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                Calculate similarity scores between your skill repertoire and trending industry roles, with precise gap identification.
              </p>
            </Card>

            <Card hover={true}>
              <div className="w-10 h-10 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center mb-4">
                <Sliders className="w-5 h-5" />
              </div>
              <h3 className="text-lg font-bold text-slate-900 mb-2">4. What-If Simulation</h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                Simulate potential compensation shifts before investing months learning new technologies or transitioning roles.
              </p>
            </Card>

            <Card hover={true}>
              <div className="w-10 h-10 rounded-xl bg-sky-50 text-sky-600 flex items-center justify-center mb-4">
                <Compass className="w-5 h-5" />
              </div>
              <h3 className="text-lg font-bold text-slate-900 mb-2">5. Career Growth Roadmap</h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                Step-by-step sequential learning recommendations tailored to elevate you from your current level to target salary bands.
              </p>
            </Card>

            <Card hover={true}>
              <div className="w-10 h-10 rounded-xl bg-rose-50 text-rose-600 flex items-center justify-center mb-4">
                <LineChart className="w-5 h-5" />
              </div>
              <h3 className="text-lg font-bold text-slate-900 mb-2">6. Explainable Insights</h3>
              <p className="text-sm text-slate-600 leading-relaxed">
                No black boxes. Understand precisely why predictions were made, powered by transparent feature importance metrics.
              </p>
            </Card>
          </div>
        </div>
      </section>

      {/* How It Works */}
      <section id="how-it-works" className="py-20 bg-slate-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center max-w-3xl mx-auto mb-16">
            <h2 className="text-xs font-bold uppercase tracking-wider text-indigo-600">Three Simple Steps</h2>
            <p className="mt-2 text-3xl font-extrabold text-slate-900 tracking-tight sm:text-4xl">
              How WorthIQ Works
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="bg-white p-6 rounded-xl border border-slate-200/90 relative">
              <div className="w-8 h-8 rounded-lg bg-indigo-600 text-white font-bold text-sm flex items-center justify-center mb-4">
                1
              </div>
              <h4 className="text-base font-bold text-slate-900 mb-2">Build Your Skill Profile</h4>
              <p className="text-xs text-slate-600 leading-relaxed">
                Input your technical competencies, current role, years of experience and educational background into your private profile.
              </p>
            </div>

            <div className="bg-white p-6 rounded-xl border border-slate-200/90 relative">
              <div className="w-8 h-8 rounded-lg bg-indigo-600 text-white font-bold text-sm flex items-center justify-center mb-4">
                2
              </div>
              <h4 className="text-base font-bold text-slate-900 mb-2">Algorithmic Benchmarking</h4>
              <p className="text-xs text-slate-600 leading-relaxed">
                Our models analyze market trends, skill distributions and compensation percentiles to establish your accurate valuation.
              </p>
            </div>

            <div className="bg-white p-6 rounded-xl border border-slate-200/90 relative">
              <div className="w-8 h-8 rounded-lg bg-indigo-600 text-white font-bold text-sm flex items-center justify-center mb-4">
                3
              </div>
              <h4 className="text-base font-bold text-slate-900 mb-2">Targeted Career Progression</h4>
              <p className="text-xs text-slate-600 leading-relaxed">
                Review ROI recommendations, unlock higher salary brackets and pursue the exact skills that maximize your growth.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Tech Stack Banner */}
      <section id="tech-stack" className="py-16 bg-white border-t border-slate-200/80">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-xs font-semibold uppercase tracking-wider text-slate-400 mb-8">
            Robust Architecture &middot; Enterprise Grade Stack
          </p>
          <div className="flex flex-wrap items-center justify-center gap-8 sm:gap-12 text-slate-700 font-semibold text-sm">
            <div className="flex items-center gap-2"><Code2 className="w-5 h-5 text-indigo-600" /> React 18 & Vite</div>
            <div className="flex items-center gap-2"><Layers className="w-5 h-5 text-indigo-600" /> Django & DRF</div>
            <div className="flex items-center gap-2"><Database className="w-5 h-5 text-indigo-600" /> PostgreSQL 16</div>
            <div className="flex items-center gap-2"><Lock className="w-5 h-5 text-indigo-600" /> JWT Authentication</div>
            <div className="flex items-center gap-2"><ShieldCheck className="w-5 h-5 text-indigo-600" /> Docker Containers</div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="mt-auto bg-slate-900 text-slate-400 py-12 border-t border-slate-800">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-6">
          <div className="flex items-center gap-2">
            <span className="font-extrabold text-white text-lg">Worth<span className="text-indigo-400">IQ</span></span>
            <span className="text-xs text-slate-500">&copy; 2026 WorthIQ. All rights reserved.</span>
          </div>
          <div className="flex items-center gap-6 text-xs">
            <Link to="/login" className="hover:text-white transition-colors">Sign In</Link>
            <Link to="/register" className="hover:text-white transition-colors">Register</Link>
            <a href="#features" className="hover:text-white transition-colors">Features</a>
            <span className="text-slate-600">&middot;</span>
            <span className="text-slate-400">Final-Year B.Tech Project</span>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
