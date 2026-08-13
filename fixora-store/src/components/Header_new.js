import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';

const Header = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const location = useLocation();

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const isActive = (path) => {
    return location.pathname === path ? 'text-green border-b-2 border-green' : '';
  };

  return (
    <header className="bg-black shadow-lg sticky top-0 z-50">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center py-4">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-gradient rounded-lg flex items-center justify-center">
              <span className="text-black font-bold text-xl">F</span>
            </div>
            <span className="text-2xl font-bold text-white">Fixora</span>
          </Link>

          {/* Desktop Navigation */}
          <nav className="hidden lg:flex items-center space-x-8">
            <Link to="/" className={`nav-link ${isActive('/')}`}>Home</Link>
            <Link to="/about" className={`nav-link ${isActive('/about')}`}>About</Link>
            <Link to="/services" className={`nav-link ${isActive('/services')}`}>Services</Link>
            <Link to="/products" className={`nav-link ${isActive('/products')}`}>Products</Link>
            <Link to="/portfolio" className={`nav-link ${isActive('/portfolio')}`}>Portfolio</Link>
            <Link to="/weather" className={`nav-link ${isActive('/weather')}`}>Weather</Link>
            <Link to="/contact" className={`nav-link ${isActive('/contact')}`}>Contact</Link>
          </nav>

          {/* CTA Button */}
          <div className="hidden lg:block">
            <Link to="/contact" className="btn">
              Get Started
            </Link>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={toggleMenu}
            className="lg:hidden text-white p-2"
            aria-label="Toggle menu"
          >
            <i className={`fas ${isMenuOpen ? 'fa-times' : 'fa-bars'} text-xl`}></i>
          </button>
        </div>

        {/* Mobile Navigation */}
        {isMenuOpen && (
          <div className="lg:hidden py-4 border-t border-gray-800">
            <nav className="flex flex-col space-y-4">
              <Link to="/" className={`nav-link ${isActive('/')}`} onClick={toggleMenu}>
                Home
              </Link>
              <Link to="/about" className={`nav-link ${isActive('/about')}`} onClick={toggleMenu}>
                About
              </Link>
              <Link to="/services" className={`nav-link ${isActive('/services')}`} onClick={toggleMenu}>
                Services
              </Link>
              <Link to="/products" className={`nav-link ${isActive('/products')}`} onClick={toggleMenu}>
                Products
              </Link>
              <Link to="/portfolio" className={`nav-link ${isActive('/portfolio')}`} onClick={toggleMenu}>
                Portfolio
              </Link>
              <Link to="/weather" className={`nav-link ${isActive('/weather')}`} onClick={toggleMenu}>
                Weather
              </Link>
              <Link to="/contact" className={`nav-link ${isActive('/contact')}`} onClick={toggleMenu}>
                Contact
              </Link>
              <Link to="/contact" className="btn mt-4" onClick={toggleMenu}>
                Get Started
              </Link>
            </nav>
          </div>
        )}
      </div>
    </header>
  );
};

export default Header;
