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
    <div class="card p-4 m-4" >
      <!-- <div class="actions flex pb-4">
        <v-btn 
        prepend-icon="pi pi-plus" 
        color="green" 
        rounded="lg" 
        class="mr-2" 
        @click="openNew"
        >
          Add Patient Encounter
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
      </div> -->
      <div class="filters flex flex-wrap flex-col pb-2">
        <a-input v-model:value="filters['global'].value" placeholder="Search" size="large" style="width: 450px;">
          <template #prefix>
            <v-icon icon="mdi mdi-magnify" color="grey"></v-icon>
          </template>
        </a-input>
      </div>
      <!-- <ListView
      :columns="columns"
      :rows="encounters"
      :options="{
        onRowClick: openRow,
        selectable: true,
        showTooltip: true,
        resizeColumn: true,
        emptyState: {
          title: 'No patient encounters found',
          description: 'Create a new patient encounter to get started',
          button: {
            label: 'New Patient Encounter',
            variant: 'solid',
            onClick: openNew,
          },
        },
      }"
      @update:selections="(selections) => {selectedRows = Array.from(selections)}"
      row-key="name"
      /> -->
      <DataTable 
      :value="encounters" 
      paginator 
      :rows="20" 
      removableSort 
      :rowsPerPageOptions="[20, 100, 500, 2500]"
      v-model:filters="filters"
      :globalFilterFields="['name', 'patient_name', 'practitioner_name', 'status']"
      selectionMode="single"
      @row-click="openRow"
      v-model:selection="selectedRows"
      dataKey="name"
      >
        <template #empty> No Patient Encounters found </template>
        <Column selectionMode="multiple" headerStyle="width: 3rem"></Column>
        <Column header="Title" field="title" sortable style="width: 25%"></Column>
        <Column header="Status" field="status" sortable style="width: 25%"></Column>
        <Column header="Encounter Date" field="encounter_date" sortable style="width: 25%"></Column>
        <Column header="ID" field="name" sortable style="width: 25%"></Column>
      </DataTable>
    </div>

    <!-- <v-dialog v-model="rowDialog" :width="dialogWidth">
      <v-card :title="title">
        <template v-slot:text>
          <slot name="dialog" :row="row"></slot>
        </template>
        <v-card-actions>
          <v-btn prepend-icon="mdi mdi-close" size="small" variant="text" @click="hideDialog">Cancel</v-btn>
          <v-btn prepend-icon="mdi mdi-check" size="small" variant="flat" color="green" @click="saveItem(row)">Save</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="deleteRowsDialog" header="Confirm" width="auto">
      <v-card title="Confirm">
        <template v-slot:text>
          <div class="flex items-center gap-4">
            <i class="pi pi-exclamation-triangle !text-3xl" />
            <span v-if="selectedRows.length == 1">Are you sure you want to delete this encounter?</span>
            <span v-else>Are you sure you want to delete the selected encounters?</span>
          </div>
        </template>
        
        <v-card-actions>
          <v-btn
            text="No"
            variant="text"
            @click="deleteRowsDialog = false"
          ></v-btn>
          <v-btn
            text="Yes"
            variant="text"
            @click="deleteSelectedRows"
          ></v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog> -->

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
import { FilterMatchMode } from 'primevue/api';

import {VIcon} from 'vuetify/components/VIcon';
import {VToolbar, VToolbarItems} from 'vuetify/components/VToolbar';
import {VDialog} from 'vuetify/components/VDialog';

export default {
  inject: ['$socket', '$call'],
  components: {
    ListView, VIcon, VToolbar, VToolbarItems, VDialog,
  },
  data() {
    return {
      alertVisible: false,
      deleteRowsDialog: false,
      selectedRows: null,
      encounters: [],
      columns: [
        {label: 'Title', key: 'title'},
        {label: 'Status', key: 'status'},
        {label: 'Encounter Date', key: 'encounter_date'},
        {label: 'Practitioner Name', key: 'practitioner_name'},
        {label: 'ID', key: 'name'},
      ],
      searchFilter: '',
      filters: {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS },
      },
    };
  },
  created() {
    this.fetchRecords();
    this.$socket.on('patient_encounters_updated', response => {
      if(response){
        this.encounters = response
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
        doctype: 'Patient Encounter', 
        fields: ['name', 'title', 'status', 'encounter_date', 'practitioner_name'],
        order_by: 'modified desc',
        limit_page_length: null
      }).then(response => {
        this.encounters = response
        this.loadingOverlay = false;
      })
      .catch(error => {
        this.loadingOverlay = false;
        console.error('Error fetching records:', error);
      });
    },
    openNew() {
      console.log(this.selectedRows)
      this.row = {};
      this.rowDialog = true;
    },
    openRow({data}) {
      this.$router.push({ name: 'patient-encounter', params: { encounterId: data.name } });
    },
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