<template>
  <div class="text-center pa-4">
    <v-dialog
      v-model="dialogVisible"
      transition="dialog-bottom-transition"
      fullscreen
    >
      <v-card>
        <v-toolbar color="yellow-darken-1">
          <v-btn
            icon="mdi mdi-close"
            @click="dialogVisible = false"
          ></v-btn>

          <v-toolbar-title>Procedure</v-toolbar-title>

          <v-spacer></v-spacer>

          <v-toolbar-items>
            <v-btn
              text="Save"
              variant="text"
              @click="triggerReactFunction"
            ></v-btn>
          </v-toolbar-items>
        </v-toolbar>

        <ExcalidrawWrapper />
        
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import { reactive } from 'vue';

import { VContainer, VCol, VRow, VSpacer } from 'vuetify/components/VGrid';
import { VInfiniteScroll } from 'vuetify/components/VInfiniteScroll';
import { VToolbar, VToolbarItems, VToolbarTitle } from 'vuetify/components/VToolbar';
import ExcalidrawWrapper from '@/components/ExcalidrawWrapper.vue';


export default {
	inject: ['$call'],
	components: {
		VContainer, VCol, VRow, VSpacer, VInfiniteScroll, VToolbar, VToolbarItems, VToolbarTitle, ExcalidrawWrapper
	},
	props: {
		isOpen: {
      type: Boolean,
      required: true,
      default: false,
    },
    doctype: {
      type: String,
      required: true,
      default: '',
    },
    docname: {
      type: String,
      required: true,
      default: '',
    },
    encounterType: {
      type: String,
      default: '',
    },
	},
  computed: {
    dialogVisible: {
      get() {
        return this.isOpen;
      },
      set(value) {
        this.$emit('update:isOpen', value);
      },
    },
  },
	data() {
		return {
      lodingOverlay: false,
      notifications: false,
      sound: true,
      widgets: false,
		};
	},
	methods: {
    updateIsOpen(value) {
      this.$emit('update:isOpen', value);
    },
    closeDialog() {
      this.updateIsOpen(false);
    },
    triggerReactFunction() {
      const event = new CustomEvent('vueToReactEvent', {
        detail: {
          callback: async (data) => {
            const base64Image = await this.convertBlobToBase64(data.blob);
            this.$call('healthcare_doworks.api.methods.upload_annotation', {
              doctype: this.doctype, 
              docname: this.docname, 
              encounter_type: this.encounterType,
              annotation_template: data.annotationsTemplate,
              file_data: base64Image,
              jsonText: data.jsonText,
            }).then(response => {
              this.closeDialog()
            })
          }
        }
      });
      window.dispatchEvent(event);
    },
    async convertBlobToBase64(blob) {
      return new Promise((resolve, reject) => {
        const reader = new FileReader();
        reader.onloadend = () => {
          // Create the base64 string with the MIME type prefix
          const base64String = reader.result;
          resolve(base64String);
        };
        reader.onerror = reject;
        reader.readAsDataURL(blob);
      });
    }
	},
};
</script>
