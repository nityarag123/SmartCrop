import React from 'react';
import { Link } from 'react-router-dom';

const Blog = () => {
  const blogPosts = [
    {
      title: 'The Future of Web Development in 2024',
      excerpt: 'Exploring the latest trends and technologies shaping the web development landscape.',
      date: 'March 15, 2024',
      readTime: '5 min read',
      category: 'Technology'
    },
    {
      title: 'Digital Transformation: A Complete Guide',
      excerpt: 'Learn how businesses can successfully navigate their digital transformation journey.',
      date: 'March 10, 2024',
      readTime: '8 min read',
      category: 'Business'
    },
    {
      title: 'Cybersecurity Best Practices for Modern Businesses',
      excerpt: 'Essential security measures every business should implement to protect their data.',
      date: 'March 5, 2024',
      readTime: '6 min read',
      category: 'Security'
    }
  ];

  return (
    <div>
      <section className="hero">
        <div className="container mx-auto px-4">
          <div className="hero-content text-center">
            <h1 className="text-5xl md:text-7xl font-bold mb-6 text-gradient">Blog</h1>
            <p className="text-xl md:text-2xl text-gray-300 mb-8 max-w-3xl mx-auto">
              Insights, trends, and expert advice on technology and business.
            </p>
          </div>
        </div>
      </section>

      <section className="section bg-darker">
        <div className="container mx-auto px-4">
          <div className="grid-3">
            {blogPosts.map((post, index) => (
              <article key={index} className="card">
                <h2 className="text-xl font-semibold mb-3 text-green">{post.title}</h2>
                <p className="text-gray-400 mb-4">{post.excerpt}</p>
                <div className="flex justify-between items-center text-sm text-gray-500 mb-4">
                  <span>{post.date}</span>
                  <span>{post.readTime}</span>
                </div>
                <span className="inline-block px-3 py-1 bg-green text-black text-sm rounded-full mb-4">
                  {post.category}
                </span>
                <Link to="#" className="text-green hover:text-white transition-colors">
                  Read More <i className="fas fa-arrow-right ml-2"></i>
                </Link>
              </article>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
};

export default Blog;
