<template>
  <div ref="canvasContainer" class="canvas-container" @click="onMouseClick"></div>
</template>

<script>
import * as THREE from 'three';

export default {
  name: 'DentalChart',
  data() {
    return {
      scene: null,
      camera: null,
      renderer: null,
      mesh: null,
      raycaster: new THREE.Raycaster(),
      mouse: new THREE.Vector2(),
    };
  },
  mounted() {
    this.initThree();
  },
  methods: {
    initThree() {
      // Create the scene
      this.scene = new THREE.Scene();
      
      // Set up the camera
      this.camera = new THREE.PerspectiveCamera(
        75,
        this.$refs.canvasContainer.clientWidth / this.$refs.canvasContainer.clientHeight,
        0.1,
        1000
      );
      this.camera.position.z = 5;
      
      // Set up the renderer
      this.renderer = new THREE.WebGLRenderer();
      this.renderer.setSize(this.$refs.canvasContainer.clientWidth, this.$refs.canvasContainer.clientHeight);
      this.$refs.canvasContainer.appendChild(this.renderer.domElement);
      
      // Add a simple cube to the scene
      const geometry = new THREE.BoxGeometry();
      const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
      this.mesh = new THREE.Mesh(geometry, material);
      this.scene.add(this.mesh);
      
      // Start the animation loop
      this.animate();
    },
    animate() {
      requestAnimationFrame(this.animate);
      this.mesh.rotation.x += 0.01;
      this.mesh.rotation.y += 0.01;
      this.renderer.render(this.scene, this.camera);
    },
    onMouseClick(event) {
      // Calculate mouse position in normalized device coordinates (-1 to +1)
      this.mouse.x = (event.clientX / this.$refs.canvasContainer.clientWidth) * 2 - 1;
      this.mouse.y = -(event.clientY / this.$refs.canvasContainer.clientHeight) * 2 + 1;
      
      // Update the raycaster
      this.raycaster.setFromCamera(this.mouse, this.camera);
      
      // Calculate objects intersecting the picking ray
      const intersects = this.raycaster.intersectObjects(this.scene.children);
      
      if (intersects.length > 0) {
        // Change the color of the intersected object
        intersects[0].object.material.color.set(0xff0000);
        alert('Tooth clicked!');
      }
    },
  },
};
</script>

<style>
.canvas-container {
  width: 100%;
  height: 100vh;
}
</style>