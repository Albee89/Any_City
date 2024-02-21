import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';  
import Search from './components/Search';
import About from './components/About';
import Home from './components/Home';
import "./App.css";



function App() {
  return (
    <Router>
      <div>
        <nav>
          <ul>
          <li><Link to="/">Home</Link></li>
            <li><Link to="/search">Search</Link></li>
            <li><Link to="/about">About</Link></li>
            
            
          
          </ul>
        </nav>
        
        <Routes>  
        <Route path="/" element={<Home />} />
          <Route path="/search" element={<Search />} />
          <Route path="/about" element={<About />} />
        </Routes>  
      </div>
    </Router>
  );
}

export default App;
