<template></template>

<script>
import * as THREE from "three";
import { changeColorTo, morphTo } from "../../helpers";

export default {
  name: "SphereParticle",
  props: ["particleSystem", "maxParticles", "sphereColor","sphereTextContent"],
  data() {
    return {
      sphereParticles: undefined,
      colorList: ["#ffffff", "#FF53AF", "#70CDB3", "#009EF9"]
    };
  },
  mounted() {
    this.sphereParticles = new THREE.Geometry();
    for (let i = 0; i < this.maxParticles; i++) {
      this.sphereParticles.vertices.push(this.setRandomPointInSphere());
    }
    changeColorTo(this.particleSystem, this.sphereColor);
    morphTo(this.particleSystem, this.sphereParticles);
  },
  watch: {
    // sphereColor(newValue, oldValue) {
    //   if (newValue === oldValue) return;
    //   if (!newValue) {
    //     for (let i = 0; i < this.maxParticles; i++) {
    //       this.sphereParticles.colors[i] = new THREE.Color(
    //         this.colorList[Math.floor(Math.random() * this.colorList.length)]
    //       );
    //     }
    //     morphTo(this.particleSystem, this.sphereParticles, newValue);
    //   } else {
    //     const color = this.hexToRgb(this.sphereColor);
    //     for (let i = 0; i < this.maxParticles; i++) {
    //       this.sphereParticles.colors[i] = new THREE.Color(color);
    //     }
    //     morphTo(this.particleSystem, this.sphereParticles, newValue);
    //   }
    // },
    sphereTextContent(newValue, oldValue){
      if (newValue === oldValue) return;
      if(newValue==0&&oldValue!=0){
        this.sphereParticles = new THREE.Geometry();
        for (let i = 0; i < this.maxParticles; i++) {
          this.sphereParticles.vertices.push(this.setRandomPointInSphere());
        }
        morphTo(this.particleSystem, this.sphereParticles);
      }
    }
  },
  methods: {
    hexToRgb(hex) {
      if (typeof hex === "string" && hex.length > 1) {
        var result = /([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(
          hex.replace("0x", "").replace("#", "")
        );
        return result
          ? `rgb(${parseInt(result[1], 16)}, ${parseInt(
              result[2],
              16
            )}, ${parseInt(result[3], 16)})`
          : hex;
      }
    },
    setRandomPointInSphere() {
      let v = new THREE.Vector3(
        Math.random() - 0.5,
        Math.random() - 0.5,
        Math.random() - 0.5
      ).normalize();
      var radius3 = Math.random() * 50 + 1;
      v = v.multiplyScalar(radius3);
      /* Below is sphere surface, above is filled sphere */

      /*    const x = THREE.Math.randFloat( -1, 1 );
            const y = THREE.Math.randFloat( -1, 1 );
            const z = THREE.Math.randFloat( -1, 1 );*/

      /*   const normalizationFactor = 1 / Math.sqrt( x * x + y * y + z * z );
            v.x = x * normalizationFactor * (radius + THREE.Math.randFloat( -10, 10 ));
            v.y = y * normalizationFactor * (radius + THREE.Math.randFloat( -10, 10 ));
            v.z = z * normalizationFactor * (radius + THREE.Math.randFloat( -10, 10 ));*/
      return v;
    }
  }
};
</script>

<style lang="scss" scoped>
</style>