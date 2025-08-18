"use client"

import { useState } from "react"

export default function Encrypt() {
  const [inputText, setInputText] = useState("")
  const [password, setPassword] = useState("")
  const [output, setOutput] = useState("")
  const [selectedAlgorithm, setSelectedAlgorithm] = useState("aes")
  const [selectedMode, setSelectedMode] = useState("encrypt")
  const [file, setFile] = useState(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState("")
  const [rsaKeys, setRsaKeys] = useState({ public: "", private: "" })

  const algorithms = [
    { value: "aes", label: "AES Encryption" },
    { value: "rsa", label: "RSA Encryption" },
    { value: "hybrid", label: "Hybrid Encryption" },
  ]

  const modes = [
    { value: "encrypt", label: "Encrypt" },
    { value: "decrypt", label: "Decrypt" },
  ]

  const handleGenerateKeys = async () => {
    setError("")
    setBusy(true)

    try {
      const res = await fetch("/encrypt/generate-keys", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      })

      if (!res.ok) {
        const errorData = await res.json().catch(() => null)
        throw new Error(errorData?.error || `Request failed with ${res.status}`)
      }

      const data = await res.json()
      setRsaKeys({ public: data.public_key, private: data.private_key })
    } catch (err) {
      setError(err.message || "Failed to generate keys")
    } finally {
      setBusy(false)
    }
  }

  const handleTextOperation = async () => {
    setError("")
    setOutput("")

    if (!inputText.trim()) {
      setError("Please enter text to process.")
      return
    }

    if (selectedAlgorithm === "aes" && !password.trim()) {
      setError("Please enter a password for AES encryption.")
      return
    }

    if (selectedAlgorithm === "rsa" && selectedMode === "encrypt" && !rsaKeys.public) {
      setError("Please generate RSA keys first.")
      return
    }

    if (selectedAlgorithm === "rsa" && selectedMode === "decrypt" && !rsaKeys.private) {
      setError("Please generate RSA keys first.")
      return
    }

    const payload = {
      text: inputText,
      mode: selectedMode,
    }

    if (selectedAlgorithm === "aes") {
      payload.password = password
    } else if (selectedAlgorithm === "rsa") {
      payload.key = selectedMode === "encrypt" ? rsaKeys.public : rsaKeys.private
    } else if (selectedAlgorithm === "hybrid") {
      payload.password = password
    }

    try {
      setBusy(true)
      const res = await fetch(`/encrypt/${selectedAlgorithm}-text`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      })

      if (!res.ok) {
        const errorData = await res.json().catch(() => null)
        throw new Error(errorData?.error || `Request failed with ${res.status}`)
      }

      const data = await res.json()
      setOutput(data.result)
    } catch (err) {
      setError(err.message || "Operation failed")
    } finally {
      setBusy(false)
    }
  }

  const handleFileOperation = async () => {
    setError("")
    setOutput("")

    if (!file) {
      setError("Please select a file.")
      return
    }

    if (selectedAlgorithm === "aes" && !password.trim()) {
      setError("Please enter a password for AES encryption.")
      return
    }

    const form = new FormData()
    form.append("file", file)
    form.append("mode", selectedMode)

    if (selectedAlgorithm === "aes") {
      form.append("password", password)
    } else if (selectedAlgorithm === "rsa") {
      form.append("key", selectedMode === "encrypt" ? rsaKeys.public : rsaKeys.private)
    } else if (selectedAlgorithm === "hybrid") {
      form.append("password", password)
    }

    try {
      setBusy(true)
      const res = await fetch(`/encrypt/${selectedAlgorithm}-file`, {
        method: "POST",
        body: form,
      })

      if (!res.ok) {
        const errorData = await res.json().catch(() => null)
        throw new Error(errorData?.error || `Request failed with ${res.status}`)
      }

      const blob = await res.blob()
      const url = URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = `${selectedMode}ed_${file.name}`
      document.body.appendChild(a)
      a.click()
      a.remove()
      URL.revokeObjectURL(url)

      setOutput(`File ${selectedMode}ed successfully and downloaded.`)
    } catch (err) {
      setError(err.message || "File operation failed")
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="min-h-screen bg-black text-gray-300 px-6 py-12 max-w-7xl mx-auto font-orbitron">
      {/* Header with cryptographic symbols */}
      <div className="relative mb-12">
        <div className="absolute top-0 left-0 w-full h-16 overflow-hidden pointer-events-none">
          <div className="flex space-x-8 text-cyan-400 opacity-30 text-sm animate-pulse">
            {Array.from({ length: 50 }, (_, i) => (
              <span key={i} className="whitespace-nowrap">
                {
                  [
                    "∑",
                    "∆",
                    "Ω",
                    "α",
                    "β",
                    "γ",
                    "δ",
                    "ε",
                    "ζ",
                    "η",
                    "θ",
                    "λ",
                    "μ",
                    "π",
                    "ρ",
                    "σ",
                    "τ",
                    "φ",
                    "χ",
                    "ψ",
                    "ω",
                    "∞",
                    "≡",
                    "⊕",
                    "⊗",
                    "∧",
                    "∨",
                    "¬",
                    "→",
                    "↔",
                  ][Math.floor(Math.random() * 30)]
                }
              </span>
            ))}
          </div>
        </div>
        <h1 className="text-4xl font-bold text-center text-cyan-400 mt-8 mb-4">Text & File Encryption</h1>
        <p className="text-center text-gray-400">Secure your data with advanced cryptographic algorithms</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
        {/* Left Panel - Controls */}
        <div className="space-y-8">
          {/* Algorithm Selection */}
          <div>
            <label className="block mb-3 font-semibold text-cyan-400">Encryption Algorithm</label>
            <select
              value={selectedAlgorithm}
              onChange={(e) => setSelectedAlgorithm(e.target.value)}
              className="w-full p-3 rounded bg-gray-900 border border-cyan-500/30 text-gray-300 font-semibold focus:border-cyan-400 focus:outline-none"
            >
              {algorithms.map((alg) => (
                <option key={alg.value} value={alg.value}>
                  {alg.label}
                </option>
              ))}
            </select>
          </div>

          {/* Mode Selection */}
          <div>
            <label className="block mb-3 font-semibold text-cyan-400">Operation Mode</label>
            <select
              value={selectedMode}
              onChange={(e) => setSelectedMode(e.target.value)}
              className="w-full p-3 rounded bg-gray-900 border border-cyan-500/30 text-gray-300 font-semibold focus:border-cyan-400 focus:outline-none"
            >
              {modes.map((mode) => (
                <option key={mode.value} value={mode.value}>
                  {mode.label}
                </option>
              ))}
            </select>
          </div>

          {/* RSA Key Generation */}
          {selectedAlgorithm === "rsa" && (
            <div className="bg-gray-900/50 p-4 rounded border border-cyan-500/20">
              <h3 className="text-cyan-400 font-semibold mb-3">RSA Key Management</h3>
              <button
                onClick={handleGenerateKeys}
                disabled={busy}
                className="w-full px-4 py-2 rounded bg-cyan-600 hover:bg-cyan-700 text-white font-semibold transition-colors disabled:bg-gray-700"
              >
                {busy ? "Generating..." : "Generate RSA Keys"}
              </button>
              {rsaKeys.public && <div className="mt-3 text-xs text-green-400">✓ RSA keys generated successfully</div>}
            </div>
          )}

          {/* Password Input */}
          {(selectedAlgorithm === "aes" || selectedAlgorithm === "hybrid") && (
            <div>
              <label className="block mb-3 font-semibold text-cyan-400">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="Enter encryption password"
                className="w-full p-3 rounded bg-gray-900 border border-cyan-500/30 text-gray-300 focus:border-cyan-400 focus:outline-none"
              />
            </div>
          )}

          {/* Text Input */}
          <div>
            <label className="block mb-3 font-semibold text-cyan-400">Text Input</label>
            <textarea
              value={inputText}
              onChange={(e) => setInputText(e.target.value)}
              placeholder="Enter text to encrypt/decrypt"
              rows={6}
              className="w-full p-3 rounded bg-gray-900 border border-cyan-500/30 text-gray-300 focus:border-cyan-400 focus:outline-none resize-none"
            />
            <button
              onClick={handleTextOperation}
              disabled={busy}
              className="w-full mt-3 px-6 py-3 rounded bg-blue-600 hover:bg-blue-700 text-white font-bold transition-colors disabled:bg-gray-700"
            >
              {busy ? "Processing..." : `${selectedMode.charAt(0).toUpperCase() + selectedMode.slice(1)} Text`}
            </button>
          </div>

          {/* File Input */}
          <div>
            <label className="block mb-3 font-semibold text-cyan-400">File Input</label>
            <input
              type="file"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="w-full p-3 rounded bg-gray-900 border border-cyan-500/30 text-gray-300 file:mr-4 file:py-2 file:px-4 file:rounded file:border-0 file:bg-cyan-600 file:text-white"
            />
            <button
              onClick={handleFileOperation}
              disabled={busy || !file}
              className="w-full mt-3 px-6 py-3 rounded bg-green-600 hover:bg-green-700 text-white font-bold transition-colors disabled:bg-gray-700"
            >
              {busy ? "Processing..." : `${selectedMode.charAt(0).toUpperCase() + selectedMode.slice(1)} File`}
            </button>
          </div>
        </div>

        {/* Right Panel - Output */}
        <div className="space-y-6">
          <div>
            <label className="block mb-3 font-semibold text-cyan-400">Output</label>
            <div className="bg-gray-900 rounded border border-cyan-500/30 p-4 min-h-[400px] overflow-auto">
              {error ? (
                <div className="text-red-400 text-sm">{error}</div>
              ) : output ? (
                <div className="text-gray-300 whitespace-pre-wrap break-all text-sm">{output}</div>
              ) : (
                <div className="text-gray-500 text-center mt-20">Output will appear here after processing</div>
              )}
            </div>
          </div>

          {/* RSA Keys Display */}
          {selectedAlgorithm === "rsa" && (rsaKeys.public || rsaKeys.private) && (
            <div className="space-y-4">
              {rsaKeys.public && (
                <div>
                  <label className="block mb-2 text-sm font-semibold text-cyan-400">Public Key</label>
                  <textarea
                    value={rsaKeys.public}
                    readOnly
                    rows={4}
                    className="w-full p-2 rounded bg-gray-900 border border-cyan-500/20 text-gray-400 text-xs resize-none"
                  />
                </div>
              )}
              {rsaKeys.private && (
                <div>
                  <label className="block mb-2 text-sm font-semibold text-cyan-400">Private Key</label>
                  <textarea
                    value={rsaKeys.private}
                    readOnly
                    rows={4}
                    className="w-full p-2 rounded bg-gray-900 border border-cyan-500/20 text-gray-400 text-xs resize-none"
                  />
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
