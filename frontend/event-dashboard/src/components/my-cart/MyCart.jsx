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
        <div className="w-full max-w-6xl mt-16 mb-8">
          <h2 className="text-4xl text-slate-700 font-medium mb-12 text-left tracking-tight">Event Details & Budget</h2>
          <div className="flex flex-col gap-10">
            {/* Event Items Box */}
            <div className="bg-white rounded-3xl shadow-2xl border-2 border-[#0071dc] pl-10 md:p-16 flex flex-col  overflow-hidden mb-8">
              
              <h3 className="text-3xl font-bold text-[#0071dc] mb-4 flex items-center gap-2 border-b border-blue-100 pb-2">
                <span role="img" aria-label="gift">🎁</span> Event Items
              </h3>
              {plan ? (
                <div className=" text-slate-800 text-xl">
                  <div><span className="font-bold">Theme:</span> {plan.decoration_theme}</div>
                  {plan.cake_suggestion && (
                    <div><span className="font-bold">Cake:</span> {plan.cake_suggestion.type}</div>
                  )}
                  {plan.decoration_items?.length > 0 && (
                    <div>
                      <span className="font-bold">Decor:</span>
                      <ul className="list-disc list-inside ml-4 mt-1 text-xl">
                        {plan.decoration_items.map((item, idx) => (
                          <li key={idx}>{item}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  {plan.gift_suggestions && (
                    <div>
                      <span className="font-bold">Gifts:</span>
                      <ul className="list-disc list-inside text-xl ml-4 mt-1">
                        {extractGiftNames(plan.gift_suggestions).map((gift, idx) => (
                          <li key={idx}>{gift}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ) : (
                <p className="text-slate-400">No event items found.</p>
              )}
            </div>
            {/* Budget Box */}
            <div className="bg-white rounded-2xl shadow-lg border-4 border-[#0071dc] p-10 md:p-12 flex flex-col min-h-[400px]">
              <h3 className="text-4xl font-bold text-[#0071dc] mb-6 flex items-center gap-2">
                <span role="img" aria-label="budget">💸</span> Budget
              </h3>
              {budget ? (
                <ul className="space-y-5 text-slate-800 text-base flex-1 overflow-auto">
                  {Object.entries(budget).map(([category, b], idx) => (
                    <li key={idx} className="flex gap-6 justify-between border-b border-gray-200 pb-2">
                      <span className="capitalize text-lg font-semibold">{category}:</span>
                      <span className="text-emerald-600 font-bold">${b.min_budget} - ${b.max_budget}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-slate-400">No budget info available.</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default MyCart;