<template>
  <v-dialog v-model="dialogVisible" width="auto" scrollable>
    <v-card rounded="lg">
      <v-card-title class="d-flex justify-space-between align-center">
        <div class="text-h5 text-medium-emphasis ps-2">New Patient</div>
        <v-btn icon="mdi mdi-close" variant="text" @click="closeDialog"></v-btn>
      </v-card-title>
      <v-divider class="m-0"></v-divider>
      <v-card-text>
        <a-form layout="vertical" :model="form" :rules="rules">
          <v-container>
            <v-row>
              <v-col cols="12" md="6">
                <a-form-item label="First Name" name="first_name" >
                  <a-input v-model:value="form.first_name" @change="updateFullName"/>
                </a-form-item>
                <a-form-item label="Middle Name (optional)" name="middle_name">
                  <a-input v-model:value="form.middle_name" @change="updateFullName"/>
                </a-form-item>
                <a-form-item label="Last Name" name="last_name" >
                  <a-input v-model:value="form.last_name" @change="updateFullName"/>
                </a-form-item>
                <a-form-item label="Full Name" name="patient_name" >
                  <a-input v-model:value="form.patient_name" disabled/>
                </a-form-item>
              </v-col>
              <v-col cols="12" md="6">
                <a-form-item label="CPR" name="custom_cpr" >
                  <a-input v-model:value="form.custom_cpr"/>
                </a-form-item>
                <a-form-item label="Gender" name="sex">
                  <a-select 
                  v-model:value="form.sex" 
                  :options="$resources.genders.data" 
                  :fieldNames="{label: 'gender', value: 'name'}"
                  allowClear
                  ></a-select>
                </a-form-item>
                <a-form-item label="Mobile" name="mobile">
                  <a-input v-model:value="form.mobile"/>
                </a-form-item>
              </v-col>
            </v-row> 
          </v-container>
        </a-form>
      </v-card-text>    
      <v-divider class="mt-2"></v-divider>
          
      <v-card-actions class="my-2 d-flex justify-end">
      <v-btn
      class="text-none"
      text="Cancel"
      @click="closeDialog"
      ></v-btn>
      <v-btn
      class="text-none"
      color="blue"
      
      text="submit"
      variant="tonal"
      @click="onSubmit()"
      type="submit"
      ></v-btn>
      </v-card-actions>
    </v-card>
    <v-overlay :model-value="lodingOverlay" class="align-center justify-center">
    <v-progress-circular color="primary" size="64" indeterminate></v-progress-circular>
    </v-overlay>
  </v-dialog>
</template>

<script >
import { Form } from 'ant-design-vue';
import { reactive } from 'vue';

import { VDivider } from 'vuetify/components/VDivider';
import { VInfiniteScroll } from 'vuetify/components/VInfiniteScroll';
import { VItemGroup, VItem } from 'vuetify/components/VItemGroup';
import { VOverlay } from 'vuetify/components/VOverlay';
import { VProgressCircular } from 'vuetify/components/VProgressCircular';

export default {
  inject: ['$call'],
  components: {VInfiniteScroll, VItemGroup, VItem, VOverlay, VProgressCircular},
  props: {
    isOpen: {type: Boolean, required: true, default: false},
  },
  resources: {
    genders() { return { type: 'list', doctype: 'Gender', fields: ['gender', 'name'], auto: true, pageLength: null, cache: 'genders' } },
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
      form: {
        doctype: 'Patient',
        first_name: '',
        middle_name: '',
        last_name: '',
        patient_name: '',
        sex: '',
        mobile: '',
      },
      rules: {
        first_name: [{ required: true, message: 'Please type a first name!' }],
        sex: [{ required: true, message: 'Please choose a gender!' }],
      },
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
        this.$emit('submitted', this.form)
        // this.lodingOverlay = true;
        // this.$call('healthcare_doworks.api.methods.new_doc', {form: this.form})
        // .then(response => {
        //   this.lodingOverlay = false;
        //   this.$emit('submitted', response)
        //   this.closeDialog()
        // }).catch(error => {
        //   console.error(error);
        //   let message = error.message.split('\n');
        //   message = message.find(line => line.includes('frappe.exceptions'));
        //   if(message){
        //     const firstSpaceIndex = message.indexOf(' ');
        //     this.$emit('show-alert', message.substring(firstSpaceIndex + 1, 10000))
        //   }
        // });
      })
      .catch(err => {
        console.log('error', err);
      });
    },
    updateFullName() {
      this.form.patient_name = (this.form.first_name ? this.form.first_name : '' ) + 
      (this.form.middle_name ? ' ' + this.form.middle_name : '') + 
      (this.form.last_name ? ' ' + this.form.last_name : '')
    },
  },
};
</script>