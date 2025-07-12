import React from 'react';
import CartItem from './CartItem';

const MyCart = ({ cartData }) => {
  if (!cartData || !cartData.cart) {
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
    <div className="min-h-screen bg-[#f8fafc] flex flex-col items-center pt-40 pb-16">
      <div className="sticky top-0 z-40 w-full bg-[#f8fafc] pb-6">
        <h1 className="text-5xl font-extrabold text-blue-700 tracking-tight drop-shadow-lg text-center">Your Cart</h1>
      </div>
      
      {/* Cart Cards Section */}
      <div className="w-full flex justify-center mb-10">
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-10 justify-items-center">
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
      {/* Event Details Section - Full Width */}
      <div className="w-full max-w-6xl px-4 mt-10">
        <h2 className="text-4xl font-extrabold text-blue-700 mb-8 text-center tracking-tight">Event Details & Budget</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
          {/* Event Items Box */}
          <div className="bg-white rounded-2xl shadow-lg border-4 border-[#0071dc] p-10 flex flex-col h-[360px]">
            <h3 className="text-2xl font-bold text-[#0071dc] mb-6 flex items-center gap-2">
              <span role="img" aria-label="gift">🎁</span> Event Items
            </h3>
            {plan ? (
              <div className="space-y-5 text-slate-800 text-base flex-1 overflow-auto">
                <div><span className="font-bold text-[#0071dc]">Theme:</span> {plan.decoration_theme}</div>
                {plan.cake_suggestion && (
                  <div><span className="font-bold text-[#0071dc]">Cake:</span> {plan.cake_suggestion.type}</div>
                )}
                {plan.decoration_items?.length > 0 && (
                  <div>
                    <span className="font-bold text-[#0071dc]">Decor:</span>
                    <ul className="list-disc list-inside ml-4 mt-1 text-base">
                      {plan.decoration_items.map((item, idx) => (
                        <li key={idx}>{item}</li>
                      ))}
                    </ul>
                  </div>
                )}
                {plan.gift_suggestions && (
                  <div>
                    <span className="font-bold text-[#0071dc]">Gifts:</span>
                    <ul className="list-disc list-inside ml-4 mt-1 text-base">
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
          <div className="bg-white rounded-2xl shadow-lg border-4 border-[#0071dc] p-10 flex flex-col h-[360px]">
            <h3 className="text-2xl font-bold text-[#0071dc] mb-6 flex items-center gap-2">
              <span role="img" aria-label="budget">💸</span> Budget
            </h3>
            {budget ? (
              <ul className="space-y-5 text-slate-800 text-base flex-1 overflow-auto">
                {Object.entries(budget).map(([category, b], idx) => (
                  <li key={idx} className="flex justify-between border-b border-gray-200 pb-2">
                    <span className="capitalize font-semibold">{category}:</span>
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
  );
};

export default MyCart;