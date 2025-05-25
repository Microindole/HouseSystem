document.addEventListener("DOMContentLoaded", function () {
    const provinceSelect = document.getElementById("province");
    const citySelect = document.getElementById("city");
    const districtSelect = document.getElementById("district");
    const addressInput = document.getElementById("address");

    let pcaData = {};

    // 加载 JSON 文件
    fetch("/static/json/pca-code.json")
        .then(res => res.json())
        .then(data => {
            pcaData = data;
            loadProvinces();
        });

    function loadProvinces() {
        for (let province in pcaData) {
            const opt = document.createElement("option");
            opt.value = province;
            opt.textContent = province;
            provinceSelect.appendChild(opt);
        }
    }

    provinceSelect.addEventListener("change", () => {
        const selectedProvince = provinceSelect.value;
        citySelect.innerHTML = `<option value="">选择市</option>`;
        districtSelect.innerHTML = `<option value="">选择区/县</option>`;

        if (selectedProvince && pcaData[selectedProvince]) {
            for (let city in pcaData[selectedProvince]) {
                const opt = document.createElement("option");
                opt.value = city;
                opt.textContent = city;
                citySelect.appendChild(opt);
            }
        }

        updateAddress();
    });

    citySelect.addEventListener("change", () => {
        const selectedProvince = provinceSelect.value;
        const selectedCity = citySelect.value;
        districtSelect.innerHTML = `<option value="">选择区/县</option>`;

        if (selectedProvince && selectedCity && pcaData[selectedProvince][selectedCity]) {
            for (let district of pcaData[selectedProvince][selectedCity]) {
                const opt = document.createElement("option");
                opt.value = district;
                opt.textContent = district;
                districtSelect.appendChild(opt);
            }
        }

        updateAddress();
    });

    districtSelect.addEventListener("change", updateAddress);

    function updateAddress() {
        const province = provinceSelect.value;
        const city = citySelect.value;
        const district = districtSelect.value;
        addressInput.value = `${province}${city}${district}`;
    }
});
