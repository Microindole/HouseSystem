// 倒计时相关变量
let fpCodeTimer = null;
let fpCodeCountdown = 60;

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
            fpCodeCountdown = 60; // Reset countdown
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
    // showFpError(''); // No longer needed
};

// 2. 获取验证码
document.getElementById('fp-send-code-btn').onclick = function() {
    const username = document.getElementById('fp-username').value.trim();
    const email = document.getElementById('fp-email').value.trim();
    if (!username || !email) {
        if (window.showMessage) {
            window.showMessage('请输入用户名和邮箱', 'warning');
        } else {
            alert('请输入用户名和邮箱');
        }
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
                // showFpError(''); // No longer needed
                if (window.showMessage) {
                    window.showMessage(data.msg || '验证码已发送，请查收！', 'success');
                } else {
                    alert(data.msg || '验证码已发送，请查收！');
                }
                startFpCodeCountdown();
            } else {
                if (window.showMessage) {
                    window.showMessage(data.msg || '发送失败', 'error');
                } else {
                    alert(data.msg || '发送失败');
                }
            }
        })
        .catch(() => {
            if (window.showMessage) {
                window.showMessage('网络错误，请稍后重试', 'error');
            } else {
                alert('网络错误，请稍后重试');
            }
        });
};

// 3. 下一步，校验验证码
document.getElementById('fp-next-btn').onclick = function() {
    const username = document.getElementById('fp-username').value.trim();
    const email = document.getElementById('fp-email').value.trim();
    const code = document.getElementById('fp-code').value.trim();
    if (!username || !email || !code) {
        if (window.showMessage) {
            window.showMessage('请填写完整信息', 'warning');
        } else {
            alert('请填写完整信息');
        }
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
                // showFpError(''); // No longer needed
                document.getElementById('forget-password-panel').style.display = 'none';
                document.getElementById('reset-password-panel').style.display = '';
            } else {
                if (window.showMessage) {
                    window.showMessage(data.msg || '验证码校验失败', 'error');
                } else {
                    alert(data.msg || '验证码校验失败');
                }
            }
        })
        .catch(() => {
            if (window.showMessage) {
                window.showMessage('网络错误，请稍后重试', 'error');
            } else {
                alert('网络错误，请稍后重试');
            }
        });
};

// 4. 提交新密码
document.getElementById('rp-submit-btn').onclick = function() { // Removed async
    const username = document.getElementById('fp-username').value.trim();
    const email = document.getElementById('fp-email').value.trim();
    const code = document.getElementById('fp-code').value.trim();
    const password = document.getElementById('rp-password').value.trim();
    const confirm_password = document.getElementById('rp-confirm-password').value.trim();

    if (!password || password.length < 6) {
        if (window.showMessage) {
            window.showMessage('密码至少6位', 'warning');
        } else {
            alert('密码至少6位');
        }
        return;
    }
    if (password !== confirm_password) {
        if (window.showMessage) {
            window.showMessage('两次密码不一致', 'warning');
        } else {
            alert('两次密码不一致');
        }
        return;
    }
    fetch('/account/reset_password', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({username, email, code, password})
    })
        .then(res => res.json())
        .then(data => {
            if (data.success) {
                if (window.showMessage) {
                    window.showMessage(data.msg || '密码重置成功！', 'success');
                } else {
                    alert(data.msg || '密码重置成功！');
                }
                // Add a slight delay before reload to allow user to see the message
                setTimeout(() => {
                    location.reload();
                }, 1500);
            } else {
                if (window.showMessage) {
                    window.showMessage(data.msg || '密码重置失败。', 'error');
                } else {
                    alert(data.msg || '密码重置失败。');
                }
            }
        })
        .catch(() => {
            if (window.showMessage) {
                window.showMessage('网络错误，请稍后重试', 'error');
            } else {
                alert('网络错误，请稍后重试');
            }
        });
};

// 返回登录按钮事件
    document.getElementById('fp-back-login-btn').onclick = function() {
    document.getElementById('login-main-panel').style.display = '';
    document.getElementById('forget-password-panel').style.display = 'none';
    document.getElementById('reset-password-panel').style.display = 'none';
    // showFpError(''); // No longer needed
};