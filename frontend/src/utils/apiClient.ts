import axios from 'axios';

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://app1.caprover.example.com';

const apiClient = axios.create({
    baseURL: BASE_URL,
    withCredentials: true,
});

const handleError = (error: any) => {
    if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        console.error("Data:", error.response.data);
        console.error("Status:", error.response.status);
        console.error("Headers:", error.response.headers);
    } else if (error.request) {
        // The request was made but no response was received
        console.error("No response received:", error.request);
    } else {
        // Something happened in setting up the request that triggered an Error
        console.error("Error:", error.message);
    }
    return Promise.reject(error);
};

apiClient.interceptors.response.use(
    response => response,
    error => handleError(error)
);

export default apiClient;
