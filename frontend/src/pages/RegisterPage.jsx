import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Logo } from '../components/common/Logo';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { User, Mail, Lock, AlertCircle, ArrowRight, CheckCircle2 } from 'lucide-react';

export const RegisterPage = () => {
  const { register } = useAuth();
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    password: '',
    confirm_password: '',
  });
  const [errors, setErrors] = useState({});
  const [serverError, setServerError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const validate = () => {
    const newErrors = {};

    if (!formData.full_name.trim()) {
      newErrors.full_name = 'Full name is required.';
    }

    if (!formData.email.trim()) {
      newErrors.email = 'Email address is required.';
    } else if (!/\S+@\S+\.\S+/.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address.';
    }

    if (!formData.password) {
      newErrors.password = 'Password is required.';
    } else if (formData.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters.';
    }

    if (!formData.confirm_password) {
      newErrors.confirm_password = 'Password confirmation is required.';
    } else if (formData.password !== formData.confirm_password) {
      newErrors.confirm_password = 'Passwords do not match.';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
    if (errors[name]) {
      setErrors((prev) => ({ ...prev, [name]: '' }));
    }
    if (serverError) {
      setServerError('');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;

    setIsLoading(true);
    setServerError('');

    try {
      await register({
        full_name: formData.full_name.trim(),
        email: formData.email.trim().toLowerCase(),
        password: formData.password,
        confirm_password: formData.confirm_password,
      });

      // Newly registered users are navigated straight to Profile Setup
      navigate('/profile/setup');
    } catch (err) {
      console.error('Registration error:', err);
      if (err.response?.data) {
        const data = err.response.data;
        if (data.email) {
          setErrors((prev) => ({ ...prev, email: Array.isArray(data.email) ? data.email.join(' ') : data.email }));
        } else if (data.password) {
          setErrors((prev) => ({ ...prev, password: Array.isArray(data.password) ? data.password.join(' ') : data.password }));
        } else if (data.confirm_password) {
          setErrors((prev) => ({ ...prev, confirm_password: Array.isArray(data.confirm_password) ? data.confirm_password.join(' ') : data.confirm_password }));
        } else if (data.non_field_errors) {
          setServerError(data.non_field_errors.join(' '));
        } else if (data.detail) {
          setServerError(data.detail);
        } else {
          setServerError('Registration failed. Please check your information.');
        }
      } else {
        setServerError('Cannot connect to WorthIQ backend server. Ensure Django is running on port 8000.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8 antialiased">
      <div className="sm:mx-auto sm:w-full sm:max-w-md text-center">
        <Logo size="lg" to="/" />
        <h2 className="mt-6 text-2xl font-extrabold text-slate-900 tracking-tight">
          Create your WorthIQ Account
        </h2>
        <p className="mt-2 text-xs text-slate-500">
          Get real-time salary benchmarks and personalized skill gap insights
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-6 sm:px-10 shadow-sm border border-slate-200/90 rounded-2xl">
          {serverError && (
            <div className="mb-6 p-3 rounded-lg bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-start gap-2.5">
              <AlertCircle className="w-4 h-4 shrink-0 mt-0.5 text-rose-500" />
              <span>{serverError}</span>
            </div>
          )}

          <form className="space-y-4" onSubmit={handleSubmit} noValidate>
            <Input
              label="Full Name"
              name="full_name"
              type="text"
              placeholder="e.g. Alex Morgan"
              icon={User}
              value={formData.full_name}
              onChange={handleChange}
              error={errors.full_name}
              required
              autoFocus
            />

            <Input
              label="Email Address"
              name="email"
              type="email"
              placeholder="you@example.com"
              icon={Mail}
              value={formData.email}
              onChange={handleChange}
              error={errors.email}
              required
              autoComplete="email"
            />

            <Input
              label="Password"
              name="password"
              type="password"
              placeholder="Minimum 6 characters"
              icon={Lock}
              value={formData.password}
              onChange={handleChange}
              error={errors.password}
              required
              autoComplete="new-password"
            />

            <Input
              label="Confirm Password"
              name="confirm_password"
              type="password"
              placeholder="Re-enter your password"
              icon={Lock}
              value={formData.confirm_password}
              onChange={handleChange}
              error={errors.confirm_password}
              required
              autoComplete="new-password"
            />

            <div className="pt-2">
              <Button
                type="submit"
                variant="primary"
                size="md"
                className="w-full"
                isLoading={isLoading}
                iconRight={ArrowRight}
              >
                Create Account
              </Button>
            </div>
          </form>

          <div className="mt-6 pt-6 border-t border-slate-100 text-center">
            <p className="text-xs text-slate-600">
              Already have an account?{' '}
              <Link to="/login" className="font-semibold text-indigo-600 hover:text-indigo-700">
                Sign in instead
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RegisterPage;
