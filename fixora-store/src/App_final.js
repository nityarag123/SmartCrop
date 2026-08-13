import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './App.css';

// Import all page components
import Header from './components/Header';
import Footer from './components/Footer';
import WhatsAppButton from './components/WhatsAppButton';
import Home from './pages/Home';
import About from './pages/About';
import Services from './pages/Services';
import Products from './pages/Products';
import Contact from './pages/Contact';
import Blog from './pages/Blog';
import Portfolio from './pages/Portfolio';
import Team from './pages/Team';
import Weather from './pages/Weather';
import Careers from './pages/Careers';
import Testimonials from './pages/Testimonials';
import FAQ from './pages/FAQ';
import PrivacyPolicy from './pages/PrivacyPolicy';
import TermsOfService from './pages/TermsOfService';
import Sitemap from './pages/Sitemap';
import Industries from './pages/Industries';
import CaseStudies from './pages/CaseStudies';
import Resources from './pages/Resources';
import Events from './pages/Events';
import News from './pages/News';
import Partners from './pages/Partners';
import Investors from './pages/Investors';
import Sustainability from './pages/Sustainability';
import Quality from './pages/Quality';
import Certifications from './pages/Certifications';
import Awards from './pages/Awards';
import PressReleases from './pages/PressReleases';

function App() {
  return (
    <Router>
      <div className="App">
        <Header />
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
            <Route path="/services" element={<Services />} />
            <Route path="/products" element={<Products />} />
            <Route path="/contact" element={<Contact />} />
            <Route path="/blog" element={<Blog />} />
            <Route path="/portfolio" element={<Portfolio />} />
            <Route path="/team" element={<Team />} />
            <Route path="/weather" element={<Weather />} />
            <Route path="/careers" element={<Careers />} />
            <Route path="/testimonials" element={<Testimonials />} />
            <Route path="/faq" element={<FAQ />} />
            <Route path="/privacy-policy" element={<PrivacyPolicy />} />
            <Route path="/terms-of-service" element={<TermsOfService />} />
            <Route path="/sitemap" element={<Sitemap />} />
            <Route path="/industries" element={<Industries />} />
            <Route path="/case-studies" element={<CaseStudies />} />
            <Route path="/resources" element={<Resources />} />
            <Route path="/events" element={<Events />} />
            <Route path="/news" element={<News />} />
            <Route path="/partners" element={<Partners />} />
            <Route path="/investors" element={<Investors />} />
            <Route path="/sustainability" element={<Sustainability />} />
            <Route path="/quality" element={<Quality />} />
            <Route path="/certifications" element={<Certifications />} />
            <Route path="/awards" element={<Awards />} />
            <Route path="/press-releases" element={<PressReleases />} />
          </Routes>
        </main>
        <Footer />
        <WhatsAppButton />
      </div>
    </Router>
  );
}

export default App;
