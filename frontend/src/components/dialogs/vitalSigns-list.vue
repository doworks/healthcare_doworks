<template>
    <div>
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
                selectionMode="single" 
                :value="vitalSigns" 
                dataKey="name" 
                tableStyle="min-width: 50rem"
                :rowClass="rowClass"
                @row-click="openVitalSigns"
                >
                    <Column selectionMode="multiple" headerStyle="width: 3rem"></Column>
                    <Column field="title" header="Title"></Column>
                    <Column field="patient" header="Patient"></Column>
                    <Column field="temprature" header="Body Temprature"></Column>
                    <Column field="pulse" header="Heart Rate / Pulse"></Column>
                    <Column field="appointment" header="Patient Appointment"></Column>
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
        <vitalSignsDialog :isOpen="vsDialogOpen" @update:isOpen="vsDialogOpen = $event" @show-alert="showAlert" :appointment="appointment" :vitalSigns="selectedSigns"/>
    </div>
</template>

<script >
import dayjs from 'dayjs';

import { VContainer, VCol, VRow } from 'vuetify/components/VGrid';
import { VDivider } from 'vuetify/components/VDivider';
import { VInfiniteScroll } from 'vuetify/components/VInfiniteScroll';
import { VItemGroup, VItem } from 'vuetify/components/VItemGroup';
import { VToolbar, VToolbarItems } from 'vuetify/components/VToolbar';

export default {
	inject: ['$call'],
	components: {
		VDivider, VContainer, VCol, VRow, VInfiniteScroll, VItemGroup, VItem, VToolbar, VToolbarItems,
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
	data() {
		return {
            lodingOverlay: false,
            selectedSigns: {},
            vitalSigns: [],
            vsDialogOpen: false,
            message: '',
            alertVisible: false,
            actions: [
                {
                    label: 'Add Vital Signs',
                    icon: 'pi pi-plus',
                    command: () => {
                        console.log(this.appointment)
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
    created() {
    },
    mounted() {
    },
    watch: {
        apointment(newVal) {
            if (newVal) {
                this.fetchVitalSigns()
            }
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
        fetchVitalSigns(){
            this.lodingOverlay = true;
            this.$call('healthcare_doworks.api.methods.vital_signs_list', {patient: this.appointment.patient_details.id})
            .then(response => {
                this.vitalSigns = response.map(signs => {
                    signs.signs_date = dayjs(signs.signs_date + ' ' + signs.signs_time);
                    signs.signs_time = signs.signs_date
                    return signs
                })
                this.lodingOverlay = false;
            }).catch(error => {
                console.error(error);
                let message = error.message.split('\n');
                message = message.find(line => line.includes('frappe.exceptions'));
                if(message){
                    const firstSpaceIndex = message.indexOf(' ');
                    this.$emit('show-alert', message.substring(firstSpaceIndex + 1, 10000))
                }
                this.lodingOverlay = false;
            });
        },
        openVitalSigns(isNew = false) {
            if(isNew)
                this.selectedSigns = null
            this.vsDialogOpen = true
        },
        rowClass(data) {
            return [{ 'bg-primary': data.appointment === this.appointment.name }];
        },
	},
};
</script>