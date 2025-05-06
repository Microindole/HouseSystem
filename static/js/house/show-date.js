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
    var textarea = document.querySelector('.comment-input');
    // console.log("页面加载完成，获取 textarea:", textarea); // 新增日志

    // 悬停显示回复按钮
    document.querySelectorAll('.comment').forEach(function(commentEl) {
        var replyBtn = commentEl.querySelector('.reply-btn'); // 把 replyBtn 获取移到这里
        if (replyBtn) { // 添加判断 replyBtn 是否存在
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
                var commentId = commentEl.getAttribute('data-comment-id'); // 获取 comment_id
                var atInfo = document.querySelector('.at-info');
                var atText = document.getElementById('at-text');

                console.log("[回复按钮点击] 获取到的 commentId:", commentId); // 新增日志

                atInfo.style.display = 'flex';
                atText.textContent = '@' + username + ': ' + desc;
                textarea.focus();
                // 保存被@信息到 textarea 的 dataset
                textarea.dataset.at = commentId; // 只保存 comment_id 即可
                console.log("[回复按钮点击后] 设置 textarea.dataset.at 为:", textarea.dataset.at); // 新增日志
                // 滚动到输入框
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
            console.log("[取消@按钮点击前] textarea.dataset.at:", textarea.dataset.at); // 新增日志
            textarea.removeAttribute('data-at'); // 清除 comment_id
            console.log("[取消@按钮点击后] textarea.dataset.at:", textarea.dataset.at); // 新增日志
        });
    }

    // --- 提交评论功能 (合并后的唯一监听器) ---
    var btn = document.getElementById('submit-comment-btn');
    if (btn && textarea) {
        btn.addEventListener('click', function() {
            var comment = textarea.value.trim();
            if (!comment) {
                alert('请输入评论内容');
                textarea.focus();
                return;
            }

            console.log("[提交按钮点击] 开始处理，检查 textarea.dataset.at:", textarea.dataset.at); // 新增日志

            // 创建隐藏表单
            var form = document.createElement('form');
            form.method = 'POST';
            form.action = '/house/add_comment_form'; // 确认后端路由是这个
            form.style.display = 'none';

            // 添加评论内容
            var inputComment = document.createElement('input');
            inputComment.name = 'comment';
            inputComment.value = comment;
            form.appendChild(inputComment);

            // 添加房屋ID
            var inputHouseId = document.createElement('input');
            inputHouseId.name = 'house_id';
            inputHouseId.value = window.houseId;
            form.appendChild(inputHouseId);

            // 如果有@信息 (即 textarea.dataset.at 存在)，添加 at 字段
            if (textarea.dataset.at) {
                console.log("[提交按钮点击] 检测到 textarea.dataset.at 存在，值为:", textarea.dataset.at, "。准备添加 at input。"); // 新增日志
                var inputAt = document.createElement('input');
                inputAt.name = 'at'; // 后端接收的字段名是 at
                inputAt.value = textarea.dataset.at; // 值为 comment_id
                form.appendChild(inputAt);
            } else {
                console.log("[提交按钮点击] 未检测到 textarea.dataset.at。"); // 新增日志
            }

            // 提交表单
            console.log("[提交按钮点击] 准备提交表单。"); // 新增日志
            document.body.appendChild(form);
            form.submit();

            // 清除 @ 状态 (可选，如果希望提交后清除)
            if (cancelAt) {
                 // cancelAt.click(); // 暂时注释掉，避免干扰调试
            }
            // textarea.value = ''; // 暂时注释掉
        });
    } else {
        console.error("未找到提交按钮或文本区域！"); // 新增错误日志
    }
});