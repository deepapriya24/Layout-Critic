import { useState, useRef } from "react";

export default function UploadZone({ onFileSelected, previewUrl, isLoading }) {
  const [isDragOver, setIsDragOver] = useState(false);
  const inputRef = useRef(null);

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    const file = e.dataTransfer.files?.[0];
    if (file) onFileSelected(file);
  };

  const handleChange = (e) => {
    const file = e.target.files?.[0];
    if (file) onFileSelected(file);
  };

  return (
    <div
      onDragOver={(e) => {
        e.preventDefault();
        setIsDragOver(true);
      }}
      onDragLeave={() => setIsDragOver(false)}
      onDrop={handleDrop}
      onClick={() => inputRef.current?.click()}
      className={`relative overflow-hidden rounded-xl border-2 border-dashed cursor-pointer
        transition-all duration-300 min-h-[320px] flex items-center justify-center
        ${isDragOver ? "border-accent shadow-glow bg-panel/60" : "border-accent/40 bg-panel/30"}
        hover:border-accent hover:shadow-glowSm`}
    >
      <input
        ref={inputRef}
        type="file"
        accept="image/png, image/jpeg, image/webp"
        className="hidden"
        onChange={handleChange}
      />

      {previewUrl ? (
        <img src={previewUrl} alt="preview" className="w-full h-full object-contain max-h-[420px]" />
      ) : (
        <div className="text-center px-6">
          <p className="font-mono text-accent text-lg mb-2">DROP UI SCREENSHOT</p>
          <p className="text-sm text-gray-400">or click to browse — PNG, JPG, WEBP</p>
        </div>
      )}

      {isLoading && (
        <div className="absolute inset-0 pointer-events-none">
          <div className="absolute left-0 right-0 h-[2px] bg-accent shadow-glow animate-scan" />
        </div>
      )}
    </div>
  );
}
