<template>
  <div id="cesiumContainer"></div>
</template>

<script setup>
import { onMounted } from "vue";
import * as Cesium from "cesium";

onMounted(() => {
    const YOURURL = "/models/chlif/tileset.json";

  let viewer = new Cesium.Viewer("cesiumContainer", {
      homeButton: false, //主页按钮
      baseLayerPicker: false, //是否显示图层选择控件
      navigationHelpButton: true, //帮助信息按钮
      geocoder: true, //是否显示地名查找控件
      terrainProvider: new Cesium.EllipsoidTerrainProvider(), // 使用椭球地形
      requestRenderMode: true //显式渲染

  });

  viewer._cesiumWidget._creditContainer.style.display = "none";
  viewer.scene.globe.show = false;
  viewer.scene.debugShowFramesPerSecond = true;
  viewer.scene.requestRenderMode = true;
  viewer.scene.backgroundColor = new Cesium.Color(10, 10, 10, 1);
  viewer.terrainProvider = new Cesium.EllipsoidTerrainProvider();
  var position = Cesium.Cartesian3.fromDegrees(10, 10, 100); // 经度、纬度、海拔高度
  var heading = Cesium.Math.toRadians(0); // 头朝向
  var pitch = 0; // 俯仰角
  var roll = Cesium.Math.toRadians(90); // 滚动角
  var hpr = new Cesium.HeadingPitchRoll(heading, pitch, roll);
  // 获取正确的矩阵来定位模型
  var modelMatrix = Cesium.Transforms.headingPitchRollToFixedFrame(position, hpr);
  // 处理 skyBox、sun、moon、skyAtmosphere
  if (Cesium.defined(viewer.scene.skyBox)) {
      viewer.scene.skyBox.destroy();
      viewer.scene.skyBox = undefined;
  }
  if (Cesium.defined(viewer.scene.sun)) {
      viewer.scene.sun.destroy();
      viewer.scene.sun = undefined;
  }
  if (Cesium.defined(viewer.scene.moon)) {
      viewer.scene.moon.destroy();
      viewer.scene.moon = undefined;
  }
  if (Cesium.defined(viewer.scene.skyAtmosphere)) {
      viewer.scene.skyAtmosphere.destroy();
      viewer.scene.skyAtmosphere = undefined;
  }

    // 加载 Tileset
    console.log("Tileset URL:", YOURURL);
    Cesium.Cesium3DTileset.fromUrl(YOURURL, {
        modelMatrix: modelMatrix,
        // maximumScreenSpaceError: 0.1,
        skipLevels: true, // 跳过不必要的级别

  })
      .then((tileset) => {
          viewer.scene.primitives.add(tileset);
          tileset.enableCache = true;

          const boundingSphere = tileset.boundingSphere;
          const radius = boundingSphere.radius;
          // 自动飞到模型位置
          viewer.camera.flyToBoundingSphere(boundingSphere, {
              duration: 0.5,

              offset: new Cesium.HeadingPitchRange(
                  Cesium.Math.toRadians(0),
                  Cesium.Math.toRadians(0),
                  boundingSphere.radius * 3.0
              )
          });
          viewer.camera.lookAt(position, new Cesium.HeadingPitchRange(
              0,  // 头朝向（heading）
              0,  // 俯仰角（pitch）
              -10,
          ));
      })
      .catch((error) => {
          console.error("Tileset 加载失败:", error);
      });
});
</script>

<style>
#cesiumContainer {
  width: 100%;
  height: 100%;
  overflow: hidden;
}
</style>
