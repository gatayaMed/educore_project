// js/auth.js
// Authentication functions

function getToken() {
    return localStorage.getItem('auth_token');
}

function saveToken(token) {
    localStorage.setItem('auth_token', token);
}

function removeToken() {
    localStorage.removeItem('auth_token');
}

function isAuthenticated() {
    return !!getToken();
}

function logout() {
    removeToken();
    localStorage.removeItem('user_data');
    window.location.href = 'login.html';
}

function checkAuthStatus() {
    const navAuth = document.getElementById('navAuth');
    if (!navAuth) return;
    
    const token = getToken();
    
    if (token) {
        // User is logged in
        navAuth.innerHTML = `
            <div class="dropdown">
                <button class="btn btn-light dropdown-toggle" type="button" data-bs-toggle="dropdown">
                    <i class="bi bi-person-circle"></i> Mein Konto
                </button>
                <ul class="dropdown-menu dropdown-menu-end">
                    <li><a class="dropdown-item" href="#" onclick="logout()">
                        <i class="bi bi-box-arrow-right"></i> Abmelden
                    </a></li>
                </ul>
            </div>
        `;
    } else {
        // User is logged out
        navAuth.innerHTML = `
            <a class="nav-link btn btn-light text-primary px-3" href="login.html">
                <i class="bi bi-box-arrow-in-right me-1"></i> Anmelden
            </a>
        `;
    }
}

// Login form handler
if (document.getElementById('loginForm')) {
    document.getElementById('loginForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const username = document.getElementById('username').value;
        const password = document.getElementById('password').value;
        const loginBtn = document.getElementById('loginBtn');
        
        if (!loginBtn) return;
        
        loginBtn.disabled = true;
        loginBtn.innerHTML = '<span class="spinner-border spinner-border-sm"></span> Wird angemeldet...';
        
        try {
            const response = await login(username, password);
            
            if (response.token) {
                saveToken(response.token);
                showAlert('Erfolgreich angemeldet!', 'success');
                
                setTimeout(() => {
                    window.location.href = 'courses.html';
                }, 1000);
            }
        } catch (error) {
            let errorMessage = 'Anmeldung fehlgeschlagen';
            if (error.non_field_errors) {
                errorMessage = error.non_field_errors.join(', ');
            } else if (error.error) {
                errorMessage = error.error;
            }
            showAlert(errorMessage, 'danger');
            loginBtn.disabled = false;
            loginBtn.innerHTML = '<i class="bi bi-box-arrow-in-right"></i> Anmelden';
        }
    });
}

function showAlert(message, type) {
    const alertContainer = document.getElementById('alertMessage');
    if (!alertContainer) return;
    
    alertContainer.innerHTML = `
        <div class="alert alert-${type} alert-dismissible fade show" role="alert">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
    
    setTimeout(() => {
        const alert = alertContainer.querySelector('.alert');
        if (alert) {
            alert.remove();
        }
    }, 5000);
}