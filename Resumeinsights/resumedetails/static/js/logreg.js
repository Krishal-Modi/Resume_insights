document.querySelectorAll('input').forEach(input => {
    input.addEventListener('focus', function() {
        this.classList.add('active');
    });

    input.addEventListener('blur', function() {
        if (this.value === '') {
            this.classList.remove('active');
        }
    });

    // Add a 3D effect on focus
    input.addEventListener('focus', function() {
        this.style.transform = 'translateZ(10px)';
    });

    input.addEventListener('blur', function() {
        this.style.transform = 'translateZ(0)';
    });
});
