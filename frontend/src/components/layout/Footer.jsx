import React from 'react';
import { Link } from 'react-router-dom';
import {
  MapPin,
  Mail,
  Phone,
  ArrowUpRight,
  Sparkles,
  TrendingUp,
  ShieldCheck,
  Github,
  Linkedin,
  Twitter,
  Database,
  Code2,
} from 'lucide-react';

export const Footer = () => {
  const handleSmoothScroll = (e, sectionId) => {
    e.preventDefault();
    if (window.location.pathname !== '/') {
      window.location.href = `/#${sectionId}`;
      return;
    }
    const el = document.getElementById(sectionId);
    if (el) {
      const yOffset = -80;
      const y = el.getBoundingClientRect().top + window.pageYOffset + yOffset;
      window.scrollTo({ top: y, behavior: 'smooth' });
      window.history.pushState(null, '', `#${sectionId}`);
    }
  };

  return (
    <footer className="bg-[#0f172a] text-slate-300 pt-16 pb-12 border-t border-slate-800 relative overflow-hidden font-sans">
      {/* Subtle background glow */}
      <div className="absolute top-0 right-1/4 w-96 h-96 bg-indigo-500/5 blur-[120px] rounded-full pointer-events-none" />
      <div className="absolute bottom-0 left-1/4 w-96 h-96 bg-blue-500/5 blur-[120px] rounded-full pointer-events-none" />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        {/* Main 5-Column Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-12 gap-8 lg:gap-8 pb-12 border-b border-slate-800/80">
          
          {/* Column 1: Brand & Bio (3 cols) */}
          <div className="lg:col-span-3 space-y-4">
            <Link to="/" className="inline-flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-indigo-600 via-indigo-500 to-blue-500 flex items-center justify-center shadow-lg shadow-indigo-600/30 text-white font-black text-lg tracking-wider">
                W
              </div>
              <span className="text-xl font-black tracking-tight text-white flex items-center">
                Worth<span className="text-indigo-400">IQ</span>
              </span>
            </Link>

            <p className="text-xs text-slate-400 leading-relaxed pr-2">
              AI-powered Career &amp; Compensation Intelligence platform estimating real market valuation, quantifying skill ROI with SHAP explainability, and mapping engineering career trajectories.
            </p>

            <p className="text-[11px] text-slate-500 pt-2">
              &copy; {new Date().getFullYear()} WorthIQ Platform.<br />
              Final-Year B.Tech CSE Capstone Project.
            </p>
          </div>

          {/* Column 2: Get in Touch (3 cols) */}
          <div className="lg:col-span-3 space-y-3.5">
            <h4 className="text-sm font-bold text-indigo-400 tracking-wider uppercase">
              Get in Touch
            </h4>

            <ul className="space-y-3 text-xs text-slate-300">
              <li className="flex items-start gap-3 group">
                <div className="w-7 h-7 rounded-lg bg-indigo-950/70 border border-indigo-800/50 flex items-center justify-center shrink-0 mt-0.5 text-indigo-400">
                  <MapPin className="w-3.5 h-3.5" />
                </div>
                <div>
                  <span className="font-semibold text-white block">Location</span>
                  <span className="text-slate-400">Tech Hub Zone, Noida &amp; Bengaluru, India</span>
                </div>
              </li>

              <li className="flex items-start gap-3 group">
                <div className="w-7 h-7 rounded-lg bg-indigo-950/70 border border-indigo-800/50 flex items-center justify-center shrink-0 mt-0.5 text-indigo-400">
                  <Mail className="w-3.5 h-3.5" />
                </div>
                <div>
                  <span className="font-semibold text-white block">Email Inquiries</span>
                  <a href="mailto:support@worthiq.ai" className="text-slate-400 hover:text-indigo-300 transition-colors">
                    support@worthiq.ai
                  </a>
                </div>
              </li>

              <li className="flex items-start gap-3 group">
                <div className="w-7 h-7 rounded-lg bg-indigo-950/70 border border-indigo-800/50 flex items-center justify-center shrink-0 mt-0.5 text-indigo-400">
                  <Phone className="w-3.5 h-3.5" />
                </div>
                <div>
                  <span className="font-semibold text-white block">Helpline / Chat</span>
                  <span className="text-slate-400">+91 (120) 456-7890</span>
                </div>
              </li>
            </ul>
          </div>

          {/* Column 3: Intelligence & Services (2 cols) */}
          <div className="lg:col-span-2 space-y-3.5">
            <h4 className="text-sm font-bold text-indigo-400 tracking-wider uppercase">
              Capabilities
            </h4>

            <ul className="space-y-2.5 text-xs text-slate-400">
              <li>
                <Link to="/salary-analysis" className="hover:text-white transition-colors">
                  Salary Potential Engine
                </Link>
              </li>
              <li>
                <Link to="/skill-impact" className="hover:text-white transition-colors">
                  Skill Intelligence &amp; ROI
                </Link>
              </li>
              <li>
                <Link to="/job-matching" className="hover:text-white transition-colors">
                  AI Job Role Matching
                </Link>
              </li>
              <li>
                <Link to="/career-roadmap" className="hover:text-white transition-colors">
                  DAG Career Roadmaps
                </Link>
              </li>
              <li>
                <Link to="/what-if-simulator" className="hover:text-white transition-colors">
                  What-If Simulator
                </Link>
              </li>
              <li>
                <Link to="/resume-analysis" className="hover:text-white transition-colors">
                  Resume Intelligence
                </Link>
              </li>
            </ul>
          </div>

          {/* Column 4: Platform & Links (2 cols) */}
          <div className="lg:col-span-2 space-y-3.5">
            <h4 className="text-sm font-bold text-indigo-400 tracking-wider uppercase">
              Platform
            </h4>

            <ul className="space-y-2.5 text-xs text-slate-400">
              <li>
                <a
                  href="#features"
                  onClick={(e) => handleSmoothScroll(e, 'features')}
                  className="hover:text-white transition-colors"
                >
                  Features Overview
                </a>
              </li>
              <li>
                <a
                  href="#how-it-works"
                  onClick={(e) => handleSmoothScroll(e, 'how-it-works')}
                  className="hover:text-white transition-colors"
                >
                  How It Works
                </a>
              </li>
              <li>
                <a
                  href="#technology"
                  onClick={(e) => handleSmoothScroll(e, 'technology')}
                  className="hover:text-white transition-colors"
                >
                  Technology Stack
                </a>
              </li>
              <li>
                <a
                  href="#about"
                  onClick={(e) => handleSmoothScroll(e, 'about')}
                  className="hover:text-white transition-colors"
                >
                  About the Project
                </a>
              </li>
              <li>
                <Link to="/saved-reports" className="hover:text-white transition-colors">
                  Saved Reports
                </Link>
              </li>
              <li>
                <Link to="/login" className="hover:text-white transition-colors">
                  Sign In
                </Link>
              </li>
            </ul>
          </div>

          {/* Column 5: Social Pills & Tech Note (2 cols) */}
          <div className="lg:col-span-2 space-y-4">
            {/* Blue Circular Icon Buttons (matching screenshot styling) */}
            <div className="flex items-center gap-2.5">
              <a
                href="https://github.com/haniharish/WorthIQ-Skill-Based-Salary-Potential-Career-Growth-Analyzer"
                target="_blank"
                rel="noreferrer"
                aria-label="GitHub Repository"
                className="w-9 h-9 rounded-full bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs flex items-center justify-center shadow-md shadow-blue-600/30 transition-transform hover:-translate-y-0.5"
              >
                Gh
              </a>
              <a
                href="https://linkedin.com"
                target="_blank"
                rel="noreferrer"
                aria-label="LinkedIn Profile"
                className="w-9 h-9 rounded-full bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs flex items-center justify-center shadow-md shadow-blue-600/30 transition-transform hover:-translate-y-0.5"
              >
                In
              </a>
              <a
                href="https://twitter.com"
                target="_blank"
                rel="noreferrer"
                aria-label="Twitter Profile"
                className="w-9 h-9 rounded-full bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs flex items-center justify-center shadow-md shadow-blue-600/30 transition-transform hover:-translate-y-0.5"
              >
                X
              </a>
            </div>

            <p className="text-xs text-slate-400 leading-relaxed">
              Trained on 25,332 verified Indian tech compensation records using calibrated Quantile Random Forest and TreeSHAP explainability.
            </p>

            <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-slate-800/80 border border-slate-700/60 text-[11px] text-emerald-400">
              <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
              <span>Random Forest ML 2.0 Live</span>
            </div>
          </div>

        </div>

        {/* Bottom Bar: Copyright & System Status */}
        <div className="pt-8 flex flex-col sm:flex-row items-center justify-between gap-4 text-xs text-slate-500">
          <p>
            Designed &amp; Developed with React, Tailwind CSS, Django REST Framework &amp; PostgreSQL.
          </p>

          <div className="flex items-center gap-6">
            <span className="hover:text-slate-400 transition-colors cursor-pointer">
              Privacy Policy
            </span>
            <span className="hover:text-slate-400 transition-colors cursor-pointer">
              Terms of Service
            </span>
            <span className="hover:text-slate-400 transition-colors cursor-pointer">
              Security
            </span>
          </div>
        </div>

      </div>
    </footer>
  );
};

export default Footer;
