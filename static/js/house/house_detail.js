/**
 * 房源详情页面 JavaScript 模块
 */
// 全局变量（页面传入）
let houseId, landlordPhone, currentUser;
// 初始化全局变量
function initGlobalVariables(config) {
    houseId = config.houseId;
    landlordPhone = config.landlordPhone;
    currentUser = config.currentUser;
    window.houseId = houseId; // 兼容旧代码
}
// 显示电话号码
function showPhone() {
    const phoneElement = document.getElementById('landlord-phone');
    if (phoneElement && landlordPhone) {
        phoneElement.textContent = landlordPhone;
    }
}
// 维修申请相关函数
function showRepairModal() {
    document.getElementById('repairModal').style.display = 'flex';
}
function closeRepairModal() {
    document.getElementById('repairModal').style.display = 'none';
    document.getElementById('repairForm').reset();
}
// 提交维修申请
function initRepairForm() {
    const repairForm = document.getElementById('repairForm');
    if (!repairForm) return;
    repairForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const content = document.getElementById('repairContent').value.trim();

        if (!content) {
            if (window.showMessage) {
                window.showMessage('请填写维修内容描述', 'warning');
            } else {
                alert('请填写维修内容描述');
            }
            return;
        }
        fetch('/house/repair/request', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                house_id: houseId,
                content: content
            })
        }).then(response => response.json()).then(data => {
            if (data.success) {
                if (window.showMessage) {
                    window.showMessage(data.message, 'success');
                } else {
                    alert(data.message);
                }
                closeRepairModal();
            } else {
                if (window.showMessage) {
                    window.showMessage('提交失败：' + data.message, 'error');
                } else {
                    alert('提交失败：' + data.message);
                }
            }
        }).catch(error => {
            console.error('Error:', error);
            if (window.showMessage) {
                window.showMessage('提交失败，请稍后重试', 'error');
            } else {
                alert('提交失败，请稍后重试');
            }
        });
    });
}
// 预约看房相关函数
function showAppointmentModal() {
    const modal = document.getElementById('appointmentModal');
    modal.style.display = 'flex';
    // 设置最小时间为当前时间
    const now = new Date();
    now.setMinutes(now.getMinutes() - now.getTimezoneOffset());
    const timeInput = document.getElementById('appointmentTime');
    if (timeInput) {
        timeInput.min = now.toISOString().slice(0, 16);
    }
}
function closeAppointmentModal() {
    document.getElementById('appointmentModal').style.display = 'none';
    document.getElementById('appointmentForm').reset();
}
// 初始化预约表单
function initAppointmentForm() {
    const appointmentForm = document.getElementById('appointmentForm');
    if (!appointmentForm) return;
    appointmentForm.addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(this);
        const data = Object.fromEntries(formData);
        fetch('/house/appointment', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        }).then(response => response.json()).then(data => {
            if (data.code === 200) {
                if (window.showMessage) {
                    window.showMessage(data.msg, 'success');
                } else {
                    alert(data.msg);
                }
                closeAppointmentModal();
                setTimeout(() => {
                    location.reload();
                }, 1500);
            } else {
                if (window.showMessage) {
                    window.showMessage(data.msg || '预约失败', 'error');
                } else {
                    alert(data.msg || '预约失败');
                }
            }
        }).catch(error => {
            console.error('Error:', error);
            if (window.showMessage) {
                window.showMessage('提交失败，请稍后重试', 'error');
            } else {
                alert('提交失败，请稍后重试');
            }
        });
    });
}
// 评论回复功能
function replyToComment(commentId, username) {
    const atCommentIdInput = document.getElementById('at-comment-id');
    const atText = document.getElementById('at-text');
    const atInfo = document.querySelector('.at-info');
    const commentInput = document.querySelector('.comment-input');

    if (atCommentIdInput) atCommentIdInput.value = commentId;
    if (atText) atText.textContent = `回复 @${username}：`;
    if (atInfo) atInfo.style.display = 'block';
    if (commentInput) commentInput.focus();
}

// 取消回复
function initCancelReply() {
    const cancelAt = document.getElementById('cancel-at');
    if (!cancelAt) return;
    cancelAt.addEventListener('click', function() {
        const atCommentIdInput = document.getElementById('at-comment-id');
        const atText = document.getElementById('at-text');
        const atInfo = document.querySelector('.at-info');

        if (atCommentIdInput) atCommentIdInput.value = '';
        if (atText) atText.textContent = '';
        if (atInfo) atInfo.style.display = 'none';
    });
}
// 初始化评论提交
function initCommentSubmit() {
    const submitButton = document.getElementById('submit-comment-btn');
    if (!submitButton) return;
    let isSubmitting = false;

    submitButton.addEventListener('click', function() {
        if (isSubmitting) return;

        const commentInput = document.querySelector('.comment-input');
        const atCommentIdInput = document.getElementById('at-comment-id');
        const content = commentInput.value.trim();
        const atCommentId = atCommentIdInput.value;

        if (!content) {
            if (window.showMessage) {
                window.showMessage('请输入评论内容', 'warning');
            } else {
                alert('请输入评论内容');
            }
            return;
        }
        isSubmitting = true;
        submitButton.disabled = true;
        submitButton.textContent = '提交中...';
        const formData = new FormData();
        formData.append('house_id', houseId);
        formData.append('comment', content);
        if (atCommentId) {
            formData.append('at', atCommentId);
        }
        fetch('/house/add_comment_form', {
            method: 'POST',
            body: formData
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // 清空输入框和回复状态
                    commentInput.value = '';
                    atCommentIdInput.value = '';
                    document.getElementById('at-text').textContent = '';
                    document.querySelector('.at-info').style.display = 'none';

                    // 动态添加新评论到页面顶部
                    addCommentToPage(data.comment);

                    // 更新评论总数
                    updateCommentCount(1);

                    if (window.showMessage) {
                        window.showMessage('评论发表成功！', 'success');
                    } else {
                        alert('评论发表成功！');
                    }
                } else {
                    if (window.showMessage) {
                        window.showMessage('评论提交失败：' + (data.message || '未知错误'), 'error');
                    } else {
                        alert('评论提交失败：' + (data.message || '未知错误'));
                    }
                }
            })
            .catch(error => {
                console.error('Error submitting comment:', error);
                if (window.showMessage) {
                    window.showMessage('评论提交失败，网络错误或服务器无响应，请稍后重试', 'error');
                } else {
                    alert('评论提交失败，网络错误或服务器无响应，请稍后重试');
                }
            })
            .finally(() => {
                isSubmitting = false;
                submitButton.disabled = false;
                submitButton.textContent = '提交评论';
            });
    });
}
// 动态添加评论到页面
function addCommentToPage(commentData) {
    const commentsList = document.querySelector('.comments-list');
    if (!commentsList) return;

    const commentHtml = `
        <div class="comment" data-comment-id="${commentData.comment_id}" data-username="${commentData.username}" data-desc="${commentData.desc}">
            <div class="comment-header">
                <span>
                    <strong class="comment-username">${commentData.username}</strong>
                    <span class="comment-type">(${commentData.type === 2 ? '房东' : '租客'})</span>
                </span>
                <span class="comment-time" data-raw="${commentData.time}">刚刚</span>
                ${currentUser.isLoggedIn ? `<button class="reply-btn" onclick="replyToComment(${commentData.comment_id}, '${commentData.username}')">回复</button>` : ''}
            </div>
            <div class="comment-body">
                <p>${commentData.desc}</p>
                ${commentData.at_username && commentData.at_desc ? `<p class="comment-reply">@${commentData.at_username}: ${commentData.at_desc}</p>` : ''}
            </div>
        </div>
    `;
    commentsList.insertAdjacentHTML('afterbegin', commentHtml);
    // 添加回复按钮悬停效果
    const newComment = commentsList.firstElementChild;
    initCommentHoverEffect(newComment);
}

// 初始化评论悬停效果
function initCommentHoverEffects() {
    document.querySelectorAll('.comment').forEach(initCommentHoverEffect);
}

function initCommentHoverEffect(commentEl) {
    const replyBtn = commentEl.querySelector('.reply-btn');
    if (!replyBtn) return;

    commentEl.addEventListener('mouseenter', function() {
        replyBtn.style.display = 'inline-block';
    });
    commentEl.addEventListener('mouseleave', function() {
        replyBtn.style.display = 'none';
    });
}
// 更新评论总数
function updateCommentCount(increment) {
    const commentSection = document.querySelector('.comments-section h2');
    if (!commentSection) return;
    const currentText = commentSection.textContent;
    const match = currentText.match(/\((\d+)条\)/);
    if (match) {
        const currentCount = parseInt(match[1]);
        const newCount = currentCount + increment;
        commentSection.textContent = currentText.replace(/\(\d+条\)/, `(${newCount}条)`);
    }
}
// 删除房源（房东专用）
async function deleteHouse(houseId) { // MODIFIED: Added async
    let confirmed = false;
    if (window.showConfirm) {
        confirmed = await window.showConfirm('确定要删除这套房源吗？此操作不可恢复。', {
            title: '删除确认',
            type: 'warning',
            confirmText: '确定删除',
            cancelText: '取消'
        });
    } else { // Fallback to native confirm
        confirmed = confirm('确定要删除这套房源吗？此操作不可恢复。');
    }
    if (!confirmed) return;
    fetch(`/house/delete/${houseId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                if (window.showMessage) {
                    window.showMessage(data.message, 'success');
                } else {
                    alert(data.message);
                }
                setTimeout(() => {
                    window.location.href = '/account/landlord/home'; // Redirect to landlord's home page
                }, 1500);
            } else {
                if (window.showMessage) {
                    window.showMessage('删除失败：' + data.message, 'error');
                } else {
                    alert('删除失败：' + data.message);
                }
            }
        })
        .catch(error => {
            console.error('Error:', error);
            if (window.showMessage) {
                window.showMessage('删除失败，请稍后重试', 'error');
            } else {
                alert('删除失败，请稍后重试');
            }
        });
}
// 时间格式化（从 show-date.js 中整合）
function formatCommentTimes() {
    document.querySelectorAll('.comment-time').forEach(function(el) {
        const rawTime = el.getAttribute('data-raw');
        if (!rawTime) return;
        const date = new Date(rawTime.replace(/-/g, '/')); // Ensure cross-browser date parsing
        const now = new Date();
        const diffSeconds = Math.floor((now - date) / 1000);
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
            el.textContent = date.toLocaleDateString();
        }
    });
}
// 初始化地图
function initMap(houseData) {
    const mapContainer = document.getElementById('map-container');
    if (!mapContainer || typeof BMapGL === 'undefined') return;
    
    const map = new BMapGL.Map('map-container', {
        enableMapClick: true,
        displayOptions: {
            building: true,
            poi: true,
            indoor: false
        }
    });
    
    map.setMapStyleV2({
        styleId: '01e6259d6df0835e035b80a7ee838682'
    });
    
    map.addControl(new BMapGL.ScaleControl());
    map.addControl(new BMapGL.ZoomControl());
    map.enableScrollWheelZoom(true);

    const fullAddress = `${houseData.region} ${houseData.addr}`;
    const myGeo = new BMapGL.Geocoder();

    myGeo.getPoint(fullAddress, function(point) {
        if (point) {
            map.centerAndZoom(point, 17);
            
            const marker = new BMapGL.Marker(point);
            map.addOverlay(marker);
            
            // 初始化地图详情组件
            if (typeof initMapDetailComponent === 'function') {
                initMapDetailComponent(map, houseData, marker);
            }
            
        } else {
            handleMapError(map, houseData.region);
        }
    }, "全国");
}

// 修改 handleMapError 函数，同样移除信息窗口
function handleMapError(map, region) {
    const myGeo = new BMapGL.Geocoder();
    myGeo.getPoint(region, function(regionPoint) {
        if (regionPoint) {
            map.centerAndZoom(regionPoint, 14);
            
            // 只添加标记点
            const regionMarker = new BMapGL.Marker(regionPoint);
            map.addOverlay(regionMarker);

            // 显示错误提示（保留这个提示）
            document.getElementById('map-container').insertAdjacentHTML(
                'beforeend',
                '<div style="position:absolute;bottom:10px;left:10px;right:10px;background:rgba(255,255,255,0.9);padding:10px;border-radius:4px;text-align:center;color:#f56c6c;font-weight:bold;box-shadow:0 2px 6px rgba(0,0,0,0.2);">无法精确定位房源地址，已显示所在地区</div>'
            );
        } else {
            document.getElementById('map-container').innerHTML = '<div style="text-align:center;padding:30px;background:#f8f9fa;border-radius:8px;"><p style="color:#f56c6c;font-weight:bold;">无法显示地图，请检查房源地址信息</p></div>';
        }
    }, "全国");
}
// 主初始化函数
function initHouseDetail(config) {
    initGlobalVariables(config);
    // 初始化各个模块
    initRepairForm();
    initAppointmentForm();
    initCancelReply();
    initCommentSubmit();
    initCommentHoverEffects();
    // 格式化时间
    formatCommentTimes();
    // 初始化地图（需要等待页面加载完成）
    if (config.houseData) {
        initMap(config.houseData);
    }
}
// 暴露全局函数（供HTML调用）
window.showPhone = showPhone;
window.showRepairModal = showRepairModal;
window.closeRepairModal = closeRepairModal;
window.showAppointmentModal = showAppointmentModal;
window.closeAppointmentModal = closeAppointmentModal;
window.replyToComment = replyToComment;
window.deleteHouse = deleteHouse;
window.initHouseDetail = initHouseDetail;