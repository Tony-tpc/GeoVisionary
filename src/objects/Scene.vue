<template>
    <canvas ref="canvas"></canvas>
    <Options @speedChanged="onSpeedChange"/>
    <PlanetCard v-if="selectedPlanetCard != null" :planetInfo="selectedPlanetCard"  @closeCard="selectedPlanetCard = null"/>
    <div class="date-display" :class="{disabled: idealizedSpeed}">
        <div class="ico">
            <svg viewBox="0 0 448 512" xmlns="http://www.w3.org/2000/svg"><path d="M0 464c0 26.5 21.5 48 48 48h352c26.5 0 48-21.5 48-48V192H0v272zm320-196c0-6.6 5.4-12 12-12h40c6.6 0 12 5.4 12 12v40c0 6.6-5.4 12-12 12h-40c-6.6 0-12-5.4-12-12v-40zm0 128c0-6.6 5.4-12 12-12h40c6.6 0 12 5.4 12 12v40c0 6.6-5.4 12-12 12h-40c-6.6 0-12-5.4-12-12v-40zM192 268c0-6.6 5.4-12 12-12h40c6.6 0 12 5.4 12 12v40c0 6.6-5.4 12-12 12h-40c-6.6 0-12-5.4-12-12v-40zm0 128c0-6.6 5.4-12 12-12h40c6.6 0 12 5.4 12 12v40c0 6.6-5.4 12-12 12h-40c-6.6 0-12-5.4-12-12v-40zM64 268c0-6.6 5.4-12 12-12h40c6.6 0 12 5.4 12 12v40c0 6.6-5.4 12-12 12H76c-6.6 0-12-5.4-12-12v-40zm0 128c0-6.6 5.4-12 12-12h40c6.6 0 12 5.4 12 12v40c0 6.6-5.4 12-12 12H76c-6.6 0-12-5.4-12-12v-40zM400 64h-48V16c0-8.8-7.2-16-16-16h-32c-8.8 0-16 7.2-16 16v48H160V16c0-8.8-7.2-16-16-16h-32c-8.8 0-16 7.2-16 16v48H48C21.5 64 0 85.5 0 112v48h448v-48c0-26.5-21.5-48-48-48z" fill="#ffffff" class="fill-000000"></path></svg>
        </div>
        <p>{{ date }}</p>
    </div>
</template>

<script>
import * as THREE from "three";
import { OrbitControls } from "three/examples/jsm/controls/OrbitControls";
import { GLTFLoader } from "three/examples/jsm/loaders/GLTFLoader";
import { PLANETS } from "../constants";
import { Lensflare, LensflareElement } from "three/examples/jsm/objects/Lensflare.js";
import Options from "./Options.vue";
import PlanetCard from "./PlanetCard.vue";
import '@/sass/main.scss';
const loader = new GLTFLoader();

export default {
    data() {
        return {
            speed: 1,
            idealizedSpeed: true,
            time: 0,
            selectedPlanetCard: null,
        }
    },
    emits: ["onSceneLoad"],
    components: {
        Options,
        PlanetCard,
    },
    beforeUnmount() {
      // 停止动画循环
      if (this.renderer) {
        this.renderer.setAnimationLoop(null);
      }

      // 移除窗口resize监听
      window.onresize = null;

      // 移除canvas事件监听
      const canvas = this.$refs.canvas;
      if (canvas) {
        canvas.removeEventListener("mousemove", this.handleMouseMove);
        canvas.removeEventListener("mousedown", this.handleMouseDown);
        canvas.removeEventListener("mouseup", this.handleMouseUp);
      }

      // 销毁控制器
      if (this.controls) {
        this.controls.dispose();
      }

      // 清理渲染器
      if (this.renderer) {
        this.renderer.dispose();
        const gl = this.renderer.domElement.getContext('webgl');
        gl && gl.getExtension('WEBGL_lose_context')?.loseContext();
        this.renderer.forceContextLoss();
        this.renderer.domElement = null;
      }

      // 清理场景资源的方法
      const disposeScene = (scene) => {
        if (!scene) return;

        scene.traverse(child => {
          if (child.isMesh) {
            child.geometry.dispose();
            if (child.material) {
              if (Array.isArray(child.material)) {
                child.material.forEach(m => m.dispose());
              } else {
                child.material.dispose();
              }
            }
          }
          // 清理纹理等其他资源
          if (child.texture) child.texture.dispose();
        });
        scene.children = [];
      };

      // 清理主场景和背景场景
      disposeScene(this.scene);
      disposeScene(this.backgroundScene);

      // 释放引用
      this.scene = null;
      this.backgroundScene = null;
      this.camera = null;
      this.renderer = null;
      this.controls = null;
    },
    async mounted() {
      this.time = Date.now();

      // 保存关键引用到组件实例
      this.scene = this.createScene();
      this.backgroundScene = this.createBackgroundScene();
      this.camera = this.createCamera();
      this.renderer = this.createRenderer(this.scene, this.camera);

      this.setupLighting(this.scene);

      this.controls = this.createControls(this.camera, this.renderer);
      this.clock = new THREE.Clock();
      this.mouse = new THREE.Vector2();
      this.raycaster = new THREE.Raycaster();

      // 初始化状态相关引用
      this.hoverObject = { planet: null, outline: null };
      this.selectedPlanet = null;
      this.clickedPlanet = null;

      // 保存事件处理器引用
      this.handleMouseMove = (e) => {
        e.preventDefault();
        this.mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
        this.mouse.y = - (e.clientY / window.innerHeight) * 2 + 1;
      };

      this.handleMouseDown = (e) => {
        this.mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
        this.mouse.y = - (e.clientY / window.innerHeight) * 2 + 1;

        if (this.hoverObject.planet != null) {
          const planet = this.findMeshPlanet(this.hoverObject.planet);
          if (planet) this.clickedPlanet = planet.name;
        }
      };

      this.handleMouseUp = (e) => {
        if (!this.clickedPlanet) return;
        this.mouse.x = (e.clientX / window.innerWidth) * 2 - 1;
        this.mouse.y = - (e.clientY / window.innerHeight) * 2 + 1;

        if (this.hoverObject.planet != null) {
          const planet = this.findMeshPlanet(this.hoverObject.planet);
          if (planet.name !== this.clickedPlanet) {
            this.clickedPlanet = null;
            return;
          }
          if (planet.name === "sun") {
            this.controls.minDistance = 60;
            this.controls.maxDistance = 500;
            this.controls.target.set(0, 0, 0);
          } else {
            let box = new THREE.Box3().setFromObject(planet.children[0].children[0]);
            let diameter = Math.abs(box.max.x - box.min.x);
            this.controls.minDistance = diameter * 1.25;
            this.controls.maxDistance = diameter * 2.5;
          }
          this.selectedPlanetCard = planet.userData;
          this.selectedPlanet = planet;
          this.clickedPlanet = null;
        }
      };

      // 添加事件监听器
      this.$refs.canvas.addEventListener("mousemove", this.handleMouseMove);
      this.$refs.canvas.addEventListener("mousedown", this.handleMouseDown);
      this.$refs.canvas.addEventListener("mouseup", this.handleMouseUp);

      // 初始化太阳系
      this.planets = await this.createSolarSystem(this.scene);

      // 配置渲染循环
      this.renderer.autoClear = false;
      this.camera.layers.enable(1);

      this.renderer.setAnimationLoop(() => {
        let delta = this.clock.getDelta();
        for (let planet of this.planets) {
          planet.tick(delta);
        }

        if (this.selectedPlanet) {
          this.selectedPlanet.children[0].getWorldPosition(this.controls.target);
        }
        this.controls.update();

        this.raycaster.setFromCamera(this.mouse, this.camera);
        const intersects = this.raycaster.intersectObjects(this.planets, true);

        // Hover 处理逻辑...
        if (intersects.length > 0 && this.hoverObject.planet == null) {
          this.hoverObject.planet = intersects[0].object;
          this.hoverObject.outline = this.highlightPlanet(intersects[0].object);
        } else if (intersects.length > 0 && this.hoverObject.planet !== intersects[0].object) {
          this.unhighlightPlanet(this.hoverObject.planet);
          this.hoverObject.planet = intersects[0].object;
          this.hoverObject.outline = this.highlightPlanet(intersects[0].object);
        } else if (intersects.length === 0 && this.hoverObject.planet != null) {
          this.unhighlightPlanet(this.hoverObject.planet);
          this.hoverObject.planet = null;
          this.hoverObject.outline = null;
        }

        if (!this.idealizedSpeed) this.time += this.speed * 1000 * delta;

        this.renderer.clear();
        this.camera.layers.set(1);
        this.renderer.render(this.backgroundScene, this.camera);
        this.renderer.render(this.scene, this.camera);

        this.camera.layers.set(0);
        this.renderer.render(this.scene, this.camera);
      });

      // 窗口resize处理
      this.handleResize = () => {
        this.resizeRenderer(this.renderer);
        this.camera.aspect = window.innerWidth / window.innerHeight;
        this.camera.updateProjectionMatrix();
      };
      window.addEventListener('resize', this.handleResize);

      this.$emit('onSceneLoad');
    },
    methods: {
        // Look through list of all planets and initialize them
        createSolarSystem: async function(scene) {
            const planets = []; // List of Object3D of planets
            for(let planet of PLANETS) {
                // Load 3D model
                
                let gltf = await loader.loadAsync(`/assets/gltf/${planet.name}.glb`);
                let updateObject;
                let userData = this.getUserDataFor(planet);
                // Get the object the planet that is orbiting
                if(planet.orbitObject != null) {
                    let orbitObject = this.findOrbitObject(planets, planet.orbitObject);
                    gltf.scene.position.z = planet.scaledOrbitalRadius;
                    gltf.scene.rotation.z = THREE.MathUtils.degToRad(planet.axialTilt ?? 0);

                    // Create a pivot for orbit
                    let pivot = new THREE.Object3D();
                    pivot.name = planet.name;
                    pivot.userData = userData;
                    pivot.userData.isPivot = true;
                    pivot.add(gltf.scene);
                    pivot.rotation.x = THREE.MathUtils.degToRad(planet.orbitalInclination);

                    updateObject = pivot;

                    // Create trajectory for planet's orbit
                    const material = new THREE.MeshBasicMaterial( { color: 0xffffff } );
                    material.side = THREE.DoubleSide;
                    material.transparent = true;
                    material.opacity = 0.15;
                    let trajectory = new THREE.Mesh(new THREE.TorusGeometry(planet.scaledOrbitalRadius, 0.05, 8, 64 ), material);
                    trajectory.rotation.x = THREE.MathUtils.degToRad(90);
                    pivot.add(trajectory);

                    gltf.scene.children[0].userData.trajectory = trajectory;
                    gltf.scene.children[0].userData.canHover = true;

                    orbitObject.add(pivot);
                    planets.push(pivot);
                }
                else{
                    // This is basically only for Sun
                    let group = new THREE.Group();
                    gltf.scene.rotation.z = THREE.MathUtils.degToRad(planet.axialTilt ?? 0);
                    group.add(gltf.scene);
                    group.userData = userData;
                    gltf.scene.userData.canHover = true;
                    group.name = planet.name;

                    updateObject = group;

                    scene.add(group);
                    planets.push(group);
                }

                // Update event
                this.createUpdateLoop(updateObject);
            }

            return planets;
        },
        // Creates outline around planet and makes trajectory brighter
        highlightPlanet: function (mesh) {
            if(!mesh.parent.userData.canHover) return;
            mesh.parent.traverse(function (child) {
                if (child instanceof THREE.Mesh) {
                    child.material.emissive = new THREE.Color(0x404040);
                    child.material.emissiveIntensity = 1.31;
                }
            });

            const trajectory = mesh.parent.userData.trajectory;
            if(trajectory) {
                trajectory.material.opacity = 1;
            }

            return null;
        },
        // Removes outline from planet and makes trajectory transparent
        unhighlightPlanet: function (mesh) {
            if(!mesh?.parent.userData.canHover) return;
            mesh.parent.traverse(function (child) {
                if (child instanceof THREE.Mesh) {
                    child.material.emissive = new THREE.Color(0x000000);
                }
            });
            const trajectory = mesh.parent.userData.trajectory;
            if(trajectory) {
                trajectory.material.opacity = 0.15;
            }
        },
        // Finds the correct object to orbit in the list of planets
        findOrbitObject: function(planets, name) {
            let planet = planets.find(p => p.userData.displayName === name);
            if(planet.userData.isPivot) {
                return planet.children.find(p => !p.userData.isPivot);
            }
            return planet;
        },
        // Return the planet that contains given mesh
        findMeshPlanet: function(mesh) {
            if(mesh.userData.isPlanet) return mesh;
            return mesh.parent == null ? null : this.findMeshPlanet(mesh.parent);
        },
        // Adds tick method to planet that runs every frame 
        createUpdateLoop: function(planet) {
            planet.tick = (e) => {
                // Planet orbit around its parent
                if(planet.userData.orbitalRadius !== 0){
                    planet.userData.currentDistance += this.idealizedSpeed
                    ? Math.max((e * planet.userData.orbitalVelocity * planet.userData.orbitalRadius / 100), 6000)
                    : (planet.userData.orbitalVelocity * e) * this.speed;

                    if(planet.userData.currentDistance > planet.userData.orbitalCircumference){
                        planet.userData.currentDistance = planet.userData.currentDistance % planet.userData.orbitalCircumference
                    }

                    planet.rotation.y = planet.userData.currentDistance / planet.userData.orbitalCircumference * Math.PI * 2;
                }

                // Planet rotation around its own axis 
                planet.userData.currentRotation += this.idealizedSpeed 
                ? (planet.userData.planetCircumference * e * 0.1)
                : (planet.userData.rotationVelocity * e) * this.speed;
                let rY = planet.userData.currentRotation / planet.userData.planetCircumference * Math.PI * 2;
                // Find the Group that holds the Meshes and rotate it
                if(planet.userData.isPivot){
                    planet.children[0].children[0].rotation.y = rY;
                }
                else{
                    planet.children[0].rotation.y = rY;
                }
            };  
        },
        createScene: function() {
            const scene = new THREE.Scene();

            return scene;
        },
        // Create and configure camera and return it
        createCamera: function () { 
            const camera = new THREE.PerspectiveCamera(47, window.innerWidth / window.innerHeight, 0.1, 1000);

            return camera;
        },
        // Create a separate scene with background 
        createBackgroundScene: function() {
            const backgroundScene = new THREE.Scene();
            const loader = new THREE.CubeTextureLoader();
            const texture = loader.load([
                '/assets/universe.jpg',
                '/assets/universe.jpg',
                '/assets/universe.jpg',
                '/assets/universe.jpg',
                '/assets/universe.jpg',
                '/assets/universe.jpg',
            ]);            
            backgroundScene.background = texture;

            return backgroundScene;
        },
        // Create and configure renderer and return it 
        createRenderer: function (scene, camera) { 
            const renderer = new THREE.WebGLRenderer({
                powerPreference: "high-performance",
                canvas: this.$refs.canvas,
                antialias: true,
                alpha: true,
            });
            renderer.setClearColor( 0x000000, 0 );

            this.resizeRenderer(renderer);

            renderer.autoClearColor = false;
            renderer.outputEncoding = THREE.LinearEncoding;
            renderer.render(scene, camera);

            return renderer;
        },
        // Create and configure controls and return it 
        createControls: function (camera, renderer) {
            const controls = new OrbitControls(camera, renderer.domElement);
            controls.autoRotate = false;
            controls.enableDamping = true;
            controls.dampingFactor = 0.1;
            controls.enablePan = false;
            controls.minDistance = 60;
            controls.maxDistance = 500;
            controls.object.rotation.x = -0.841;
            controls.object.rotation.y = 0.528;
            controls.object.rotation.z = 0.513;
            controls.object.position.x = 98.467;
            controls.object.position.y = 125.67;
            controls.object.position.z = 112.32;

            return controls;
        },
        setupLighting: function (scene) {
            const ambientLight = new THREE.AmbientLight(0xffffff, 0.2);
            scene.add(ambientLight);

            // Light from the Sun
            const pointLight = new THREE.PointLight(0xFFA500, 150, 300);
            scene.add(pointLight);

            const textureLoader = new THREE.TextureLoader();

            const textureFlare0 = textureLoader.load( "/assets/textures/lensflare0.png" );
            const textureFlare1 = textureLoader.load( "/assets/textures/lensflare1.png" );

            const lensflare = new Lensflare();
            lensflare.layers.enable(1);
            lensflare.addElement( new LensflareElement(textureFlare0, 100));
            lensflare.addElement( new LensflareElement(textureFlare1, 40));
            pointLight.add(lensflare);

            // Lights used to brighten up the sun
            const rectLight1 = new THREE.RectAreaLight(0xffffff, 7, 20, 25);
            rectLight1.position.set(-12, 0, 0);
            rectLight1.lookAt(0, 0, 0)
            scene.add(rectLight1);

            const rectLight2 = new THREE.RectAreaLight(0xffffff, 7, 20, 25);
            rectLight2.position.set(12, 0, 0);
            rectLight2.lookAt(0, 0, 0)
            scene.add(rectLight2);

            const rectLight3 = new THREE.RectAreaLight(0xffffff, 7, 20, 20);
            rectLight3.position.set(0, 10, 12);
            rectLight3.lookAt(0, 0, 0)
            scene.add(rectLight3);

            const rectLight4 = new THREE.RectAreaLight(0xffffff, 7, 20, 20);
            rectLight4.position.set(0, 10, -12);
            rectLight4.lookAt(0, 0, 0)
            scene.add(rectLight4);

            const rectLight5 = new THREE.RectAreaLight(0xffffff, 7, 20, 20);
            rectLight5.position.set(0, -10, 12);
            rectLight5.lookAt(0, 0, 0)
            scene.add(rectLight5);

            const rectLight6 = new THREE.RectAreaLight(0xffffff, 7, 20, 20);
            rectLight6.position.set(0, -10, -12);
            rectLight6.lookAt(0, 0, 0)
            scene.add(rectLight6);

            // Directional lights used to get better shading
            const dirLight1 = new THREE.DirectionalLight(0xffffff, 0.1);
            dirLight1.position.set(-250, 15, 0);
            dirLight1.lookAt(0, 0, 0);
            scene.add(dirLight1);
            
            const dirLight2 = new THREE.DirectionalLight(0xffffff, 0.1);
            dirLight2.position.set(250, 15, 0);
            dirLight2.lookAt(0, 0, 0);
            scene.add(dirLight2);
            
            const dirLight3 = new THREE.DirectionalLight(0xffffff, 0.1);
            dirLight3.position.set(0, 15, -250);
            dirLight3.lookAt(0, 0, 0);
            scene.add(dirLight3);
            
            const dirLight4 = new THREE.DirectionalLight(0xffffff, 0.1);
            dirLight4.position.set(0, 15, 250);
            dirLight4.lookAt(0, 0, 0);
            scene.add(dirLight4);
        },
        // Set's the renderers size to current window size
        resizeRenderer: function (renderer) { 
            renderer.setPixelRatio(window.devicePixelRatio);
            renderer.setSize(window.innerWidth, window.innerHeight);
        },
        // Event that gets called when speed option changed
        onSpeedChange(value) {
            this.idealizedSpeed = false;
            switch(value) {
                case "realtime":
                    this.speed = 1;
                    break;
                case "day_sec": 
                    this.speed = 86400;
                    break;
                case "mon_sec":
                    this.speed = 2419200;
                    break;
                case "idealized":
                    this.idealizedSpeed = true;
                    break;
            }
        },
        getUserDataFor(planet) {
            return {
                name: planet.name,
                displayName: planet.displayName,
                caption: planet.caption,
                description: planet.description,
                year: planet.year,
                day: planet.day,
                distanceFromSun: planet.distanceFromSun,
                distance: planet.distance,
                moons: planet.moons,
                meanTemp: planet.meanTemp,
                minTemp: planet.minTemp,
                maxTemp: planet.maxTemp,
                timesLarger: planet.timesLarger,
                orbitObject: planet.orbitObject,
                isPlanet: true,
                orbitalVelocity: planet.orbitalVelocity,
                orbitalRadius: planet.orbitalRadius,
                currentDistance: 2 * Math.PI * planet.orbitalRadius * Math.random(),
                currentRotation: 0,
                planetCircumference: 2 * Math.PI * planet.radius,
                orbitalCircumference: 2 * Math.PI * planet.orbitalRadius,
                scaledOrbitalRadius: planet.scaledOrbitalRadius,
                isPivot: false,
                radius: planet.radius,
                rotationVelocity: planet.rotationVelocity,
            };
        },
    },
    computed: {
        date() {
            const date = new Date(this.time);
            const result = `${("0" + date.getDate()).slice(-2)}. ${("0" + (date.getMonth() + 1).toString()).slice(-2)}. ${date.getFullYear()}`;

            return result;
        }
    },
}
</script>

<style scoped lang="scss">
    canvas{
        width: 100vw;
        height: 100vh;
    }
    .date-display {
        position: absolute;
        top: 10%;
        left: 0;
        padding: 1em;
        display: flex;
        gap: 8px;
        color: #f2f6ff;
        &.disabled{
            opacity: 0.2;
        }
    }
    @media (max-width: 560px) {
        .date-display {
            top: 16px;
        }
    }
</style>