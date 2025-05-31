function searchTenants() {
  const input = document.getElementById('tenantSearch').value.trim().toLowerCase();
  const rows = document.querySelectorAll('.user-box:first-child tbody tr');
  rows.forEach(row => {
    const username = row.cells[0].textContent.toLowerCase();
    row.style.display = username.includes(input) ? '' : 'none';
  });
}

function resetTenants() {
  document.getElementById('tenantSearch').value = '';
  const rows = document.querySelectorAll('.user-box:first-child tbody tr');
  rows.forEach(row => row.style.display = '');
}

function searchLandlords() {
  const input = document.getElementById('landlordSearch').value.trim().toLowerCase();
  const rows = document.querySelectorAll('.user-box:last-child tbody tr');
  rows.forEach(row => {
    const username = row.cells[0].textContent.toLowerCase();
    row.style.display = username.includes(input) ? '' : 'none';
  });
}

function resetLandlords() {
  document.getElementById('landlordSearch').value = '';
  const rows = document.querySelectorAll('.user-box:last-child tbody tr');
  rows.forEach(row => row.style.display = '');
}

function getStatusText(status) {
  switch (status) {
    case 0: return '空置';
    case 1: return '出租中';
    case 2: return '装修中';
    default: return '未知';
  }
}

// 函数仍然是 async 因为内部有 await fetch 和 await res.json()
async function showHouses(landlordName) {
  try {
    const res = await fetch(`/account/admin/landlord_houses/${encodeURIComponent(landlordName)}`, {
      headers: { 'X-Requested-With': 'XMLHttpRequest' }
    });
    if (!res.ok) throw new Error('房东房源加载失败');
    const data = await res.json();

    document.getElementById('modal-title').innerText = `房东 ${landlordName} 的房源列表`;
    const tbody = document.getElementById('house-table-body');
    tbody.innerHTML = '';
    data.forEach(h => {
      const row = document.createElement('tr');
      row.innerHTML = `
        <td>${h.house_id}</td>
        <td>${getStatusText(h.status)}</td>
        <td>${h.phone}</td>
        <td>${h.update_time}</td>
        <td>${h.house_name || ''}</td>
        <td>${h.region || ''}</td>
        <td>${h.addr || ''}</td>
        <td>
          ${h.status === 0 ? `<button class="btn-dangerous" onclick="downHouse(${h.house_id}, '${landlordName}')">下架</button>` : ''}
        </td>
      `;
      tbody.appendChild(row);
    });

    document.getElementById('houseModal').style.display = 'block';
  } catch (err) {
    console.error(err);
    // showAlert 前移除了 await
    window.showAlert('获取房源失败，请检查房东用户名是否正确', { type: 'error', title: '加载失败' });
  }
}

// 函数仍然是 async 因为内部有 await fetch, await res.json() 和 await showHouses()
async function downHouse(houseId, landlordName) {
  try {
    const res = await fetch('/account/admin/down_house', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Requested-With': 'XMLHttpRequest'
      },
      body: JSON.stringify({ house_id: houseId, landlord_name: landlordName })
    });
    const result = await res.json();
    if (result.success) {
      await showHouses(landlordName); // 调用 async 函数 showHouses 仍然建议使用 await
    } else {
      // showAlert 前移除了 await
      window.showAlert(result.message || '下架失败', { type: 'error', title: '操作失败' });
    }
  } catch (err) {
    console.error(err);
    // showAlert 前移除了 await
    window.showAlert('请求失败', { type: 'error', title: '网络错误' });
  }
}

function closeModal() {
  document.getElementById('houseModal').style.display = 'none';
}