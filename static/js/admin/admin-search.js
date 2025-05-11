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

function showHouses(landlordName) {
  fetch(`/account/admin/landlord_houses/${encodeURIComponent(landlordName)}`, {
    headers: { 'X-Requested-With': 'XMLHttpRequest' }
  })
    .then(res => {
      if (!res.ok) throw new Error('房东房源加载失败');
      return res.json();
    })
    .then(data => {
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
    })
    .catch(err => {
      console.error(err);
      alert('获取房源失败，请检查房东用户名是否正确');
    });
}



function downHouse(houseId, landlordName) {
  fetch('/account/admin/down_house', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Requested-With': 'XMLHttpRequest'
    },
    body: JSON.stringify({ house_id: houseId, landlord_name: landlordName })
  })
    .then(res => res.json())
    .then(result => {
      if (result.success) {
        showHouses(landlordName); // 重新加载房源
      } else {
        alert(result.message || '下架失败');
      }
    })
    .catch(err => {
      console.error(err);
      alert('请求失败');
    });
}

function closeModal() {
  document.getElementById('houseModal').style.display = 'none';
}
