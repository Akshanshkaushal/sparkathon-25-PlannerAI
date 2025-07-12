// src/pages/DashboardPage.jsx

import React, { useState } from 'react';
import UserForm from '../components/dashboard/UserForm';
import Sidebar from "../components/layout/Sidebar";

function MainLayout({ children }) {
  const [eventName, setEventName] = useState('');
  const [plan, setPlan] = useState(null);
  const [budget, setBudget] = useState(null);

  // Pass these setters to child components (like DashboardPage) so they can update the sidebar
  return (
    <div className="flex">
      <Sidebar eventName={eventName} plan={plan} budget={budget} />
      <main className="flex-1">{React.cloneElement(children, { setEventName, setPlan, setBudget })}</main>
    </div>
  );
}

const featureCards = [
  {
    bg: "bg-blue-100",
    iconColor: "text-[#0071dc]",
    title: "Smart Planning",
    desc: "AI analyzes your preferences to create the perfect event plan"
  },
  {
    bg: "bg-gray-100",
    iconColor: "text-slate-500",
    title: "Curated Products",
    desc: "Hand-picked items that match your style and budget"
  },
  {
    bg: "bg-green-100",
    iconColor: "text-green-600",
    title: "Budget Friendly",
    desc: "Stay within your budget with smart price recommendations"
  }
];

const DashboardPage = () => {
  return (
    <div className="min-h-screen w-full flex flex-col items-center justify-center bg-blue-50 py-24 px-2">
      <div className="relative max-w-7xl w-full flex flex-col items-center">
        {/* Main Content (no box) */}
        <h1 className="text-3xl sm:text-4xl font-bold text-[#0071dc] mb-8 text-center font-display tracking-tight mt-24">
          Create Your Perfect Event
        </h1>
        <p className="text-slate-700 text-lg sm:text-xl text-center mb-12 font-sans font-medium max-w-2xl mx-auto">
          Let our AI create a personalized shopping plan for your special occasion. We'll suggest decorations, gifts, and everything you need to make it memorable.
        </p>
        {/* Form */}
        <div className="w-full max-w-3xl mb-16">
          <UserForm />
        </div>
        {/* Divider */}
        <div className="border-t border-gray-300 mt-16 mb-16 w-full max-w-5xl" />
        {/* Feature Cards */}
        <div className="grid grid-cols-1 sm:grid-cols-3 gap-16 w-full max-w-6xl mt-12">
          {featureCards.map((item, index) => (
            <div
              key={index}
              className="bg-white rounded-2xl shadow-lg p-12 text-center flex flex-col items-center hover:shadow-2xl transition"
            >
              <div className={`w-14 h-14 flex items-center justify-center ${item.bg} rounded-full mb-4`}>
                <svg className={`w-7 h-7 ${item.iconColor}`} fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 4v1m0 14v1m8-9h1M3 12H2m16.95-4.95l.707.707M5.05 5.05l-.707-.707M18.364 18.364l.707.707M5.636 18.364l-.707.707"
                  />
                </svg>
              </div>
              <h3 className="font-bold text-2xl text-slate-800 mb-3 font-display tracking-tight">{item.title}</h3>
              <p className="text-lg text-gray-600 font-sans font-medium">{item.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
