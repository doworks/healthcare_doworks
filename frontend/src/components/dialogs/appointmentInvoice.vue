<template>
  <v-dialog v-model="dialogVisible" width="1400px" scrollable>
    <v-card rounded="lg">
        <v-card-title class="d-flex justify-space-between align-center">
          <div class="text-h5 text-medium-emphasis ps-2"><br>{{ patient.patient_name }}</br> Appointment Invoice</div>
          <v-btn icon="mdi mdi-close" variant="text" @click="closeDialog"></v-btn>
        </v-card-title>
        <v-divider class="m-0"></v-divider>
        <v-card-text>
          <v-container fluid>
              <v-row>
                <v-col cols="12">
                  <h5>Invoice Items</h5>
                  <EditableTable :columns="[
                    {label: 'Item', key: 'item'},
                    {label: 'Cost', key: 'cost'},
                    {label: 'Customer Amount', key: 'customer_amount'},
                    {label: 'Insurance Amount', key: 'insurance_amount'},
                    {label: 'Invoices', key: 'invoice'},
                  ]"
                  :rows="appointment.custom_invoice_items"
                  @update="(items, row, isNew) => {
                    if(items && row)
                      newChildRow({
                        fieldName: 'custom_invoice_items', 
                        rules: {item: [{ required: true, message: 'Please choose an item!' }]},
                        items, row, isNew
                      })
                  }"
                  @delete="rows => {deleteChildRow({fieldName: 'custom_invoice_items', rows})}"
                  title="Invoice Items"
                  >
                  </EditableTable>
                </v-col>
              </v-row>
          </v-container>
        </v-card-text>
        
        <v-divider class="m-0"></v-divider>
        
        <v-card-actions class="my-2 d-flex justify-end">
        <v-btn
        class="text-none"
        text="Cancel"
        @click="closeDialog"
        ></v-btn>
        <v-btn
        class="text-none"
        color="blue"
        text="Submit"
        variant="tonal"
        @click="onSubmit()"
        type="submit"
        ></v-btn>
        </v-card-actions>
    </v-card>
    <v-overlay
      :model-value="lodingOverlay"
      class="align-center justify-center"
      >
      <v-progress-circular
        color="primary"
        size="64"
        indeterminate
      ></v-progress-circular>
    </v-overlay>
  </v-dialog>
</template>

<script >
import dayjs from 'dayjs';

import { VDivider } from 'vuetify/components/VDivider';
import { VInfiniteScroll } from 'vuetify/components/VInfiniteScroll';
import { VItemGroup, VItem } from 'vuetify/components/VItemGroup';
import { VOverlay } from 'vuetify/components/VOverlay';
import { VProgressCircular } from 'vuetify/components/VProgressCircular';
import EditableTable from '../editableTable.vue';

export default {
inject: ['$call'],
components: {
  VDivider, VInfiniteScroll, VItemGroup, VItem, VOverlay, VProgressCircular,
},
props: {
  isOpen: {
    type: Boolean,
    required: true,
    default: false,
  },
  appointment: {
    required: true,
    default: {
      name: '',
    }
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
  };
},
  mounted() {
    this.allergies = this.patient.custom_allergies_table
    this.infectedDiseases = this.patient.custom_infected_diseases
    this.surgicalHistory = this.patient.custom_surgical_history_table.map(sur => {
      sur.dayDate = dayjs(sur.date)
      return sur
    })
    this.medications = this.patient.custom_medications.map(med => {
      med.dayDate = dayjs(med.from_date)
      return med
    })
    this.habits = this.patient.custom_habits__social
    this.riskFactors = this.patient.custom_risk_factors_table
    this.chronicDiseases = this.patient.custom_chronic_diseases
    this.geneticDiseases = this.patient.custom_genetic_conditions
  },
  watch: {
    patient: {
      handler(newValue) {
        if(newValue){
          this.allergies = this.patient.custom_allergies_table
          this.infectedDiseases = this.patient.custom_infected_diseases
          this.surgicalHistory = this.patient.custom_surgical_history_table.map(sur => {
            sur.dayDate = dayjs(sur.date)
            return sur
          })
          this.medications = this.patient.custom_medications.map(med => {
            med.dayDate = dayjs(med.from_date)
            return med
          })
          this.habits = this.patient.custom_habits__social
          this.riskFactors = this.patient.custom_risk_factors_table
          this.chronicDiseases = this.patient.custom_chronic_diseases
          this.geneticDiseases = this.patient.custom_genetic_conditions
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
    newChildRow({parentDoctype ,prarentDocname, fieldName, rules, items, row, isNew}) {
      const { validate } = Form.useForm(row, rules);
      validate().then(() => {
        let formClone = {...row}
        delete formClone.modified
        delete formClone.modified_by
        delete formClone.name
        if(isNew){
          this.$call('healthcare_doworks.api.general_methods.add_child_entry', {
            parent_doctype: parentDoctype || 'Patient Appointment', 
            parent_doc_name: prarentDocname || this.appointment.name, 
            child_table_fieldname: fieldName, 
            child_data: formClone
          }).then(response => {
          }).catch(error => {
            console.error(error);
            let message = error.message.split('\n');
            message = message.find(line => line.includes('frappe.exceptions'));
            if(message){
              const firstSpaceIndex = message.indexOf(' ');
              this.showAlert(message.substring(firstSpaceIndex + 1) , 10000)
            }
            else
              this.showAlert('Sorry. There is an error!' , 10000)
          });
        }
        else{
          this.$call('healthcare_doworks.api.general_methods.modify_child_entry', {
            parent_doctype: parentDoctype || 'Patient Appointment', 
            parent_doc_name: prarentDocname || this.appointment.name, 
            child_table_fieldname: fieldName, 
            filters: {name: row.name}, 
            update_data: formClone
          }).then(response => {
          }).catch(error => {
            console.error(error);
            let message = error.message.split('\n');
            message = message.find(line => line.includes('frappe.exceptions'));
            if(message){
              const firstSpaceIndex = message.indexOf(' ');
              this.showAlert(message.substring(firstSpaceIndex + 1) , 10000)
            }
            else
              this.showAlert('Sorry. There is an error!' , 10000)
          });
        }
      })
      .catch(err => {
        console.log('error', err);
      });
    },
    deleteChildRow({parentDoctype, prarentDocname, fieldName, rows, filterField}) {
      rows.forEach(row => {
        this.$call('healthcare_doworks.api.general_methods.delete_child_entry', {
          parent_doctype: parentDoctype || 'Patient Appointment', 
          parent_doc_name: prarentDocname || this.appointment.name, 
          child_table_fieldname: fieldName, 
          filters: {[filterField || 'name']: row}
        }).then(response => {
        }).catch(error => {
          console.error(error);
          let message = error.message.split('\n');
          message = message.find(line => line.includes('frappe.exceptions'));
          if(message){
            const firstSpaceIndex = message.indexOf(' ');
            this.showAlert(message.substring(firstSpaceIndex + 1) , 10000)
          }
          else
            this.showAlert('Sorry. There is an error!' , 10000)
        })
        .catch(err => {
          console.log('error', err);
        });
      })
    },
  },
};
</script>