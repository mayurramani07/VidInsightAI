import { Code2, Sparkles, Video } from "lucide-react";
import { motion } from "framer-motion";

function Navbar() {
  return (
    <header className="sticky top-0 z-40 border-b border-white/10 bg-[#07070c]/75 backdrop-blur-xl">
      <nav className="mx-auto flex max-w-8xl items-center justify-between px-6 py-2 sm:px-6 lg:px-6 lg:py-2">
        <motion.div
          initial={{ opacity: 0, x: -18 }}
          animate={{ opacity: 1, x: 0 }}
          className="flex items-center gap-3"
        >
          <div className="flex h-8 w-8 items-center justify-center rounded-2xl bg-[#7c3aed] shadow-[0_0_35px_rgba(124,58,237,0.45)]">
            <Video size={18} />
          </div>

          <div>
            <h1 className="font-['Syne'] text-lg font-bold tracking-tight">
              VidInsight AI
            </h1>
            <p className="text-[11px] uppercase tracking-[0.25em] text-white/40">
              Video Intelligence
            </p>
          </div>
        </motion.div>

        <div className="hidden items-center gap-3 sm:flex">
          <span className="rounded-full border border-[#06b6d4]/30 bg-[#06b6d4]/10 px-3 py-1 text-xs text-[#06b6d4]">
            RAG Powered
          </span>

          {/* <button className="flex items-center gap-2 rounded-full border border-white/10 bg-white/5 px-4 py-2 text-sm text-white/70 transition hover:border-[#9f67ff]/50 hover:text-white">
            <Code2 size={16} />
            Project
          </button> */}

          {/* <button className="flex items-center gap-2 rounded-full bg-white px-4 py-2 text-sm font-semibold text-black transition hover:bg-[#9f67ff] hover:text-white">
            <Sparkles size={16} />
            Try Now
          </button> */}
        </div>
      </nav>
    </header>
  );
}

export default Navbar;