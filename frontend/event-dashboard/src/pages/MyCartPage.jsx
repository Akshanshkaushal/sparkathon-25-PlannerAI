import React from 'react';
import { useLocation } from 'react-router-dom';
import MyCart from '../components/my-cart/MyCart';

const MyCartPage = () => {
  const location = useLocation();
  const { cartData } = location.state || {};

  return (
    <div>
      <h1 className="text-3xl font-bold text-text-primary mb-6">My Cart</h1>
      <MyCart cartData={cartData} />
    </div>
  );
};

export default MyCartPage;