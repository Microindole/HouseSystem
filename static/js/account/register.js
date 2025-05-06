document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('register-form').addEventListener('submit', function (e) {
        const password = document.getElementById('password').value;
        const confirmPassword = document.getElementById('confirm_password').value;
        const errorElement = document.getElementById('password-error');

        if (password !== confirmPassword) {
            e.preventDefault(); // 阻止表单提交
            errorElement.style.display = 'block'; // 显示错误信息
        } else {
            errorElement.style.display = 'none'; // 隐藏错误信息
        }
    });
});
