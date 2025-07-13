import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Header from './components/layout/Header';
import Sidebar from './components/layout/Sidebar';
import DashboardPage from './pages/DashboardPage';
import MyCartPage from './pages/MyCartPage';
import Navbar from './components/layout/Navbar';


const App = () => {
  return (
    <Router>
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-purple-50">
        
          <div className="flex-1 flex flex-col">
            <Navbar />
            <main className="flex-1 p-6 overflow-y-auto">
              <div className="max-w-8xl mx-auto">
                <Routes>
                  <Route path="/" element={<DashboardPage />} />
                  <Route path="/my-cart" element={<MyCartPage />} />
                </Routes>
              </div>
            </main>
          </div>
        </div>
      
    </Router>
  );
};

export default App;