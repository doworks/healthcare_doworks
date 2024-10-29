<template>
  <div class="text-center pa-4">
    <!-- <ConfirmDialog id="confirm">
      <template #container="{ message, acceptCallback, rejectCallback }">
        <div class="flex flex-col items-center p-8 bg-surface-0 dark:bg-surface-900 rounded">
          <div class="rounded-full bg-black text-primary-contrast inline-flex justify-center items-center h-24 w-24 -mt-20">
            <i class="pi pi-question"></i>
          </div>
          <span class="font-bold text-2xl block mb-2 mt-6">{{ message.header }}</span>
          <p class="mb-0">{{ message.message }}</p>
          <div class="flex items-center gap-2 mt-6">
            <Button label="Cancel" severity="secondary" outlined @click="rejectCallback" class="w-32"></Button>
            <Button label="Close" severity="danger" @click="acceptCallback" class="w-32"></Button>
          </div>
        </div>
      </template>
    </ConfirmDialog> -->
    <v-dialog
      v-model="dialogVisible"
      transition="dialog-bottom-transition"
      fullscreen
    >
      <v-card>
        <v-toolbar color="yellow-darken-1">
          <v-btn
            icon="mdi mdi-close"
            @click="confirmClose"
          ></v-btn>

          <v-toolbar-title>Procedure</v-toolbar-title>

          <v-spacer></v-spacer>

          <v-toolbar-items>
            <v-btn
              class="text-none" 
              text="Save"
              variant="text"
              @click="save"
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
    patient: {
      type: String,
      required: true,
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
      loding: false,
      notifications: false,
      sound: true,
      widgets: false,
		};
	},
  watch: {
    isOpen: {
			handler(newValue) {
				if(newValue){
          this.passHistory()
        }
			}
		},
  },
	methods: {
    updateIsOpen(value) {
      this.$emit('update:isOpen', value);
    },
    closeDialog() {
      this.updateIsOpen(false);
    },
    save() {
      this.loding = true
      const event = new CustomEvent('reactSaveAnotation', {
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
              this.$toast.add({
                severity: 'success',
                summary: 'Success',
                detail: 'Annotation saved',
                life: 3000 // Duration in ms
              });
              this.loding = false
              this.closeDialog()
            }).catch(error => {
              this.loding = false
              this.$emit('show-alert', error.message, 'error')
            });
          }
        }
      });
      window.dispatchEvent(event);
    },
    confirmClose(event) {
      this.$confirm.require({
        target: event.currentTarget,
        header: 'Are you sure?',
        message: 'If you close the window everything will discarded',
        icon: 'pi pi-info-circle',
        acceptLabel: 'Close',
        rejectLabel: 'Cancel',
        acceptProps: {
          severity: 'danger'
        },
        rejectProps: {
          severity: 'secondary'
        },
        accept: () => {
          this.dialogVisible = false
        },
      });
    },
    passHistory() {
      this.$call('healthcare_doworks.api.methods.get_annotation_history', { patient: this.patient }).then(response => {
        const event = new CustomEvent('reactSetAnnotationHistory', {detail: {annotations:response}});
        window.dispatchEvent(event);
      }).catch(error => {
        this.loding = false
        this.$emit('show-alert', error.message, 'error')
      });
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
