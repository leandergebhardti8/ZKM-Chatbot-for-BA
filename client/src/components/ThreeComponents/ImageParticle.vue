<template>
  <canvas ref="imageCanvas" style="display: none;"></canvas>
</template>

<script>
import * as THREE from "three";
import GeometryUtils from "../../assets/libs/GeometryUtils";
import { morphTo } from "../../helpers";
export default {
  name: "ImageParticle",
  props: {
    particleSystem: {
      type: Object || undefined,
      default: undefined
    },
    maxParticles: {
      type: Number,
      default: 1000
    },
    imageSource: {
      type: String || undefined,
      default: undefined
    },
    size: {
      type: Number,
      default: 1.45
    }
  },
  mounted() {
    this.onLoadImageHandler(this.imageSource);
  },
  watch: {
    size(newValue) {
      this.onLoadImageHandler(this.imageSource);
    },
    imageSource(newValue) {
      this.onLoadImageHandler(this.imageSource);
    },
  },
  methods: {
    loadImage(src) {
      return new Promise((resolve, reject) => {
        let img = new Image();
        img.crossOrigin = "Anonymous";
        img.onload = () => resolve(img);
        img.onerror = reject;
        img.src = src;
      });
    },
    async onLoadImageHandler(imgaeSrc, number) {
      const canvas = this.$refs["imageCanvas"];
      const ctx = canvas.getContext("2d");
      const image = await this.loadImage(imgaeSrc);
      const size = image.width;
      canvas.width = image.width;
      canvas.height = image.height;

      ctx.drawImage(image, 0, 0);
      let imageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
      let data = imageData.data;
      const target = [];
      const targetGeometry = new THREE.Geometry();

      for (let i = 0; i < data.length; i++) {
        if (data[i] == 0) {
          let pixNumber = i / 4;
          let xPos = pixNumber % size;
          let yPos = parseInt(pixNumber / size);
          let pos = { x: xPos / size - 0.5, y: -yPos / size + 1 };

          target.push(pos);
        }
      }
      for (let i = 0; i < this.maxParticles; i++) {
        let ii = Math.round((i * target.length) / this.maxParticles);
        let geoPos = new THREE.Vector3(
         (target[ii].x * 50 + Math.random(2)) * this.size,
         (target[ii].y * 50 + Math.random(2) - 25) * this.size,
          Math.random(5) - 2.5
        );
        targetGeometry.vertices.push(geoPos);
        // targetGeometry.colors.push(new THREE.Color(this.colorList[Math.floor(Math.random() * this.colorList.length)]));
     //   target[i].size = 1 + 1 * Math.sin(10 * i + this.elapsed * 10);
     //  container.offsetWidth/30 + container.offsetWidth/30 * Math.sin(1 * i + this.elapsed * 5);
      }
      morphTo(this.particleSystem, targetGeometry);
    }
  }
};
</script>

<style lang="sass" scoped>
</style>