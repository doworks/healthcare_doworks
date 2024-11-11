<template>
  <v-dialog v-model="dialogVisible" width="auto" scrollable>
    <ConfirmDialog group="delete-biocom" >
      <template #container="{ message, acceptCallback, rejectCallback }">
        <div class="flex flex-col items-center p-8 bg-surface-0 dark:bg-surface-900 rounded">
          <div class="rounded-full bg-black text-primary-contrast inline-flex justify-center items-center h-24 w-24 -mt-20">
            <i class="pi pi-question"></i>
          </div>
          <span class="font-bold text-2xl block mb-2 mt-6">{{ message.header }}</span>
          <p class="mb-0">{{ message.message }}</p>
          <div class="flex items-center gap-2 mt-6">
            <Button label="Cancel" severity="secondary" outlined @click="rejectCallback" class="w-32"></Button>
            <Button label="Close" severity="danger" @click="acceptCallback" class="w-32"></Button>
          </div>
        </div>
      </template>
    </ConfirmDialog>
    <v-card rounded="lg">
      <v-card-title class="d-flex justify-space-between align-center">
        <div class="text-h5 text-medium-emphasis ps-2">BIOCOM</div>
        <v-btn icon="mdi mdi-close" variant="text" @click="closeDialog"></v-btn>
      </v-card-title>
      <v-divider class="m-0"></v-divider>
      <v-card-text>
        <a-form layout="vertical" :model="form" :rules="rules">
          <v-container>
            <v-row>
              <v-col cols="12">
                <DataTable 
                :value="$resources.biocoms.data" 
                v-model:selection="selectedRows"
                editMode="cell" 
                @cell-edit-complete="onCellEditComplete"
                :pt="{
                  table: { style: 'min-width: 50rem; width: 800px' },
                  column: {
                    columnHeaderContent : {
                      class: 'justify-center'
                    },
                    bodycell: ({ state }) => ({
                      class: [{ 'pt-0 pb-0': state['d_editing'] }, 'text-center']
                    })
                  }
                }"
                >
                  <template #empty> No BIOCOM found </template>
                  <ColumnGroup type="header">
                    <Row>
                      <Column :rowspan="3"/>
                      <Column header="Date" :rowspan="3" field="date"/>
                      <Column header="Pressure" :rowspan="3" field="pressure"/>
                      <Column field="location" :rowspan="3"/>
                    </Row>
                    <Row>
                      <Column header="Left" class="bg-indigo" :colspan="2"/>
                      <Column header="Right" class="bg-indigo" :colspan="2"/>
                    </Row>
                    <Row>
                      <Column header="Before" class="bg-pink-lighten-5" field="beforeLeft"/>
                      <Column header="After" class="bg-blue-lighten-5" field="afterLeft"/>
                      <Column header="Before" class="bg-pink-lighten-5" field="beforeRight"/>
                      <Column header="After" class="bg-blue-lighten-5" field="afterRight"/>
                    </Row>
                  </ColumnGroup>
                  <Column selectionMode="multiple" headerStyle="width: 3rem"></Column>
                  <Column field="date" style="width: 20%">
                    <template #body="{ data }">
                      {{ data.dateFormat }}
                    </template>
                    <template #editor="{ data }">
                      <a-date-picker
                      v-model:value="data.dayDate"
                      format="D/MM/YYYY"
                      style="width: 100%; align-items: center; max-height: 62px; text-align: center"
                      :allowClear="false"
                      />
                    </template>
                  </Column>
                  <Column field="pressure" style="width: 20%">
                    <template #body="{ data }">
                      {{ data.pressure }}
                    </template>
                    <template #editor="{ data }">
                      <a-input v-model:value="data.pressure"/>
                    </template>
                  </Column>
                  <Column field="location" style="width: 10%">
                    <template #body="{ data }">
                      Upper<br>Lower
                    </template>
                  </Column>
                  <Column field="beforeLeft" class="bg-pink-lighten-5" style="width: 12.5%">
                    <template #body="{ data }">
                      {{ data.before_upper_left }}<br>{{ data.before_lower_left }}
                    </template>
                    <template #editor="{ data }">
                      <a-input v-model:value="data.before_upper_left"/>
                      <a-input v-model:value="data.before_lower_left"/>
                    </template>
                  </Column>
                  <Column field="afterLeft" class="bg-blue-lighten-5" style="width: 12.5%">
                    <template #body="{ data }">
                      {{ data.after_upper_left }}<br>{{ data.after_lower_left }}
                    </template>
                    <template #editor="{ data }">
                      <a-input v-model:value="data.after_upper_left"/>
                      <a-input v-model:value="data.after_lower_left"/>
                    </template>
                  </Column>
                  <Column field="beforeRight" class="bg-pink-lighten-5" style="width: 12.5%">
                    <template #body="{ data }">
                      {{ data.before_upper_right }}<br>{{ data.before_lower_right }}
                    </template>
                    <template #editor="{ data }">
                      <a-input v-model:value="data.before_upper_right"/>
                      <a-input v-model:value="data.before_lower_right"/>
                    </template>
                  </Column>
                  <Column field="afterRight" class="bg-blue-lighten-5" style="width: 12.5%">
                    <template #body="{ data }">
                      {{ data.after_upper_right }}<br>{{ data.after_lower_right }}
                    </template>
                    <template #editor="{ data }">
                      <a-input v-model:value="data.after_upper_right"/>
                      <a-input v-model:value="data.after_lower_right"/>
                    </template>
                  </Column>
              </DataTable>
              </v-col>
            </v-row> 
          </v-container>
        </a-form>
      </v-card-text>    

      <v-card-actions class="my-2 d-flex justify-end">
      <v-btn
      class="text-none"
      color="red"

      text="Delete"
      @click="confirmDelete"
      :disabled="!selectedRows || selectedRows.length == 0"
      ></v-btn>
      <v-btn
      class="text-none"
      color="green"
      
      text="Add row"
      variant="tonal"
      @click="addRow"
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
    appointment: {default: {}},
  },
  resources: {
    biocoms() { return { 
      type: 'list', 
      doctype: 'Biocom', 
      fields: ['name', 'date', 'pressure', 'appointment', 
        'before_upper_left', 'before_lower_left', 'before_upper_right', 'before_lower_right',
        'after_upper_left', 'after_lower_left', 'after_upper_right', 'after_lower_right'
      ], 
      filters: {patient: this.appointment.patient},
      auto: true, 
      pageLength: 10,
      orderBy: 'date desc',
      transform(data) {
        return data.map(biocom => {
          biocom.dayDate = dayjs(biocom.date)
          biocom.dateFormat = dayjs(biocom.date).format('D/MM/YYYY')
          return biocom
        })
      },
      insert: {
        onSuccess() {
          this.$toast.add({
            severity: 'success',
            summary: 'Success',
            detail: 'New BIOCOM inserted',
            life: 3000 // Duration in ms
          });
        },
        onError() {}
      },
      delete: {
        onSuccess() {
          this.$toast.add({
            severity: 'success',
            summary: 'Success',
            detail: 'Selected row/s deleted',
            life: 3000 // Duration in ms
          });
        },
        onError() {}
      },
      setValue: {
        onSuccess() {
          this.$toast.add({
            severity: 'success',
            summary: 'Success',
            detail: 'Biocom Saved',
            life: 3000 // Duration in ms
          });
        },
        onError() {}
      },
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
    onCellEditComplete(cell) {
      cell.newData.date = cell.newData.dayDate.format('YYYY-MM-DD')

      const keys1 = Object.keys(cell.data);
      const keys2 = Object.keys(cell.newData);
      // If they have different numbers of keys, exit
      if (keys1.length !== keys2.length) return;
      // Check each key in data to see if it exists in newData and has the same value
      if(keys1.every(value => cell.data[value] == cell.newData[value])) return;

      this.$resources.biocoms.setValue.submit(cell.newData)
    },
    addRow() {
      this.$resources.biocoms.insert.submit({
        appointment: this.appointment.name,
        patient: this.appointment.patient,
        date: dayjs().format('YYYY-MM-DD')
      })
    },
    confirmDelete(event) {
      this.$confirm.require({
        target: event.currentTarget,
        group: 'delete-biocom',
        header: 'Are you sure?',
        message: 'Do you really want to delete the selected row/s',
        icon: 'pi pi-info-circle',
        acceptLabel: 'Delete',
        rejectLabel: 'Cancel',
        acceptProps: {
          severity: 'danger'
        },
        rejectProps: {
          severity: 'secondary'
        },
        accept: () => {
          this.selectedRows.forEach(value => {
            this.$resources.biocoms.delete.submit(value.name)
          })
        },
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