function loadRegionSelect(provinceId, cityId, districtId, selectedProvince, selectedCity, selectedDistrict) {
    fetch('/static/json/pca-code.json')
        .then(res => res.json())
        .then(data => {
            const provinceSelect = document.getElementById(provinceId);
            const citySelect = document.getElementById(cityId);
            const districtSelect = document.getElementById(districtId);

            // 填充省
            provinceSelect.innerHTML = '<option value="">选择省</option>';
            Object.keys(data).forEach(province => {
                provinceSelect.innerHTML += `<option value="${province}" ${province === selectedProvince ? 'selected' : ''}>${province}</option>`;
            });

            function loadCities(province) {
                citySelect.innerHTML = '<option value="">选择市</option>';
                districtSelect.innerHTML = '<option value="">选择区县</option>';
                if (province && data[province]) {
                    Object.keys(data[province]).forEach(city => {
                        citySelect.innerHTML += `<option value="${city}" ${city === selectedCity ? 'selected' : ''}>${city}</option>`;
                    });
                }
            }

            function loadDistricts(province, city) {
                districtSelect.innerHTML = '<option value="">选择区县</option>';
                if (province && city && data[province][city]) {
                    data[province][city].forEach(district => {
                        districtSelect.innerHTML += `<option value="${district}" ${district === selectedDistrict ? 'selected' : ''}>${district}</option>`;
                    });
                }
            }

            provinceSelect.addEventListener('change', () => {
                loadCities(provinceSelect.value);
            });

            citySelect.addEventListener('change', () => {
                loadDistricts(provinceSelect.value, citySelect.value);
            });

            // 初始触发加载
            loadCities(selectedProvince);
            loadDistricts(selectedProvince, selectedCity);
        });
}
