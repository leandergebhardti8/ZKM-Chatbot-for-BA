<template>
  <div id="container">
    <ImageParticle
      v-if="sphereTextContent != '' && particleSystem && getIcon"
      :particleSystem="particleSystem"
      :maxParticles="maxParticles"
      :imageSource="getIcon && getIconImageContent"
      :sphereColor="sphereColor"
    />
    <TypeParticle
      v-else-if="sphereTextContent.length > 0 && particleSystem"
      :text="sphereTextContent"
      :particleSystem="particleSystem"
      :maxParticles="maxParticles"
      :sphereColor="sphereColor"
      :size="3"
    />
    <SphereParticle
      v-if="particleSystem"
      :particleSystem="particleSystem"
      :maxParticles="maxParticles"
      :sphereColor="sphereColor"
      :sphereTextContent="sphereTextContent"
    />
  </div>
</template>

<script>
/* eslint-disable no-param-reassign */
// eslint-disable-next-line no-unused-vars
import * as THREE from "three";
import gsap, { random } from "gsap";
import { GeometryUtils } from "three/examples/jsm/utils/GeometryUtils";
import { mapGetters, mapState } from "vuex";
import TypeParticle from "./ThreeComponents/TypeParticle";
import SphereParticle from "./ThreeComponents/SphereParticle";
import ImageParticle from "./ThreeComponents/ImageParticle";
import {_vertexShader, _fragmentShader} from './ThreeComponents/shaders';
import { changeColorTo } from "../helpers";

export default {
  name: "Three",
  props: {},
  data() {
    return {
      camera: undefined,
      scene: undefined,
      renderer: undefined,
      particleSystem: undefined,
      elapsed: 0,
      maxParticles: 1000
    };
  },
  components: {
    TypeParticle,
    SphereParticle,
    ImageParticle
  },
  computed: {
    ...mapState(["sphereTextContent", "sphereColor"]),
    ...mapGetters(["getIcon", "getIconImageContent"])
  },
  mounted() {
    // window.addEventListener('resize', this.onWindowResize, false);
    this.init(); 
  },
  destroyed() {
		// window.removeEventListener('resize', this.onWindowResize);
  },
  watch: {
    sphereColor(newValue, oldValue) {
      if (newValue === oldValue) return;
      changeColorTo(this.particleSystem, newValue);
    },
  },
  methods: {
    init() {
      const container = document.getElementById("container");
      this.scene = new THREE.Scene();
      this.camera = new THREE.PerspectiveCamera(
        35,
        container.offsetWidth / container.offsetHeight,
        1,
        1000
      );
      this.camera.position.set(0, 0, 200);

      this.camera.lookAt(this.scene.position);
      this.scene.add(this.camera);

      //Setup Geometry for shader
      var positions = new Float32Array(this.maxParticles * 3);
      var colors = new Float32Array(this.maxParticles * 3);
      var sizes = new Float32Array(this.maxParticles);

      const geometry = new THREE.BufferGeometry();
      geometry.setAttribute(
        "position",
        new THREE.BufferAttribute(positions, 3)
      );
      geometry.setAttribute(
        "customColor",
        new THREE.BufferAttribute(colors, 3)
      );
      geometry.setAttribute("size", new THREE.BufferAttribute(sizes, 1));
      var material = new THREE.ShaderMaterial({
        uniforms: {
          color: {
            value: new THREE.Color('#ffffff')
          },
          pointTexture: {
            value: new THREE.TextureLoader().load(
              require("../assets/img/spark.png")
            )
          }
        },
        vertexShader: _vertexShader,
        fragmentShader: _fragmentShader,

        blending: THREE.AdditiveBlending,
        depthTest: false,
        transparent: true
      });

      this.particleSystem = new THREE.Points(geometry, material);
      this.scene.add(this.particleSystem);
      // render
      this.renderer = new THREE.WebGLRenderer({ alpha: true });
      this.renderer.setClearColor(0xffffff, 0);
      // this.renderer.setPixelRatio(window.devicePixelRatio);
      this.renderer.setSize(
        container.offsetWidth,
        container.offsetHeight
      );
      // this.renderer.shadowMap.enabled = true;
      container.appendChild(this.renderer.domElement);
      this.animate();
    },

    onWindowResize() {
      const container = document.getElementById("container");
      this.camera.aspect = container.offsetWidth / container.offsetHeight;
      this.camera.updateProjectionMatrix();
      this.renderer.setSize(container.offsetWidth, container.offsetHeight);
    },

    animate() {
      const vm = this;
      const container = document.getElementById("container");
      this.particleSystem.geometry.verticesNeedUpdate = true;
      this.particleSystem.geometry.colorsNeedUpdate = true;
      this.elapsed += 0.005;
      //   this.particleSystem.rotation.x = this.elapsed;
      //   this.particleSystem.rotation.y = this.elapsed;

      const attributes = this.particleSystem.geometry.attributes;
      for (let i = 0; i < attributes.size.array.length; i++) {
        attributes.size.array[i] =
          // container.offsetHeight/40 + container.offsetHeight/40 * Math.sin(1 * i + this.elapsed * 15);
          4 + 3 * Math.sin(1 * i + this.elapsed * 15);
      }
      attributes.size.needsUpdate = true;
      attributes.position.needsUpdate = true;
      attributes.customColor.needsUpdate = true;
      //     this.particleSystem.rotation.z = this.elapsed;
      //    this.particleSystem.material.size = Math.random()* (2) + 0.5;
      this.renderer.setClearColor(0xffffff, 0);
      this.renderer.render(this.scene, this.camera);

      this.onWindowResize();
      requestAnimationFrame(() => {
        vm.animate();
      });
    },

    // slowDown () {
    //     TimelineLite.to(animationVars, 0.3, {ease:
    //     Power2.easeOut, speed: normalSpeed, delay: 0.2});
    // },

    morphSize(newParticles, size = 1) {
      this.particleSystem.material.size = size;
    }
  }
};
</script>

<style scoped lang="scss">
  #container {
    width: 100%;
    height: 98%;
    display: block;
    margin: auto;
    z-index: 12;
  }

</style>