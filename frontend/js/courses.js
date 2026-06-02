// Course-related functions
async function loadFeaturedCourses() {
    try {
        const token = getToken();
        if (!token) return;
        
        const response = await apiRequest(`${API_BASE_URL}/api/kurse/?page_size=3`, 'GET', token);
        
        if (response.results && response.results.length > 0) {
            displayFeaturedCourses(response.results);
        }
    } catch (error) {
        console.error('Error loading featured courses:', error);
    }
}

function displayFeaturedCourses(courses) {
    const container = document.getElementById('featuredCourses');
    if (!container) return;
    
    container.innerHTML = courses.map(course => `
        <div class="col-md-4">
            <div class="card h-100 shadow-sm">
                <div class="card-body">
                    <h5 class="card-title">${escapeHtml(course.titel)}</h5>
                    <p class="card-text text-muted">
                        ${escapeHtml(course.beschreibung.substring(0, 80))}...
                    </p>
                    <div class="mb-2">
                        <small class="text-muted">
                            <i class="bi bi-calendar"></i> ${formatDate(course.start_datum)}
                        </small>
                    </div>
                    <div class="d-flex justify-content-between align-items-center">
                        <span class="badge ${course.ist_voll ? 'bg-danger' : 'bg-success'}">
                            ${course.ist_voll ? 'Ausgebucht' : `${course.verfuegbare_plaetze} Plätze frei`}
                        </span>
                        <a href="course-detail.html?id=${course.id}" class="btn btn-sm btn-outline-primary">
                            Details <i class="bi bi-arrow-right"></i>
                        </a>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}