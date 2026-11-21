import React from 'react';
import { useAuth } from '../context/AuthContext';
import { Card, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import { Settings, Shield, Bell, Database, Server, Key } from 'lucide-react';

export const SettingsPage = () => {
  const { user } = useAuth();

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          System &amp; Account Settings
        </h1>
        <p className="text-xs sm:text-sm text-slate-500 mt-1">
          Manage your environment preferences, authentication sessions and system integrations
        </p>
      </div>

      {/* Security & Authentication */}
      <Card>
        <CardHeader
          title="Security &amp; JWT Session"
          subtitle="Token lifecycle and cryptographic settings"
          icon={Shield}
        />
        <div className="space-y-4 pt-2 text-xs">
          <div className="flex items-center justify-between p-3 rounded-lg bg-slate-50 border border-slate-100">
            <div>
              <p className="font-semibold text-slate-800">Access Token Lifetime</p>
              <p className="text-slate-500 text-[11px]">Rotates automatically via Django REST Framework SimpleJWT</p>
            </div>
            <Badge variant="indigo" size="xs">60 Minutes</Badge>
          </div>

          <div className="flex items-center justify-between p-3 rounded-lg bg-slate-50 border border-slate-100">
            <div>
              <p className="font-semibold text-slate-800">Refresh Token Rotation &amp; Blacklisting</p>
              <p className="text-slate-500 text-[11px]">Enabled with server-side blacklist table</p>
            </div>
            <Badge variant="emerald" size="xs">Active</Badge>
          </div>
        </div>
      </Card>

      {/* Database Connection Info */}
      <Card>
        <CardHeader
          title="Database &amp; Services Architecture"
          subtitle="PostgreSQL container and API endpoints"
          icon={Database}
        />
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 pt-2 text-xs">
          <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-100">
            <span className="text-[10px] font-bold text-slate-400 uppercase">PostgreSQL Database</span>
            <p className="text-sm font-bold text-slate-900 mt-1">Docker :5432</p>
            <p className="text-[11px] text-slate-500 mt-0.5">worthiq_db &middot; Containerized</p>
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
