<template>
  <div class="loading-container">
    <img :src="gifSrc" alt="Loading..." />
  </div>
</template>

<script>
export default {
  name: "GifLoader",
  props: {
    gifSrc: {
      type: String,
      required: true,
    },
  },
};
</script>

<style scoped>
.loading-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 90vh; /* Full screen height */
}
</style>