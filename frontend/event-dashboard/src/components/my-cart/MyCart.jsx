import React from 'react';
import CartItem from './CartItem';

const MyCart = ({ cartData }) => {
  if (!cartData || !cartData.cart) {
    return <p className="text-text-primary text-center">No cart data available. Please generate a plan from the dashboard.</p>;
  }

  const { cart, budget, plan } = cartData;

  return (
    <div className="space-y-8">
      <div>
        <h2 className="text-3xl font-bold text-text-primary mb-4">Your Event Plan</h2>
        <p className="text-lg text-text-secondary"><strong>Theme:</strong> {plan.decoration_theme}</p>
      </div>

      {Object.keys(cart).map((category) => (
        cart[category].length > 0 && (
          <div key={category}>
            <h3 className="text-2xl font-semibold text-text-primary capitalize mb-4">{category}</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {cart[category].map((item, index) => (
                <CartItem key={index} item={item} />
              ))}
            </div>
          </div>
        )
      ))}
    </div>
  );
};

export default MyCart;