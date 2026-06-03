import { useState } from "react";
import { Languages, Link, Loader2, PlayCircle } from "lucide-react";

function AnalyzePanel({ onAnalyze, loading }) {
  const [source, setSource] = useState("");
  const [language, setLanguage] = useState("english");

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!source.trim()) {
      alert("Please enter YouTube URL or local file path.");
      return;
    }

    onAnalyze({
      source: source.trim(),
      language,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="glass-card rounded-[2rem] p-6">
      <div className="mb-6">
        <p className="mb-2 text-xs uppercase tracking-[0.25em] text-[#9f67ff]">
          Input Source
        </p>

        <h2 className="font-['Syne'] text-2xl font-bold">
          Analyse your video
        </h2>

        <p className="mt-2 text-sm leading-6 text-white/50">
          Paste a YouTube URL or provide your local video/audio file path.
        </p>
      </div>

      <div className="space-y-5">
        <label className="block">
          <span className="mb-2 flex items-center gap-2 text-sm text-white/60">
            <Link size={16} />
            YouTube URL / File Path
          </span>

          <input
            value={source}
            onChange={(e) => setSource(e.target.value)}
            placeholder="https://youtube.com/watch?v=... or C:/video.mp4"
            className="w-full rounded-2xl border border-white/10 bg-black/30 px-2 py-4 text-sm text-white outline-none transition placeholder:text-white/25 focus:border-[#9f67ff]"
          />
        </label>

        <label className="block">
          <span className="mb-2 flex items-center gap-2 text-sm text-white/60">
            <Languages size={16} />
            Language
          </span>

          <select
            value={language}
            onChange={(e) => setLanguage(e.target.value)}
            className="w-full rounded-2xl border border-white/10 bg-black/30 px-2 py-4 text-sm text-white outline-none transition focus:border-[#9f67ff]"
          >
            <option className="bg-[#101018]" value="english">
              English
            </option>
            <option className="bg-[#101018]" value="hinglish">
              Hinglish
            </option>
          </select>
        </label>

        <button
          type="submit"
          disabled={loading}
          className="flex w-full items-center justify-center gap-3 rounded-2xl bg-gradient-to-r from-[#7c3aed] to-[#06b6d4] px-5 py-4 font-['Syne'] text-sm font-bold uppercase tracking-[0.15em] text-white transition hover:scale-[1.01] disabled:cursor-not-allowed disabled:opacity-60"
        >
          {loading ? (
            <>
              <Loader2 className="animate-spin" size={18} />
              Analysing...
            </>
          ) : (
            <>
              <PlayCircle size={18} />
              Analyse Video
            </>
          )}
        </button>
      </div>
    </form>
  );
}

export default AnalyzePanel;