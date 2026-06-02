// API Configuration
// Use relative URLs - Coolify/Traefik handles routing
const API_BASE_URL = '';  // Empty = same domain

// All API calls will go to /api/ which Traefik routes to backend
// Example: GET /api/kurse/ 

// Global API request function
async function apiRequest(endpoint, method = 'GET', token = null, data = null) {
    const headers = {
        'Content-Type': 'application/json',
    };
    
    if (token) {
        headers['Authorization'] = `Token ${token}`;
    }
    
    const config = {
        method: method,
        headers: headers,
    };
    
    if (data && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
        config.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(endpoint, config);
        const responseData = await response.json();
        
        if (!response.ok) {
            throw responseData;
        }
        
        return responseData;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}