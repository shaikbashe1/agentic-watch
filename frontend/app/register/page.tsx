"use client";
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function RegisterPage() {
    const router = useRouter();
    const [company, setCompany] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const handleRegister = (e: React.FormEvent) => {
        e.preventDefault();
        // In a real app, call API to register company and user
        localStorage.setItem('agentwatch_token', 'dummy-jwt-token');
        router.push('/settings/api-keys');
    };

    return (
        <div className="flex h-screen items-center justify-center bg-gray-50">
            <div className="w-full max-w-md p-8 bg-white rounded shadow-md">
                <h1 className="text-2xl font-bold mb-6 text-center text-blue-600">Create an Account</h1>
                <form onSubmit={handleRegister} className="space-y-4">
                    <div>
                        <label className="block text-sm font-medium mb-1">Company / Workspace Name</label>
                        <input type="text" value={company} onChange={e => setCompany(e.target.value)} className="w-full p-2 border rounded" required />
                    </div>
                    <div>
                        <label className="block text-sm font-medium mb-1">Email</label>
                        <input type="email" value={email} onChange={e => setEmail(e.target.value)} className="w-full p-2 border rounded" required />
                    </div>
                    <div>
                        <label className="block text-sm font-medium mb-1">Password</label>
                        <input type="password" value={password} onChange={e => setPassword(e.target.value)} className="w-full p-2 border rounded" required />
                    </div>
                    <button type="submit" className="w-full py-2 bg-green-600 text-white rounded hover:bg-green-700">Register</button>
                </form>
                <div className="mt-4 text-center text-sm">
                    Already have an account? <a href="/login" className="text-blue-600 hover:underline">Login</a>
                </div>
            </div>
        </div>
    );
}
