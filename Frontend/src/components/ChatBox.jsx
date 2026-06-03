import { useState } from "react";
import { Bot, Loader2, Send, Trash2, UserRound } from "lucide-react";
import { askMeetingQuestion } from "../api/api";

function ChatBox() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content:
        "Ask me anything about the video transcript. For example: What were the main points discussed?",
    },
  ]);

  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSend = async (e) => {
    e.preventDefault();

    const cleanQuestion = question.trim();
    if (!cleanQuestion) return;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: cleanQuestion,
      },
    ]);

    setQuestion("");
    setLoading(true);

    try {
      const data = await askMeetingQuestion({
        question: cleanQuestion,
      });

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.answer || data.response || "No answer received.",
        },
      ]);
    } catch (err) {
      console.error(err);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content:
            err?.response?.data?.detail ||
            "Sorry, I could not answer this question.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const clearChat = () => {
    setMessages([
      {
        role: "assistant",
        content:
          "Ask me anything about the video transcript. For example: What were the main points discussed?",
      },
    ]);
  };

  return (
    <section className="glass-card rounded-[2rem] p-6">
      <div className="mb-5 flex items-center justify-between">
        <div>
          <p className="mb-2 text-xs uppercase tracking-[0.25em] text-[#06b6d4]">
            RAG Chat
          </p>

          <h2 className="font-['Syne'] text-2xl font-bold">
            Chat with your video
          </h2>
        </div>

        <button
          onClick={clearChat}
          className="rounded-full border border-white/10 bg-white/5 p-3 text-white/50 transition hover:text-white"
        >
          <Trash2 size={17} />
        </button>
      </div>

      <div className="mb-5 max-h-[420px] space-y-4 overflow-y-auto rounded-[1.5rem] border border-white/10 bg-black/20 p-4">
        {messages.map((message, index) => {
          const isUser = message.role === "user";

          return (
            <div
              key={index}
              className={`flex gap-3 ${
                isUser ? "justify-end" : "justify-start"
              }`}
            >
              {!isUser && (
                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-[#06b6d4]/20 text-[#06b6d4]">
                  <Bot size={17} />
                </div>
              )}

              <div
                className={`max-w-[82%] rounded-2xl px-4 py-3 text-sm leading-7 ${
                  isUser
                    ? "bg-[#7c3aed] text-white"
                    : "border border-white/10 bg-white/5 text-white/70"
                }`}
              >
                {message.content}
              </div>

              {isUser && (
                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-[#9f67ff]/20 text-[#9f67ff]">
                  <UserRound size={17} />
                </div>
              )}
            </div>
          );
        })}

        {loading && (
          <div className="flex items-center gap-3 text-sm text-white/50">
            <Loader2 size={17} className="animate-spin text-[#06b6d4]" />
            Thinking from transcript...
          </div>
        )}
      </div>

      <form onSubmit={handleSend} className="flex gap-3">
        <input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask: What were the key decisions?"
          className="min-w-0 flex-1 rounded-2xl border border-white/10 bg-black/30 px-4 py-4 text-sm text-white outline-none placeholder:text-white/25 focus:border-[#9f67ff]"
        />

        <button
          type="submit"
          disabled={loading}
          className="flex items-center gap-2 rounded-2xl bg-gradient-to-r from-[#7c3aed] to-[#06b6d4] px-5 py-4 font-['Syne'] text-sm font-bold text-white transition hover:scale-[1.02] disabled:opacity-60"
        >
          {loading ? (
            <Loader2 size={18} className="animate-spin" />
          ) : (
            <Send size={18} />
          )}
          <span className="hidden sm:inline">Send</span>
        </button>
      </form>
    </section>
  );
}

export default ChatBox;