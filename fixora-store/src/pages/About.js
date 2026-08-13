import React from 'react';
import { Link } from 'react-router-dom';

const About = () => {
  return (
    <div>
      {/* Hero Section */}
      <section className="hero">
        <div className="container mx-auto px-4">
          <div className="hero-content text-center">
            <h1 className="text-5xl md:text-7xl font-bold mb-6 text-gradient">
              About Fixora
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto">
              Learn about our mission, values, and the team behind Fixora's success.
            </p>
          </div>
        </div>
      </section>

      {/* Mission Section */}
      <section className="section bg-darker">
        <div className="container mx-auto px-4">
          <div className="grid-2">
            <div>
              <h2 className="text-3xl font-bold mb-6 text-green">Our Mission</h2>
              <p className="text-gray-300 text-lg mb-6">
                At Fixora, our mission is to empower businesses with innovative solutions
                that drive growth, efficiency, and success. We believe in the power of
                technology and strategic thinking to transform challenges into opportunities.
              </p>
              <p className="text-gray-300 text-lg">
                Founded in 2020, we've been helping companies of all sizes achieve their
                goals through our comprehensive suite of services and unwavering commitment
                to excellence.
              </p>
            </div>
            <div className="card">
              <h3 className="text-2xl font-semibold mb-4 text-green">Company Stats</h3>
              <div className="space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-gray-300">Years in Business</span>
                  <span className="text-green font-bold">4+</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-300">Projects Completed</span>
                  <span className="text-green font-bold">500+</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-300">Happy Clients</span>
                  <span className="text-green font-bold">200+</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-300">Team Members</span>
                  <span className="text-green font-bold">50+</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Values Section */}
      <section className="section">
        <div className="container mx-auto px-4">
          <h2 className="section-title">Our Values</h2>
          <div className="grid-3">
            <div className="card text-center">
              <div className="w-16 h-16 bg-gradient rounded-lg flex items-center justify-center mx-auto mb-4">
                <i className="fas fa-heart text-black text-2xl"></i>
              </div>
              <h3 className="text-xl font-semibold mb-3">Excellence</h3>
              <p className="text-gray-400">
                We strive for excellence in everything we do, delivering quality results that exceed expectations.
              </p>
            </div>
            <div className="card text-center">
              <div className="w-16 h-16 bg-gradient rounded-lg flex items-center justify-center mx-auto mb-4">
                <i className="fas fa-handshake text-black text-2xl"></i>
              </div>
              <h3 className="text-xl font-semibold mb-3">Integrity</h3>
              <p className="text-gray-400">
                We conduct business with honesty, transparency, and ethical practices in all our dealings.
              </p>
            </div>
            <div className="card text-center">
              <div className="w-16 h-16 bg-gradient rounded-lg flex items-center justify-center mx-auto mb-4">
                <i className="fas fa-lightbulb text-black text-2xl"></i>
              </div>
              <h3 className="text-xl font-semibold mb-3">Innovation</h3>
              <p className="text-gray-400">
                We embrace innovation and continuously seek new ways to solve problems and create value.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Team Section */}
      <section className="section bg-darker">
        <div className="container mx-auto px-4">
          <h2 className="section-title">Leadership Team</h2>
          <div className="grid-3">
            <div className="card text-center">
              <div className="w-24 h-24 bg-gradient rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-black font-bold text-2xl">JD</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">John Doe</h3>
              <p className="text-green mb-3">CEO & Founder</p>
              <p className="text-gray-400 text-sm">
                15+ years of experience in business strategy and technology leadership.
              </p>
            </div>
            <div className="card text-center">
              <div className="w-24 h-24 bg-gradient rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-black font-bold text-2xl">JS</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Jane Smith</h3>
              <p className="text-green mb-3">CTO</p>
              <p className="text-gray-400 text-sm">
                Expert in software architecture and emerging technologies.
              </p>
            </div>
            <div className="card text-center">
              <div className="w-24 h-24 bg-gradient rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-black font-bold text-2xl">MB</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Mike Brown</h3>
              <p className="text-green mb-3">COO</p>
              <p className="text-gray-400 text-sm">
                Operations specialist with a focus on efficiency and growth.
              </p>
            </div>
          </div>
          <div className="text-center mt-8">
            <Link to="/team" className="btn btn-outline">
              View Full Team
            </Link>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Ready to Work with Us?
          </h2>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            Join hundreds of satisfied clients who trust Fixora for their business needs.
          </p>
          <Link to="/contact" className="btn">
            Get Started Today
          </Link>
        </div>
      </section>
    </div>
  );
};

export default About;
