import React from 'react';

const Input = ({ label, name, value, onChange, placeholder = '', type = 'text' }) => {
  return (
    <div>
      <label htmlFor={name} className="block text-sm font-medium text-text-secondary">
        {label}
      </label>
      <input
        type={type}
        name={name}
        id={name}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        className="mt-1 block w-full bg-accent border border-gray-600 rounded-md shadow-sm py-2 px-3 text-text-primary focus:outline-none focus:ring-highlight focus:border-highlight"
      />
    </div>
  );
};

export default Input;