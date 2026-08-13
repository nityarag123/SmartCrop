import React from 'react';
import { Link } from 'react-router-dom';

const Products = () => {
  const products = [
    {
      icon: 'fas fa-laptop-code',
      title: 'Fixora CRM',
      description: 'Complete customer relationship management system for businesses of all sizes.',
      features: ['Contact Management', 'Sales Pipeline', 'Analytics Dashboard', 'Mobile App'],
      price: 'Starting at $29/month'
    },
    {
      icon: 'fas fa-chart-bar',
      title: 'Fixora Analytics',
      description: 'Advanced business intelligence and analytics platform for data-driven decisions.',
      features: ['Real-time Reports', 'Custom Dashboards', 'Data Visualization', 'API Integration'],
      price: 'Starting at $49/month'
    },
    {
      icon: 'fas fa-store',
      title: 'Fixora Commerce',
      description: 'E-commerce platform with built-in marketing and inventory management.',
      features: ['Online Store', 'Payment Processing', 'Inventory Management', 'Marketing Tools'],
      price: 'Starting at $39/month'
    },
    {
      icon: 'fas fa-project-diagram',
      title: 'Fixora Project',
      description: 'Project management and collaboration tools for teams and organizations.',
      features: ['Task Management', 'Team Collaboration', 'Time Tracking', 'Resource Planning'],
      price: 'Starting at $19/month'
    },
    {
      icon: 'fas fa-shield-alt',
      title: 'Fixora Security',
      description: 'Comprehensive cybersecurity solutions to protect your business assets.',
      features: ['Threat Detection', 'Data Encryption', 'Access Control', 'Compliance Tools'],
      price: 'Starting at $59/month'
    },
    {
      icon: 'fas fa-mobile-alt',
      title: 'Fixora Mobile',
      description: 'Custom mobile application development for iOS and Android platforms.',
      features: ['Native Apps', 'Cross-platform', 'App Store Deployment', 'Maintenance'],
      price: 'Custom Pricing'
    }
  ];

  return (
    <div>
      {/* Hero Section */}
      <section className="hero">
        <div className="container mx-auto px-4">
          <div className="hero-content text-center">
            <h1 className="text-5xl md:text-7xl font-bold mb-6 text-gradient">
              Our Products
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto">
              Powerful software solutions designed to streamline your business operations and drive growth.
            </p>
          </div>
        </div>
      </section>

      {/* Products Grid */}
      <section className="section bg-darker">
        <div className="container mx-auto px-4">
          <h2 className="section-title">Featured Products</h2>
          <div className="grid-3">
            {products.map((product, index) => (
              <div key={index} className="card">
                <div className="w-16 h-16 bg-gradient rounded-lg flex items-center justify-center mb-4">
                  <i className={`${product.icon} text-black text-2xl`}></i>
                </div>
                <h3 className="text-2xl font-semibold mb-3 text-green">{product.title}</h3>
                <p className="text-gray-400 mb-4">{product.description}</p>
                <ul className="space-y-2 mb-6">
                  {product.features.map((feature, idx) => (
                    <li key={idx} className="flex items-center text-gray-300 text-sm">
                      <i className="fas fa-check text-green mr-2"></i>
                      {feature}
                    </li>
                  ))}
                </ul>
                <div className="flex justify-between items-center">
                  <span className="text-green font-semibold">{product.price}</span>
                  <Link to="/contact" className="btn btn-sm">
                    Learn More
                  </Link>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="section">
        <div className="container mx-auto px-4">
          <h2 className="section-title">Why Choose Our Products?</h2>
          <div className="grid-2">
            <div className="card">
              <h3 className="text-2xl font-semibold mb-4 text-green">Scalable & Reliable</h3>
              <p className="text-gray-400 mb-4">
                Our products are built with scalability in mind, ensuring they grow with your business
                and provide reliable performance even under high loads.
              </p>
              <ul className="space-y-2">
                <li className="flex items-center text-gray-300">
                  <i className="fas fa-check text-green mr-2"></i>
                  Cloud-native architecture
                </li>
                <li className="flex items-center text-gray-300">
                  <i className="fas fa-check text-green mr-2"></i>
                  99.9% uptime guarantee
                </li>
                <li className="flex items-center text-gray-300">
                  <i className="fas fa-check text-green mr-2"></i>
                  Automatic scaling
                </li>
              </ul>
            </div>
            <div className="card">
              <h3 className="text-2xl font-semibold mb-4 text-green">Security First</h3>
              <p className="text-gray-400 mb-4">
                Security is built into every layer of our products, ensuring your data and
                your customers' data is always protected.
              </p>
              <ul className="space-y-2">
                <li className="flex items-center text-gray-300">
                  <i className="fas fa-check text-green mr-2"></i>
                  End-to-end encryption
                </li>
                <li className="flex items-center text-gray-300">
                  <i className="fas fa-check text-green mr-2"></i>
                  Regular security audits
                </li>
                <li className="flex items-center text-gray-300">
                  <i className="fas fa-check text-green mr-2"></i>
                  Compliance ready
                </li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section className="section bg-darker">
        <div className="container mx-auto px-4">
          <h2 className="section-title">Simple, Transparent Pricing</h2>
          <div className="grid-3">
            <div className="card text-center">
              <h3 className="text-2xl font-semibold mb-2">Starter</h3>
              <div className="text-4xl font-bold text-green mb-4">$19<span className="text-lg text-gray-400">/month</span></div>
              <ul className="space-y-3 mb-6 text-left">
                <li className="flex items-center text-gray-300">
                  <i className="fas fa-check text-green mr-2"></i>
                  Up to 5 users
                </li>
                <li className="flex items-center text-gray-300">
                  <i className="fas fa-check text-green mr-2"></i>
                  Basic features
                </li>
                <li className="flex items-center text-gray-300">
                  <i className="fas fa-check text-green mr-2"></i>
                  Email support
                </li>
              </ul>
              <Link to="/contact" className="btn w-full">Get Started</Link>
            </div>
            <div className="card text-center border-2 border-green">
              <div className="absolute top-0 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
                <span className="bg-green text-black px-4 py-1 rounded-full text-sm font-semibold">Most Popular</span>
              </div>
              <h3 className="text-2xl font-semibold mb-2">Professional</h3>
              <div className="text-4xl font-bold text-green mb-4">$49<span className="text-lg text-gray-400">/month</span></div>
              <ul className="space-y-3 mb-6 text-left">
                <li className="flex items-center text-gray-300">
                  <i className="fas fa-check text-green mr-2"></i>
                  Up to 25 users
                </li>
                <li className="flex items-center text-gray-300">
                  <i className="fas fa-check text-green mr-2"></i>
                  All features
                </li>
                <li className="flex items-center text-gray-300">
                  <i className="fas fa-check text-green mr-2"></i>
                  Priority support
                </li>
              </ul>
              <Link to="/contact" className="btn w-full">Get Started</Link>
            </div>
            <div className="card text-center">
              <h3 className="text-2xl font-semibold mb-2">Enterprise</h3>
              <div className="text-4xl font-bold text-green mb-4">Custom</div>
              <ul className="space-y-3 mb-6 text-left">
                <li className="flex items-center text-gray-300">
                  <i className="fas fa-check text-green mr-2"></i>
                  Unlimited users
                </li>
                <li className="flex items-center text-gray-300">
                  <i className="fas fa-check text-green mr-2"></i>
                  Custom features
                </li>
                <li className="flex items-center text-gray-300">
                  <i className="fas fa-check text-green mr-2"></i>
                  24/7 support
                </li>
              </ul>
              <Link to="/contact" className="btn w-full">Contact Sales</Link>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Need a Custom Solution?
          </h2>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            We also offer custom development services to create tailored solutions for your specific business needs.
          </p>
          <Link to="/contact" className="btn">
            Discuss Your Project
          </Link>
        </div>
      </section>
    </div>
  );
};

export default Products;
