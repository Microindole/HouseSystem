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
    if (val.length === 0) {
        autocompleteDiv.style.display = 'none';
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
        autocompleteDiv.style.display = 'none';
    }
    // 类型显示
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
        houseSelectDiv.style.display = 'none';
        houseSelect.value = '';
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