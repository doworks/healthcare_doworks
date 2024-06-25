<template>
    <v-dialog v-model="dialogVisible" width="auto" scrollable>
        <v-card rounded="lg">
            <a-form layout="vertical" :model="form">
                <v-card-title class="d-flex justify-space-between align-center">
                    <div class="text-h5 text-medium-emphasis ps-2">{{`${form.patient_name}'s visit on ${form.encounter_date}`}}</div>
                    <v-btn icon="mdi mdi-close" variant="text" @click="closeDialog"></v-btn>
                </v-card-title>
                <v-divider class="m-0"></v-divider>
                <v-card-text>
                    <v-container>
                        <v-row>
                            <v-col cols="12" md="6">
                                <a-form-item 
                                label="Appointment" 
                                name="appointment" 
                                >
                                    <a-input v-model:value="form.appointment" disabled/>
                                </a-form-item>
                                <a-form-item 
                                label="Patient" 
                                name="patient" 
                                >
                                    <a-input v-model:value="form.patient_name" disabled/>
                                </a-form-item>
                                <a-form-item 
                                label="Gender" 
                                name="patient_sex" 
                                >
                                    <a-input v-model:value="form.patient_sex"disabled/>
                                </a-form-item>
                                <a-form-item label="Age" name="patient_age">
                                    <a-input v-model:value="form.patient_age"disabled/>
                                </a-form-item>
                            </v-col>
                            <v-col cols="12" md="6">
                                <a-form-item label="Encounter Date" name="encounter_date">
                                    <a-input v-model:value="form.encounter_date" disabled/>
                                </a-form-item>
                                <a-form-item label="Encounter Time" name="encounter_time">
                                    <a-input v-model:value="form.encounter_time" disabled/>
                                </a-form-item>
                                <a-form-item label="Practitioner" name="practitioner" >
                                    <a-input v-model:value="form.practitioner"disabled/>
                                </a-form-item>
                                <a-form-item label="Department" name="medical_department">
                                    <a-input v-model:value="form.medical_department" disabled/>
                                </a-form-item>
                            </v-col>
                        </v-row>
                        <v-divider class="mt-2 mb-8"></v-divider>
                        <h3 class="mb-4">Encounter Impression</h3>
                        <v-row>
                            <v-col cols="12" md="6">
                                <a-form-item label="Symptoms" name="symptoms">
                                    <a-select
                                    v-model:value="form.symptomsArray"
                                    :options="$resources.complaints"
                                    :fieldNames="{label: 'complaints', value: 'complaints'}"
                                    mode="multiple"
                                    style="width: 100%"
                                    disabled
                                    ></a-select>
                                </a-form-item>
                            </v-col>
                            <v-col cols="12" md="6">
                                <a-form-item label="Diagnosis" name="diagnosis">
                                    <a-select
                                    v-model:value="form.diagnosisArray"
                                    :options="$resources.diagnosis"
                                    :fieldNames="{label: 'diagnosis', value: 'diagnosis'}"
                                    mode="multiple"
                                    style="width: 100%"
                                    disabled
                                    ></a-select>
                                </a-form-item>
                            </v-col>
                        </v-row>
                        <v-divider class="mt-2 mb-8"></v-divider>
                        <h3 class="mb-4">Medications</h3>
                        <div v-for="(prescription, index) in form.drug_prescription">
                            <h5>{{ index }}</h5>
                            <v-row>
                                <v-col cols="12" md="6">
                                    <a-form-item label="Medication" name="medication">
                                        <a-input v-model:value="prescription.Medication" disabled/>
                                    </a-form-item>
                                    <a-form-item label="Drug Code" name="drug_code">
                                        <a-input v-model:value="prescription.drug_code" disabled/>
                                    </a-form-item>
                                    <a-form-item label="Drug Name / Description" name="drug_name">
                                        <a-input v-model:value="prescription.drug_name" disabled/>
                                    </a-form-item>
                                    <a-form-item label="Strength" name="strength">
                                        <a-input v-model:value="prescription.strength" disabled/>
                                    </a-form-item>
                                    <a-form-item label="Strength UOM" name="strength_uom">
                                        <a-input v-model:value="prescription.strength_uom" disabled/>
                                    </a-form-item>
                                    <a-form-item label="Dosage Form" name="dosage_form">
                                        <a-input v-model:value="prescription.dosage_form" disabled/>
                                    </a-form-item>
                                </v-col>
                                <v-col cols="12" md="6">
                                    <a-form-item label="Dosage" name="dosage">
                                        <a-input v-model:value="prescription.dosage" disabled/>
                                    </a-form-item>
                                    <a-form-item label="Interval" name="interval">
                                        <a-input v-model:value="prescription.interval" disabled/>
                                    </a-form-item>
                                    <a-form-item label="Interval UOM" name="interval_uom">
                                        <a-input v-model:value="prescription.interval_uom" disabled/>
                                    </a-form-item>
                                    <a-form-item label="Period" name="period">
                                        <a-input v-model:value="prescription.period" disabled/>
                                    </a-form-item>
                                    <a-form-item label="Number Of Repeats Allowed" name="number_of_repeats_allowed">
                                        <a-input v-model:value="prescription.number_of_repeats_allowed" disabled/>
                                    </a-form-item>
                                </v-col>
                            </v-row>
                        </div>
                        <v-divider class="mt-2 mb-8"></v-divider>
                        <h3 class="mb-4">Investigation</h3>
                        <div v-for="(prescription, index) in form.lab_test_prescription">
                            <h5>{{ index }}</h5>
                            <v-row>
                                <v-col cols="12" md="6">
                                    <a-form-item label="Lab Test" name="lab_test">
                                        <a-input v-model:value="prescription.lab_test" disabled/>
                                    </a-form-item>
                                    <a-form-item label="Observation" name="observation_template">
                                        <a-input v-model:value="prescription.observation_template" disabled/>
                                    </a-form-item>
                                    <a-form-item label="Lab Test Name" name="lab_test_name">
                                        <a-input v-model:value="prescription.lab_test_name" disabled/>
                                    </a-form-item>
                                </v-col>
                                <v-col cols="12" md="6">
                                    <a-form-item label="Comments" name="lab_test_comment">
                                        <a-textarea v-model:value="prescription.lab_test_comment" :rows="4" disabled/>
                                    </a-form-item>
                                </v-col>
                            </v-row>
                        </div>
                        <h3 class="mb-4">Procedure</h3>
                        <div v-for="(prescription, index) in form.procedure_prescription">
                            <h5>{{ index }}</h5>
                            <v-row>
                                <v-col cols="12" md="6">
                                    <a-form-item label="Clinical Procedure" name="procedure">
                                        <a-input v-model:value="prescription.procedure" disabled/>
                                    </a-form-item>
                                    <a-form-item label="Procedure Name" name="procedure_name">
                                        <a-input v-model:value="prescription.procedure_name" disabled/>
                                    </a-form-item>
                                    <a-form-item label="Department" name="department">
                                        <a-input v-model:value="prescription.department" disabled/>
                                    </a-form-item>
                                    <a-form-item label="Referring Practitioner" name="practitioner">
                                        <a-input v-model:value="prescription.practitioner" disabled/>
                                    </a-form-item>
                                    <a-form-item label="Service Request" name="service_request">
                                        <a-input v-model:value="prescription.service_request" disabled/>
                                    </a-form-item>
                                </v-col>
                                <v-col cols="12" md="6">
                                    <a-form-item label="Date" name="date">
                                        <a-input v-model:value="prescription.date" disabled/>
                                    </a-form-item>
                                    <a-form-item label="Comments" name="comments">
                                        <a-input v-model:value="prescription.comments" disabled/>
                                    </a-form-item>
                                </v-col>
                            </v-row>
                        </div>
                        <h3 class="mb-4">Rehabilitation</h3>
                        <div v-for="(therapy, index) in form.therapies">
                            <h5>{{ index }}</h5>
                            <v-row>
                                <v-col cols="12">
                                    <a-form-item label="Therapy Type" name="therapy_type">
                                        <a-input v-model:value="therapy.therapy_type" disabled/>
                                    </a-form-item>
                                    <a-form-item label="No of Sessions" name="no_of_sessions">
                                        <a-input v-model:value="therapy.no_of_sessions" disabled/>
                                    </a-form-item>
                                    <a-form-item label="Sessions Completed" name="sessions_completed">
                                        <a-input v-model:value="therapy.lab_test_name" disabled/>
                                    </a-form-item>
                                    <a-form-item label="Service Request" name="service_request">
                                        <a-input v-model:value="therapy.service_request" disabled/>
                                    </a-form-item>
                                </v-col>
                            </v-row>
                        </div>
                    </v-container>
                </v-card-text>
            </a-form>
        </v-card>
    </v-dialog>
</template>

<script >
import { VBtn } from 'vuetify/components/VBtn'
import { VDialog } from 'vuetify/components/VDialog';
import { VCard, VCardTitle, VCardText, VCardActions } from 'vuetify/components/VCard';
import { VContainer, VCol, VRow } from 'vuetify/components/VGrid';
import { VDivider } from 'vuetify/components/VDivider';
import { VInfiniteScroll } from 'vuetify/components/VInfiniteScroll';
import { VItemGroup, VItem } from 'vuetify/components/VItemGroup';

export default {
	inject: ['$call'],
	components: {
		VBtn, VDialog, VCard, VCardTitle, VCardText, VCardActions, VDivider, VContainer, VCol, VRow, 
        VInfiniteScroll, VItemGroup, VItem,
	},
	props: {
		isOpen: {
            type: Boolean,
            required: true,
            default: false,
        },
        form: {
            default: {},
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
	methods: {
        updateIsOpen(value) {
            this.$emit('update:isOpen', value);
        },
        closeDialog() {
            this.updateIsOpen(false);
        },
	},
};
</script>