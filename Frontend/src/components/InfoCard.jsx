import { motion } from "framer-motion";

function InfoCard({ title, icon, children, accent = "purple" }) {
  const accentMap = {
    purple: "from-[#7c3aed] to-[#c084fc]",
    cyan: "from-[#06b6d4] to-[#38bdf8]",
    green: "from-green-500 to-emerald-400",
    orange: "from-orange-500 to-yellow-400",
  };

  const accentClass = accentMap[accent] || accentMap.purple;

  return (
    <motion.div
      initial={{ opacity: 0, y: 18 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-card relative overflow-hidden rounded-[2rem] p-6"
    >
      <div
        className={`absolute left-0 top-0 h-full w-1 bg-gradient-to-b ${accentClass}`}
      />

      <div className="mb-4 flex items-center gap-3">
        <div
          className={`rounded-2xl bg-gradient-to-br ${accentClass} p-3 text-white`}
        >
          {icon}
        </div>

        <h3 className="font-['Syne'] text-lg font-bold">{title}</h3>
      </div>

      <div className="markdown-content text-sm text-white/65">{children}</div>
    </motion.div>
  );
}

export default InfoCard;