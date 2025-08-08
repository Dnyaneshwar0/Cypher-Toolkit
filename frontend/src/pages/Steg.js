import React, { useState } from 'react';

export default function Steg() {
  const [file1, setFile1] = useState(null);
  const [file2, setFile2] = useState(null);
  const [output, setOutput] = useState(null);
  const [selectedOption, setSelectedOption] = useState('encode');

  // Create preview URLs for files
  const preview1 = file1 ? URL.createObjectURL(file1) : null;
  const preview2 = file2 ? URL.createObjectURL(file2) : null;

  // Example options - you can customize
  const options = [
    // { value: '', label: 'Select option' },
    { value: 'encode', label: 'Encode' },
    { value: 'decode', label: 'Decode' },
  ];

  // Fake backend conversion simulation
  const handleConvert = () => {
    if (!selectedOption) {
      alert('Please select an option.');
      return;
    }

    if (selectedOption === 'encode' && !file1 && !file2) {
      alert('Please upload at least one file.');
      return;
    } else if (selectedOption === 'decode' && !file1) {
      alert('Please upload a file.');
      return;
    }

    // For demo, just show a text output with selected option + filenames
    setOutput(`Processed ${file1?.name || ''} and ${selectedOption === 'encode' ? (file2?.name || '') : ''} with ${selectedOption}`);
  };

  // Download handler for output
  const handleDownload = () => {
    if (!output) return;
    const blob = new Blob([output], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'output.txt';
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="min-h-screen bg-black text-gray-300 px-6 py-12 max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-3 gap-12 font-orbitron">

      {/* Left: file inputs + previews */}
      <div className="space-y-10">
        {/* File input 1 */}
        <div>
          <label className="block mb-2 font-semibold text-neon">Upload File 1</label>
          <input
            type="file"
            accept="image/*,video/*,text/*"
            onChange={e => setFile1(e.target.files[0])}
            className="w-full p-2 rounded bg-gray-900 border border-gray-700 text-gray-300"
          />
          {preview1 && (
            <div className="mt-4 border border-gray-700 rounded p-2 flex justify-center items-center">
              {file1.type.startsWith('image/') ? (
                <img src={preview1} alt="preview 1" className="max-w-full rounded" />
              ) : (
                <p className="text-sm italic">{file1.name}</p>
              )}
            </div>
          )}
        </div>

        {/* Conditionally render File input 2 only if encode is selected */}
        {selectedOption === 'encode' && (
          <div>
            <label className="block mb-2 font-semibold text-neon">Upload File 2</label>
            <input
              type="file"
              accept="image/*,video/*,text/*"
              onChange={e => setFile2(e.target.files[0])}
              className="w-full p-2 rounded bg-gray-900 border border-gray-700 text-gray-300"
            />
            {preview2 && (
              <div className="mt-4 border border-gray-700 rounded p-2 flex justify-center items-center">
                {file2.type.startsWith('image/') ? (
                  <img src={preview2} alt="preview 2" className="max-w-full rounded" />
                ) : (
                  <p className="text-sm italic">{file2.name}</p>
                )}
              </div>
            )}
          </div>
        )}
      </div>

      {/* Center: dropdown + convert button */}
      <div className="flex flex-col justify-center items-center space-y-6">
        <select
          value={selectedOption}
          onChange={e => setSelectedOption(e.target.value)}
          className="w-48 p-3 rounded bg-gray-900 border border-gray-700 text-gray-300 font-semibold text-center text-lg cursor-pointer"
        >
          {options.map(opt => (
            <option key={opt.value} value={opt.value} disabled={opt.value === ''}>
              {opt.label}
            </option>
          ))}
        </select>

        <button
          onClick={handleConvert}
          className="px-8 py-3 bg-blue-600 hover:bg-blue-700 rounded text-white font-bold text-lg transition-shadow shadow-md shadow-blue-500"
        >
          Convert
        </button>
      </div>

      {/* Right: output preview + download */}
      <div className="flex flex-col space-y-6">
        <label className="font-semibold text-neon">Output Preview</label>
        <div
          className="flex-1 bg-gray-900 rounded border border-gray-700 p-4 overflow-auto text-sm whitespace-pre-wrap"
          style={{ minHeight: '300px' }}
        >
          {output || 'Output will appear here after conversion.'}
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
