const BASE_URL = "https://wiki-quiz-app-sauw.onrender.com";

export async function generateQuiz(url) {
  const res = await fetch(`${BASE_URL}/generate-quiz`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url }),
  });
  if (!res.ok) throw new Error("Quiz generation failed");
  return res.json();
}

export async function fetchHistory() {
  const res = await fetch(`${BASE_URL}/quizzes`);
  return res.json();
}

export async function fetchQuiz(id) {
  const res = await fetch(`${BASE_URL}/quizzes/${id}`);
  return res.json();
}
