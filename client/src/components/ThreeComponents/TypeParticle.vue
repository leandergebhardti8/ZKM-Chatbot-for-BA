<template></template>

<script>
import * as THREE from "three";
import GeometryUtils from "../../assets/libs/GeometryUtils";
import { morphTo } from "../../helpers";

export default {
  name: "Type",
  props: {
    particleSystem: {
      type: Object || undefined,
      default: undefined
    },
    maxParticles: {
      type: Number,
      default: 2000
    },
    text: {
      type: String || undefined,
      default: undefined
    },
    size: {
      type: Number,
      default: 1
    }
  },
  mounted() {
    if (this.particleSystem) this.generateText(this.particleSystem);
  },
  watch: {
    text(newValue) {
      if (!newValue || !this.particleSystem) return;
      this.generateText(this.particleSystem);
    },
    size(newValue) {
      if (!newValue || !this.particleSystem) return;
      this.generateText(this.particleSystem);
    },
  },
  methods: {
    createVertices(points) {
      const color_list = ['#ffffff', '#FF53AF', '#70CDB3', '#009EF9'];
      let v = new THREE.Geometry();
      for (var p = 0; p < this.maxParticles; p++) {
        var vertex = new THREE.Vector3();
        vertex.x = points[p]["x"];
        vertex.y = points[p]["y"];
        vertex.z = points[p]["z"];
        v.vertices.push(vertex); 
        v.colors.push(new THREE.Color(color_list[Math.floor(Math.random() * color_list.length)]));
      }
      return v;
    },
    generateText(particleSystem) {
      var loader = new THREE.FontLoader();
      var typeface =
        "https://dl.dropboxusercontent.com/s/bkqic142ik0zjed/swiss_black_cond.json?";

      loader.load(typeface, async font => {
        let fontGeo = {};

        fontGeo.geometry = new THREE.TextGeometry(this.text, {
          font: font,
          size: this.size * 10,
          height: 0.1,
          curveSegments: 100
        });

        fontGeo.geometry.center();

        fontGeo.points = GeometryUtils.randomPointsInGeometry(
          fontGeo.geometry,
          this.maxParticles
        );
        fontGeo.particles = await this.createVertices(fontGeo.points);
        morphTo(particleSystem, fontGeo.particles);
      });
    }
  }
};
</script>

<style lang="sass" scoped>
</style>