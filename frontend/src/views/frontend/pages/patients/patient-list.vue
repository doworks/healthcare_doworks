<template>
  <!-- Main Wrapper -->
  <div class="main-wrapper mr-3 h-full overflow-hidden">
    <v-alert
      v-if="alertVisible"
      position="absolute"
      location="top center"
      color="red-lighten-3"
      icon="$error"
      style="z-index: 3000; margin-top: 15px"
      closable
    >
      <div v-html="message"></div>
    </v-alert>
    <!-- Page Content -->
    <div class="card p-4 m-4" style="height: calc(100% - 50px);">
      <div class="actions flex pb-4">
        <v-btn 
        prepend-icon="pi pi-plus" 
        color="green" 
        rounded="lg" 
        class="mr-2 text-none" 
        @click="openNew"
        >
          Add Patient
        </v-btn>
        <v-btn 
        v-if="selectedRows && selectedRows.length" 
        prepend-icon="pi pi-trash" 
        color="red" 
        rounded="lg" 
        @click="deleteRowsDialog = true" 
        class="text-none" 
        >
          Delete
        </v-btn>
      </div>
      <div class="filters flex flex-wrap flex-col pb-2">
        <a-input v-model:value="filters['global'].value" placeholder="Search" size="large" style="width: 450px;">
          <template #prefix>
            <v-icon icon="mdi mdi-magnify" color="grey"></v-icon>
          </template>
        </a-input>
      </div>
      <DataTable 
      :value="patients" 
      paginator 
      :rows="20" 
      removableSort 
      :rowsPerPageOptions="[20, 100, 500, 2500]"
      v-model:filters="filters"
      :globalFilterFields="['custom_cpr', 'patient_name', 'mobile', 'email', 'custom_file_number']"
      selectionMode="single"
      @row-click="openRow"
      v-model:selection="selectedRows"
      dataKey="name"
      >
        <template #empty> No Patients found </template>
        <Column selectionMode="multiple" headerStyle="width: 3rem"></Column>
        <Column header="Full Name" field="patient_name" sortable></Column>
        <Column header="CPR" field="custom_cpr" sortable></Column>
        <Column header="File Number" field="custom_file_number" sortable></Column>
        <Column header="Age" field="age" sortable></Column>
        <Column header="Mobile" field="mobile" sortable></Column>
        <Column header="Email" field="email" sortable></Column>
      </DataTable>
    </div>
    <v-overlay
      :model-value="loadingOverlay"
      class="align-center justify-center"
    >
      <v-progress-circular
        color="primary"
        size="64"
        indeterminate
      ></v-progress-circular>
    </v-overlay>
  </div>
</template>
  
<script >
import { ListView } from 'frappe-ui'
import { FilterMatchMode } from '@primevue/core/api';

import {VIcon} from 'vuetify/components/VIcon';
import {VToolbar, VToolbarItems} from 'vuetify/components/VToolbar';

export default {
  inject: ['$socket', '$call'],
  components: {
    ListView, VIcon, VToolbar, VToolbarItems,
  },
  data() {
    return {
      selectedRows: null,
      patients: [],
      filters: {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS },
      },
      searchFilter: '',
      alertVisible: false,
    };
  },
  created() {
    this.fetchRecords();
    this.$socket.on('patients', response => {
      if(response){
        response.age = this.calculateAge(response.dob)
        this.patients = response
      }
    })
  },
  methods: {
    showAlert(message, duration) {
      this.message = message;
      this.alertVisible = true;
      setTimeout(() => {
        this.alertVisible = false;
      }, duration);
    },
    fetchRecords() {
      this.loadingOverlay = true;
      this.$call('frappe.client.get_list', {
        doctype: 'Patient', 
        fields: ['name', 'patient_name', 'custom_cpr', 'sex', 'dob', 'mobile', 'email', 'custom_file_number'],
        order_by: 'name',
        limit_page_length: null
      }).then(response => {
        this.patients = response.map(patient => {
          patient.age = this.calculateAge(patient.dob)
          return patient
        })
        this.loadingOverlay = false;
      })
      .catch(error => {
        this.loadingOverlay = false;
        console.error('Error fetching records:', error);
      });
    },
    openNew() {
      this.$router.push({ name: 'patient', params: { patientId: 'new-patient' } });
    },
    openRow({data}) {
      this.$router.push({ name: 'patient', params: { patientId: data.name } });
    },
    calculateAge(birthdate) {
      const today = new Date();
      const birthDate = new Date(birthdate);
      let age = today.getFullYear() - birthDate.getFullYear();
      const monthDifference = today.getMonth() - birthDate.getMonth();

      // If the current month is before the birth month or it's the same month but the day hasn't passed, subtract 1 from age
      if (monthDifference < 0 || (monthDifference === 0 && today.getDate() < birthDate.getDate())) {
        age--;
      }

      return age + '';
    }
  },
  name: 'Patients List',
};
</script>
  
<style>
/* Hide the ListSelectBanner */
.editable-table .absolute.inset-x-0.bottom-6.mx-auto.w-max.text-base {
  display: none !important;
}
</style>  