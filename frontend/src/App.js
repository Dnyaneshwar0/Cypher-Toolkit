import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Dummy from './pages/Dummy';
import Steg from './pages/Steg';
import Footer from './components/Footer';

export default function App() {
  return (
    <>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dummy" element={<Dummy />} />
        <Route path="/steg" element={<Steg />} />
      </Routes>
      <Footer />
    </>
  );
}
