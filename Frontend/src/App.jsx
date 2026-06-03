import { useRef, useState } from "react";
import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import AnalyzePanel from "./components/AnalyzePanel";
import PipelineStatus from "./components/PipelineStatus";
import ResultDashboard from "./components/ResultDashboard";
import ChatBox from "./components/ChatBox";
import { analyzeVideo } from "./api/api";

const initialSteps = [
  { key: "audio", label: "Audio Processing", status: "pending" },
  { key: "transcript", label: "Transcription", status: "pending" },
  { key: "title", label: "Title Generation", status: "pending" },
  { key: "summary", label: "Summarisation", status: "pending" },
  { key: "extract", label: "Insight Extraction", status: "pending" },
  { key: "rag", label: "RAG Engine", status: "pending" },
];

function App() {
  const [result, setResult] = useState(null);
  const [steps, setSteps] = useState(initialSteps);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const timersRef = useRef([]);

  const updateStep = (key, status) => {
    setSteps((prev) =>
      prev.map((step) => (step.key === key ? { ...step, status } : step))
    );
  };

  const resetTimers = () => {
    timersRef.current.forEach((timer) => clearTimeout(timer));
    timersRef.current = [];
  };

  const startLiveProgress = () => {
    resetTimers();

    setSteps(initialSteps);

    updateStep("audio", "active");

    timersRef.current.push(
      setTimeout(() => {
        updateStep("audio", "done");
        updateStep("transcript", "active");
      }, 1500)
    );

    timersRef.current.push(
      setTimeout(() => {
        updateStep("transcript", "done");
        updateStep("title", "active");
      }, 4000)
    );

    timersRef.current.push(
      setTimeout(() => {
        updateStep("title", "done");
        updateStep("summary", "active");
      }, 5500)
    );

    timersRef.current.push(
      setTimeout(() => {
        updateStep("summary", "done");
        updateStep("extract", "active");
      }, 7500)
    );

    timersRef.current.push(
      setTimeout(() => {
        updateStep("extract", "done");
        updateStep("rag", "active");
      }, 9500)
    );
  };

  const markAllDone = () => {
    setSteps((prev) =>
      prev.map((step) => ({
        ...step,
        status: "done",
      }))
    );
  };

  const markFailed = () => {
    setSteps((prev) =>
      prev.map((step) =>
        step.status === "active"
          ? { ...step, status: "pending" }
          : step
      )
    );
  };

  const handleAnalyze = async ({ source, language }) => {
    try {
      setLoading(true);
      setError("");
      setResult(null);

      startLiveProgress();

      const data = await analyzeVideo({
        source,
        language,
      });

      resetTimers();
      markAllDone();

      setResult(data);
    } catch (err) {
      console.error(err);

      resetTimers();
      markFailed();

      setError(
        err?.response?.data?.detail ||
          err?.message ||
          "Something went wrong while analysing the video."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen overflow-hidden bg-[#07070c] text-white">
      <Navbar />

      <section className="mx-auto max-w-10xl px-4 pb-20 pt-10 sm:px-6 lg:px-8">
        <Hero />

        <div className="mt-10 grid gap-6 lg:grid-cols-[430px_1fr]">
          <div className="space-y-6">
            <AnalyzePanel onAnalyze={handleAnalyze} loading={loading} />
            <PipelineStatus steps={steps} />
          </div>

          <div className="space-y-6">
            {error && (
              <div className="rounded-3xl border border-red-500/30 bg-red-500/10 p-5 text-sm leading-7 text-red-200">
                {error}
              </div>
            )}

            <ResultDashboard result={result} loading={loading} />

            {result && <ChatBox />}
          </div>
        </div>
      </section>
    </main>
  );
}

export default App;