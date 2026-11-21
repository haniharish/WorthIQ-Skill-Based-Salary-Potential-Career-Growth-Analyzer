import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Card, CardHeader } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Badge } from '../components/ui/Badge';
import {
  User,
  Mail,
  Briefcase,
  Clock,
  MapPin,
  GraduationCap,
  IndianRupee,
  Sparkles,
  Edit,
  ShieldCheck,
  Calendar,
} from 'lucide-react';

export const ProfilePage = () => {
  const { user, profile } = useAuth();

  const formattedDate = user?.date_joined
    ? new Date(user.date_joined).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
      })
    : 'Recently';

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            My Professional Profile
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 mt-1">
            Persisted user account and technical skill records in PostgreSQL
          </p>
        </div>

        <Link to="/profile/setup">
          <Button variant="primary" size="md" icon={Edit}>
            Edit Profile Data
          </Button>
        </Link>
      </div>

      {/* Account Info Card */}
      <Card>
        <CardHeader
          title="Account Information"
          subtitle="Authentication and security credentials"
          icon={User}
          badge={<Badge variant="emerald" dot={true}>Verified Active</Badge>}
        />

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6 pt-2">
          <div className="space-y-1">
            <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Full Name</p>
            <p className="text-sm font-bold text-slate-900">{user?.full_name}</p>
          </div>

          <div className="space-y-1">
            <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Email Address</p>
            <p className="text-sm font-semibold text-slate-700">{user?.email}</p>
          </div>

          <div className="space-y-1">
            <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Member Since</p>
            <p className="text-sm text-slate-600 flex items-center gap-1.5">
              <Calendar className="w-3.5 h-3.5 text-slate-400" />
              {formattedDate}
            </p>
          </div>

          <div className="space-y-1">
            <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Security Method</p>
            <p className="text-sm text-slate-600 flex items-center gap-1.5">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
              JWT Bearer &middot; Password Hashed
            </p>
          </div>
        </div>
      </Card>

      {/* Career Details Card */}
      <Card>
        <CardHeader
          title="Career & Compensation Profile"
          subtitle="Model inputs used for market benchmarking"
          icon={Briefcase}
        />

        {!profile ? (
          <div className="text-center py-6">
            <p className="text-xs text-slate-500 mb-3">No career details saved yet.</p>
            <Link to="/profile/setup">
              <Button variant="primary" size="sm">
                Set Up Career Details
              </Button>
            </Link>
          </div>
        ) : (
          <div className="space-y-6 pt-2">
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
              <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-100">
                <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Target Role</p>
                <p className="text-sm font-bold text-slate-900 mt-1">{profile.job_role}</p>
              </div>

              <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-100">
                <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Experience</p>
                <p className="text-sm font-bold text-slate-900 mt-1">
                  {profile.years_of_experience} {profile.years_of_experience === 1 ? 'Year' : 'Years'}
                </p>
              </div>

              <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-100">
                <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Location</p>
                <p className="text-sm font-bold text-slate-900 mt-1">
                  {profile.location || 'Not specified'}
                </p>
              </div>

              <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-100">
                <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Current Salary</p>
                <p className="text-sm font-bold text-slate-900 mt-1">
                  {profile.current_salary ? `₹${profile.current_salary} LPA` : 'Private / Unspecified'}
                </p>
              </div>
            </div>

            {/* Education */}
            {profile.education && (
              <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-100 flex items-center gap-3">
                <div className="p-2 rounded-lg bg-indigo-50 text-indigo-600">
                  <GraduationCap className="w-4 h-4" />
                </div>
                <div>
                  <p className="text-[11px] font-semibold text-slate-400 uppercase tracking-wider">Highest Education</p>
                  <p className="text-sm font-semibold text-slate-800">{profile.education}</p>
                </div>
              </div>
            )}

            {/* Skills */}
            <div>
              <p className="text-xs font-semibold text-slate-700 uppercase tracking-wider mb-2.5">
                Technical Skills ({profile.skills?.length || 0})
              </p>
              <div className="flex flex-wrap gap-2">
                {profile.skills?.map((skill) => (
                  <span
                    key={skill.id || skill.name}
                    className="px-3 py-1 text-xs font-semibold rounded-lg bg-indigo-50 border border-indigo-200/80 text-indigo-700"
                  >
                    {skill.name}
                  </span>
                ))}
              </div>
            </div>
          </div>
        )}
      </Card>
    </div>
  );
};

export default ProfilePage;
