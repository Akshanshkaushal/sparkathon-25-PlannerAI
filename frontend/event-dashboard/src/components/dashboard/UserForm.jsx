// src/components/dashboard/UserForm.jsx

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { triggerEvent, updateUserPreferences } from '../../api/eventApi';
import { Input } from "../ui/input";
import {Button} from '../ui/button';
import Loader from '../common/Loader';

const UserForm = () => {
  const [formData, setFormData] = useState({
    username: '',
    eventname: '',
    preferences: '',
    minBudget: '',
    maxBudget: '',
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const navigate = useNavigate();

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({ ...prev, [name]: value }));
  };

  const dummyCartData = {
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

  const handleSubmit = (e) => {
    e.preventDefault();
    navigate('/my-cart', { state: { cartData: dummyCartData } });
  };

  const handlePreferencesSubmit = (e) => {
    e.preventDefault();
    navigate('/my-cart', { state: { cartData: dummyCartData } });
  };

  return (
    <form onSubmit={handleSubmit} className="w-full flex flex-col gap-4">
      <div className="grid  grid-cols-1 sm:grid-cols-2 gap-4">
        <Input
          label="Username (Email)"
          labelClassName="text-blue-600"
          name="username"
          value={formData.username}
          onChange={handleChange}
          placeholder="username@example.com"
          required
        />
        <Input
          label="Event Name"
          name="eventname"
          value={formData.eventname}
          onChange={handleChange}
          placeholder="Birthday, Wedding, etc."
          required
        />
      </div>

      <Input
        label="Preferences (comma-separated)"
        name="preferences"
        value={formData.preferences}
        onChange={handleChange}
        placeholder="books, gadgets, travel, cooking"
        required
      />

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        <Input
          label="Minimum Budget ($)"
          name="minBudget"
          type="number"
          value={formData.minBudget}
          onChange={handleChange}
          placeholder="100"
          required
        />
        <Input
          label="Maximum Budget ($)"
          name="maxBudget"
          type="number"
          value={formData.maxBudget}
          onChange={handleChange}
          placeholder="500"
          required
        />
      </div>

      {error && (
        <div className="bg-red-100 border border-red-300 text-red-800 px-4 py-2 rounded-xl flex items-center gap-2 text-sm shadow">
          <svg className="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          {error}
        </div>
      )}

      {success && (
        <div className="bg-green-100 border border-green-300 text-green-800 px-4 py-2 rounded-xl flex items-center gap-2 text-sm shadow">
          <svg className="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
          </svg>
          {success}
        </div>
      )}

      <div className="flex flex-col sm:flex-row gap-2 mt-2">
        {loading ? (
          <div className="flex items-center justify-center space-x-3 bg-[#0071dc] text-white py-6 px-8 rounded-xl w-full shadow text-lg">
            <Loader />
            <span className="font-medium">Processing...</span>
          </div>
        ) : (
          <div className='flex items-center  gap-11'>
            <Button type="submit" className="w-full mb-3">
              <svg className="w-6 h-6 mr-3 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              Generate Event Plan
            </Button>
            <Button type="button" onClick={handlePreferencesSubmit} className="w-full mt-1">
              <svg className="w-6 h-6 mr-3 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
              Save Preferences Only
            </Button>
          </div>
        )}
      </div>

      <div className="text-center pt-3">
        <div className="inline-flex items-center gap-2 text-sm text-gray-700 bg-indigo-100/60 px-4 py-2 rounded-full shadow">
          <span className="text-xl">✨</span>
          <p>Our AI will analyze your preferences and create a personalized shopping plan</p>
        </div>
      </div>
    </form>
  );
};

export default UserForm;
