import React from 'react';
import Button from '../common/Button';

const CartItem = ({ item }) => {
  const handleViewProduct = () => {
    if (item.link && item.link !== 'https://product-link.com') {
      window.open(item.link, '_blank', 'noopener,noreferrer');
    } else {
      alert('This is a demo product. In a real application, this would link to the actual product page.');
    }
  };

  // Card states: you can pass props for disabled, focused, etc. if needed
  // For now, just show normal/hover/active

  return (
    <div
      className="relative bg-white rounded-2xl shadow-lg flex flex-col items-center h-full transition-all duration-200 border-2 border-transparent hover:border-blue-400 focus-within:border-blue-500 active:border-blue-600 group"
      tabIndex={0}
    >
      {/* Blue Header */}
      <div className="w-full h-16 rounded-t-2xl bg-[#0071dc] flex items-center justify-between px-4 mb-[-32px] z-10">
        {/* Label/Badge */}
        <span className="badge badge-new bg-white/80 text-[#0071dc] font-bold px-3 py-1 rounded-full text-xs shadow-md">
          {item.isBestSeller ? 'Best Seller' : 'Recommended'}
        </span>
        {/* Optionally, add more icons or actions here */}
      </div>
      {/* Image Section */}
      <div className="w-full h-36 flex items-center justify-center rounded-xl mb-4 bg-gradient-to-br from-blue-50 to-indigo-100 mt-[-32px] z-0">
        {item.image ? (
          <img 
            src={item.image} 
            alt={item.title} 
            className="w-24 h-24 object-contain rounded-xl drop-shadow-md"
            onError={(e) => {
              e.target.style.display = 'none';
              e.target.nextSibling.style.display = 'flex';
            }}
          />
        ) : (
          <svg className="w-16 h-16 text-blue-200" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
          </svg>
        )}
      </div>
      {/* Title */}
      <h3 className="text-lg font-bold text-slate-800 mb-1 text-center line-clamp-2">
        {item.title}
      </h3>
      {/* Description */}
      <p className="text-gray-500 text-sm mb-4 text-center line-clamp-2">
        {item.description || item.source || 'No description available.'}
      </p>
      {/* Price */}
      <div className="text-[#0071dc] font-semibold text-base mb-4">
        {item.price && item.price.currency}{item.price && item.price.currentPrice}
      </div>
      {/* Action Buttons */}
      <div className="w-full space-y-2">
        <Button
          onClick={handleViewProduct}
          className="w-full text-sm py-2"
        >
          <svg className="w-4 h-4 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
          </svg>
          View Product
        </Button>
        <button className="w-full bg-blue-100 hover:bg-blue-200 text-[#0071dc] font-semibold py-2 rounded-lg shadow transition text-sm">
          <svg className="w-4 h-4 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13l2.5 5m6-5v6a2 2 0 01-2 2H9a2 2 0 01-2-2v-6m8 0V9a2 2 0 00-2-2H9a2 2 0 00-2 2v4.01" />
          </svg>
          Add to Cart
        </button>
      </div>
    </div>
  );
};

export default CartItem;