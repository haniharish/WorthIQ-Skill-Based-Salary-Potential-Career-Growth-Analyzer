import React from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Card, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import {
  Settings,
  Shield,
  Database,
  User,
  LogOut,
  Sun,
  Laptop,
  CheckCircle2,
  Lock,
  Calendar,
  ExternalLink,
} from 'lucide-react';

export const SettingsPage = () => {
  const { user, profile, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6 pb-12">
      {/* Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          System &amp; Account Settings
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1">
          Manage your account profile, authentication sessions, and system configuration
        </p>
      </div>

      {/* Account Profile Summary */}
      <Card>
        <CardHeader
          title="Account Profile"
          subtitle="Signed in account credentials and linked profile"
          icon={User}
        />
        <div className="pt-2 divide-y divide-slate-100 text-xs">
          <div className="py-3 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <p className="font-semibold text-slate-800">Full Name</p>
              <p className="text-slate-500 text-[11px] mt-0.5">{user?.full_name || 'Not provided'}</p>
            </div>
            <Link to="/profile">
              <Button variant="outline" size="sm">
                Edit in Profile
              </Button>
            </Link>
          </div>

          <div className="py-3 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <p className="font-semibold text-slate-800">Email Address</p>
              <p className="text-slate-500 text-[11px] mt-0.5">{user?.email}</p>
            </div>
            <Badge variant="emerald" size="xs" dot>
              Verified Active
            </Badge>
          </div>

          <div className="py-3 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
            <div>
              <p className="font-semibold text-slate-800">Registered Job Track</p>
              <p className="text-slate-500 text-[11px] mt-0.5">
                {profile?.job_role || 'Not configured'} &middot; {profile?.years_of_experience ?? 0} yrs exp
              </p>
            </div>
            <Link to="/profile/setup">
              <Button variant="outline" size="sm">
                Update Track
              </Button>
            </Link>
          </div>
        </div>
      </Card>

      {/* Display & Theme Preferences */}
      <Card>
        <CardHeader
          title="Appearance &amp; Accessibility"
          subtitle="Interface color themes and display modes"
          icon={Sun}
        />
        <div className="space-y-4 pt-2 text-xs">
          <div className="flex items-center justify-between p-3.5 rounded-xl bg-slate-50 border border-slate-100">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-white border border-slate-200 text-amber-500">
                <Sun className="w-4 h-4" />
              </div>
              <div>
                <p className="font-semibold text-slate-800">Theme Mode</p>
                <p className="text-slate-500 text-[11px]">SaaS Light theme optimized for analytical clarity</p>
              </div>
            </div>
            <Badge variant="indigo" size="xs">
              Light Default
            </Badge>
          </div>

          <div className="flex items-center justify-between p-3.5 rounded-xl bg-slate-50 border border-slate-100">
            <div className="flex items-center gap-3">
              <div className="p-2 rounded-lg bg-white border border-slate-200 text-indigo-600">
                <Laptop className="w-4 h-4" />
              </div>
              <div>
                <p className="font-semibold text-slate-800">Motion &amp; Animations</p>
                <p className="text-slate-500 text-[11px]">Respects system prefers-reduced-motion setting</p>
              </div>
            </div>
            <Badge variant="emerald" size="xs">
              Auto Adapted
            </Badge>
          </div>
        </div>
      </Card>

      {/* Security & Authentication */}
      <Card>
        <CardHeader
          title="Security &amp; JWT Session"
          subtitle="Token lifecycle and cryptographic settings"
          icon={Shield}
        />
        <div className="space-y-3 pt-2 text-xs">
          <div className="flex items-center justify-between p-3.5 rounded-xl bg-slate-50 border border-slate-100">
            <div>
              <p className="font-semibold text-slate-800">Access Token Lifetime</p>
              <p className="text-slate-500 text-[11px]">Rotates automatically via Django REST Framework SimpleJWT</p>
            </div>
            <Badge variant="indigo" size="xs">
              60 Minutes
            </Badge>
          </div>

          <div className="flex items-center justify-between p-3.5 rounded-xl bg-slate-50 border border-slate-100">
            <div>
              <p className="font-semibold text-slate-800">Refresh Token Rotation &amp; Blacklisting</p>
              <p className="text-slate-500 text-[11px]">Active with server-side PostgreSQL blacklist</p>
            </div>
            <Badge variant="emerald" size="xs">
              Enforced
            </Badge>
          </div>

          <div className="p-3.5 rounded-xl bg-rose-50/50 border border-rose-100 flex items-center justify-between">
            <div>
              <p className="font-semibold text-rose-950">Active Session</p>
              <p className="text-rose-700 text-[11px]">Sign out of current browser session and revoke refresh token</p>
            </div>
            <Button
              variant="outline"
              size="sm"
              icon={LogOut}
              onClick={handleLogout}
              className="border-rose-300 text-rose-800 hover:bg-rose-100/70"
            >
              Sign Out
            </Button>
          </div>
        </div>
      </Card>

      {/* Services & Database Architecture */}
      <Card>
        <CardHeader
          title="Services &amp; Infrastructure"
          subtitle="Local development ports and database container status"
          icon={Database}
        />
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2 text-xs">
          <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-100">
            <span className="text-[10px] font-bold text-slate-400 uppercase">PostgreSQL Database</span>
            <p className="text-sm font-bold text-slate-900 mt-1">Docker :5432</p>
            <p className="text-[11px] text-slate-500 mt-0.5">worthiq_db &middot; Healthy</p>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-100">
            <span className="text-[10px] font-bold text-slate-400 uppercase">Django Backend</span>
            <p className="text-sm font-bold text-slate-900 mt-1">Port 8000</p>
            <p className="text-[11px] text-slate-500 mt-0.5">Django 5.2 &middot; DRF</p>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-100">
            <span className="text-[10px] font-bold text-slate-400 uppercase">React Vite Frontend</span>
            <p className="text-sm font-bold text-slate-900 mt-1">Port 5180</p>
            <p className="text-[11px] text-slate-500 mt-0.5">strictPort: true</p>
          </div>
        </div>
      </Card>
    </div>
  );
};

export default SettingsPage;
