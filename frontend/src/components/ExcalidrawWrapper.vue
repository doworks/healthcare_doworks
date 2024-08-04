<template>
  <div id="reactContainer" class="h-100">
    <!-- render react component in here -->
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { ExcalidrawConnector } from './react/ExcalidrawConnector';

onMounted(() => {
  const reactComponent = new ExcalidrawConnector(document.getElementById('reactContainer')!);
  reactComponent.render();
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
/* .excalidraw-wrapper.leftdrawer-open .layer-ui__wrapper__footer-left{
  padding-left: 240px
} */

.v-overlay__content{
  overflow-x: hidden;
}
</style>