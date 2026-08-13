import React, { useState } from 'react';

const Contact = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    company: '',
    phone: '',
    subject: '',
    message: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle form submission here
    console.log('Form submitted:', formData);
    alert('Thank you for your message! We will get back to you soon.');
    setFormData({
      name: '',
      email: '',
      company: '',
      phone: '',
      subject: '',
      message: ''
    });
  };

  return (
    <div>
      {/* Hero Section */}
      <section className="hero">
        <div className="container mx-auto px-4">
          <div className="hero-content text-center">
            <h1 className="text-5xl md:text-7xl font-bold mb-6 text-gradient">
              Contact Us
            </h1>
            <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto">
              Get in touch with our team. We're here to help you succeed.
            </p>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section className="section bg-darker">
        <div className="container mx-auto px-4">
          <div className="grid-2">
            {/* Contact Form */}
            <div className="card">
              <h2 className="text-2xl font-semibold mb-6 text-green">Send us a Message</h2>
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="grid-2">
                  <div>
                    <label htmlFor="name" className="block text-gray-300 mb-2">Name *</label>
                    <input
                      type="text"
                      id="name"
                      name="name"
                      value={formData.name}
                      onChange={handleChange}
                      required
                      className="form-input w-full"
                      placeholder="Your full name"
                    />
                  </div>
                  <div>
                    <label htmlFor="email" className="block text-gray-300 mb-2">Email *</label>
                    <input
                      type="email"
                      id="email"
                      name="email"
                      value={formData.email}
                      onChange={handleChange}
                      required
                      className="form-input w-full"
                      placeholder="your.email@example.com"
                    />
                  </div>
                </div>
                <div className="grid-2">
                  <div>
                    <label htmlFor="company" className="block text-gray-300 mb-2">Company</label>
                    <input
                      type="text"
                      id="company"
                      name="company"
                      value={formData.company}
                      onChange={handleChange}
                      className="form-input w-full"
                      placeholder="Your company name"
                    />
                  </div>
                  <div>
                    <label htmlFor="phone" className="block text-gray-300 mb-2">Phone</label>
                    <input
                      type="tel"
                      id="phone"
                      name="phone"
                      value={formData.phone}
                      onChange={handleChange}
                      className="form-input w-full"
                      placeholder="+1 (555) 123-4567"
                    />
                  </div>
                </div>
                <div>
                  <label htmlFor="subject" className="block text-gray-300 mb-2">Subject *</label>
                  <input
                    type="text"
                    id="subject"
                    name="subject"
                    value={formData.subject}
                    onChange={handleChange}
                    required
                    className="form-input w-full"
                    placeholder="How can we help you?"
                  />
                </div>
                <div>
                  <label htmlFor="message" className="block text-gray-300 mb-2">Message *</label>
                  <textarea
                    id="message"
                    name="message"
                    value={formData.message}
                    onChange={handleChange}
                    required
                    rows="5"
                    className="form-input form-textarea w-full"
                    placeholder="Tell us about your project or inquiry..."
                  ></textarea>
                </div>
                <button type="submit" className="btn w-full">
                  Send Message
                </button>
              </form>
            </div>

            {/* Contact Information */}
            <div className="space-y-8">
              <div className="card">
                <h3 className="text-xl font-semibold mb-4 text-green">Get in Touch</h3>
                <div className="space-y-4">
                  <div className="flex items-start">
                    <i className="fas fa-map-marker-alt text-green mr-3 mt-1"></i>
                    <div>
                      <p className="text-gray-300 font-semibold">Address</p>
                      <p className="text-gray-400">123 Business Street, Suite 100<br />New York, NY 10001</p>
                    </div>
                  </div>
                  <div className="flex items-start">
                    <i className="fas fa-phone text-green mr-3 mt-1"></i>
                    <div>
                      <p className="text-gray-300 font-semibold">Phone</p>
                      <p className="text-gray-400">+1 (555) 123-4567</p>
                    </div>
                  </div>
                  <div className="flex items-start">
                    <i className="fas fa-envelope text-green mr-3 mt-1"></i>
                    <div>
                      <p className="text-gray-300 font-semibold">Email</p>
                      <p className="text-gray-400">info@fixora.com</p>
                    </div>
                  </div>
                  <div className="flex items-start">
                    <i className="fas fa-clock text-green mr-3 mt-1"></i>
                    <div>
                      <p className="text-gray-300 font-semibold">Business Hours</p>
                      <p className="text-gray-400">Monday - Friday: 9:00 AM - 6:00 PM EST</p>
                    </div>
                  </div>
                </div>
              </div>

              <div className="card">
                <h3 className="text-xl font-semibold mb-4 text-green">Follow Us</h3>
                <div className="flex space-x-4">
                  <a href="#" className="w-12 h-12 bg-gray-800 rounded-lg flex items-center justify-center text-gray-400 hover:text-green hover:bg-gray-700 transition-colors">
                    <i className="fab fa-facebook-f"></i>
                  </a>
                  <a href="#" className="w-12 h-12 bg-gray-800 rounded-lg flex items-center justify-center text-gray-400 hover:text-green hover:bg-gray-700 transition-colors">
                    <i className="fab fa-twitter"></i>
                  </a>
                  <a href="#" className="w-12 h-12 bg-gray-800 rounded-lg flex items-center justify-center text-gray-400 hover:text-green hover:bg-gray-700 transition-colors">
                    <i className="fab fa-linkedin-in"></i>
                  </a>
                  <a href="#" className="w-12 h-12 bg-gray-800 rounded-lg flex items-center justify-center text-gray-400 hover:text-green hover:bg-gray-700 transition-colors">
                    <i className="fab fa-instagram"></i>
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Map Section */}
      <section className="section">
        <div className="container mx-auto px-4">
          <div className="card">
            <h2 className="text-2xl font-semibold mb-6 text-green">Find Us</h2>
            <div className="aspect-video bg-gray-800 rounded-lg flex items-center justify-center">
              <div className="text-center text-gray-400">
                <i className="fas fa-map-marked-alt text-4xl mb-4"></i>
                <p>Interactive map would be displayed here</p>
                <p className="text-sm">123 Business Street, Suite 100, New York, NY 10001</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* FAQ Section */}
      <section className="section bg-darker">
        <div className="container mx-auto px-4">
          <h2 className="section-title">Frequently Asked Questions</h2>
          <div className="grid-2">
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold mb-2 text-green">How quickly can you start on my project?</h3>
                <p className="text-gray-400">We typically begin new projects within 1-2 weeks, depending on our current workload and project complexity.</p>
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-2 text-green">Do you offer ongoing support?</h3>
                <p className="text-gray-400">Yes, we provide comprehensive support and maintenance services for all our projects.</p>
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-2 text-green">What is your typical project timeline?</h3>
                <p className="text-gray-400">Project timelines vary based on scope, but most projects are completed within 4-12 weeks.</p>
              </div>
            </div>
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold mb-2 text-green">Do you work with international clients?</h3>
                <p className="text-gray-400">Absolutely! We work with clients worldwide and are experienced in managing remote projects.</p>
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-2 text-green">What industries do you specialize in?</h3>
                <p className="text-gray-400">We work across various industries including technology, healthcare, finance, and e-commerce.</p>
              </div>
              <div>
                <h3 className="text-lg font-semibold mb-2 text-green">Can you work with our existing systems?</h3>
                <p className="text-gray-400">Yes, we specialize in integrating with existing systems and can work with your current technology stack.</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Contact;
