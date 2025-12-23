// API Configuration
// Auto-detect API URL based on environment
const getApiUrl = () => {
    // Production: Use environment variable or detect from current domain
    if (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1') {
        // If frontend is on Vercel, backend should be on Railway
        // You can set this via Vercel environment variable
        const envApiUrl = window.API_URL || 'https://your-backend.railway.app/api';
        return envApiUrl;
    }
    // Development: Use localhost
    return 'http://localhost:5000/api';
};

const API_URL = getApiUrl();

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { API_URL };
}

