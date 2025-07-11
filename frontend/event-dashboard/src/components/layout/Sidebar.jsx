import React from 'react';
import { NavLink } from 'react-router-dom';

const Sidebar = () => {
  return (
    <aside className="w-64 bg-secondary p-4">
      <nav>
        <ul>
          <li>
            <NavLink to="/" className="block py-2 px-4 rounded hover:bg-accent text-text-secondary" activeClassName="bg-accent text-text-primary">
              Dashboard
            </NavLink>
          </li>
          <li>
            <NavLink to="/my-cart" className="block py-2 px-4 rounded hover:bg-accent text-text-secondary" activeClassName="bg-accent text-text-primary">
              My Cart
            </NavLink>
          </li>
        </ul>
      </nav>
    </aside>
  );
};

export default Sidebar;