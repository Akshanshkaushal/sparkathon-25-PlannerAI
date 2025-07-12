import React from 'react';

const Button = ({ children, onClick, className = '', type = 'button', disabled = false }) => {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`bg-[#0071dc] hover:bg-blue-800 text-white font-semibold rounded-xl shadow-lg px-6 py-3 text-lg transition-all duration-200 border border-[#0071dc] focus:outline-none focus:ring-2 focus:ring-blue-300 disabled:opacity-50 disabled:cursor-not-allowed ${className}`}
    >
      {children}
    </button>
  );
};

export default Button;