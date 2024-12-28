import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000'; // Your FastAPI URL

export const api = axios.create({
  baseURL: API_BASE_URL,
});

export const getRandomSelection = async () => {
  const response = await api.get('/your-endpoint');
  return response.data;
};