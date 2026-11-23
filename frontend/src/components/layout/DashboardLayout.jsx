import React, { useState, useEffect } from 'react';
import { NavLink, Outlet, useNavigate, useLocation, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Logo } from '../common/Logo';
import { Breadcrumbs } from '../ui/Breadcrumbs';
import {
  LayoutDashboard,
  TrendingUp,
  Sparkles,
  Briefcase,
  Compass,
  Sliders,
  BookmarkCheck,
  User,
  Settings,
  LogOut,
  ChevronDown,
  Menu,
  X,
  PlusCircle,
  HelpCircle,
} from 'lucide-react';

const navigationGroups = [
  {
    group: 'Main',
    items: [
      { name: 'Overview', path: '/dashboard', icon: LayoutDashboard },
      { name: 'Salary Analysis', path: '/salary-analysis', icon: TrendingUp },
      { name: 'Saved Reports', path: '/saved-reports', icon: BookmarkCheck },
    ],
  },
  {
    group: 'Intelligence Engine',
    items: [
      { name: 'Skill Intelligence', path: '/skill-impact', icon: Sparkles },
      { name: 'Job Role Matching', path: '/job-matching', icon: Briefcase },
      { name: 'Career Roadmap', path: '/career-roadmap', icon: Compass },
      { name: 'What-If Simulator', path: '/what-if-simulator', icon: Sliders },
    ],
  },
  {
    group: 'Account & Settings',
    items: [
      { name: 'My Profile', path: '/profile', icon: User },
      { name: 'Settings', path: '/settings', icon: Settings },
    ],
  },
];

export const DashboardLayout = () => {
  const { user, profile, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [profileDropdownOpen, setProfileDropdownOpen] = useState(false);

  // Close drawer on escape key
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === 'Escape') {
        setSidebarOpen(false);
        setProfileDropdownOpen(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  // Close profile dropdown on outside click
  useEffect(() => {
    const handleClickOutside = () => {
      setProfileDropdownOpen(false);
    };
    if (profileDropdownOpen) {
      window.addEventListener('click', handleClickOutside);
    }
    return () => window.removeEventListener('click', handleClickOutside);
  }, [profileDropdownOpen]);

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const initials = user?.full_name
    ? user.full_name
        .split(' ')
        .map((n) => n[0])
        .join('')
        .toUpperCase()
        .slice(0, 2)
    : 'WQ';

  return (
    <div className="min-h-screen bg-[#F7F8FC] flex flex-col antialiased text-[#172033]">
      {/* Top Navbar */}
      <header className="sticky top-0 z-40 h-16 bg-white/95 backdrop-blur-xs border-b border-slate-200/90 flex items-center justify-between px-4 sm:px-6 lg:px-8">
        <div className="flex items-center gap-3 sm:gap-4">
          <button
            type="button"
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="lg:hidden p-2 rounded-xl text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition-colors"
            aria-label="Toggle navigation menu"
            aria-expanded={sidebarOpen}
          >
            {sidebarOpen ? <X className="w-5 h-5" /> : <Menu className="w-5 h-5" />}
          </button>
          <Logo size="sm" to="/dashboard" />

          <div className="hidden sm:block h-5 w-px bg-slate-200" />

          {/* Breadcrumbs aligned cleanly to the left next to Logo */}
          <div className="hidden sm:flex items-center">
            <Breadcrumbs />
          </div>
        </div>

        {/* Right Header controls */}
        <div className="flex items-center gap-3">
          <Link
            to="/salary-analysis"
            className="hidden sm:inline-flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg text-white bg-indigo-600 hover:bg-indigo-700 shadow-2xs transition-colors"
          >
            <PlusCircle className="w-3.5 h-3.5" />
            <span>Analyze Salary</span>
          </Link>

          {/* User Profile dropdown */}
          <div className="relative">
            <button
              type="button"
              onClick={(e) => {
                e.stopPropagation();
                setProfileDropdownOpen(!profileDropdownOpen);
              }}
              className="flex items-center gap-2.5 p-1 rounded-xl hover:bg-slate-100 transition-colors cursor-pointer"
              aria-expanded={profileDropdownOpen}
              aria-label="User profile options"
            >
              <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-indigo-600 to-violet-600 text-white font-bold text-xs flex items-center justify-center shadow-xs">
                {initials}
              </div>
              <div className="hidden sm:block text-left max-w-[130px]">
                <p className="text-xs font-bold text-slate-900 leading-tight truncate">
                  {user?.full_name || 'Engineer'}
                </p>
                <p className="text-[10px] text-slate-500 leading-tight truncate">
                  {profile?.job_role || user?.email}
                </p>
              </div>
              <ChevronDown className="w-3.5 h-3.5 text-slate-400" />
            </button>

            {profileDropdownOpen && (
              <div
                className="absolute right-0 mt-2 w-56 bg-white rounded-2xl shadow-xl border border-slate-200 py-1.5 z-50 animate-in fade-in zoom-in-95 duration-150"
                onClick={(e) => e.stopPropagation()}
              >
                <div className="px-4 py-2.5 border-b border-slate-100 bg-slate-50/50">
                  <p className="text-xs font-bold text-slate-900 truncate">{user?.full_name}</p>
                  <p className="text-[11px] text-slate-500 truncate">{user?.email}</p>
                </div>

                <div className="py-1">
                  <NavLink
                    to="/profile"
                    onClick={() => setProfileDropdownOpen(false)}
                    className="flex items-center gap-2.5 px-4 py-2 text-xs font-medium text-slate-700 hover:bg-indigo-50 hover:text-indigo-600 transition-colors"
                  >
                    <User className="w-4 h-4 text-slate-400" />
                    <span>My Profile</span>
                  </NavLink>
                  <NavLink
                    to="/settings"
                    onClick={() => setProfileDropdownOpen(false)}
                    className="flex items-center gap-2.5 px-4 py-2 text-xs font-medium text-slate-700 hover:bg-indigo-50 hover:text-indigo-600 transition-colors"
                  >
                    <Settings className="w-4 h-4 text-slate-400" />
                    <span>Settings</span>
                  </NavLink>
                </div>

                <div className="pt-1 border-t border-slate-100">
                  <button
                    type="button"
                    onClick={handleLogout}
                    className="w-full flex items-center gap-2.5 px-4 py-2 text-xs font-medium text-rose-600 hover:bg-rose-50 cursor-pointer text-left transition-colors"
                  >
                    <LogOut className="w-4 h-4 text-rose-500" />
                    <span>Sign Out</span>
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Main Container */}
      <div className="flex-1 flex overflow-hidden">
        {/* Mobile Backdrop */}
        {sidebarOpen && (
          <div
            className="fixed inset-0 z-20 bg-slate-900/40 backdrop-blur-2xs lg:hidden transition-opacity"
            onClick={() => setSidebarOpen(false)}
            aria-hidden="true"
          />
        )}

        {/* Sidebar Navigation */}
        <aside
          className={`
            fixed lg:static inset-y-16 left-0 z-30 w-64 bg-white border-r border-slate-200/90
            flex flex-col transition-transform duration-200 ease-in-out shadow-xs lg:shadow-none
            ${sidebarOpen ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
          `}
        >
          {/* Navigation group loop */}
          <div className="flex-1 overflow-y-auto px-3 py-5 space-y-6">
            {navigationGroups.map((group) => (
              <div key={group.group} className="space-y-1">
                <p className="px-3 text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-2">
                  {group.group}
                </p>
                {group.items.map((item) => {
                  const Icon = item.icon;
                  return (
                    <NavLink
                      key={item.path}
                      to={item.path}
                      onClick={() => setSidebarOpen(false)}
                      className={({ isActive }) => `
                        flex items-center justify-between px-3 py-2 rounded-xl text-xs font-semibold transition-all group
                        ${
                          isActive
                            ? 'bg-indigo-50 text-indigo-700 shadow-2xs font-bold'
                            : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                        }
                      `}
                    >
                      <div className="flex items-center gap-2.5">
                        <Icon
                          className={`w-4 h-4 transition-colors ${
                            location.pathname === item.path
                              ? 'text-indigo-600'
                              : 'text-slate-400 group-hover:text-slate-600'
                          }`}
                        />
                        <span>{item.name}</span>
                      </div>
                      {item.badge && (
                        <span
                          className={`text-[10px] px-1.5 py-0.5 rounded-full font-bold ${
                            item.badge === 'AI'
                              ? 'bg-violet-100 text-violet-700'
                              : 'bg-indigo-100 text-indigo-700'
                          }`}
                        >
                          {item.badge}
                        </span>
                      )}
                    </NavLink>
                  );
                })}
              </div>
            ))}
          </div>

          {/* Sidebar Footer */}
          <div className="p-3 border-t border-slate-100 bg-slate-50/50">
            <div className="p-3 rounded-xl bg-white border border-slate-200/80 shadow-2xs">
              <div className="flex items-center gap-2 mb-1">
                <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
                <span className="text-[11px] font-bold text-slate-800">WorthIQ AI Active</span>
              </div>
              <p className="text-[10px] text-slate-500 leading-tight">
                Model: Random Forest Regressor 2.0 &middot; SHAP Explainer
              </p>
            </div>
          </div>
        </aside>

        {/* Content Outlet */}
        <main className="flex-1 overflow-y-auto px-4 sm:px-6 lg:px-8 py-6 sm:py-8">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;
