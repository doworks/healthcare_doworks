<template>
  <div>
    <v-dialog v-model="dialogVisible" min-width="600" width="auto" scrollable>
        <v-card rounded="lg">
          <a-form layout="vertical" :model="form" :rules="rules">
            <v-card-title class="d-flex justify-space-between align-center">
              <div class="text-h5 text-medium-emphasis ps-2">{{!form.name ? 'New ' : ''}}Checklist Form</div>
              <v-btn icon="mdi mdi-close" variant="text" @click="closeDialog"></v-btn>
            </v-card-title>
            <v-divider class="m-0"></v-divider>
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12" md="6">
                    <a-form-item label="Policy Number">
                      <a-select
                      class="w-full"
                      v-model:value="form.form_template"
                      :options="$resources.checklistFormTemplates.data?.options"
                      :fieldNames="{label: 'patient_name', value: 'name'}"
                      show-search
                      :loading="$resources.checklistFormTemplates.list.loading"
                      @search="(value) => {handleSearch(
                        value, 
                        $resources.checklistFormTemplates, 
                      )}"
                      @change="(value, option) => {
                        getChecklistFormItems(option.name)
                      }"
                      :filterOption="false"
                      >
                      </a-select>
                    </a-form-item>
                  </v-col>
                </v-row>

                <v-row v-if="form.children?.checklist_items">
                  <v-col>
                    <template v-for="(item, index) in form.children?.checklist_items" :key="index">
                      <a-form-item v-if="item.type == 'Select' || item.type == 'Text'" :label="item.label">
                        <!-- <a-radio-group v-if="item.type == 'Select'" v-model="item.value">
                          <a-radio v-for="(option, i) in item.options?.split('\n')" :key="i" style="display: flex; height: 30px; line-height: 30px" :value="option">{{ option }}</a-radio>
                        </a-radio-group> -->
                        <a-checkbox-group v-if="item.type == 'Select'" v-model:value="item.value" @change="(val) => {
                            item.value = []
                            item.value[0] = val[val.length - 1]
                          }">
                          <a-checkbox 
                          v-for="(option, i) in item.options?.split('\n')" 
                          :key="i" 
                          class="w-full"
                          :value="option"
                          >
                            {{ option }}
                          </a-checkbox>
                        </a-checkbox-group>
                        <a-textarea v-if="item.type == 'Text'" v-model:value="item.value" :rows="4"/>
                      </a-form-item>
                      <a-checkbox v-if="item.type == 'Check'" class="mb-3 w-full" v-model:checked="item.value">{{ item.label }}</a-checkbox>
                      <v-divider class="mt-2" v-if="item.type == 'Section'"></v-divider>
                      <h3 class="my-0 py-0 text-center" v-if="item.type == 'Section'">{{ item.label }}</h3>
                      <h4 class="my-0 py-0 text-center" v-if="item.type == 'Section'">{{ item.options }}</h4>
                      <v-divider class="mb-2" v-if="item.type == 'Section'"></v-divider>
                      <h4 class="my-0 py-0" v-if="item.type == 'Header'">{{ item.label }}</h4>
                      <!-- <br v-if="item.type == 'Divider'" v-for="n in item.options"/> -->
                      <div v-if="item.type == 'Divider'" :class="'m-' + item.options"></div>
                    </template>
                  </v-col>
                </v-row>
              </v-container>
            </v-card-text>
                
            <v-divider class="mt-2"></v-divider>
                
            <v-card-actions class="my-2 d-flex justify-end">
              <v-btn class="text-none" text="Cancel" @click="closeDialog"></v-btn>
              <v-btn class="text-none" color="blue" text="submit" variant="tonal" @click="onSubmit()" type="submit"></v-btn>
            </v-card-actions>
          </a-form>
        </v-card>
      <v-overlay :model-value="lodingOverlay" class="align-center justify-center">
        <v-progress-circular color="primary" size="64" indeterminate></v-progress-circular>
      </v-overlay>
    </v-dialog>
  </div>
</template>

<script >
import dayjs from 'dayjs';
import { reactive } from 'vue';
import { Form } from 'ant-design-vue';
import { VContainer, VCol, VRow } from 'vuetify/components/VGrid';
import { VDivider } from 'vuetify/components/VDivider';
import { VInfiniteScroll } from 'vuetify/components/VInfiniteScroll';
import { VItemGroup, VItem } from 'vuetify/components/VItemGroup';

export default {
	inject: ['$call'],
	components: {
		VDivider, VContainer, VCol, VRow, VInfiniteScroll, VItemGroup, VItem,
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
        name: '',
      }
    },
    name: {
      type: String,
      default: '',
    }
	},
  resources: {
    checklistFormTemplates() { return { 
			type: 'list', 
			doctype: 'Checklist Form Template', 
			fields: ['name', 'form_name'], 
			auto: true, 
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
    rules() {
      return reactive({});
    },
  },
	data() {
		return {
      form: reactive({
        doctype: 'Checklist Form',
        name: this.name || '',
        appointment: this.appointment.name,
        form_template: '',
        children: {
          checklist_items: []
        }
      }),
      lodingOverlay: false,
		};
	},
  watch: {
    appointment: {
      handler(newValue) {
        if(newValue){
          this.form.appointment = newValue.name
          this.form.patient = newValue.patient
        }
      }
    },
    name: {
      handler(newValue) {
        if(newValue){
          this.form.name = newValue
          this.fetchRecords();
        }
      }
    },
    isOpen: {
      handler(newValue) {
        if(newValue){
          this.form = {
            doctype: 'Checklist Form',
            name: this.name || '',
            appointment: this.appointment.name,
            form_template: '',
            children: {
              checklist_items: []
            }
          }
          this.fetchRecords();
        }
      }
    },
  },
  mounted() {
    this.form = {
      doctype: 'Checklist Form',
      name: this.name || '',
      form_template: '',
      appointment: this.appointment.name,
      children: {
        checklist_items: []
      }
    }
    this.fetchRecords();
  },
	methods: {
    updateIsOpen(value) {
      this.$emit('update:isOpen', value);
    },
    closeDialog() {
      this.updateIsOpen(false);
    },
    fetchRecords() {
      if(this.name){
        this.lodingOverlay = true
        this.$call('healthcare_doworks.api.methods.get_checklist_form', {name: this.name})
        .then(response => {
          response.children.checklist_items = response.children.checklist_items.map(value => {
            if(value.type == 'Select' && value.value != null){
              value.value = JSON.parse(value.value)
            }
            return value
          })
          this.form = {...this.form, ...response}
          this.lodingOverlay = false
        })
        .catch(error => {
          this.lodingOverlay = false;
          this.$emit('show-alert', error.message, 'error')
          console.error('Error fetching records:', error);
        });
      }
    },
    getChecklistFormItems(template) {
      this.$call('healthcare_doworks.api.methods.get_checklist_form_items', {template})
      .then(response => {
        this.form.children = {
          checklist_items: response.map(value => {
            if(value.type == 'Select' && value.value)
              value.value = JSON.parse(value.value)
            return value
          })
        }
        this.lodingOverlay = false
      })
      .catch(error => {
        this.lodingOverlay = false;
        this.$emit('show-alert', error.message, 'error')
        console.error('Error fetching records:', error);
      });
    },
    handleCheckboxChange(item, option) {
      // Set the value when a checkbox is selected
      item.value = option;
    },
    onSubmit() {
      const { validate } = Form.useForm(this.form, this.rules);
      validate().then(() => {
        this.lodingOverlay = true;
        let formClone = {...this.form}
        let children = formClone.children
        children.checklist_items.map(value => {
          if(value.type == 'Select' && value.value)
            value.value = JSON.stringify(value.value)
          return value
        })

        delete formClone.children
        const old = !!formClone.name
        if(old){
          this.$call('healthcare_doworks.api.methods.edit_doc', {form: formClone, children})
          .then(response => {
            this.$toast.add({
              severity: 'success',
              summary: 'Success',
              detail: 'Form Saved',
              life: 3000 // Duration in ms
            });
            this.lodingOverlay = false;
            this.closeDialog()
          }).catch(error => {
            this.$emit('show-alert', error.message, 'error')
          });
        }
        else{
          this.$call('healthcare_doworks.api.methods.new_doc', {form: formClone, children})
          .then(response => {
            this.$toast.add({
                severity: 'success',
                summary: 'Success',
                detail: 'Form Created',
                life: 3000 // Duration in ms
            });
            this.lodingOverlay = false;
            this.closeDialog()
          }).catch(error => {
            this.$emit('show-alert', error.message, 'error')
          });
        }
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
    handleSearch(query, resource, filters={}, initialFilters={}, orFilters=[]) {
      // Clear the previous timeout to avoid spamming requests
      clearTimeout(this.searchTimeout);

      // Set a new timeout (300ms) for debouncing
      this.searchTimeout = setTimeout(() => {
        if (query) {
          // Update list resource options to fetch matching records from server
          resource.update({filters, orFilters});

          // Fetch the updated results
          resource.reload();
        } else {
          // If no search query, load initial records
          resource.update({filters: initialFilters, orFilters});
          resource.reload();
        }
      }, 300);  // Debounce delay of 300ms
    },
	},
};
</script>