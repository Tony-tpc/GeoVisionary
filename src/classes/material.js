import * as THREE from "three";
import vertexShader from "./vt.glsl";
import fragmentShader from "./fm.glsl";

export const MeteorShaderMaterial = new THREE.ShaderMaterial({
    uniforms: {
        time: { value: 0 },
        //弥补自定义shader没有PointsMaterial材质的size属性
        size: { value: 8 },
        progress: { value: 0 },
        color: { value: new THREE.Color("#0f00f0") },
        /**
         * 流星的弧度 0为直线
         */
        radian: { value: 0 },
        /**
         * 切断开始
         */
        cutStart: { value: 0 },
        /**
         * 切断结束
         */
        cutEnd: { value: 0 },
    },
    blending: THREE.AdditiveBlending,
    // side: 2,
    transparent: true,
    // blending: THREE.AdditiveBlending,
    vertexShader,
    //弥补自定义shader没有PointsMaterial材质的sizeAttenuation属性
    fragmentShader,
    // alphaTest: 0.001,
    // depthTest: false,
    depthWrite: false,
});

