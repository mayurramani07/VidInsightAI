import axios from "axios";

const LOCAL_BACKEND = "http://127.0.0.1:8000";
const RENDER_BACKEND = "https://vidinsightai.onrender.com";

let activeBaseURL = null;

const checkBackend = async (baseURL) => {
  try {
    await axios.get(`${baseURL}/`, {
      timeout: 3000,
    });

    return true;
  } catch (error) {
    return false;
  }
};

const getActiveBaseURL = async () => {
  if (activeBaseURL) {
    return activeBaseURL;
  }

  const isLocalRunning = await checkBackend(LOCAL_BACKEND);

  if (isLocalRunning) {
    activeBaseURL = LOCAL_BACKEND;
    console.log("Using local backend:", activeBaseURL);
    return activeBaseURL;
  }

  activeBaseURL = RENDER_BACKEND;
  console.log("Using Render backend:", activeBaseURL);
  return activeBaseURL;
};

const apiPost = async (endpoint, data) => {
  const baseURL = await getActiveBaseURL();

  try {
    const response = await axios.post(`${baseURL}${endpoint}`, data, {
      timeout: 1000 * 60 * 20,
    });

    return response.data;
  } catch (error) {
    if (baseURL === LOCAL_BACKEND) {
      console.log("Local failed, retrying with Render...");

      activeBaseURL = RENDER_BACKEND;

      const response = await axios.post(`${RENDER_BACKEND}${endpoint}`, data, {
        timeout: 1000 * 60 * 20,
      });

      return response.data;
    }

    throw error;
  }
};

export const analyzeVideo = async ({ source, language }) => {
  return await apiPost("/api/analyze", {
    source,
    language,
  });
};

export const askMeetingQuestion = async ({ question }) => {
  return await apiPost("/api/chat", {
    question,
  });
};

export default axios;