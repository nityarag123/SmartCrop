import React from 'react';
import { Link } from 'react-router-dom';

const Services = () => {
  const services = [
    {
      icon: 'fas fa-chart-line',
      title: 'Business Consulting',
      description: 'Strategic planning and business development services to help you grow and scale.',
      features: ['Market Analysis', 'Strategic Planning', 'Business Development', 'Performance Optimization']
    },
    {
      icon: 'fas fa-code',
      title: 'Software Development',
      description: 'Custom software solutions built with modern technologies and best practices.',
      features: ['Web Applications', 'Mobile Apps', 'API Development', 'System Integration']
    },
    {
      icon: 'fas fa-palette',
      title: 'UI/UX Design',
      description: 'Beautiful, user-centered designs that enhance user experience and engagement.',
      features: ['User Research', 'Interface Design', 'Prototyping', 'Usability Testing']
    },
    {
      icon: 'fas fa-bullhorn',
      title: 'Digital Marketing',
      description: 'Comprehensive digital marketing strategies to increase your online presence.',
      features: ['SEO Optimization', 'Social Media', 'Content Marketing', 'PPC Advertising']
    },
    {
      icon: 'fas fa-cloud',
      title: 'Cloud Solutions',
      description: 'Scalable cloud infrastructure and migration services for modern businesses.',
      features: ['Cloud Migration', 'Infrastructure Setup', 'DevOps', 'Monitoring']
    },
    {
      icon: 'fas fa-shield-alt',
      title: 'Cybersecurity',
      description: 'Comprehensive security solutions to protect your business and data.',
      features: ['Security Audits', 'Threat Assessment', 'Data Protection', 'Compliance']
    }
  ];

  return (
    <div>
      {/* Hero Section */}
      <section className="hero">
        <div className="container mx-auto px-4">
          <div className="hero-content text-center">
            <h1 className="text-5xl md:text-7xl font-bold mb-6 text-gradient">
              Our Services
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto">
              Comprehensive business solutions tailored to your specific needs and goals.
            </p>
          </div>
        </div>
      </section>

      {/* Services Grid */}
      <section className="section bg-darker">
        <div className="container mx-auto px-4">
          <h2 className="section-title">What We Offer</h2>
          <div className="grid-3">
            {services.map((service, index) => (
              <div key={index} className="card">
                <div className="w-16 h-16 bg-gradient rounded-lg flex items-center justify-center mb-4">
                  <i className={`${service.icon} text-black text-2xl`}></i>
                </div>
                <h3 className="text-2xl font-semibold mb-3 text-green">{service.title}</h3>
                <p className="text-gray-400 mb-4">{service.description}</p>
                <ul className="space-y-2">
                  {service.features.map((feature, idx) => (
                    <li key={idx} className="flex items-center text-gray-300">
                      <i className="fas fa-check text-green mr-2"></i>
                      {feature}
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Process Section */}
      <section className="section">
        <div className="container mx-auto px-4">
          <h2 className="section-title">Our Process</h2>
          <div className="grid-4">
            <div className="text-center">
              <div className="w-20 h-20 bg-gradient rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-black font-bold text-xl">1</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Discovery</h3>
              <p className="text-gray-400">We understand your needs and objectives</p>
            </div>
            <div className="text-center">
              <div className="w-20 h-20 bg-gradient rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-black font-bold text-xl">2</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Strategy</h3>
              <p className="text-gray-400">We develop a comprehensive plan</p>
            </div>
            <div className="text-center">
              <div className="w-20 h-20 bg-gradient rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-black font-bold text-xl">3</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Execution</h3>
              <p className="text-gray-400">We implement the solution</p>
            </div>
            <div className="text-center">
              <div className="w-20 h-20 bg-gradient rounded-full flex items-center justify-center mx-auto mb-4">
                <span className="text-black font-bold text-xl">4</span>
              </div>
              <h3 className="text-xl font-semibold mb-2">Support</h3>
              <p className="text-gray-400">We provide ongoing maintenance</p>
            </div>
          </div>
        </div>
      </section>

      {/* Industries Section */}
      <section className="section bg-darker">
        <div className="container mx-auto px-4">
          <h2 className="section-title">Industries We Serve</h2>
          <div className="grid-2">
            <div className="space-y-4">
              <div className="flex items-center">
                <i className="fas fa-building text-green mr-3 text-xl"></i>
                <span className="text-gray-300">Technology & Software</span>
              </div>
              <div className="flex items-center">
                <i className="fas fa-shopping-cart text-green mr-3 text-xl"></i>
                <span className="text-gray-300">E-commerce & Retail</span>
              </div>
              <div className="flex items-center">
                <i className="fas fa-heartbeat text-green mr-3 text-xl"></i>
                <span className="text-gray-300">Healthcare</span>
              </div>
              <div className="flex items-center">
                <i className="fas fa-graduation-cap text-green mr-3 text-xl"></i>
                <span className="text-gray-300">Education</span>
              </div>
            </div>
            <div className="space-y-4">
              <div className="flex items-center">
                <i className="fas fa-briefcase text-green mr-3 text-xl"></i>
                <span className="text-gray-300">Finance & Banking</span>
              </div>
              <div className="flex items-center">
                <i className="fas fa-industry text-green mr-3 text-xl"></i>
                <span className="text-gray-300">Manufacturing</span>
              </div>
              <div className="flex items-center">
                <i className="fas fa-plane text-green mr-3 text-xl"></i>
                <span className="text-gray-300">Travel & Hospitality</span>
              </div>
              <div className="flex items-center">
                <i className="fas fa-futbol text-green mr-3 text-xl"></i>
                <span className="text-gray-300">Sports & Entertainment</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Ready to Get Started?
          </h2>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            Let's discuss your project and find the perfect solution for your business needs.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link to="/contact" className="btn">
              Get Free Consultation
            </Link>
            <Link to="/portfolio" className="btn btn-outline">
              View Our Work
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Services;
