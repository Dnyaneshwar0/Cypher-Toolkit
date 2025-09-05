"use client"
import React, { useEffect, useMemo, useState } from 'react';

export default function Steg() {
  const [file1, setFile1] = useState(null);
  const [file2, setFile2] = useState(null);
  const [output, setOutput] = useState(null); // { url, filename, kind: 'image'|'text' }
  const [selectedOption, setSelectedOption] = useState('encode');
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState('');

  const preview1 = useMemo(() => (file1 ? URL.createObjectURL(file1) : null), [file1]);
  const preview2 = useMemo(() => (file2 ? URL.createObjectURL(file2) : null), [file2]);

  useEffect(() => () => {
    if (preview1) URL.revokeObjectURL(preview1);
    if (preview2) URL.revokeObjectURL(preview2);
  }, [preview1, preview2]);

  useEffect(() => {
    return () => {
      if (output?.url) URL.revokeObjectURL(output.url);
    };
  }, [output?.url]);

  const options = [
    { value: 'encode', label: 'Encode' },
    { value: 'decode', label: 'Decode' },
    { value: 'diffmap', label: 'Generate Diff Map' },
    { value: 'diffmap', label: 'Generate Diff Map' },
  ];

  const handleConvert = async () => {
    setError('');
    setOutput(null);

    if ((selectedOption === 'encode' || selectedOption === 'diffmap') && (!file1 || !file2)) {
      setError('Please upload two files.');
      return;
    }
    if (selectedOption === 'decode' && !file1) {
      setError('Please upload a file.');
    if (selectedOption === 'decode' && !file1) {
      setError('Please upload a file.');
      return;
    }

    const form = new FormData();
    let url = '';
    let expectedFilename = '';

    if (selectedOption === 'encode') {
      form.append('carrier', file1);
      form.append('secret', file2);
      url = '/steg/encode';
      expectedFilename = 'encoded_output.png';
    } else if (selectedOption === 'decode') {
      form.append('encoded', file1);
      url = '/steg/decode';
      expectedFilename = 'decoded_output.png';
    } else {
      form.append('original', file1);
      form.append('encoded', file2);
      url = '/steg/diff';
      expectedFilename = 'diff_map.png';
    }

    try {
      setBusy(true);
      const res = await fetch(url, {
        method: 'POST',
        body: form,
      });

      if (!res.ok) {
        const maybeJson = await res.json().catch(() => null);
        throw new Error(maybeJson?.error || `Request failed with ${res.status}`);
      }

      const blob = await res.blob();
      const objectUrl = URL.createObjectURL(blob);
      setOutput({ url: objectUrl, filename: expectedFilename, kind: 'image', blob });
    } catch (err) {
      setError(err.message || 'Something went wrong');
    } finally {
      setBusy(false);
    }
  };

    const form = new FormData();
    let url = '';
    let expectedFilename = '';

    if (selectedOption === 'encode') {
      form.append('carrier', file1);
      form.append('secret', file2);
      url = '/steg/encode';   // 🔹 updated
      expectedFilename = 'encoded_output.png';
    } else if (selectedOption === 'decode') {
      form.append('encoded', file1);
      url = '/steg/decode';   // 🔹 updated
      expectedFilename = 'decoded_output.png';
    } else {
      form.append('original', file1);
      form.append('encoded', file2);
      url = '/steg/diff';     // 🔹 updated
      expectedFilename = 'diff_map.png';
    }


    try {
      setBusy(true);
      const res = await fetch(url, {
        method: 'POST',
        body: form,
      });

      if (!res.ok) {
        const maybeJson = await res.json().catch(() => null);
        throw new Error(maybeJson?.error || `Request failed with ${res.status}`);
      }

      // The backend returns PNG images for all three routes.
      const blob = await res.blob();
      const objectUrl = URL.createObjectURL(blob);

      setOutput({ url: objectUrl, filename: expectedFilename, kind: 'image', blob });
    } catch (err) {
      setError(err.message || 'Something went wrong');
    } finally {
      setBusy(false);
    }
  };

  const handleDownload = () => {
    if (!output) return;
    const a = document.createElement('a');
    a.href = output.url;
    a.download = output.filename || 'output.bin';
    document.body.appendChild(a);
    a.click();
    a.remove();
  };

  // Revoke previous output URL when output changes/unmount
  useEffect(() => {
    return () => {
      if (output?.url) URL.revokeObjectURL(output.url);
    };
  }, [output?.url]);

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
        <h1 className="text-4xl font-bold text-center text-cyan-400 mt-0 mb-12">Steganography Tools</h1>
        <p className="text-center text-gray-400">Hide, extract, and compare hidden information in images</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-[1.3fr_0.4fr_1.3fr] gap-12">
        {/* File Inputs */}
        <div className="space-y-8">
          <div>
            <label className="block mb-2 font-semibold text-cyan-400">Upload File 1</label>
            <input
              type="file"
              accept="image/*"
              onChange={(e) => setFile1(e.target.files?.[0] || null)}
              className="w-full p-3 rounded bg-gray-900 border border-cyan-500/30 text-gray-300
              file:mr-4 file:py-2 file:px-4 file:rounded file:border-0
              file:bg-cyan-600 file:text-white file:cursor-pointer"
            />

            {preview1 && (
              <div className="mt-3 border border-cyan-500/20 rounded p-2">
                <img src={preview1} alt="preview 1" className="max-w-full rounded" />
              </div>
            )}
          </div>

          {(selectedOption === 'encode' || selectedOption === 'diffmap') && (
            <div>
              <label className="block mb-2 font-semibold text-cyan-400">Upload File 2</label>
              <input
                type="file"
                accept="image/*"
                onChange={(e) => setFile2(e.target.files?.[0] || null)}
                className="w-full p-3 rounded bg-gray-900 border border-cyan-500/30 text-gray-300
                file:mr-4 file:py-2 file:px-4 file:rounded file:border-0
                file:bg-cyan-600 file:text-white file:cursor-pointer"
              />

              {preview2 && (
                <div className="mt-3 border border-cyan-500/20 rounded p-2">
                  <img src={preview2} alt="preview 2" className="max-w-full rounded" />
                </div>
              )}
            </div>
          )}
        </div>

        {/* Center Controls */}
        {/* <div className="flex flex-col justify-center items-center space-y-6"> */}
        <div className="flex flex-col justify-center items-center mx-auto space-y-6">
          <select
            value={selectedOption}
            onChange={(e) => setSelectedOption(e.target.value)}
            className="w-full p-3 rounded bg-gray-900 border border-cyan-500/30 text-gray-300 font-semibold focus:border-cyan-400"
          >
            {options.map((opt) => (
              <option key={opt.value} value={opt.value}>
                {opt.label}
              </option>
            ))}
          </select>

          <button
            onClick={handleConvert}
            disabled={busy}
            className="w-full px-6 py-3 rounded bg-blue-600 hover:bg-blue-700 text-white font-bold transition-colors disabled:bg-gray-700"
          >
            {busy ? 'Processing…' : 'Convert'}
          </button>

          {error && <div className="text-red-400 text-sm">{error}</div>}
        </div>

        {/* Output Preview */}
        <div className="space-y-6">
          <div>
            <label className="block mb-2 font-semibold text-cyan-400">Output Preview</label>
            <div className="bg-gray-900 rounded border border-cyan-500/30 p-4 min-h-[300px] flex items-center justify-center">
              {!output ? (
                <span className="text-gray-500 text-sm">Output will appear here after processing</span>
              ) : output.kind === 'image' ? (
                <img src={output.url} alt="output" className="max-w-full max-h-full rounded" />
              ) : (
                <span className="text-gray-500 text-sm">Unsupported output</span>
              )}
            </div>
          </div>

          <button
            onClick={handleDownload}
            disabled={!output}
            className="w-full px-6 py-3 rounded bg-green-600 hover:bg-green-700 text-white font-semibold transition-colors disabled:bg-gray-700"
          >
            Download Output
          </button>
        </div>
      </div>
    </div>
  );
}