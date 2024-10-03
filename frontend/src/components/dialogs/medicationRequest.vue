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
                                        :options="$resources.medications.data?.options"
                                        :fieldNames="{label: 'name', value: 'name'}"
                                        show-search
                                        :loading="$resources.medications.list.loading"
                                        @search="(value) => {handleSearch(
                                            value, 
                                            $resources.medications, 
                                            {name: ['like', `%${value}%`]}, 
                                            {},
                                        )}"
                                        :filterOption="false"
                                    ></a-select>
                                </a-form-item>
                                <a-form-item label="Medication Item" name="medication_item">
                                    <a-select
                                        v-model:value="form.medication_item"
                                        :options="$resources.items.data?.options"
                                        :fieldNames="{label: 'item_name', value: 'name'}"
                                        show-search
                                        :loading="$resources.items.list.loading"
                                        @search="(value) => {handleSearch(
                                            value, 
                                            $resources.items, 
                                            {item_name: ['like', `%${value}%`]}, 
                                            {},
                                        )}"
                                        :filterOption="false"
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
                                        :options="$resources.dosageForms.data?.options"
                                        :fieldNames="{label: 'dosage_form', value: 'name'}"
                                        show-search
                                        :loading="$resources.dosageForms.list.loading"
                                        @search="(value) => {handleSearch(
                                            value, 
                                            $resources.dosageForms, 
                                            {dosage_form: ['like', `%${value}%`]}, 
                                            {},
                                        )}"
                                        :filterOption="false"
                                    ></a-select>
                                </a-form-item>
                                <a-form-item label="Dosage" name="dosage">
                                    <a-select
                                        v-model:value="form.dosage"
                                        :options="$resources.prescriptionDosages.data?.options"
                                        :fieldNames="{label: 'dosage', value: 'name'}"
                                        show-search
                                        :loading="$resources.prescriptionDosages.list.loading"
                                        @search="(value) => {handleSearch(
                                            value, 
                                            $resources.prescriptionDosages, 
                                            {dosage: ['like', `%${value}%`]}, 
                                            {},
                                        )}"
                                        :filterOption="false"
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
                                        :options="$resources.prescriptionDurations.data?.options"
                                        :fieldNames="{label: 'name', value: 'name'}"
                                        show-search
                                        :loading="$resources.prescriptionDurations.list.loading"
                                        @search="(value) => {handleSearch(
                                            value, 
                                            $resources.prescriptionDurations, 
                                            {name: ['like', `%${value}%`]}, 
                                            {},
                                        )}"
                                        :filterOption="false"
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
            default: {
                patient: '',
                practitioner: '',
            }
        },
	},
    resources: {
        medications() { return { 
			type: 'list', 
			doctype: 'Medication', 
			fields: ['name'], 
			auto: true, 
			orderBy: 'name', 
			pageLength: 10,
            url: 'frappe.desk.reportview.get', 
            transform(data) {
                if(data.values.length == 0)
                    data.options = []
                else
                    data.options = this.transformData(data.keys, data.values);  // Transform the result into objects
                return data
            }
		}},
        items() { return { 
			type: 'list', 
			doctype: 'Item', 
			fields: ['name', 'item_name'], 
			auto: true, 
			orderBy: 'item_name', 
			pageLength: 10,
            url: 'frappe.desk.reportview.get', 
            transform(data) {
                if(data.values.length == 0)
                    data.options = []
                else
                    data.options = this.transformData(data.keys, data.values);  // Transform the result into objects
                return data
            }
		}},
        dosageForms() { return { 
            type: 'list', 
            doctype: 'Dosage Form', 
            fields: ['name', 'dosage_form'], 
            auto: true, 
            orderBy: 'dosage_form', 
            pageLength: 10,
            url: 'frappe.desk.reportview.get', 
            transform(data) {
                if(data.values.length == 0)
                    data.options = []
                else
                    data.options = this.transformData(data.keys, data.values);  // Transform the result into objects
                return data
            }
        }},
        prescriptionDosages() { return { 
            type: 'list', 
            doctype: 'Prescription Dosage', 
            fields: ['name', 'dosage'], 
            auto: true, 
            orderBy: 'dosage', 
            pageLength: 10,
            url: 'frappe.desk.reportview.get', 
            transform(data) {
                if(data.values.length == 0)
                    data.options = []
                else
                    data.options = this.transformData(data.keys, data.values);  // Transform the result into objects
                return data
            }
        }},
        prescriptionDurations() { return { 
            type: 'list', 
            doctype: 'Prescription Duration', 
            fields: ['name'], 
            auto: true, 
            orderBy: 'name', 
            pageLength: 10,
            url: 'frappe.desk.reportview.get', 
            transform(data) {
                if(data.values.length == 0)
                    data.options = []
                else
                    data.options = this.transformData(data.keys, data.values);  // Transform the result into objects
                return data
            }
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
                    this.$toast.add({
                        severity: 'success',
                        summary: 'Success',
                        detail: 'Medication request created successfully',
                        life: 3000 // Duration in ms
                    });
                    this.lodingOverlay = false;
                    this.closeDialog()
                }).catch(error => {
                    this.$emit('show-alert', error.message, 'error')
                });
            })
            .catch(err => {
                console.log('error', err);
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