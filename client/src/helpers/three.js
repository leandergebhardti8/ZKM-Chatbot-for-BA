import gsap from 'gsap';
import * as THREE from 'three';

export const morphTo = (particleSystem, newParticles) => {
  const particleGeometry = particleSystem.geometry;
  const countLength = particleGeometry.attributes.position.count;

  var positions = new Float32Array(countLength * 3);
  var colors = new Float32Array(countLength * 3);
  for (let i = 0; i < countLength; i++) {
    newParticles.vertices[i].toArray(positions, i * 3);
    if (newParticles.colors[i]) newParticles.colors[i].toArray(colors, i * 3);
  }

  gsap.to(particleGeometry.attributes.position.array, positions);
  // gsap.to(particleGeometry.attributes.customColor.array, colors);
};

export const changeColorTo = (particleSystem, color) => {
  const particleGeometry = particleSystem.geometry;
  const countLength = particleGeometry.attributes.position.count;
  console.log('COLOR: ' + color);
  var colors = (colors = new Float32Array(countLength * 3));
  if (!color) {
    console.log('NO COLOR');
    const colorList = [
      new THREE.Color('#ffffff'),
      new THREE.Color('#FF53AF'),
      new THREE.Color('#70CDB3'),
      new THREE.Color('#009EF9'),
    ];
    for (var i = 0; i < countLength; i++) {
      const randomColor = Math.floor(Math.random() * colorList.length);
      colorList[randomColor].toArray(colors, i * 3);
    }
  } else {
    var colorRgb = new THREE.Color(color);
    for (var i = 0; i < countLength; i++) {
      colorRgb.toArray(colors, i * 3);
    }
  }
  gsap.to(particleGeometry.attributes.customColor.array, colors);
};
