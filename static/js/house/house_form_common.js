// static/js/common/house_form_common.js

/**
 * 更新城市下拉框的选项
 * @param {object} pcaData - 包含省市区数据的对象
 * @param {HTMLSelectElement} provinceSelectEl - 省份选择框元素
 * @param {HTMLSelectElement} citySelectEl - 城市选择框元素
 * @param {HTMLSelectElement} districtSelectEl - 区县选择框元素
 */
function updateCities(pcaData, provinceSelectEl, citySelectEl, districtSelectEl) {
    const selectedProvince = provinceSelectEl.value;
    citySelectEl.innerHTML = '<option value="">请选择城市</option>'; // 重置城市选项
    districtSelectEl.innerHTML = '<option value="">请先选择城市</option>'; // 重置区县选项

    if (selectedProvince && pcaData && pcaData[selectedProvince]) {
        const cities = Object.keys(pcaData[selectedProvince]);
        cities.forEach(function(cityName) {
            const option = document.createElement('option');
            option.value = cityName;
            option.textContent = cityName;
            citySelectEl.appendChild(option);
        });
    }
}

/**
 * 更新区县下拉框的选项
 * @param {object} pcaData - 包含省市区数据的对象
 * @param {HTMLSelectElement} provinceSelectEl - 省份选择框元素
 * @param {HTMLSelectElement} citySelectEl - 城市选择框元素
 * @param {HTMLSelectElement} districtSelectEl - 区县选择框元素
 */
function updateDistricts(pcaData, provinceSelectEl, citySelectEl, districtSelectEl) {
    const selectedProvince = provinceSelectEl.value;
    const selectedCity = citySelectEl.value;
    districtSelectEl.innerHTML = '<option value="">请选择区县</option>'; // 重置区县选项

    if (selectedProvince && selectedCity &&
        pcaData &&
        pcaData[selectedProvince] &&
        pcaData[selectedProvince][selectedCity]) {

        const districts = pcaData[selectedProvince][selectedCity];
        if (Array.isArray(districts)) {
            districts.forEach(function(districtName) {
                const option = document.createElement('option');
                option.value = districtName;
                option.textContent = districtName;
                districtSelectEl.appendChild(option);
            });
        } else {
            console.error("未能获取到有效的区县列表: ", districts);
        }
    }
}

/**
 * 验证房源表单的通用逻辑
 * @param {HTMLFormElement} formElement - 当前提交的表单元素
 * @returns {boolean} - 如果验证通过返回 true，否则返回 false
 */
function validateHouseForm(formElement) {
    const phoneInput = formElement.querySelector('#phone');
    if (phoneInput) {
        const phone = phoneInput.value;
        const phonePattern = /^[1][3-9]\d{9}$/; // 11位手机号正则
        if (!phonePattern.test(phone)) {
            if (window.showMessage) {
                window.showMessage('请输入正确的11位手机号码。', 'warning');
            } else {
                alert('请输入正确的11位手机号码。');
            }
            phoneInput.focus();
            return false;
        }
    }

    const priceInput = formElement.querySelector('#price');
    if (priceInput) {
        const price = parseFloat(priceInput.value);
        if (isNaN(price) || price <= 0) {
            if (window.showMessage) {
                window.showMessage('月租金必须为大于0的有效数字。', 'warning');
            } else {
                alert('月租金必须为大于0的有效数字。');
            }
            priceInput.focus();
            return false;
        }
    }

    const depositInput = formElement.querySelector('#deposit');
    if (depositInput) {
        const depositValue = depositInput.value;
        if (depositValue) { // 仅当用户输入了押金时才校验
            const deposit = parseFloat(depositValue);
            if (isNaN(deposit) || deposit < 0) {
                if (window.showMessage) {
                    window.showMessage('押金金额不能为负数，且必须为有效数字。', 'warning');
                } else {
                    alert('押金金额不能为负数，且必须为有效数字。');
                }
                depositInput.focus();
                return false;
            }
        }
    }

    const selects = formElement.querySelectorAll('select[required]');
    for (let i = 0; i < selects.length; i++) {
        if (selects[i].value === "") {
            const labelElement = formElement.querySelector(`label[for='${selects[i].id}']`);
            const labelText = labelElement ? labelElement.textContent.replace('*','').trim() : '该必选项';
            const message = `请选择${labelText}。`;
            if (window.showMessage) {
                window.showMessage(message, 'warning');
            } else {
                alert(message);
            }
            selects[i].focus();
            return false;
        }
    }
    return true; // 所有验证通过
}