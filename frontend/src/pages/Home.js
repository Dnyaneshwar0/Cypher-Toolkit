import React from 'react';
import FeatureCard from '../components/FeatureCard';
import backgroundImage from '../assets/background.jpg';
import { Link } from 'react-router-dom';

export default function Home() {
  return (
    <div>
      {/* Hero Section */}
      <section
        className="h-screen flex flex-col justify-center items-center text-center px-4 bg-cover bg-center relative"
        style={{ backgroundImage: `url(${backgroundImage})` }}
        >
        <div className="bg-black bg-opacity-60 w-full h-full absolute top-0 left-0"></div>
        <div className="relative z-10 flex flex-col items-center">
            <h1 className="text-5xl font-extrabold text-neon drop-shadow-lg font-orbitron tracking-wider">
            Cypher Toolkit
            </h1>
            <p className="mt-4 text-lg text-gray-400 max-w-xl">
            A futuristic toolkit for learning and experimenting with encryption, encoding, steganography, and more.
            </p>
        </div>

        <a
            href="#features"
            className="absolute bottom-12 left-1/2 transform -translate-x-1/2 px-6 py-3 text-lg bg-gray-900 border-2 border-blue-500 text-gray-300 rounded-full font-semibold hover:shadow-blue-500 hover:bg-gray-800 transition z-10"
        >
            Explore Features
        </a>
      </section>


      {/* Features Section */}
      <section id="features" className="py-20 bg-black">
        <div className="max-w-7xl mx-auto px-4 grid grid-cols-1 md:grid-cols-3 gap-12">
          {/* Left Column */}
          <div className="space-y-14">
            <Link to="/dummy" className='block'>
              <FeatureCard
                title="Text Encryption"
                description="Encrypt and decrypt text using Caesar, Vigenère, and other ciphers."
                gif={backgroundImage}
              />
            </Link>
            <Link to="/steg#" className='block'>
              <FeatureCard
                title="Steganography"
                description="Hide and reveal messages in images. A fun and secretive way to communicate!"
                gif={backgroundImage}
              />
            </Link>
          </div>

          {/* Center Column */}
          <div className="flex flex-col justify-center items-center text-center">
            <h2 className="text-3xl font-bold text-neon mb-4 font-orbitron">
              Your Cipher Playground
            </h2>
            <p className="text-gray-400 max-w-sm">
              Unlock the world of encryption, hidden messages, and fun tools to test and learn cryptographic methods.
            </p>
          </div>

          {/* Right Column */}
          <div className="space-y-14">
            <Link to="/dummy" className='block'>
              <FeatureCard
                title="Base64 Encoding"
                description="Encode or decode messages using Base64 — perfect for web devs and tinkerers."
                gif={backgroundImage}
              />
            </Link>
            <Link to="/dummy" className='block'>
              <FeatureCard
                title="CAPTCHA Generator"
                description="Generate custom CAPTCHAs and test human vs bot recognition."
                gif={backgroundImage}
              />
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
}
