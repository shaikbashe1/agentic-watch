"use client";
import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface User {
    id: string;
    email: string;
    role: string;
    created_at: string;
}

export default function TeamPage() {
    const router = useRouter();
    const [team, setTeam] = useState<User[]>([]);
    const [email, setEmail] = useState('');
    const [role, setRole] = useState('Viewer');
    const [error, setError] = useState('');
    const [success, setSuccess] = useState('');

    useEffect(() => {
        fetchTeam();
    }, []);

    const fetchTeam = async () => {
        const token = localStorage.getItem('agentwatch_token');
        if (!token) {
            router.push('/login');
            return;
        }

        try {
            const res = await fetch('http://localhost:8000/team', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (res.ok) {
                const data = await res.json();
                setTeam(data);
            }
        } catch (err) {
            console.error("Failed to fetch team", err);
        }
    };

    const handleInvite = async (e: React.FormEvent) => {
        e.preventDefault();
        setError('');
        setSuccess('');
        const token = localStorage.getItem('agentwatch_token');

        try {
            const res = await fetch('http://localhost:8000/team/invite', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ email, role })
            });
            
            if (!res.ok) {
                const data = await res.json();
                throw new Error(data.detail || 'Failed to invite user');
            }
            
            setSuccess(`Successfully invited ${email} as ${role}`);
            setEmail('');
            fetchTeam();
        } catch (err: any) {
            setError(err.message);
        }
    };

    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-4">Team Management</h1>
            <p className="mb-6 text-gray-600">Invite colleagues to your workspace and manage their access permissions.</p>
            
            <div className="bg-white p-6 rounded shadow mb-8 max-w-2xl">
                <h2 className="text-xl font-bold mb-4">Invite New Member</h2>
                {error && <div className="mb-4 p-2 bg-red-100 text-red-700 text-sm rounded">{error}</div>}
                {success && <div className="mb-4 p-2 bg-green-100 text-green-700 text-sm rounded">{success}</div>}
                
                <form onSubmit={handleInvite} className="flex gap-4 items-end">
                    <div className="flex-1">
                        <label className="block text-sm font-medium mb-1">Email Address</label>
                        <input type="email" value={email} onChange={e => setEmail(e.target.value)} className="w-full p-2 border rounded" required />
                    </div>
                    <div className="w-48">
                        <label className="block text-sm font-medium mb-1">Role</label>
                        <select value={role} onChange={e => setRole(e.target.value)} className="w-full p-2 border rounded">
                            <option>Admin</option>
                            <option>Developer</option>
                            <option>Viewer</option>
                        </select>
                    </div>
                    <button type="submit" className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700 h-10">Send Invite</button>
                </form>
            </div>

            <div className="bg-white rounded shadow">
                <table className="w-full text-left border-collapse">
                    <thead>
                        <tr className="bg-gray-50 border-b">
                            <th className="p-4 font-medium text-gray-600">Email</th>
                            <th className="p-4 font-medium text-gray-600">Role</th>
                            <th className="p-4 font-medium text-gray-600">Joined Date</th>
                        </tr>
                    </thead>
                    <tbody>
                        {team.map(member => (
                            <tr key={member.id} className="border-b last:border-0 hover:bg-gray-50">
                                <td className="p-4">{member.email}</td>
                                <td className="p-4">
                                    <span className={`px-2 py-1 rounded text-xs font-bold ${
                                        member.role === 'Owner' ? 'bg-purple-100 text-purple-800' :
                                        member.role === 'Admin' ? 'bg-red-100 text-red-800' :
                                        member.role === 'Developer' ? 'bg-blue-100 text-blue-800' :
                                        'bg-gray-100 text-gray-800'
                                    }`}>
                                        {member.role}
                                    </span>
                                </td>
                                <td className="p-4 text-sm text-gray-500">{new Date(member.created_at).toLocaleDateString()}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
                {team.length === 0 && <div className="p-8 text-center text-gray-500">No team members found.</div>}
            </div>
        </div>
    );
}
