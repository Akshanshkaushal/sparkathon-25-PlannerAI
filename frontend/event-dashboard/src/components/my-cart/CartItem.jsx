import React from 'react';
import Card from '../common/Card';

const CartItem = ({ item }) => {
  return (
    <Card className="flex flex-col justify-between">
      <div>
        <h3 className="text-xl font-bold text-text-primary">{item.title}</h3>
        <p className="text-text-secondary mt-2">Source: {item.source}</p>
        <p className="text-text-secondary">Reviews: {item.reviewsCount}</p>
        {item.isBestSeller && <span className="text-xs font-semibold inline-block py-1 px-2 uppercase rounded-full text-green-600 bg-green-200 mt-2">Best Seller</span>}
      </div>
      <div className="mt-4">
        <p className="text-lg font-semibold text-text-primary">{item.price.currency}{item.price.currentPrice}</p>
        <a href={item.link} target="_blank" rel="noopener noreferrer" className="text-blue-400 hover:underline mt-2 inline-block">
          View Product
        </a>
      </div>
    </Card>
  );
};

export default CartItem;