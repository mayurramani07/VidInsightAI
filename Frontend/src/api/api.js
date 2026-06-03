import axios from "axios";

const API_BASE_URL = "https://vidinsightai.onrender.com";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 1000 * 60 * 20,
});

export const analyzeVideo = async ({ source, language }) => {
  const response = await api.post("/api/analyze", {
    source,
    language,
  });

  return response.data;
};

export const askMeetingQuestion = async ({ question }) => {
  const response = await api.post("/api/chat", {
    question,
  });

  return response.data;
};

export default api;