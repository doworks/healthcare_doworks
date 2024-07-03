<template>
    <div class="modal">
      <div class="modal-content">
        <span class="close" @click="$emit('close')">&times;</span>
        <h2>Annotate Tooth {{ tooth.id }}</h2>
        <form @submit.prevent="submitAnnotation">
          <label for="problem">Problem:</label>
          <input type="text" v-model="annotation.problem" id="problem" />
          <label for="severity">Severity:</label>
          <input type="text" v-model="annotation.severity" id="severity" />
          <button type="submit">Save</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    props: ['tooth'],
    data() {
      return {
        annotation: {
          problem: '',
          severity: '',
        },
      };
    },
    methods: {
      submitAnnotation() {
        // Emit the annotation data to the parent component
        this.$emit('save-annotation', { toothId: this.tooth.id, ...this.annotation });
        this.$emit('close');
      },
    },
  };
  </script>
  
  <style>
  .modal {
    display: block; /* Show the modal */
    position: fixed;
    z-index: 1;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    overflow: auto;
    background-color: rgb(0, 0, 0);
    background-color: rgba(0, 0, 0, 0.4);
  }
  
  .modal-content {
    background-color: #fefefe;
    margin: 15% auto;
    padding: 20px;
    border: 1px solid #888;
    width: 80%;
  }
  
  .close {
    color: #aaa;
    float: right;
    font-size: 28px;
    font-weight: bold;
  }
  
  .close:hover,
  .close:focus {
    color: black;
    text-decoration: none;
    cursor: pointer;
  }
  </style>