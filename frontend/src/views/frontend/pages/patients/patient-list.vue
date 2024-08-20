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
        class="mr-2" 
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
        >
          Delete
        </v-btn>
      </div>
      <div class="filters flex flex-wrap flex-col pb-2">
        <a-input v-model:value="searchFilter" placeholder="Search" size="large" style="width: 450px;">
          <template #prefix>
            <v-icon icon="mdi mdi-magnify" color="grey"></v-icon>
          </template>
        </a-input>
      </div>
      <ListView
      :columns="columns"
      :rows="patients"
      :options="{
        onRowClick: openRow,
        selectable: true,
        showTooltip: true,
        resizeColumn: true,
        emptyState: {
          title: 'No patients found',
          description: 'Create a new patient to get started',
          button: {
            label: 'New Patient',
            variant: 'solid',
            onClick: openNew,
          },
        },
      }"
      @update:selections="(selections) => {selectedRows = Array.from(selections)}"
      row-key="name"
      />
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
      columns: [
        {label: 'Full Name', key: 'patient_name'},
        {label: 'CPR', key: 'custom_cpr'},
        {label: 'Gender', key: 'sex'},
        {label: 'Age', key: 'age'},
        {label: 'Mobile', key: 'mobile'},
        {label: 'Email', key: 'email'},
      ],
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
  mounted() {
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
        order_by: 'name'
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
      this.row = {};
      this.rowDialog = true;
    },
    openRow(row) {
      this.$router.push({ name: 'patient', params: { patientId: row.name } });
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

      return age;
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