import React from 'react';

const Header = () => {
  return (
    <header className="w-full bg-white border-b border-gray-200 py-4 px-6 flex items-center justify-between shadow-md fixed top-0 left-0 right-0 z-50">
      <div className="flex items-center space-x-4">
        <div className="w-8 h-8 bg-[#0071dc] rounded-2xl flex items-center justify-center shadow-xl">
          <svg className="w-5 h-5 text-white drop-shadow-lg" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 7l-8-4-8 4m16 0l-8 4m8-4v10l-8 4m0-10L4 7m8 4v10M4 7v10l8 4" />
          </svg>
        </div>
        <div>
          <h1 className="text-xl font-bold text-[#0071dc] font-['Inter','Poppins','Roboto',sans-serif]">Event Planner AI</h1>
          <p className="text-xs text-slate-500 font-['Inter','Poppins','Roboto',sans-serif]">Smart Shopping & Planning</p>
        </div>
      </div>
      <div className="flex items-center space-x-4">
        <button className="flex items-center bg-[#0071dc] hover:bg-blue-800 text-white font-semibold px-6 py-3 rounded-xl shadow-lg text-lg transition-all duration-200 border border-[#0071dc] focus:outline-none focus:ring-2 focus:ring-blue-300">
          <svg className="w-6 h-6 mr-2 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <rect x="3" y="8" width="18" height="13" rx="2" strokeWidth="2" stroke="currentColor" fill="none" />
            <path d="M16 2v4M8 2v4M3 10h18" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
          Connect to Calendar
        </button>
      </div>
    </header>
  );
};

export default Header;