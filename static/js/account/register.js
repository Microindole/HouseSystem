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
        // Basic email regex, for more robust validation, consider a library or more complex regex
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
        // The hidden 'address' field is populated by select-region.js
        // We just need to check if it has a value after selections are made.
        // This assumes select-region.js correctly populates it.
        if (provinceSelect.value === '' || citySelect.value === '' || districtSelect.value === '') {
            return '请选择完整的省市区地址';
        }
        // Also update the hidden field before form submission if not already handled by select-region.js
        if (provinceSelect.value && citySelect.value && districtSelect.value) {
            addressHiddenInput.value = provinceSelect.value + citySelect.value + districtSelect.value;
        } else {
            addressHiddenInput.value = ''; // Clear if not fully selected
        }
        if (addressHiddenInput.value === '') return '请选择完整的省市区地址';
        return '';
    }

    function validateUserType() {
        if (userTypeSelect.value === '') return '请选择用户角色';
        return '';
    }

    // --- Event Listeners for Real-time Feedback (Optional but good UX) ---
    // Add 'blur' or 'input' event listeners to each field to validate as user types or leaves field
    if (usernameInput) usernameInput.addEventListener('blur', () => showError(usernameInput, validateUsername()));
    if (passwordInput) passwordInput.addEventListener('blur', () => showError(passwordInput, validatePassword()));
    if (confirmPasswordInput) {
        confirmPasswordInput.addEventListener('blur', () => showError(confirmPasswordInput, validateConfirmPassword()));
        // Also re-validate confirm_password if password changes
        passwordInput.addEventListener('input', () => {
            if (confirmPasswordInput.value) showError(confirmPasswordInput, validateConfirmPassword());
        });
    }
    if (emailInput) emailInput.addEventListener('blur', () => showError(emailInput, validateEmail()));
    if (phoneInput) phoneInput.addEventListener('blur', () => showError(phoneInput, validatePhone()));
    // For address, validation might be better on submit or when district changes
    if (districtSelect) districtSelect.addEventListener('change', () => {
        // Trigger address validation or clear error if now valid
        const addressError = validateAddress();
        // Show error on a common element for address or near the district select
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
                alert('请输入有效的邮箱地址');
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
                    alert('验证码已发送，请查收邮箱');
                } else {
                    sendEmailCodeBtn.disabled = false;
                    sendEmailCodeBtn.textContent = '发送验证码';
                    alert(data.msg || '发送失败');
                }
            })
            .catch(() => {
                sendEmailCodeBtn.disabled = false;
                sendEmailCodeBtn.textContent = '发送验证码';
                alert('发送失败，请稍后重试');
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

    // --- Form Submission Handler ---
    form.addEventListener('submit', function (e) {
        let isValid = true;

        // Perform all validations
        if (usernameInput && validateUsername()) { showError(usernameInput, validateUsername()); isValid = false; }
        if (passwordInput && validatePassword()) { showError(passwordInput, validatePassword()); isValid = false; }
        if (confirmPasswordInput && validateConfirmPassword()) { showError(confirmPasswordInput, validateConfirmPassword()); isValid = false; }
        if (emailInput && validateEmail()) { showError(emailInput, validateEmail()); isValid = false; }
        if (phoneInput && validatePhone()) { showError(phoneInput, validatePhone()); isValid = false; }
        
        const addressError = validateAddress();
        if (addressError) {
            // Show address error (e.g., below the district dropdown)
            const addressErrorElement = districtSelect.closest('.form-group').querySelector('.error-text.address-error');
             if (addressErrorElement) {
                addressErrorElement.textContent = addressError;
                addressErrorElement.style.display = 'block';
            } else { // Fallback if specific error element not found
                alert("地址错误: " + addressError); // Simple alert as fallback
            }
            isValid = false;
        } else {
            const addressErrorElement = districtSelect.closest('.form-group').querySelector('.error-text.address-error');
            if (addressErrorElement) addressErrorElement.style.display = 'none';
        }

        if (userTypeSelect && validateUserType()) { showError(userTypeSelect, validateUserType()); isValid = false; }

        // 密码强度校验（必须在validatePassword之后）
        if (passwordInput) {
            const strength = getPasswordStrength(passwordInput.value);
            if (strength <= 1) {
                showError(passwordInput, '密码强度较低，请尝试更复杂的密码');
                isValid = false;
            }
        }

        if (!isValid) {
            e.preventDefault(); // 阻止表单提交
            // 找到第一个显示的错误文本
            const firstError = form.querySelector('.input-error, .error-text[style*="block"]');
            let errorMsg = '请修正表单中的错误。';
            if (firstError) {
                firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
                // 获取具体错误内容
                if (firstError.classList.contains('error-text')) {
                    errorMsg = firstError.textContent;
                } else if (firstError.nextElementSibling && firstError.nextElementSibling.classList.contains('error-text')) {
                    errorMsg = firstError.nextElementSibling.textContent;
                }
            }
            // Display a general error message if needed
            let generalErrorContainer = document.getElementById('general-form-error');
            if (!generalErrorContainer) {
                generalErrorContainer = document.createElement('p');
                generalErrorContainer.id = 'general-form-error';
                generalErrorContainer.className = 'error-message global-error'; // For styling
                form.insertBefore(generalErrorContainer, form.firstChild);
            }
            generalErrorContainer.textContent = errorMsg;
            generalErrorContainer.style.display = 'block';
        } else {
             // Clear general error if form is valid before submission
            const generalErrorContainer = document.getElementById('general-form-error');
            if (generalErrorContainer) generalErrorContainer.style.display = 'none';
            // If all client-side validations pass, the form will submit.
            // Server-side validation will still run.
        }
    });

    const strengthContainer = document.getElementById('password-strength-container');
    const strengthBar = document.getElementById('password-strength-bar');
    const strengthBarInner = document.getElementById('password-strength-bar-inner');

    passwordInput.addEventListener('input', function () {
        const val = passwordInput.value;
        const strength = getPasswordStrength(val);
        let color = '';
        let percent = 0;
        let text = '';

        switch (strength) {
            case 0:
                color = '#d9534f'; percent = 20; text = '非常弱'; break;
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
        } else {
            strengthContainer.style.display = 'none';
            strengthBarInner.style.width = '0';
            strengthBarInner.textContent = '';
        }
    });

    // 失去焦点时隐藏
    passwordInput.addEventListener('blur', function () {
        if (!passwordInput.value) {
            strengthContainer.style.display = 'none';
            strengthBarInner.style.width = '0';
            strengthBarInner.textContent = '';
        }
    });

    // 更科学的密码强度检测函数
    function getPasswordStrength(password) {
        if (!password) return 0;

        // 常见简单密码列表（可根据需要扩展）
        const simplePasswords = [
            // 数字顺序
            '123456', '12345678', '123456789', '1234567890', '111111', '000000',
            // 字母顺序
            'abcdef', 'abcde', 'abcd', 'abc123', 'a1b2c3', 'abcdefghijklmnopqrstuvwxyz',
            // 键盘顺序
            'qwerty', 'qwert', 'qazwsx', 'asdfgh', 'zxcvbn', 'qweasd', 'qwe123', '1qaz2wsx',
            // 常见弱密码
            'password', 'letmein', 'iloveyou', 'admin', 'welcome', 'monkey', 'dragon', 'sunshine', 'princess'
        ];
        if (simplePasswords.includes(password.toLowerCase())) {
            return 0; // 非常弱
        }

        let types = 0;
        if (/[a-z]/.test(password)) types++;
        if (/[A-Z]/.test(password)) types++;
        if (/\d/.test(password)) types++;
        if (/[^A-Za-z0-9]/.test(password)) types++;

        // 只一种类型
        if (types === 1) return 0; // 非常弱
        // 两种类型
        if (types === 2) {
            if (password.length < 10) return 1; // 弱
            return 2; // 中
        }
        // 三种类型
        if (types === 3) {
            if (password.length < 10) return 2; // 中
            return 3; // 强
        }
        // 四种类型
        if (types === 4) {
            if (password.length < 12) return 3; // 强
            return 4; // 非常强
        }
        // 兜底
        return 1;
    }
});
