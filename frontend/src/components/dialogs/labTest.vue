<template>
  <v-dialog v-model="dialogVisible" width="auto" scrollable>
    <v-card rounded="lg">
      <a-form layout="vertical" :model="form" :rules="rules">
        <v-card-title class="d-flex justify-space-between align-center">
          <div class="text-h5 text-medium-emphasis ps-2">Lab Test</div>
          <v-btn icon="mdi mdi-close" variant="text" @click="closeDialog"></v-btn>
        </v-card-title>
        <v-divider class="m-0"></v-divider>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" md="6">
                <a-form-item label="Test Template" name="template">
                  <a-select
                    v-model:value="form.template"
                    :options="$resources.labTestTemplates.data?.options"
                    @change="(value, option) => {form.department = option.department}"
                    :fieldNames="{label: 'name', value: 'name'}"
                    show-search
                    :loading="$resources.labTestTemplates.list.loading"
                    @search="(value) => {handleSearch(
                      value, 
                      $resources.labTestTemplates, 
                      {name: ['like', `%${value}%`]}, 
                      {},
                    )}"
                    :filterOption="false"
                  ></a-select>
                </a-form-item>
                <a-form-item label="Department" name="department" v-if="form.department">
                  <a-input disabled v-model:value="form.department"/>
                </a-form-item>
              </v-col>
              <v-col cols="12" md="6">
                <a-form-item label="Date" name="formDate">
                  <a-date-picker 
                    v-model:value="form.formDate"
                    format="DD/MM/YYYY" 
                    style="z-index: 3000; width: 100%;"
                  />
                </a-form-item>
                <a-form-item label="Time" name="formTime">
                  <a-time-picker v-model:value="form.formTime" use12-hours format="h:mm a" style="z-index: 3000; width: 100%;"/>
                </a-form-item>
              </v-col>
            </v-row>
            <v-divider class="mt-2 mb-8"></v-divider>
            <v-row>
              <v-expansion-panels multiple>
                <v-expansion-panel>
                  <v-expansion-panel-title>Comments</v-expansion-panel-title>
                  <v-expansion-panel-text>
                    <a-form-item label="Comments" name="lab_test_comment">
                      <a-textarea v-model:value="form.lab_test_comment" :rows="12" style="width: 100%;"/>
                    </a-form-item>
                  </v-expansion-panel-text>
                </v-expansion-panel>
                <v-expansion-panel>
                  <v-expansion-panel-title>Custom Result</v-expansion-panel-title>
                  <v-expansion-panel-text>
                    <a-form-item label="Custom Result" name="custom_result">
                      <QuillEditor v-model:content="form.custom_result" :options="editorOptions" style="height: 300px"/>
                    </a-form-item>
                  </v-expansion-panel-text>
                </v-expansion-panel>

                <v-expansion-panel>
                  <v-expansion-panel-title>Worksheet Print</v-expansion-panel-title>
                  <v-expansion-panel-text>
                    <a-form-item label="Worksheet Print" name="worksheet_instructions">
                      <QuillEditor v-model:content="form.worksheet_instructions" :options="editorOptions" style="height: 300px"/>
                    </a-form-item>
                  </v-expansion-panel-text>
                </v-expansion-panel>

                <v-expansion-panel>
                  <v-expansion-panel-title>Result Legend Print</v-expansion-panel-title>
                  <v-expansion-panel-text>
                    <v-row>
                      <v-col cols="12" md="6">
                        <a-form-item label="Print Position" name="legend_print_position">
                          <a-select
                            v-model:value="form.legend_print_position"
                            :options="[{label:'', value:''},{label:'Bottom', value:'Bottom'},{label:'Top', value:'Top'},{label:'Both', value:'Both'}]"
                          ></a-select>
                        </a-form-item>
                      </v-col>
                    </v-row>
                    <a-form-item label="Result Legend" name="result_legend">
                      <QuillEditor v-model:content="form.result_legend" :options="editorOptions" style="height: 300px"/>
                    </a-form-item>
                  </v-expansion-panel-text>
                </v-expansion-panel>
              </v-expansion-panels>
            </v-row>
          </v-container>
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
          
          text="Save"
          variant="tonal"
          @click="onSubmit()"
          type="submit"
          ></v-btn>
        </v-card-actions>
      </a-form>
    </v-card>
  </v-dialog>
</template>
  
<script >
import dayjs from 'dayjs';
import { Form } from 'ant-design-vue';
import { reactive } from 'vue';

import { QuillEditor } from '@vueup/vue-quill'
import '@vueup/vue-quill/dist/vue-quill.snow.css';

import { VBtn } from 'vuetify/components/VBtn'
import { VDialog } from 'vuetify/components/VDialog';
import { VCard, VCardTitle, VCardText, VCardActions } from 'vuetify/components/VCard';
import { VContainer, VCol, VRow } from 'vuetify/components/VGrid';
import { VDivider } from 'vuetify/components/VDivider';
import { VItemGroup, VItem } from 'vuetify/components/VItemGroup';
import { VOverlay } from 'vuetify/components/VOverlay';
import { VProgressCircular } from 'vuetify/components/VProgressCircular';
import { VExpansionPanels, VExpansionPanel, VExpansionPanelTitle, VExpansionPanelText } from 'vuetify/components/VExpansionPanel';


export default {
  inject: ['$call'],
  components: {
    VBtn, VDialog, VCard, VCardTitle, VCardText, VCardActions, VDivider, VContainer, VCol, VRow, VItemGroup, QuillEditor,
    VItem, VOverlay, VProgressCircular, VExpansionPanels, VExpansionPanel, VExpansionPanelTitle, VExpansionPanelText,
  },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
      default: false,
    },
    appointment: {
      default: {
        patient: '',
        patient_sex: '',
        practitioner: '',
        service_unit: '',
        department: '',
      }
    }
  },
  resources: {
    labTestTemplates() { return { 
      type: 'list', 
      doctype: 'Lab Test Template', 
      fields: ['name', 'department'], 
      auto: true,
      orderBy: 'name',
      pageLength: 10,
      url: 'frappe.desk.reportview.get', 
      transform(data) {
        if(data.values.length == 0)
          data.options = []
        else
          data.options = this.transformData(data.keys, data.values);  // Transform the result into objects
        return data
      }
    }},
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
        doctype: 'Lab Test',
        template: '',
        department: '',
        formDate: undefined,
        formTime: undefined,
        patient: this.appointment.patient,
        patient_sex: this.appointment.patient_sex,
        practitioner: this.appointment.practitioner,
        service_unit: this.appointment.service_unit,
        requesting_department: this.appointment.department,
        lab_test_comment: '',
        custom_result: '',
        worksheet_instructions: '',
        legend_print_position: '',
        result_legend: '',
      });
    },
    rules() {
      return reactive({
        template: [{ required: true, message: 'Please choose a test template!' }],
        patient: [{ required: true, message: 'Please choose a patient!' }],
      });
    },
  },
  data() {
    return {
      lodingOverlay: false,
      editorOptions: {
        theme: 'snow',
        modules: {
          toolbar: [
            [{ header: [1, 2, 3, false] }],
            [{ size: ['small', false, 'large', 'huge'] }],
            ['bold', 'italic', 'underline', 'strike'],
            [{ color: [] }, { background: [] }],
            ['blockquote', 'code-block'],
            [{ direction: 'rtl' }],
            ['link', 'image'],
            [{ list: 'ordered'}, { list: 'bullet' }, { list: 'check' }],
            [{ align: [] }],
            [{ indent: '-1'}, { indent: '+1' }],
          ],
        },
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
        this.lodingOverlay = true;
        this.form.date = dayjs(this.form.formDate).format('YYYY-MM-DD')
        this.form.time = dayjs(this.form.formTime).format('HH:mm')
        this.$call('healthcare_doworks.api.methods.new_doc', {form: this.form})
        .then(response => {
          this.$toast.add({
            severity: 'success',
            summary: 'Success',
            detail: 'Lab test created successfully',
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
    transformData (keys, values) {
      return values.map(row => {
        const obj = {};
        keys.forEach((key, index) => {
          obj[key] = row[index];  // Map each key to its corresponding value
        });
        return obj;
      });
    },
    handleSearch(query, resource, filters, initialFilters) {
      // Clear the previous timeout to avoid spamming requests
      clearTimeout(this.searchTimeout);

      // Set a new timeout (300ms) for debouncing
      this.searchTimeout = setTimeout(() => {
        if (query) {
          // Update list resource options to fetch matching records from server
          resource.update({filters});

          // Fetch the updated results
          resource.reload();
        } else {
          // If no search query, load initial records
          resource.update({filters: initialFilters});
          resource.reload();
        }
      }, 300);  // Debounce delay of 300ms
    },
  },
};
</script>