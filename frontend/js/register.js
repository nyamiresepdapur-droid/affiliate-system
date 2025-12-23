// Register Page JavaScript
// Load API URL from config or use default
// Production: Railway backend
// Development: Localhost
const API_URL = (typeof window !== 'undefined' && window.API_URL) || 
                (window.location.hostname !== 'localhost' && window.location.hostname !== '127.0.0.1'
                    ? 'https://affiliate-system-production.up.railway.app/api'
                    : 'http://localhost:5000/api');

let registrationData = {
    fullName: '',
    whatsapp: '',
    email: '',
    membership: '',
    price: 0,
    paymentMethod: '',
    paymentDetail: ''
};

let currentStep = 1;
const totalSteps = 3;

// Initialize
document.addEventListener('DOMContentLoaded', function() {
    // Check if coming from landing page with selected plan
    const urlParams = new URLSearchParams(window.location.search);
    const plan = urlParams.get('plan');
    if (plan === 'basic' || plan === 'vip') {
        registrationData.membership = plan;
        registrationData.price = plan === 'basic' ? 97000 : 299000;
        goToStep(2);
    }

    setupEventListeners();
});

function setupEventListeners() {
    // Personal Info Form
    document.getElementById('personalInfoForm').addEventListener('submit', function(e) {
        e.preventDefault();
        if (validateStep1()) {
            goToStep(2);
        }
    });

    // Membership Selection
    document.querySelectorAll('.membership-card').forEach(card => {
        card.addEventListener('click', function() {
            document.querySelectorAll('.membership-card').forEach(c => c.classList.remove('selected'));
            this.classList.add('selected');
            
            registrationData.membership = this.dataset.membership;
            registrationData.price = parseInt(this.dataset.price);
            
            document.getElementById('btnNextStep2').disabled = false;
        });
    });

    // Payment Method
    document.getElementById('paymentMethod').addEventListener('change', function() {
        const container = document.getElementById('paymentDetailContainer');
        if (this.value) {
            container.style.display = 'block';
            registrationData.paymentMethod = this.value;
        } else {
            container.style.display = 'none';
        }
    });

    // Payment Proof Preview
    document.getElementById('paymentProof').addEventListener('change', function(e) {
        const file = e.target.files[0];
        if (file) {
            if (file.size > 5 * 1024 * 1024) {
                showAlert('File terlalu besar. Maksimal 5MB.', 'danger');
                this.value = '';
                return;
            }
            const reader = new FileReader();
            reader.onload = function(e) {
                const preview = document.getElementById('paymentProofPreview');
                preview.src = e.target.result;
                preview.classList.add('show');
            };
            reader.readAsDataURL(file);
        }
    });

    // Payment Form Submit
    document.getElementById('paymentForm').addEventListener('submit', function(e) {
        e.preventDefault();
        submitRegistration();
    });

    // Submit button
    document.getElementById('btnSubmit').addEventListener('click', function() {
        if (validateStep3()) {
            document.getElementById('paymentForm').dispatchEvent(new Event('submit'));
        }
    });
}

function validateStep1() {
    const fullName = document.getElementById('fullName').value.trim();
    const whatsapp = document.getElementById('whatsapp').value.trim();
    const email = document.getElementById('email').value.trim();

    if (!fullName) {
        showAlert('Nama lengkap harus diisi!', 'danger');
        return false;
    }

    if (!whatsapp) {
        showAlert('Nomor WhatsApp harus diisi!', 'danger');
        return false;
    }

    if (whatsapp.length < 10) {
        showAlert('Nomor WhatsApp tidak valid!', 'danger');
        return false;
    }

    if (email && !isValidEmail(email)) {
        showAlert('Format email tidak valid!', 'danger');
        return false;
    }

    registrationData.fullName = fullName;
    registrationData.whatsapp = whatsapp;
    registrationData.email = email || '';

    return true;
}

function validateStep3() {
    const paymentMethod = document.getElementById('paymentMethod').value;
    const paymentDetail = document.getElementById('paymentDetail').value.trim();
    const paymentProof = document.getElementById('paymentProof').files[0];

    if (!paymentMethod) {
        showAlert('Pilih metode pembayaran!', 'danger');
        return false;
    }

    if (!paymentDetail) {
        showAlert('Detail pembayaran harus diisi!', 'danger');
        return false;
    }

    if (!paymentProof) {
        showAlert('Upload bukti pembayaran!', 'danger');
        return false;
    }

    registrationData.paymentMethod = paymentMethod;
    registrationData.paymentDetail = paymentDetail;

    return true;
}

function goToStep(step) {
    if (step < 1 || step > totalSteps) return;

    // Hide all sections
    document.querySelectorAll('.form-section').forEach(section => {
        section.classList.remove('active');
    });

    // Update step indicators
    for (let i = 1; i <= totalSteps; i++) {
        const indicator = document.getElementById(`step${i}-indicator`);
        if (i < step) {
            indicator.classList.remove('active');
            indicator.classList.add('completed');
        } else if (i === step) {
            indicator.classList.add('active');
            indicator.classList.remove('completed');
        } else {
            indicator.classList.remove('active', 'completed');
        }
    }

    // Show current step
    if (step === 1) {
        document.getElementById('step1').classList.add('active');
    } else if (step === 2) {
        document.getElementById('step2').classList.add('active');
        updateMembershipDisplay();
    } else if (step === 3) {
        document.getElementById('step3').classList.add('active');
        updatePaymentDisplay();
    }

    currentStep = step;
}

function updateMembershipDisplay() {
    // Membership already selected from cards
}

function updatePaymentDisplay() {
    const membershipName = registrationData.membership === 'basic' ? 'Basic Member' : 'VIP Member';
    document.getElementById('selectedMembershipDisplay').textContent = membershipName;
    document.getElementById('selectedPriceDisplay').textContent = registrationData.price.toLocaleString('id-ID');
}

async function submitRegistration() {
    const submitBtn = document.getElementById('btnSubmit');
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Mengirim...';

    try {
        // Prepare form data
        const formData = new FormData();
        formData.append('full_name', registrationData.fullName);
        formData.append('whatsapp', registrationData.whatsapp);
        formData.append('email', registrationData.email || '');
        formData.append('membership_tier', registrationData.membership);
        formData.append('membership_price', registrationData.price);
        formData.append('payment_method', registrationData.paymentMethod);
        formData.append('payment_detail', registrationData.paymentDetail);
        
        const paymentProof = document.getElementById('paymentProof').files[0];
        if (paymentProof) {
            formData.append('payment_proof', paymentProof);
        }

        // Submit to backend
        const response = await fetch(`${API_URL}/register`, {
            method: 'POST',
            body: formData,
            // Don't set Content-Type header, let browser set it with boundary for FormData
        });

        const data = await response.json();

        if (response.ok) {
            // Success
            showSuccessMessage();
        } else {
            // Error
            showAlert(data.error || 'Terjadi kesalahan saat mendaftar. Silakan coba lagi.', 'danger');
            submitBtn.disabled = false;
            submitBtn.innerHTML = 'Daftar Sekarang';
        }
    } catch (error) {
        console.error('Registration error:', error);
        showAlert('Terjadi kesalahan. Pastikan backend sedang running dan coba lagi.', 'danger');
        submitBtn.disabled = false;
        submitBtn.innerHTML = 'Daftar Sekarang';
    }
}

function showSuccessMessage() {
    // Hide all form sections
    document.querySelectorAll('.form-section').forEach(section => {
        section.classList.remove('active');
        section.style.display = 'none';
    });

    // Show success message
    document.getElementById('successMessage').style.display = 'block';
}

function showAlert(message, type = 'info') {
    const alertContainer = document.getElementById('alertContainer');
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    alertContainer.innerHTML = '';
    alertContainer.appendChild(alert);

    // Auto dismiss after 5 seconds
    setTimeout(() => {
        alert.classList.remove('show');
        setTimeout(() => alert.remove(), 150);
    }, 5000);
}

function isValidEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

