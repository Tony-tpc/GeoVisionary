

// 着色器材质
import * as THREE from "three";
import {BufferAttribute, BufferGeometry} from "three";

const vertexShader = `
varying vec3 vColor;
uniform float time;
uniform float size;
uniform float progress;
uniform vec3 target;
uniform float wave;
uniform float radian;
uniform float cutStart;
uniform float cutEnd;
attribute float percent;
attribute vec3 color;

void main() {
    vec3 dispatchPos;

    float p = min(progress, 1.);
    float rp = p >= percent ? percent : p;

    if(rp > cutStart && rp < cutEnd) {
        rp = cutStart;
    }
    dispatchPos = position + (target - position) * rp;
    dispatchPos.y *= sin(rp * 0.4) * radian;

    vColor = color;

    vec4 viewPosition = modelViewMatrix * vec4(dispatchPos, 1.0);

    gl_Position = projectionMatrix * viewPosition;

    gl_PointSize = size;

    gl_PointSize *= (120. / -(modelViewMatrix * vec4(dispatchPos, 1.0)).z);
    gl_PointSize *= (0.2 + rp);
}
`;

const fragmentShader = `
varying vec3 vColor;

void main() {
    float strength = distance(gl_PointCoord, vec2(0.5));
    strength = step(0.5, strength);
    strength = 1.0 - strength;
    gl_FragColor = vec4(vColor, strength);
}
`;

const MeteorShaderMaterial = new THREE.ShaderMaterial({
    uniforms: {
        time: { value: 0 },
        size: { value: 8 },
        progress: { value: 0 },
        color: { value: new THREE.Color("#0f00f0") },
        radian: { value: 0 },
        cutStart: { value: 0 },
        cutEnd: { value: 0 },
        target: { value: new THREE.Vector3(0, 0, 0) },
    },
    blending: THREE.AdditiveBlending,
    transparent: true,
    vertexShader,
    fragmentShader,
    depthWrite: false,
});

const defaultProps = {
    numberOfPoints: 1000,
    color: {
        left: new THREE.Color("#5555ff"),
        right: new THREE.Color("#00ffff"),
    },
    target: new THREE.Vector3(250, 20, 0),
};

export default class MeteorClass {
    constructor(
        numberOfPoints,
        target,
        color,
        radian,
        second,
        hideSecond,
        cut,
    ) {
        this.group = new THREE.Group();
        this.numberOfPoints = numberOfPoints || defaultProps.numberOfPoints;
        this.color = color || defaultProps.color;
        this.target = target || defaultProps.target;
        this.second = second;
        this.hideSecond = hideSecond;
        this.material = MeteorShaderMaterial.clone();
        this.initSize = this.material.uniforms.size.value;
        this.clock = new THREE.Clock();
        this.t = 0;

        if (radian) {
            this.material.uniforms.radian.value = radian;
        }
        if (cut) {
            this.material.uniforms.cutStart.value = cut[0];
            this.material.uniforms.cutEnd.value = cut[1];
        }
        this.initObj();
    }

    genGeometry() {
        const numberOfPoints = this.numberOfPoints;
        const geometry = new BufferGeometry();
        const positions = new Float32Array(numberOfPoints * 3);
        const colors = new Float32Array(numberOfPoints * 3);
        const percents = new Float32Array(numberOfPoints);
        const { left: leftColor, right: rightColor } = this.color;
        const gradientColor = {
            r: leftColor.r - rightColor.r,
            g: leftColor.g - rightColor.g,
            b: leftColor.b - rightColor.b,
        };

        for (let i = 0; i <= numberOfPoints; i++) {
            const i3 = i * 3;
            const x = 0;
            const y = 0;
            const z = 0;
            positions[i3] = x;
            positions[i3 + 1] = y;
            positions[i3 + 2] = z;
            const percent = i / numberOfPoints;
            percents[i] = percent;

            colors[i3] = leftColor.r - gradientColor.r * percent;
            colors[i3 + 1] = leftColor.g - gradientColor.g * percent;
            colors[i3 + 2] = leftColor.b - gradientColor.b * percent;
        }

        geometry.setAttribute("position", new BufferAttribute(positions, 3));
        geometry.setAttribute("color", new BufferAttribute(colors, 3));
        geometry.setAttribute("percent", new BufferAttribute(percents, 1));
        return geometry;
    }

    initObj() {
        const geometry = this.genGeometry();
        this.material.uniforms.target.value = this.target;
        const mesh = new THREE.Points(geometry, this.material);
        this.group.add(mesh);
    }

    update(p) {
        let percent = p || 0;
        if (this.second) {
            this.t += this.clock.getDelta();
            percent = this.t / this.second;

            if (percent >= 1 && this.hideSecond) {
                let over = 1 - (this.t - this.second) / this.hideSecond;

                if (over <= 0) {
                    this.t = 0;
                    over = 1;
                    percent = 0;
                }
                this.material.uniforms.size.value = this.initSize * over;
            }
        } else {
            if (percent > 1) {
                this.material.uniforms.size.value /= 1.1;
            } else {
                this.material.uniforms.size.value = this.initSize;
            }
        }
        this.material.uniforms.progress.value = percent;
    }
}