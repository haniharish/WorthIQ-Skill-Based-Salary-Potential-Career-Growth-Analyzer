import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ToastProvider } from './context/ToastContext';
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
import PredictionExplanationPage from './pages/PredictionExplanationPage';
import ProfilePage from './pages/ProfilePage';
import SettingsPage from './pages/SettingsPage';

export function App() {
  return (
    <AuthProvider>
      <ToastProvider>
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
            
            {/* Skill Intelligence with canonical route and alias */}
            <Route path="/skill-impact" element={<SkillImpactPage />} />
            <Route path="/skill-intelligence" element={<Navigate to="/skill-impact" replace />} />
            <Route path="/skills" element={<Navigate to="/skill-impact" replace />} />

            {/* Job Matching with canonical route and alias */}
            <Route path="/job-matching" element={<JobMatchingPage />} />
            <Route path="/role-matching" element={<Navigate to="/job-matching" replace />} />
            <Route path="/roles" element={<Navigate to="/job-matching" replace />} />

            {/* Career Roadmap with canonical route and alias */}
            <Route path="/career-roadmap" element={<CareerRoadmapPage />} />
            <Route path="/roadmaps" element={<Navigate to="/career-roadmap" replace />} />

            {/* What-If Simulation Sandbox */}
            <Route path="/what-if-simulator" element={<WhatIfSimulatorPage />} />

            {/* Saved Reports with canonical route and alias */}
            <Route path="/saved-reports" element={<SavedReportsPage />} />
            <Route path="/reports" element={<Navigate to="/saved-reports" replace />} />

            {/* SHAP Explainability Engine */}
            <Route path="/explanations/:predictionId" element={<PredictionExplanationPage />} />

            {/* Profile and Settings */}
            <Route path="/profile" element={<ProfilePage />} />
            <Route path="/settings" element={<SettingsPage />} />
          </Route>

          {/* Catch-all redirect */}
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </ToastProvider>
    </AuthProvider>
  );
}

export default App;
