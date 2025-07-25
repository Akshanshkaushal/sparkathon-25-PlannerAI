import React from 'react';
import Button from '../ui/button';
import placeholder1 from '../../assets/placeholder1.jpg';
import placeholder2 from '../../assets/placeholder2.jpeg';
import placeholder3 from '../../assets/placeholder3.jpeg';

const CartItem = ({ item, index = 0 }) => {
  // Define array of 3 placeholder images
  const placeholderImages = [
    placeholder1,
    placeholder2, 
    placeholder3
  ];
  
  // Get image based on the item's title content
  const getImageIndex = () => {
    if (item.title) {
      if (item.title.includes('Chocolate') || item.title.includes('Cake') || item.title.includes('Literary')) {
        return 0; // First placeholder for anything with "Chocolate", "Cake" or "Literary"
      } else if (item.title.includes('Fairy') || item.title.includes('lights') || item.title.includes('lighting') || item.title.includes('vintage') || item.title.includes('Vintage') || item.title.includes('lanterns')) {
        return 2; // Second placeholder for "Fairy lights"
      } else if (item.title.includes('Book') || item.title.includes('Gift Card')) {
        return 1; // Third placeholder for "Bookstore Gift Card"
      }
    }
    
    // If no specific match, fall back to index-based assignment
    if (index !== undefined) {
      return index % placeholderImages.length;
    }
    
    // Fallback if index isn't provided
    if (item.id !== undefined) {
      return (item.id - 1) % placeholderImages.length;
    }
    
    // Final fallback
    return 0;
  };
  
  // Get the image to display
  const displayImage = placeholderImages[getImageIndex()];

  const handleViewProduct = () => {
    if (item.link && item.link !== 'https://product-link.com') {
      window.open(item.link, '_blank', 'noopener,noreferrer');
    } else {
      alert('This is a demo product. In a real application, this would link to the actual product page.');
    }
  };

  return (
    <div
      className="relative bg-white rounded-3xl overflow-hidden shadow-xl hover:shadow-2xl flex flex-col gap-2 items-center h-full transition-all duration-300 border border-gray-100 hover:border-blue-400 focus-within:border-blue-500 active:border-blue-600 group transform hover:-translate-y-1"
      tabIndex={0}
    >
      {/* Accent top bar with gradient */}
      <div className="absolute top-0 left-0 w-full h-2 bg-gradient-to-r from-blue-500 to-indigo-600"></div>
      
      {/* Badge Overlay - positioned absolutely */}
      <div className="absolute top-4 left-4 z-20">
        <span className="badge badge-new bg-white/90 backdrop-blur-sm text-blue-600 font-medium px-3 py-1.5 rounded-full text-xs shadow-md border border-blue-100">
          {item.isBestSeller ? '⭐ Best Seller' : '🔥 Recommended'}
        </span>
      </div>
      
      {/* Image Section - made larger and more prominent */}
      <div className="w-full h-48 flex items-center justify-center bg-gradient-to-br from-blue-50/70 to-indigo-50/70 mt-0 mb-2 overflow-hidden">
        <img 
          src={displayImage}
          alt={item.title} 
          className="w-full h-full object-cover transition-transform duration-500 group-hover:scale-105"
          onError={(e) => {
            e.target.style.display = 'none';
            e.target.nextSibling.style.display = 'flex';
          }}
        />
        <svg className="w-16 h-16 text-blue-200 hidden" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      </div>

      {/* Content container with padding */}
      <div className='flex flex-col justify-center items-center px-5 py-3'>
        {/* Title with improved typography */}
        <h3 className="text-xl font-bold text-slate-800 mb-2 text-center line-clamp-2 tracking-tight">
          {item.title}
        </h3>
        
        {/* Description with better spacing */}
        <p className="text-gray-500 text-sm mb-4 text-center line-clamp-2 leading-relaxed">
          {item.description || item.source || 'No description available.'}
        </p>
        
        {/* Price with enhanced styling */}
        <div className="text-blue-600 font-semibold text-lg mb-3">
          {item.price && item.price.currency}{item.price && item.price.currentPrice}
        </div>
      </div>
      
      {/* Action Buttons - improved layout and styling */}
      <div className="w-full mt-auto px-4 pb-5 pt-0 flex justify-center gap-3">
        <Button
          onClick={handleViewProduct}
          className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 rounded-lg shadow-md transition-colors text-sm flex items-center justify-center"
        >
          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
          </svg>
          View Details
        </Button>
        <button className="flex-1 bg-blue-50 hover:bg-blue-100 text-blue-600 font-medium py-2.5 rounded-lg shadow-sm transition-colors text-sm flex items-center justify-center">
          <svg className="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13l2.5 5m6-5v6a2 2 0 01-2 2H9a2 2 0 01-2-2v-6m8 0V9a2 2 0 00-2-2H9a2 2 0 00-2 2v4.01" />
          </svg>
          Add to Cart
        </button>
      </div>
    </div>
  );
};

export default CartItem;