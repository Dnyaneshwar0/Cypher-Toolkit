import React, { useState, useEffect } from "react";

export default function Captcha() {
  const [mode, setMode] = useState("generate"); // generate | solve
  const [capId, setCapId] = useState("");
  const [imageUrl, setImageUrl] = useState("");
  const [input, setInput] = useState("");
  const [result, setResult] = useState("");
  const [ocrResult, setOcrResult] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function createCaptcha() {
    try {
      setBusy(true);
      setError("");
      setResult("");
      setOcrResult("");
      setInput("");

      const res = await fetch("/captcha/generate?len=6");
      if (!res.ok) throw new Error(`Generate failed: ${res.status}`);
      const data = await res.json();

      setCapId(data.id);
      setImageUrl(data.image_url); // e.g. /captcha/image/<id>
    } catch (e) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }

  async function verifyCaptcha() {
    try {
      setBusy(true);
      setError("");
      const res = await fetch("/captcha/verify", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: capId, text: input }),
      });
      if (!res.ok) throw new Error(`Verify failed: ${res.status}`);
      const data = await res.json();
      setResult(data.ok ? "✅ Correct!" : "❌ Incorrect, try again.");
    } catch (e) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }

  async function solveWithOCR() {
    try {
      setBusy(true);
      setError("");
      const res = await fetch("/captcha/solve", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id: capId }),
      });
      if (!res.ok) throw new Error(`Solve failed: ${res.status}`);
      const data = await res.json();
      setOcrResult(data.text || "(no text)");
    } catch (e) {
      setError(e.message);
    } finally {
      setBusy(false);
    }
  }

  // auto-generate one when page opens
  useEffect(() => {
    createCaptcha();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="min-h-screen bg-black text-gray-300 px-6 py-12 max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-12 font-orbitron">

      {/* Left: Captcha display */}
      <div className="flex flex-col items-center justify-center space-y-6">
        <div className="bg-gray-900 border border-gray-700 rounded-lg p-6 flex items-center justify-center min-h-[120px] min-w-[320px]">
          {imageUrl ? (
            <img
              src={imageUrl + `?t=${capId}`} // bust cache
              alt="captcha"
              className="rounded max-h-[140px]"
            />
          ) : (
            <div className="text-gray-500">No Captcha</div>
          )}
        </div>

        <button
          onClick={createCaptcha}
          disabled={busy}
          className={`px-6 py-2 rounded text-white font-semibold ${busy ? "bg-gray-700 cursor-wait" : "bg-blue-600 hover:bg-blue-700"}`}
        >
          Generate Captcha
        </button>
      </div>

      {/* Middle: Dropdown */}
      <div className="flex flex-col justify-center items-center space-y-6">
        <select
          value={mode}
          onChange={(e) => { setMode(e.target.value); setResult(""); setOcrResult(""); }}
          className="w-56 p-3 rounded bg-gray-900 border border-gray-700 text-gray-300 font-semibold text-center text-lg cursor-pointer"
        >
          <option value="generate">Captcha Generation</option>
          <option value="solve">Captcha Solver</option>
        </select>
        {error && <div className="text-red-400 text-sm">{error}</div>}
      </div>

      {/* Right: Guess/Solve */}
      <div className="flex flex-col justify-center items-center space-y-6">
        {mode === "generate" ? (
          <>
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              className="w-56 p-2 rounded bg-gray-900 border border-gray-700 text-gray-200 text-center"
              placeholder="Enter captcha"
              disabled={!capId || busy}
            />
            <button
              onClick={verifyCaptcha}
              disabled={!capId || busy}
              className={`px-6 py-2 rounded text-white font-semibold ${busy ? "bg-gray-700 cursor-wait" : "bg-green-600 hover:bg-green-700"}`}
            >
              Submit
            </button>
            {result && <div className="text-lg font-bold">{result}</div>}
          </>
        ) : (
          <>
            <button
              onClick={solveWithOCR}
              disabled={!capId || busy}
              className={`px-6 py-2 rounded text-white font-semibold ${busy ? "bg-gray-700 cursor-wait" : "bg-purple-600 hover:bg-purple-700"}`}
            >
              Solve with OCR
            </button>
            {ocrResult && (
              <div className="text-2xl font-bold text-yellow-400">{ocrResult}</div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
