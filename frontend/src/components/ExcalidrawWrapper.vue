<template>
  <div id="reactContainer" class="h-100">
    <!-- render react component in here -->
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onBeforeUnmount } from 'vue';
import { ExcalidrawConnector } from './react/ExcalidrawConnector';

const reactComponentRef = ref<ExcalidrawConnector | null>(null);

onMounted(() => {
  reactComponentRef.value = new ExcalidrawConnector(document.getElementById('reactContainer')!);
  reactComponentRef.value.render();
});

onBeforeUnmount(() => {
  if (reactComponentRef.value) {
    reactComponentRef.value.unmount(); // Unmount the React component
  }
});
</script>

<style scoped>
.h-100 {
  height: 100%;
}
</style>

<style>
.excalidraw .drawings-sidebar {
  border: 0 !important;
}
.excalidraw [title="Library"], .layer-ui__wrapper__footer-right, .dropdown-menu-button{
  display: none !important;
}
.excalidraw-wrapper .App-menu_top__left,.layer-ui__wrapper__footer-left{
  padding-left: 0
}
.excalidraw-wrapper .shapes-section{
  padding-left: 295px
}
.excalidraw-wrapper.leftdrawer-open .App-menu_top__left{
  padding-left: 240px
}
.excalidraw-wrapper .layer-ui__wrapper__footer .footer-center{
  justify-content: center;
}
/* .excalidraw-wrapper.leftdrawer-open .layer-ui__wrapper__footer-left{
  padding-left: 240px
} */

.v-overlay__content{
  overflow-x: hidden;
}
</style>