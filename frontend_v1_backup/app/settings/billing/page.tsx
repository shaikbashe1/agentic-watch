"use client";
import React, { useState } from 'react';

export default function BillingPage() {
    return (
        <div className="p-6">
            <h1 className="text-2xl font-bold mb-4">Billing & Plans</h1>
            <p className="mb-6 text-gray-600">Manage your subscription and view your current platform usage.</p>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                {/* Free Plan */}
                <div className="bg-white border-2 border-transparent p-6 rounded shadow-sm hover:border-blue-500">
                    <h2 className="text-xl font-bold mb-2">Free Tier</h2>
                    <p className="text-gray-500 mb-4">$0 / month</p>
                    <ul className="text-sm space-y-2 mb-6">
                        <li>✅ Up to 2 Agents</li>
                        <li>✅ 10k Events / month</li>
                        <li>✅ 7-day log retention</li>
                    </ul>
                    <button className="w-full py-2 bg-gray-200 text-gray-800 rounded font-medium" disabled>Current Plan</button>
                </div>
                
                {/* Pro Plan */}
                <div className="bg-white border-2 border-blue-500 p-6 rounded shadow-md relative">
                    <div className="absolute top-0 right-0 bg-blue-500 text-white text-xs px-2 py-1 rounded-bl">RECOMMENDED</div>
                    <h2 className="text-xl font-bold mb-2">Pro Tier</h2>
                    <p className="text-gray-500 mb-4">$49 / month</p>
                    <ul className="text-sm space-y-2 mb-6">
                        <li>✅ Up to 20 Agents</li>
                        <li>✅ 1M Events / month</li>
                        <li>✅ 90-day log retention</li>
                        <li>✅ Custom Policies</li>
                    </ul>
                    <button className="w-full py-2 bg-blue-600 text-white rounded font-medium hover:bg-blue-700">Upgrade to Pro</button>
                </div>
                
                {/* Enterprise Plan */}
                <div className="bg-white border-2 border-transparent p-6 rounded shadow-sm hover:border-gray-500">
                    <h2 className="text-xl font-bold mb-2">Enterprise</h2>
                    <p className="text-gray-500 mb-4">Custom Pricing</p>
                    <ul className="text-sm space-y-2 mb-6">
                        <li>✅ Unlimited Agents</li>
                        <li>✅ Unlimited Events</li>
                        <li>✅ Infinite retention</li>
                        <li>✅ Dedicated Support</li>
                        <li>✅ SSO & SAML</li>
                    </ul>
                    <button className="w-full py-2 bg-gray-800 text-white rounded font-medium hover:bg-gray-900">Contact Sales</button>
                </div>
            </div>
            
            <div className="bg-white p-6 rounded shadow">
                <h2 className="text-xl font-bold mb-4">Current Usage</h2>
                <div className="space-y-4">
                    <div>
                        <div className="flex justify-between mb-1 text-sm">
                            <span>Events Ingested</span>
                            <span className="font-medium text-gray-700">4,521 / 10,000</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                            <div className="bg-blue-600 h-2 rounded-full" style={{ width: '45%' }}></div>
                        </div>
                    </div>
                    <div>
                        <div className="flex justify-between mb-1 text-sm">
                            <span>Active Agents</span>
                            <span className="font-medium text-gray-700">2 / 2</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                            <div className="bg-red-500 h-2 rounded-full" style={{ width: '100%' }}></div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
