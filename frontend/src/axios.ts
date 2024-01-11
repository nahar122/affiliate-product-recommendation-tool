// src/axios.js
import axios from "axios";

const instance = axios.create({
  baseURL: `${import.meta.env.VITE_API_URL}/api`, // Replace with your API base URL
  // You can add more default settings here like headers, etc.
});

// You can also add global request and response interceptors here
instance.interceptors.request.use((request) => {
  // Modify or log request before sending it
  return request;
});

instance.interceptors.response.use(
  (response) => {
    // Handle or transform response data
    return response;
  },
  (error) => {
    // Handle response errors
    return Promise.reject(error);
  }
);

export default instance;
