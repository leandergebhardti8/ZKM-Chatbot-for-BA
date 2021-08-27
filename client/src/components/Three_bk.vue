<template>
	<div>
		<div id="container"></div>
	</div>
</template>

<script>
/* eslint-disable no-param-reassign */
// eslint-disable-next-line no-unused-vars
import '@/assets/libs/Detector';
const THREE = require('three');
export default {
	name: 'HelloWorld',
	props: {},
	data() {
		return {
			container: undefined,
			player: {},
			stats: undefined,
			controls: undefined,
			camera: undefined,
			scene: undefined,
			renderer: undefined,
			clock: undefined,
            animations: {},
            distance: 100,
            sphere: undefined,
            elapsed: 0,
            maxParticles: 10000,
            sphereGeometry: undefined
		};
	},
	mounted() {
		this.container = document.getElementById('container');
        this.init();
	},
	methods: {
		init() {
            this.scene = new THREE.Scene();
			this.camera = new THREE.PerspectiveCamera(
				45,
				container.offsetWidth / container.offsetHeight,
				1,
				1000
			);
            this.camera.position.set(0, 0, 200);
            
            this.camera.lookAt(this.scene.position);
            this.scene.add(this.camera);
            const game = this;
            this.sphereGeometry = new THREE.Geometry();
            let spherical = new THREE.Spherical();
            for (let i = 0; i < this.maxParticles; i++) {
                this.sphereGeometry.vertices.push(this.setRandomPointInSphere(50)); // 10 is the desired radius
            }
            console.log("vertices lenght", this.sphereGeometry.vertices.length);
            var material = new THREE.PointsMaterial({
            color: 0xffffff,
            size: 1
            });
            this.sphere = new THREE.Points(this.sphereGeometry, material);
            this.scene.add(this.sphere);

			// render
			this.renderer = new THREE.WebGLRenderer({ alpha: true });
			this.renderer.setClearColor(0xffffff, 0);
			this.renderer.setPixelRatio(window.devicePixelRatio);
			this.renderer.setSize(container.offsetWidth, container.offsetHeight);
			// this.renderer.shadowMap.enabled = true;
			this.container.appendChild(this.renderer.domElement);
			game.animate();
        },
        setRandomPointInSphere(radius) {
            const v = new THREE.Vector3();
            const x = THREE.Math.randFloat( -1, 1 );
            const y = THREE.Math.randFloat( -1, 1 );
            const z = THREE.Math.randFloat( -1, 1 );
            const normalizationFactor = 1 / Math.sqrt( x * x + y * y + z * z );
            v.x = x * normalizationFactor * (radius + THREE.Math.randFloat( -10, 10 ));
            v.y = y * normalizationFactor * (radius + THREE.Math.randFloat( -10, 10 ));
            v.z = z * normalizationFactor * (radius + THREE.Math.randFloat( -10, 10 ));
            return v;
        },
		onWindowResize() {
			this.camera.aspect = container.offsetWidth / container.offsetHeight;
			this.camera.updateProjectionMatrix();
			this.renderer.setSize(container.offsetWidth, container.offsetHeight);
        },
        update() {
            this.elapsed += 0.005;
           // this.sphere.rotation.x = this.elapsed;
            //this.sphere.rotation.y = this.elapsed;
            //this.sphere.rotation.z = this.elapsed;
            this.renderer.setClearColor(0xffffff, 0);
            this.renderer.render(this.scene, this.camera);
            this.onWindowResize();
        },
		animate() {
			const game = this;
            this.update();
			requestAnimationFrame(() => {
				game.animate();
            });
		}
	}
};
</script>

<style scoped lang="scss">
#app{ 
    #container {
        width: 100%;
        height: 100%;
        display: block;
        margin: auto;
        z-index: 12;
    }
}
</style>
