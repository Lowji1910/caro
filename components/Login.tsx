import React, { useState } from 'react';
import { User, Lock, ArrowRight, Gamepad2 } from 'lucide-react';
import Button from './Button';
import { GRADIENTS } from '../constants';

interface LoginProps {
    onLogin: (e: React.FormEvent, form: any) => void;
    onSignupClick: () => void;
    isLoading: boolean;
}

const Login: React.FC<LoginProps> = ({ onLogin, onSignupClick, isLoading }) => {
    const [form, setForm] = useState({ username: '', password: '' });
    const [focusedField, setFocusedField] = useState<string | null>(null);

    const handleSubmit = (e: React.FormEvent) => {
        onLogin(e, form);
    };

    return (
        <div className="min-h-screen w-full flex items-center justify-center bg-[#f8fafc] relative overflow-hidden">
            {/* Animated Background Elements */}
            <div className="absolute top-0 left-0 w-full h-full overflow-hidden z-0">
                <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-blue-400/20 rounded-full blur-[100px] animate-pulse" />
                <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-purple-400/20 rounded-full blur-[100px] animate-pulse delay-1000" />
                <div className="absolute top-[40%] left-[60%] w-[30%] h-[30%] bg-pink-400/20 rounded-full blur-[100px] animate-pulse delay-2000" />
            </div>

            <div className="relative z-10 w-full max-w-5xl h-[600px] bg-white rounded-[40px] shadow-2xl overflow-hidden flex flex-col md:flex-row m-4 border border-white/50">
                {/* Left Side - Visual */}
                <div className={`hidden md:flex w-1/2 bg-gradient-to-br ${GRADIENTS.bg1} p-12 flex-col justify-between relative overflow-hidden`}>
                    <div className="absolute inset-0 bg-black/5" />
                    <div className="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/cubes.png')] opacity-10" />

                    {/* Decorative Circles */}
                    <div className="absolute top-12 right-12 w-24 h-24 bg-white/10 rounded-full blur-2xl" />
                    <div className="absolute bottom-12 left-12 w-32 h-32 bg-white/10 rounded-full blur-2xl" />

                    <div className="relative z-10">
                        <div className="w-16 h-16 bg-white/20 backdrop-blur-md rounded-2xl flex items-center justify-center mb-8 border border-white/20 shadow-lg">
                            <Gamepad2 className="text-white w-8 h-8" />
                        </div>
                        <h1 className="text-5xl font-black text-white mb-6 leading-tight">
                            Chào mừng đến<br />Ranked Arena
                        </h1>
                        <p className="text-blue-50 text-lg font-medium leading-relaxed max-w-md">
                            Trải nghiệm thế hệ game chiến thuật đối kháng mới. Thách đấu người chơi, leo rank và trở thành huyền thoại.
                        </p>
                    </div>

                    <div className="relative z-10 flex gap-4 text-sm font-medium text-blue-100">
                        <div className="px-4 py-2 bg-white/10 rounded-full backdrop-blur-sm border border-white/10">
                            Tic-Tac-Toe
                        </div>
                        <div className="px-4 py-2 bg-white/10 rounded-full backdrop-blur-sm border border-white/10">
                            Caro (Gomoku)
                        </div>
                    </div>
                </div>

                {/* Right Side - Form */}
                <div className="w-full md:w-1/2 p-8 md:p-12 flex flex-col justify-center bg-white/80 backdrop-blur-xl">
                    <div className="max-w-md mx-auto w-full">
                        <div className="mb-10">
                            <h2 className="text-3xl font-bold text-gray-800 mb-2">Đăng Nhập</h2>
                            <p className="text-gray-500">Nhập thông tin tài khoản để truy cập</p>
                        </div>

                        <form onSubmit={handleSubmit} className="space-y-6">
                            <div className="space-y-5">
                                <div className={`group relative transition-all duration-300 ${focusedField === 'username' ? 'scale-[1.02]' : ''}`}>
                                    <div className={`absolute left-4 top-1/2 -translate-y-1/2 transition-colors duration-300 ${focusedField === 'username' ? 'text-blue-500' : 'text-gray-400'}`}>
                                        <User size={20} />
                                    </div>
                                    <input
                                        type="text"
                                        placeholder="Tên đăng nhập"
                                        value={form.username}
                                        onChange={e => setForm({ ...form, username: e.target.value })}
                                        onFocus={() => setFocusedField('username')}
                                        onBlur={() => setFocusedField(null)}
                                        className={`w-full pl-12 pr-4 py-4 bg-gray-50 border-2 rounded-2xl outline-none transition-all duration-300 font-medium text-gray-700 placeholder-gray-400
                      ${focusedField === 'username' ? 'border-blue-500 bg-white shadow-lg shadow-blue-500/10' : 'border-transparent hover:bg-gray-100'}`}
                                    />
                                </div>

                                <div className={`group relative transition-all duration-300 ${focusedField === 'password' ? 'scale-[1.02]' : ''}`}>
                                    <div className={`absolute left-4 top-1/2 -translate-y-1/2 transition-colors duration-300 ${focusedField === 'password' ? 'text-blue-500' : 'text-gray-400'}`}>
                                        <Lock size={20} />
                                    </div>
                                    <input
                                        type="password"
                                        placeholder="Mật khẩu"
                                        value={form.password}
                                        onChange={e => setForm({ ...form, password: e.target.value })}
                                        onFocus={() => setFocusedField('password')}
                                        onBlur={() => setFocusedField(null)}
                                        className={`w-full pl-12 pr-4 py-4 bg-gray-50 border-2 rounded-2xl outline-none transition-all duration-300 font-medium text-gray-700 placeholder-gray-400
                      ${focusedField === 'password' ? 'border-blue-500 bg-white shadow-lg shadow-blue-500/10' : 'border-transparent hover:bg-gray-100'}`}
                                    />
                                </div>
                            </div>

                            <div className="pt-4 space-y-4">
                                <Button
                                    type="submit"
                                    className="w-full py-4 text-lg font-bold rounded-2xl shadow-xl shadow-blue-500/20 hover:shadow-blue-500/30 transition-all duration-300 hover:scale-[1.02] active:scale-[0.98]"
                                    loading={isLoading}
                                >
                                    <span className="flex items-center justify-center gap-2">
                                        Đăng Nhập <ArrowRight size={20} />
                                    </span>
                                </Button>

                                <div className="relative flex items-center gap-4 py-2">
                                    <div className="h-px bg-gray-200 flex-1" />
                                    <span className="text-gray-400 text-sm font-medium">HOẶC</span>
                                    <div className="h-px bg-gray-200 flex-1" />
                                </div>

                                <Button
                                    type="button"
                                    variant="secondary"
                                    className="w-full py-4 text-lg font-bold rounded-2xl border-2 border-gray-100 hover:border-gray-200 hover:bg-gray-50 transition-all duration-300"
                                    onClick={onSignupClick}
                                >
                                    Tạo Tài Khoản Mới
                                </Button>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Login;
