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

    // Simulate API call
    setTimeout(() => {
        // Simple validation
        if (email && password) {
            window.location.href = 'dashboard.html';
        } else {
            alert('Mohon isi email dan password');
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

