import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Menu, X, ArrowRight, LayoutDashboard, LogOut, Sparkles } from 'lucide-react';

export const Navbar = () => {
  const { isAuthenticated, user, logout } = useAuth();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [isScrolled, setIsScrolled] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20);
    };
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const handleLogout = async () => {
    await logout();
    navigate('/');
  };

  const handleNavClick = (e, sectionId) => {
    e.preventDefault();
    if (window.location.pathname !== '/') {
      navigate(`/#${sectionId}`);
      return;
    }
    const el = document.getElementById(sectionId);
    if (el) {
      const yOffset = -90;
      const y = el.getBoundingClientRect().top + window.pageYOffset + yOffset;
      window.scrollTo({ top: y, behavior: 'smooth' });
    }
    if (mobileMenuOpen) {
      setMobileMenuOpen(false);
    }
  };

  return (
    <header className="sticky top-3 sm:top-5 z-50 px-3 sm:px-6 w-full max-w-5xl mx-auto transition-all duration-300 font-sans">
      {/* Floating Island Pill Container */}
      <div
        className={`rounded-full px-3.5 sm:px-5 py-2.5 transition-all duration-300 flex items-center justify-between border ${
          isScrolled
            ? 'bg-slate-950/95 backdrop-blur-xl border-slate-800 shadow-2xl shadow-slate-950/40'
            : 'bg-slate-900/90 backdrop-blur-lg border-slate-800/80 shadow-xl shadow-slate-950/20'
        }`}
      >
        {/* Left: Circular Logo Badge & Brand Name */}
        <Link to="/" className="flex items-center gap-2.5 group shrink-0">
          <div className="w-8 h-8 rounded-full bg-white text-slate-950 flex items-center justify-center font-black text-sm shadow-md group-hover:scale-105 transition-transform">
            W
          </div>
          <span className="text-sm sm:text-base font-extrabold tracking-tight text-white flex items-center">
            Worth<span className="text-indigo-400">IQ</span>
          </span>
        </Link>

        {/* Center: Sleek Desktop Navigation Links */}
        <nav className="hidden md:flex items-center gap-1 sm:gap-2">
          <a
            href="#features"
            onClick={(e) => handleNavClick(e, 'features')}
            className="px-3.5 py-1.5 rounded-full text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-800/70 transition-all"
          >
            Features
          </a>
          <a
            href="#how-it-works"
            onClick={(e) => handleNavClick(e, 'how-it-works')}
            className="px-3.5 py-1.5 rounded-full text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-800/70 transition-all"
          >
            How It Works
          </a>
          <a
            href="#technology"
            onClick={(e) => handleNavClick(e, 'technology')}
            className="px-3.5 py-1.5 rounded-full text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-800/70 transition-all"
          >
            Technology
          </a>
          <a
            href="#about"
            onClick={(e) => handleNavClick(e, 'about')}
            className="px-3.5 py-1.5 rounded-full text-xs font-semibold text-slate-300 hover:text-white hover:bg-slate-800/70 transition-all"
          >
            About
          </a>
        </nav>

        {/* Right: High-Contrast Pill CTA */}
        <div className="hidden sm:flex items-center gap-2.5 shrink-0">
          {isAuthenticated ? (
            <div className="flex items-center gap-2">
              <Link
                to="/dashboard"
                className="bg-white hover:bg-slate-100 text-slate-950 px-4 py-1.5 rounded-full text-xs font-bold shadow-md transition-all flex items-center gap-1.5 group"
              >
                <LayoutDashboard className="w-3.5 h-3.5 text-indigo-600" />
                <span>Dashboard</span>
                <ArrowRight className="w-3 h-3 group-hover:translate-x-0.5 transition-transform" />
              </Link>
              <button
                type="button"
                onClick={handleLogout}
                title="Sign Out"
                className="p-1.5 rounded-full text-slate-400 hover:text-rose-400 hover:bg-slate-800/80 transition-colors"
              >
                <LogOut className="w-3.5 h-3.5" />
              </button>
            </div>
          ) : (
            <div className="flex items-center gap-2">
              <Link
                to="/login"
                className="px-3 py-1.5 rounded-full text-xs font-semibold text-slate-300 hover:text-white transition-colors"
              >
                Sign In
              </Link>
              <Link
                to="/register"
                className="bg-white hover:bg-slate-100 text-slate-950 px-4 py-2 rounded-full text-xs font-bold shadow-md transition-all flex items-center gap-1.5 group hover:scale-[1.02]"
              >
                <span>Get Started Free</span>
                <ArrowRight className="w-3 h-3 group-hover:translate-x-0.5 transition-transform" />
              </Link>
            </div>
          )}
        </div>

        {/* Mobile Hamburger Toggle */}
        <div className="flex sm:hidden items-center gap-2">
          {!isAuthenticated && (
            <Link
              to="/login"
              className="px-2.5 py-1 text-[11px] font-semibold text-slate-300 hover:text-white"
            >
              Sign In
            </Link>
          )}
          <button
            type="button"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="p-1.5 rounded-full text-slate-300 hover:text-white bg-slate-800/60 hover:bg-slate-800 transition-colors focus:outline-none"
            aria-label="Toggle navigation menu"
          >
            {mobileMenuOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
        </div>
      </div>

      {/* Mobile Floating Dropdown Menu Card */}
      {mobileMenuOpen && (
        <div className="sm:hidden mt-2 bg-slate-950/95 backdrop-blur-2xl border border-slate-800/90 rounded-3xl p-4 shadow-2xl space-y-3 animate-in fade-in slide-in-from-top-2 duration-200">
          <nav className="flex flex-col space-y-1 text-xs font-medium text-slate-300">
            <a
              href="#features"
              onClick={(e) => handleNavClick(e, 'features')}
              className="px-3 py-2 rounded-xl hover:bg-slate-800/80 hover:text-white transition-colors"
            >
              Features
            </a>
            <a
              href="#how-it-works"
              onClick={(e) => handleNavClick(e, 'how-it-works')}
              className="px-3 py-2 rounded-xl hover:bg-slate-800/80 hover:text-white transition-colors"
            >
              How It Works
            </a>
            <a
              href="#technology"
              onClick={(e) => handleNavClick(e, 'technology')}
              className="px-3 py-2 rounded-xl hover:bg-slate-800/80 hover:text-white transition-colors"
            >
              Technology
            </a>
            <a
              href="#about"
              onClick={(e) => handleNavClick(e, 'about')}
              className="px-3 py-2 rounded-xl hover:bg-slate-800/80 hover:text-white transition-colors"
            >
              About
            </a>
          </nav>

          <div className="pt-2 border-t border-slate-800/80 flex flex-col gap-2">
            {isAuthenticated ? (
              <>
                <Link
                  to="/dashboard"
                  onClick={() => setMobileMenuOpen(false)}
                  className="bg-white text-slate-950 text-center py-2.5 rounded-full text-xs font-bold shadow-md flex items-center justify-center gap-1.5"
                >
                  <LayoutDashboard className="w-3.5 h-3.5 text-indigo-600" />
                  <span>Go to Dashboard</span>
                </Link>
                <button
                  type="button"
                  onClick={handleLogout}
                  className="py-2 rounded-full text-xs text-rose-400 hover:bg-slate-900 border border-slate-800 text-center font-medium"
                >
                  Sign Out
                </button>
              </>
            ) : (
              <>
                <Link
                  to="/register"
                  onClick={() => setMobileMenuOpen(false)}
                  className="bg-white text-slate-950 text-center py-2.5 rounded-full text-xs font-bold shadow-md flex items-center justify-center gap-1.5"
                >
                  <span>Get Started Free</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
                <Link
                  to="/login"
                  onClick={() => setMobileMenuOpen(false)}
                  className="text-center py-2 text-xs text-slate-300 hover:text-white font-medium"
                >
                  Sign In to Account
                </Link>
              </>
            )}
          </div>
        </div>
      )}
    </header>
  );
};

export default Navbar;
