import React, { useEffect, useState } from 'react';
import CartItem from './CartItem';
import { LoaderFour } from '../ui/loader';


const MyCart = ({ cartData }) => {
  if (!cartData) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <LoaderFour />
      </div>
    );
  }
  if (!cartData.cart) {
    return (
      <div className="text-center py-12">
        <p className="text-slate-500 text-lg">No cart data available. Please generate a plan from the dashboard.</p>
      </div>
    );
  }

  const { cart, plan, budget } = cartData;
  // Flatten all cart items into a single array
  const allCartItems = Object.values(cart || {}).flat();
  // Helper function to extract gift names properly
  const extractGiftNames = (giftSuggestions) => {
    if (!giftSuggestions) return [];
    const allGifts = [];
    Object.values(giftSuggestions).forEach(giftArray => {
      if (Array.isArray(giftArray)) {
        giftArray.forEach(gift => {
          if (typeof gift === 'string') {
            allGifts.push(gift);
          } else if (gift && gift.title) {
            allGifts.push(gift.title);
          } else if (gift && gift.name) {
            allGifts.push(gift.name);
          }
        });
      }
    });
    return allGifts;
  };

  return (
    <div className='flex justify-center py-5'>
      <div className="min-h-screen layout-content-container gap-12 flex flex-col max-w-7xl flex-1 w-full mt-32 px-8 md:px-20">
        {/* Cart Section */}
        <div className='flex flex-col gap-4'>
          <div className='flex flex-wrap justify-between'>
            <h1 className="text-5xl font-medium mt-24 text-slate-700 tracking-tight drop-shadow-lg">Your Cart</h1>
          </div>
          <div className="w-full flex mb-10">
            <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-10 items-center">
              {allCartItems.length > 0 ? (
                allCartItems.map((item, index) => (
                  <div key={index} className="w-[360px] h-[360px]">
                    <CartItem item={item} />
                  </div>
                ))
              ) : (
                <div className="col-span-full text-center text-slate-400 py-12">No products found in your cart.</div>
              )}
            </div>
          </div>
        </div>

        {/* Event Details & Budget Section */}
       
       

      </div>
    </div>
  );
}

export default MyCart;