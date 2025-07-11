import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/layout/Header';
import Sidebar from './components/layout/Sidebar';
import DashboardPage from './pages/DashboardPage';
import MyCartPage from './pages/MyCartPage';

const App = () => {
  return (
    <Router>
      <div className="flex h-screen bg-primary">
        <Sidebar />
        <div className="flex-1 flex flex-col">
          <Header />
          <main className="flex-1 p-6 overflow-y-auto">
            <Routes>
              <Route path="/" element={<DashboardPage />} />
              <Route path="/my-cart" element={<MyCartPage />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
};

export default App;