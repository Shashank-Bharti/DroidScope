// Depth slider value update
document.getElementById('maxDepth').addEventListener('input', function(e) {
    document.getElementById('depthValue').textContent = e.target.value;
});

// Clear logs function
function clearLogs() {
    const terminalOutput = document.getElementById('terminalOutput');
    terminalOutput.innerHTML = '<div class="log-entry log-info"><span class="log-timestamp">[00:00:00]</span><span class="log-message">Logs cleared</span></div>';
}

// Append log to terminal
let logStartTime = null;

function appendLog(message, type = 'info') {
    if (!logStartTime) {
        logStartTime = Date.now();
    }
    
    const terminalOutput = document.getElementById('terminalOutput');
    const elapsed = Date.now() - logStartTime;
    const seconds = Math.floor(elapsed / 1000);
    const minutes = Math.floor(seconds / 60);
    const hours = Math.floor(minutes / 60);
    
    const timestamp = `[${String(hours).padStart(2, '0')}:${String(minutes % 60).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}]`;
    
    // Handle multi-line messages - split and display each line with same timestamp
    const lines = message.split('\n');
    lines.forEach(line => {
        if (line.trim()) {  // Only display non-empty lines
            const logEntry = document.createElement('div');
            logEntry.className = `log-entry log-${type}`;
            logEntry.innerHTML = `<span class="log-timestamp">${timestamp}</span><span class="log-message">${line}</span>`;
            terminalOutput.appendChild(logEntry);
        }
    });
    
    terminalOutput.scrollTop = terminalOutput.scrollHeight;
}

// Start test
async function startTest() {
    const appName = document.getElementById('appName').value.trim();
    const category = document.getElementById('category').value;
    const maxDepth = parseInt(document.getElementById('maxDepth').value);
    
    // Validation
    if (!appName) {
        alert('Please enter an application name');
        return;
    }
    
    if (!category) {
        alert('Please select a category');
        return;
    }
    
    // Reset log start time
    logStartTime = null;
    clearLogs();
    
    // Hide config, show progress
    document.getElementById('configPanel').classList.add('hidden');
    document.getElementById('progressPanel').classList.remove('hidden');
    document.getElementById('resultsPanel').classList.add('hidden');
    
    try {
        appendLog('Starting test configuration...', 'info');
        
        // Show stop button
        document.getElementById('stopAgentBtn').classList.remove('hidden');
        
        // Start the test
        const response = await fetch('/api/run-test', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                app_name: appName,
                category: category,
                max_depth: maxDepth
            })
        });
        
        const data = await response.json();
        console.log('Test started:', data);
        appendLog(`Test initiated for ${appName}`, 'success');
        
        // Listen for progress updates and logs
        listenForProgress();
        listenForLogs();
        
    } catch (error) {
        console.error('Error starting test:', error);
        appendLog('Error: ' + error.message, 'error');
        alert('Error starting test: ' + error.message);
        resetTest();
    }
}

// Listen for SSE log updates
function listenForLogs() {
    const logSource = new EventSource('/api/logs');
    
    logSource.onmessage = function(event) {
        const data = JSON.parse(event.data);
        
        // Skip keepalive messages
        if (data.keepalive) return;
        
        // Display log message
        appendLog(data.message, data.type || 'info');
    };
    
    logSource.onerror = function(error) {
        console.error('Log SSE Error:', error);
        logSource.close();
    };
    
    // Store reference for cleanup
    window.logEventSource = logSource;
}

// Listen for SSE progress updates
function listenForProgress() {
    const eventSource = new EventSource('/api/progress');
    
    eventSource.onmessage = function(event) {
        const data = JSON.parse(event.data);
        
        // Skip keepalive messages
        if (data.keepalive) return;
        
        // Update progress
        updateProgress(data.message, data.percentage);
        
        // If complete, load results
        if (data.percentage >= 100) {
            eventSource.close();
            setTimeout(loadResults, 2000);
        } else if (data.percentage < 0) {
            // Error occurred
            eventSource.close();
            alert('Test failed: ' + data.message);
            resetTest();
        }
    };
    
    eventSource.onerror = function(error) {
        console.error('SSE Error:', error);
        eventSource.close();
    };
}

// Update progress bar and message
function updateProgress(message, percentage) {
    const progressBar = document.getElementById('progressBar');
    const progressMessage = document.getElementById('progressMessage');
    
    progressBar.style.width = percentage + '%';
    progressMessage.textContent = message;
}

// Load and display results
async function loadResults() {
    try {
        const response = await fetch('/api/results');
        const data = await response.json();
        
        if (data.error) {
            alert('Error loading results: ' + data.error);
            resetTest();
            return;
        }
        
        // Hide progress, show results
        document.getElementById('progressPanel').classList.add('hidden');
        document.getElementById('resultsPanel').classList.remove('hidden');
        
        // Display results
        displaySummary(data.summary);
        displayMetrics(data); // Pass entire data object with nested metrics
        displayPositive(data.positive);
        displayIssues(data.issues);
        displayRecommendations(data.recommendations || data.suggestions); // Handle both old and new field names
        
    } catch (error) {
        console.error('Error loading results:', error);
        alert('Error loading results: ' + error.message);
        resetTest();
    }
}

// Display summary
function displaySummary(summary) {
    const summaryContent = document.getElementById('summaryContent');
    summaryContent.innerHTML = marked.parse(summary || 'No summary available.');
}

// Display positive findings
function displayPositive(positive) {
    const positiveContent = document.getElementById('positiveContent');
    if (!positive || positive.length === 0) {
        positiveContent.innerHTML = '<p class="text-gray-400">No positive findings documented.</p>';
        return;
    }
    
    const html = positive.map(item => `
        <div class="result-card">
            <div class="result-card-header">
                <span class="result-card-title">${item.aspect || 'Positive Finding'}</span>
                <span class="result-badge badge-good">Good</span>
            </div>
            <div class="result-card-description">${item.description || 'No description available'}</div>
            ${item.location ? `
                <div class="result-card-meta">
                    <div class="result-card-meta-item"><strong>Location:</strong> ${item.location}</div>
                </div>
            ` : ''}
        </div>
    `).join('');
    
    positiveContent.innerHTML = html;
}

// Store chart instances globally
let depthChartInstance = null;
let complexityChartInstance = null;
let severityChartInstance = null;

// Display metrics with charts
function displayMetrics(data) {
    // Safely extract metrics from new comprehensive schema
    const navMetrics = data.navigation_metrics || {};
    const appMetadata = data.app_metadata || {};
    const complexityScore = data.complexity_score || 0;
    
    // Support both old flat structure and new nested structure
    const totalScreens = appMetadata.screens_discovered || navMetrics.screens_discovered || data.total_screens || 0;
    const maxDepth = navMetrics.max_depth || data.max_depth || 0;
    const avgDepth = navMetrics.avg_depth || data.avg_depth || 0;
    const hubScreens = navMetrics.hub_screen_count || data.hub_screen_count || 0;
    
    // Destroy previous depth chart if exists
    if (depthChartInstance) {
        depthChartInstance.destroy();
    }
    
    // Depth Chart
    depthChartInstance = new Chart(document.getElementById('depthChart'), {
        type: 'bar',
        data: {
            labels: ['Total Screens', 'Max Depth', 'Avg Depth', 'Hub Screens'],
            datasets: [{
                label: 'Navigation Metrics',
                data: [
                    totalScreens,
                    maxDepth,
                    avgDepth,
                    hubScreens
                ],
                backgroundColor: [
                    'rgba(255, 255, 255, 0.9)',
                    'rgba(200, 200, 200, 0.9)',
                    'rgba(150, 150, 150, 0.9)',
                    'rgba(100, 100, 100, 0.9)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Navigation Depth',
                    color: '#e0e0e0'
                },
                legend: { display: false }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: { color: '#a0a0a0' },
                    grid: { color: '#333333' }
                },
                x: {
                    ticks: { color: '#a0a0a0' },
                    grid: { color: '#333333' }
                }
            }
        }
    });
    
    // Destroy previous complexity chart if exists
    if (complexityChartInstance) {
        complexityChartInstance.destroy();
    }
    
    // Complexity Chart (Gauge-style)
    complexityChartInstance = new Chart(document.getElementById('complexityChart'), {
        type: 'doughnut',
        data: {
            labels: ['Complexity', 'Remaining'],
            datasets: [{
                data: [complexityScore, 10 - complexityScore],
                backgroundColor: [
                    complexityScore > 7 ? 'rgba(80, 80, 80, 0.9)' :
                    complexityScore > 4 ? 'rgba(150, 150, 150, 0.9)' :
                    'rgba(255, 255, 255, 0.9)',
                    'rgba(30, 30, 30, 0.3)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                title: {
                    display: true,
                    text: `Complexity Score: ${complexityScore}/10`,
                    color: '#e0e0e0'
                },
                legend: { display: false }
            }
        }
    });
    
    // Additional Stats Cards
    const interactionFeedback = data.interaction_feedback || {};
    const visualHierarchy = data.visual_hierarchy || {};
    const errorHandling = data.error_handling || {};
    const explorationCoverage = data.exploration_coverage || {};
    
    const additionalStatsHtml = `
        <div class="metric-stat-card">
            <div class="metric-stat-value">${maxDepth}</div>
            <div class="metric-stat-label">Max Depth</div>
        </div>
        <div class="metric-stat-card">
            <div class="metric-stat-value">${totalScreens}</div>
            <div class="metric-stat-label">Total Screens</div>
        </div>
        <div class="metric-stat-card">
            <div class="metric-stat-value">${interactionFeedback.silent_failures || 0}</div>
            <div class="metric-stat-label">Silent Failures</div>
        </div>
        <div class="metric-stat-card">
            <div class="metric-stat-value">${Math.round(interactionFeedback.visible_feedback_rate_pct || 0)}%</div>
            <div class="metric-stat-label">Feedback Rate</div>
        </div>
        <div class="metric-stat-card">
            <div class="metric-stat-value">${visualHierarchy.cta_visibility || 'N/A'}</div>
            <div class="metric-stat-label">CTA Clarity</div>
        </div>
        <div class="metric-stat-card">
            <div class="metric-stat-value">${errorHandling.preventable_errors || 0}</div>
            <div class="metric-stat-label">Preventable Errors</div>
        </div>
        <div class="metric-stat-card">
            <div class="metric-stat-value">${navMetrics.orphan_screens || 0}</div>
            <div class="metric-stat-label">Orphan Screens</div>
        </div>
        <div class="metric-stat-card">
            <div class="metric-stat-value">${Math.round(explorationCoverage.dead_elements_pct || 0)}%</div>
            <div class="metric-stat-label">Dead Elements</div>
        </div>
    `;
    
    document.getElementById('additionalStats').innerHTML = additionalStatsHtml;
}

// Display issues
function displayIssues(issues) {
    const issuesContent = document.getElementById('issuesContent');
    
    if (!issues || issues.length === 0) {
        issuesContent.innerHTML = '<p>No issues found.</p>';
        
        // Destroy previous severity chart if exists
        if (severityChartInstance) {
            severityChartInstance.destroy();
        }
        
        // Update severity chart with no data
        severityChartInstance = new Chart(document.getElementById('severityChart'), {
            type: 'pie',
            data: {
                labels: ['No Issues'],
                datasets: [{
                    data: [1],
                    backgroundColor: ['rgba(255, 255, 255, 0.7)']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: true,
                plugins: {
                    title: {
                        display: true,
                        text: 'Issue Severity Distribution',
                        color: '#e0e0e0'
                    }
                }
            }
        });
        return;
    }
    
    // Count severities with safe access
    const severityCounts = {
        High: 0,
        Medium: 0,
        Low: 0
    };
    
    issues.forEach(issue => {
        const severity = issue.severity || 'Medium'; // Default to Medium if undefined
        severityCounts[severity] = (severityCounts[severity] || 0) + 1;
    });
    
    // Destroy previous severity chart if exists
    if (severityChartInstance) {
        severityChartInstance.destroy();
    }
    
    // Severity Chart
    severityChartInstance = new Chart(document.getElementById('severityChart'), {
        type: 'pie',
        data: {
            labels: Object.keys(severityCounts),
            datasets: [{
                data: Object.values(severityCounts),
                backgroundColor: [
                    'rgba(100, 100, 100, 0.9)',
                    'rgba(180, 180, 180, 0.9)',
                    'rgba(255, 255, 255, 0.9)'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Issue Severity Distribution',
                    color: '#e0e0e0'
                },
                legend: {
                    labels: { color: '#e0e0e0' }
                }
            }
        }
    });
    
    // Display issues with safe property access
    const html = issues.map(issue => {
        const severity = issue.severity || 'Medium';
        const badgeClass = severity.toLowerCase();
        
        return `
            <div class="result-card">
                <div class="result-card-header">
                    <span class="result-card-title">${issue.category || 'Issue'}</span>
                    <span class="result-badge badge-${badgeClass}">${severity}</span>
                </div>
                <div class="result-card-description">${issue.description || 'No description available'}</div>
                ${issue.location || issue.impact || issue.effort ? `
                    <div class="result-card-meta">
                        ${issue.location ? `<div class="result-card-meta-item"><strong>Location:</strong> ${issue.location}</div>` : ''}
                        ${issue.impact ? `<div class="result-card-meta-item"><strong>Impact:</strong> ${issue.impact}</div>` : ''}
                        ${issue.effort ? `<div class="result-card-meta-item"><strong>Effort to Fix:</strong> ${issue.effort}</div>` : ''}
                    </div>
                ` : ''}
            </div>
        `;
    }).join('');
    
    issuesContent.innerHTML = html;
}

// Display recommendations (new schema) or suggestions (old schema)
function displayRecommendations(recommendations) {
    const suggestionsContent = document.getElementById('suggestionsContent');
    
    if (!recommendations || recommendations.length === 0) {
        suggestionsContent.innerHTML = '<p class="text-gray-400">No recommendations available.</p>';
        return;
    }
    
    const html = recommendations.map(rec => {
        // Support both old 'suggestions' format and new 'recommendations' format
        const priority = rec.priority || 'Medium';
        const title = rec.recommendation || rec.title || 'Recommendation';
        const rationale = rec.rationale || rec.impact || 'No details provided';
        const effort = rec.effort || 'Unknown';
        const expectedImpact = rec.expected_impact || {};
        
        const badgeClass = priority.toLowerCase();
        
        return `
            <div class="result-card">
                <div class="result-card-header">
                    <span class="result-card-title">${title}</span>
                    <span class="result-badge badge-${badgeClass}">${priority} Priority</span>
                </div>
                <div class="result-card-description">${rationale}</div>
                ${effort !== 'Unknown' || expectedImpact.task_success_increase_pct || expectedImpact.time_reduction_pct || expectedImpact.error_reduction_pct ? `
                    <div class="result-card-meta">
                        ${effort !== 'Unknown' ? `<div class="result-card-meta-item"><strong>Effort:</strong> ${effort}</div>` : ''}
                        ${expectedImpact.task_success_increase_pct ? `<div class="result-card-meta-item"><strong>Task Success Impact:</strong> +${expectedImpact.task_success_increase_pct}%</div>` : ''}
                        ${expectedImpact.time_reduction_pct ? `<div class="result-card-meta-item"><strong>Time Saved:</strong> ${expectedImpact.time_reduction_pct}%</div>` : ''}
                        ${expectedImpact.error_reduction_pct ? `<div class="result-card-meta-item"><strong>Error Reduction:</strong> ${expectedImpact.error_reduction_pct}%</div>` : ''}
                    </div>
                ` : ''}
            </div>
        `;
    }).join('');
    
    suggestionsContent.innerHTML = html;
}

// Download report
function downloadReport() {
    fetch('/api/results')
        .then(res => res.json())
        .then(data => {
            const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `ux-analysis-${Date.now()}.json`;
            a.click();
            URL.revokeObjectURL(url);
        });
}

// Stop agent execution
async function stopAgent() {
    if (confirm('Are you sure you want to stop the agent execution?')) {
        try {
            appendLog('Stopping agent...', 'warning');
            
            const response = await fetch('/api/stop-agent', {
                method: 'POST'
            });
            
            const data = await response.json();
            
            if (data.success) {
                appendLog('Agent stopped successfully', 'info');
                document.getElementById('stopAgentBtn').classList.add('hidden');
                updateProgress('Agent execution stopped by user', -1);
            } else {
                appendLog('Failed to stop agent: ' + data.error, 'error');
            }
        } catch (error) {
            appendLog('Error stopping agent: ' + error.message, 'error');
        }
    }
}

// Reset test
function resetTest() {
    // Hide stop button
    document.getElementById('stopAgentBtn').classList.add('hidden');
    
    // Close event sources if they exist
    if (window.logEventSource) {
        window.logEventSource.close();
        window.logEventSource = null;
    }
    
    document.getElementById('configPanel').classList.remove('hidden');
    document.getElementById('progressPanel').classList.add('hidden');
    document.getElementById('resultsPanel').classList.add('hidden');
    
    // Reset form
    document.getElementById('appName').value = '';
    document.getElementById('category').value = '';
    document.getElementById('maxDepth').value = 6;
    document.getElementById('depthValue').textContent = '6';
    
    // Reset logs
    logStartTime = null;
    clearLogs();
}
