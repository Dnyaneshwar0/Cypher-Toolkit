"use client"

import { useEffect, useState, useRef } from "react"
import FeatureCard from "../components/FeatureCard"
import { Link } from "react-router-dom"

export default function Home() {
  const [isLoaded, setIsLoaded] = useState(false)
  const [visibleCards, setVisibleCards] = useState([])
  const [mousePosition, setMousePosition] = useState({ x: 0, y: 0 })
  const [matrixCode, setMatrixCode] = useState([])
  const heroRef = useRef(null)

  useEffect(() => {
    setIsLoaded(true)
    const timer = setTimeout(() => {
      setVisibleCards([0, 1, 2, 3])
    }, 500)

    const initialMatrix = Array.from({ length: 40 }, (_, i) => ({
      id: i,
      x: i * (window.innerWidth / 40),
      characters: Array.from({ length: 25 }, () => (Math.random() > 0.5 ? "1" : "0")),
      speed: Math.random() * 3 + 2,
      opacity: Math.random() * 0.7 + 0.4,
    }))
    setMatrixCode(initialMatrix)

    return () => clearTimeout(timer)
  }, [])

  useEffect(() => {
    const handleMouseMove = (e) => {
      setMousePosition({ x: e.clientX, y: e.clientY })
    }

    window.addEventListener("mousemove", handleMouseMove)
    return () => window.removeEventListener("mousemove", handleMouseMove)
  }, [])

  useEffect(() => {
    const animateMatrix = () => {
      setMatrixCode((prev) =>
        prev.map((stream) => ({
          ...stream,
          characters: stream.characters.map(() =>
            Math.random() > 0.6
              ? Math.random() > 0.5
                ? "1"
                : "0"
              : stream.characters[Math.floor(Math.random() * stream.characters.length)],
          ),
        })),
      )
    }

    const matrixInterval = setInterval(animateMatrix, 120)

    return () => {
      clearInterval(matrixInterval)
    }
  }, [])

  const handleExploreClick = (e) => {
    e.preventDefault()
    document.getElementById("features").scrollIntoView({
      behavior: "smooth",
      block: "start",
    })
  }

  return (
    <div>
      {/* Hero Section */}
      <section
        ref={heroRef}
        className="h-screen flex flex-col justify-center items-center text-center px-4 relative overflow-hidden"
        style={{
          backgroundImage: `url('/data/images/encrypt/img1.png')`,
          backgroundSize: "cover",
          backgroundPosition: "center",
          backgroundRepeat: "no-repeat",
        }}
      >
        <div className="absolute inset-0 pointer-events-none">
          {matrixCode.map((stream) => (
            <div
              key={stream.id}
              className="absolute top-0 text-green-400 text-sm font-mono leading-tight font-bold"
              style={{
                left: `${stream.x}px`,
                opacity: stream.opacity,
                animation: `matrix-fall ${8 + stream.speed}s linear infinite`,
                textShadow: "0 0 8px rgba(34, 197, 94, 0.8)",
                filter: "brightness(1.2)",
              }}
            >
              {stream.characters.map((char, index) => (
                <div key={index} className="animate-pulse">
                  {char}
                </div>
              ))}
            </div>
          ))}
        </div>

        <div
          className="absolute inset-0 transition-all duration-300"
          style={{
            background: `radial-gradient(800px circle at ${mousePosition.x}px ${mousePosition.y}px, rgba(59, 130, 246, 0.15), rgba(0,0,0,0.7))`,
          }}
        ></div>

        <div
          className={`relative z-10 flex flex-col items-center transition-all duration-1000 ${isLoaded ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}
        >
          <h1
            className="text-5xl md:text-6xl lg:text-7xl font-extrabold text-blue-400 drop-shadow-lg font-orbitron tracking-wider relative"
            style={{
              textShadow: `0 0 30px rgba(59, 130, 246, 0.8), 0 0 60px rgba(59, 130, 246, 0.5)`
            }}
          >
            Cypher Toolkit
            {/* <span
              className="absolute inset-0 text-cyan-300 opacity-40 animate-ping"
              style={{ animationDuration: "3s" }}
            >
              Cypher Toolkit
            </span> */}
          </h1>
          <p className="mt-4 text-lg md:text-xl text-gray-300 max-w-xl leading-relaxed">
            A futuristic toolkit for learning and experimenting with encryption, encoding, steganography, and more.
          </p>
        </div>

        <div className="absolute bottom-12 left-1/2 transform -translate-x-1/2 z-10">
          <button
            onClick={handleExploreClick}
            className="px-8 py-4 text-lg bg-gray-900 border-2 border-blue-500 text-blue-300 rounded-full font-semibold hover:shadow-lg hover:shadow-blue-500/50 hover:bg-gray-800 hover:border-blue-400 transition-all duration-300 group relative overflow-hidden"
            style={{
              boxShadow: `0 0 20px rgba(59, 130, 246, ${0.4 + Math.sin(Date.now() / 1000) * 0.3})`,
            }}
          >
            <div className="absolute inset-0 bg-gradient-to-r from-blue-600 to-cyan-400 opacity-0 group-hover:opacity-20 transition-opacity duration-300"></div>
            <span className="group-hover:animate-bounce inline-block relative z-10">Explore Features</span>
          </button>
        </div>
      </section>

      {/* Features Section */}
      <section
        id="features"
        className="py-20 relative"
        style={{
          backgroundImage: `url('/data/images/encrypt/img1.png')`,
          backgroundSize: "cover",
          backgroundPosition: "center",
          backgroundRepeat: "no-repeat",
        }}
      >
        <div className="absolute inset-0 bg-black bg-opacity-70"></div>

        <div className="absolute inset-0 opacity-5">
          <div
            className="w-full h-full"
            style={{
              backgroundImage: `radial-gradient(circle at 25% 25%, #3b82f6 0%, transparent 50%), radial-gradient(circle at 75% 75%, #06b6d4 0%, transparent 50%)`,
              backgroundSize: "100px 100px",
            }}
          ></div>
        </div>

        <div className="max-w-7xl mx-auto px-4 grid grid-cols-1 md:grid-cols-3 gap-12 relative z-10">
          {/* Left Column */}
          <div className="space-y-14">
            <div
              className={`transition-all duration-700 delay-100 ${visibleCards.includes(0) ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}
            >
              <Link to="/encrypt#" className="block">
                <FeatureCard
                  title="Text Encryption"
                  description="Encrypt and decrypt text using Caesar, Vigenère, and other ciphers."
                />
              </Link>
            </div>
            <div
              className={`transition-all duration-700 delay-300 ${visibleCards.includes(1) ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}
            >
              <Link to="/steg#" className="block">
                <FeatureCard
                  title="Steganography"
                  description="Hide and reveal messages in images. A fun and secretive way to communicate!"
                />
              </Link>
            </div>
          </div>

          {/* Center Column */}
          <div
            className={`flex flex-col justify-center items-center text-center transition-all duration-700 delay-200 ${visibleCards.length > 0 ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}
          >
            <h2 className="text-3xl md:text-4xl font-bold text-blue-400 mb-4 font-orbitron">Your Cipher Playground</h2>
            <p className="text-gray-300 max-w-sm leading-relaxed">
              Unlock the world of encryption, hidden messages, and fun tools to test and learn cryptographic methods.
            </p>
            <div className="mt-6 w-16 h-1 bg-gradient-to-r from-blue-500 to-cyan-300 rounded-full animate-pulse relative overflow-hidden">
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-cyan-200 to-transparent opacity-50 animate-ping"></div>
            </div>
          </div>

          {/* Right Column */}
          <div className="space-y-14">
            <div
              className={`transition-all duration-700 delay-400 ${visibleCards.includes(2) ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}
            >
              <Link to="/dummy" className="block">
                <FeatureCard
                  title="Base64 Encoding"
                  description="Encode or decode messages using Base64 — perfect for web devs and tinkerers."
                />
              </Link>
            </div>
            <div
              className={`transition-all duration-700 delay-500 ${visibleCards.includes(3) ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"}`}
            >
              <Link to="/dummy" className="block">
                <FeatureCard
                  title="CAPTCHA Generator"
                  description="Generate custom CAPTCHAs and test human vs bot recognition."
                />
              </Link>
            </div>
          </div>
        </div>
      </section>

      <style jsx>{`
        @keyframes matrix-fall {
          0% { transform: translateY(-100vh); }
          100% { transform: translateY(100vh); }
        }
      `}</style>
    </div>
  )
}
