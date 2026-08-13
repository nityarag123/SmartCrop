import React from 'react';
import { Link } from 'react-router-dom';

const Footer = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-darker border-t border-gray-800">
      <div className="container mx-auto px-4 py-12">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
          {/* Company Info */}
          <div>
            <div className="flex items-center space-x-3 mb-4">
              <div className="w-8 h-8 bg-gradient rounded-lg flex items-center justify-center">
                <span className="text-black font-bold">F</span>
              </div>
              <span className="text-xl font-bold text-white">Fixora</span>
            </div>
            <p className="text-gray-400 mb-4">
              Professional business solutions and services for modern enterprises.
            </p>
            <div className="flex space-x-4">
              <a href="#" className="text-gray-400 hover:text-green transition-colors">
                <i className="fab fa-facebook-f"></i>
              </a>
              <a href="#" className="text-gray-400 hover:text-green transition-colors">
                <i className="fab fa-twitter"></i>
              </a>
              <a href="#" className="text-gray-400 hover:text-green transition-colors">
                <i className="fab fa-linkedin-in"></i>
              </a>
              <a href="#" className="text-gray-400 hover:text-green transition-colors">
                <i className="fab fa-instagram"></i>
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-white font-semibold mb-4">Quick Links</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/about" className="text-gray-400 hover:text-green transition-colors">
                  About Us
                </Link>
              </li>
              <li>
                <Link to="/services" className="text-gray-400 hover:text-green transition-colors">
                  Services
                </Link>
              </li>
              <li>
                <Link to="/products" className="text-gray-400 hover:text-green transition-colors">
                  Products
                </Link>
              </li>
              <li>
                <Link to="/portfolio" className="text-gray-400 hover:text-green transition-colors">
                  Portfolio
                </Link>
              </li>
              <li>
                <Link to="/contact" className="text-gray-400 hover:text-green transition-colors">
                  Contact
                </Link>
              </li>
            </ul>
          </div>

          {/* Services */}
          <div>
            <h3 className="text-white font-semibold mb-4">Services</h3>
            <ul className="space-y-2">
              <li>
                <Link to="/services" className="text-gray-400 hover:text-green transition-colors">
                  Consulting
                </Link>
              </li>
              <li>
                <Link to="/services" className="text-gray-400 hover:text-green transition-colors">
                  Development
                </Link>
              </li>
              <li>
                <Link to="/services" className="text-gray-400 hover:text-green transition-colors">
                  Design
                </Link>
              </li>
              <li>
                <Link to="/services" className="text-gray-400 hover:text-green transition-colors">
                  Marketing
                </Link>
              </li>
              <li>
                <Link to="/services" className="text-gray-400 hover:text-green transition-colors">
                  Support
                </Link>
              </li>
            </ul>
          </div>

          {/* Contact Info */}
          <div>
            <h3 className="text-white font-semibold mb-4">Contact Info</h3>
            <div className="space-y-2 text-gray-400">
              <p>
                <i className="fas fa-map-marker-alt mr-2 text-green"></i>
                123 Business Street, Suite 100
              </p>
              <p>
                <i className="fas fa-phone mr-2 text-green"></i>
                +1 (555) 123-4567
              </p>
              <p>
                <i className="fas fa-envelope mr-2 text-green"></i>
                info@fixora.com
              </p>
              <p>
                <i className="fas fa-clock mr-2 text-green"></i>
                Mon - Fri: 9:00 AM - 6:00 PM
              </p>
            </div>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="border-t border-gray-800 mt-8 pt-8 flex flex-col md:flex-row justify-between items-center">
          <p className="text-gray-400 text-sm">
            © {currentYear} Fixora Store. All rights reserved.
          </p>
          <div className="flex space-x-6 mt-4 md:mt-0">
            <Link to="/privacy-policy" className="text-gray-400 hover:text-green text-sm transition-colors">
              Privacy Policy
            </Link>
            <Link to="/terms-of-service" className="text-gray-400 hover:text-green text-sm transition-colors">
              Terms of Service
            </Link>
            <Link to="/sitemap" className="text-gray-400 hover:text-green text-sm transition-colors">
              Sitemap
            </Link>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
