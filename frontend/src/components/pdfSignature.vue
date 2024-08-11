<template>
  <div id="print-html" style="position: relative;">
    <!-- Render the HTML content dynamically -->
    <div ref="htmlContent" v-html="html"></div>

    <!-- Signature pad overlay -->
    <canvas
      ref="signatureCanvas"
      :style="signatureCanvasStyle"
    ></canvas>
  </div>
  <button @click="clearSignature">Clear Signature</button>
  <button @click="saveSignature">Save Signature</button>
</template>
  
<script>
import SignaturePad from 'signature_pad';

export default {
  props: {
    html: {
      type: String,
      required: true,
      default: '',
    },
  },
  data() {
    return {
      htmlContent: `
        <div>
          <h1>Document Title</h1>
          <p>This is a sample document content.</p>
          <p>Please sign below:</p>
          <div style="border: 1px dashed #ccc; width: 200px; height: 50px; margin-top: 20px;"></div>
        </div>
      `,
      signaturePad: null,
      signatureCanvasStyle: {
        position: 'absolute',
        border: '1px solid #ccc',
        display: 'none', // Initially hide the canvas
        top: '300px',
        left: '150px',
      },
    };
  },
  mounted() {
    this.initSignaturePad();
    this.positionSignatureCanvas();
  },
  methods: {
    initSignaturePad() {
      const canvas = this.$refs.signatureCanvas;
      this.signaturePad = new SignaturePad(canvas, {
        backgroundColor: 'rgba(255, 255, 255, 0)',
        penColor: 'black',
      });
    },
    positionSignatureCanvas() {
      // Wait for the DOM to update before accessing the signature-area
      this.$nextTick(() => {
        const signatureArea = this.$refs.htmlContent.querySelector('.signature-area');
        if (signatureArea) {
          const { top, left, width, height } = signatureArea.getBoundingClientRect();
          const containerOffset = this.$refs.htmlContent.getBoundingClientRect();
          
          // Position the canvas over the signature area
          this.signatureCanvasStyle.top = `${top - containerOffset.top}px`;
          this.signatureCanvasStyle.left = `${left - containerOffset.left}px`;
          this.signatureCanvasStyle.width = `${width}px`;
          this.signatureCanvasStyle.height = `${height}px`;
          this.signatureCanvasStyle.display = 'block'; // Show the canvas

          // Set the canvas dimensions to match the signature area
          const canvas = this.$refs.signatureCanvas;
          canvas.width = width;
          canvas.height = height;
        }
      });
    },
    clearSignature() {
      this.signaturePad.clear();
    },
    saveSignature() {
      if (this.signaturePad.isEmpty()) {
        alert("Please provide a signature first.");
        return;
      }
      const dataUrl = this.signaturePad.toDataURL(); // Save this data URL to your server
      return dataUrl
      // Example: send the dataUrl to your server or do further processing
    },
  },
};
</script>

<style>
#print-html .action-banner{
  display: none
}
</style>