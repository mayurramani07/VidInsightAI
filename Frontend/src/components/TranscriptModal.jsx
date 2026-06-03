import { X } from "lucide-react";

function TranscriptModal({ transcript, onClose }) {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 p-4 backdrop-blur-lg">
      <div className="glass-card max-h-[85vh] w-full max-w-4xl overflow-hidden rounded-[2rem]">
        <div className="flex items-center justify-between border-b border-white/10 p-5">
          <div>
            <p className="text-xs uppercase tracking-[0.25em] text-[#9f67ff]">
              Full Transcript
            </p>

            <h3 className="font-['Syne'] text-xl font-bold">
              Transcript Preview
            </h3>
          </div>

          <button
            onClick={onClose}
            className="rounded-full border border-white/10 bg-white/5 p-3 transition hover:bg-white/10"
          >
            <X size={18} />
          </button>
        </div>

        <div className="max-h-[70vh] overflow-y-auto p-6">
          <pre className="whitespace-pre-wrap text-sm leading-8 text-white/65">
            {transcript}
          </pre>
        </div>
      </div>
    </div>
  );
}

export default TranscriptModal;