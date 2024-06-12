import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Navbar from './components/navbar.js';
import Home from './routes/landing/landing';
import Finances from './routes/finances/finances.js';
import Consumption from './routes/consumption/consumption.js';
import NotFound from './routes/not-found/not-found.js';
import About from './routes/about/about.js';
import './core-ui/App.css';

const App = () => {
  return (
    <div className="app flex flex-col min-h-screen">
      <Navbar />
      <div className="flex-grow bg-gradient-to-r from-dark-purple to-dark-blue">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/finances" element={<Finances />} />
          <Route path="/consumption" element={<Consumption />} />
          <Route path="/about" element={<About />} />
          <Route path="*" element={<NotFound />} />
        </Routes>
      </div>
    </div>
  );
};

export default App;
