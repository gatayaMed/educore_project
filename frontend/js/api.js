// frontend/js/api.js
// Use absolute URL for production
const API_BASE_URL = 'https://educore.smarta.website';

async function apiRequest(endpoint, method = 'GET', token = null, data = null) {
    // Make sure endpoint starts with /api/
    let url = endpoint;
    if (!url.startsWith('http')) {
        url = `${API_BASE_URL}${url.startsWith('/') ? url : '/' + url}`;
    }
    
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
        console.log('API Request:', method, url);
        const response = await fetch(url, config);
        
        // Check if response is HTML (error)
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('text/html')) {
            console.error('Got HTML instead of JSON. Response status:', response.status);
            throw new Error(`API returned HTML (${response.status}). Check Traefik routing.`);
        }
        
        const responseData = await response.json();
        
        if (!response.ok) {
            throw responseData;
        }
        
        return responseData;
    } catch (error) {
        console.error('API Error:', error);
        console.error('Failed URL:', url);
        throw error;
    }
}

// Login function
async function login(username, password) {
    return apiRequest('/api-token-auth/', 'POST', null, {
        username: username,
        password: password
    });
}