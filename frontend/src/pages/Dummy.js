"use client"
import React from "react"

export default function Dummy() {
  return (
    <div className="min-h-screen bg-black text-gray-300 px-6 py-12 max-w-7xl mx-auto font-orbitron">
      {/* Symbolic Header */}
      <div className="relative mb-12">
        <div className="absolute top-0 left-0 w-full h-16 overflow-hidden pointer-events-none">
          <div className="flex space-x-8 text-cyan-400 opacity-30 text-sm animate-pulse">
            {Array.from({ length: 50 }, (_, i) => (
              <span key={i} className="whitespace-nowrap mt-12">
                {"∑∆Ωαβγδεζηθλμπρστω∞≡⊕⊗∧∨¬→↔".charAt(Math.floor(Math.random() * 20))}
              </span>
            ))}
          </div>
        </div>
        <h1 className="text-4xl font-bold text-center text-cyan-400 mt-0 mb-12">Dummy Page</h1>
        <p className="text-center text-gray-400">This section is under construction</p>
      </div>

      {/* Centered Message */}
      <div className="flex items-center justify-center h-[50vh]">
        <div className="text-3xl text-cyan-300 font-semibold border border-cyan-500/30 p-8 rounded bg-gray-900 shadow shadow-cyan-500/20">
          Coming Soon...
        </div>
      </div>
    </div>
  )
}
