import React from 'react';
import { NavLink } from 'react-router-dom';

const Sidebar = ({ eventName, plan, budget }) => {
  return (
    <aside className="w-64 min-h-screen bg-white border-r border-gray-200 text-slate-800 flex flex-col py-12 px-7 space-y-12 shadow-lg font-['Inter','Poppins','Roboto','Montserrat',sans-serif]">
      <div className="mb-12 flex items-center space-x-4 px-2">
        <div className="w-11 h-11 bg-[#0071dc] rounded-2xl flex items-center justify-center shadow-xl">
          <svg className="w-7 h-7 text-white drop-shadow-lg" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
          </svg>
        </div>
        <span className="text-3xl font-black tracking-wide text-[#0071dc] font-['Montserrat','Inter','Poppins','Roboto',sans-serif]">Planner AI</span>
      </div>
      <nav className="flex-1">
        <ul className="space-y-4">
          <li>
            <NavLink 
              to="/" 
              className={({ isActive }) =>
                `flex items-center space-x-4 px-6 py-3 rounded-2xl font-semibold transition-all duration-200 text-lg tracking-wide ${
                  isActive
                    ? 'bg-[#0071dc] text-white shadow-lg'
                    : 'hover:bg-blue-50 hover:text-[#0071dc] text-slate-700'
                }`
              }
            >
              <svg className="w-5 h-5 text-[#0071dc]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
              </svg>
              <span>Create Event</span>
            </NavLink>
          </li>
          <li>
            <NavLink 
              to="/my-cart" 
              className={({ isActive }) =>
                `flex items-center space-x-4 px-6 py-3 rounded-2xl font-semibold transition-all duration-200 text-lg tracking-wide ${
                  isActive
                    ? 'bg-[#0071dc] text-white shadow-lg'
                    : 'hover:bg-blue-50 hover:text-[#0071dc] text-slate-700'
                }`
              }
            >
              <svg className="w-5 h-5 text-[#0071dc]" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13l2.5 5m6-5v6a2 2 0 01-2 2H9a2 2 0 01-2-2v-6m8 0V9a2 2 0 00-2-2H9a2 2 0 00-2 2v4.01" />
              </svg>
              <span>My Cart</span>
            </NavLink>
          </li>
        </ul>
      </nav>
      {/* Event Info Section */}
      {(eventName || plan || budget) && (
        <>
          <div className="text-lg font-bold text-[#0071dc] mb-2 mt-2">Event Details</div>
          <div className="mb-8 p-4 bg-blue-50 rounded-2xl shadow-inner border border-gray-200">
            {eventName && (
              <div className="mb-3">
                <div className="text-xs text-slate-400 mb-1">Current Event</div>
                <div className="text-lg font-bold text-blue-700 truncate">{eventName}</div>
              </div>
            )}
            {plan && (
              <div className="mb-3">
                <div className="text-xs text-slate-400 mb-1">Theme</div>
                <div className="text-base font-semibold text-blue-700">{plan.decoration_theme}</div>
                {plan.cake_suggestion && (
                  <div className="mt-2">
                    <div className="text-xs text-slate-400">Cake</div>
                    <div className="text-sm text-slate-700">{plan.cake_suggestion.type}</div>
                  </div>
                )}
                {plan.decoration_items && plan.decoration_items.length > 0 && (
                  <div className="mt-2">
                    <div className="text-xs text-slate-400">Decor</div>
                    <ul className="text-sm text-slate-700 list-disc ml-4">
                      {plan.decoration_items.slice(0, 2).map((item, idx) => (
                        <li key={idx}>{item}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
            {budget && (
              <div>
                <div className="text-xs text-slate-400 mb-1">Budget</div>
                <ul className="text-sm text-emerald-600">
                  {Object.entries(budget).map(([cat, b], idx) => (
                    <li key={idx} className="flex justify-between">
                      <span className="capitalize">{cat}:</span>
                      <span>${b.min_budget} - ${b.max_budget}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </>
      )}
      <div className="mt-auto pt-12 border-t border-gray-200">
        <div className="flex items-center space-x-3 mb-2">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
          <span className="text-sm font-semibold text-slate-700">AI Status</span>
        </div>
        <p className="text-xs text-slate-400 font-['Inter','Poppins','Roboto','Montserrat',sans-serif]">Powered by advanced AI for personalized event planning</p>
      </div>
    </aside>
  );
};

export default Sidebar;