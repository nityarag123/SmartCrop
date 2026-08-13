import React from 'react';

const WhatsAppButton = ({ message = "Hello! I need help with weather information.", className = "" }) => {
  const handleWhatsAppClick = () => {
    const phoneNumber = "919876543210"; // Replace with actual WhatsApp business number
    const encodedMessage = encodeURIComponent(message);
    const whatsappUrl = `https://wa.me/${phoneNumber}?text=${encodedMessage}`;
    window.open(whatsappUrl, '_blank');
  };

  return (
    <button
      onClick={handleWhatsAppClick}
      className={`fixed bottom-6 right-6 z-50 w-14 h-14 bg-green-500 hover:bg-green-600 rounded-full shadow-lg transition-all duration-300 flex items-center justify-center group ${className}`}
      aria-label="Contact via WhatsApp"
    >
      <i className="fab fa-whatsapp text-white text-2xl"></i>

      {/* Tooltip */}
      <div className="absolute bottom-full right-0 mb-2 px-3 py-1 bg-gray-800 text-white text-sm rounded-lg opacity-0 group-hover:opacity-100 transition-opacity duration-300 whitespace-nowrap">
        Chat on WhatsApp
        <div className="absolute top-full right-4 w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-gray-800"></div>
      </div>
    </button>
  );
};

export default WhatsAppButton;
