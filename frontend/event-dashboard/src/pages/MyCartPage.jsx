import React from 'react';
import { useLocation, Link } from 'react-router-dom';
import MyCart from '../components/my-cart/MyCart';
import Button from '../components/common/Button';

const MyCartPage = () => {
  const location = useLocation();
  const { cartData } = location.state || {};

  if (!cartData) {
    return (
      <div className="min-h-[70vh] flex flex-col items-center justify-center">
        <div className="max-w-lg mx-auto text-center">
          <div className="w-28 h-28 bg-gradient-to-br from-blue-200 to-indigo-200 rounded-full flex items-center justify-center mx-auto mb-8 shadow-lg">
            <svg className="w-16 h-16 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 3h2l.4 2M7 13h10l4-8H5.4m0 0L7 13m0 0l-2.5 5M7 13l2.5 5m6-5v6a2 2 0 01-2 2H9a2 2 0 01-2-2v-6m8 0V9a2 2 0 00-2-2H9a2 2 0 00-2 2v4.01" />
            </svg>
          </div>
          <h2 className="text-3xl font-bold text-slate-800 mb-4 font-display">Your Cart is Empty</h2>
          <p className="text-lg text-gray-600 mb-8 font-sans">Start by creating an event plan to see your personalized shopping recommendations.</p>
          <Link to="/">
            <Button className="text-xl py-4 px-10">
              <svg className="w-6 h-6 mr-2 inline" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
              </svg>
              Create Event Plan
            </Button>
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="fade-in py-24">
      <MyCart cartData={cartData} />
    </div>
  );
};

export default MyCartPage;