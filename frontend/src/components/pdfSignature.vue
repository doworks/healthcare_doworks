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
      signaturePad: null,
      signatureCanvasStyle: {
        position: 'absolute',
        border: '1px solid #ccc',
        display: 'none', // Initially hide the canvas
        top: '0px',
        left: '0px',
        width: '0px',
        height: '0px',
      },
    };
  },
  mounted() {
    this.initSignaturePad();
    this.positionSignatureCanvas();

    // Add event listeners
    window.addEventListener('resize', this.positionSignatureCanvas);

    // Observe mutations in the htmlContent
    this.observer = new MutationObserver(() => {
      this.positionSignatureCanvas();
    });

    this.observer.observe(this.$refs.htmlContent, {
      childList: true,
      subtree: true,
      attributes: true,
      characterData: true,
    });
  },
  beforeDestroy() {
    window.removeEventListener('resize', this.positionSignatureCanvas);
    if (this.observer) {
      this.observer.disconnect();
    }
  },
  watch: {
    html(newValue, oldValue) {
      // Wait for the DOM to update with the new HTML content
      this.$nextTick(() => {
        this.positionSignatureCanvas();
      });
    },
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
          const signatureAreaRect = signatureArea.getBoundingClientRect();
          const containerRect = this.$refs.htmlContent.getBoundingClientRect();

          // Calculate the position relative to the container
          const top = signatureAreaRect.top - containerRect.top + this.$refs.htmlContent.scrollTop;
          const left = signatureAreaRect.left - containerRect.left + this.$refs.htmlContent.scrollLeft;
          const width = signatureAreaRect.width;
          const height = signatureAreaRect.height;

          // Update the style of the canvas
          this.signatureCanvasStyle.top = `${top}px`;
          this.signatureCanvasStyle.left = `${left}px`;
          this.signatureCanvasStyle.width = `${width}px`;
          this.signatureCanvasStyle.height = `${height}px`;
          this.signatureCanvasStyle.display = 'block'; // Show the canvas

          // Set the canvas dimensions to match the signature area
          const canvas = this.$refs.signatureCanvas;
          canvas.width = width;
          canvas.height = height;

          // Reinitialize the signature pad with the new dimensions
          if (this.signaturePad) {
            this.signaturePad.clear();
            this.signaturePad.off();
            this.signaturePad = new SignaturePad(canvas, {
              backgroundColor: 'rgba(255, 255, 255, 0)',
              penColor: 'black',
            });
          }
        } else {
          // Hide the canvas if signature area is not found
          this.signatureCanvasStyle.display = 'none';
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
      return dataUrl;
      // Example: send the dataUrl to your server or do further processing
    },
  },
};
</script>

<style>
#print-html .action-banner {
  display: none;
}
</style>
