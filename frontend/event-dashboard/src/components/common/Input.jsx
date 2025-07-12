// src/components/common/Input.jsx

import React from 'react';

const Input = ({ label, name, value, onChange, placeholder, type = "text", required = false, className = "" }) => {
  return (
    <div className={`flex flex-col ${className}`}>
      <label htmlFor={name} className="text-xl font-semibold text-gray-800 mb-2">
        {label}
        {required && <span className="text-red-500"> *</span>}
      </label>
      <input
        id={name}
        name={name}
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        className="py-5 px-6 text-lg rounded-xl border-2 border-indigo-300 shadow focus:ring-2 focus:ring-indigo-400 focus:outline-none text-gray-700 placeholder-gray-400 bg-white transition duration-150 ease-in-out"
      />
    </div>
  );
};

export default Input;
