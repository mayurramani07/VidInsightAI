import Navbar from "./components/Navbar";
import Hero from "./components/Hero";
import AnalyzePanel from "./components/AnalyzePanel";

function App() {
  return (
    <main className="min-h-screen overflow-hidden bg-[#07070c] text-white">
      <Navbar />

      <section className="mx-auto max-w-10xl px-4 pb-20 pt-8 sm:px-6 lg:px-8">
        <Hero />

      </section>
    </main>
  );
}

export default App;