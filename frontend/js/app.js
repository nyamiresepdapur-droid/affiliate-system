// Load API URL from config or use default
// Production: Railway backend
// Development: Localhost
const API_URL = (typeof window !== 'undefined' && window.API_URL) || 
                (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1'
                    ? 'https://affiliate-system-production.up.railway.app/api'
                    : 'http://localhost:5000/api');
let currentUser = null;
let token = null;

// Check if already logged in
if (localStorage.getItem('token')) {
    token = localStorage.getItem('token');
    const savedUser = localStorage.getItem('user');
    if (savedUser) {
        try {
            currentUser = JSON.parse(savedUser);
            // Verify token is still valid by checking dashboard
            verifyTokenAndShowDashboard();
        } catch (e) {
            console.error('Error parsing saved user:', e);
            clearAuth();
        }
    } else {
        clearAuth();
    }
} else {
    // No token, show login
    token = null;
    currentUser = null;
}

function verifyTokenAndShowDashboard() {
    // Try to load dashboard to verify token
    if (!token) {
        showLogin();
        return;
    }
    
    loadDashboard().then(() => {
        showDashboard();
    }).catch((error) => {
        console.error('Token verification failed:', error);
        clearAuth();
        showLogin();
    });
}

function clearAuth() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    token = null;
    currentUser = null;
}

// ==================== AUTH ====================
document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('loginUsername').value;
    const password = document.getElementById('loginPassword').value;
    
    try {
        const res = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });
        
        // Check if response is JSON
        const contentType = res.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            const text = await res.text();
            console.error('Non-JSON response from login:', text.substring(0, 200));
            showAlert('loginAlert', `Backend error: Server returned HTML instead of JSON. Pastikan backend running di ${API_URL.replace('/api', '')}`, 'error');
            return;
        }
        
        const data = await res.json();
        if (res.ok) {
            token = data.token;
            currentUser = data.user;
            localStorage.setItem('token', token);
            localStorage.setItem('user', JSON.stringify(currentUser));
            showDashboard();
        } else {
            showAlert('loginAlert', data.error || 'Login gagal', 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        showAlert('loginAlert', `Connection error: ${error.message}. Pastikan backend sudah running di ${API_URL.replace('/api', '')}!`, 'error');
    }
});

document.getElementById('registerForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const data = {
        username: document.getElementById('regUsername').value,
        email: document.getElementById('regEmail').value,
        full_name: document.getElementById('regFullName').value,
        password: document.getElementById('regPassword').value,
        role: document.getElementById('regRole').value
    };
    
    try {
        const res = await fetch(`${API_URL}/auth/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        
        const result = await res.json();
        if (res.ok) {
            showAlert('registerAlert', 'Register berhasil! Silakan login.', 'success');
            setTimeout(() => showLogin(), 2000);
        } else {
            showAlert('registerAlert', result.error, 'error');
        }
    } catch (error) {
        showAlert('registerAlert', 'Connection error', 'error');
    }
});

function showLogin() {
    document.getElementById('loginForm').style.display = 'block';
    document.getElementById('registerForm').style.display = 'none';
}

function showRegister() {
    document.getElementById('loginForm').style.display = 'none';
    document.getElementById('registerForm').style.display = 'block';
}

function showDashboard() {
    document.getElementById('loginScreen').classList.add('hidden');
    document.getElementById('dashboard').classList.remove('hidden');
    document.getElementById('userName').textContent = currentUser.full_name || currentUser.username;
    document.getElementById('userRole').textContent = currentUser.role.toUpperCase();
    document.getElementById('userRole').className = `badge badge-${currentUser.role === 'owner' ? 'success' : currentUser.role === 'manager' ? 'info' : 'warning'}`;
    
    // Hide/show buttons and navigation based on role
    if (currentUser.role !== 'owner') {
        // Hide admin-only buttons
        document.getElementById('btnAddProduct')?.classList.add('hidden');
        document.getElementById('btnAddTeam')?.classList.add('hidden');
        document.getElementById('btnAddCommission')?.classList.add('hidden');
        document.getElementById('btnCalculatePayment')?.classList.add('hidden');
        document.getElementById('productsActions')?.classList.add('hidden');
        document.getElementById('teamsActions')?.classList.add('hidden');
        document.getElementById('contentActions')?.classList.add('hidden');
        
        // Hide admin-only navigation buttons
        document.getElementById('navUsers')?.style.setProperty('display', 'none');
        document.getElementById('navReports')?.style.setProperty('display', 'none');
        document.getElementById('navTeams')?.style.setProperty('display', 'none');
        document.getElementById('navContent')?.style.setProperty('display', 'none');
        document.getElementById('navCommissions')?.style.setProperty('display', 'none');
        document.getElementById('navPayments')?.style.setProperty('display', 'none');
        document.getElementById('navDailyCommissions')?.style.setProperty('display', 'none');
        document.getElementById('navVideoStatistics')?.style.setProperty('display', 'none');
        document.getElementById('navMemberSummary')?.style.setProperty('display', 'none');
        document.getElementById('navSyncSheets')?.style.setProperty('display', 'none');
    } else {
        // Show admin navigation for owner
        document.getElementById('navUsers')?.style.setProperty('display', 'inline-block');
        document.getElementById('navReports')?.style.setProperty('display', 'inline-block');
        document.getElementById('navTeams')?.style.setProperty('display', 'inline-block');
        document.getElementById('navContent')?.style.setProperty('display', 'inline-block');
        document.getElementById('navCommissions')?.style.setProperty('display', 'inline-block');
        document.getElementById('navPayments')?.style.setProperty('display', 'inline-block');
        document.getElementById('navDailyCommissions')?.style.setProperty('display', 'inline-block');
        document.getElementById('navVideoStatistics')?.style.setProperty('display', 'inline-block');
        document.getElementById('navMemberSummary')?.style.setProperty('display', 'inline-block');
        document.getElementById('navSyncSheets')?.style.setProperty('display', 'inline-block');
        document.getElementById('navBotStatus')?.style.setProperty('display', 'inline-block');
    }
    
    loadDashboard();
    
    // Start notification polling
    startNotificationPolling();
}

function logout() {
    // Stop notification polling
    stopNotificationPolling();
    
    clearAuth();
    document.getElementById('loginScreen').classList.remove('hidden');
    document.getElementById('dashboard').classList.add('hidden');
}

function clearAuth() {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    token = null;
    currentUser = null;
}

function showLogin() {
    document.getElementById('loginScreen').classList.remove('hidden');
    document.getElementById('dashboard').classList.add('hidden');
}

// Helper function untuk fetch dengan auto-handle auth
async function authenticatedFetch(url, options = {}) {
    // Get token from localStorage if not in memory
    if (!token) {
        token = localStorage.getItem('token');
    }
    
    if (!token) {
        clearAuth();
        showLogin();
        throw new Error('No token available. Please login.');
    }
    
    const defaultHeaders = {
        'Authorization': `Bearer ${token}`
    };
    
    // Only add Content-Type for requests with body (POST, PUT, PATCH)
    if (options.method && ['POST', 'PUT', 'PATCH'].includes(options.method.toUpperCase())) {
        defaultHeaders['Content-Type'] = 'application/json';
    }
    
    // Merge headers - ensure Authorization is always included
    const mergedHeaders = {
        ...defaultHeaders,
        ...(options.headers || {})
    };
    
    // Ensure Authorization header is set
    if (!mergedHeaders['Authorization']) {
        mergedHeaders['Authorization'] = `Bearer ${token}`;
    }
    
    const mergedOptions = {
        ...options,
        headers: mergedHeaders
    };
    
    console.log('authenticatedFetch:', url, 'Headers:', mergedHeaders);
    
    const res = await fetch(url, mergedOptions);
    
    // Handle 401 Unauthorized
    if (res.status === 401) {
        clearAuth();
        showLogin();
        const error = await res.json().catch(() => ({ error: 'Session expired' }));
        throw new Error(error.error || error.msg || 'Session expired. Please login again.');
    }
    
    // Handle 404 Not Found
    if (res.status === 404) {
        const contentType = res.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            const error = await res.json().catch(() => ({ error: 'Endpoint not found' }));
            throw new Error(error.error || 'Endpoint not found. Pastikan backend running dan endpoint tersedia.');
        } else {
            throw new Error('Endpoint not found (404). Pastikan backend running di http://localhost:5000');
        }
    }
    
    // Handle other errors (403, 500, etc)
    if (!res.ok) {
        const contentType = res.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            const error = await res.json().catch(() => ({ error: `HTTP ${res.status}` }));
            throw new Error(error.error || error.message || `HTTP ${res.status}: ${res.statusText}`);
        } else {
            const text = await res.text();
            throw new Error(`Server error: HTTP ${res.status}. Pastikan backend running di http://localhost:5000`);
        }
    }
    
    return res;
}

function showSection(section) {
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
    document.getElementById(`section-${section}`).classList.add('active');
    if (event && event.target) {
        event.target.classList.add('active');
    }
    
    // Load data based on section
    if (section === 'products') loadProducts();
    else if (section === 'users') loadUsers();
    else if (section === 'reports') loadReports();
    else if (section === 'my-reports') loadMyReports();
    else if (section === 'my-commissions') loadMyCommissions();
    else if (section === 'my-payments') loadMyPayments();
    else if (section === 'my-profile') loadMyProfile();
    else if (section === 'teams') loadTeams();
    else if (section === 'content') loadContent();
    else if (section === 'commissions') loadCommissions();
    else if (section === 'payments') loadPayments();
    else if (section === 'daily-commissions') loadDailyCommissions();
    else if (section === 'video-statistics') loadVideoStatistics();
    else if (section === 'member-summary') loadMemberSummary();
    else if (section === 'bot-status') checkBotStatus();
    else if (section === 'dashboard') loadDashboard();
}

// ==================== DASHBOARD ====================
function applyDashboardFilter() {
    loadDashboard();
}

function resetDashboardFilter() {
    document.getElementById('dashboardDateFrom').value = '';
    document.getElementById('dashboardDateTo').value = '';
    loadDashboard();
}

async function loadDashboard() {
    try {
        // Get date filters
        const dateFrom = document.getElementById('dashboardDateFrom')?.value || '';
        const dateTo = document.getElementById('dashboardDateTo')?.value || '';
        
        // Build URL with date filters and timestamp to prevent cache
        let url = `${API_URL}/dashboard/stats`;
        const params = [];
        if (dateFrom) params.push(`date_from=${dateFrom}`);
        if (dateTo) params.push(`date_to=${dateTo}`);
        params.push(`t=${Date.now()}`); // Prevent cache
        if (params.length > 0) url += '?' + params.join('&');
        
        const res = await authenticatedFetch(url);
        
        // Check if response is JSON
        const contentType = res.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            const text = await res.text();
            console.error('Non-JSON response:', text.substring(0, 200));
            throw new Error(`Server returned HTML instead of JSON. Status: ${res.status}. Make sure backend is running on ${API_URL}`);
        }
        
        if (!res.ok) {
            const error = await res.json().catch(() => ({ error: `HTTP ${res.status}: ${res.statusText}` }));
            throw new Error(error.error || `HTTP ${res.status}`);
        }
        
        const stats = await res.json();
        
        const statsGrid = document.getElementById('statsGrid');
        statsGrid.innerHTML = '';
        
        // User Metrics
        if (stats.total_users !== undefined) {
            addStatCard(statsGrid, '👥 Total Users', stats.total_users, 'users');
            addStatCard(statsGrid, '✅ Active Users (30d)', stats.active_users, 'users');
            if (stats.recent_users !== undefined) {
                addStatCard(statsGrid, '🆕 New Users (7d)', stats.recent_users, 'users');
            }
        }
        
        // Video Metrics
        if (stats.total_videos !== undefined) {
            addStatCard(statsGrid, '🎬 Total Videos', stats.total_videos, 'videos');
            addStatCard(statsGrid, '📅 Videos This Month', stats.videos_this_month, 'videos');
            addStatCard(statsGrid, '⏳ Pending Videos', stats.pending_videos, 'videos');
            addStatCard(statsGrid, '✅ Approved Videos', stats.approved_videos, 'videos');
            if (stats.approval_rate !== undefined) {
                addStatCard(statsGrid, '📊 Approval Rate', stats.approval_rate + '%', 'percentage');
            }
        }
        
        // Quality Metrics
        if (stats.avg_quality_score !== undefined) {
            addStatCard(statsGrid, '⭐ Avg Quality Score', stats.avg_quality_score + '/10', 'score');
            addStatCard(statsGrid, '🌟 High Quality Videos', stats.high_quality_videos, 'videos');
        }
        
        // Commission Metrics
        if (stats.total_commissions !== undefined) {
            addStatCard(statsGrid, '💰 Total Commissions', formatCurrency(stats.total_commissions), 'money');
            addStatCard(statsGrid, '💵 Owner Earnings', formatCurrency(stats.owner_earnings), 'money');
            addStatCard(statsGrid, '👨‍👩‍👧‍👦 Team Earnings', formatCurrency(stats.team_earnings), 'money');
            addStatCard(statsGrid, '⏳ Pending Commissions', formatCurrency(stats.pending_commissions), 'money');
        }
        
        // Team Metrics
        if (stats.total_teams !== undefined) {
            addStatCard(statsGrid, '👥 Total Teams', stats.total_teams, 'teams');
            addStatCard(statsGrid, '👤 Total Members', stats.total_members, 'members');
        }
        
        // Payment Metrics
        if (stats.total_payments !== undefined) {
            addStatCard(statsGrid, '💳 Total Paid', formatCurrency(stats.total_payments), 'money');
            addStatCard(statsGrid, '⏳ Pending Payments', formatCurrency(stats.pending_payments), 'money');
        }
        
        // Top Performers
        if (stats.top_earners && stats.top_earners.length > 0) {
            const topEarnersList = document.getElementById('topEarnersList');
            topEarnersList.innerHTML = stats.top_earners.map((earner, index) => `
                <div style="display: flex; justify-content: space-between; padding: 10px; border-bottom: 1px solid #eee;">
                    <div>
                        <strong>${index + 1}. ${earner.name}</strong>
                    </div>
                    <div style="color: #28a745; font-weight: bold;">
                        ${formatCurrency(earner.earnings)}
                    </div>
                </div>
            `).join('');
        }
        
        if (stats.top_videos && stats.top_videos.length > 0) {
            const topVideosList = document.getElementById('topVideosList');
            topVideosList.innerHTML = stats.top_videos.map((video, index) => `
                <div style="padding: 10px; border-bottom: 1px solid #eee;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                        <strong>${index + 1}. ${video.title}</strong>
                        <span style="color: #ffc107; font-weight: bold;">⭐ ${video.score}</span>
                    </div>
                    <div style="font-size: 0.9em; color: #666;">
                        By: ${video.creator}
                    </div>
                    ${video.link ? `<div style="font-size: 0.85em; margin-top: 5px;"><a href="${video.link}" target="_blank" style="color: #007bff;">View Video →</a></div>` : ''}
                </div>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading dashboard:', error);
    }
}

function addStatCard(container, label, value, type) {
    const card = document.createElement('div');
    card.className = 'stat-card';
    
    // Add icon/color based on type
    let cardClass = '';
    if (type === 'money') cardClass = 'stat-card-money';
    else if (type === 'users') cardClass = 'stat-card-users';
    else if (type === 'videos') cardClass = 'stat-card-videos';
    else if (type === 'percentage') cardClass = 'stat-card-percentage';
    else if (type === 'score') cardClass = 'stat-card-score';
    
    if (cardClass) card.className += ' ' + cardClass;
    
    card.innerHTML = `
        <h3>${label}</h3>
        <div class="value">${value}</div>
    `;
    container.appendChild(card);
}

// ==================== USERS ====================
async function loadUsers() {
    if (currentUser.role !== 'owner') {
        alert('Hanya owner yang bisa melihat semua users');
        return;
    }
    
    try {
        const res = await authenticatedFetch(`${API_URL}/users`);
        
        // Check if response is JSON
        const contentType = res.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            const text = await res.text();
            console.error('Non-JSON response from users:', text.substring(0, 200));
            throw new Error(`Server returned HTML instead of JSON. Status: ${res.status}. Pastikan backend running di ${API_URL.replace('/api', '')}`);
        }
        
        const data = await res.json();
        
        // Handle pagination response format (same as products)
        const users = Array.isArray(data.users) ? data.users : (Array.isArray(data) ? data : []);
        
        console.log('Loaded users:', users.length, 'items');
        console.log('Users data:', users);
        
        const tbody = document.getElementById('usersTable');
        if (!tbody) {
            console.error('usersTable element not found');
            return;
        }
        
        if (users.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" style="text-align: center;">Belum ada user terdaftar</td></tr>';
        } else {
            tbody.innerHTML = users.map(u => `
                <tr>
                    <td><strong>${u.full_name || u.username || 'N/A'}</strong></td>
                    <td>${u.whatsapp || '-'}</td>
                    <td>${u.tiktok_akun || '-'}</td>
                    <td>${u.email || '-'}</td>
                    <td>${u.telegram_username ? '@' + u.telegram_username : '-'}</td>
                    <td>${u.created_at || '-'}</td>
                    <td><span class="badge badge-success">${u.status || 'Active'}</span></td>
                    <td>
                        ${currentUser.role === 'owner' ? `
                            <button class="btn btn-primary btn-sm" onclick="editUser(${u.id})" style="margin-right: 5px;">✏️ Edit</button>
                        ` : ''}
                    </td>
                </tr>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading users:', error);
        const tbody = document.getElementById('usersTable');
        if (tbody) {
            tbody.innerHTML = `<tr><td colspan="8" style="text-align: center; padding: 20px; color: #dc3545;">Error loading users: ${error.message}</td></tr>`;
        }
        alert('Error loading users: ' + error.message);
    }
}

async function editUser(userId) {
    try {
        const res = await authenticatedFetch(`${API_URL}/users`);
        const data = await res.json();
        // Handle pagination response format
        const users = Array.isArray(data.users) ? data.users : (Array.isArray(data) ? data : []);
        const user = users.find(u => u.id === userId);
        
        if (!user) {
            alert('User tidak ditemukan');
            return;
        }
        
        const modalBody = document.getElementById('modalBody');
        modalBody.innerHTML = `
            <h2>Edit User</h2>
            <form id="editUserForm">
                <div class="form-group">
                    <label>Nama Lengkap *</label>
                    <input type="text" id="editFullName" value="${user.full_name || ''}" required>
                </div>
                <div class="form-group">
                    <label>Email</label>
                    <input type="email" id="editEmail" value="${user.email || ''}">
                </div>
                <div class="form-group">
                    <label>WhatsApp</label>
                    <input type="text" id="editWhatsapp" value="${user.whatsapp || ''}">
                </div>
                <div class="form-group">
                    <label>TikTok Akun</label>
                    <input type="text" id="editTiktokAkun" value="${user.tiktok_akun || ''}">
                </div>
                <div class="form-group">
                    <label>Telegram Username</label>
                    <input type="text" id="editTelegramUsername" value="${user.telegram_username || ''}" placeholder="@username">
                </div>
                <div class="form-group">
                    <label>Wallet (DANA/OVO/GoPay)</label>
                    <input type="text" id="editWallet" value="${user.wallet || ''}">
                </div>
                <div class="form-group">
                    <label>Bank Account</label>
                    <input type="text" id="editBankAccount" value="${user.bank_account || ''}">
                </div>
                <button type="submit" class="btn btn-primary btn-block">Update User</button>
            </form>
        `;
        document.getElementById('modal').classList.remove('hidden');
        
        document.getElementById('editUserForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            const data = {
                full_name: document.getElementById('editFullName').value,
                email: document.getElementById('editEmail').value,
                whatsapp: document.getElementById('editWhatsapp').value,
                tiktok_akun: document.getElementById('editTiktokAkun').value,
                telegram_username: document.getElementById('editTelegramUsername').value,
                wallet: document.getElementById('editWallet').value,
                bank_account: document.getElementById('editBankAccount').value
            };
            
            try {
                const res = await authenticatedFetch(`${API_URL}/users/${userId}`, {
                    method: 'PUT',
                    body: JSON.stringify(data)
                });
                
                if (res.ok) {
                    closeModal();
                    loadUsers();
                    alert('User berhasil diupdate!');
                } else {
                    const error = await res.json();
                    alert('Error: ' + (error.error || 'Update gagal'));
                }
            } catch (error) {
                alert('Error: ' + error.message);
            }
        });
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// ==================== REPORTS ====================
function resetReportFilter() {
    document.getElementById('reportStatusFilter').value = '';
    document.getElementById('reportDateFrom').value = '';
    document.getElementById('reportDateTo').value = '';
    loadReports();
}

async function loadReports() {
    try {
        const statusFilter = document.getElementById('reportStatusFilter')?.value || '';
        const dateFrom = document.getElementById('reportDateFrom')?.value || '';
        const dateTo = document.getElementById('reportDateTo')?.value || '';
        
        // Build URL with filters
        const params = [];
        if (statusFilter) params.push(`status=${statusFilter}`);
        if (dateFrom) params.push(`date_from=${dateFrom}`);
        if (dateTo) params.push(`date_to=${dateTo}`);
        
        const url = params.length > 0 ? `${API_URL}/reports?${params.join('&')}` : `${API_URL}/reports`;
        const res = await authenticatedFetch(url);
        
        // Check if response is JSON
        const contentType = res.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            const text = await res.text();
            console.error('Non-JSON response from reports:', text.substring(0, 200));
            throw new Error(`Server returned HTML instead of JSON. Status: ${res.status}. Pastikan backend running di ${API_URL.replace('/api', '')}`);
        }
        
        const data = await res.json();
        
        // Handle pagination response format (same as products and users)
        const reports = Array.isArray(data.reports) ? data.reports : (Array.isArray(data) ? data : []);
        
        console.log('Loaded reports:', reports.length, 'items');
        console.log('Reports data:', reports);
        console.log('Current user:', currentUser);
        console.log('Current user role:', currentUser?.role);
        
        const tbody = document.getElementById('reportsTable');
        if (reports.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" style="text-align: center;">Belum ada laporan</td></tr>';
        } else {
            tbody.innerHTML = reports.map(r => {
                const isOwner = currentUser && currentUser.role === 'owner';
                const isPending = (r.status || 'pending') === 'pending';
                const reportId = r.id || r.report_id || 0;
                
                console.log(`Report ${reportId}: status=${r.status}, isOwner=${isOwner}, isPending=${isPending}`);
                
                let actionButtons = '-';
                if (isOwner && isPending) {
                    actionButtons = `
                        <button class="btn btn-success btn-sm" onclick="approveReport(${reportId})" style="margin-right: 5px;">✅ Approve</button>
                        <button class="btn btn-danger btn-sm" onclick="rejectReport(${reportId})">❌ Reject</button>
                    `;
                } else if (r.status === 'approved') {
                    actionButtons = '<span style="color: #28a745;">✓ Approved</span>';
                } else if (r.status === 'rejected') {
                    actionButtons = '<span style="color: #dc3545;">✗ Rejected</span>';
                }
                
                return `
                <tr>
                    <td>${r.created_at || '-'}</td>
                    <td><strong>${r.user_name || r.creator_name || 'Unknown'}</strong></td>
                    <td><a href="${r.link_video || '#'}" target="_blank" rel="noopener noreferrer" style="color: #007bff;">${(r.link_video || '').substring(0, 40)}...</a></td>
                    <td>${r.tanggal_upload || '-'}</td>
                    <td>${r.tiktok_akun || '-'}</td>
                    <td><span class="badge badge-${r.status === 'approved' ? 'success' : r.status === 'rejected' ? 'danger' : 'warning'}">${r.status || 'pending'}</span></td>
                    <td>${actionButtons}</td>
                </tr>
            `;
            }).join('');
        }
    } catch (error) {
        console.error('Error loading reports:', error);
        const tbody = document.getElementById('reportsTable');
        if (tbody) {
            tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; padding: 20px; color: #dc3545;">Error loading reports: ${error.message}</td></tr>`;
        }
        alert('Error loading reports: ' + error.message);
    }
}

async function approveReport(reportId) {
    if (!confirm('Approve report ini?')) return;
    
    try {
        const res = await authenticatedFetch(`${API_URL}/reports/${reportId}/approve`, {
            method: 'POST',
            body: JSON.stringify({ quality_score: 7 }) // Default quality score
        });
        
        if (res.ok) {
            alert('Report berhasil diapprove!');
            loadReports();
            loadDashboard();
        } else {
            const error = await res.json();
            alert('Error: ' + (error.error || 'Approve gagal'));
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function rejectReport(reportId) {
    const notes = prompt('Alasan reject (optional):');
    if (notes === null) return; // User cancelled
    
    try {
        const res = await authenticatedFetch(`${API_URL}/reports/${reportId}/reject`, {
            method: 'POST',
            body: JSON.stringify({ notes: notes || '' })
        });
        
        if (res.ok) {
            alert('Report berhasil direject');
            loadReports();
            loadDashboard();
        } else {
            const error = await res.json();
            alert('Error: ' + (error.error || 'Reject gagal'));
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// ==================== GOOGLE SHEETS SYNC ====================
async function syncGoogleSheets(e) {
    if (currentUser.role !== 'owner') {
        alert('Hanya owner yang bisa sync Google Sheets');
        return;
    }
    
    if (!confirm('Sync data dari Google Sheets ke database? Ini akan update data yang ada.')) {
        return;
    }
    
    const btn = (e && e.target) ? e.target : event.target;
    const originalText = btn.textContent;
    btn.textContent = '🔄 Syncing...';
    btn.disabled = true;
    
    try {
        const res = await authenticatedFetch(`${API_URL}/google-sheets/sync`, {
            method: 'POST'
        });
        
        const data = await res.json();
        if (res.ok) {
            // Show sync results with counts
            let message = 'Sync berhasil! Data dari Google Sheets sudah di-update ke database.';
            if (data.counts) {
                message += `\n\nData yang di-sync:\n`;
                message += `- Products: ${data.counts.products}\n`;
                message += `- Users: ${data.counts.users}\n`;
                message += `- Reports: ${data.counts.reports}`;
            }
            alert(message);
            // Always reload all sections to show synced data
            await loadProducts();
            await loadUsers();
            await loadReports();
            await loadDashboard(); // Refresh dashboard to show updated data
            // Switch to dashboard to see updated stats
            showSection('dashboard');
        } else {
            alert('Error: ' + (data.error || 'Sync gagal'));
        }
    } catch (error) {
        alert('Connection error: ' + error.message);
    } finally {
        btn.textContent = originalText;
        btn.disabled = false;
    }
}

// ==================== PRODUCTS ====================
let currentProductPage = 1;
let productsPerPage = 20;
let totalProducts = 0;
let totalProductPages = 0;

async function loadProducts(page = 1) {
    try {
        currentProductPage = page;
        const search = document.getElementById('productSearch')?.value || '';
        let url = `${API_URL}/products?page=${page}&per_page=${productsPerPage}`;
        if (search) {
            url += `&search=${encodeURIComponent(search)}`;
        }
        
        const res = await authenticatedFetch(url);
        
        // Check if response is JSON
        const contentType = res.headers.get('content-type');
        if (!contentType || !contentType.includes('application/json')) {
            const text = await res.text();
            console.error('Non-JSON response from products:', text.substring(0, 200));
            throw new Error(`Server returned HTML instead of JSON. Status: ${res.status}. Pastikan backend running di ${API_URL.replace('/api', '')}`);
        }
        
        const data = await res.json();
        
        // Handle pagination response format
        const products = Array.isArray(data.products) ? data.products : (Array.isArray(data) ? data : []);
        const pagination = data.pagination || {};
        
        totalProducts = pagination.total || products.length;
        totalProductPages = pagination.pages || 1;
        currentProductPage = pagination.page || page;
        
        console.log('Loaded products:', products.length, 'items, page:', currentProductPage, 'of', totalProductPages, 'total:', totalProducts);
        
        const tbody = document.getElementById('productsTable');
        if (!tbody) {
            console.error('productsTable element not found');
            return;
        }
        
        // Update pagination info
        const paginationInfo = document.getElementById('productsPaginationInfo');
        if (paginationInfo) {
            const start = (currentProductPage - 1) * productsPerPage + 1;
            const end = Math.min(start + products.length - 1, totalProducts);
            paginationInfo.textContent = `Menampilkan ${start}-${end} dari ${totalProducts} produk`;
        }
        
        if (products.length === 0) {
            tbody.innerHTML = '<tr><td colspan="10" style="text-align: center; padding: 20px;">Belum ada produk. Klik "Tambah Produk" untuk menambah produk baru atau klik "Sync Google Sheets" untuk sync dari Google Sheets.</td></tr>';
            // Hide pagination
            const paginationDiv = document.getElementById('productsPagination');
            if (paginationDiv) paginationDiv.innerHTML = '';
            return;
        }
        
        // Calculate row number (starting from 1 for current page)
        const startRowNumber = (currentProductPage - 1) * productsPerPage + 1;
        
        tbody.innerHTML = products.map((p, index) => {
            const rowNumber = startRowNumber + index;
            return `
            <tr>
                <td><input type="checkbox" class="product-checkbox" value="${p.id}" onchange="updateSelectAllCheckbox()"></td>
                <td><strong>${rowNumber}</strong></td>
                <td><strong>${p.product_name || 'N/A'}</strong></td>
                <td>${formatCurrency(p.product_price || 0)}</td>
                <td><a href="${p.product_link || '#'}" target="_blank" rel="noopener noreferrer" style="color: #007bff; text-decoration: none;">${(p.product_link || '').substring(0, 40)}${(p.product_link || '').length > 40 ? '...' : ''}</a></td>
                <td>${formatCurrency(p.regular_commission || 0)}</td>
                <td>${formatCurrency(p.gmv_max_commission || 0)}</td>
                <td>${p.target_gmv && p.target_gmv > 0 ? formatCurrency(p.target_gmv) : '0'}</td>
                <td><span class="badge badge-${p.status === 'active' ? 'success' : 'warning'}">${p.status || 'active'}</span></td>
                ${currentUser.role === 'owner' ? `<td>
                    <button class="btn btn-primary" onclick="editProduct(${p.id})" style="margin-right: 5px; padding: 5px 10px; font-size: 12px;">Edit</button>
                    <button class="btn btn-danger" onclick="deleteProduct(${p.id})" style="padding: 5px 10px; font-size: 12px;">Hapus</button>
                </td>` : '<td></td>'}
            </tr>
        `;
        }).join('');
        
        // Update pagination controls
        updateProductsPagination();
    } catch (error) {
        console.error('Error loading products:', error);
        const tbody = document.getElementById('productsTable');
        if (tbody) {
            tbody.innerHTML = `<tr><td colspan="10" style="text-align: center; padding: 20px; color: #dc3545;">Error loading products: ${error.message}</td></tr>`;
        }
        alert('Error loading products: ' + error.message);
    }
}

function updateProductsPagination() {
    const paginationDiv = document.getElementById('productsPagination');
    if (!paginationDiv) return;
    
    if (totalProductPages <= 1) {
        paginationDiv.innerHTML = '';
        return;
    }
    
    let paginationHTML = '';
    
    // Previous button
    if (currentProductPage > 1) {
        paginationHTML += `<button class="btn btn-secondary" onclick="loadProducts(${currentProductPage - 1})" style="padding: 8px 15px;">« Sebelumnya</button>`;
    } else {
        paginationHTML += `<button class="btn btn-secondary" disabled style="padding: 8px 15px;">« Sebelumnya</button>`;
    }
    
    // Page numbers
    const maxPagesToShow = 5;
    let startPage = Math.max(1, currentProductPage - Math.floor(maxPagesToShow / 2));
    let endPage = Math.min(totalProductPages, startPage + maxPagesToShow - 1);
    
    if (endPage - startPage < maxPagesToShow - 1) {
        startPage = Math.max(1, endPage - maxPagesToShow + 1);
    }
    
    if (startPage > 1) {
        paginationHTML += `<button class="btn btn-secondary" onclick="loadProducts(1)" style="padding: 8px 12px;">1</button>`;
        if (startPage > 2) {
            paginationHTML += `<span style="padding: 8px;">...</span>`;
        }
    }
    
    for (let i = startPage; i <= endPage; i++) {
        if (i === currentProductPage) {
            paginationHTML += `<button class="btn btn-primary" disabled style="padding: 8px 12px; font-weight: bold;">${i}</button>`;
        } else {
            paginationHTML += `<button class="btn btn-secondary" onclick="loadProducts(${i})" style="padding: 8px 12px;">${i}</button>`;
        }
    }
    
    if (endPage < totalProductPages) {
        if (endPage < totalProductPages - 1) {
            paginationHTML += `<span style="padding: 8px;">...</span>`;
        }
        paginationHTML += `<button class="btn btn-secondary" onclick="loadProducts(${totalProductPages})" style="padding: 8px 12px;">${totalProductPages}</button>`;
    }
    
    // Next button
    if (currentProductPage < totalProductPages) {
        paginationHTML += `<button class="btn btn-secondary" onclick="loadProducts(${currentProductPage + 1})" style="padding: 8px 15px;">Selanjutnya »</button>`;
    } else {
        paginationHTML += `<button class="btn btn-secondary" disabled style="padding: 8px 15px;">Selanjutnya »</button>`;
    }
    
    paginationDiv.innerHTML = paginationHTML;
}

function toggleSelectAllProducts() {
    const selectAll = document.getElementById('selectAllProducts');
    const checkboxes = document.querySelectorAll('.product-checkbox');
    if (selectAll) {
        checkboxes.forEach(cb => {
            cb.checked = selectAll.checked;
        });
    }
}

function updateSelectAllCheckbox() {
    const selectAll = document.getElementById('selectAllProducts');
    const checkboxes = document.querySelectorAll('.product-checkbox');
    if (selectAll && checkboxes.length > 0) {
        const allChecked = Array.from(checkboxes).every(cb => cb.checked);
        selectAll.checked = allChecked;
    }
}

async function showAddProductModal() {
    // Load categories
    let categories = [];
    try {
        const catRes = await authenticatedFetch(`${API_URL}/products/categories`);
        categories = await catRes.json();
    } catch (error) {
        console.error('Error loading categories:', error);
        categories = ['Fashion & Apparel', 'Beauty & Personal Care', 'Electronics', 'Other'];
    }
    
    const modalBody = document.getElementById('modalBody');
    modalBody.innerHTML = `
        <h2>➕ Tambah Produk</h2>
        <div style="margin-bottom: 20px; border-bottom: 2px solid #ddd; display: flex; gap: 0;">
            <button type="button" class="btn btn-secondary" onclick="switchProductTab('manual')" id="tabManual" style="border-radius: 4px 4px 0 0; margin-right: 0; border-right: 1px solid #ccc; padding: 10px 15px; font-weight: bold; font-size: 13px;">✏️ Manual</button>
            <button type="button" class="btn btn-info" onclick="switchProductTab('scrape')" id="tabScrape" style="border-radius: 4px 4px 0 0; margin-right: 0; border-right: 1px solid #ccc; padding: 10px 15px; font-weight: bold; font-size: 13px;">🔍 Tokopedia/Shopee</button>
            <button type="button" class="btn btn-success" onclick="switchProductTab('tiktok')" id="tabTiktok" style="border-radius: 4px 4px 0 0; padding: 10px 15px; font-weight: bold; font-size: 13px;">🎵 TikTok Shop</button>
        </div>
        <div id="productTabContent">
            <form id="addProductForm">
            <div class="form-group">
                <label>Nama Produk *</label>
                <input type="text" id="productName" required placeholder="Contoh: Sarung Tangan Premium">
            </div>
            <div class="form-group">
                <label>Kategori *</label>
                <select id="productCategory" required>
                    <option value="">Pilih Kategori</option>
                    ${categories.map(cat => `<option value="${cat}">${cat}</option>`).join('')}
                </select>
            </div>
            <div class="form-group">
                <label>Link Produk *</label>
                <input type="url" id="productLink" required placeholder="https://...">
            </div>
            <div class="form-group">
                <label>Harga Produk (Rp) *</label>
                <input type="number" id="productPrice" required min="0" step="100" placeholder="50000" oninput="calculateProductCommissions()">
            </div>
            <div class="form-group">
                <label>Komisi Reguler (%) *</label>
                <input type="number" id="productCommissionPercent" required min="0" max="100" step="0.1" placeholder="10" oninput="calculateProductCommissions()">
                <small>Persentase komisi dari harga jual</small>
            </div>
            <div class="form-group">
                <label>Komisi Reguler (Rp) *</label>
                <input type="number" id="productRegular" required min="0" step="100" placeholder="5000" readonly>
                <small>Otomatis dihitung dari Harga × Komisi %</small>
            </div>
            <div class="form-group">
                <label>Komisi GMV (%) *</label>
                <input type="number" id="productGMVPercent" required min="0" max="100" step="0.1" placeholder="30" oninput="calculateProductCommissions()">
                <small>Persentase komisi GMV maksimal dari harga jual</small>
            </div>
            <div class="form-group">
                <label>Komisi GMV Max (Rp) *</label>
                <input type="number" id="productGMV" required min="0" step="100" placeholder="15000" readonly>
                <small>Otomatis dihitung dari Harga × Komisi GMV %</small>
            </div>
            <div class="form-group">
                <label>Target GMV (Rp)</label>
                <input type="number" id="productTargetGMV" min="0" step="1000" placeholder="1000000" value="0">
                <small>Target GMV untuk mendapatkan komisi maksimal (opsional)</small>
            </div>
            <div class="form-group">
                <label>Status</label>
                <select id="productStatus" required>
                    <option value="active">Active</option>
                    <option value="inactive">Inactive</option>
                </select>
            </div>
            <button type="submit" class="btn btn-primary btn-block">Tambah Produk</button>
        </form>
        <div id="scrapeProductForm" style="display: none;">
            <div class="form-group">
                <label>URL Produk Tokopedia/Shopee *</label>
                <input type="url" id="productUrlInput" placeholder="https://www.tokopedia.com/... atau https://shopee.co.id/..." style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;">
                <small>Paste URL produk Tokopedia atau Shopee di sini</small>
            </div>
            <div style="text-align: center; margin: 15px 0; color: #666;">ATAU</div>
            <div class="form-group">
                <label>Paste HTML dari halaman produk (Opsional)</label>
                <textarea id="htmlInput" rows="8" placeholder="Paste HTML di sini jika URL tidak bekerja..." style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px; font-family: monospace; font-size: 12px;"></textarea>
                <small>Gunakan jika URL tidak bekerja</small>
            </div>
            <button type="button" class="btn btn-info btn-block" onclick="extractProductFromHTML()" style="margin-bottom: 10px;">🔍 Ekstrak Data</button>
            <div id="extractedData" style="display: none; padding: 15px; background: #f8f9fa; border-radius: 4px; margin-bottom: 15px;">
                <h4 style="margin-top: 0; color: #28a745;">✅ Data berhasil diekstrak!</h4>
                <div id="extractedDataContent"></div>
                <button type="button" class="btn btn-success btn-block" onclick="useExtractedData()" style="margin-top: 15px;">Lanjutkan ke Form Tambah Produk</button>
            </div>
        </div>
        <div id="tiktokScrapeForm" style="display: none;">
            <div class="form-group">
                <label>URL Produk TikTok Shop *</label>
                <input type="url" id="tiktokUrlInput" placeholder="https://www.tiktok.com/@shop/video/1234567890" style="width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 4px;">
                <small>Paste URL produk TikTok Shop di sini. Sistem akan menggunakan API untuk mendapatkan data lengkap.</small>
            </div>
            <button type="button" class="btn btn-success btn-block" onclick="scrapeTiktokProduct()" style="margin-bottom: 10px;">🎵 Scrape dengan TikTok API</button>
            <div id="tiktokExtractedData" style="display: none; padding: 15px; background: #f8f9fa; border-radius: 4px; margin-bottom: 15px;">
                <h4 style="margin-top: 0; color: #28a745;">✅ Data berhasil di-scrape dari TikTok Shop!</h4>
                <div id="tiktokExtractedDataContent"></div>
                <button type="button" class="btn btn-success btn-block" onclick="useTiktokExtractedData()" style="margin-top: 15px;">Lanjutkan ke Form Tambah Produk</button>
            </div>
        </div>
        </div>
    `;
    document.getElementById('modal').classList.remove('hidden');
    
    // Initialize tab state
    window.currentProductTab = 'manual';
    switchProductTab('manual');
    
    // Add calculation function
    window.calculateProductCommissions = function() {
        const price = parseFloat(document.getElementById('productPrice').value) || 0;
        const regularPercent = parseFloat(document.getElementById('productCommissionPercent').value) || 0;
        const gmvPercent = parseFloat(document.getElementById('productGMVPercent').value) || 0;
        
        const regularCommission = (price * regularPercent) / 100;
        const gmvCommission = (price * gmvPercent) / 100;
        
        document.getElementById('productRegular').value = Math.round(regularCommission);
        document.getElementById('productGMV').value = Math.round(gmvCommission);
    };
    
    document.getElementById('addProductForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const price = parseFloat(document.getElementById('productPrice').value) || 0;
        const regularPercent = parseFloat(document.getElementById('productCommissionPercent').value) || 0;
        const gmvPercent = parseFloat(document.getElementById('productGMVPercent').value) || 0;
        
        // Validate inputs
        if (!price || price <= 0) {
            alert('Harga produk harus diisi dan lebih dari 0!');
            return;
        }
        if (!regularPercent || regularPercent <= 0) {
            alert('Komisi Reguler (%) harus diisi dan lebih dari 0!');
            return;
        }
        if (!gmvPercent || gmvPercent <= 0) {
            alert('Komisi GMV (%) harus diisi dan lebih dari 0!');
            return;
        }
        
        // Calculate commissions from percentages
        const regularCommission = (price * regularPercent) / 100;
        const gmvCommission = (price * gmvPercent) / 100;
        
        const productName = document.getElementById('productName').value.trim();
        const category = document.getElementById('productCategory').value;
        const productLink = document.getElementById('productLink').value.trim();
        
        // Validate required fields
        if (!productName) {
            alert('Nama Produk harus diisi!');
            return;
        }
        if (!category) {
            alert('Kategori harus dipilih!');
            return;
        }
        if (!productLink) {
            alert('Link Produk harus diisi!');
            return;
        }
        
        const data = {
            product_name: productName,
            category: category,
            product_link: productLink,
            product_price: price,
            commission_percent: regularPercent,
            gmv_percent: gmvPercent,
            regular_commission: Math.round(regularCommission),
            gmv_max_commission: Math.round(gmvCommission),
            target_gmv: parseFloat(document.getElementById('productTargetGMV').value.replace(/,/g, '.')) || 0,
            status: document.getElementById('productStatus').value
        };
        
        console.log('Sending product data:', data);
        
        try {
            const res = await authenticatedFetch(`${API_URL}/products`, {
                method: 'POST',
                body: JSON.stringify(data)
            });
            
            if (!res.ok) {
                const error = await res.json();
                throw new Error(error.error || `HTTP ${res.status}: ${res.statusText}`);
            }
            
            const result = await res.json();
            console.log('Product created successfully:', result);
            
            // Close modal first
            closeModal();
            
            // Reload products and switch to products section to see the new product
            try {
                await loadProducts(1);
                // Switch to products section to see the new product
                showSection('products');
                alert('Produk berhasil ditambahkan!');
            } catch (error) {
                console.error('Error reloading products:', error);
                alert('Produk berhasil ditambahkan, tapi gagal memuat ulang daftar produk. Silakan refresh halaman.');
            }
        } catch (error) {
            console.error('Error adding product:', error);
            alert('Error: ' + error.message);
        }
    });
}

function switchProductTab(tab) {
    window.currentProductTab = tab;
    const manualForm = document.getElementById('addProductForm');
    const scrapeForm = document.getElementById('scrapeProductForm');
    const tiktokForm = document.getElementById('tiktokScrapeForm');
    const tabManual = document.getElementById('tabManual');
    const tabScrape = document.getElementById('tabScrape');
    const tabTiktok = document.getElementById('tabTiktok');
    
    // Reset all forms
    if (manualForm) manualForm.style.display = 'none';
    if (scrapeForm) scrapeForm.style.display = 'none';
    if (tiktokForm) tiktokForm.style.display = 'none';
    
    // Reset all tabs
    [tabManual, tabScrape, tabTiktok].forEach(t => {
        if (t) {
            t.classList.remove('btn-primary');
            t.style.backgroundColor = '';
            t.style.color = '';
            t.style.borderBottom = 'none';
        }
    });
    
    if (tab === 'manual') {
        if (manualForm) manualForm.style.display = 'block';
        if (tabManual) {
            tabManual.classList.add('btn-primary');
            tabManual.style.backgroundColor = '#007bff';
            tabManual.style.color = 'white';
            tabManual.style.borderBottom = '2px solid #007bff';
        }
        if (tabScrape) {
            tabScrape.classList.add('btn-info');
            tabScrape.style.backgroundColor = '#17a2b8';
            tabScrape.style.color = 'white';
        }
        if (tabTiktok) {
            tabTiktok.classList.add('btn-success');
            tabTiktok.style.backgroundColor = '#28a745';
            tabTiktok.style.color = 'white';
        }
    } else if (tab === 'scrape') {
        if (scrapeForm) scrapeForm.style.display = 'block';
        if (tabManual) {
            tabManual.classList.add('btn-secondary');
            tabManual.style.backgroundColor = '#6c757d';
            tabManual.style.color = 'white';
        }
        if (tabScrape) {
            tabScrape.classList.add('btn-primary');
            tabScrape.style.backgroundColor = '#007bff';
            tabScrape.style.color = 'white';
            tabScrape.style.borderBottom = '2px solid #007bff';
        }
        if (tabTiktok) {
            tabTiktok.classList.add('btn-success');
            tabTiktok.style.backgroundColor = '#28a745';
            tabTiktok.style.color = 'white';
        }
    } else if (tab === 'tiktok') {
        if (tiktokForm) tiktokForm.style.display = 'block';
        if (tabManual) {
            tabManual.classList.add('btn-secondary');
            tabManual.style.backgroundColor = '#6c757d';
            tabManual.style.color = 'white';
        }
        if (tabScrape) {
            tabScrape.classList.add('btn-info');
            tabScrape.style.backgroundColor = '#17a2b8';
            tabScrape.style.color = 'white';
        }
        if (tabTiktok) {
            tabTiktok.classList.add('btn-primary');
            tabTiktok.style.backgroundColor = '#007bff';
            tabTiktok.style.color = 'white';
            tabTiktok.style.borderBottom = '2px solid #007bff';
        }
    }
}

async function extractProductFromHTML() {
    const urlInput = document.getElementById('productUrlInput');
    const htmlInput = document.getElementById('htmlInput');
    const url = urlInput?.value.trim() || '';
    const html = htmlInput?.value.trim() || '';
    
    if (!url && !html) {
        alert('Silakan paste URL produk Tokopedia atau HTML terlebih dahulu!');
        return;
    }
    
    // Show loading
    const extractedDiv = document.getElementById('extractedData');
    const extractedContent = document.getElementById('extractedDataContent');
    if (extractedDiv && extractedContent) {
        extractedDiv.style.display = 'block';
        extractedContent.innerHTML = '<div style="text-align: center; padding: 20px;"><div class="spinner" style="border: 4px solid #f3f3f3; border-top: 4px solid #3498db; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 0 auto;"></div><p style="margin-top: 10px;">Mengekstrak data produk...</p></div>';
    }
    
    try {
        // Call backend API to extract product data
        const response = await authenticatedFetch(`${API_URL}/products/extract`, {
            method: 'POST',
            body: JSON.stringify({
                url: url,
                html: html
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Gagal mengekstrak data produk');
        }
        
        const result = await response.json();
        
        if (result.success && result.data) {
            const data = result.data;
            
            // Check if we have at least name or price
            if (!data.product_name && !data.price) {
                throw new Error(result.error || 'Tidak dapat mengekstrak data produk. Pastikan URL valid atau coba paste HTML lengkap.');
            }
            
            // Display extracted data
            if (extractedDiv && extractedContent) {
                const sourceText = result.source === 'embedded_json' ? 'Embedded JSON (Paling Akurat)' : 
                                  result.source === 'tokopedia_api' ? 'Tokopedia API (Akurat)' : 
                                  'HTML Parsing';
                
                extractedContent.innerHTML = `
                    <div style="margin-bottom: 10px;">
                        <strong>✓ Nama:</strong> ${data.product_name || '<span style="color: #dc3545;">Tidak ditemukan</span>'}
                    </div>
                    <div style="margin-bottom: 10px;">
                        <strong>✓ Kategori:</strong> ${data.category || 'General'}
                    </div>
                    <div style="margin-bottom: 10px;">
                        <strong>✓ Harga:</strong> ${data.price && data.price > 0 ? formatCurrency(data.price) : '<span style="color: #dc3545;">Tidak ditemukan</span>'}
                    </div>
                    ${data.description ? `<div style="margin-bottom: 10px;">
                        <strong>Deskripsi:</strong> ${data.description.substring(0, 100)}${data.description.length > 100 ? '...' : ''}
                    </div>` : ''}
                    ${data.shop_name ? `<div style="margin-bottom: 10px;">
                        <strong>Shop:</strong> ${data.shop_name}
                    </div>` : ''}
                    <div style="margin-top: 10px; padding: 10px; background: #e7f3ff; border-radius: 4px; font-size: 12px; color: #0066cc;">
                        <strong>Source:</strong> ${sourceText}
                    </div>
                `;
                extractedDiv.style.display = 'block';
                
                // Store extracted data for later use
                window.extractedProductData = {
                    productName: data.product_name || '',
                    category: data.category || 'General',
                    price: data.price || 0,
                    description: data.description || '',
                    productLink: data.product_link || url
                };
            }
        } else {
            throw new Error(result.error || 'Data tidak ditemukan dalam response');
        }
    } catch (error) {
        console.error('Error extracting data:', error);
        if (extractedDiv && extractedContent) {
            extractedContent.innerHTML = `<div style="color: #dc3545; padding: 10px;">❌ Error: ${error.message}</div>`;
        } else {
            alert('Error extracting data: ' + error.message);
        }
    }
}

async function scrapeTiktokProduct() {
    const tiktokUrl = document.getElementById('tiktokUrlInput')?.value.trim() || '';
    
    if (!tiktokUrl) {
        alert('Silakan paste link TikTok Shop terlebih dahulu!');
        return;
    }
    
    // Show loading
    const extractedDiv = document.getElementById('tiktokExtractedData');
    const extractedContent = document.getElementById('tiktokExtractedDataContent');
    if (extractedDiv && extractedContent) {
        extractedDiv.style.display = 'block';
        extractedContent.innerHTML = '<div style="text-align: center; padding: 20px;"><div class="spinner" style="border: 4px solid #f3f3f3; border-top: 4px solid #28a745; border-radius: 50%; width: 40px; height: 40px; animation: spin 1s linear infinite; margin: 0 auto;"></div><p style="margin-top: 10px;">Mengekstrak data dari TikTok Shop...</p></div>';
    }
    
    try {
        const response = await authenticatedFetch(`${API_URL}/products/scrape-tiktok`, {
            method: 'POST',
            body: JSON.stringify({
                tiktok_url: tiktokUrl
            })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Gagal scrape produk dari TikTok Shop');
        }
        
        const result = await response.json();
        
        if (result.success && result.data) {
            const data = result.data;
            
            // Check if we have at least name or price
            if (!data.product_name && !data.price) {
                throw new Error(result.error || 'Tidak dapat mengekstrak data produk dari TikTok Shop.');
            }
            
            // Display extracted data
            if (extractedDiv && extractedContent) {
                const images = data.product_images ? JSON.parse(data.product_images) : [];
                const imagePreview = images.length > 0 ? `<img src="${images[0]}" style="max-width: 100px; max-height: 100px; border-radius: 4px; margin: 10px 0;" alt="Product Image">` : '';
                
                extractedContent.innerHTML = `
                    ${imagePreview}
                    <div style="margin-bottom: 10px;">
                        <strong>✓ Nama:</strong> ${data.product_name || '<span style="color: #dc3545;">Tidak ditemukan</span>'}
                    </div>
                    <div style="margin-bottom: 10px;">
                        <strong>✓ Kategori:</strong> ${data.category || 'General'}
                    </div>
                    <div style="margin-bottom: 10px;">
                        <strong>✓ Harga:</strong> ${data.price && data.price > 0 ? formatCurrency(data.price) : '<span style="color: #dc3545;">Tidak ditemukan</span>'}
                        ${data.original_price && data.original_price > data.price ? `<br><small style="color: #666;">Harga asli: ${formatCurrency(data.original_price)} (Diskon ${data.discount_percent || 0}%)</small>` : ''}
                    </div>
                    ${data.stock_quantity !== undefined ? `<div style="margin-bottom: 10px;">
                        <strong>✓ Stock:</strong> ${data.stock_quantity} unit
                    </div>` : ''}
                    ${data.rating && data.rating > 0 ? `<div style="margin-bottom: 10px;">
                        <strong>✓ Rating:</strong> ⭐ ${data.rating.toFixed(1)} (${data.review_count || 0} review)
                    </div>` : ''}
                    ${data.tiktok_seller_name ? `<div style="margin-bottom: 10px;">
                        <strong>✓ Seller:</strong> ${data.tiktok_seller_name}
                    </div>` : ''}
                    ${data.description ? `<div style="margin-bottom: 10px;">
                        <strong>Deskripsi:</strong> ${data.description.substring(0, 100)}${data.description.length > 100 ? '...' : ''}
                    </div>` : ''}
                    <div style="margin-top: 10px; padding: 10px; background: #e7f3ff; border-radius: 4px; font-size: 12px; color: #0066cc;">
                        <strong>Source:</strong> TikTok Shop API (Akurat & Lengkap)
                    </div>
                `;
                extractedDiv.style.display = 'block';
                
                // Store extracted data for later use
                window.tiktokExtractedProductData = {
                    productName: data.product_name || '',
                    category: data.category || 'General',
                    price: data.price || 0,
                    originalPrice: data.original_price || data.price || 0,
                    description: data.description || '',
                    productLink: data.product_link || tiktokUrl,
                    productImages: images,
                    stockQuantity: data.stock_quantity || 0,
                    rating: data.rating || 0,
                    reviewCount: data.review_count || 0,
                    sellerName: data.tiktok_seller_name || '',
                    tiktokProductId: data.tiktok_product_id || ''
                };
            }
        } else {
            throw new Error(result.error || 'Data tidak ditemukan dalam response');
        }
    } catch (error) {
        console.error('Error scraping TikTok product:', error);
        if (extractedDiv && extractedContent) {
            extractedContent.innerHTML = `<div style="color: #dc3545; padding: 10px;">❌ Error: ${error.message}</div>`;
        } else {
            alert('Error scraping TikTok product: ' + error.message);
        }
    }
}

function useTiktokExtractedData() {
    if (!window.tiktokExtractedProductData) {
        alert('Tidak ada data yang diekstrak!');
        return;
    }
    
    const data = window.tiktokExtractedProductData;
    
    // Fill form fields
    if (document.getElementById('productName')) {
        document.getElementById('productName').value = data.productName;
    }
    if (document.getElementById('productCategory')) {
        document.getElementById('productCategory').value = data.category;
    }
    if (document.getElementById('productLink') && data.productLink) {
        document.getElementById('productLink').value = data.productLink;
    }
    if (document.getElementById('productPrice') && data.price > 0) {
        document.getElementById('productPrice').value = data.price;
        // Trigger commission calculation
        if (window.calculateProductCommissions) {
            window.calculateProductCommissions();
        }
    }
    
    // Switch to manual tab
    switchProductTab('manual');
    
    // Clear extracted data display
    const extractedDiv = document.getElementById('tiktokExtractedData');
    if (extractedDiv) {
        extractedDiv.style.display = 'none';
    }
    
    // Clear TikTok URL input
    const tiktokUrlInput = document.getElementById('tiktokUrlInput');
    if (tiktokUrlInput) {
        tiktokUrlInput.value = '';
    }
    
    // Focus on first empty field
    if (!document.getElementById('productLink').value) {
        document.getElementById('productLink').focus();
    }
}

function useExtractedData() {
    if (!window.extractedProductData) {
        alert('Tidak ada data yang diekstrak!');
        return;
    }
    
    const data = window.extractedProductData;
    
    // Fill form fields
    if (document.getElementById('productName')) {
        document.getElementById('productName').value = data.productName;
    }
    if (document.getElementById('productCategory')) {
        document.getElementById('productCategory').value = data.category;
    }
    if (document.getElementById('productLink') && data.productLink) {
        document.getElementById('productLink').value = data.productLink;
    }
    if (document.getElementById('productPrice') && data.price > 0) {
        document.getElementById('productPrice').value = data.price;
        // Trigger commission calculation
        if (window.calculateProductCommissions) {
            window.calculateProductCommissions();
        }
    }
    
    // Switch to manual tab
    switchProductTab('manual');
    
    // Clear extracted data display
    const extractedDiv = document.getElementById('extractedData');
    if (extractedDiv) {
        extractedDiv.style.display = 'none';
    }
    
    // Clear HTML input
    const htmlInput = document.getElementById('htmlInput');
    if (htmlInput) {
        htmlInput.value = '';
    }
    
    // Focus on first empty field
    if (!document.getElementById('productLink').value) {
        document.getElementById('productLink').focus();
    }
}

async function editProduct(productId) {
    // Load product data
    const res = await fetch(`${API_URL}/products`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    const products = await res.json();
    const product = products.find(p => p.id === productId);
    
    if (!product) {
        alert('Product not found');
        return;
    }
    
    // Load categories
    let categories = [];
    try {
        const catRes = await authenticatedFetch(`${API_URL}/products/categories`);
        categories = await catRes.json();
    } catch (error) {
        categories = ['Fashion & Apparel', 'Beauty & Personal Care', 'Electronics', 'Other'];
    }
    
    const modalBody = document.getElementById('modalBody');
    modalBody.innerHTML = `
        <h2>Edit Produk</h2>
        <form id="editProductForm">
            <div class="form-group">
                <label>Nama Produk *</label>
                <input type="text" id="editProductName" value="${product.product_name || product.title || ''}" required>
            </div>
            <div class="form-group">
                <label>Kategori TikTok *</label>
                <select id="editProductCategory" required>
                    ${categories.map(cat => `<option value="${cat}" ${cat === product.category ? 'selected' : ''}>${cat}</option>`).join('')}
                </select>
            </div>
            <div class="form-group">
                <label>Link Produk *</label>
                <input type="url" id="editProductLink" value="${product.product_link || ''}" required>
            </div>
            <div class="form-group">
                <label>Harga Produk (Rp) *</label>
                <input type="number" id="editProductPrice" value="${product.product_price || 0}" required min="0" step="100" oninput="calculateEditCommission()">
            </div>
            <div class="form-group">
                <label>Komisi (%) *</label>
                <input type="number" id="editProductCommissionPercent" value="${product.commission_percent || 0}" required min="0" max="100" step="0.1" oninput="calculateEditCommission()">
            </div>
            <div class="form-group">
                <label>Komisi Reguler (Rp) *</label>
                <input type="number" id="editProductRegular" value="${product.regular_commission || 0}" required min="0" step="100">
            </div>
            <div class="form-group">
                <label>Komisi GMV Max (Rp) *</label>
                <input type="number" id="editProductGMV" value="${product.gmv_max_commission || 0}" required min="0" step="100">
            </div>
            <div class="form-group">
                <label>Status</label>
                <select id="editProductStatus">
                    <option value="active" ${product.status === 'active' ? 'selected' : ''}>Active</option>
                    <option value="inactive" ${product.status === 'inactive' ? 'selected' : ''}>Inactive</option>
                </select>
            </div>
            <button type="submit" class="btn btn-primary btn-block">Update Produk</button>
        </form>
    `;
    document.getElementById('modal').classList.remove('hidden');
    
    window.calculateEditCommission = function() {
        const price = parseFloat(document.getElementById('editProductPrice').value) || 0;
        const percent = parseFloat(document.getElementById('editProductCommissionPercent').value) || 0;
        const commission = (price * percent) / 100;
        document.getElementById('editProductRegular').value = Math.round(commission);
    };
    
    document.getElementById('editProductForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            product_name: document.getElementById('editProductName').value,
            category: document.getElementById('editProductCategory').value,
            product_link: document.getElementById('editProductLink').value,
            product_price: parseFloat(document.getElementById('editProductPrice').value),
            commission_percent: parseFloat(document.getElementById('editProductCommissionPercent').value),
            regular_commission: parseFloat(document.getElementById('editProductRegular').value),
            gmv_max_commission: parseFloat(document.getElementById('editProductGMV').value),
            status: document.getElementById('editProductStatus').value
        };
        
        try {
            const res = await authenticatedFetch(`${API_URL}/products/${productId}`, {
                method: 'PUT',
                body: JSON.stringify(data)
            });
            
            if (res.ok) {
                closeModal();
                loadProducts();
            } else {
                const result = await res.json();
                alert(result.error || 'Error updating product');
            }
        } catch (error) {
            alert('Connection error');
        }
    });
}

async function deleteProduct(productId) {
    if (!confirm('Yakin ingin menghapus produk ini?')) {
        return;
    }
    
    try {
        const res = await authenticatedFetch(`${API_URL}/products/${productId}`, {
            method: 'DELETE'
        });
        
        if (res.ok) {
            loadProducts();
            loadDashboard();
        } else {
            const result = await res.json();
            alert(result.error || 'Error deleting product');
        }
    } catch (error) {
        alert('Connection error');
    }
}

// ==================== TEAMS ====================
async function loadTeams() {
    try {
        const res = await authenticatedFetch(`${API_URL}/teams`);
        const teams = await res.json();
        
        const tbody = document.getElementById('teamsTable');
        tbody.innerHTML = teams.map(t => `
            <tr>
                <td>${t.name}</td>
                <td>${t.manager_name || 'No Manager'}</td>
                <td>${formatCurrency(t.target_commission)}</td>
                <td>${t.manager_bonus_percent}%</td>
                ${currentUser.role === 'owner' ? `<td><button class="btn btn-primary" onclick="addMemberToTeam(${t.id})">Add Member</button></td>` : '<td></td>'}
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading teams:', error);
    }
}

async function showAddTeamModal() {
    // Get users for manager selection
    const usersRes = await authenticatedFetch(`${API_URL}/users`);
    const users = await usersRes.json();
    const managers = users.filter(u => u.role === 'manager');
    
    const modalBody = document.getElementById('modalBody');
    modalBody.innerHTML = `
        <h2>Add Team</h2>
        <form id="addTeamForm">
            <div class="form-group">
                <label>Team Name</label>
                <input type="text" id="teamName" required>
            </div>
            <div class="form-group">
                <label>Manager</label>
                <select id="teamManager">
                    <option value="">No Manager</option>
                    ${managers.map(m => `<option value="${m.id}">${m.full_name || m.username}</option>`).join('')}
                </select>
            </div>
            <div class="form-group">
                <label>Target Commission</label>
                <input type="number" id="teamTarget" value="0">
            </div>
            <div class="form-group">
                <label>Manager Bonus %</label>
                <input type="number" id="teamBonus" min="5" max="10" value="5">
            </div>
            <button type="submit" class="btn btn-primary btn-block">Add Team</button>
        </form>
    `;
    document.getElementById('modal').classList.remove('hidden');
    
    document.getElementById('addTeamForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            name: document.getElementById('teamName').value,
            manager_id: document.getElementById('teamManager').value || null,
            target_commission: parseFloat(document.getElementById('teamTarget').value),
            manager_bonus_percent: parseFloat(document.getElementById('teamBonus').value)
        };
        
        try {
            const res = await authenticatedFetch(`${API_URL}/teams`, {
                method: 'POST',
                body: JSON.stringify(data)
            });
            
            if (res.ok) {
                closeModal();
                loadTeams();
            } else {
                alert('Error adding team');
            }
        } catch (error) {
            alert('Connection error');
        }
    });
}

async function addMemberToTeam(teamId) {
    const usersRes = await authenticatedFetch(`${API_URL}/users`);
    const users = await usersRes.json();
    const members = users.filter(u => u.role === 'member');
    
    const modalBody = document.getElementById('modalBody');
    modalBody.innerHTML = `
        <h2>Add Member to Team</h2>
        <form id="addMemberForm">
            <div class="form-group">
                <label>Member</label>
                <select id="memberSelect" required>
                    ${members.map(m => `<option value="${m.id}">${m.full_name || m.username}</option>`).join('')}
                </select>
            </div>
            <button type="submit" class="btn btn-primary btn-block">Add Member</button>
        </form>
    `;
    document.getElementById('modal').classList.remove('hidden');
    
    document.getElementById('addMemberForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            user_id: parseInt(document.getElementById('memberSelect').value)
        };
        
        try {
            const res = await authenticatedFetch(`${API_URL}/teams/${teamId}/members`, {
                method: 'POST',
                body: JSON.stringify(data)
            });
            
            if (res.ok) {
                closeModal();
                loadTeams();
            } else {
                alert('Error adding member');
            }
        } catch (error) {
            alert('Connection error');
        }
    });
}

// ==================== CONTENT ====================
async function loadContent() {
    try {
        const res = await authenticatedFetch(`${API_URL}/content`);
        const content = await res.json();
        
        const tbody = document.getElementById('contentTable');
        tbody.innerHTML = content.map(c => `
            <tr>
                <td>${c.title}</td>
                <td>${c.product_title || 'N/A'}</td>
                <td>${c.creator_name || 'N/A'}</td>
                <td>${c.platform}</td>
                <td>${c.quality_score}</td>
                <td><span class="badge badge-${c.status === 'approved' ? 'success' : c.status === 'rejected' ? 'danger' : 'warning'}">${c.status}</span></td>
                ${currentUser.role === 'owner' && c.status === 'pending' ? `<td><button class="btn btn-success" onclick="approveContent(${c.id})">Approve</button></td>` : '<td></td>'}
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading content:', error);
    }
}

async function showAddContentModal() {
    const productsRes = await authenticatedFetch(`${API_URL}/products`);
    const products = await productsRes.json();
    
    const modalBody = document.getElementById('modalBody');
    modalBody.innerHTML = `
        <h2>Create Content</h2>
        <form id="addContentForm">
            <div class="form-group">
                <label>Product</label>
                <select id="contentProduct" required>
                    ${products.map(p => `<option value="${p.id}">${p.title}</option>`).join('')}
                </select>
            </div>
            <div class="form-group">
                <label>Title</label>
                <input type="text" id="contentTitle" required>
            </div>
            <div class="form-group">
                <label>Description</label>
                <textarea id="contentDescription"></textarea>
            </div>
            <div class="form-group">
                <label>Media URL</label>
                <input type="url" id="contentMedia">
            </div>
            <div class="form-group">
                <label>Platform</label>
                <select id="contentPlatform">
                    <option value="tiktok">TikTok</option>
                    <option value="shopee">Shopee</option>
                </select>
            </div>
            <button type="button" class="btn btn-info" onclick="generateContentAI()" style="margin-bottom: 10px;">Generate with AI</button>
            <button type="submit" class="btn btn-primary btn-block">Create Content</button>
        </form>
    `;
    document.getElementById('modal').classList.remove('hidden');
    
    document.getElementById('addContentForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            product_id: parseInt(document.getElementById('contentProduct').value),
            title: document.getElementById('contentTitle').value,
            description: document.getElementById('contentDescription').value,
            media_url: document.getElementById('contentMedia').value,
            platform: document.getElementById('contentPlatform').value
        };
        
        try {
            const res = await authenticatedFetch(`${API_URL}/content`, {
                method: 'POST',
                body: JSON.stringify(data)
            });
            
            if (res.ok) {
                closeModal();
                loadContent();
            } else {
                alert('Error creating content');
            }
        } catch (error) {
            alert('Connection error');
        }
    });
}

async function generateContentAI() {
    const productId = document.getElementById('contentProduct').value;
    const platform = document.getElementById('contentPlatform').value;
    
    try {
        const res = await authenticatedFetch(`${API_URL}/ai/generate-content`, {
            method: 'POST',
            body: JSON.stringify({ product_id: parseInt(productId), platform })
        });
        
        const data = await res.json();
        document.getElementById('contentTitle').value = data.title;
        document.getElementById('contentDescription').value = data.description + '\n\n' + data.hashtags;
    } catch (error) {
        alert('Error generating content');
    }
}

async function approveContent(contentId) {
    const qualityScore = prompt('Quality Score (0-10):');
    if (qualityScore && !isNaN(qualityScore)) {
        try {
            const res = await authenticatedFetch(`${API_URL}/content/${contentId}/approve`, {
                method: 'POST',
                body: JSON.stringify({ quality_score: parseFloat(qualityScore) })
            });
            
            if (res.ok) {
                loadContent();
            } else {
                alert('Error approving content');
            }
        } catch (error) {
            alert('Connection error');
        }
    }
}

// ==================== COMMISSIONS ====================
async function loadCommissions() {
    try {
        const res = await authenticatedFetch(`${API_URL}/commissions`);
        const commissions = await res.json();
        
        const tbody = document.getElementById('commissionsTable');
        if (commissions.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" style="text-align: center;">Belum ada commission</td></tr>';
        } else {
            tbody.innerHTML = commissions.map(c => `
                <tr>
                    <td>Content #${c.content_id}</td>
                    <td>${c.creator_name || 'N/A'}</td>
                    <td>${formatCurrency(c.total_commission)}</td>
                    <td>${formatCurrency(c.owner_share)}</td>
                    <td>${formatCurrency(c.team_share)}</td>
                    <td>${formatCurrency(c.manager_bonus)}</td>
                    <td><span class="badge badge-${c.status === 'paid' ? 'success' : 'warning'}">${c.status}</span></td>
                </tr>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading commissions:', error);
        alert('Error loading commissions: ' + error.message);
    }
}

async function autoCalculateCommissions() {
    if (!confirm('Auto-calculate commissions dari semua approved reports?\n\nIni akan membuat commission record untuk setiap approved report yang belum punya commission.')) {
        return;
    }
    
    try {
        const res = await authenticatedFetch(`${API_URL}/commissions/auto-calculate`, {
            method: 'POST'
        });
        
        if (res.ok) {
            const data = await res.json();
            alert(`Berhasil membuat ${data.count} commission dari approved reports!`);
            loadCommissions();
            loadDashboard();
        } else {
            const error = await res.json();
            alert('Error: ' + (error.error || 'Auto-calculate gagal'));
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function showAddCommissionModal() {
    const contentRes = await authenticatedFetch(`${API_URL}/content`);
    const contents = await contentRes.json();
    const approved = contents.filter(c => c.status === 'approved');
    
    const modalBody = document.getElementById('modalBody');
    modalBody.innerHTML = `
        <h2>Add Commission</h2>
        <form id="addCommissionForm">
            <div class="form-group">
                <label>Content</label>
                <select id="commissionContent" required>
                    ${approved.map(c => `<option value="${c.id}">${c.title}</option>`).join('')}
                </select>
            </div>
            <div class="form-group">
                <label>Total Commission</label>
                <input type="number" id="commissionTotal" required>
            </div>
            <button type="submit" class="btn btn-primary btn-block">Add Commission</button>
        </form>
    `;
    document.getElementById('modal').classList.remove('hidden');
    
    document.getElementById('addCommissionForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const data = {
            content_id: parseInt(document.getElementById('commissionContent').value),
            total_commission: parseFloat(document.getElementById('commissionTotal').value)
        };
        
        try {
            const res = await authenticatedFetch(`${API_URL}/commissions`, {
                method: 'POST',
                body: JSON.stringify(data)
            });
            
            if (res.ok) {
                closeModal();
                loadCommissions();
                loadDashboard();
            } else {
                alert('Error adding commission');
            }
        } catch (error) {
            alert('Connection error');
        }
    });
}

// ==================== PAYMENTS ====================
async function loadPayments() {
    try {
        const res = await authenticatedFetch(`${API_URL}/payments`);
        const payments = await res.json();
        
        const tbody = document.getElementById('paymentsTable');
        if (payments.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align: center;">Belum ada payment</td></tr>';
        } else {
            tbody.innerHTML = payments.map(p => `
                <tr>
                    <td>${p.user_name || 'N/A'}</td>
                    <td>${formatCurrency(p.amount)}</td>
                    <td>${p.payment_type}</td>
                    <td>${p.period || 'N/A'}</td>
                    <td><span class="badge badge-${p.status === 'paid' ? 'success' : 'warning'}">${p.status}</span></td>
                    <td>
                        ${currentUser.role === 'owner' && p.status === 'pending' ? `
                            <button class="btn btn-success btn-sm" onclick="markPaymentPaid(${p.id})">✓ Mark as Paid</button>
                        ` : p.status === 'paid' ? '<span style="color: #28a745;">✓ Paid</span>' : '-'}
                    </td>
                </tr>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading payments:', error);
        alert('Error loading payments: ' + error.message);
    }
}

async function markPaymentPaid(paymentId) {
    if (!confirm('Mark payment ini sebagai Paid?')) return;
    
    try {
        const res = await authenticatedFetch(`${API_URL}/payments/${paymentId}/mark-paid`, {
            method: 'POST'
        });
        
        if (res.ok) {
            alert('Payment berhasil ditandai sebagai Paid!');
            loadPayments();
            loadDashboard();
        } else {
            const error = await res.json();
            alert('Error: ' + (error.error || 'Mark as paid gagal'));
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

function showCalculatePaymentModal() {
    const now = new Date();
    const currentMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
    
    const modalBody = document.getElementById('modalBody');
    modalBody.innerHTML = `
        <h2>Calculate Payments</h2>
        <form id="calculatePaymentForm">
            <div class="form-group">
                <label>Period (Format: YYYY-MM)</label>
                <input type="text" id="paymentPeriod" value="${currentMonth}" required pattern="\\d{4}-\\d{2}">
                <small>Contoh: 2024-01</small>
            </div>
            <button type="submit" class="btn btn-primary btn-block">Calculate Payments</button>
        </form>
    `;
    document.getElementById('modal').classList.remove('hidden');
    
    document.getElementById('calculatePaymentForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const period = document.getElementById('paymentPeriod').value;
        
        try {
            const res = await authenticatedFetch(`${API_URL}/payments/calculate`, {
                method: 'POST',
                body: JSON.stringify({ period })
            });
            
            const data = await res.json();
            if (res.ok) {
                alert(`Pembayaran untuk periode ${period} berhasil dihitung! (${data.count} payments)`);
                closeModal();
                loadPayments();
                loadDashboard();
            } else {
                alert(data.error || 'Error calculating payments');
            }
        } catch (error) {
            alert('Connection error');
        }
    });
}

// ==================== MY REPORTS (User-specific) ====================
let currentMyReportPage = 1;
let totalMyReportPages = 1;

async function loadMyReports(page = 1) {
    try {
        currentMyReportPage = page;
        const statusFilter = document.getElementById('myReportStatusFilter')?.value || '';
        const search = document.getElementById('myReportSearch')?.value.trim() || '';
        
        // Build URL with filters
        const params = [];
        params.push(`page=${page}`);
        params.push(`per_page=20`);
        if (statusFilter) params.push(`status=${statusFilter}`);
        if (search) params.push(`search=${encodeURIComponent(search)}`);
        
        const url = `${API_URL}/my/reports?${params.join('&')}`;
        const res = await authenticatedFetch(url);
        
        if (!res.ok) {
            const error = await res.json();
            throw new Error(error.error || 'Gagal memuat laporan');
        }
        
        const data = await res.json();
        const reports = Array.isArray(data.reports) ? data.reports : [];
        
        // Update pagination
        if (data.pagination) {
            currentMyReportPage = data.pagination.page;
            totalMyReportPages = data.pagination.pages;
        }
        
        const tbody = document.getElementById('myReportsTable');
        if (!tbody) {
            console.error('myReportsTable element not found');
            return;
        }
        
        if (reports.length === 0) {
            tbody.innerHTML = '<tr><td colspan="8" style="text-align: center; padding: 20px;">Belum ada laporan. Klik "Submit New Report" untuk membuat laporan baru.</td></tr>';
        } else {
            const startIndex = (currentMyReportPage - 1) * 20;
            tbody.innerHTML = reports.map((r, index) => {
                const statusBadge = r.status === 'approved' ? 'badge-success' : 
                                   r.status === 'rejected' ? 'badge-danger' : 'badge-warning';
                const statusText = r.status === 'approved' ? '✅ Approved' : 
                                  r.status === 'rejected' ? '❌ Rejected' : '⏳ Pending';
                const canEdit = r.status === 'pending';
                
                return `
                <tr>
                    <td>${startIndex + index + 1}</td>
                    <td><a href="${r.link_video || '#'}" target="_blank" style="color: #007bff; word-break: break-all;">${(r.link_video || '').substring(0, 40)}${(r.link_video || '').length > 40 ? '...' : ''}</a></td>
                    <td>${r.tanggal_upload ? new Date(r.tanggal_upload).toLocaleDateString('id-ID') : '-'}</td>
                    <td>${r.tiktok_akun || '-'}</td>
                    <td><span class="badge badge-info">${r.platform || 'tiktok'}</span></td>
                    <td><span class="badge ${statusBadge}">${statusText}</span></td>
                    <td>${r.created_at ? new Date(r.created_at).toLocaleDateString('id-ID') : '-'}</td>
                    <td>
                        ${canEdit ? `
                            <button class="btn btn-primary btn-sm" onclick="editMyReport(${r.id})" style="margin-right: 5px;">✏️ Edit</button>
                            <button class="btn btn-danger btn-sm" onclick="deleteMyReport(${r.id})">🗑️ Delete</button>
                        ` : `
                            <button class="btn btn-info btn-sm" onclick="viewMyReport(${r.id})">👁️ View</button>
                        `}
                    </td>
                </tr>
            `;
            }).join('');
        }
        
        // Update pagination
        updateMyReportsPagination();
        
    } catch (error) {
        console.error('Error loading my reports:', error);
        const tbody = document.getElementById('myReportsTable');
        if (tbody) {
            tbody.innerHTML = `<tr><td colspan="8" style="text-align: center; padding: 20px; color: #dc3545;">Error loading reports: ${error.message}</td></tr>`;
        }
    }
}

function updateMyReportsPagination() {
    const paginationDiv = document.getElementById('myReportsPagination');
    if (!paginationDiv || totalMyReportPages <= 1) {
        if (paginationDiv) paginationDiv.innerHTML = '';
        return;
    }
    
    let paginationHTML = '';
    
    // Previous button
    if (currentMyReportPage > 1) {
        paginationHTML += `<button class="btn btn-secondary" onclick="loadMyReports(${currentMyReportPage - 1})" style="margin: 0 5px;">Previous</button>`;
    }
    
    // Page numbers
    const maxVisible = 5;
    let startPage = Math.max(1, currentMyReportPage - Math.floor(maxVisible / 2));
    let endPage = Math.min(totalMyReportPages, startPage + maxVisible - 1);
    
    if (endPage - startPage < maxVisible - 1) {
        startPage = Math.max(1, endPage - maxVisible + 1);
    }
    
    if (startPage > 1) {
        paginationHTML += `<button class="btn btn-secondary" onclick="loadMyReports(1)" style="margin: 0 2px;">1</button>`;
        if (startPage > 2) {
            paginationHTML += `<span style="margin: 0 5px;">...</span>`;
        }
    }
    
    for (let i = startPage; i <= endPage; i++) {
        if (i === currentMyReportPage) {
            paginationHTML += `<button class="btn btn-primary" style="margin: 0 2px;" disabled>${i}</button>`;
        } else {
            paginationHTML += `<button class="btn btn-secondary" onclick="loadMyReports(${i})" style="margin: 0 2px;">${i}</button>`;
        }
    }
    
    if (endPage < totalMyReportPages) {
        if (endPage < totalMyReportPages - 1) {
            paginationHTML += `<span style="margin: 0 5px;">...</span>`;
        }
        paginationHTML += `<button class="btn btn-secondary" onclick="loadMyReports(${totalMyReportPages})" style="margin: 0 2px;">${totalMyReportPages}</button>`;
    }
    
    // Next button
    if (currentMyReportPage < totalMyReportPages) {
        paginationHTML += `<button class="btn btn-secondary" onclick="loadMyReports(${currentMyReportPage + 1})" style="margin: 0 5px;">Next</button>`;
    }
    
    paginationDiv.innerHTML = paginationHTML;
}

async function showSubmitReportModal() {
    try {
        // Load products for dropdown
        const productsRes = await authenticatedFetch(`${API_URL}/products?per_page=1000`);
        const productsData = await productsRes.json();
        const products = Array.isArray(productsData.products) ? productsData.products : [];
        
        const modalBody = document.getElementById('modalBody');
        const today = new Date().toISOString().split('T')[0];
        
        modalBody.innerHTML = `
            <h2>➕ Submit New Report</h2>
            <form id="submitReportForm">
                <div class="form-group">
                    <label>Link Video TikTok/Shopee *</label>
                    <input type="url" id="reportLinkVideo" required placeholder="https://www.tiktok.com/@user/video/123 atau https://shopee.co.id/...">
                    <small>Paste link video TikTok atau Shopee di sini</small>
                </div>
                <div class="form-group">
                    <label>Tanggal Upload *</label>
                    <input type="date" id="reportTanggalUpload" required value="${today}">
                </div>
                <div class="form-group">
                    <label>Akun TikTok/Shopee *</label>
                    <input type="text" id="reportTiktokAkun" required placeholder="@username">
                </div>
                <div class="form-group">
                    <label>Platform *</label>
                    <select id="reportPlatform" required>
                        <option value="tiktok">TikTok</option>
                        <option value="shopee">Shopee</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Produk (Optional)</label>
                    <select id="reportProductId">
                        <option value="">Pilih Produk (Opsional)</option>
                        ${products.map(p => `<option value="${p.id}">${p.product_name}</option>`).join('')}
                    </select>
                    <small>Pilih produk yang dipromosikan (opsional)</small>
                </div>
                <div class="form-group">
                    <label>Deskripsi (Optional)</label>
                    <textarea id="reportDescription" rows="3" placeholder="Tambahkan deskripsi atau catatan..."></textarea>
                </div>
                <button type="submit" class="btn btn-primary btn-block">Submit Report</button>
                <button type="button" class="btn btn-secondary btn-block" onclick="closeModal()" style="margin-top: 10px;">Cancel</button>
            </form>
        `;
        
        document.getElementById('modal').classList.remove('hidden');
        
        document.getElementById('submitReportForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            await submitReport();
        });
    } catch (error) {
        alert('Error loading form: ' + error.message);
    }
}

async function submitReport() {
    try {
        const linkVideo = document.getElementById('reportLinkVideo').value.trim();
        const tanggalUpload = document.getElementById('reportTanggalUpload').value;
        const tiktokAkun = document.getElementById('reportTiktokAkun').value.trim();
        const platform = document.getElementById('reportPlatform').value;
        const productId = document.getElementById('reportProductId').value;
        const description = document.getElementById('reportDescription').value.trim();
        
        const data = {
            link_video: linkVideo,
            tanggal_upload: tanggalUpload,
            tiktok_akun: tiktokAkun,
            platform: platform
        };
        
        if (productId) {
            data.product_id = parseInt(productId);
        }
        
        if (description) {
            data.description = description;
        }
        
        const res = await authenticatedFetch(`${API_URL}/my/reports`, {
            method: 'POST',
            body: JSON.stringify(data)
        });
        
        if (!res.ok) {
            const error = await res.json();
            throw new Error(error.error || 'Gagal submit laporan');
        }
        
        const result = await res.json();
        alert('✅ Laporan berhasil dibuat! Status: Pending');
        closeModal();
        loadMyReports(1);
        
    } catch (error) {
        alert('Error submitting report: ' + error.message);
    }
}

async function editMyReport(reportId) {
    try {
        const res = await authenticatedFetch(`${API_URL}/my/reports/${reportId}`);
        if (!res.ok) {
            const error = await res.json();
            throw new Error(error.error || 'Gagal memuat laporan');
        }
        
        const report = await res.json();
        
        // Load products
        const productsRes = await authenticatedFetch(`${API_URL}/products?per_page=1000`);
        const productsData = await productsRes.json();
        const products = Array.isArray(productsData.products) ? productsData.products : [];
        
        const modalBody = document.getElementById('modalBody');
        modalBody.innerHTML = `
            <h2>✏️ Edit Report</h2>
            <form id="editReportForm">
                <div class="form-group">
                    <label>Link Video TikTok/Shopee *</label>
                    <input type="url" id="editReportLinkVideo" required value="${report.link_video || ''}">
                </div>
                <div class="form-group">
                    <label>Tanggal Upload *</label>
                    <input type="date" id="editReportTanggalUpload" required value="${report.tanggal_upload || ''}">
                </div>
                <div class="form-group">
                    <label>Akun TikTok/Shopee *</label>
                    <input type="text" id="editReportTiktokAkun" required value="${report.tiktok_akun || ''}">
                </div>
                <div class="form-group">
                    <label>Platform *</label>
                    <select id="editReportPlatform" required>
                        <option value="tiktok" ${report.platform === 'tiktok' ? 'selected' : ''}>TikTok</option>
                        <option value="shopee" ${report.platform === 'shopee' ? 'selected' : ''}>Shopee</option>
                    </select>
                </div>
                <div class="form-group">
                    <label>Produk (Optional)</label>
                    <select id="editReportProductId">
                        <option value="">Pilih Produk (Opsional)</option>
                        ${products.map(p => `<option value="${p.id}" ${p.id === report.product_id ? 'selected' : ''}>${p.product_name}</option>`).join('')}
                    </select>
                </div>
                <div class="form-group">
                    <label>Deskripsi (Optional)</label>
                    <textarea id="editReportDescription" rows="3">${report.description || ''}</textarea>
                </div>
                <div style="padding: 10px; background: #fff3cd; border-radius: 4px; margin-bottom: 15px;">
                    <strong>Status:</strong> <span class="badge badge-warning">${report.status}</span><br>
                    <small>Hanya laporan dengan status "pending" yang bisa di-edit.</small>
                </div>
                <button type="submit" class="btn btn-primary btn-block">Update Report</button>
                <button type="button" class="btn btn-secondary btn-block" onclick="closeModal()" style="margin-top: 10px;">Cancel</button>
            </form>
        `;
        
        document.getElementById('modal').classList.remove('hidden');
        
        document.getElementById('editReportForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            await updateMyReport(reportId);
        });
        
    } catch (error) {
        alert('Error loading report: ' + error.message);
    }
}

async function updateMyReport(reportId) {
    try {
        const linkVideo = document.getElementById('editReportLinkVideo').value.trim();
        const tanggalUpload = document.getElementById('editReportTanggalUpload').value;
        const tiktokAkun = document.getElementById('editReportTiktokAkun').value.trim();
        const platform = document.getElementById('editReportPlatform').value;
        const productId = document.getElementById('editReportProductId').value;
        const description = document.getElementById('editReportDescription').value.trim();
        
        const data = {
            link_video: linkVideo,
            tanggal_upload: tanggalUpload,
            tiktok_akun: tiktokAkun,
            platform: platform
        };
        
        if (productId) {
            data.product_id = parseInt(productId);
        } else {
            data.product_id = null;
        }
        
        if (description) {
            data.description = description;
        }
        
        const res = await authenticatedFetch(`${API_URL}/my/reports/${reportId}`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
        
        if (!res.ok) {
            const error = await res.json();
            throw new Error(error.error || 'Gagal update laporan');
        }
        
        alert('✅ Laporan berhasil di-update!');
        closeModal();
        loadMyReports(currentMyReportPage);
        
    } catch (error) {
        alert('Error updating report: ' + error.message);
    }
}

async function deleteMyReport(reportId) {
    if (!confirm('Apakah Anda yakin ingin menghapus laporan ini? Laporan yang sudah di-approve atau di-reject tidak bisa di-hapus.')) {
        return;
    }
    
    try {
        const res = await authenticatedFetch(`${API_URL}/my/reports/${reportId}`, {
            method: 'DELETE'
        });
        
        if (!res.ok) {
            const error = await res.json();
            throw new Error(error.error || 'Gagal menghapus laporan');
        }
        
        alert('✅ Laporan berhasil di-hapus!');
        loadMyReports(currentMyReportPage);
        
    } catch (error) {
        alert('Error deleting report: ' + error.message);
    }
}

async function viewMyReport(reportId) {
    try {
        const res = await authenticatedFetch(`${API_URL}/my/reports/${reportId}`);
        if (!res.ok) {
            const error = await res.json();
            throw new Error(error.error || 'Gagal memuat laporan');
        }
        
        const report = await res.json();
        
        const modalBody = document.getElementById('modalBody');
        const statusBadge = report.status === 'approved' ? 'badge-success' : 
                           report.status === 'rejected' ? 'badge-danger' : 'badge-warning';
        const statusText = report.status === 'approved' ? '✅ Approved' : 
                          report.status === 'rejected' ? '❌ Rejected' : '⏳ Pending';
        
        modalBody.innerHTML = `
            <h2>👁️ View Report</h2>
            <div style="padding: 20px;">
                <div style="margin-bottom: 15px;">
                    <strong>Link Video:</strong><br>
                    <a href="${report.link_video || '#'}" target="_blank" style="color: #007bff; word-break: break-all;">${report.link_video || '-'}</a>
                </div>
                <div style="margin-bottom: 15px;">
                    <strong>Tanggal Upload:</strong> ${report.tanggal_upload ? new Date(report.tanggal_upload).toLocaleDateString('id-ID') : '-'}
                </div>
                <div style="margin-bottom: 15px;">
                    <strong>Akun TikTok/Shopee:</strong> ${report.tiktok_akun || '-'}
                </div>
                <div style="margin-bottom: 15px;">
                    <strong>Platform:</strong> <span class="badge badge-info">${report.platform || 'tiktok'}</span>
                </div>
                <div style="margin-bottom: 15px;">
                    <strong>Produk:</strong> ${report.product_name || '-'}
                </div>
                <div style="margin-bottom: 15px;">
                    <strong>Status:</strong> <span class="badge ${statusBadge}">${statusText}</span>
                </div>
                ${report.description ? `<div style="margin-bottom: 15px;">
                    <strong>Deskripsi:</strong><br>
                    ${report.description}
                </div>` : ''}
                <div style="margin-bottom: 15px;">
                    <strong>Created At:</strong> ${report.created_at ? new Date(report.created_at).toLocaleString('id-ID') : '-'}
                </div>
                ${report.updated_at ? `<div style="margin-bottom: 15px;">
                    <strong>Updated At:</strong> ${new Date(report.updated_at).toLocaleString('id-ID')}
                </div>` : ''}
            </div>
            <button type="button" class="btn btn-secondary btn-block" onclick="closeModal()">Close</button>
        `;
        
        document.getElementById('modal').classList.remove('hidden');
        
    } catch (error) {
        alert('Error loading report: ' + error.message);
    }
}

// ==================== NOTIFICATIONS ====================
let notificationPollInterval = null;

async function loadNotifications(unreadOnly = false) {
    try {
        const url = `${API_URL}/notifications?page=1&per_page=20${unreadOnly ? '&unread_only=true' : ''}`;
        const res = await authenticatedFetch(url);
        
        if (!res.ok) {
            throw new Error('Failed to load notifications');
        }
        
        const data = await res.json();
        const notifications = data.notifications || [];
        const unreadCount = data.unread_count || 0;
        
        // Update badge count
        const badgeCount = document.getElementById('notificationCount');
        if (badgeCount) {
            if (unreadCount > 0) {
                badgeCount.textContent = unreadCount > 99 ? '99+' : unreadCount;
                badgeCount.style.display = 'flex';
            } else {
                badgeCount.style.display = 'none';
            }
        }
        
        // Update notification list
        const notificationList = document.getElementById('notificationList');
        if (notificationList) {
            if (notifications.length === 0) {
                notificationList.innerHTML = '<div style="padding: 20px; text-align: center; color: #666;">No notifications</div>';
            } else {
                notificationList.innerHTML = notifications.map(notif => {
                    const timeAgo = getTimeAgo(notif.created_at);
                    const unreadClass = !notif.is_read ? 'unread' : '';
                    const icon = getNotificationIcon(notif.type);
                    
                    return `
                        <div class="notification-item ${unreadClass}" onclick="markNotificationRead(${notif.id})">
                            <div class="notification-title">${icon} ${notif.title}</div>
                            ${notif.message ? `<div class="notification-message">${notif.message}</div>` : ''}
                            <div class="notification-time">${timeAgo}</div>
                            <div class="notification-actions">
                                ${!notif.is_read ? `<button class="btn-mark-read" onclick="event.stopPropagation(); markNotificationRead(${notif.id})">Mark Read</button>` : ''}
                                <button class="btn-delete" onclick="event.stopPropagation(); deleteNotification(${notif.id})">Delete</button>
                            </div>
                        </div>
                    `;
                }).join('');
            }
        }
        
    } catch (error) {
        console.error('Error loading notifications:', error);
    }
}

function getNotificationIcon(type) {
    const icons = {
        'report_approved': '✅',
        'report_rejected': '❌',
        'commission_added': '💰',
        'milestone': '🎉',
        'reminder': '⏰'
    };
    return icons[type] || '🔔';
}

function getTimeAgo(dateString) {
    if (!dateString) return '';
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins} minute${diffMins > 1 ? 's' : ''} ago`;
    if (diffHours < 24) return `${diffHours} hour${diffHours > 1 ? 's' : ''} ago`;
    if (diffDays < 7) return `${diffDays} day${diffDays > 1 ? 's' : ''} ago`;
    return date.toLocaleDateString('id-ID');
}

function toggleNotifications() {
    const dropdown = document.getElementById('notificationDropdown');
    if (dropdown) {
        dropdown.classList.toggle('hidden');
        if (!dropdown.classList.contains('hidden')) {
            loadNotifications();
        }
    }
}

async function markNotificationRead(notificationId) {
    try {
        const res = await authenticatedFetch(`${API_URL}/notifications/${notificationId}/read`, {
            method: 'POST'
        });
        
        if (res.ok) {
            // Reload notifications
            loadNotifications();
            // Update unread count
            updateUnreadCount();
        }
    } catch (error) {
        console.error('Error marking notification as read:', error);
    }
}

async function markAllNotificationsRead() {
    try {
        const res = await authenticatedFetch(`${API_URL}/notifications/read-all`, {
            method: 'POST'
        });
        
        if (res.ok) {
            loadNotifications();
            updateUnreadCount();
        }
    } catch (error) {
        console.error('Error marking all notifications as read:', error);
    }
}

async function deleteNotification(notificationId) {
    if (!confirm('Delete this notification?')) {
        return;
    }
    
    try {
        const res = await authenticatedFetch(`${API_URL}/notifications/${notificationId}`, {
            method: 'DELETE'
        });
        
        if (res.ok) {
            loadNotifications();
            updateUnreadCount();
        }
    } catch (error) {
        console.error('Error deleting notification:', error);
        alert('Error deleting notification: ' + error.message);
    }
}

async function updateUnreadCount() {
    try {
        const res = await authenticatedFetch(`${API_URL}/notifications/unread-count`);
        if (res.ok) {
            const data = await res.json();
            const unreadCount = data.unread_count || 0;
            const badgeCount = document.getElementById('notificationCount');
            if (badgeCount) {
                if (unreadCount > 0) {
                    badgeCount.textContent = unreadCount > 99 ? '99+' : unreadCount;
                    badgeCount.style.display = 'flex';
                } else {
                    badgeCount.style.display = 'none';
                }
            }
        }
    } catch (error) {
        console.error('Error updating unread count:', error);
    }
}

function startNotificationPolling() {
    // Update unread count every 30 seconds
    if (notificationPollInterval) {
        clearInterval(notificationPollInterval);
    }
    
    // Initial load
    updateUnreadCount();
    
    // Poll every 30 seconds
    notificationPollInterval = setInterval(() => {
        updateUnreadCount();
    }, 30000);
}

function stopNotificationPolling() {
    if (notificationPollInterval) {
        clearInterval(notificationPollInterval);
        notificationPollInterval = null;
    }
}

// Close notification dropdown when clicking outside
document.addEventListener('click', (e) => {
    const dropdown = document.getElementById('notificationDropdown');
    const btn = document.getElementById('notificationBtn');
    if (dropdown && btn && !dropdown.contains(e.target) && !btn.contains(e.target)) {
        dropdown.classList.add('hidden');
    }
});

// ==================== MY COMMISSIONS (User-specific) ====================
async function loadMyCommissions() {
    try {
        const res = await authenticatedFetch(`${API_URL}/commissions`);
        const commissions = await res.json();
        
        if (!Array.isArray(commissions)) {
            throw new Error('Invalid response format: expected array');
        }
        
        // Calculate summary
        const totalCommission = commissions.reduce((sum, c) => sum + (c.team_share || 0), 0);
        const totalPending = commissions.filter(c => c.status === 'pending').reduce((sum, c) => sum + (c.team_share || 0), 0);
        const totalPaid = commissions.filter(c => c.status === 'paid').reduce((sum, c) => sum + (c.team_share || 0), 0);
        
        const summaryDiv = document.getElementById('myCommissionsSummary');
        summaryDiv.innerHTML = `
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 15px;">
                <div><strong>Total Commissions:</strong><br>${formatCurrency(totalCommission)}</div>
                <div><strong>Pending:</strong><br>${formatCurrency(totalPending)}</div>
                <div><strong>Paid:</strong><br>${formatCurrency(totalPaid)}</div>
            </div>
        `;
        
        const tbody = document.getElementById('myCommissionsTable');
        if (commissions.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align: center;">Belum ada komisi</td></tr>';
        } else {
            tbody.innerHTML = commissions.map(c => `
                <tr>
                    <td>${c.created_at ? new Date(c.created_at).toLocaleDateString('id-ID') : '-'}</td>
                    <td>${formatCurrency(c.total_commission || 0)}</td>
                    <td><strong>${formatCurrency(c.team_share || 0)}</strong></td>
                    <td>${formatCurrency(c.owner_share || 0)}</td>
                    <td>${formatCurrency(c.manager_bonus || 0)}</td>
                    <td><span class="badge badge-${c.status === 'paid' ? 'success' : 'warning'}">${c.status || 'pending'}</span></td>
                </tr>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading my commissions:', error);
        alert('Error loading commissions: ' + error.message);
    }
}

// ==================== MY PAYMENTS (User-specific) ====================
async function loadMyPayments() {
    try {
        const res = await authenticatedFetch(`${API_URL}/payments`);
        const payments = await res.json();
        
        if (!Array.isArray(payments)) {
            throw new Error('Invalid response format: expected array');
        }
        
        // Calculate summary
        const totalAmount = payments.reduce((sum, p) => sum + (p.amount || 0), 0);
        const totalPending = payments.filter(p => p.status === 'pending').reduce((sum, p) => sum + (p.amount || 0), 0);
        const totalPaid = payments.filter(p => p.status === 'paid').reduce((sum, p) => sum + (p.amount || 0), 0);
        
        const summaryDiv = document.getElementById('myPaymentsSummary');
        summaryDiv.innerHTML = `
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 15px;">
                <div><strong>Total Amount:</strong><br>${formatCurrency(totalAmount)}</div>
                <div><strong>Pending:</strong><br>${formatCurrency(totalPending)}</div>
                <div><strong>Paid:</strong><br>${formatCurrency(totalPaid)}</div>
            </div>
        `;
        
        const tbody = document.getElementById('myPaymentsTable');
        if (payments.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" style="text-align: center;">Belum ada payment</td></tr>';
        } else {
            tbody.innerHTML = payments.map(p => `
                <tr>
                    <td>${p.period || 'N/A'}</td>
                    <td><strong>${formatCurrency(p.amount || 0)}</strong></td>
                    <td>${p.payment_type || '-'}</td>
                    <td><span class="badge badge-${p.status === 'paid' ? 'success' : 'warning'}">${p.status || 'pending'}</span></td>
                    <td>${p.created_at ? new Date(p.created_at).toLocaleDateString('id-ID') : '-'}</td>
                </tr>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading my payments:', error);
        alert('Error loading payments: ' + error.message);
    }
}

// ==================== MY PROFILE (User-specific) ====================
async function loadMyProfile() {
    try {
        const res = await authenticatedFetch(`${API_URL}/my/profile`);
        const profile = await res.json();
        
        document.getElementById('myProfileUsername').value = profile.username || '';
        document.getElementById('myProfileFullName').value = profile.full_name || '';
        document.getElementById('myProfileEmail').value = profile.email || '';
        document.getElementById('myProfileWhatsApp').value = profile.whatsapp || '';
        document.getElementById('myProfileWallet').value = profile.wallet || '';
        document.getElementById('myProfileBankAccount').value = profile.bank_account || '';
        
        // Setup form submit handler
        const form = document.getElementById('myProfileForm');
        form.onsubmit = async (e) => {
            e.preventDefault();
            await updateMyProfile();
        };
    } catch (error) {
        console.error('Error loading my profile:', error);
        alert('Error loading profile: ' + error.message);
    }
}

async function updateMyProfile() {
    try {
        const data = {
            full_name: document.getElementById('myProfileFullName').value.trim(),
            email: document.getElementById('myProfileEmail').value.trim(),
            whatsapp: document.getElementById('myProfileWhatsApp').value.trim(),
            wallet: document.getElementById('myProfileWallet').value.trim(),
            bank_account: document.getElementById('myProfileBankAccount').value.trim()
        };
        
        const res = await authenticatedFetch(`${API_URL}/my/profile`, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
        
        if (!res.ok) {
            const error = await res.json();
            throw new Error(error.error || 'Update profile gagal');
        }
        
        const result = await res.json();
        alert('Profile berhasil diupdate!');
        loadMyProfile(); // Reload to show updated data
    } catch (error) {
        console.error('Error updating profile:', error);
        alert('Error: ' + error.message);
    }
}

// ==================== UTILS ====================
function formatCurrency(amount) {
    // Format sesuai Google Sheets: Rp50,000 (tanpa spasi, koma sebagai pemisah ribuan)
    if (amount === null || amount === undefined || isNaN(amount)) {
        return 'Rp0';
    }
    const num = parseFloat(amount);
    return `Rp${num.toLocaleString('en-US', { minimumFractionDigits: 0, maximumFractionDigits: 0 })}`;
}

function showAlert(id, message, type) {
    const alertDiv = document.getElementById(id);
    alertDiv.innerHTML = `<div class="alert alert-${type}">${message}</div>`;
    setTimeout(() => {
        alertDiv.innerHTML = '';
    }, 5000);
}

function closeModal() {
    document.getElementById('modal').classList.add('hidden');
}

// ==================== BOT STATUS ====================
async function checkBotStatus() {
    const statusDiv = document.getElementById('botStatusInfo');
    if (!statusDiv) {
        // If section not active, show it first
        showSection('bot-status');
        await new Promise(resolve => setTimeout(resolve, 100));
        return checkBotStatus();
    }
    
    statusDiv.innerHTML = `
        <div style="font-size: 48px; margin-bottom: 20px;">⏳</div>
        <p>Checking bot status...</p>
    `;
    
    try {
        // Check via Telegram API (indirect check)
        const token = '8524026560:AAFRvTa0o52AB3GlPMCxY48Cvq7SRUkmDqE';
        const response = await fetch(`https://api.telegram.org/bot${token}/getMe`);
        const data = await response.json();
        
        if (data.ok && data.result) {
            const bot = data.result;
            statusDiv.innerHTML = `
                <div style="font-size: 48px; margin-bottom: 20px; color: #28a745;">✅</div>
                <h3 style="color: #28a745;">Bot is Running!</h3>
                <div style="margin-top: 20px; text-align: left; display: inline-block;">
                    <p><strong>Bot Name:</strong> ${bot.first_name || 'N/A'}</p>
                    <p><strong>Username:</strong> @${bot.username || 'N/A'}</p>
                    <p><strong>Bot ID:</strong> ${bot.id || 'N/A'}</p>
                </div>
                <div style="margin-top: 20px; padding: 15px; background: #d4edda; border-radius: 8px; color: #155724;">
                    <strong>✅ Bot siap digunakan!</strong><br>
                    Semua commands sudah aktif dan bot bisa receive messages.
                </div>
            `;
        } else {
            throw new Error('Bot API not responding');
        }
    } catch (error) {
        statusDiv.innerHTML = `
            <div style="font-size: 48px; margin-bottom: 20px; color: #dc3545;">❌</div>
            <h3 style="color: #dc3545;">Bot is Not Running</h3>
            <p style="margin-top: 20px;">Bot tidak terdeteksi atau tidak bisa terhubung.</p>
            <p style="margin-top: 10px; color: #6c757d;">
                Pastikan <code>app.py</code> sedang running di terminal.
            </p>
            <div style="margin-top: 20px; padding: 15px; background: #f8d7da; border-radius: 8px; color: #721c24;">
                <strong>⚠️ Bot belum running!</strong><br>
                Silakan start bot dengan double-click <code>START_BOT.bat</code>
            </div>
        `;
    }
}

function openBotFolder() {
    // Open folder in Windows Explorer
    const folderPath = 'D:\\affiliate-system';
    // Use file:// protocol for Windows
    window.open(`file:///${folderPath.replace(/\\/g, '/')}`, '_blank');
}

// ==================== DAILY COMMISSIONS ====================
async function loadDailyCommissions() {
    try {
        const dateFilterEl = document.getElementById('dailyCommDateFilter');
        // Set default to today if not set
        if (dateFilterEl && !dateFilterEl.value) {
            const today = new Date().toISOString().split('T')[0];
            dateFilterEl.value = today;
        }
        const dateFilter = dateFilterEl?.value || '';
        let url = `${API_URL}/daily-commissions`;
        if (dateFilter) {
            url += `?date=${dateFilter}`;
        }
        
        const res = await authenticatedFetch(url);
        const data = await res.json();
        
        const commissions = Array.isArray(data.daily_commissions) ? data.daily_commissions : [];
        
        const tbody = document.getElementById('dailyCommissionsTable');
        if (commissions.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align: center; padding: 20px;">Belum ada komisi harian</td></tr>';
        } else {
            tbody.innerHTML = commissions.map(dc => `
                <tr>
                    <td>${dc.date || '-'}</td>
                    <td><strong>${dc.user_name || 'N/A'}</strong></td>
                    <td>${formatCurrency(dc.commission_amount || 0)}</td>
                    <td>${dc.notes || '-'}</td>
                    <td>${dc.updated_by_name || '-'}</td>
                    <td>
                        <button class="btn btn-primary btn-sm" onclick="editDailyCommission(${dc.id})" style="margin-right: 5px;">✏️ Edit</button>
                        <button class="btn btn-danger btn-sm" onclick="deleteDailyCommission(${dc.id})">🗑️ Hapus</button>
                    </td>
                </tr>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading daily commissions:', error);
        const tbody = document.getElementById('dailyCommissionsTable');
        if (tbody) {
            tbody.innerHTML = `<tr><td colspan="6" style="text-align: center; padding: 20px; color: #dc3545;">Error loading daily commissions: ${error.message}</td></tr>`;
        }
        alert('Error loading daily commissions: ' + error.message);
    }
}

async function showAddDailyCommissionModal() {
    // Load users
    let users = [];
    try {
        const usersRes = await authenticatedFetch(`${API_URL}/users`);
        const usersData = await usersRes.json();
        users = Array.isArray(usersData.users) ? usersData.users : (Array.isArray(usersData) ? usersData : []);
        users = users.filter(u => u.role === 'member');
    } catch (error) {
        console.error('Error loading users:', error);
        alert('Error loading users: ' + error.message);
        return;
    }
    
    const today = new Date().toISOString().split('T')[0];
    
    const modalBody = document.getElementById('modalBody');
    modalBody.innerHTML = `
        <h2>➕ Tambah Komisi Harian</h2>
        <form id="addDailyCommissionForm">
            <div class="form-group">
                <label>Tanggal *</label>
                <input type="date" id="dailyCommDate" value="${today}" required max="${today}">
            </div>
            <div class="form-group">
                <label>Member *</label>
                <select id="dailyCommUserId" required>
                    <option value="">Pilih Member</option>
                    ${users.map(u => `<option value="${u.id}">${u.full_name || u.username}</option>`).join('')}
                </select>
            </div>
            <div class="form-group">
                <label>Jumlah Komisi (Rp) *</label>
                <input type="number" id="dailyCommAmount" required min="0" step="100" placeholder="50000">
            </div>
            <div class="form-group">
                <label>Catatan</label>
                <textarea id="dailyCommNotes" rows="3" placeholder="Catatan (opsional)"></textarea>
            </div>
            <button type="submit" class="btn btn-primary btn-block">Simpan Komisi</button>
        </form>
    `;
    document.getElementById('modal').classList.remove('hidden');
    
    document.getElementById('addDailyCommissionForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const data = {
            user_id: parseInt(document.getElementById('dailyCommUserId').value),
            date: document.getElementById('dailyCommDate').value,
            commission_amount: parseFloat(document.getElementById('dailyCommAmount').value),
            notes: document.getElementById('dailyCommNotes').value.trim()
        };
        
        try {
            const res = await authenticatedFetch(`${API_URL}/daily-commissions`, {
                method: 'POST',
                body: JSON.stringify(data)
            });
            
            if (res.ok) {
                closeModal();
                loadDailyCommissions();
                alert('Komisi harian berhasil disimpan!');
            } else {
                const error = await res.json();
                alert('Error: ' + (error.error || 'Gagal menyimpan komisi'));
            }
        } catch (error) {
            alert('Error: ' + error.message);
        }
    });
}

async function editDailyCommission(commissionId) {
    try {
        const res = await authenticatedFetch(`${API_URL}/daily-commissions`);
        const data = await res.json();
        const commissions = Array.isArray(data.daily_commissions) ? data.daily_commissions : [];
        const commission = commissions.find(dc => dc.id === commissionId);
        
        if (!commission) {
            alert('Komisi tidak ditemukan');
            return;
        }
        
        // Load users
        let users = [];
        try {
            const usersRes = await authenticatedFetch(`${API_URL}/users`);
            const usersData = await usersRes.json();
            users = Array.isArray(usersData.users) ? usersData.users : (Array.isArray(usersData) ? usersData : []);
            users = users.filter(u => u.role === 'member');
        } catch (error) {
            console.error('Error loading users:', error);
        }
        
        const modalBody = document.getElementById('modalBody');
        modalBody.innerHTML = `
            <h2>✏️ Edit Komisi Harian</h2>
            <form id="editDailyCommissionForm">
                <div class="form-group">
                    <label>Tanggal *</label>
                    <input type="date" id="editDailyCommDate" value="${commission.date}" required>
                </div>
                <div class="form-group">
                    <label>Member *</label>
                    <select id="editDailyCommUserId" required>
                        ${users.map(u => `<option value="${u.id}" ${u.id === commission.user_id ? 'selected' : ''}>${u.full_name || u.username}</option>`).join('')}
                    </select>
                </div>
                <div class="form-group">
                    <label>Jumlah Komisi (Rp) *</label>
                    <input type="number" id="editDailyCommAmount" value="${commission.commission_amount}" required min="0" step="100">
                </div>
                <div class="form-group">
                    <label>Catatan</label>
                    <textarea id="editDailyCommNotes" rows="3">${commission.notes || ''}</textarea>
                </div>
                <button type="submit" class="btn btn-primary btn-block">Update Komisi</button>
            </form>
        `;
        document.getElementById('modal').classList.remove('hidden');
        
        document.getElementById('editDailyCommissionForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const data = {
                date: document.getElementById('editDailyCommDate').value,
                commission_amount: parseFloat(document.getElementById('editDailyCommAmount').value),
                notes: document.getElementById('editDailyCommNotes').value.trim()
            };
            
            try {
                const res = await authenticatedFetch(`${API_URL}/daily-commissions/${commissionId}`, {
                    method: 'PUT',
                    body: JSON.stringify(data)
                });
                
                if (res.ok) {
                    closeModal();
                    loadDailyCommissions();
                    alert('Komisi harian berhasil diupdate!');
                } else {
                    const error = await res.json();
                    alert('Error: ' + (error.error || 'Gagal update komisi'));
                }
            } catch (error) {
                alert('Error: ' + error.message);
            }
        });
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function deleteDailyCommission(commissionId) {
    if (!confirm('Yakin ingin menghapus komisi harian ini?')) return;
    
    try {
        const res = await authenticatedFetch(`${API_URL}/daily-commissions/${commissionId}`, {
            method: 'DELETE'
        });
        
        if (res.ok) {
            loadDailyCommissions();
            alert('Komisi harian berhasil dihapus!');
        } else {
            const error = await res.json();
            alert('Error: ' + (error.error || 'Gagal menghapus komisi'));
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// ==================== VIDEO STATISTICS ====================
async function loadVideoStatistics() {
    try {
        const dateFilterEl = document.getElementById('videoStatDateFilter');
        // Set default to today if not set
        if (dateFilterEl && !dateFilterEl.value) {
            const today = new Date().toISOString().split('T')[0];
            dateFilterEl.value = today;
        }
        const dateFilter = dateFilterEl?.value || '';
        let url = `${API_URL}/video-statistics`;
        if (dateFilter) {
            url += `?date=${dateFilter}`;
        }
        
        const res = await authenticatedFetch(url);
        const data = await res.json();
        
        const statistics = Array.isArray(data.video_statistics) ? data.video_statistics : [];
        
        const tbody = document.getElementById('videoStatisticsTable');
        if (statistics.length === 0) {
            tbody.innerHTML = '<tr><td colspan="7" style="text-align: center; padding: 20px;">Belum ada statistik video</td></tr>';
        } else {
            tbody.innerHTML = statistics.map(vs => `
                <tr>
                    <td>${vs.date || '-'}</td>
                    <td><strong>${vs.user_name || 'N/A'}</strong></td>
                    <td>${vs.tiktok_akun || '-'}</td>
                    <td>${vs.video_count || 0}</td>
                    <td>${vs.total_views || 0}</td>
                    <td>${vs.total_likes || 0}</td>
                    <td>
                        <button class="btn btn-primary btn-sm" onclick="editVideoStatistic(${vs.id})" style="margin-right: 5px;">✏️ Edit</button>
                        <button class="btn btn-danger btn-sm" onclick="deleteVideoStatistic(${vs.id})">🗑️ Hapus</button>
                    </td>
                </tr>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading video statistics:', error);
        const tbody = document.getElementById('videoStatisticsTable');
        if (tbody) {
            tbody.innerHTML = `<tr><td colspan="7" style="text-align: center; padding: 20px; color: #dc3545;">Error loading video statistics: ${error.message}</td></tr>`;
        }
        alert('Error loading video statistics: ' + error.message);
    }
}

async function showAddVideoStatisticModal() {
    // Load users
    let users = [];
    try {
        const usersRes = await authenticatedFetch(`${API_URL}/users`);
        const usersData = await usersRes.json();
        users = Array.isArray(usersData.users) ? usersData.users : (Array.isArray(usersData) ? usersData : []);
        users = users.filter(u => u.role === 'member');
    } catch (error) {
        console.error('Error loading users:', error);
        alert('Error loading users: ' + error.message);
        return;
    }
    
    const today = new Date().toISOString().split('T')[0];
    
    const modalBody = document.getElementById('modalBody');
    modalBody.innerHTML = `
        <h2>➕ Tambah Statistik Video</h2>
        <form id="addVideoStatisticForm">
            <div class="form-group">
                <label>Tanggal *</label>
                <input type="date" id="videoStatDate" value="${today}" required max="${today}">
            </div>
            <div class="form-group">
                <label>Member *</label>
                <select id="videoStatUserId" required>
                    <option value="">Pilih Member</option>
                    ${users.map(u => `<option value="${u.id}">${u.full_name || u.username}</option>`).join('')}
                </select>
            </div>
            <div class="form-group">
                <label>TikTok Akun *</label>
                <input type="text" id="videoStatTiktokAkun" required placeholder="@username atau username">
            </div>
            <div class="form-group">
                <label>Jumlah Video *</label>
                <input type="number" id="videoStatCount" required min="0" placeholder="5">
            </div>
            <div class="form-group">
                <label>Total Views (Opsional)</label>
                <input type="number" id="videoStatViews" min="0" placeholder="0">
            </div>
            <div class="form-group">
                <label>Total Likes (Opsional)</label>
                <input type="number" id="videoStatLikes" min="0" placeholder="0">
            </div>
            <button type="submit" class="btn btn-primary btn-block">Simpan Statistik</button>
        </form>
    `;
    document.getElementById('modal').classList.remove('hidden');
    
    document.getElementById('addVideoStatisticForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const data = {
            user_id: parseInt(document.getElementById('videoStatUserId').value),
            date: document.getElementById('videoStatDate').value,
            tiktok_akun: document.getElementById('videoStatTiktokAkun').value.trim(),
            video_count: parseInt(document.getElementById('videoStatCount').value),
            total_views: parseInt(document.getElementById('videoStatViews').value) || 0,
            total_likes: parseInt(document.getElementById('videoStatLikes').value) || 0
        };
        
        try {
            const res = await authenticatedFetch(`${API_URL}/video-statistics`, {
                method: 'POST',
                body: JSON.stringify(data)
            });
            
            if (res.ok) {
                closeModal();
                loadVideoStatistics();
                alert('Statistik video berhasil disimpan!');
            } else {
                const error = await res.json();
                alert('Error: ' + (error.error || 'Gagal menyimpan statistik'));
            }
        } catch (error) {
            alert('Error: ' + error.message);
        }
    });
}

async function editVideoStatistic(statisticId) {
    try {
        const res = await authenticatedFetch(`${API_URL}/video-statistics`);
        const data = await res.json();
        const statistics = Array.isArray(data.video_statistics) ? data.video_statistics : [];
        const statistic = statistics.find(vs => vs.id === statisticId);
        
        if (!statistic) {
            alert('Statistik tidak ditemukan');
            return;
        }
        
        // Load users
        let users = [];
        try {
            const usersRes = await authenticatedFetch(`${API_URL}/users`);
            const usersData = await usersRes.json();
            users = Array.isArray(usersData.users) ? usersData.users : (Array.isArray(usersData) ? usersData : []);
            users = users.filter(u => u.role === 'member');
        } catch (error) {
            console.error('Error loading users:', error);
        }
        
        const modalBody = document.getElementById('modalBody');
        modalBody.innerHTML = `
            <h2>✏️ Edit Statistik Video</h2>
            <form id="editVideoStatisticForm">
                <div class="form-group">
                    <label>Tanggal *</label>
                    <input type="date" id="editVideoStatDate" value="${statistic.date}" required>
                </div>
                <div class="form-group">
                    <label>Member *</label>
                    <select id="editVideoStatUserId" required>
                        ${users.map(u => `<option value="${u.id}" ${u.id === statistic.user_id ? 'selected' : ''}>${u.full_name || u.username}</option>`).join('')}
                    </select>
                </div>
                <div class="form-group">
                    <label>TikTok Akun *</label>
                    <input type="text" id="editVideoStatTiktokAkun" value="${statistic.tiktok_akun}" required>
                </div>
                <div class="form-group">
                    <label>Jumlah Video *</label>
                    <input type="number" id="editVideoStatCount" value="${statistic.video_count}" required min="0">
                </div>
                <div class="form-group">
                    <label>Total Views</label>
                    <input type="number" id="editVideoStatViews" value="${statistic.total_views || 0}" min="0">
                </div>
                <div class="form-group">
                    <label>Total Likes</label>
                    <input type="number" id="editVideoStatLikes" value="${statistic.total_likes || 0}" min="0">
                </div>
                <button type="submit" class="btn btn-primary btn-block">Update Statistik</button>
            </form>
        `;
        document.getElementById('modal').classList.remove('hidden');
        
        document.getElementById('editVideoStatisticForm').addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const data = {
                date: document.getElementById('editVideoStatDate').value,
                tiktok_akun: document.getElementById('editVideoStatTiktokAkun').value.trim(),
                video_count: parseInt(document.getElementById('editVideoStatCount').value),
                total_views: parseInt(document.getElementById('editVideoStatViews').value) || 0,
                total_likes: parseInt(document.getElementById('editVideoStatLikes').value) || 0
            };
            
            try {
                const res = await authenticatedFetch(`${API_URL}/video-statistics/${statisticId}`, {
                    method: 'PUT',
                    body: JSON.stringify(data)
                });
                
                if (res.ok) {
                    closeModal();
                    loadVideoStatistics();
                    alert('Statistik video berhasil diupdate!');
                } else {
                    const error = await res.json();
                    alert('Error: ' + (error.error || 'Gagal update statistik'));
                }
            } catch (error) {
                alert('Error: ' + error.message);
            }
        });
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function deleteVideoStatistic(statisticId) {
    if (!confirm('Yakin ingin menghapus statistik video ini?')) return;
    
    try {
        const res = await authenticatedFetch(`${API_URL}/video-statistics/${statisticId}`, {
            method: 'DELETE'
        });
        
        if (res.ok) {
            loadVideoStatistics();
            alert('Statistik video berhasil dihapus!');
        } else {
            const error = await res.json();
            alert('Error: ' + (error.error || 'Gagal menghapus statistik'));
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

async function autoSyncVideoStatistics() {
    if (!confirm('Auto-sync statistik video dari data content yang sudah ada?\n\nIni akan menghitung jumlah video per member per akun per tanggal dari data content.')) {
        return;
    }
    
    try {
        const res = await authenticatedFetch(`${API_URL}/video-statistics/auto-sync`, {
            method: 'POST',
            body: JSON.stringify({})
        });
        
        if (res.ok) {
            const data = await res.json();
            alert(`Auto-sync berhasil!\n\nCreated: ${data.created}\nUpdated: ${data.updated}\nTotal: ${data.total}`);
            loadVideoStatistics();
        } else {
            const error = await res.json();
            alert('Error: ' + (error.error || 'Auto-sync gagal'));
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// ==================== MEMBER DAILY SUMMARY ====================
async function loadMemberSummary() {
    try {
        const dateFrom = document.getElementById('summaryDateFrom')?.value || '';
        const dateTo = document.getElementById('summaryDateTo')?.value || '';
        
        let url = `${API_URL}/member-daily-summary`;
        const params = [];
        if (dateFrom) params.push(`date_from=${dateFrom}`);
        if (dateTo) params.push(`date_to=${dateTo}`);
        if (params.length > 0) {
            url += '?' + params.join('&');
        }
        
        const res = await authenticatedFetch(url);
        const data = await res.json();
        
        const summaries = Array.isArray(data.summaries) ? data.summaries : [];
        
        const tbody = document.getElementById('memberSummaryTable');
        if (summaries.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 20px;">Belum ada data summary</td></tr>';
        } else {
            tbody.innerHTML = summaries.map(s => `
                <tr>
                    <td>${s.date || '-'}</td>
                    <td><strong>${s.user_name || 'N/A'}</strong></td>
                    <td>${formatCurrency(s.total_commission || 0)}</td>
                    <td>${s.total_videos || 0}</td>
                    <td>${s.total_akun || 0}</td>
                </tr>
            `).join('');
        }
    } catch (error) {
        console.error('Error loading member summary:', error);
        const tbody = document.getElementById('memberSummaryTable');
        if (tbody) {
            tbody.innerHTML = `<tr><td colspan="5" style="text-align: center; padding: 20px; color: #dc3545;">Error loading member summary: ${error.message}</td></tr>`;
        }
        alert('Error loading member summary: ' + error.message);
    }
}

