import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import ProtectedRoute from './components/common/ProtectedRoute';
import PublicRoute from './components/common/PublicRoute';

// Layouts & Pages
import DashboardLayout from './components/layout/DashboardLayout';
import LandingPage from './pages/LandingPage';
import LoginPage from './pages/LoginPage';
import RegisterPage from './pages/RegisterPage';
import ProfileSetupPage from './pages/ProfileSetupPage';
import DashboardPage from './pages/DashboardPage';
import SalaryAnalysisPage from './pages/SalaryAnalysisPage';
import SkillImpactPage from './pages/SkillImpactPage';
import JobMatchingPage from './pages/JobMatchingPage';
import CareerRoadmapPage from './pages/CareerRoadmapPage';
import WhatIfSimulatorPage from './pages/WhatIfSimulatorPage';
import SavedReportsPage from './pages/SavedReportsPage';
import ProfilePage from './pages/ProfilePage';
import SettingsPage from './pages/SettingsPage';

export function App() {
  return (
    <AuthProvider>
      <Routes>
        {/* Public Landing Page */}
        <Route path="/" element={<LandingPage />} />

        {/* Auth Pages (Restricted when logged in) */}
        <Route
          path="/login"
          element={
            <PublicRoute>
              <LoginPage />
            </PublicRoute>
          }
        />
        <Route
          path="/register"
          element={
            <PublicRoute>
              <RegisterPage />
            </PublicRoute>
          }
        />

        {/* Profile Setup Page (Accessible to authenticated users) */}
        <Route
          path="/profile/setup"
          element={
            <ProtectedRoute>
              <ProfileSetupPage />
            </ProtectedRoute>
          }
        />

        {/* Authenticated Dashboard Shell and Sub-routes */}
        <Route
          element={
            <ProtectedRoute>
              <DashboardLayout />
            </ProtectedRoute>
          }
        >
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/salary-analysis" element={<SalaryAnalysisPage />} />
          <Route path="/skill-impact" element={<SkillImpactPage />} />
          <Route path="/job-matching" element={<JobMatchingPage />} />
          <Route path="/career-roadmap" element={<CareerRoadmapPage />} />
          <Route path="/what-if-simulator" element={<WhatIfSimulatorPage />} />
          <Route path="/saved-reports" element={<SavedReportsPage />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/settings" element={<SettingsPage />} />
        </Route>

        {/* Catch-all redirect */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AuthProvider>
  );
}

export default App;
