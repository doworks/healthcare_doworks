<template>
    <v-dialog v-model="dialogVisible" width="1400px" scrollable>
        <v-card rounded="lg">
            <v-card-title class="d-flex justify-space-between align-center">
                <div class="text-h5 text-medium-emphasis ps-2">{{ patient.patient_name }} Medical History</div>
                <v-btn icon="mdi mdi-close" variant="text" @click="closeDialog"></v-btn>
            </v-card-title>
            <v-divider class="m-0"></v-divider>
            <v-card-text>
                <v-container fluid>
                    <v-row>
                        <v-col cols="12" lg="6">
                            <h5>Allergies</h5>
                            <EditableTable :columns="[
                                {label: 'Type', key: 'type', width: 3},
                                {label: 'Severity', key: 'severity', width: 2},
                                {label: 'Note', key: 'note', width: '270px'},
                            ]"
                            :rows="allergies"
                            @update="(items) => {allergies = items}"
                            title="Allergies"
                            >
                                <template v-slot:dialog="{ row }">
                                    <a-form layout="vertical">
                                        <a-form-item label="Type">
                                            <a-select
                                            v-model:value="row.type"
                                            :options="allergiesOptions"
                                            ></a-select>
                                        </a-form-item>
                                        <a-form-item label="Severity">
                                            <a-select
                                            v-model:value="row.severity"
                                            :options="severityOptions"
                                            ></a-select>
                                        </a-form-item>
                                        <a-form-item label="Note">
                                            <a-textarea v-model:value="row.note" :rows="4" />
                                        </a-form-item>
                                    </a-form>
                                </template>
                            </EditableTable>
                        </v-col>
                        <v-col cols="12" lg="6">
                            <h5>Medical History</h5>
                            <EditableTable :columns="[
                                {label: 'Name', key: 'name1'},
                                {label: 'Note', key: 'note', width: '320px'},
                            ]"
                            :rows="infectedDiseases"
                            @update="(items) => {infectedDiseases = items}"
                            title="Medical History"
                            >
                                <template v-slot:dialog="{ row }">
                                    <a-form layout="vertical">
                                        <a-form-item label="Name">
                                            <a-input v-model:value="row.name1"/>
                                        </a-form-item>
                                        <a-form-item label="Note">
                                            <a-textarea v-model:value="row.note" :rows="4" />
                                        </a-form-item>
                                    </a-form>
                                </template>
                            </EditableTable>
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col cols="12" lg="6">
                            <h5>Surgical History</h5>
                            <EditableTable :columns="[
                                {label: 'Surgery', key: 'surgery'},
                                {label: 'Date', key: 'date'},
                                {label: 'Practitioner', key: 'practitioner'},
                                {label: 'Note', key: 'notes', width: '150px'},
                            ]"
                            :rows="surgicalHistory"
                            @update="(items) => {surgicalHistory = items}"
                            title="Surgical History"
                            >
                                <template v-slot:dialog="{ row }">
                                    <a-form layout="vertical">
                                        <a-form-item label="Surgery">
                                            <a-input v-model:value="row.surgery"/>
                                        </a-form-item>
                                        <a-form-item label="Date">
                                            <a-date-picker 
                                            v-model:value="row.dayDate"
                                            format="DD/MM/YYYY" 
                                            style="z-index: 3000"
                                            @change="date => {row.date = date.format('YYYY-MM-DD') }"
                                            />
                                        </a-form-item>
                                        <a-form-item label="Practitioner">
                                            <a-input v-model:value="row.practitioner"/>
                                        </a-form-item>
                                        <a-form-item label="Note">
                                            <a-textarea v-model:value="row.notes" :rows="4" />
                                        </a-form-item>
                                    </a-form>
                                </template>
                            </EditableTable>
                        </v-col>
                        <v-col cols="12" lg="6">
                            <h5>Medications</h5>
                            <EditableTable :columns="[
                                {label: 'Name', key: 'name1'},
                                {label: 'Reason', key: 'reason'},
                                {label: 'From Date', key: 'from_date'},
                                {label: 'Status', key: 'status', }
                            ]"
                            :rows="medications"
                            @update="(items) => {medications = items}"
                            title="Medications"
                            >
                                <template v-slot:dialog="{ row }">
                                    <a-form layout="vertical">
                                        <a-form-item label="Name">
                                            <a-input v-model:value="row.name1"/>
                                        </a-form-item>
                                        <a-form-item label="Reason">
                                            <a-input v-model:value="row.reason"/>
                                        </a-form-item>
                                        <a-form-item label="From Date">
                                            <a-date-picker 
                                            v-model:value="row.dayDate"
                                            format="DD/MM/YYYY" 
                                            style="z-index: 3000"
                                            @change="date => {row.from_date = date.format('YYYY-MM-DD') }"
                                            />
                                        </a-form-item>
                                        <a-form-item label="Status">
                                            <a-checkbox 
                                            v-model:checked="row.is_active" 
                                            @change="e => {row.status = e.target.chicked ? 'Active' : 'Inactive' }"
                                            />
                                        </a-form-item>
                                    </a-form>
                                </template>
                            </EditableTable>
                        </v-col>
                    </v-row>
                    <v-row>
                        <v-col cols="12" lg="6">
                            <h5>Habits / Social</h5>
                            <EditableTable :columns="[
                                {label: 'Habit', key: 'habit', width: 3},
                                {label: 'Note', key: 'note', width: '270px'},
                            ]"
                            :rows="habits"
                            @update="(items) => {habits = items}"
                            title="Habits / Social"
                            >
                                <template v-slot:dialog="{ row }">
                                    <a-form layout="vertical">
                                        <a-form-item label="Habit">
                                            <a-select
                                                v-model:value="row.habit"
                                                :options="habitsOptions"
                                            ></a-select>
                                        </a-form-item>

                                        <a-form-item label="Note">
                                            <a-textarea v-model:value="row.note" :rows="4" />
                                        </a-form-item>
                                    </a-form>
                                </template>
                            </EditableTable>
                        </v-col>
                        <v-col cols="12" lg="6">
                            <h5>Risk Factors</h5>
                            <EditableTable :columns="[
                                {label: 'Type', key: 'type', width: 3},
                                {label: 'Severity', key: 'severity', width: 2},
                                {label: 'Note', key: 'note', width: '270px'},
                            ]"
                            :rows="riskFactors"
                            @update="(items) => {riskFactors = items}"
                            title="Risk Factors"
                            >
                                <template v-slot:dialog="{ row }">
                                    <a-form layout="vertical">
                                        <a-form-item label="Type">
                                            <a-select
                                            v-model:value="row.type"
                                            :options="riskFactorsOptions"
                                            ></a-select>
                                        </a-form-item>
                                        <a-form-item label="Severity">
                                            <a-select
                                            v-model:value="row.severity"
                                            :options="severityOptions"
                                            ></a-select>
                                        </a-form-item>
                                        <a-form-item label="Note">
                                            <a-textarea v-model:value="row.note" :rows="4" />
                                        </a-form-item>
                                    </a-form>
                                </template>
                            </EditableTable>
                        </v-col>
                    </v-row>
                    <v-divider class="m-10"></v-divider>
                    <a-form layout="vertical">
                        <h5 class="mb-4">Family History</h5>
                        <v-row>
                            <v-col cols="12" lg="6">
                                <a-form-item label="Chronic Diseases">
                                    <a-textarea v-model:value="chronicDiseases" :rows="4" />
                                </a-form-item>
                            </v-col>
                            <v-col cols="12" lg="6">
                                <a-form-item label="Genetic Diseases">
                                    <a-textarea v-model:value="geneticDiseases" :rows="4" />
                                </a-form-item>
                            </v-col>
                        </v-row>
                    </a-form>
                </v-container>
            </v-card-text>
            
            <v-divider class="m-0"></v-divider>
            
            <v-card-actions class="my-2 d-flex justify-end">
            <v-btn
            class="text-none"
            text="Cancel"
            @click="closeDialog"
            ></v-btn>
            <v-btn
            class="text-none"
            color="blue"
            text="Save"
            variant="tonal"
            @click="onSubmit()"
            type="submit"
            ></v-btn>
            </v-card-actions>
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
</template>

<script >
import dayjs from 'dayjs';

import { VDivider } from 'vuetify/components/VDivider';
import { VInfiniteScroll } from 'vuetify/components/VInfiniteScroll';
import { VItemGroup, VItem } from 'vuetify/components/VItemGroup';
import { VOverlay } from 'vuetify/components/VOverlay';
import { VProgressCircular } from 'vuetify/components/VProgressCircular';
import EditableTable from '../editableTable.vue';

export default {
	inject: ['$call'],
	components: {
		VDivider, VInfiniteScroll, VItemGroup, VItem, VOverlay, VProgressCircular,
	},
	props: {
		isOpen: {
            type: Boolean,
            required: true,
            default: false,
        },
        patient: {
            required: true,
            default: {
                patient: '',
                name: '',
            }
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
	data() {
		return {
            lodingOverlay: false,
            severityOptions: [
                {label: '0', value: '0'},
                {label: '1', value: '1'},
                {label: '2', value: '2'},
                {label: '3', value: '3'},
                {label: '4', value: '4'},
                {label: '5', value: '5'},
            ],
            habitsOptions: [
                {label: 'Smoking', value: 'Smoking'},
                {label: 'Alcohol', value: 'Alcohol'},
                {label: 'Vegetarian', value: 'Vegetarian'},
                {label: 'In Regime', value: 'In Regime'},
                {label: 'Exercise', value: 'Exercise'},
                {label: 'Overweight', value: 'Overweight'},
                {label: 'Other', value: 'Other'},
            ],
            allergiesOptions: [
                {label: 'Food', value: 'Food'},
                {label: 'Medication', value: 'Medication'},
                {label: 'Animal', value: 'Animal'},
                {label: 'Environmental', value: 'Environmental'},
                {label: 'Other', value: 'Other'},
            ],
            riskFactorsOptions: [
                {label: 'Occupation', value: 'Occupation'},
                {label: 'Living Place', value: 'Living Place'},
                {label: 'Others', value: 'Others'},
            ],
            allergies: [],
            infectedDiseases: [],
            surgicalHistory: [],
            medications: [],
            habits: [],
            riskFactors: [],
            chronicDiseases: '',
            geneticDiseases: '',
		};
	},
    mounted() {
        this.allergies = this.patient.custom_allergies_table
        this.infectedDiseases = this.patient.custom_infected_diseases
        this.surgicalHistory = this.patient.custom_surgical_history_table.map(sur => {
            sur.dayDate = dayjs(sur.date)
            return sur
        })
        this.medications = this.patient.custom_medications.map(med => {
            med.dayDate = dayjs(med.from_date)
            return med
        })
        this.habits = this.patient.custom_habits__social
        this.riskFactors = this.patient.custom_risk_factors_table
        this.chronicDiseases = this.patient.custom_chronic_diseases
        this.geneticDiseases = this.patient.custom_genetic_conditions
    },
    watch: {
        patient: {
			handler(newValue) {
				if(newValue){
                    this.allergies = this.patient.custom_allergies_table
                    this.infectedDiseases = this.patient.custom_infected_diseases
                    this.surgicalHistory = this.patient.custom_surgical_history_table.map(sur => {
                        sur.dayDate = dayjs(sur.date)
                        return sur
                    })
                    this.medications = this.patient.custom_medications.map(med => {
                        med.dayDate = dayjs(med.from_date)
                        return med
                    })
                    this.habits = this.patient.custom_habits__social
                    this.riskFactors = this.patient.custom_risk_factors_table
                    this.chronicDiseases = this.patient.custom_chronic_diseases
                    this.geneticDiseases = this.patient.custom_genetic_conditions
                }
			}
		},
    },
	methods: {
        updateIsOpen(value) {
            this.$emit('update:isOpen', value);
        },
        closeDialog() {
            this.updateIsOpen(false);
        },
        onSubmit() {
            const data = {
                patient: this.patient.name,
                allergies: this.allergies,
                infected_diseases: this.infectedDiseases,
                surgical_history: this.surgicalHistory,
                medications: this.medications,
                habits: this.habits,
                risk_factors: this.riskFactors,
                chronic_diseases: this.chronicDiseases,
                genetic_diseases: this.geneticDiseases,
            }
            this.$call('healthcare_doworks.api.methods.save_patient_history', data)
            .then(response => {
                this.$toast.add({
                    severity: 'success',
                    summary: 'Success',
                    detail: 'Patent history changed successfully',
                    life: 3000 // Duration in ms
                });
                this.lodingOverlay = false;
                this.closeDialog()
            }).catch(error => {
                this.$emit('show-alert', error.message, 'error')
            });
        },
	},
};
</script>