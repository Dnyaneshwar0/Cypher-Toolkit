import React from 'react';

function FeatureCard({ title, description, gif }) {
  return (
    //<div className="bg-gray-900 p-6 rounded-xl shadow-glow hover:scale-105 transform transition-all duration-300 border border-neon">
      <div className="bg-gray-900 p-4 rounded-xl shadow-glow cursor-pointer transform transition duration-300 hover:scale-105 hover:shadow-neon min-h-[320px] flex flex-col border border-neon">
      {gif && (
        <img
          src={gif}
          alt={title}
          className="w-full h-40 object-cover rounded-md mb-4"
        />
      )}
        <h3 className="text-xl font-bold mb-2 text-neon">{title}</h3>
        <p className="text-gray-400 flex-grow">{description}</p>
    </div>

  );
}

export default FeatureCard;

//    <div className="bg-gray-900 rounded-xl shadow-lg p-6 cursor-pointer transform transition hover:scale-105 hover:shadow-neon min-h-[220px] flex flex-col">

//      <h3 className="text-xl font-bold text-neon mb-2">{title}</h3>
//      <p className="text-gray-300 text-sm">{description}</p>
//    </div>