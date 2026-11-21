import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { authService } from '../services/authService';
import { profileService } from '../services/profileService';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    const savedUser = localStorage.getItem('worthiq_user');
    return savedUser ? JSON.parse(savedUser) : null;
  });
  const [tokens, setTokens] = useState(() => {
    const savedTokens = localStorage.getItem('worthiq_tokens');
    return savedTokens ? JSON.parse(savedTokens) : null;
  });
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchProfile = useCallback(async () => {
    try {
      const profileData = await profileService.getProfile();
      setProfile(profileData);
      return profileData;
    } catch (err) {
      console.error('Error fetching profile in AuthContext:', err);
      return null;
    }
  }, []);

  // Initialize auth state
  useEffect(() => {
    const initAuth = async () => {
      if (tokens?.access) {
        try {
          const currentUser = await authService.getCurrentUser();
          setUser(currentUser);
          localStorage.setItem('worthiq_user', JSON.stringify(currentUser));
          await fetchProfile();
        } catch (err) {
          console.error('Failed to validate session:', err);
          logout();
        }
      }
      setLoading(false);
    };

    initAuth();

    // Listen for custom logout events from axios interceptor
    const handleLogoutEvent = () => {
      setUser(null);
      setTokens(null);
      setProfile(null);
    };
    window.addEventListener('worthiq_logout', handleLogoutEvent);
    return () => window.removeEventListener('worthiq_logout', handleLogoutEvent);
  }, [tokens?.access, fetchProfile]);

  const login = async (email, password) => {
    const data = await authService.login({ email, password });
    setUser(data.user);
    setTokens(data.tokens);
    localStorage.setItem('worthiq_user', JSON.stringify(data.user));
    localStorage.setItem('worthiq_tokens', JSON.stringify(data.tokens));

    // Try fetching profile right away
    try {
      const userProfile = await profileService.getProfile();
      setProfile(userProfile);
    } catch {
      setProfile(null);
    }

    return data;
  };

  const register = async (userData) => {
    const data = await authService.register(userData);
    setUser(data.user);
    setTokens(data.tokens);
    localStorage.setItem('worthiq_user', JSON.stringify(data.user));
    localStorage.setItem('worthiq_tokens', JSON.stringify(data.tokens));
    setProfile(null);
    return data;
  };

  const logout = async () => {
    const currentRefreshToken = tokens?.refresh;
    setUser(null);
    setTokens(null);
    setProfile(null);
    localStorage.removeItem('worthiq_user');
    localStorage.removeItem('worthiq_tokens');
    if (currentRefreshToken) {
      await authService.logout(currentRefreshToken);
    }
  };

  const refreshUserProfile = async () => {
    const updated = await fetchProfile();
    if (user && updated) {
      const updatedUser = { ...user, has_profile: true };
      setUser(updatedUser);
      localStorage.setItem('worthiq_user', JSON.stringify(updatedUser));
    }
    return updated;
  };

  const value = {
    user,
    tokens,
    profile,
    loading,
    isAuthenticated: !!user && !!tokens?.access,
    hasProfile: !!profile || !!user?.has_profile,
    login,
    register,
    logout,
    refreshUserProfile,
    setProfile,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
