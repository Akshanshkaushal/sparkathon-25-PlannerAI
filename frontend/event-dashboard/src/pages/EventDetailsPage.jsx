import React from 'react';

const placeholderPlan = {
  decoration_theme: 'Birthday Bash',
  cake_suggestion: { type: 'Chocolate Truffle' },
  decoration_items: ['Balloons', 'Streamers', 'Confetti'],
  gift_suggestions: {
    specific_gifts: ['Book: The Alchemist', 'Bluetooth Speaker'],
    inspired_by_gifts: ['Personalized Mug'],
  },
};

const placeholderBudget = {
  decorations: { min_budget: 50, max_budget: 100 },
  gifts: { min_budget: 30, max_budget: 80 },
  cake: { min_budget: 20, max_budget: 40 },
};

const EventDetailsPage = () => {
  const plan = placeholderPlan;
  const budget = placeholderBudget;

  return (
    <div className="min-h-screen bg-[#f8fafc] flex flex-col items-center pt-32 pb-16">
      <div className="flex-grow w-full flex items-center justify-center">
        <div className="flex w-full max-w-7xl gap-10 mt-12 h-[420px]">
          {/* Event Items Box */}
          <div className="flex-1 bg-white rounded-2xl shadow-lg border-4 border-[#0071dc] p-10 flex flex-col">
            <h2 className="text-2xl font-bold text-[#0071dc] mb-6 flex items-center gap-2">
              <span role="img" aria-label="gift">🎁</span> Event Items
            </h2>
            <div className="flex-1 overflow-auto">
              {plan ? (
                <div className="space-y-5 text-slate-800 text-base">
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
                        {Object.values(plan.gift_suggestions).flat().map((gift, idx) => (
                          <li key={idx}>{gift}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              ) : (
                <p className="text-gray-500">No event items found.</p>
              )}
            </div>
          </div>
          {/* Budget Box */}
          <div className="flex-1 bg-white rounded-2xl shadow-lg border-4 border-[#0071dc] p-10 flex flex-col">
            <h2 className="text-2xl font-bold text-[#0071dc] mb-6 flex items-center gap-2">
              <span role="img" aria-label="budget">💸</span> Budget
            </h2>
            <div className="flex-1 overflow-auto">
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
