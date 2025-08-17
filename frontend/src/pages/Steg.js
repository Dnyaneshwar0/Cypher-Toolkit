// steg.js
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

  const options = [
    { value: 'encode', label: 'Encode' },
    { value: 'decode', label: 'Decode' },
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
      return;
    }

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
    // Do NOT revoke here immediately; user agent may still read. Revoke on next change/unmount:
    // URL.revokeObjectURL(output.url);
  };

  // Revoke previous output URL when output changes/unmount
  useEffect(() => {
    return () => {
      if (output?.url) URL.revokeObjectURL(output.url);
    };
  }, [output?.url]);

  return (
    <div className="min-h-screen bg-black text-gray-300 px-6 py-12 max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-12 font-orbitron">
      {/* File inputs */}
      <div className="space-y-10">
        <div>
          <label className="block mb-2 font-semibold text-neon">Upload File 1</label>
          <input
            type="file"
            accept="image/*"
            onChange={e => setFile1(e.target.files?.[0] || null)}
            className="w-full p-2 rounded bg-gray-900 border border-gray-700 text-gray-300"
          />
          {preview1 && (
            <div className="mt-4 border border-gray-700 rounded p-2 flex justify-center items-center">
              <img src={preview1} alt="preview 1" className="max-w-full rounded" />
            </div>
          )}
        </div>

        {(selectedOption === 'encode' || selectedOption === 'diffmap') && (
          <div>
            <label className="block mb-2 font-semibold text-neon">Upload File 2</label>
            <input
              type="file"
              accept="image/*"
              onChange={e => setFile2(e.target.files?.[0] || null)}
              className="w-full p-2 rounded bg-gray-900 border border-gray-700 text-gray-300"
            />
            {preview2 && (
              <div className="mt-4 border border-gray-700 rounded p-2 flex justify-center items-center">
                <img src={preview2} alt="preview 2" className="max-w-full rounded" />
              </div>
            )}
          </div>
        )}
      </div>

      {/* Center controls */}
      <div className="flex flex-col justify-center items-center space-y-6">
        <select
          value={selectedOption}
          onChange={e => setSelectedOption(e.target.value)}
          className="w-48 p-3 rounded bg-gray-900 border border-gray-700 text-gray-300 font-semibold text-center text-lg cursor-pointer"
        >
          {options.map(opt => (
            <option key={opt.value} value={opt.value}>
              {opt.label}
            </option>
          ))}
        </select>

        <button
          onClick={handleConvert}
          disabled={busy}
          className={`px-8 py-3 rounded text-white font-bold text-lg transition-shadow shadow-md ${
            busy
              ? 'bg-gray-700 cursor-wait'
              : 'bg-blue-600 hover:bg-blue-700 shadow-blue-500'
          }`}
        >
          {busy ? 'Processing…' : 'Convert'}
        </button>

        {error && <div className="text-red-400 text-sm">{error}</div>}
      </div>

      {/* Output + download */}
      <div className="flex flex-col space-y-6">
        <label className="font-semibold text-neon">Output Preview</label>
        <div
          className="bg-gray-900 rounded border border-gray-700 p-4 overflow-auto text-sm whitespace-pre-wrap inline-flex items-center justify-center"
        >
          {!output ? (
            'Output will appear here after conversion.'
          ) : output.kind === 'image' ? (
            <img src={output.url} alt="output" className="max-w-full max-h-full rounded" />
          ) : (
            'Unsupported output'
          )}
        </div>

        <button
          onClick={handleDownload}
          disabled={!output}
          className={`px-6 py-2 rounded font-semibold text-white text-lg transition ${
            output
              ? 'bg-green-600 hover:bg-green-700 shadow-md shadow-green-500 cursor-pointer'
              : 'bg-gray-700 cursor-not-allowed'
          }`}
        >
          Download Output
        </button>
      </div>
    </div>
  );
}
