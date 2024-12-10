// JavaScript to switch payment details based on selected option
const paymentOptions = document.querySelectorAll('.payment-option');
const detailsSections = document.querySelectorAll('.details-section');

paymentOptions.forEach(option => {
    option.addEventListener('click', () => {
        // Remove 'active' class from all options and sections
        paymentOptions.forEach(opt => opt.classList.remove('active'));
        detailsSections.forEach(section => section.classList.remove('active'));

        // Add 'active' class to the clicked option and the corresponding section
        option.classList.add('active');
        document.getElementById(option.getAttribute('data-target')).classList.add('active');
    });
});