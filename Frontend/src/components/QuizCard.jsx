export default function QuizCard({ quiz, reveal }) {
  return (
    <div className="space-y-4">
      {quiz.map((q, idx) => (
        <div
          key={idx}
          className="border rounded-lg p-4 bg-white shadow-sm"
        >
          <h3 className="font-semibold mb-2">
            {idx + 1}. {q.question}
          </h3>

          <ul className="space-y-1">
            {q.options.map((opt, i) => (
              <li
                key={i}
                className={`px-3 py-2 rounded border text-sm ${
                  reveal && opt === q.answer
                    ? "bg-green-100 border-green-400"
                    : "bg-gray-50"
                }`}
              >
                {opt}
              </li>
            ))}
          </ul>

          {reveal && (
            <p className="mt-2 text-sm text-gray-600">
              <span className="font-medium">Explanation:</span>{" "}
              {q.explanation}
            </p>
          )}

          <span className="inline-block mt-2 text-xs px-2 py-1 bg-gray-200 rounded">
            {q.difficulty}
          </span>
        </div>
      ))}
    </div>
  );
}
