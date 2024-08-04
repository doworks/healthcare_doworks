<template>
  <div class="text-center pa-4">
    <v-dialog
      v-model="dialogVisible"
      transition="dialog-bottom-transition"
      fullscreen
    >
      <v-card>
        <v-toolbar>
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
              @click="dialogVisible = false"
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
    onSubmit() {
      const { validate } = Form.useForm(this.form, this.rules);
      validate().then(() => {
        this.lodingOverlay = true;
        let formClone = {...this.form}
        formClone.signs_date = dayjs(formClone.signs_date).format('YYYY-MM-DD')
        formClone.signs_time = dayjs(formClone.signs_time).format('HH:mm')
        const old = formClone.name && true
        console.log(old)
        this.$call('healthcare_doworks.api.methods.edit_doc', {form: formClone})
        .then(response => {
          this.lodingOverlay = false;
          this.closeDialog()
        }).catch(error => {
          console.error(error);
          let message = error.message.split('\n');
          message = message.find(line => line.includes('frappe.exceptions'));
          if(message){
            const firstSpaceIndex = message.indexOf(' ');
            this.$emit('show-alert', message.substring(firstSpaceIndex + 1, 10000))
          }
        });
      })
      .catch(err => {
        console.log('error', err);
      });
    }
	},
};
</script>
