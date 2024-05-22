<template>
    <v-dialog v-model="dialogVisible" width="auto" scrollable>
        <v-card rounded="lg">
            <a-form layout="vertical" :model="form" :rules="rules">
                <v-card-title class="d-flex justify-space-between align-center">
                    <div class="text-h5 text-medium-emphasis ps-2">New Vital Signs</div>
                    <v-btn icon="mdi mdi-close" variant="text" @click="closeDialog"></v-btn>
                </v-card-title>
                <v-divider class="m-0"></v-divider>
                <v-card-text>
                    <v-container>
                        <h3 class="mb-4">Vital Signs</h3>
                        <v-row>
                            <v-col cols="12" md="6">
                                <a-form-item 
                                label="Body Temperature" 
                                name="temperature" 
                                extra="Presence of a fever (temp > 38.5 °C/101.3 °F or sustained temp > 38 °C/100.4 °F)"
                                >
                                    <a-input v-model:value="form.temperature"/>
                                </a-form-item>
                                <a-form-item 
                                label="Heart Rate / Pulse" 
                                name="pulse" 
                                extra="Adults' pulse rate is anywhere between 50 and 80 beats per minute."
                                >
                                    <a-input v-model:value="form.pulse"/>
                                </a-form-item>
                                <a-form-item 
                                label="Respiratory rate" 
                                name="respiratory_rate" 
                                extra="Normal reference range for an adult is 16-20 breaths/minute (RCP 2012)"
                                >
                                    <a-input v-model:value="form.respiratory_rate"/>
                                </a-form-item>
                                <a-form-item label="Tongue" name="tongue">
                                    <a-select
                                        v-model:value="form.tongue"
                                        :options="tongueOptions"
                                    ></a-select>
                                </a-form-item>
                                <a-form-item label="Abdomen" name="abdomen">
                                    <a-select
                                        v-model:value="form.abdomen"
                                        :options="abdomenOptions"
                                    ></a-select>
                                </a-form-item>
                            </v-col>
                            <v-col cols="12" md="6">
                                <a-form-item label="Reflexes" name="reflexes">
                                    <a-select
                                        v-model:value="form.reflexes"
                                        :options="reflexesOptions"
                                    ></a-select>
                                </a-form-item>
                                <a-form-item label="Blood Pressure (systolic)" name="bp_systolic" >
                                    <a-input v-model:value="form.bp_systolic" @change="setBloodPressure"/>
                                </a-form-item>
                                <a-form-item label="Blood Pressure (diastolic)" name="bp_diastolic" >
                                    <a-input v-model:value="form.bp_diastolic" @change="setBloodPressure"/>
                                </a-form-item>
                                <a-form-item 
                                label="Blood Pressure" 
                                name="bp" 
                                :extra="bpExtra"
                                v-if="form.bp_diastolic && form.bp_systolic"
                                >
                                    <a-input v-model:value="form.bp" disabled/>
                                </a-form-item>
                                <a-form-item label="Notes" name="vital_signs_note">
                                    <a-textarea v-model:value="form.vital_signs_note" :rows="4" />
                                </a-form-item>
                            </v-col>
                        </v-row>
                        <v-divider class="mt-2 mb-8"></v-divider>
                        <h3 class="mb-4">Nutrition Values</h3>
                        <v-row>
                            <v-col cols="12" md="6">
                                <a-form-item label="Height (In Meter)" name="height">
                                    <a-input v-model:value="form.height" @change="setBMI"/>
                                </a-form-item>
                                <a-form-item label="Weight (In Kilogram)" name="weight">
                                    <a-input v-model:value="form.weight" @change="setBMI"/>
                                </a-form-item>
                                <a-form-item label="BMI" name="bmi">
                                    <a-input v-model:value="form.bmi" disabled/>
                                </a-form-item>
                            </v-col>
                            <v-col cols="12" md="6">
                                <a-form-item label="Notes" name="nutrition_note">
                                    <a-textarea v-model:value="form.nutrition_note" :rows="4" />
                                </a-form-item>
                            </v-col>
                        </v-row>
                    </v-container>
                </v-card-text>
                
                <v-divider class="mt-2"></v-divider>
                
                <v-card-actions class="my-2 d-flex justify-end">
                <v-btn
                class="text-none"
                text="Cancel"
                @click="closeDialog"
                ></v-btn>
                <v-btn
                class="text-none"
                color="blue"
                
                text="submit"
                variant="tonal"
                @click="onSubmit()"
                type="submit"
                ></v-btn>
                </v-card-actions>
            </a-form>
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
import { Form } from 'ant-design-vue';
import { reactive } from 'vue';

import { VBtn } from 'vuetify/components/VBtn'
import { VDialog } from 'vuetify/components/VDialog';
import { VCard, VCardTitle, VCardText, VCardActions } from 'vuetify/components/VCard';
import { VContainer, VCol, VRow } from 'vuetify/components/VGrid';
import { VDivider } from 'vuetify/components/VDivider';
import { VInfiniteScroll } from 'vuetify/components/VInfiniteScroll';
import { VItemGroup, VItem } from 'vuetify/components/VItemGroup';
import { VOverlay } from 'vuetify/components/VOverlay';
import { VProgressCircular } from 'vuetify/components/VProgressCircular';

export default {
	inject: ['$call'],
	components: {
		VBtn, VDialog, VCard, VCardTitle, VCardText, VCardActions, VDivider, VContainer, VCol, VRow, 
        VInfiniteScroll, VItemGroup, VItem, VOverlay, VProgressCircular, 
	},
	props: {
		isOpen: {
            type: Boolean,
            required: true,
            default: false,
        },
        appointment: {
            defalut: {
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
        form() {
            return reactive({
                doctype: 'Vital Signs',
                patient: this.appointment.patient,
                appointment: this.appointment.name,
                signs_date: dayjs(),
                signs_time: dayjs(),
                temperature: '',
                pulse: '',
                respiratory_rate: '',
                tongue: '',
                abdomen: '',
                reflexes: '',
                bp_systolic: '',
                bp_diastolic: '',
                bp: '',
                vital_signs_note: '',
                height: '',
                weight: '',
                bmi: 0,
                nutrition_note: '',
            });
        },
        rules() {
            return reactive({
                patient: [{ required: true, message: 'Please choose a patient!' }],
                signs_date: [{ required: true, message: 'Please choose a date!' }],
                signs_time: [{ required: true, message: 'Please choose a time!' }],
            });
        },
    },
	data() {
		return {
            lodingOverlay: false,
            bpExtra: 'Normal resting blood pressure in an adult is approximately 120 mmHg systolic, and 80 mmHg diastolic, abbreviated "120/80 mmHg"',
            tongueOptions: [
                {label: '', value: ''},
                {label: 'Coated', value: 'Coated'},
                {label: 'Very Coated', value: 'Very Coated'},
                {label: 'Normal', value: 'Normal'},
                {label: 'Furry', value: 'Furry'},
                {label: 'Cuts', value: 'Cuts'},
            ],
            abdomenOptions: [
                {label: '', value: ''},
                {label: 'Normal', value: 'Normal'},
                {label: 'Bloated', value: 'Bloated'},
                {label: 'Full', value: 'Full'},
                {label: 'Fluid', value: 'Fluid'},
                {label: 'Constipated', value: 'Constipated'},
            ],
            reflexesOptions: [
                {label: '', value: ''},
                {label: 'Normal', value: 'Normal'},
                {label: 'Hyper', value: 'Hyper'},
                {label: 'Very Hyper', value: 'Very Hyper'},
                {label: 'One Sided', value: 'One Sided'},
            ],
		};
	},
	methods: {
        updateIsOpen(value) {
            this.$emit('update:isOpen', value);
        },
        closeDialog() {
            this.updateIsOpen(false);
        },
        setBloodPressure() {
            if(this.form.bp_diastolic && this.form.bp_systolic)
                this.form.bp = `${this.form.bp_systolic}/${this.form.bp_diastolic} mmHg`
            else
                this.form.bp = ''
        },
        setBMI() {
            // bmi = weight (in Kg) / height * height (in Meter)
            if(this.form.height && this.form.weight){
                let bmi = (this.form.weight / (this.form.height * this.form.height)).toFixed(2);
                let bmi_note = null;
    
                if (bmi<18.5) {
                    bmi_note = 'Underweight';
                } else if (bmi>=18.5 && bmi<25) {
                    bmi_note = 'Normal';
                } else if (bmi>=25 && bmi<30) {
                    bmi_note = 'Overweight';
                } else if (bmi>=30) {
                    bmi_note = 'Obese';
                }
                    this.form.bmi = bmi
                    this.form.nutrition_note = bmi_note
            }
            else{
                this.form.bmi = 0
                this.form.nutrition_note = ''
            }
        },
        onSubmit() {
            const { validate } = Form.useForm(this.form, this.rules);
            validate().then(() => {
                this.lodingOverlay = true;
                let formClone = {...this.form}
                formClone.signs_date = dayjs(this.form.signs_date).format('YYYY-MM-DD')
                formClone.signs_time = dayjs(this.form.signs_time).format('HH:mm')
                this.$call('healthcare_doworks.api.methods.new_doc', {form: formClone, submit: true})
                .then(response => {
                    this.lodingOverlay = false;
                    this.closeDialog()
                }).catch(error => {
                    console.error(error);
                    let message = error.message.split('\n');
                    message = message.find(line => line.includes('frappe.exceptions'));
                    if(message){
                        const firstSpaceIndex = message.indexOf(' ');
                        this.showAlert(message.substring(firstSpaceIndex + 1) , 10000)
                    }
                });
            })
            .catch(err => {
                console.log('error', err);
            });
        }
	},
};
</script>