"use client"

import { useState } from "react"

function FeatureCard({ title, description, gif }) {
  const [isHovered, setIsHovered] = useState(false)

  return (
    <div
      className="bg-gray-900 p-6 rounded-xl cursor-pointer transform transition-all duration-500 min-h-[320px] flex flex-col border-2 relative overflow-hidden group"
      style={{
        borderColor: isHovered ? "#00ffff" : "#3b82f6",
        boxShadow: isHovered
          ? "0 0 40px rgba(0, 255, 255, 0.6), 0 0 80px rgba(0, 255, 255, 0.3), inset 0 0 20px rgba(0, 255, 255, 0.1)"
          : "0 0 20px rgba(59, 130, 246, 0.4), 0 0 40px rgba(59, 130, 246, 0.2)",
        transform: isHovered ? "scale(1.08) translateY(-8px)" : "scale(1)",
        background: isHovered
          ? "linear-gradient(135deg, rgba(17, 24, 39, 0.95), rgba(31, 41, 55, 0.95))"
          : "rgba(17, 24, 39, 0.9)",
      }}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div
        className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-32 h-32 opacity-0 group-hover:opacity-30 transition-all duration-500 rounded-full"
        style={{
          background:
            "radial-gradient(circle, rgba(0, 255, 255, 0.4) 0%, rgba(59, 130, 246, 0.2) 50%, transparent 70%)",
          animation: isHovered ? "pulse 2s infinite" : "none",
          filter: "blur(20px)",
        }}
      ></div>

      <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-500">
        <div
          className="absolute top-4 left-4 w-1 h-1 bg-cyan-400 rounded-full animate-ping"
          style={{ animationDelay: "0s" }}
        ></div>
        <div
          className="absolute top-8 right-6 w-1 h-1 bg-blue-400 rounded-full animate-ping"
          style={{ animationDelay: "0.5s" }}
        ></div>
        <div
          className="absolute bottom-6 left-8 w-1 h-1 bg-cyan-300 rounded-full animate-ping"
          style={{ animationDelay: "1s" }}
        ></div>
        <div
          className="absolute bottom-4 right-4 w-1 h-1 bg-blue-300 rounded-full animate-ping"
          style={{ animationDelay: "1.5s" }}
        ></div>
      </div>

      <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
        <div className="absolute top-0 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-cyan-400 to-transparent animate-pulse"></div>
        <div
          className="absolute bottom-0 left-0 w-full h-0.5 bg-gradient-to-r from-transparent via-blue-400 to-transparent animate-pulse"
          style={{ animationDelay: "1s" }}
        ></div>
        <div
          className="absolute left-0 top-0 w-0.5 h-full bg-gradient-to-b from-transparent via-cyan-400 to-transparent animate-pulse"
          style={{ animationDelay: "0.5s" }}
        ></div>
        <div
          className="absolute right-0 top-0 w-0.5 h-full bg-gradient-to-b from-transparent via-blue-400 to-transparent animate-pulse"
          style={{ animationDelay: "1.5s" }}
        ></div>
      </div>

      <div className="relative z-10">
        {gif && (
          <img
            src={gif || "/placeholder.svg"}
            alt={title}
            className="w-full h-40 object-cover rounded-md mb-4 transition-all duration-300"
            style={{
              filter: isHovered ? "brightness(1.2) contrast(1.1)" : "brightness(1)",
              boxShadow: isHovered ? "0 0 20px rgba(0, 255, 255, 0.3)" : "none",
            }}
          />
        )}

        <h3
          className="text-xl font-bold mb-3 transition-all duration-300"
          style={{
            color: isHovered ? "#00ffff" : "#3b82f6",
            textShadow: isHovered
              ? "0 0 20px rgba(0, 255, 255, 0.8), 0 0 40px rgba(0, 255, 255, 0.4)"
              : "0 0 10px rgba(59, 130, 246, 0.6)",
            filter: `brightness(${isHovered ? 1.4 : 1.1})`,
          }}
        >
          {title}
        </h3>

        <p
          className="flex-grow transition-all duration-300"
          style={{
            color: isHovered ? "#e5e7eb" : "#9ca3af",
            textShadow: isHovered ? "0 0 8px rgba(229, 231, 235, 0.3)" : "none",
            filter: `brightness(${isHovered ? 1.2 : 1})`,
          }}
        >
          {description}
        </p>
      </div>
    </div>
  )
}

export default FeatureCard
