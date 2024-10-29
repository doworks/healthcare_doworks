<template>
    <div>
        <v-dialog v-model="dialogVisible" width="auto" scrollable>
            <v-card rounded="lg">
                <v-card-title class="d-flex justify-space-between align-center">
                    <div class="text-h5 text-medium-emphasis ps-2">Vital Signs</div>
                    <v-btn icon="mdi mdi-close" variant="text" @click="closeDialog"></v-btn>
                </v-card-title>
                <Menubar :model="actions" />
                <DataTable 
                v-model:selection="selectedSigns" 
                :metaKeySelection="true"
                selectionMode="multiple" 
                :value="$resources.vitalSigns.data" 
                dataKey="name" 
                tableStyle="min-width: 50rem"
                :rowClass="rowClass"
                @row-click="openVitalSigns"
                >
                    <template #empty>
                        <div class="p-3 flex flex-col">
                            <h5 class="mb-4 text-center">No Vital Signs</h5>
                            <v-btn prepend-icon="pi pi-plus" rounded="lg" elevation="1" class="self-center text-none" @click="() => {
                                selectedRow = null
                                vsDialogOpen = true
                            }">
                                Add Vital Signs
                            </v-btn>
                        </div>
                    </template>
                    <Column selectionMode="multiple" headerStyle="width: 3rem"></Column>
                    <Column field="name" header="Name"></Column>
                    <Column field="patient_name" header="Patient"></Column>
                    <Column field="signs_date" header="Date">
                        <template #body="{ data }">
                            {{ data.signs_date.format('DD/MM/YYYY') }}
                        </template>
                    </Column>
                    <Column field="signs_time" header="Time">
                        <template #body="{ data }">
                            {{ data.signs_date.format('h:mm a') }}
                        </template>
                    </Column>
                    <Column field="modified_by" header="Modified By"></Column>
                </DataTable>
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
        <vitalSignsDialog 
        :isOpen="vsDialogOpen" 
        @update:isOpen="vsDialogOpen = $event" 
        @show-alert="(message, type) => {$emit('show-alert', message, type)}" 
        :appointment="appointment" 
        :name="selectedRow"
        :callback="$resources.vitalSigns.reload"
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
		vitalSigns() { return { 
			type: 'list', 
			doctype: 'Vital Signs', 
			fields: ['signs_date', 'signs_time', 'patient_name', 'name', 'appointment', 'modified', 'modified_by', 'patient'], 
			filters: {'patient': this.appointment.patient},
			auto: true, 
			orderBy: 'signs_date desc, signs_time desc',
			pageLength: 1000,
			transform(data) {
				data = data.map(signs => {
                    signs.signs_date = dayjs(signs.signs_date + ' ' + signs.signs_time);
                    signs.signs_time = signs.signs_date
                    return signs
                })
                return data
			},
		}},
  	},
	data() {
		return {
            lodingOverlay: false,
            selectedSigns: [],
            selectedRow: ref(''),
            vitalSigns: [],
            vsDialogOpen: false,
            message: '',
            alertVisible: false,
            actions: [
                {
                    label: 'Add Vital Signs',
                    icon: 'pi pi-plus',
                    command: () => {
                        this.selectedRow = null
                        this.vsDialogOpen = true
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
        showAlert(message, duration) {
            this.message = message;
            this.alertVisible = true;
        },
        updateIsOpen(value) {
            this.$emit('update:isOpen', value);
        },
        closeDialog() {
            this.updateIsOpen(false);
        },
        openVitalSigns({ data }) {
            this.selectedRow = data.name
            this.vsDialogOpen = true
        },
        rowClass(data) {
            return [{ '!bg-ski-100 hover:!bg-ski-200': data.appointment === this.appointment.name }];
        },
	},
};
</script>