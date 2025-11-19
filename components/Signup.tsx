import React, { useState } from 'react';
import { ArrowLeft, Mail, Lock, User } from 'lucide-react';
import { COLORS, GRADIENTS } from '../constants';
import Button from './Button';

interface SignupProps {
  onSignup: (username: string, password: string, display_name: string) => Promise<void>;
  onBackToLogin: () => void;
}

export const Signup: React.FC<SignupProps> = ({ onSignup, onBackToLogin }) => {
  const [form, setForm] = useState({
    username: '',
    password: '',
    confirmPassword: '',
    display_name: ''
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [isLoading, setIsLoading] = useState(false);

  const validate = () => {
    const newErrors: Record<string, string> = {};

    if (!form.username.trim()) {
      newErrors.username = 'Username is required';
    } else if (form.username.length < 3) {
      newErrors.username = 'Username must be at least 3 characters';
    }

    if (!form.password) {
      newErrors.password = 'Password is required';
    } else if (form.password.length < 6) {
      newErrors.password = 'Password must be at least 6 characters';
    }

    if (form.password !== form.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    if (!form.display_name.trim()) {
      newErrors.display_name = 'Display name is required';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!validate()) return;

    setIsLoading(true);
    try {
      await onSignup(form.username, form.password, form.display_name);
    } catch (err) {
      setErrors({ submit: err instanceof Error ? err.message : 'Signup failed' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className={`min-h-screen w-full flex items-center justify-center bg-gradient-to-br ${GRADIENTS.bg1}`}>
      <div className="bg-white p-8 rounded-3xl shadow-lg w-full max-w-md border border-gray-200">
        <button
          onClick={onBackToLogin}
          className="flex items-center gap-2 text-blue-600 hover:text-blue-800 font-semibold mb-6"
        >
          <ArrowLeft size={18} /> Back to Login
        </button>

        <div className="text-center mb-8">
          <h1 className="text-4xl font-black text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-purple-600 mb-2">
            Join Arena
          </h1>
          <p className="text-gray-500 font-medium">Create your account to play</p>
        </div>

        <form onSubmit={handleSignup} className="space-y-6">
          <div className="space-y-4">
            {/* Username */}
            <div className="relative">
              <User className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 h-5 w-5" />
              <input
                type="text"
                placeholder="Username"
                value={form.username}
                onChange={(e) => {
                  setForm({...form, username: e.target.value});
                  if (errors.username) setErrors({...errors, username: ''});
                }}
                className={`w-full pl-12 pr-4 py-4 bg-white border-2 ${errors.username ? 'border-red-400' : 'border-gray-300'} focus:border-blue-400 rounded-xl outline-none transition-all font-medium text-gray-700`}
              />
              {errors.username && <p className="text-red-500 text-sm mt-1">{errors.username}</p>}
            </div>

            {/* Display Name */}
            <div className="relative">
              <User className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 h-5 w-5" />
              <input
                type="text"
                placeholder="Display Name"
                value={form.display_name}
                onChange={(e) => {
                  setForm({...form, display_name: e.target.value});
                  if (errors.display_name) setErrors({...errors, display_name: ''});
                }}
                className={`w-full pl-12 pr-4 py-4 bg-white border-2 ${errors.display_name ? 'border-red-400' : 'border-gray-300'} focus:border-blue-400 rounded-xl outline-none transition-all font-medium text-gray-700`}
              />
              {errors.display_name && <p className="text-red-500 text-sm mt-1">{errors.display_name}</p>}
            </div>

            {/* Password */}
            <div className="relative">
              <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 h-5 w-5" />
              <input
                type="password"
                placeholder="Password"
                value={form.password}
                onChange={(e) => {
                  setForm({...form, password: e.target.value});
                  if (errors.password) setErrors({...errors, password: ''});
                }}
                className={`w-full pl-12 pr-4 py-4 bg-white border-2 ${errors.password ? 'border-red-400' : 'border-gray-300'} focus:border-blue-400 rounded-xl outline-none transition-all font-medium text-gray-700`}
              />
              {errors.password && <p className="text-red-500 text-sm mt-1">{errors.password}</p>}
            </div>

            {/* Confirm Password */}
            <div className="relative">
              <Lock className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 h-5 w-5" />
              <input
                type="password"
                placeholder="Confirm Password"
                value={form.confirmPassword}
                onChange={(e) => {
                  setForm({...form, confirmPassword: e.target.value});
                  if (errors.confirmPassword) setErrors({...errors, confirmPassword: ''});
                }}
                className={`w-full pl-12 pr-4 py-4 bg-white border-2 ${errors.confirmPassword ? 'border-red-400' : 'border-gray-300'} focus:border-blue-400 rounded-xl outline-none transition-all font-medium text-gray-700`}
              />
              {errors.confirmPassword && <p className="text-red-500 text-sm mt-1">{errors.confirmPassword}</p>}
            </div>
          </div>

          {errors.submit && (
            <div className="bg-red-50 border-l-4 border-red-400 p-4 rounded">
              <p className="text-red-700 font-semibold">{errors.submit}</p>
            </div>
          )}

          <Button type="submit" className="w-full py-4 text-lg shadow-blue-300/50 shadow-lg" loading={isLoading}>
            Create Account
          </Button>
        </form>
      </div>
    </div>
  );
};

export default Signup;
