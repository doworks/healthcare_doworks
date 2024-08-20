<template>
  <div>
    <div class="card">
      <div class="d-flex m-2">
        <v-btn 
        prepend-icon="pi pi-plus" 
        color="green" 
        rounded="lg" 
        size="small" 
        class="mr-2" 
        @click="openNew"
        >
          New
        </v-btn>
        <v-btn 
        v-if="selectedRows && selectedRows.length"
        prepend-icon="pi pi-trash" 
        color="red" 
        rounded="lg" 
        size="small" 
        @click="deleteRowsDialog = true" 
        >
          Delete
        </v-btn>
      </div>
      <div class="editable-table mb-2">
        <ListView
        class="max-h-[250px]"
        :columns="columns"
        :rows="items"
        :options="{
          onRowClick: editRow,
          selectable: true,
          showTooltip: true,
          resizeColumn: true,
          emptyState: {
            title: 'No records found',
            description: 'Create a new record to get started',
            button: {
              label: 'New Record',
              variant: 'solid',
              onClick: openNew,
            },
          },
        }"
        @update:selections="(selections) => {selectedRows = Array.from(selections)}"
        row-key="name"
        />
      </div>
    </div>

    <v-dialog v-model="rowDialog" width="450px">
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
            <span v-if="selectedRows.length == 1">Are you sure you want to delete this row?</span>
            <span v-else>Are you sure you want to delete the selected items?</span>
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
    </v-dialog>
  </div>
</template>

<script>
import { FilterMatchMode } from 'primevue/api';
import { ListView } from 'frappe-ui'

export default {
  props: {
    rows: {
      default: []
    },
    columns: {
      default: []
    },
    title: {
      type: String,
      default: '',
    },
  },
  components: { ListView },
  data() {
    return {
      items: this.rows,
      rowDialog: false,
      deleteRowsDialog: false,
      row: {},
      selectedRows: null,
      filters: {'global': {value: null, matchMode: FilterMatchMode.CONTAINS}},
    }
  },
  methods: {
    openNew() {
      this.row = {};
      this.rowDialog = true;
    },
    editRow(row) {
      this.row = row;
      this.rowDialog = true;
    },
    hideDialog() {
      this.rowDialog = false;
    },
    saveItem(row) {
      if (row) {
        if (row.name) {
          delete row.modified
          delete row.modified_by
          this.items[this.findIndexById(row.name)] = row;
          this.$toast.add({severity:'success', summary: 'Updated', detail: this.title + ' Updated', life: 3000});
        }
        else {
          row.name = this.createId();
          this.items.push(row);
          this.$toast.add({severity:'success', summary: 'Created', detail: this.title + ' Created', life: 3000});
        }

        this.rowDialog = false;
        this.row = {};
        this.$emit('update', this.items)
      }
    },
    findIndexById(id) {
      let index = -1;
      for (let i = 0; i < this.items.length; i++) {
        if (this.items[i].name === id) {
          index = i;
          break;
        }
      }

      return index;
    },
    createId() {
      let id = '';
      var chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
      for ( var i = 0; i < 10; i++ ) {
        id += chars.charAt(Math.floor(Math.random() * chars.length));
      }
      return id;
    },
    deleteSelectedRows() {
      this.items = this.items.filter(val => !this.selectedRows.includes(val.name));
      this.deleteRowsDialog = false;
      this.selectedRows = [];
      this.$toast.add({severity:'success', summary: 'Deleted', detail: 'Items Deleted', life: 3000});
      this.$emit('update', this.items)
    },
  }
}
</script>

<style>
/* Hide the ListSelectBanner */
.absolute.inset-x-0.bottom-6.mx-auto.w-max.text-base {
  display: none !important;
}

</style>