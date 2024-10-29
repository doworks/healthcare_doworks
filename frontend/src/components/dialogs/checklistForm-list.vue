<template>
  <div>
    <v-dialog v-model="dialogVisible" width="auto" scrollable>
      <v-card rounded="lg">
        <v-card-title class="d-flex justify-space-between align-center">
          <div class="text-h5 text-medium-emphasis ps-2">Checklist Forms</div>
          <v-btn icon="mdi mdi-close" variant="text" @click="closeDialog"></v-btn>
        </v-card-title>
        <Menubar :model="actions" />
        <DataTable 
        v-model:selection="selectedSigns" 
        :metaKeySelection="true"
        selectionMode="multiple" 
        :value="this.$resources.checklistForms.data" 
        dataKey="name" 
        tableStyle="min-width: 50rem"
        :rowClass="rowClass"
        @row-click="openChecklistForm"
        >
          <template #empty>
            <div class="p-3 flex flex-col">
              <h5 class="mb-4 text-center">No Checklist Form</h5>
              <v-btn prepend-icon="pi pi-plus" rounded="lg" elevation="1" class="self-center text-none" @click="() => {
                this.selectedRow = null
                this.checklistFormOpen = true
              }">
                Add Checklist Form
              </v-btn>
            </div>
          </template>
          <Column selectionMode="multiple" headerStyle="width: 3rem"></Column>
          <Column field="name" header="Name"></Column>
          <Column field="form_template" header="Form Template"></Column>
        </DataTable>
      </v-card>
      <v-overlay :model-value="lodingOverlay" class="align-center justify-center">
        <v-progress-circular color="primary" size="64" indeterminate></v-progress-circular>
      </v-overlay>
    </v-dialog>
    <checklistFormDialog 
    :isOpen="checklistFormOpen" 
    @update:isOpen="checklistFormOpen = $event" 
    @show-alert="(message, type) => {$emit('show-alert', message, type)}" 
    :appointment="appointment" 
    :name="selectedRow"
    :callback="$resources.checklistForms.reload"
    />
  </div>
</template>

<script >
import dayjs from 'dayjs';
import { ref } from 'vue';
import { VContainer, VCol, VRow } from 'vuetify/components/VGrid';
import { VDivider } from 'vuetify/components/VDivider';
import { VInfiniteScroll } from 'vuetify/components/VInfiniteScroll';
import { VItemGroup, VItem } from 'vuetify/components/VItemGroup';
import { VToolbar, VToolbarItems } from 'vuetify/components/VToolbar';
import { VEmptyState } from 'vuetify/labs/VEmptyState';

export default {
	inject: ['$call'],
	components: {
		VDivider, VContainer, VCol, VRow, VInfiniteScroll, VItemGroup, VItem, VToolbar, VToolbarItems, VEmptyState,
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
	},
  resources: {
		checklistForms() { return { 
			type: 'list', 
			doctype: 'Checklist Form', 
			fields: ['name', 'form_template'], 
			filters: {'appointment': this.appointment.name},
			auto: true, 
		}},
  },
	data() {
		return {
      lodingOverlay: false,
      selectedRow: ref(''),
      checklistFormOpen: false,

      actions: [
        {
          label: 'Add Checklist Form',
          icon: 'pi pi-plus',
          command: () => {
            this.selectedRow = null
            this.checklistFormOpen = true
          }
        },
          // {
          //     label: 'Features',
          //     icon: 'pi pi-star'
          // },
      ],
		};
	},
  mounted() {
    this.selectedSigns = []
    this.selectedRow = ''
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
	methods: {
    updateIsOpen(value) {
      this.$emit('update:isOpen', value);
    },
    closeDialog() {
      this.updateIsOpen(false);
    },
    openChecklistForm({ data }) {
      this.selectedRow = data.name
      this.checklistFormOpen = true
    },
    rowClass(data) {
      return [{ '!bg-ski-100 hover:!bg-ski-200': data.appointment === this.appointment.name }];
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