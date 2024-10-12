<template>
  <Card class="p-0 mb-3 border-bottom-title" id="attachments" style="overflow: hidden;">
    <template #title>
      Attachments
      <v-btn class="float-end text-orange text-none" prepend-icon="pi pi-plus" variant="plain" @click="triggerFileInput">Add</v-btn>
    </template>
    <template #content>
      <v-file-input
        ref="fileInput"
        accept=".pdf,.doc,.docx,.jpg,.jpeg,.png"
        hidden
        @change="handleFileUpload"
        multiple
      ></v-file-input>
      <div
        class="d-flex align-items-center pb-4"
        :class="{'border-bottom': index < attachments.length - 1, 'pt-4': index > 0}"
        v-for="(doc, index) in attachments"
        :key="index"
        @mouseover="showPreview(doc)"
        @mouseleave="hidePreview"
        @click="openPreview(doc)"
        style="cursor: pointer;"
      >
        <div class="me-4">
          <Image v-if="doc.type === 'image'" :src="doc.url" preview width="100%"/>
          <i v-else :class="doc.icon" style="font-size: 2.5rem" />
        </div>
        <div class="d-flex flex-column flex-grow-1">
          <h4>{{ doc.item }}</h4>
        </div>
        <div class="text-end fw-500">
          <p class="text-fade mb-0">{{ doc.date }}</p>
        </div>
      </div>
    </template>
    <template #footer>
      <a v-if="attachments.length > 4" class="float-end">View All</a>
    </template>
  </Card>

  <Dialog :visible="previewVisible" @hide="previewVisible = false" :style="{ width: '75vw', height: '75vh' }">
    <template v-if="previewType === 'image'">
      <Image :src="previewUrl" preview width="100%"/>
    </template>
    <template v-else>
      <iframe v-if="previewType === 'pdf'" :src="previewUrl" style="width: 100%; height: 100%;" frameborder="0"></iframe>
      <iframe v-else-if="previewType === 'word'" :src="previewUrl" style="width: 100%; height: 100%;" frameborder="0"></iframe>
    </template>
  </Dialog>
</template>

<script>
import Card from 'primevue/card';
import Dialog from 'primevue/dialog';
import Image from 'primevue/image';

import { VCard, VCardTitle, VCardText, VCardActions } from 'vuetify/components/VCard';
import { VFileInput } from 'vuetify/components/VFileInput';
import { VTooltip } from 'vuetify/components/VTooltip';
import { VImg } from 'vuetify/components/VImg';
import { VHover } from 'vuetify/components/VHover';
import { VBtn } from 'vuetify/components/VBtn';
import { VContainer, VRow, VCol } from 'vuetify/components/VGrid';

export default {
  components: {
    Card, VCard, VCardTitle, VCardText, VCardActions, VFileInput, VContainer, VRow, VCol, VTooltip, VImg, VHover, VBtn,

    Dialog,
    Image,
  },
  data() {
    return {
      attachments: [
        { item: 'Chest X-Ray', date: '02/03/2024', icon: 'pi pi-file-pdf', type: 'image', url: "/private/files/hand-xray.jpeg" },
        { item: 'Ecg Test Report', date: '08/03/2024', icon: 'pi pi-file-word', type: 'word', url: 'path/to/ecg-test-report.docx' },
        { item: 'Chest X-Ray', date: '12/03/2024', icon: 'pi pi-file-pdf', type: 'pdf', url: "/private/files/test.pdf" }
      ],
      previewVisible: false,
      previewUrl: null,
      previewType: '',
    };
  },
  methods: {
    triggerFileInput() {
      this.$refs.fileInput.$el.click();
    },
    handleFileUpload(event) {
      const uploadedFiles = Array.from(event);
      uploadedFiles.forEach(file => {
        let icon = 'pi pi-file'; // Default icon for documents
        let type = 'doc'; // Default type
        if (file.type.includes('pdf')) {
          icon = 'pi pi-file-pdf';
          type = 'pdf';
        } else if (file.type.includes('word')) {
          icon = 'pi pi-file-word';
          type = 'word';
        } else{
          icon = 'pi pi-image';
          type = 'image';
        }

        const reader = new FileReader();
        reader.onload = e => {
          const newAttachment = {
            item: file.name,
            date: new Date().toLocaleDateString(),
            icon: icon,
            type: type,
            url: e.target.result // URL for preview
          };
          this.attachments.push(newAttachment);
        };

        reader.readAsDataURL(file);
      });
    },
    showPreview(doc) {
      if (doc.type === 'image') {
        this.previewUrl = doc.url;
      }
    },
    hidePreview() {
      this.previewUrl = null;
    },
    openPreview(doc) {
      this.previewUrl = doc.url;
      this.previewType = doc.type;
      this.previewVisible = true;
    }
  }
};
</script>

<style scoped>
.border-bottom-title {
  border-bottom: 1px solid #ccc;
}

.text-orange {
  color: #ff9800;
}

.text-fade {
  color: #999;
}

.float-end {
  float: right;
}

.attachment {
  position: relative;
  padding: 10px;
  cursor: pointer;
  transition: transform 0.2s;
}

.attachment:hover {
  transform: scale(1.05);
}
</style>