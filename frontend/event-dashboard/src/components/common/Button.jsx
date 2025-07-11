import React from 'react';

const Button = ({ children, onClick, className = '', type = 'button' }) => {
  return (
    <button
      type={type}
      onClick={onClick}
      className={`bg-highlight text-text-primary font-bold py-2 px-4 rounded-lg hover:bg-accent transition duration-300 ease-in-out ${className}`}
    >
      {children}
    </button>
  );
};

export default Button;