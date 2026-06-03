import { useState } from "react";
import {
  CheckSquare,
  FileQuestion,
  FileText,
  KeyRound,
  Loader2,
  MessageSquareText,
  ScrollText,
} from "lucide-react";
import InfoCard from "./InfoCard";
import TranscriptModal from "./TranscriptModal";

function EmptyState() {
  return (
    <div className="glass-card flex min-h-[520px] flex-col items-center justify-center rounded-[2rem] p-8 text-center">
      <div className="mb-5 flex h-20 w-20 items-center justify-center rounded-[2rem] bg-[#7c3aed]/20 text-[#9f67ff] shadow-[0_0_35px_rgba(124,58,237,0.35)]">
        <MessageSquareText size={34} />
      </div>

      <h2 className="font-['Syne'] text-2xl font-bold">Ready to Analyse</h2>

      <p className="mt-3 max-w-md text-sm leading-7 text-white/50">
        Enter a YouTube link or file path and start the pipeline. Your generated
        summary, decisions, action items and RAG chat will appear here.
      </p>

      <div className="mt-7 flex flex-wrap justify-center gap-3">
        <span className="rounded-full border border-[#9f67ff]/30 bg-[#9f67ff]/10 px-4 py-2 text-xs text-[#9f67ff]">
          Transcription
        </span>

        <span className="rounded-full border border-[#06b6d4]/30 bg-[#06b6d4]/10 px-4 py-2 text-xs text-[#06b6d4]">
          Summarisation
        </span>

        <span className="rounded-full border border-green-500/30 bg-green-500/10 px-4 py-2 text-xs text-green-400">
          RAG Chat
        </span>
      </div>
    </div>
  );
}

function LoadingState() {
  return (
    <div className="glass-card flex min-h-[520px] flex-col items-center justify-center rounded-[2rem] p-8 text-center">
      <Loader2 size={42} className="mb-5 animate-spin text-[#9f67ff]" />

      <h2 className="font-['Syne'] text-2xl font-bold">
        Analysing your video...
      </h2>

      <p className="mt-3 max-w-md text-sm leading-7 text-white/50">
        Processing audio, generating transcript, creating summary and building
        your RAG chain.
      </p>
    </div>
  );
}

function ResultDashboard({ result, loading }) {
  const [showTranscript, setShowTranscript] = useState(false);

  if (loading && !result) return <LoadingState />;

  if (!result) return <EmptyState />;

  return (
    <div className="space-y-6">
      <div className="glass-card rounded-[2rem] p-6">
        <div className="mb-3 flex items-center justify-between gap-4">
          <p className="text-xs uppercase tracking-[0.25em] text-[#9f67ff]">
            Session Title
          </p>

          <button
            onClick={() => setShowTranscript(true)}
            className="flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-xs text-white/60 transition hover:border-[#06b6d4]/40 hover:text-white"
          >
            <ScrollText size={15} />
            View Transcript
          </button>
        </div>

        <h2 className="font-['Syne'] text-2xl font-bold leading-snug text-white sm:text-3xl">
          {result.title}
        </h2>
      </div>

      <InfoCard title="Summary" icon={<FileText size={20} />} accent="purple">
        {result.summary}
      </InfoCard>

      <div className="grid gap-6 xl:grid-cols-3">
        <InfoCard
          title="Action Items"
          icon={<CheckSquare size={20} />}
          accent="green"
        >
          {result.action_items}
        </InfoCard>

        <InfoCard
          title="Key Decisions"
          icon={<KeyRound size={20} />}
          accent="cyan"
        >
          {result.key_decisions}
        </InfoCard>

        <InfoCard
          title="Open Questions"
          icon={<FileQuestion size={20} />}
          accent="orange"
        >
          {result.open_questions}
        </InfoCard>
      </div>

      {showTranscript && (
        <TranscriptModal
          transcript={result.transcript}
          onClose={() => setShowTranscript(false)}
        />
      )}
    </div>
  );
}

export default ResultDashboard;