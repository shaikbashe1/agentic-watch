"use client";
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function RegisterPage() {
    const router = useRouter();
    const [company, setCompany] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);

    const handleRegister = async (e: React.FormEvent) => {
        e.preventDefault();
        setIsLoading(true);
        setError('');
        
        try {
            const res = await fetch('http://localhost:8000/auth/register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ company_name: company, email, password })
            });
            
            if (!res.ok) {
                const data = await res.json();
                throw new Error(data.detail || 'Registration failed');
            }
            
            const data = await res.json();
            localStorage.setItem('agentwatch_token', data.access_token);
            router.push('/settings/team');
        } catch (err: any) {
            setError(err.message);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="flex h-screen items-center justify-center bg-gray-50">
            <div className="w-full max-w-md p-8 bg-white rounded shadow-md">
                <h1 className="text-2xl font-bold mb-6 text-center text-blue-600">Create an Account</h1>
                {error && <div className="mb-4 p-2 bg-red-100 text-red-700 text-sm rounded">{error}</div>}
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
