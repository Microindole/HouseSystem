document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('register-form');
    if (!form) return;

    const usernameInput = document.getElementById('username');
    const passwordInput = document.getElementById('password');
    const confirmPasswordInput = document.getElementById('confirm_password');
    const emailInput = document.getElementById('email');
    const phoneInput = document.getElementById('phone');
    const provinceSelect = document.getElementById('province');
    const citySelect = document.getElementById('city');
    const districtSelect = document.getElementById('district');
    const addressHiddenInput = document.getElementById('address'); // Hidden input for full address
    const userTypeSelect = document.getElementById('user_type');
    const sendEmailCodeBtn = document.getElementById('send-email-code-btn');
    let emailCodeTimer = null;
    let emailCodeCountdown = 60;

    // Function to display error messages under the input field
    function showError(inputElement, message) {
        const formGroup = inputElement.closest('.form-group');
        if (!formGroup) return;

        let errorElement = formGroup.querySelector('.error-text');
        if (!errorElement) {
            errorElement = document.createElement('p');
            errorElement.className = 'error-text'; // Use a class for styling
            formGroup.appendChild(errorElement);
        }
        errorElement.textContent = message;
        errorElement.style.display = message ? 'block' : 'none';
        inputElement.classList.toggle('input-error', !!message); // Add class to input for visual feedback
    }

    // Function to validate a single field
    function validateField(inputElement, validationFn, errorMessage) {
        if (!validationFn()) {
            showError(inputElement, errorMessage);
            return false;
        }
        showError(inputElement, ''); // Clear error
        return true;
    }

    // --- Individual Field Validation Functions ---
    function validateUsername() {
        const username = usernameInput.value.trim();
        if (username === '') return '用户名不能为空';
        if (username.length < 3 || username.length > 20) return '用户名长度必须在3到20个字符之间';
        if (!/^[a-zA-Z0-9_]+$/.test(username)) return '用户名只能包含字母、数字和下划线';
        return ''; // No error
    }

    function validatePassword() {
        const password = passwordInput.value;
        if (password === '') return '密码不能为空';
        if (password.length < 6 || password.length > 20) return '密码长度必须在6到20个字符之间';
        return '';
    }

    function validateConfirmPassword() {
        const password = passwordInput.value;
        const confirmPassword = confirmPasswordInput.value;
        if (confirmPassword === '') return '请再次输入密码';
        if (password !== confirmPassword) return '两次输入的密码不一致';
        return '';
    }

    function validateEmail() {
        const email = emailInput.value.trim();
        if (email === '') return '邮箱不能为空';
        if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) return '请输入有效的邮箱地址';
        return '';
    }

    function validatePhone() {
        const phone = phoneInput.value.trim();
        if (phone === '') return '联系方式不能为空';
        if (!/^\d{11}$/.test(phone)) return '请输入11位有效手机号';
        return '';
    }

    function validateAddress() {
        if (provinceSelect.value === '' || citySelect.value === '' || districtSelect.value === '') {
            return '请选择完整的省市区地址';
        }
        if (provinceSelect.value && citySelect.value && districtSelect.value) {
            addressHiddenInput.value = provinceSelect.value + citySelect.value + districtSelect.value;
        } else {
            addressHiddenInput.value = '';
        }
        if (addressHiddenInput.value === '') return '请选择完整的省市区地址';
        return '';
    }

    function validateUserType() {
        if (userTypeSelect.value === '') return '请选择用户角色';
        return '';
    }

    if (usernameInput) usernameInput.addEventListener('blur', () => showError(usernameInput, validateUsername()));
    if (passwordInput) passwordInput.addEventListener('blur', () => showError(passwordInput, validatePassword()));
    if (confirmPasswordInput) {
        confirmPasswordInput.addEventListener('blur', () => showError(confirmPasswordInput, validateConfirmPassword()));
        passwordInput.addEventListener('input', () => {
            if (confirmPasswordInput.value) showError(confirmPasswordInput, validateConfirmPassword());
        });
    }
    if (emailInput) emailInput.addEventListener('blur', () => showError(emailInput, validateEmail()));
    if (phoneInput) phoneInput.addEventListener('blur', () => showError(phoneInput, validatePhone()));
    if (districtSelect) districtSelect.addEventListener('change', () => {
        const addressError = validateAddress();
        const addressErrorElement = districtSelect.closest('.form-group').querySelector('.error-text.address-error');
        if (addressErrorElement) {
            addressErrorElement.textContent = addressError;
            addressErrorElement.style.display = addressError ? 'block' : 'none';
        }
    });
    if (userTypeSelect) userTypeSelect.addEventListener('change', () => showError(userTypeSelect, validateUserType()));

    if (sendEmailCodeBtn && emailInput) {
        sendEmailCodeBtn.addEventListener('click', function () {
            const email = emailInput.value.trim();
            if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
                // MODIFIED: Using window.showMessage
                if (window.showMessage) {
                    window.showMessage('请输入有效的邮箱地址', 'warning');
                } else {
                    alert('请输入有效的邮箱地址');
                }
                return;
            }
            sendEmailCodeBtn.disabled = true;
            sendEmailCodeBtn.textContent = '发送中...';
            fetch('/account/send_email_code', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: 'email=' + encodeURIComponent(email)
            })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        startEmailCodeCountdown();
                        // MODIFIED: Using window.showMessage (type 'success' is default, can be omitted if duration also default)
                        if (window.showMessage) {
                            window.showMessage('验证码已发送，请查收邮箱', 'success');
                        } else {
                            alert('验证码已发送，请查收邮箱');
                        }
                    } else {
                        sendEmailCodeBtn.disabled = false;
                        sendEmailCodeBtn.textContent = '发送验证码';
                        // MODIFIED: Using window.showMessage
                        if (window.showMessage) {
                            window.showMessage(data.msg || '发送失败', 'error');
                        } else {
                            alert(data.msg || '发送失败');
                        }
                    }
                })
                .catch(() => {
                    sendEmailCodeBtn.disabled = false;
                    sendEmailCodeBtn.textContent = '发送验证码';
                    // MODIFIED: Using window.showMessage
                    if (window.showMessage) {
                        window.showMessage('发送失败，请稍后重试', 'error');
                    } else {
                        alert('发送失败，请稍后重试');
                    }
                });
        });
    }

    function startEmailCodeCountdown() {
        emailCodeCountdown = 60;
        sendEmailCodeBtn.disabled = true;
        sendEmailCodeBtn.textContent = `${emailCodeCountdown}s后重发`;
        emailCodeTimer = setInterval(() => {
            emailCodeCountdown--;
            if (emailCodeCountdown <= 0) {
                clearInterval(emailCodeTimer);
                sendEmailCodeBtn.disabled = false;
                sendEmailCodeBtn.textContent = '发送验证码';
            } else {
                sendEmailCodeBtn.textContent = `${emailCodeCountdown}s后重发`;
            }
        }, 1000);
    }

    form.addEventListener('submit', function (e) {
        let isValid = true;

        if (usernameInput && validateUsername()) { showError(usernameInput, validateUsername()); isValid = false; }
        if (passwordInput && validatePassword()) { showError(passwordInput, validatePassword()); isValid = false; }
        if (confirmPasswordInput && validateConfirmPassword()) { showError(confirmPasswordInput, validateConfirmPassword()); isValid = false; }
        if (emailInput && validateEmail()) { showError(emailInput, validateEmail()); isValid = false; }
        if (phoneInput && validatePhone()) { showError(phoneInput, validatePhone()); isValid = false; }

        const addressError = validateAddress();
        if (addressError) {
            const addressErrorElement = districtSelect.closest('.form-group').querySelector('.error-text.address-error');
            if (addressErrorElement) {
                addressErrorElement.textContent = addressError;
                addressErrorElement.style.display = 'block';
            } else {
                // MODIFIED: Using window.showMessage
                if (window.showMessage) {
                    window.showMessage("地址错误: " + addressError, 'error');
                } else {
                    alert("地址错误: " + addressError);
                }
            }
            isValid = false;
        } else {
            const addressErrorElement = districtSelect.closest('.form-group').querySelector('.error-text.address-error');
            if (addressErrorElement) addressErrorElement.style.display = 'none';
        }

        if (userTypeSelect && validateUserType()) { showError(userTypeSelect, validateUserType()); isValid = false; }

        if (passwordInput) {
            const strength = getPasswordStrength(passwordInput.value);
            if (strength <= 1 && passwordInput.value !== '') {
                showError(passwordInput, (validatePassword() ? validatePassword() + ' ' : '') + '密码强度较低，请尝试更复杂的密码');
                isValid = false;
            }
        }

        if (!isValid) {
            e.preventDefault();
            const firstError = form.querySelector('.input-error, .error-text[style*="block"]');
            let errorMsg = '请修正表单中的错误。';
            if (firstError) {
                firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                if (firstError.classList.contains('error-text')) {
                    errorMsg = firstError.textContent;
                } else if (firstError.nextElementSibling && firstError.nextElementSibling.classList.contains('error-text')) {
                    errorMsg = firstError.nextElementSibling.textContent;
                } else if (firstError.id === 'password' && strengthContainer.style.display === 'block' && getPasswordStrength(passwordInput.value) <=1) {
                    const passErrorElement = passwordInput.closest('.form-group').querySelector('.error-text');
                    if (passErrorElement && passErrorElement.textContent.includes('密码强度较低')) {
                        errorMsg = passErrorElement.textContent;
                    }
                }
            }
            let generalErrorContainer = document.getElementById('general-form-error');
            if (!generalErrorContainer) {
                generalErrorContainer = document.createElement('p');
                generalErrorContainer.id = 'general-form-error';
                generalErrorContainer.className = 'error-message global-error';
                form.insertBefore(generalErrorContainer, form.firstChild);
            }
            generalErrorContainer.textContent = errorMsg;
            generalErrorContainer.style.display = 'block';
        } else {
            const generalErrorContainer = document.getElementById('general-form-error');
            if (generalErrorContainer) generalErrorContainer.style.display = 'none';
        }
    });

    const strengthContainer = document.getElementById('password-strength-container');
    const strengthBarInner = document.getElementById('password-strength-bar-inner');

    if (passwordInput && strengthContainer && strengthBarInner) {
        passwordInput.addEventListener('input', function () {
            const val = passwordInput.value;
            const strength = getPasswordStrength(val);
            let color = '';
            let percent = 0;
            let text = '';

            switch (strength) {
                case 0:
                    color = '#d9534f'; percent = val ? 20 : 0; text = '非常弱'; break;
                case 1:
                    color = '#f0ad4e'; percent = 40; text = '弱'; break;
                case 2:
                    color = '#5bc0de'; percent = 60; text = '中'; break;
                case 3:
                    color = '#5cb85c'; percent = 80; text = '强'; break;
                case 4:
                    color = '#428bca'; percent = 100; text = '非常强'; break;
                default:
                    color = '#eee'; percent = 0; text = '';
            }

            if (val) {
                strengthContainer.style.display = 'block';
                strengthBarInner.style.width = percent + '%';
                strengthBarInner.style.background = color;
                strengthBarInner.textContent = text;
                if (strength <= 1) {
                    const currentError = validatePassword();
                    showError(passwordInput, (currentError ? currentError + ' ' : '') + '密码强度较低，请尝试更复杂的密码');
                } else {
                    const passErrorElement = passwordInput.closest('.form-group').querySelector('.error-text');
                    if (passErrorElement && passErrorElement.textContent.includes('密码强度较低')) {
                        showError(passwordInput, validatePassword());
                    }
                }
            } else {
                strengthContainer.style.display = 'none';
                strengthBarInner.style.width = '0';
                strengthBarInner.textContent = '';
                showError(passwordInput, validatePassword());
            }
        });

        passwordInput.addEventListener('blur', function () {
            if (!passwordInput.value) {
                strengthContainer.style.display = 'none';
                strengthBarInner.style.width = '0';
                strengthBarInner.textContent = '';
            }
        });
    }

    function getPasswordStrength(password) {
        if (!password) return 0;

        const simplePasswords = [
            '123456', '12345678', '123456789', '1234567890', '111111', '000000',
            'abcdef', 'abcde', 'abcd', 'abc123', 'a1b2c3', 'abcdefghijklmnopqrstuvwxyz',
            'qwerty', 'qwert', 'qazwsx', 'asdfgh', 'zxcvbn', 'qweasd', 'qwe123', '1qaz2wsx',
            'password', 'letmein', 'iloveyou', 'admin', 'welcome', 'monkey', 'dragon', 'sunshine', 'princess'
        ];
        if (simplePasswords.includes(password.toLowerCase())) {
            return 0;
        }

        let types = 0;
        if (/[a-z]/.test(password)) types++;
        if (/[A-Z]/.test(password)) types++;
        if (/\d/.test(password)) types++;
        if (/[^A-Za-z0-9]/.test(password)) types++;

        if (password.length < 6) return 0;

        if (types === 1) {
            if (password.length < 10) return 0;
            return 1;
        }
        if (types === 2) {
            if (password.length < 8) return 1;
            if (password.length < 12) return 2;
            return 3;
        }
        if (types === 3) {
            if (password.length < 8) return 2;
            if (password.length < 10) return 3;
            return 4;
        }
        if (types === 4) {
            if (password.length < 8) return 3;
            return 4;
        }

        return 0;
    }
});