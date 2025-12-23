# Test API Endpoints Script
# Jalankan: .\test_api.ps1

Write-Host "========================================"
Write-Host "   TEST API ENDPOINTS"
Write-Host "========================================"
Write-Host ""

# Base URL
$baseUrl = "http://localhost:5000"

# Test Health Check (No auth needed)
Write-Host "=== 1. Health Check ===" -ForegroundColor Green
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/health" -Method GET
    Write-Host "Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "Response:" -ForegroundColor Yellow
    $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 10
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}
Write-Host ""

# Test API Docs (No auth needed)
Write-Host "=== 2. API Documentation ===" -ForegroundColor Green
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/api/docs" -Method GET
    Write-Host "Status: $($response.StatusCode)" -ForegroundColor Green
    Write-Host "Response:" -ForegroundColor Yellow
    $response.Content | ConvertFrom-Json | ConvertTo-Json -Depth 5
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}
Write-Host ""

# Login to get token
Write-Host "=== 3. Login ===" -ForegroundColor Green
try {
    $loginBody = @{
        username = "owner"
        password = "admin123"
    } | ConvertTo-Json

    $response = Invoke-WebRequest -Uri "$baseUrl/api/auth/login" -Method POST -Body $loginBody -ContentType "application/json"
    $token = ($response.Content | ConvertFrom-Json).token
    Write-Host "Login successful!" -ForegroundColor Green
    Write-Host "Token: $($token.Substring(0, 20))..." -ForegroundColor Yellow
    
    # Set headers for authenticated requests
    $headers = @{ 
        "Authorization" = "Bearer $token"
        "Content-Type" = "application/json"
    }
} catch {
    Write-Host "Login failed: $_" -ForegroundColor Red
    Write-Host "Skipping authenticated endpoints..." -ForegroundColor Yellow
    exit
}
Write-Host ""

# Test Users with Pagination
Write-Host "=== 4. Users (Page 1, 20 per page) ===" -ForegroundColor Green
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/api/users?page=1&per_page=20" -Method GET -Headers $headers
    Write-Host "Status: $($response.StatusCode)" -ForegroundColor Green
    $data = $response.Content | ConvertFrom-Json
    Write-Host "Total Users: $($data.pagination.total)" -ForegroundColor Yellow
    Write-Host "Page: $($data.pagination.page) of $($data.pagination.pages)" -ForegroundColor Yellow
    Write-Host "Users in this page: $($data.users.Count)" -ForegroundColor Yellow
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}
Write-Host ""

# Test Products with Filter
Write-Host "=== 5. Products (Active status) ===" -ForegroundColor Green
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/api/products?status=active" -Method GET -Headers $headers
    Write-Host "Status: $($response.StatusCode)" -ForegroundColor Green
    $data = $response.Content | ConvertFrom-Json
    Write-Host "Total Products: $($data.pagination.total)" -ForegroundColor Yellow
    Write-Host "Active Products in this page: $($data.products.Count)" -ForegroundColor Yellow
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}
Write-Host ""

# Test Reports with Filter
Write-Host "=== 6. Reports (Pending status) ===" -ForegroundColor Green
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/api/reports?status=pending" -Method GET -Headers $headers
    Write-Host "Status: $($response.StatusCode)" -ForegroundColor Green
    $data = $response.Content | ConvertFrom-Json
    Write-Host "Total Reports: $($data.pagination.total)" -ForegroundColor Yellow
    Write-Host "Pending Reports in this page: $($data.reports.Count)" -ForegroundColor Yellow
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}
Write-Host ""

# Test Search
Write-Host "=== 7. Products Search (keyword: 'test') ===" -ForegroundColor Green
try {
    $response = Invoke-WebRequest -Uri "$baseUrl/api/products?search=test" -Method GET -Headers $headers
    Write-Host "Status: $($response.StatusCode)" -ForegroundColor Green
    $data = $response.Content | ConvertFrom-Json
    Write-Host "Search Results: $($data.pagination.total) products found" -ForegroundColor Yellow
} catch {
    Write-Host "Error: $_" -ForegroundColor Red
}
Write-Host ""

Write-Host "========================================"
Write-Host "   TEST COMPLETED"
Write-Host "========================================"

