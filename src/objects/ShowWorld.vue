<template>
    <div class="main-container">
        <!-- Cesium 地图容器 -->
        <div id="leafletMap" @contextmenu.prevent="showContextMenu">
            <el-menu v-show="contextMenu.visible" ref="contextMenuRef" :style="menuStyle" class="custom-context-menu"
                mode="vertical" @select="handleMenuSelect">
                <el-menu-item index="addMarker" class="menu-item">
                    <span class="menu-text">添加标记</span>
                </el-menu-item>
                <el-menu-item index="clearMarkers" class="menu-item">
                    <span class="menu-text">清除所有标记</span>
                </el-menu-item>
                <el-menu-item index="zoomToMax" class="menu-item">
                    <span class="menu-text">缩放到最大</span>
                </el-menu-item>
                <el-menu-item index="askai" class="menu-item">
                    <span class="menu-text">询问AI</span>
                </el-menu-item>
            </el-menu>
        </div>

        <!-- 聊天窗口 -->
        <div class="chat-container" :class="{ 'chat-collapsed': isChatCollapsed }">
            <!-- 聊天窗口头部
            <div class="chat-header">
                <span>Chat with AI</span>
                <button @click="toggleChat" class="chat-toggle-btn">
                    {{ isChatCollapsed ? '展开' : '收起' }}
                </button>
            </div> -->

            <!-- 聊天内容 -->
            <div class="chat-content">
                <Chat ref="chatRef" v-if="!isChatCollapsed" />
            </div>
        </div>
    </div>
</template>


<script setup>
import { ref, onMounted } from "vue";
import L from "leaflet";
import "leaflet/dist/leaflet.css";
import { ElMessage } from 'element-plus'
import Chat from "@/objects/Chat.vue";
import sign from '@/assets/sign.png'
// 标记管理
let map = null;
const markers = ref([]);
const contextMenu = ref({
    visible: false,
    x: 100,
    y: 100,
    position: null
});
const contextMenuRef = ref(null);
const menuStyle = ref({});
// 控制聊天窗口的收起和展开
const isChatCollapsed = ref(false);
// 继承chat
const chatRef = ref(null);

const TDU_Key = import.meta.env.VITE_TDU_Key
const TXDT_Key = import.meta.env.VITE_TXDT_Key


// 右键菜单逻辑（保持原有结构，修改坐标获取方式）
const showContextMenu = (event) => {
    const container = document.getElementById('leafletMap');
    const rect = container.getBoundingClientRect();
    const menuWidth = 140; // 菜单宽度
    const menuHeight = 100; // 菜单高度

    // 转换坐标到地图坐标
    const point = map.latLngToContainerPoint(map.getCenter());
    const latlng = map.containerPointToLatLng([
        event.clientX - rect.left,
        event.clientY - rect.top
    ]);

    contextMenu.value = {
        visible: true,
        x: event.clientX - rect.left,
        y: event.clientY - rect.top,
        position: latlng
    };

    // 更新菜单样式
    menuStyle.value = {
        position: 'fixed',
        left: `${contextMenu.value.x}px`,
        top: `${contextMenu.value.y}px`,
        zIndex: 9999
    };

    // 点击其他地方关闭菜单
    setTimeout(() => {
        document.addEventListener('click', closeContextMenu, { once: true });
    }, 0); 

};

// 地图初始化
onMounted(() => {
    map = L.map('leafletMap', {
        preferCanvas: true,
        contextmenu: true,
        // crs: L.CRS.EPSG3857,
        contextmenuWidth: 140
    }).setView([31.2304, 121.4737], 13);

    // 使用符合国家规定的天地图服务（GCJ-02坐标系）
    L.tileLayer(`http://t0.tianditu.gov.cn/img_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=img&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&tk=${TDU_Key}`, {
        maxZoom: 18,
        subdomains: ['a', 'b', 'c']
    }).addTo(map);

    // 添加中文标注图层（GCJ-02坐标系）
    L.tileLayer(`http://t0.tianditu.gov.cn/cia_w/wmts?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=cia&STYLE=default&TILEMATRIXSET=w&FORMAT=tiles&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&tk=${TDU_Key}`, {
        maxZoom: 18,
        subdomains: ['a', 'b', 'c']
    }).addTo(map);
});

// 归一化经纬度
function normalizeCoordinate(coord, max) {
    // 对于经度，max为180；对于纬度，max为90
    while (coord < -max) coord += 2 * max;
    while (coord > max) coord -= 2 * max;
    return coord;
}

// 添加标记方法
const addMarker = (latlng) => {
    const marker = L.marker(latlng, {
        icon: L.icon({
            iconUrl: sign,
            iconSize: [40, 40],
            iconAnchor: [20, 40]
        })
    }).addTo(map);

    markers.value.push(marker);
    ElMessage.success(`标记添加成功 (${(normalizeCoordinate(latlng.lat, 90)).toFixed(4)}, ${(normalizeCoordinate(latlng.lng, 180)).toFixed(4)})`);
    map.invalidateSize(true);
};

// 清除标记方法
const clearMarkers = () => {
    markers.value.forEach(marker => map.removeLayer(marker));
    markers.value = [];
    ElMessage.success("已清除所有标记");
    map.invalidateSize(true);

};

// 缩放到最大范围
const zoomToMax = () => {
    map.setView([0, 0], 2);
    ElMessage.success("已缩放到最大范围");
};

// 菜单项处理
const handleMenuSelect = (index) => {
    switch (index) {
        case 'addMarker':
            addMarker(contextMenu.value.position);
            break;
        case 'askai':
            handleMapClick(contextMenu.value.position);
            break;
        case 'clearMarkers':
            clearMarkers();
            break;
        case 'zoomToMax':
            zoomToMax();
            break;
    }
    closeContextMenu();
};

// 询问ai   
const handleMapClick = async (cartesian) => {
    addMarker(cartesian);

    if (!cartesian) return;
    console.log(cartesian.lat, cartesian.lng);

    const lat = (normalizeCoordinate(cartesian.lat, 90)).toFixed(5);
    const lng = (normalizeCoordinate(cartesian.lng, 180)).toFixed(5);
    console.log(lat, lng);

    const region = await reverseGeocoding(lat, lng);
    console.log(region);

    // 询问 AI
    askAI(lng, lat, region);
}


const reverseGeocoding = async (lat, lng) => {
    var region = "";
    try {
        const response = await fetch(
            `/qqmap/ws/geocoder/v1?key=${TXDT_Key}&location=${lat},${lng}`
        )
        // 严格模式下的JSON解析
        const text = await response.text();
        const data = JSON.parse(text); // 避免使用response.json()的潜在问题
        if (data.status !== 0) {
            throw new Error(data.message || '地址解析失败')
        }
        if (data.result.address_component.nation != "" && data.result.address_component.nation != "Ocean" && data.result.address_component.nation != "undefined")
            region += `nation: ${data.result.address_component.nation}  `;
        if (data.result.address_component.province != "" && data.result.address_component.province != "undefined")
            region += `province: ${data.result.address_component.province}  `;
        if (data.result.address_component.city != "" && data.result.address_component.city != "undefined")
            region += `city: ${data.result.address_component.city}  `;
    } catch (error) {
        console.error('逆地址解析失败:', error)
    }
    return region;
}

const askAI = async (latitude, longitude, region) => {
    var head = ""
    if (region != "") {
        head =
            `
现在，请告诉我${region}的地理信息和人文特点：
纬度 ${latitude}，经度 ${longitude}
`
    }
    else head =
        `
现在，请告诉我以下位置的地理信息和人文特点：
纬度 ${latitude}，经度 ${longitude}
`

    const prompt = `
请按照以下格式回答：

1. **地理位置**：
   - 经纬度：{纬度}, {经度}
   - 所属国家/地区：{国家/地区}
   - 所属省份/州：{省份/州}
   - 所属城市：{城市}

2. **地理信息**：
   - 地形：{地形类型}
   - 气候：{气候类型}
   - 自然资源：{自然资源}

3. **人文特点**：
   - 人口：{人口数量}
   - 语言：{主要语言}
   - 文化特色：{文化特色}
   - 著名景点：{著名景点}

4. **其他信息**：
   - 历史背景：{历史背景}
   - 经济发展：{经济发展}
`
    // 解析 AI 返回的经纬度并标记
    chatRef.value.handleAIResponse(head + prompt);
};

// 监听拖动事件
const handleDrag = () => {
    if (contextMenu.value.visible) {
        closeContextMenu();
    }
};

const closeContextMenu = () => {
    contextMenu.value.visible = false;
};
</script>
<style>
/* 调整地图容器样式 */
#leafletMap {
    flex: 1;
    height: 100vh;
    z-index: 1;
}

/* 主容器布局 */
.main-container {
    display: flex;
    height: 100vh;
    width: 100%;
    margin: 0 auto;
    overflow-y: scroll;
}

.custom-context-menu {
    position: absolute;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    border-radius: 8px;
    background: linear-gradient(145deg, #ffffff, #f9f9f9);
    border: 1px solid #e0e0e0;
    min-width: 160px;
    padding: 8px 0;
    z-index: 9999;
}

/* 聊天窗口容器 */
.chat-container {
    width: 400px;
    /* 默认宽度 */
    height: 100vh;
    background-color: #ffffff;
    box-shadow: -2px 0 8px rgba(0, 0, 0, 0.1);
    transition: width 0.3s ease;
    display: flex;
    flex-direction: column;
    overflow-y: scroll;
    overflow-x: hidden;
}

/* 菜单项样式 */
.menu-item {
    height: 36px;
    line-height: 36px;
    font-size: 14px;
    color: #333;
    padding: 0 16px;
    margin: 0 8px;
    border-radius: 6px;
    transition: all 0.2s ease;
}

/* 菜单项悬停效果 */
.menu-item:hover {
    background: linear-gradient(145deg, #f0f0f0, #e0e0e0);
    color: #409eff;
    transform: translateX(4px);
}
</style>