const receiverInput = document.getElementById('receiver');
const autocompleteDiv = document.getElementById('receiver-autocomplete');
const receiverTypeDiv = document.getElementById('receiver-type');
const houseSelectDiv = document.getElementById('house-select-div');
const houseSelect = document.getElementById('house_id');
const myHouseSelectDiv = document.getElementById('my-house-select-div');

// 页面加载时判断是否显示“我的房源”
if (typeof userType !== 'undefined' && userType === 2 && myHouseSelectDiv) {
    myHouseSelectDiv.style.display = '';
}

// 自动补全功能
receiverInput.addEventListener('input', function() {
    const val = this.value.trim();

    // 动态定位和设置宽度
    const rect = receiverInput.getBoundingClientRect();
    // 对于 position: fixed 的元素，直接使用 getBoundingClientRect 的值，因为它们都是相对于视口的
    autocompleteDiv.style.left = rect.left + 'px';
    autocompleteDiv.style.top = rect.bottom + 'px'; // autocompleteDiv 的顶部紧随 receiverInput 的底部
    autocompleteDiv.style.width = rect.width + 'px'; // 确保宽度与输入框一致

    if (val.length === 0) {
        autocompleteDiv.style.display = 'none';
        autocompleteDiv.innerHTML = ''; // 清空内容
        receiverTypeDiv.textContent = '';
        houseSelectDiv.style.display = 'none';
        houseSelect.value = '';
        return;
    }

    const matches = userList.filter(u => u.username.includes(val));
    if (matches.length > 0) {
        autocompleteDiv.innerHTML = matches.map(u =>
            `<div class="autocomplete-item" data-username="${u.username}" data-type="${u.type}">${u.username} <span style="color:#888;font-size:12px;">(${u.type})</span></div>`
        ).join('');
        autocompleteDiv.style.display = 'block';
    } else {
        autocompleteDiv.innerHTML = ''; // 清空内容
        autocompleteDiv.style.display = 'none';
    }

    // 类型显示逻辑 (保持不变)
    const exact = userList.find(u => u.username === val && u.type === '房东');
    if (exact) {
        receiverTypeDiv.textContent = `用户类型：${exact.type}`;
        fetch(`/feedback/get_houses_by_landlord?landlord_name=${encodeURIComponent(val)}`)
            .then(res => res.json())
            .then(data => {
                houseSelect.innerHTML = `<option value="">不关联房源</option>`;
                data.houses.forEach(h => {
                    houseSelect.innerHTML += `<option value="${h.house_id}">${h.house_name}</option>`;
                });
                houseSelectDiv.style.display = '';
            });
    } else {
        // 如果不是房东或没有精确匹配，也可能需要隐藏房源选择
        const matchedUser = userList.find(u => u.username === val);
        if (!matchedUser || matchedUser.type !== '房东') {
             houseSelectDiv.style.display = 'none';
             houseSelect.value = '';
        }
        // 如果只是没有精确匹配到房东，但可能匹配到其他用户，receiverTypeDiv 可以不清空
        // receiverTypeDiv.textContent = ''; // 根据需求决定是否清空
    }
});

// 选择自动补全项
autocompleteDiv.addEventListener('click', function(e) {
    if (e.target.classList.contains('autocomplete-item')) {
        receiverInput.value = e.target.dataset.username;
        receiverTypeDiv.textContent = `用户类型：${e.target.dataset.type}`;
        autocompleteDiv.style.display = 'none';
        if (e.target.dataset.type === '房东') {
            fetch(`/feedback/get_houses_by_landlord?landlord_name=${encodeURIComponent(e.target.dataset.username)}`)
                .then(res => res.json())
                .then(data => {
                    houseSelect.innerHTML = `<option value="">不关联房源</option>`;
                    data.houses.forEach(h => {
                        houseSelect.innerHTML += `<option value="${h.house_id}">${h.house_name}</option>`;
                    });
                    houseSelectDiv.style.display = '';
                });
        } else {
            houseSelectDiv.style.display = 'none';
            houseSelect.value = '';
        }
    }
});

// 点击外部关闭自动补全
document.addEventListener('click', function(e) {
    if (!autocompleteDiv.contains(e.target) && e.target !== receiverInput) {
        autocompleteDiv.style.display = 'none';
    }
});