/**
 * 地图详情组件 - 提供丰富的地图功能
 */

class MapDetailComponent {
    constructor(mapInstance, houseData) {
        this.map = mapInstance;
        this.houseData = houseData;
        this.currentMarker = null;
        this.trafficLayer = null;
        this.isTrafficVisible = false;
        this.poiMarkers = [];
        this.routeLayer = null;
        this.isVisible = false;
        
        this.init();
    }

    init() {
        this.createMapButton();
        this.createModal();
        this.bindEvents();
    }

    // 创建地图按钮
    createMapButton() {
        const mapContainer = document.getElementById('map-container');
        if (!mapContainer) return;

        const mapButton = document.createElement('button');
        mapButton.id = 'map-detail-btn';
        mapButton.className = 'map-detail-trigger';
        mapButton.innerHTML = `
            <span class="map-icon">🗺️</span>
            <span class="map-text">地图工具</span>
        `;
        mapButton.title = '打开地图工具箱';
        
        mapContainer.appendChild(mapButton);
    }

    // 创建模态框
    createModal() {
        const modal = document.createElement('div');
        modal.id = 'map-detail-modal';
        modal.className = 'map-detail-modal';
        modal.innerHTML = this.getModalHTML();
        
        document.body.appendChild(modal);
    }

    // 获取模态框HTML
    getModalHTML() {
        return `
            <div class="map-detail-overlay">
                <div class="map-detail-content">
                    <div class="map-detail-header">
                        <h3>地图工具箱</h3>
                        <button class="close-btn" id="close-map-detail">&times;</button>
                    </div>
                    
                    <div class="map-detail-body">
                        <div class="map-tools-grid">
                            <!-- 基础功能 -->
                            <div class="tool-section">
                                <h4>🎯 基础工具</h4>
                                <div class="tool-buttons">
                                    <button class="tool-btn" id="center-location" title="回到房源位置">
                                        <span class="icon">📍</span>
                                        <span>房源位置</span>
                                    </button>
                                    <button class="tool-btn" id="toggle-traffic" title="切换实时路况">
                                        <span class="icon">🚦</span>
                                        <span>实时路况</span>
                                    </button>
                                    <button class="tool-btn" id="measure-distance" title="测量距离">
                                        <span class="icon">📏</span>
                                        <span>测量距离</span>
                                    </button>
                                    <button class="tool-btn" id="satellite-view" title="卫星视图">
                                        <span class="icon">🛰️</span>
                                        <span>卫星地图</span>
                                    </button>
                                </div>
                            </div>

                            <!-- 周边设施 -->
                            <div class="tool-section">
                                <h4>🏪 周边设施</h4>
                                <div class="tool-buttons">
                                    <button class="tool-btn poi-btn" data-type="地铁站" title="查找附近地铁站">
                                        <span class="icon">🚇</span>
                                        <span>地铁站</span>
                                    </button>
                                    <button class="tool-btn poi-btn" data-type="公交站" title="查找附近公交站">
                                        <span class="icon">🚌</span>
                                        <span>公交站</span>
                                    </button>
                                    <button class="tool-btn poi-btn" data-type="医院" title="查找附近医院">
                                        <span class="icon">🏥</span>
                                        <span>医院</span>
                                    </button>
                                    <button class="tool-btn poi-btn" data-type="学校" title="查找附近学校">
                                        <span class="icon">🏫</span>
                                        <span>学校</span>
                                    </button>
                                    <button class="tool-btn poi-btn" data-type="超市" title="查找附近超市">
                                        <span class="icon">🛒</span>
                                        <span>超市</span>
                                    </button>
                                    <button class="tool-btn poi-btn" data-type="餐厅" title="查找附近餐厅">
                                        <span class="icon">🍽️</span>
                                        <span>餐厅</span>
                                    </button>
                                </div>
                            </div>

                            <!-- 路线规划 -->
                            <div class="tool-section">
                                <h4>🛣️ 路线规划</h4>
                                <div class="route-form">
                                    <input type="text" id="start-address" placeholder="输入起点地址" class="route-input">
                                    <div class="route-buttons">
                                        <button class="tool-btn" id="plan-driving" title="驾车路线">
                                            <span class="icon">🚗</span>
                                            <span>驾车</span>
                                        </button>
                                        <button class="tool-btn" id="plan-transit" title="公交路线">
                                            <span class="icon">🚌</span>
                                            <span>公交</span>
                                        </button>
                                        <button class="tool-btn" id="plan-walking" title="步行路线">
                                            <span class="icon">🚶</span>
                                            <span>步行</span>
                                        </button>
                                    </div>
                                </div>
                            </div>

                            <!-- 地图信息 -->
                            <div class="tool-section">
                                <h4>ℹ️ 地图信息</h4>
                                <div class="map-info">
                                    <div class="info-item">
                                        <span class="label">缩放级别:</span>
                                        <span id="zoom-level">-</span>
                                    </div>
                                    <div class="info-item">
                                        <span class="label">中心坐标:</span>
                                        <span id="center-coords">-</span>
                                    </div>
                                    <div class="info-item">
                                        <span class="label">房源地址:</span>
                                        <span>${this.houseData.region} ${this.houseData.addr}</span>
                                    </div>
                                </div>
                                <div class="tool-buttons">
                                    <button class="tool-btn" id="clear-all" title="清除所有标记">
                                        <span class="icon">🧹</span>
                                        <span>清除标记</span>
                                    </button>
                                    <button class="tool-btn" id="refresh-map" title="刷新地图">
                                        <span class="icon">🔄</span>
                                        <span>刷新地图</span>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }

    // 绑定事件
    bindEvents() {
        // 打开模态框
        document.getElementById('map-detail-btn').addEventListener('click', () => {
            this.showModal();
        });

        // 关闭模态框
        document.getElementById('close-map-detail').addEventListener('click', () => {
            this.hideModal();
        });

        // 点击遮罩关闭
        document.querySelector('.map-detail-overlay').addEventListener('click', (e) => {
            if (e.target === e.currentTarget) {
                this.hideModal();
            }
        });

        // 基础工具事件
        document.getElementById('center-location').addEventListener('click', () => {
            this.centerToHouse();
        });

        document.getElementById('toggle-traffic').addEventListener('click', () => {
            this.toggleTraffic();
        });

        document.getElementById('measure-distance').addEventListener('click', () => {
            this.startMeasure();
        });

        document.getElementById('satellite-view').addEventListener('click', () => {
            this.toggleSatellite();
        });

        // POI查找事件
        document.querySelectorAll('.poi-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const poiType = e.currentTarget.dataset.type;
                this.searchPOI(poiType);
            });
        });

        // 路线规划事件
        document.getElementById('plan-driving').addEventListener('click', () => {
            this.planRoute('driving');
        });

        document.getElementById('plan-transit').addEventListener('click', () => {
            this.planRoute('transit');
        });

        document.getElementById('plan-walking').addEventListener('click', () => {
            this.planRoute('walking');
        });

        // 清除和刷新
        document.getElementById('clear-all').addEventListener('click', () => {
            this.clearAllMarkers();
        });

        document.getElementById('refresh-map').addEventListener('click', () => {
            this.refreshMap();
        });

        // 地图事件监听
        if (this.map) {
            this.map.addEventListener('zoomend', () => {
                this.updateMapInfo();
            });

            this.map.addEventListener('moveend', () => {
                this.updateMapInfo();
            });
        }
    }

    // 显示模态框
    showModal() {
        const modal = document.getElementById('map-detail-modal');
        modal.style.display = 'block';
        document.body.style.overflow = 'hidden';
        this.isVisible = true;
        this.updateMapInfo();
    }

    // 隐藏模态框
    hideModal() {
        const modal = document.getElementById('map-detail-modal');
        modal.style.display = 'none';
        document.body.style.overflow = '';
        this.isVisible = false;
    }

    // 回到房源位置
    centerToHouse() {
        if (!this.map || !this.currentMarker) return;
        
        try {
            const point = this.currentMarker.getPosition();
            this.map.centerAndZoom(point, 17);
            this.showSuccess('已回到房源位置');
        } catch (error) {
            this.showError('定位失败');
        }
    }

    // 切换交通流量
    toggleTraffic() {
        const button = document.getElementById('toggle-traffic');
        
        try {
            if (this.isTrafficVisible) {
                if (this.trafficLayer) {
                    this.map.removeOverlay(this.trafficLayer);
                    this.trafficLayer = null;
                }
                button.classList.remove('active');
                this.isTrafficVisible = false;
                this.showSuccess('已关闭实时路况');
            } else {
                this.trafficLayer = new BMapGL.TrafficLayer();
                this.map.addOverlay(this.trafficLayer);
                button.classList.add('active');
                this.isTrafficVisible = true;
                this.showSuccess('已开启实时路况');
            }
        } catch (error) {
            this.showError('路况功能暂时不可用');
        }
    }

    // 测量距离
    startMeasure() {
        try {
            if (typeof BMapGLLib !== 'undefined' && BMapGLLib.DistanceTool) {
                const distanceTool = new BMapGLLib.DistanceTool(this.map);
                distanceTool.open();
                this.showSuccess('点击地图开始测距');
            } else {
                this.showError('测距工具未加载');
            }
        } catch (error) {
            this.showError('测距功能暂时不可用');
        }
    }

    // 切换卫星视图
    toggleSatellite() {
        const button = document.getElementById('satellite-view');
        
        try {
            if (button.classList.contains('active')) {
                this.map.setMapType(BMAP_NORMAL_MAP);
                button.classList.remove('active');
                this.showSuccess('已切换到普通地图');
            } else {
                this.map.setMapType(BMAP_SATELLITE_MAP);
                button.classList.add('active');
                this.showSuccess('已切换到卫星地图');
            }
        } catch (error) {
            this.showError('地图类型切换失败');
        }
    }

    // 搜索POI
    searchPOI(poiType) {
        if (!this.currentMarker) return;

        const housePoint = this.currentMarker.getPosition();
        const local = new BMapGL.LocalSearch(this.map, {
            renderOptions: { 
                map: this.map, 
                autoViewport: false 
            },
            onSearchComplete: (results) => {
                if (local.getStatus() === BMAP_STATUS_SUCCESS) {
                    this.clearPOIMarkers();
                    
                    for (let i = 0; i < Math.min(results.getCurrentNumPois(), 10); i++) {
                        const poi = results.getPoi(i);
                        this.addPOIMarker(poi, poiType);
                    }
                    
                    this.showSuccess(`找到 ${Math.min(results.getCurrentNumPois(), 10)} 个${poiType}`);
                } else {
                    this.showError(`未找到附近的${poiType}`);
                }
            }
        });
        
        local.searchNearby(poiType, housePoint, 2000);
    }

    // 添加POI标记
    addPOIMarker(poi, type) {
        const iconMap = {
            '地铁站': '🚇', '公交站': '🚌', '医院': '🏥',
            '学校': '🏫', '超市': '🛒', '餐厅': '🍽️'
        };
        
        const icon = iconMap[type] || '📍';
        const marker = new BMapGL.Marker(poi.point);
        
        this.map.addOverlay(marker);
        this.poiMarkers.push(marker);
        
        // 添加信息窗口
        const infoWindow = new BMapGL.InfoWindow(`
            <div style="padding: 8px;">
                <h5 style="margin: 0 0 5px 0;">${icon} ${poi.title}</h5>
                <p style="margin: 0; font-size: 12px; color: #666;">${poi.address}</p>
            </div>
        `);
        
        marker.addEventListener('click', () => {
            this.map.openInfoWindow(infoWindow, poi.point);
        });
    }

    // 路线规划
    planRoute(type) {
        const startAddress = document.getElementById('start-address').value.trim();
        if (!startAddress) {
            this.showError('请输入起点地址');
            return;
        }

        if (!this.currentMarker) {
            this.showError('房源位置未找到');
            return;
        }

        const endPoint = this.currentMarker.getPosition();
        
        try {
            if (this.routeLayer) {
                this.map.clearOverlays();
                this.routeLayer = null;
            }

            switch (type) {
                case 'driving':
                    this.routeLayer = new BMapGL.DrivingRoute(this.map, {
                        renderOptions: { map: this.map, autoViewport: true }
                    });
                    break;
                case 'transit':
                    this.routeLayer = new BMapGL.TransitRoute(this.map, {
                        renderOptions: { map: this.map, autoViewport: true }
                    });
                    break;
                case 'walking':
                    this.routeLayer = new BMapGL.WalkingRoute(this.map, {
                        renderOptions: { map: this.map, autoViewport: true }
                    });
                    break;
            }
            
            this.routeLayer.search(startAddress, endPoint);
            this.showSuccess(`正在规划${type === 'driving' ? '驾车' : type === 'transit' ? '公交' : '步行'}路线`);
            
        } catch (error) {
            this.showError('路线规划失败');
        }
    }

    // 清除POI标记
    clearPOIMarkers() {
        this.poiMarkers.forEach(marker => {
            this.map.removeOverlay(marker);
        });
        this.poiMarkers = [];
    }

    // 清除所有标记
    clearAllMarkers() {
        this.clearPOIMarkers();
        
        if (this.routeLayer) {
            this.map.clearOverlays();
            this.routeLayer = null;
        }
        
        if (this.trafficLayer) {
            this.map.removeOverlay(this.trafficLayer);
            this.trafficLayer = null;
            this.isTrafficVisible = false;
            document.getElementById('toggle-traffic').classList.remove('active');
        }
        
        // 重新添加房源标记
        if (this.currentMarker) {
            this.map.addOverlay(this.currentMarker);
        }
        
        this.showSuccess('已清除所有标记');
    }

    // 刷新地图
    refreshMap() {
        try {
            this.map.reset();
            this.centerToHouse();
            this.clearAllMarkers();
            this.showSuccess('地图已刷新');
        } catch (error) {
            this.showError('地图刷新失败');
        }
    }

    // 更新地图信息
    updateMapInfo() {
        if (!this.isVisible || !this.map) return;
        
        try {
            const zoom = this.map.getZoom();
            const center = this.map.getCenter();
            
            document.getElementById('zoom-level').textContent = zoom;
            document.getElementById('center-coords').textContent = 
                `${center.lng.toFixed(6)}, ${center.lat.toFixed(6)}`;
        } catch (error) {
            console.error('更新地图信息失败:', error);
        }
    }

    // 设置当前标记
    setCurrentMarker(marker) {
        this.currentMarker = marker;
    }

    // 显示成功消息
    showSuccess(message) {
        if (window.showMessage) {
            window.showMessage(message, 'success');
        } else {
            console.log('✓ ' + message);
        }
    }

    // 显示错误消息
    showError(message) {
        if (window.showMessage) {
            window.showMessage(message, 'error');
        } else {
            console.error('✗ ' + message);
        }
    }
}

// 全局变量
let mapDetailComponent = null;

// 初始化地图详情组件
function initMapDetailComponent(mapInstance, houseData, marker) {
    if (mapDetailComponent) {
        mapDetailComponent.setCurrentMarker(marker);
        return mapDetailComponent;
    }
    
    mapDetailComponent = new MapDetailComponent(mapInstance, houseData);
    mapDetailComponent.setCurrentMarker(marker);
    
    return mapDetailComponent;
}

// 暴露到全局
window.initMapDetailComponent = initMapDetailComponent;