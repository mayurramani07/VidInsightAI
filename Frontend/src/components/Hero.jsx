import { motion } from "framer-motion";
import { Brain, FileText, MessageSquareText, WandSparkles } from "lucide-react";

function Hero() {
  const features = [
    { icon: <FileText size={15} />, label: "Transcription" },
    { icon: <WandSparkles size={15} />, label: "Smart Summary" },
    { icon: <Brain size={15} />, label: "RAG Engine" },
    { icon: <MessageSquareText size={15} />, label: "Chat with Video" },
  ];

  return (
    <section className="relative overflow-hidden rounded-[2rem] border border-white/10 bg-white/[0.03] p-6 shadow-[0_0_45px_rgba(124,58,237,0.25)] sm:p-10">
      <div className="absolute right-10 top-10 h-40 w-40 rounded-full bg-[#7c3aed]/20 blur-3xl" />
      <div className="absolute bottom-0 left-1/2 h-36 w-36 rounded-full bg-[#06b6d4]/20 blur-3xl" />

      <div className="relative z-10 grid gap-8 lg:grid-cols-[1.4fr_0.8fr] lg:items-center">
        <div>
          <motion.div
            initial={{ opacity: 0, y: 18 }}
            animate={{ opacity: 1, y: 0 }}
            className="mb-5 inline-flex rounded-full border border-[#9f67ff]/30 bg-[#9f67ff]/10 px-4 py-2 text-xs uppercase tracking-[0.25em] text-[#9f67ff]"
          >
            AI Video Assistant with RAG
          </motion.div>

          <motion.h2
            initial={{ opacity: 0, y: 22 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.08 }}
            className="gradient-text font-['Syne'] text-4xl font-bold leading-tight sm:text-5xl lg:text-5xl">
            Turn long videos into clear insights.
          </motion.h2>

          <motion.p
            initial={{ opacity: 0, y: 22 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.16 }}
            className="mt-3 max-w-xl text-sm leading-6 text-white/60 sm:text-base"
          >
            Upload a video or paste a YouTube link. VidInsight AI transcribes it,
            summarizes the content, extracts action items, key decisions and
            lets you ask questions using transcript-based RAG.
          </motion.p>

          <div className="mt-7 flex flex-wrap gap-3">
            {features.map((item) => (
              <div
                key={item.label}
                className="flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-white/70"
              >
                <span className="text-[#06b6d4]">{item.icon}</span>
                {item.label}
              </div>
            ))}
          </div>
        </div>

        <motion.div
          initial={{ opacity: 0, scale: 0.92 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ delay: 0.22 }}
          className="glass-card relative rounded-[2rem] p-5"
        >
          <div className="mb-4 flex items-center justify-between">
            <span className="text-xs uppercase tracking-[0.25em] text-white/40">
              Pipeline
            </span>

            <span className="rounded-full bg-green-500/10 px-3 py-1 text-xs text-green-400">
              Ready
            </span>
          </div>

          <div className="space-y-3">
            {["Audio", "Transcript", "Summary", "Extraction", "RAG Chat"].map(
              (item, index) => (
                <div
                  key={item}
                  className="flex items-center justify-between rounded-2xl border border-white/10 bg-black/20 p-4"
                >
                  <div className="flex items-center gap-3">
                    <div className="flex h-8 w-8 items-center justify-center rounded-full bg-[#7c3aed]/20 text-xs text-[#9f67ff]">
                      {index + 1}
                    </div>

                    <span className="text-sm text-white/70">{item}</span>
                  </div>

                  <div className="h-2 w-2 animate-pulse rounded-full bg-[#06b6d4]" />
                </div>
              )
            )}
          </div>
        </motion.div>
      </div>
    </section>
  );
}

export default Hero;