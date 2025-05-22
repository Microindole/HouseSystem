function showPhone() {
    const phoneElement = document.getElementById('landlord-phone');
    if (phoneElement && typeof landlordPhone !== 'undefined') {
        phoneElement.textContent = landlordPhone;
    }
}

// 留言时间格式化
function formatCommentTimes() {
    const timeElements = document.querySelectorAll('.comment-time');
    const now = new Date();
    timeElements.forEach(function(el) {
        const raw = el.getAttribute('data-raw');
        if (!raw) return;
        const commentDate = new Date(raw.replace(/-/g, '/'));
        const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
        const commentDay = new Date(commentDate.getFullYear(), commentDate.getMonth(), commentDate.getDate());
        const diffDays = Math.floor((today - commentDay) / (1000 * 60 * 60 * 24));
        let display = '';
        if (diffDays === 0) {
            display = '今天';
        } else if (diffDays === 1) {
            display = '昨天';
        } else if (diffDays < 7) {
            const weekMap = ['星期日','星期一','星期二','星期三','星期四','星期五','星期六'];
            display = weekMap[commentDate.getDay()];
        } else {
            display = raw.slice(0, 10);
        }
        el.textContent = display;
    });
}
document.addEventListener('DOMContentLoaded', formatCommentTimes);

document.addEventListener('DOMContentLoaded', function() {
    // --- 回复功能 ---
    // 这部分回复逻辑如果与 house_detail.html 中的 replyToComment 函数功能重叠或冲突，
    // 也应该考虑统一管理，但主要问题是下面的提交评论功能。
    var textarea = document.querySelector('.comment-input');
    // console.log("页面加载完成，获取 textarea:", textarea); 

    document.querySelectorAll('.comment').forEach(function(commentEl) {
        var replyBtn = commentEl.querySelector('.reply-btn'); 
        if (replyBtn) { 
            commentEl.addEventListener('mouseenter', function() {
                replyBtn.style.display = 'inline-block';
            });
            commentEl.addEventListener('mouseleave', function() {
                replyBtn.style.display = 'none';
            });

            // 点击回复
            replyBtn.addEventListener('click', function() {
                var username = commentEl.getAttribute('data-username');
                var desc = commentEl.getAttribute('data-desc');
                var commentId = commentEl.getAttribute('data-comment-id'); 
                var atInfo = document.querySelector('.at-info');
                var atText = document.getElementById('at-text');

                // console.log("[回复按钮点击] 获取到的 commentId:", commentId); 

                atInfo.style.display = 'flex';
                atText.textContent = '@' + username + ': ' + desc;
                textarea.focus();
                textarea.dataset.at = commentId; 
                // console.log("[回复按钮点击后] 设置 textarea.dataset.at 为:", textarea.dataset.at); 
                textarea.scrollIntoView({behavior: 'smooth', block: 'center'});
            });
        }
    });

    // 取消@功能
    var cancelAt = document.getElementById('cancel-at');
    if (cancelAt) {
        cancelAt.addEventListener('click', function() {
            var atInfo = document.querySelector('.at-info');
            atInfo.style.display = 'none';
            // console.log("[取消@按钮点击前] textarea.dataset.at:", textarea.dataset.at); 
            textarea.removeAttribute('data-at'); 
            // console.log("[取消@按钮点击后] textarea.dataset.at:", textarea.dataset.at); 
        });
    }
});

// ... 其他 show-date.js 中的代码，如 formatCommentTimes ...
function formatCommentTimes() {
    document.querySelectorAll('.comment-time').forEach(function(el) {
        const rawTime = el.getAttribute('data-raw');
        if (rawTime) {
            const date = new Date(rawTime);
            // 强制转换为北京时间 (不依赖浏览器时区)
            const beijingTimestamp = new Date(date.getTime() + (8 - date.getTimezoneOffset() / 60) * 3600000);

            const now = new Date();
            const diffSeconds = Math.floor((now - beijingTimestamp) / 1000);
            const diffMinutes = Math.floor(diffSeconds / 60);
            const diffHours = Math.floor(diffMinutes / 60);
            const diffDays = Math.floor(diffHours / 24);

            if (diffSeconds < 60) {
                el.textContent = '刚刚';
            } else if (diffMinutes < 60) {
                el.textContent = `${diffMinutes}分钟前`;
            } else if (diffHours < 24) {
                el.textContent = `${diffHours}小时前`;
            } else if (diffDays === 1) {
                el.textContent = '昨天';
            } else if (diffDays < 7) {
                el.textContent = `${diffDays}天前`;
            } else {
                el.textContent = beijingTimestamp.toLocaleDateString();
            }
        } else {
            el.textContent = '未知时间';
        }
    });
}
document.addEventListener('DOMContentLoaded', formatCommentTimes);