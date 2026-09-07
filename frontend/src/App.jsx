import { useState } from "react";
import UploadZone from "./components/UploadZone";
import ScoreRing from "./components/ScoreRing";
import ScoreOverlay from "./components/ScoreOverlay";
import IssuesSidebar from "./components/IssuesSidebar";
import Loader from "./components/Loader";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function App() {
  const [previewUrl, setPreviewUrl] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const handleFileSelected = async (file) => {
    setError(null);
    setResult(null);
    setPreviewUrl(URL.createObjectURL(file));
    setIsLoading(true);

    try {
      const formData = new FormData();
      formData.append("file", file);

      const res = await fetch(`${API_URL}/analyze`, {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const body = await res.json().catch(() => ({}));
        throw new Error(body.detail || "Analysis failed");
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  const categoryEntries = result ? Object.entries(result.categories) : [];

  return (
    <div className="min-h-screen px-6 py-10 max-w-6xl mx-auto">
      <header className="mb-8 text-center">
        <h1 className="font-mono text-3xl md:text-4xl text-accent tracking-tight drop-shadow-[0_0_12px_rgba(232,122,45,0.4)]">
          LAYOUT CRITIC
        </h1>
        <p className="text-gray-400 mt-2 text-sm">
          Drop a UI screenshot and get an instant AI-powered design critique.
        </p>
      </header>

      <div className="grid md:grid-cols-2 gap-6 items-start">
        <UploadZone
          onFileSelected={handleFileSelected}
          previewUrl={previewUrl}
          isLoading={isLoading}
        />

        <div>
          {isLoading && <Loader />}
          {error && (
            <p className="text-red-400 font-mono text-sm text-center py-4">{error}</p>
          )}
          {result && !isLoading && (
            <div className="flex flex-col gap-6">
              <div className="flex justify-center">
                <ScoreRing score={result.overall_score} label="Overall" size={130} />
              </div>
              <div className="grid grid-cols-3 gap-4 justify-items-center">
                {categoryEntries.map(([key, val]) => (
                  <ScoreRing key={key} score={val.score} label={key.replace("_", " ")} size={80} />
                ))}
              </div>
            </div>
          )}
        </div>
      </div>

      {result && !isLoading && (
        <div className="grid md:grid-cols-2 gap-6 mt-8">
          <ScoreOverlay imageUrl={previewUrl} issues={result.issues} />
          <IssuesSidebar issues={result.issues} />
        </div>
      )}
    </div>
  );
}
