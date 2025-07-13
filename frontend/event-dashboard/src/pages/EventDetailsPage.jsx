import React from 'react';

const dummyData = {
  budget: {
    cake: { max_budget: 100, min_budget: 30 },
    decorations: { max_budget: 150, min_budget: 50 },
    gifts: { max_budget: 200, min_budget: 100 }
  },
  cart: {
    cake: [
      {
        isBestSeller: true,
        link: "https://product-link.com",
        price: { currency: "$", currentPrice: "100.00" },
        reviewsCount: "200",
        source: "Existing Products",
        title: "Chocolate Molten Lava Cake"
      }
    ],
    decorations: [
      {
        isBestSeller: false,
        link: "https://product-link.com",
        price: { currency: "$", currentPrice: "30.00" },
        reviewsCount: "N/A",
        source: "Created Suggestion",
        title: "Decorative Quote Banners"
      }
    ],
    gifts: [
      {
        isBestSeller: true,
        link: "https://www.amazon.com/dp/B08N36XNTT",
        price: { currency: "$", currentPrice: "139.99" },
        reviewsCount: "20000",
        source: "Existing Products",
        title: "E-Reader (e.g., Kindle Paperwhite)"
      }
    ]
  },
  plan: {
    cake_suggestion: {
      size: "Two-tiered cake, serving approximately 12-15 people",
      type: "Chocolate Molten Lava Cake"
    },
    decoration_items: [
      "Bookshelves with fairy lights",
      "Gadget-themed centerpieces (like mini robots or tech gadgets)",
      "Vintage book pages as table runners",
      "Balloon bouquets in colors of book covers (e.g., blue, gold, red)",
      "Quote banners featuring famous literary quotes and tech phrases"
    ],
    decoration_theme: "Literary Tech Wonderland",
    gift_suggestions: {
      inspired_by_gifts: [
        {
          description: "A lamp that adjusts brightness based on the time of day and can sync with reading apps, enhancing the reading experience.",
          name: "Interactive Reading Lamp"
        },
        {
          description: "A stylish bag designed to organize and store gadgets and accessories, which would appeal to anyone who loves tech and gadgets.",
          name: "Gadget Organizer Bag"
        }
      ],
      specific_gifts: [
        {
          description: "A portable e-reader that allows Akshansh Kaushal to carry thousands of books in one device, perfect for a book lover.",
          name: "E-Reader (e.g., Kindle Paperwhite)"
        },
        {
          description: "A voice-activated smart speaker that not only plays music but can read audiobooks and provide information, merging gadgets with books.",
          name: "Smart Speaker (e.g., Amazon Echo)"
        },
        {
          description: "A gift card to a favorite local or online bookstore, allowing Akshansh Kaushal to choose books that pique their interest.",
          name: "Bookstore Gift Card"
        }
      ]
    }
  }
};

const EventDetailsPage = () => {
  const { plan, budget, cart } = dummyData;

  return (
    <div className="min-h-screen bg-gradient-to-br from-[#f8fafc] to-[#e0f2fe] flex flex-col items-center pt-24 pb-12">
      <div className="flex-grow w-full flex items-center justify-center">
        <div className="flex flex-col md:flex-row w-full max-w-7xl gap-8 md:gap-10 mt-8 md:mt-12">
          {/* Event Items Box */}
          <div className="bg-white rounded-3xl shadow-2xl border-2 border-[#0071dc] p-6 md:p-10 flex flex-col min-h-[420px] max-h-[600px] overflow-hidden">
            <h2 className="text-2xl font-bold text-[#0071dc] mb-4 md:mb-6 flex items-center gap-2">
              <span role="img" aria-label="gift">🎁</span> Event Items
            </h2>
            <div className="flex-1 overflow-y-auto space-y-6 pr-2">
              {plan ? (
                <div className="space-y-5 text-slate-800 text-base">
                  <div><span className="font-bold text-[#0071dc]">Theme:</span> {plan.decoration_theme}</div>
                  {plan.cake_suggestion && (
                    <div><span className="font-bold text-[#0071dc]">Cake:</span> {plan.cake_suggestion.type} <span className="text-gray-500">({plan.cake_suggestion.size})</span></div>
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
                        {plan.gift_suggestions.specific_gifts.map((gift, idx) => (
                          <li key={idx}><span className="font-semibold">{gift.name}</span>: <span className="text-gray-500">{gift.description}</span></li>
                        ))}
                        {plan.gift_suggestions.inspired_by_gifts.map((gift, idx) => (
                          <li key={idx}><span className="font-semibold">{gift.name}</span>: <span className="text-gray-500">{gift.description}</span></li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ) : (
                <p className="text-gray-500">No event items found.</p>
              )}
              {/* Cart Items */}
              <div>
                <span className="font-bold text-[#0071dc]">Products:</span>
                <div className="mt-2 space-y-3">
                  {Object.entries(cart).map(([category, items]) => (
                    <div key={category} className="mb-2">
                      <span className="font-semibold capitalize text-[#0071dc]">{category}:</span>
                      <ul className="ml-4 mt-1">
                        {items.map((item, idx) => (
                          <li key={idx} className="mb-2 flex flex-col md:flex-row md:items-center md:gap-2">
                            <a href={item.link} target="_blank" rel="noopener noreferrer" className="text-blue-600 underline font-medium">{item.title}</a>
                            <span className="ml-0 md:ml-2 text-gray-700">{item.price.currency}{item.price.currentPrice}</span>
                            <span className="ml-0 md:ml-2 text-xs text-gray-500">{item.isBestSeller ? "Best Seller" : item.source}</span>
                            {item.reviewsCount && <span className="ml-0 md:ml-2 text-xs text-gray-400">Reviews: {item.reviewsCount}</span>}
                          </li>
                        ))}
                      </ul>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>
          {/* Budget Box */}
          <div className="flex-1 bg-white rounded-3xl shadow-2xl border-2 border-[#0071dc] p-6 md:p-10 flex flex-col min-h-[420px] max-h-[600px] overflow-hidden">
            <h2 className="text-2xl font-bold text-[#0071dc] mb-4 md:mb-6 flex items-center gap-2">
              <span role="img" aria-label="budget">💸</span> Budget
            </h2>
            <div className="flex-1 overflow-y-auto pr-2">
              {budget ? (
                <ul className="space-y-5 text-slate-800 text-base">
                  {Object.entries(budget).map(([category, b], idx) => (
                    <li key={idx} className="flex justify-between border-b border-gray-200 pb-2">
                      <span className="capitalize font-semibold">{category}:</span>
                      <span className="text-gray-700">${b.min_budget} - ${b.max_budget}</span>
                    </li>
                  ))}
                </ul>
              ) : (
                <p className="text-gray-500">No budget info available.</p>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EventDetailsPage;
