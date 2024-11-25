<template>
  <!-- Main Wrapper -->
  <div class="main-wrapper mr-3" id="farmacy-dashboard" style="margin-right: -10px;">
    <v-alert
      v-if="alertActive && alertType === 'error'"
      type="error"
      position="fixed"
      location="top center"
      color="red-lighten-3"
      style="z-index: 3000; margin-top: 15px"
      closable
      @click:close="() => {
        alertActive = false
        alertType = ''
        alertMessage = ''
      }"
    >
      <div v-html="alertMessage"></div>
    </v-alert>
    <!-- Page Content -->
    <DataTable v-model:expandedRows="expandedRows" :value="medicationRequests" dataKey="encounter">
      <template #empty><v-empty-state title="No Midications"></v-empty-state></template>
      <template #header>
        <div class="flex flex-wrap justify-end gap-2">
          <Button text icon="pi pi-plus" label="Expand All" @click="expandAll" />
          <Button text icon="pi pi-minus" label="Collapse All" @click="collapseAll" />
        </div>
      </template>
      <Column expander style="width: 5rem" />
      <Column field="practitioner_name" header="Practitioner"></Column>
      <Column field="patient_name" header="Patient"></Column>
      <Column field="orderDate" header="Date"></Column>
      <Column field="orderTime" header="Time"></Column>
      <Column field="encounter" header="Encounter"></Column>
      <Column headerStyle="width:4rem">
        <template #body="{ data }">
          <v-btn icon="mdi mdi-check-all" variant="text" color="blue" @click="() => {
            data.items.forEach(value => {
              changeStatus(value.name, 'completed-Medication Request Status')
            })
          }"/>
        </template>
      </Column>
      <template #expansion="slotProps">
        <div class="p-4">
          <!-- <h5>Medicines for {{ slotProps.data.encounter }}</h5> -->
          <DataTable :value="slotProps.data.items" tableClass="bg-amber">
            <Column field="medication" header="Medication"></Column>
            <Column field="medication_item" header="Medication Item"></Column>
            <Column field="dosage" header="Frequency"></Column>
            <Column field="period" header="Duration"></Column>
            <Column field="dosage_form" header="Form"></Column>
            <Column field="status_title" header="Status"></Column>
            <Column headerStyle="width:4rem">
              <template #body="row">
                <v-menu open-on-hover>
                  <template v-slot:activator="{ props }">
                    <v-btn class="text-none" variant="text" color="amber" v-bind="props">
                      Change Status
                    </v-btn>
                  </template>

                  <v-list>
                    <v-list-item v-for="(status, index) in statusOptions" :value="status.title" :key="index" @click="() => {
                      changeStatus(row.data.name, status.status)
                    }">
                      <v-list-item-title>{{ status.title }}</v-list-item-title>
                    </v-list-item>
                  </v-list>
                </v-menu>
              </template>
            </Column>
          </DataTable>
        </div>
      </template>
    </DataTable>
  </div>
  <!-- /Main Wrapper -->
</template>
<script>
import dayjs from 'dayjs';
import { ref } from 'vue';

import AppointmentTab from '../doctors/doctor-appointment-tab.vue'

import { VAvatar } from 'vuetify/components/VAvatar';
import { VChip } from 'vuetify/components/VChip';
import { VEmptyState } from 'vuetify/labs/VEmptyState';
import { VProgressLinear } from 'vuetify/components/VProgressLinear'
import { VList, VListItem, VListItemTitle } from 'vuetify/components/VList'
import { VMenu } from 'vuetify/components/VMenu'

export default {
  inject: ['$call', '$socket'],
  components: {
    AppointmentTab, VAvatar, VChip, VEmptyState, VProgressLinear, VList, VListItem, VListItemTitle, VMenu
  },
  resources: {
  },
  data() {
    return {
      medicationRequests: [],
      expandedRows: {},
      statusOptions: [
        { title: 'Active', status: 'active-Medication Request Status' },
        { title: 'Completed', status: 'completed-Medication Request Status' },
        { title: 'On Hold', status: 'on-hold-Medication Request Status' },
        { title: 'Cancelled', status: 'cancelled-Medication Request Status' },
        { title: 'Ended', status: 'ended-Medication Request Status' },
      ],

      vitalSignsOpen: false,
      medicalHistoryActive: false,
      appointmentNoteOpen: false,
      serviceUnitOpen: false,
      transferOpen: false,
      paymentTypeOpen: false,
      appointmentInvoiceOpen: false,
      selectedRow: {name: '', patient_details: {id: ''}},

      alertMessage: '',
      alertType: '', // 'success' or 'error'
      alertActive: false,
    };
  },
  created() {
    this.$socket.on('medication_request_updated', updatedRequest => {
      this.fetchRecords()
    })
  },
  mounted() {
    this.fetchRecords();
  },
  methods: {
    showAlert(message, type) {
      this.alertMessage = message;
      this.alertType = type;
      this.alertActive = true;
    },
    fetchRecords() {
      this.$call('healthcare_doworks.api.methods.get_medication_requests')
      .then(response => {
        this.medicationRequests = response.map(value => {
          const dateTime = dayjs(value.order_date + ' ' + value.order_time)
          value.orderDate = dateTime.format('DD/MM/YYYY')
          value.orderTime = dateTime.format('HH:mm')
          return value
        })
      })
      .catch(error => {
        this.showAlert(error.message, 'error')
        console.error('Error fetching records:', error);
      });
    },
    expandAll() {
      this.expandedRows = this.medicationRequests.reduce((acc, p) => (acc[p.encounter] = true) && acc, {});
    },
    collapseAll() {
      this.expandedRows = null;
    },
    changeStatus(request, status) {
      this.$call('frappe.client.set_value', 
        {doctype: 'Medication Request', name: request, fieldname: 'status', value: status}
      ).then(response => {
        this.$toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Medicen status changed',
          life: 3000 // Duration in ms
        });
      }).catch(error => {
        this.showAlert(error.message, 'error')
      });
    },
    appointmentNoteDialog(row) {
      this.selectedRow = row
			this.appointmentNoteOpen = true;
		},
    vitalSignDialog(row) {
      this.selectedRow = row
      this.vitalSignsOpen = true;
    },
    appointmentInvoiceDialog(row) {
      this.selectedRow = row
			this.appointmentInvoiceOpen = true;
		},
    transferPractitionerDialog(row) {
      this.appointmentForm.name = row.name;
      this.appointmentForm.practitioner = row.practitioner;
      this.appointmentForm.practitioner_name = row.practitioner_name;
			this.transferOpen = true
		},
    serviceUnitDialog(row) {
      this.appointmentForm.name = row.name;
      this.appointmentForm.service_unit = row.service_unit;
			this.serviceUnitOpen = true
		},
    onSubmitTransferPractitioner() {
      this.lodingOverlay = true;
      this.$call('healthcare_doworks.api.methods.transferToPractitioner', 
        {app: this.appointmentForm.name, practitioner: this.appointmentForm.practitioner}
      ).then(response => {
        this.$toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Appointment transformed',
          life: 3000 // Duration in ms
        });
        this.lodingOverlay = false;
        this.transferOpen = false;
      }).catch(error => {
        this.showAlert(error.message, 'error')
      });
    },
    onSubmitServiceUnit() {
      this.lodingOverlay = true;
      this.$call('frappe.client.set_value', 
        {doctype: 'Patient Appointment', name: this.appointmentForm.name, fieldname: 'service_unit', value: this.appointmentForm.service_unit}
      ).then(response => {
        this.$toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Appointment room changed',
          life: 3000 // Duration in ms
        });
        this.lodingOverlay = false;
        this.serviceUnitOpen = false;
      }).catch(error => {
        this.showAlert(error.message, 'error')
      });
    },
    onSubmitPaymentType() {
      this.lodingOverlay = true;
      if(this.appointmentForm.custom_payment_type == 'Insurance'){
        let form = {...this.patientInsurance, custom_default_payment_type: this.appointmentForm.custom_payment_type}
        form.custom_expiration_date = form.custom_expiration_date.format('YYYY-MM-DD')
        this.$call('healthcare_doworks.api.methods.edit_doc', {form}).then(response => {
          this.$toast.add({
            severity: 'success',
            summary: 'Success',
            detail: 'Patient insurance details saved',
            life: 3000 // Duration in ms
          });
          this.lodingOverlay = false;
          this.paymentTypeOpen = false;
        }).catch(error => {
          this.showAlert(error.message, 'error')
        });
      }

      this.$call('frappe.client.set_value', 
        {doctype: 'Patient Appointment', name: this.appointmentForm.name, fieldname: 'custom_payment_type', value: this.appointmentForm.custom_payment_type}
      ).then(response => {
        this.$toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Appointment payment type saved',
          life: 3000 // Duration in ms
        });
        this.lodingOverlay = false;
        this.paymentTypeOpen = false;
      }).catch(error => {
        this.showAlert(error.message, 'error')
      });
    },
    toggleOP(event) {
      this.$refs.op.toggle(event)
    },
    nextAppointmentTimeDiff() {
      dayjs()
    },
    pageChanged(event) {
      this.start = event.first;
      const maxed = [20, 100, 500, 2500].some(val => this.groupedAppointments[this.tab].length == val)
      if(event.rows > this.limit[this.tab] && event.rows >= this.groupedAppointments[this.tab].length && maxed){
        this.limit[this.tab] = event.rows;
        this.fetchRecords();
      }
      else
        this.limit[this.tab] = event.rows;
    },
    updateProgress() {
      this.progressValue = (this.appointments.length / this.totalRecords) * 100;
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
  name: "farmacy-dashboard",
};
</script>
