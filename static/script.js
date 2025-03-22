// login.html
function validateForm(event) {
    event.preventDefault();
    const recaptcha = document.getElementById('g-recaptcha-response');
    const recaptchaError = document.getElementById('recaptcha-error');

    if (recaptcha && recaptcha.value === '') {
        recaptchaError.style.display = 'block';
    } else {
        recaptchaError.style.display = 'none';
        event.target.submit();
    }
}
