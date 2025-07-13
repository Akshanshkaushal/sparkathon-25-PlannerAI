// src/pages/DashboardPage.jsx

import React, { useState } from 'react';
import SpotlightCard from '../components/ui/SpotlightCard';
import UserForm from '../components/dashboard/UserForm';
import Sidebar from "../components/layout/Sidebar";
import { BackgroundBeamsWithCollision } from '../components/ui/background-beams-with-collision';
import { TypewriterEffect } from '../components/ui/typewriter-effect';
import { TextLoop } from "@/components/ui/text-loop";

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
    
      <div className="relative max-w-8xl w-full flex flex-col  items-center min-h-screen py-24 px-2 justify-center">
        <BackgroundBeamsWithCollision className="absolute w-full h-full left-0 top-0 z-0" />
        <div className="relative z-10 w-full flex flex-col gap-7 items-center">
          {/* Main Content (no box) */}
          
          <TypewriterEffect
            words={[
              { text: "Create Your Perfect Event" },
            ]}
            className="text-blue-600"
            cursorClassName=""
          />
          <p className="text-slate-700 text-lg sm:text-xl text-center  font-sans font-medium max-w-2xl mx-auto">
            Let our AI create a personalized shopping plan for your special occasion.
          </p>
          
          <span className='text-slate-700 text-lg sm:text-xl text-center mb-12 font-sans font-medium max-w-2xl mx-auto'>We'll suggest <TextLoop interval={2} className="text-blue-600 text-lg sm:text-xl font-bold">
            <span>decorations</span>
            <span>gifts</span>
            <span>everything you need</span>
          </TextLoop> to make it memorable.</span>
          {/* Form */}
          <div className="w-full max-w-3xl mb-16">
            <UserForm />
          </div>
          {/* Divider */}
          <div className="border-t border-gray-300 mt-16 mb-16 w-full max-w-5xl" />
          {/* Feature Cards */}
          <div className="flex max-w-6xl gap-12 items-center justify-center">
            {featureCards.map((item, index) => (
              <SpotlightCard className="custom-spotlight-card justify-center items-center min-h-[340px] md:min-h-64 flex" spotlightColor="rgba(0, 229, 255, 0.2)">
                <div className='items-center justify-center flex flex-col flex-1 h-full'>
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
                  <p className="text-lg text-gray-600 text-center font-sans font-medium">{item.desc}</p>
                </div>
              </SpotlightCard>
            ))}
          </div>
        </div>
      </div>
    
  );
};

export default DashboardPage;
