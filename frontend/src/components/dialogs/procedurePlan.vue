<template>
  <v-dialog v-model="dialogVisible" width="auto" scrollable>
    <v-card rounded="lg">
      <v-card-title class="d-flex justify-space-between align-center">
        <div class="text-h5 text-medium-emphasis ps-2">Procedure Plan</div>
        <v-btn icon="mdi mdi-close" variant="text" @click="closeDialog"></v-btn>
      </v-card-title>
      <v-divider class="m-0"></v-divider>
      <v-card-text>
        <a-form layout="vertical" :model="form" :rules="rules">
          <v-container>
            <v-row>
              <v-col cols="12" md="6">
                <a-form-item label="Plan Template" name="plan_template">
                  <LinkField 
                  doctype="Procedure Plan Template" 
                  :value="form.plan_template" 
                  @change="(data) => { 
                    form.plan_template = data 
                    if(data){
                      $validateLink({
                        doctype: 'Procedure Plan Template', 
                        docname:data, 
                        fields:['number_of_sessions', 'item', 'item_name']
                      })
                      .then(response => {
                        form.number_of_sessions = response.number_of_sessions
                        form.item = response.item
                        form.item_name = response.item_name
                      })
                      $getList({
                        doctype: 'Procedure Template Multi-select', 
                        filters: {parent: data}, 
                        fields: ['template'],
                        parent: 'Procedure Plan Template'
                      })
                      .then(response => {
                        children.procedures = response.map(value => value.template)
                      })
                    }
                    else{
                      form.number_of_sessions = ''
                      form.item = ''
                      form.item_name = ''
                      children.procedures = []
                    }
                  }"
                  />
                </a-form-item>
                <a-form-item label="Procedures" name="procedures">
                  <LinkField 
                  doctype="Clinical Procedure Template" 
                  mode="multiple"
                  :value="children.procedures" 
                  @change="(data) => { children.procedures = data }"
                  />
                </a-form-item>
                <a-form-item label="Number Of Sessions" name="number_of_sessions">
                  <a-input v-model:value="form.number_of_sessions"/>
                </a-form-item>
              </v-col>
              <v-col cols="12" md="6">
                <a-form-item label="Date" name="date">
                  <a-date-picker 
                  v-model:value="form.date"
                  format="DD/MM/YYYY" 
                  style="z-index: 3000"
                  class="w-full"
                  />
                </a-form-item>
              </v-col>
            </v-row>
            <v-divider class="mb-2"></v-divider>
            <h4>Billing</h4>
            <v-row>
              <v-col cols="12" md="6">
                <a-form-item label="Payment Type" name="payment_type">
                  <a-select
                  v-model:value="form.payment_type"
                  :options="[{label:'Single', value:'Single'},{label:'Package', value:'Package'}]"
                  allowClear
                  class="w-full"
                  />
                </a-form-item>
                <a-form-item label="Item" name="item">
                  <LinkField 
                  doctype="Item" 
                  :value="form.item" 
                  @change="(data) => { 
                    form.item = data 
                    $validateLink({doctype: 'Item', docname:data, fields:['item_name']})
                    .then(response => {
                      form.item_name = response.item_name
                    })
                  }"
                  />
                </a-form-item>
                <a-form-item v-if="form.item_name" label="Item Name" name="item_name">
                  <a-input v-model:value="form.item_name" disabled/>
                </a-form-item>
              </v-col>
            </v-row> 
          </v-container>
        </a-form>
      </v-card-text>    

      <v-card-actions class="my-2 d-flex justify-end">
      <v-btn
      class="text-none"
      color="green"
      
      text="Save"
      variant="tonal"
      @click="onSubmit"
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
import dayjs from 'dayjs';
import { reactive } from 'vue';

import { VDivider } from 'vuetify/components/VDivider';
import { VInfiniteScroll } from 'vuetify/components/VInfiniteScroll';
import { VItemGroup, VItem } from 'vuetify/components/VItemGroup';
import { VOverlay } from 'vuetify/components/VOverlay';
import { VProgressCircular } from 'vuetify/components/VProgressCircular';

export default {
  inject: ['$call', '$validateLink', '$getList'],
  components: {VInfiniteScroll, VItemGroup, VItem, VOverlay, VProgressCircular},
  props: {
    isOpen: {type: Boolean, required: true, default: false},
    patient: {type: String, default: ''},
  },
  resources: {
    
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
    form() {
      return reactive({
        doctype: 'Procedure Plan',
        name: this.name || '',
        patient: this.patient || '',
        date: dayjs(),
        plan_template: '',
        number_of_sessions: '',
        payment_type: 'Single',
        item: '',
        item_name: '',
      });
    },
    children() {
      return reactive({
        procedures: []
      });
    },
    rules() {
      return reactive({});
    },
  },
  data() {
    return {
      lodingOverlay: false,
      selectedRows: null,
    };
  },
  // watch: {
  //   isOpen(newVal) {
  //     if (newVal) {

  //     }
  //   },
  // },
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
        let form = {...this.form}
        form.date = dayjs(form.date).format('YYYY-MM-DD')
        let children = {procedures: this.children.procedures.map(value => {
          return {template: value}
        })}
        
        this.$call('healthcare_doworks.api.methods.new_doc', {form, children})
        .then(response => {
          this.$toast.add({
            severity: 'success',
            summary: 'Success',
            detail: 'New Session Created',
            life: 3000 // Duration in ms
          });
          this.lodingOverlay = false;
          this.closeDialog()
        }).catch(error => {
          this.$emit('show-alert', error.message, 'error')
        });
      })
      .catch(err => {
        console.log('error', err);
      });
    },
  },
};
</script>