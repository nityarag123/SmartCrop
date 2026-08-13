import React from 'react';
import { Link } from 'react-router-dom';

const Home = () => {
  return (
    <div>
      {/* Hero Section */}
      <section className="hero">
        <div className="container mx-auto px-4">
          <div className="hero-content text-center">
            <h1 className="text-5xl md:text-7xl font-bold mb-6 text-gradient">
              Welcome to Fixora
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto">
              Professional business solutions and services for modern enterprises.
              We deliver exceptional results through innovation and expertise.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link to="/services" className="btn">
                Our Services
              </Link>
              <Link to="/contact" className="btn btn-outline">
                Get in Touch
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="section bg-darker">
        <div className="container mx-auto px-4">
          <h2 className="section-title">Why Choose Fixora?</h2>
          <div className="grid-3">
            <div className="card text-center">
              <div className="w-16 h-16 bg-gradient rounded-lg flex items-center justify-center mx-auto mb-4">
                <i className="fas fa-rocket text-black text-2xl"></i>
              </div>
              <h3 className="text-xl font-semibold mb-3">Innovation</h3>
              <p className="text-gray-400">
                Cutting-edge solutions that drive your business forward with the latest technologies.
              </p>
            </div>
            <div className="card text-center">
              <div className="w-16 h-16 bg-gradient rounded-lg flex items-center justify-center mx-auto mb-4">
                <i className="fas fa-shield-alt text-black text-2xl"></i>
              </div>
              <h3 className="text-xl font-semibold mb-3">Reliability</h3>
              <p className="text-gray-400">
                Dependable services and support you can count on, 24/7 availability guaranteed.
              </p>
            </div>
            <div className="card text-center">
              <div className="w-16 h-16 bg-gradient rounded-lg flex items-center justify-center mx-auto mb-4">
                <i className="fas fa-chart-line text-black text-2xl"></i>
              </div>
              <h3 className="text-xl font-semibold mb-3">Growth</h3>
              <p className="text-gray-400">
                Scalable solutions that grow with your business and maximize your potential.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Services Preview */}
      <section className="section">
        <div className="container mx-auto px-4">
          <h2 className="section-title">Our Services</h2>
          <div className="grid-2">
            <div className="card">
              <h3 className="text-2xl font-semibold mb-4 text-green">Business Consulting</h3>
              <p className="text-gray-400 mb-4">
                Strategic guidance and expert advice to help your business thrive in competitive markets.
              </p>
              <Link to="/services" className="text-green hover:text-white transition-colors">
                Learn More <i className="fas fa-arrow-right ml-2"></i>
              </Link>
            </div>
            <div className="card">
              <h3 className="text-2xl font-semibold mb-4 text-green">Technology Solutions</h3>
              <p className="text-gray-400 mb-4">
                Custom software development and IT infrastructure solutions tailored to your needs.
              </p>
              <Link to="/services" className="text-green hover:text-white transition-colors">
                Learn More <i className="fas fa-arrow-right ml-2"></i>
              </Link>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section bg-darker">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Ready to Transform Your Business?
          </h2>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            Let's discuss how Fixora can help you achieve your goals and drive success.
          </p>
          <Link to="/contact" className="btn btn-lg">
            Start Your Journey
          </Link>
        </div>
      </section>
    </div>
  );
};

export default Home;
