/**
 * Handle Login Form Submission
 * @param {Event} event 
 */
function handleLogin(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    const btn = event.target.querySelector('button');
    const originalContent = btn.innerHTML;

    // Simulate loading
    btn.disabled = true;
    btn.innerHTML = '<span class="material-icons" style="animation: spin 1s linear infinite;">refresh</span> Memproses...';

    // Add spin animation to style if not exists
    if (!document.getElementById('spin-style')) {
        const style = document.createElement('style');
        style.id = 'spin-style';
        style.innerHTML = '@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }';
        document.head.appendChild(style);
    }

    // Role Based Logic
    const users = {
        // Akun Baru (Poso)
        'admin.smpn1poso@edumanesia.id': { password: 'AdminSmpPos1', redirect: 'dashboard.html' },
        'kepsek.smpn1poso@edumanesia.id': { password: 'KepsekSmpPos1', redirect: 'kepsek_dashboard.html' },
        'bupati@posokab.edumanesia.id': { password: 'PosoMaju2026!', redirect: 'bupati_dashboard.html' },
        
        // Akun Lama (Default/Banggai Laut)
        'admin@sekolah.id': { password: 'admin123', redirect: 'dashboard.html' },
        'kepsek@sekolah.id': { password: 'kepsek123', redirect: 'kepsek_dashboard.html' },
        'bupati@daerah.go.id': { password: 'bupati123', redirect: 'bupati_dashboard.html' },
        'gubernur@provinsi.go.id': { password: 'gubernur123', redirect: 'gubernur_dashboard.html' }
    };

    // Simulate API call
    setTimeout(() => {
        if (users[email] && users[email].password === password) {
            window.location.href = users[email].redirect;
        } else {
            alert('Email atau Password salah!');
            btn.disabled = false;
            btn.innerHTML = originalContent;
        }
    }, 1500);
}

/**
 * Handle Save School Profile
 * @param {Event} event
 */
function handleSaveProfile(event) {
    event.preventDefault();
    const btn = event.target.querySelector('button[type="submit"]');
    const originalContent = btn.innerHTML;

    // Simulate loading
    btn.disabled = true;
    btn.innerHTML = '<span class="material-icons" style="animation: spin 1s linear infinite; vertical-align: middle; margin-right: 8px;">refresh</span> Menyimpan...';

    setTimeout(() => {
        alert('Data sekolah berhasil disimpan!');
        btn.disabled = false;
        btn.innerHTML = originalContent;
    }, 1500);
}

// Password Toggle Visibility
document.addEventListener('DOMContentLoaded', () => {
    const togglePassword = document.getElementById('togglePassword');
    const passwordInput = document.getElementById('password');

    if (togglePassword && passwordInput) {
        togglePassword.addEventListener('click', function () {
            // Toggle the type attribute
            const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
            passwordInput.setAttribute('type', type);

            // Toggle the icon
            this.textContent = type === 'password' ? 'visibility' : 'visibility_off';
            
            // Add a subtle scale animation
            this.style.transform = 'translateY(-50%) scale(1.1)';
            setTimeout(() => {
                this.style.transform = 'translateY(-50%) scale(1)';
            }, 100);
        });
    }
});
