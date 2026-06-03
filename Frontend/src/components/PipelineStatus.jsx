import {AudioWaveform, Brain, CheckCircle2, FileText, HelpCircle, Loader2, Search, Sparkles} from "lucide-react";

const iconMap = {
  audio: AudioWaveform,
  transcript: FileText,
  title: Sparkles,
  summary: FileText,
  extract: Search,
  rag: Brain,
};

function PipelineStatus({ steps }) {
  return (
    <div className="glass-card rounded-[2rem] p-6">
      <div className="mb-5 flex items-center justify-between">
        <div>
          <p className="mb-2 text-xs uppercase tracking-[0.25em] text-[#06b6d4]">
            Live Status
          </p>

          <h3 className="font-['Syne'] text-xl font-bold">Pipeline Steps</h3>
        </div>

        <div className="rounded-full border border-white/10 bg-white/5 p-3">
          <HelpCircle size={18} className="text-white/50" />
        </div>
      </div>

      <div className="space-y-3">
        {steps.map((step) => {
          const Icon = iconMap[step.key] || FileText;
          const isDone = step.status === "done";
          const isActive = step.status === "active";

          return (
            <div
              key={step.key}
              className={`flex items-center justify-between rounded-2xl border p-4 transition ${
                isActive
                  ? "border-[#9f67ff]/50 bg-[#9f67ff]/10"
                  : isDone
                  ? "border-green-500/30 bg-green-500/10"
                  : "border-white/10 bg-black/20"
              }`}
            >
              <div className="flex items-center gap-3">
                <div
                  className={`flex h-9 w-9 items-center justify-center rounded-xl ${
                    isActive
                      ? "bg-[#9f67ff]/20 text-[#9f67ff]"
                      : isDone
                      ? "bg-green-500/20 text-green-400"
                      : "bg-white/5 text-white/40"
                  }`}
                >
                  <Icon size={17} />
                </div>

                <span className="text-sm text-white/70">{step.label}</span>
              </div>

              {isActive ? (
                <Loader2 size={18} className="animate-spin text-[#9f67ff]" />
              ) : isDone ? (
                <CheckCircle2 size={18} className="text-green-400" />
              ) : (
                <div className="h-2 w-2 rounded-full bg-white/20" />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default PipelineStatus;