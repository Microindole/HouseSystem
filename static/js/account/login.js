// 倒计时相关变量
let fpCodeTimer = null;
let fpCodeCountdown = 60;

// 显示错误提示
function showFpError(msg) {
    let err = document.getElementById('fp-error-msg');
    if (!err) {
        err = document.createElement('div');
        err.id = 'fp-error-msg';
        err.style.color = 'red';
        err.style.margin = '8px 0';
        document.getElementById('forget-password-panel').insertBefore(err, document.getElementById('forget-password-form'));
    }
    err.textContent = msg;
    err.style.display = msg ? 'block' : 'none';
}

// 发送验证码倒计时
function startFpCodeCountdown() {
    const btn = document.getElementById('fp-send-code-btn');
    btn.disabled = true;
    btn.textContent = `${fpCodeCountdown}s后重试`;
    fpCodeTimer = setInterval(() => {
        fpCodeCountdown--;
        if (fpCodeCountdown <= 0) {
            clearInterval(fpCodeTimer);
            btn.disabled = false;
            btn.textContent = '获取验证码';
            fpCodeCountdown = 60;
        } else {
            btn.textContent = `${fpCodeCountdown}s后重试`;
        }
    }, 1000);
}

// 1. 点击“忘记密码”显示找回密码面板
document.getElementById('forget-password-link').onclick = function() {
    document.getElementById('login-main-panel').style.display = 'none';
    document.getElementById('forget-password-panel').style.display = '';
    document.getElementById('reset-password-panel').style.display = 'none';
    showFpError('');
};

// 2. 获取验证码
document.getElementById('fp-send-code-btn').onclick = function() {
    const username = document.getElementById('fp-username').value.trim();
    const email = document.getElementById('fp-email').value.trim();
    if (!username || !email) {
        showFpError('请输入用户名和邮箱');
        return;
    }
    fetch('/account/send_reset_code', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username, email})
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            showFpError('');
            startFpCodeCountdown();
        } else {
            showFpError(data.msg || '发送失败');
        }
        // alert(data.msg);
    })
    .catch(() => {
        showFpError('网络错误，请稍后重试');
    });
};

// 3. 下一步，校验验证码
document.getElementById('fp-next-btn').onclick = function() {
    const username = document.getElementById('fp-username').value.trim();
    const email = document.getElementById('fp-email').value.trim();
    const code = document.getElementById('fp-code').value.trim();
    if (!username || !email || !code) {
        showFpError('请填写完整信息');
        return;
    }
    fetch('/account/verify_reset_code', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username, email, code})
    })
    .then(res => res.json())
    .then(data => {
        if (data.success) {
            showFpError('');
            document.getElementById('forget-password-panel').style.display = 'none';
            document.getElementById('reset-password-panel').style.display = '';
        } else {
            showFpError(data.msg);
        }
    })
    .catch(() => {
        showFpError('网络错误，请稍后重试');
    });
};

// 4. 提交新密码
document.getElementById('rp-submit-btn').onclick = function() {
    const username = document.getElementById('fp-username').value.trim();
    const email = document.getElementById('fp-email').value.trim();
    const code = document.getElementById('fp-code').value.trim();
    const password = document.getElementById('rp-password').value.trim();
    const confirm = document.getElementById('rp-confirm-password').value.trim();
    if (!password || password.length < 6) {
        alert('密码至少6位');
        return;
    }
    if (password !== confirm) {
        alert('两次密码不一致');
        return;
    }
    fetch('/account/reset_password', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username, email, code, password})
    })
    .then(res => res.json())
    .then(data => {
        // alert(data.msg);
        if (data.success) {
            location.reload();
        }
    });
};

// 返回登录按钮事件
document.getElementById('fp-back-login-btn').onclick = function() {
    document.getElementById('login-main-panel').style.display = '';
    document.getElementById('forget-password-panel').style.display = 'none';
    document.getElementById('reset-password-panel').style.display = 'none';
    showFpError('');
};