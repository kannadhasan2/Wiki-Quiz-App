import { useEffect, useState } from "react";
import { generateQuiz, fetchHistory, fetchQuiz } from "./api";
import QuizCard from "./components/QuizCard";
import Modal from "./components/Modal";

export default function App() {
  const [tab, setTab] = useState("generate");
  const [url, setUrl] = useState("");
  const [result, setResult] = useState(null);
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const [selected, setSelected] = useState(null);
  const [modalOpen, setModalOpen] = useState(false);

  useEffect(() => {
    fetchHistory().then(setHistory);
  }, []);

  async function handleGenerate() {
    setLoading(true);
    try {
      const data = await generateQuiz(url);
      setResult(data);
      fetchHistory().then(setHistory);
    } finally {
      setLoading(false);
    }
  }

  async function openDetails(id) {
    const data = await fetchQuiz(id);
    setSelected(data);
    setModalOpen(true);
  }

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-5xl mx-auto">
        <h1 className="text-2xl font-bold mb-6">
          Wikipedia Quiz Generator
        </h1>

        {/* Tabs */}
        <div className="flex gap-4 mb-6">
          <button
            onClick={() => setTab("generate")}
            className={`px-4 py-2 rounded ${
              tab === "generate" ? "bg-black text-white" : "bg-white"
            }`}
          >
            Generate Quiz
          </button>
          <button
            onClick={() => setTab("history")}
            className={`px-4 py-2 rounded ${
              tab === "history" ? "bg-black text-white" : "bg-white"
            }`}
          >
            Past Quizzes
          </button>
        </div>

        {/* TAB 1 */}
        {tab === "generate" && (
          <div className="space-y-6">
            <div className="flex gap-3">
              <input
                value={url}
                onChange={(e) => setUrl(e.target.value)}
                placeholder="Paste Wikipedia URL"
                className="flex-1 border rounded px-3 py-2"
              />
              <button
                onClick={handleGenerate}
                disabled={loading}
                className="bg-black text-white px-4 py-2 rounded"
              >
                {loading ? "Generating..." : "Generate"}
              </button>
            </div>

            {result && (
              <>
                <div className="bg-white p-4 rounded shadow">
                  <h2 className="text-xl font-semibold">
                    {result.title}
                  </h2>
                  <p className="text-gray-600 text-sm mt-1">
                    {result.summary}
                  </p>
                </div>

                <QuizCard quiz={result.quiz} reveal />

                <div className="bg-white p-4 rounded shadow">
                  <h3 className="font-semibold mb-2">
                    Related Topics
                  </h3>
                  <ul className="list-disc pl-5 text-sm text-gray-700">
                    {result.related_topics.map((t, i) => (
                      <li key={i}>{t}</li>
                    ))}
                  </ul>
                </div>
              </>
            )}
          </div>
        )}

        {/* TAB 2 */}
        {tab === "history" && (
          <div className="bg-white rounded shadow overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-gray-200">
                <tr>
                  <th className="p-3 text-left">ID</th>
                  <th className="p-3 text-left">Title</th>
                  <th className="p-3">Action</th>
                </tr>
              </thead>
              <tbody>
                {history.map((h) => (
                  <tr key={h.id} className="border-t">
                    <td className="p-3">{h.id}</td>
                    <td className="p-3">{h.title}</td>
                    <td className="p-3 text-center">
                      <button
                        onClick={() => openDetails(h.id)}
                        className="text-blue-600 underline"
                      >
                        Details
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Modal */}
        <Modal open={modalOpen} onClose={() => setModalOpen(false)}>
          {selected && (
            <>
              <h2 className="text-xl font-bold mb-4">
                {selected.title}
              </h2>
              <QuizCard quiz={selected.quiz} reveal />
            </>
          )}
        </Modal>
      </div>
    </div>
  );
}
