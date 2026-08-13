import React from 'react';
import { Link } from 'react-router-dom';

const Portfolio = () => {
  const projects = [
    {
      title: 'E-Commerce Platform',
      category: 'Web Development',
      description: 'Complete e-commerce solution with payment integration and inventory management.',
      image: 'fas fa-shopping-cart',
      technologies: ['React', 'Node.js', 'MongoDB', 'Stripe']
    },
    {
      title: 'Healthcare Management System',
      category: 'Healthcare',
      description: 'Comprehensive patient management system with appointment scheduling and EMR.',
      image: 'fas fa-heartbeat',
      technologies: ['Vue.js', 'Python', 'PostgreSQL', 'AWS']
    },
    {
      title: 'Financial Dashboard',
      category: 'Finance',
      description: 'Real-time financial analytics dashboard for investment tracking and reporting.',
      image: 'fas fa-chart-line',
      technologies: ['Angular', 'TypeScript', 'D3.js', 'Firebase']
    },
    {
      title: 'Mobile Banking App',
      category: 'Mobile Development',
      description: 'Secure mobile banking application with biometric authentication.',
      image: 'fas fa-mobile-alt',
      technologies: ['React Native', 'Node.js', 'MySQL', 'JWT']
    },
    {
      title: 'Learning Management System',
      category: 'Education',
      description: 'Online learning platform with video streaming and progress tracking.',
      image: 'fas fa-graduation-cap',
      technologies: ['Next.js', 'GraphQL', 'Prisma', 'Vercel']
    },
    {
      title: 'Supply Chain Management',
      category: 'Logistics',
      description: 'End-to-end supply chain tracking and optimization platform.',
      image: 'fas fa-truck',
      technologies: ['Vue.js', 'Laravel', 'Redis', 'Docker']
    }
  ];

  return (
    <div>
      {/* Hero Section */}
      <section className="hero">
        <div className="container mx-auto px-4">
          <div className="hero-content text-center">
            <h1 className="text-5xl md:text-7xl font-bold mb-6 text-gradient">
              Our Portfolio
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto">
              Explore our successful projects and see how we've helped businesses achieve their goals.
            </p>
          </div>
        </div>
      </section>

      {/* Portfolio Grid */}
      <section className="section bg-darker">
        <div className="container mx-auto px-4">
          <h2 className="section-title">Featured Projects</h2>
          <div className="grid-3">
            {projects.map((project, index) => (
              <div key={index} className="card">
                <div className="w-16 h-16 bg-gradient rounded-lg flex items-center justify-center mb-4">
                  <i className={`${project.image} text-black text-2xl`}></i>
                </div>
                <h3 className="text-2xl font-semibold mb-2 text-green">{project.title}</h3>
                <p className="text-gray-400 mb-3">{project.category}</p>
                <p className="text-gray-300 mb-4">{project.description}</p>
                <div className="flex flex-wrap gap-2 mb-4">
                  {project.technologies.map((tech, idx) => (
                    <span key={idx} className="px-3 py-1 bg-gray-800 text-green text-sm rounded-full">
                      {tech}
                    </span>
                  ))}
                </div>
                <Link to="/contact" className="text-green hover:text-white transition-colors">
                  View Details <i className="fas fa-arrow-right ml-2"></i>
                </Link>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="section">
        <div className="container mx-auto px-4">
          <div className="grid-4">
            <div className="text-center">
              <div className="text-4xl font-bold text-green mb-2">500+</div>
              <p className="text-gray-400">Projects Completed</p>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-green mb-2">200+</div>
              <p className="text-gray-400">Happy Clients</p>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-green mb-2">50+</div>
              <p className="text-gray-400">Team Members</p>
            </div>
            <div className="text-center">
              <div className="text-4xl font-bold text-green mb-2">99%</div>
              <p className="text-gray-400">Client Satisfaction</p>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="section bg-darker">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl md:text-4xl font-bold mb-6">
            Ready to Start Your Project?
          </h2>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            Let's discuss your vision and create something amazing together.
          </p>
          <Link to="/contact" className="btn">
            Get Started Today
          </Link>
        </div>
      </section>
    </div>
  );
};

export default Portfolio;
