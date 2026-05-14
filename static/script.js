// API Base URL
const API_BASE = 'http://localhost:8000';

// Smooth scroll functions
function scrollToPlanner() {
    document.getElementById('planner').scrollIntoView({ behavior: 'smooth' });
}

function scrollToKnowledge() {
    document.getElementById('knowledge').scrollIntoView({ behavior: 'smooth' });
}

// Event Form Submission
document.getElementById('eventForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    // Show loading
    showLoading();
    
    // Get form data
    const eventType = document.getElementById('eventType').value;
    const city = document.getElementById('city').value;
    const budget = parseInt(document.getElementById('budget').value);
    const guestCount = document.getElementById('guestCount').value;
    const eventDate = document.getElementById('eventDate').value;
    const preferences = document.getElementById('preferences').value;
    const requirements = document.getElementById('requirements').value;
    
    // Build request body
    const requestBody = {
        event_type: eventType,
        city: city,
        budget: budget
    };
    
    if (guestCount) requestBody.guest_count = parseInt(guestCount);
    if (eventDate) requestBody.date = eventDate;
    if (preferences) requestBody.preferences = preferences.split(',').map(p => p.trim());
    if (requirements) requestBody.special_requirements = requirements;
    
    try {
        const response = await fetch(`${API_BASE}/api/v1/plan`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });
        
        if (!response.ok) {
            throw new Error('Failed to generate event plan');
        }
        
        const data = await response.json();
        displayResults(data);
        
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to generate event plan. Please try again.');
    } finally {
        hideLoading();
    }
});

// Display Results
function displayResults(data) {
    const resultsDiv = document.getElementById('results');
    const resultsContent = document.getElementById('resultsContent');
    
    // Store data for download
    window.currentPlan = data;
    
    let html = '';
    
    // Event Summary
    html += `
        <div class="result-section">
            <h4><i class="fas fa-info-circle"></i> Event Summary</h4>
            <div class="budget-item">
                <span class="budget-label">Event Type</span>
                <span class="budget-amount">${capitalizeFirst(data.event_type)}</span>
            </div>
            <div class="budget-item">
                <span class="budget-label">City</span>
                <span class="budget-amount">${data.city}</span>
            </div>
            <div class="budget-item">
                <span class="budget-label">Total Budget</span>
                <span class="budget-amount">₹${formatNumber(data.total_budget)}</span>
            </div>
            ${data.estimated_guest_count ? `
            <div class="budget-item">
                <span class="budget-label">Guest Count</span>
                <span class="budget-amount">${data.estimated_guest_count}</span>
            </div>
            ` : ''}
        </div>
    `;
    
    // Budget Breakdown
    html += `
        <div class="result-section">
            <h4><i class="fas fa-chart-pie"></i> Budget Breakdown</h4>
    `;
    
    data.budget_breakdown.forEach(item => {
        html += `
            <div class="budget-item">
                <div>
                    <span class="budget-label">${capitalizeFirst(item.category)}</span>
                    <span style="color: var(--gray); font-size: 0.875rem; margin-left: 0.5rem;">
                        ${item.percentage.toFixed(1)}%
                    </span>
                </div>
                <span class="budget-amount">₹${formatNumber(item.allocated_amount)}</span>
            </div>
        `;
    });
    
    html += '</div>';
    
    // Timeline
    html += `
        <div class="result-section">
            <h4><i class="fas fa-calendar-alt"></i> Timeline (${data.timeline.length} tasks)</h4>
    `;
    
    data.timeline.slice(0, 5).forEach(task => {
        html += `
            <div class="timeline-item">
                <div class="timeline-days">${task.days_before_event} days before</div>
                <div style="font-weight: 600; margin-bottom: 0.25rem;">${task.task_name}</div>
                <div style="color: var(--gray); font-size: 0.875rem;">${task.description}</div>
                ${task.is_critical ? '<div style="color: var(--danger); font-size: 0.875rem; margin-top: 0.25rem;"><i class="fas fa-exclamation-circle"></i> Critical Task</div>' : ''}
            </div>
        `;
    });
    
    if (data.timeline.length > 5) {
        html += `<p style="color: var(--gray); text-align: center; margin-top: 1rem;">+ ${data.timeline.length - 5} more tasks</p>`;
    }
    
    html += '</div>';
    
    // Vendor Suggestions
    html += `
        <div class="result-section">
            <h4><i class="fas fa-store"></i> Vendor Suggestions</h4>
    `;
    
    data.vendor_suggestions.forEach(vendor => {
        html += `
            <div class="vendor-item">
                <div class="vendor-header">
                    <span class="vendor-name">${vendor.name}</span>
                    ${vendor.rating ? `<span class="vendor-rating"><i class="fas fa-star"></i> ${vendor.rating}</span>` : ''}
                </div>
                <div style="color: var(--gray); font-size: 0.875rem; margin-bottom: 0.25rem;">
                    ${capitalizeFirst(vendor.category)}
                </div>
                <div style="font-weight: 600; color: var(--success);">
                    ₹${formatNumber(vendor.estimated_cost)}
                </div>
            </div>
        `;
    });
    
    html += '</div>';
    
    // Recommendations
    html += `
        <div class="result-section">
            <h4><i class="fas fa-lightbulb"></i> Recommendations</h4>
    `;
    
    data.recommendations.forEach(rec => {
        html += `
            <div class="recommendation-item">
                <i class="fas fa-check-circle"></i>
                <span>${rec}</span>
            </div>
        `;
    });
    
    html += '</div>';
    
    resultsContent.innerHTML = html;
    resultsDiv.style.display = 'block';
    
    // Scroll to results
    resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Knowledge Form Submission
document.getElementById('knowledgeForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const query = document.getElementById('knowledgeQuery').value;
    await queryKnowledge(query);
});

// Ask Question Function
async function askQuestion(question) {
    document.getElementById('knowledgeQuery').value = question;
    await queryKnowledge(question);
}

// Query Knowledge Base
async function queryKnowledge(query) {
    showLoading();
    
    const requestBody = {
        query: query,
        top_k: 3
    };
    
    try {
        const response = await fetch(`${API_BASE}/api/v1/knowledge/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestBody)
        });
        
        if (!response.ok) {
            throw new Error('Failed to query knowledge base');
        }
        
        const data = await response.json();
        displayKnowledgeResults(data);
        
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to query knowledge base. Please try again.');
    } finally {
        hideLoading();
    }
}

// Display Knowledge Results
function displayKnowledgeResults(data) {
    const resultsDiv = document.getElementById('knowledgeResults');
    const answerDiv = document.getElementById('knowledgeAnswer');
    
    let html = `
        <div style="margin-bottom: 1.5rem;">
            <p style="line-height: 1.8;">${data.answer}</p>
        </div>
    `;
    
    if (data.sources && data.sources.length > 0) {
        html += `
            <div class="sources">
                <h5><i class="fas fa-book"></i> Sources</h5>
        `;
        
        data.sources.forEach(source => {
            html += `
                <div class="source-item">
                    <div style="font-weight: 600; margin-bottom: 0.25rem;">${source.title}</div>
                    <div style="color: var(--gray); font-size: 0.875rem;">
                        Category: ${capitalizeFirst(source.category)}
                    </div>
                </div>
            `;
        });
        
        html += '</div>';
    }
    
    html += `
        <div style="margin-top: 1.5rem; padding-top: 1.5rem; border-top: 2px solid var(--border); text-align: center;">
            <span style="color: var(--gray); font-size: 0.875rem;">
                <i class="fas fa-chart-line"></i> Confidence: ${(data.confidence * 100).toFixed(0)}%
            </span>
        </div>
    `;
    
    answerDiv.innerHTML = html;
    resultsDiv.style.display = 'block';
    
    // Scroll to results
    resultsDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Download Plan
function downloadPlan() {
    if (!window.currentPlan) return;
    
    const dataStr = JSON.stringify(window.currentPlan, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `event-plan-${Date.now()}.json`;
    link.click();
    URL.revokeObjectURL(url);
}

// Utility Functions
function showLoading() {
    document.getElementById('loadingOverlay').style.display = 'flex';
}

function hideLoading() {
    document.getElementById('loadingOverlay').style.display = 'none';
}

function formatNumber(num) {
    return new Intl.NumberFormat('en-IN').format(num);
}

function capitalizeFirst(str) {
    return str.charAt(0).toUpperCase() + str.slice(1);
}

// Navigation Active State
document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function(e) {
        if (this.getAttribute('href').startsWith('#')) {
            e.preventDefault();
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            this.classList.add('active');
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        }
    });
});

// Scroll Spy
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section[id]');
    const scrollY = window.pageYOffset;
    
    sections.forEach(section => {
        const sectionHeight = section.offsetHeight;
        const sectionTop = section.offsetTop - 100;
        const sectionId = section.getAttribute('id');
        
        if (scrollY > sectionTop && scrollY <= sectionTop + sectionHeight) {
            document.querySelectorAll('.nav-link').forEach(link => {
                link.classList.remove('active');
                if (link.getAttribute('href') === `#${sectionId}`) {
                    link.classList.add('active');
                }
            });
        }
    });
});

console.log('🎉 Festiva Planner AI loaded successfully!');
