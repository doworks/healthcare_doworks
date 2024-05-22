<template>
    <v-dialog v-model="dialogVisible" width="auto" scrollable>
        <v-card rounded="lg">
            <a-form layout="vertical" :model="form" :rules="rules">
                <v-card-title class="d-flex justify-space-between align-center">
                    <div class="text-h5 text-medium-emphasis ps-2">Medication Request</div>
                    <v-btn icon="mdi mdi-close" variant="text" @click="closeDialog"></v-btn>
                </v-card-title>
                <v-divider class="m-0"></v-divider>
                <v-card-text>
                    <v-container>
                        <v-row>
                            <v-col cols="12" md="6">
                                <a-form-item label="Medication" name="medication">
                                    <a-select
                                        v-model:value="form.medication"
                                        :options="$resources.medications"
                                        :fieldNames="{label: 'name', value: 'name'}"
                                    ></a-select>
                                </a-form-item>
                                <a-form-item label="Medication Item" name="medication_item">
                                    <a-select
                                        v-model:value="form.medication_item"
                                        :options="$resources.items"
                                        :fieldNames="{label: 'item_name', value: 'item_name'}"
                                    ></a-select>
                                </a-form-item>
                                <a-form-item label="Order Date" name="form_order_date">
                                    <a-date-picker 
                                        v-model:value="form.form_order_date"
                                        format="DD/MM/YYYY" 
                                        style="z-index: 3000"
                                    />
                                </a-form-item>
                                <a-form-item label="Expected By" name="expected_date">
                                    <a-date-picker 
                                        v-model:value="form.expected_date"
                                        format="DD/MM/YYYY" 
                                        style="z-index: 3000"
                                    />
                                </a-form-item>
                                <a-form-item label="Order Time" name="form_order_time">
                                    <a-time-picker v-model:value="form.form_order_time" use12-hours format="h:mm a" style="z-index: 3000"/>
                                </a-form-item>
                            </v-col>
                        </v-row>
                        <v-divider class="mt-2 mb-8"></v-divider>
                        <h4>Order Specifications</h4>
                        <v-row>
                            <v-col cols="12" md="6">
                                <a-form-item label="Quantity" name="quantity">
                                    <a-input v-model:value="form.quantity"/>
                                </a-form-item>
                                <a-form-item label="Dosage Form" name="dosage_form">
                                    <a-select
                                        v-model:value="form.dosage_form"
                                        :options="$resources.dosageForms"
                                        :fieldNames="{label: 'dosage_form', value: 'dosage_form'}"
                                    ></a-select>
                                </a-form-item>
                                <a-form-item label="Dosage" name="dosage">
                                    <a-select
                                        v-model:value="form.dosage"
                                        :options="$resources.prescriptionDosages"
                                        :fieldNames="{label: 'dosage', value: 'dosage'}"
                                    ></a-select>
                                </a-form-item>
                            </v-col>
                            <v-col cols="12" md="6">
                                <a-form-item label="Order Description">
                                    <a-textarea v-model:value="form.order_description" placeholder="Order Description" :rows="4" />
                                </a-form-item>
                                <a-form-item label="Period" name="period">
                                    <a-select
                                        v-model:value="form.period"
                                        :options="$resources.prescriptionDurations"
                                        :fieldNames="{label: 'name', value: 'name'}"
                                    ></a-select>
                                </a-form-item>
                                <a-form-item label="Occurrence Time" name="occurrence_time">
                                    <a-time-picker v-model:value="form.occurrence_time" use12-hours format="h:mm a" style="z-index: 3000"/>
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
                practitioner: '',
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
                doctype: 'Medication Request',
                medication: '',
                medication_item: '',
                form_order_date: dayjs(),
                expected_date: undefined,
                form_order_time: dayjs(),
                patient: this.appointment.patient,
                practitioner: this.appointment.practitioner,
                quantity: 1,
                dosage_form: '',
                dosage: '',
                order_description: '',
                period: '',
                occurrence_time: '',
            });
        },
        rules() {
            return reactive({
                medication_item: [{ required: true, message: 'Please choose an item!' }],
                patient: [{ required: true, message: 'Please choose a patient!' }],
                practitioner: [{ required: true, message: 'Please choose a practitioner!' }],
                form_order_date: [{ required: true, message: 'Please choose a date!' }],
                form_order_time: [{ required: true, message: 'Please choose a time!' }],
                dosage_form: [{ required: true, message: 'Please choose a dosage form!' }],
                dosage: [{ required: true, message: 'Please choose a dosage!' }],
            });
        },
    },
	data() {
		return {
            lodingOverlay: false,
		};
	},
	methods: {
        updateIsOpen(value) {
            this.$emit('update:isOpen', value);
        },
        closeDialog() {
            this.updateIsOpen(false);
        },
        onSubmit() {
            const { validate } = Form.useForm(this.form, this.rules);
            validate().then(() => {
                this.lodingOverlay = true;
                this.form.order_date = dayjs(this.form.form_order_date).format('YYYY-MM-DD')
                this.form.order_time = dayjs(this.form.form_order_time).format('HH:mm')
                this.$call('healthcare_doworks.api.methods.new_doc', {form: this.form})
                .then(response => {
                    this.lodingOverlay = false;
                    this.closeDialog()
                }).catch(error => {
                    console.error(error);
                    this.lodingOverlay = false;
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