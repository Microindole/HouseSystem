document.addEventListener('DOMContentLoaded', function () {
    const provinceSelect = document.getElementById('province');
    const citySelect = document.getElementById('city');
    const districtSelect = document.getElementById('district');

    const pcaData = window.pcaDataFromServer || {}; // 你必须在模板中定义 window.pcaDataFromServer = {{ pca_data | tojson | safe }}

    function clearOptions(selectElement, defaultText) {
        selectElement.innerHTML = '';
        const option = document.createElement('option');
        option.value = '';
        option.textContent = defaultText;
        selectElement.appendChild(option);
    }

    function updateCityOptions() {
        const selectedProvince = provinceSelect.value;
        const cities = pcaData[selectedProvince] || {};

        clearOptions(citySelect, '请选择城市');
        clearOptions(districtSelect, '请先选择城市');

        Object.keys(cities).forEach(cityName => {
            const option = document.createElement('option');
            option.value = cityName;
            option.textContent = cityName;
            citySelect.appendChild(option);
        });
    }

    function updateDistrictOptions() {
        const selectedProvince = provinceSelect.value;
        const selectedCity = citySelect.value;
        const districts = (pcaData[selectedProvince] || {})[selectedCity] || [];

        clearOptions(districtSelect, '请选择区县');

        districts.forEach(d => {
            const option = document.createElement('option');
            option.value = d;
            option.textContent = d;
            districtSelect.appendChild(option);
        });
    }

    // 绑定事件
    if (provinceSelect) {
        provinceSelect.addEventListener('change', updateCityOptions);
    }

    if (citySelect) {
        citySelect.addEventListener('change', updateDistrictOptions);
    }
});
