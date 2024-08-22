<template>
  <v-dialog v-model="dialogVisible" width="auto" scrollable>
    <v-card rounded="lg">
      <a-form layout="vertical" :model="appointmentForm" :rules="rulesRef">
        <v-card-title class="d-flex justify-space-between align-center">
          <div class="text-h5 text-medium-emphasis ps-2">{{ appointmentForm.type }}</div>
          <v-btn icon="mdi mdi-close" variant="text" @click="closeDialog"></v-btn>
        </v-card-title>
        <v-divider class="m-0"></v-divider>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12" md="6">
                <a-form-item label="Appointment Category">
                  <a-select
                    v-model:value="appointmentForm.custom_appointment_category"
                    :options="categoryOptions"
                  ></a-select>
                </a-form-item>
                <a-form-item label="Appointment Type" name="appointment_type">
                  <a-select
                    v-model:value="appointmentForm.appointment_type"
                    :options="$myresources.appointmentTypes"
                    @change="(value, option) => {
                      appointmentForm.appointment_for = option.allow_booking_for;
                      appointmentForm.duration = option.default_duration;
                      appointmentForm.practitioner = '';
                      appointmentForm.practitioner_name = '';
                      appointmentForm.department = '';
                      appointmentForm.service_unit = '';
                      appointmentForm.appointment_time = '';
                    }"
                    :fieldNames="{label: 'appointment_type', value: 'appointment_type'}"
                  ></a-select>
                </a-form-item>
                <a-form-item label="Appointment For" v-if="appointmentForm.appointment_type">
                  <a-input v-model:value="appointmentForm.appointment_for" disabled/>
                </a-form-item>
                
                <a-form-item v-if="appointmentForm.appointment_type" label="Appointment Duration">
                  <a-input disabled v-model:value="appointmentForm.duration" />
                </a-form-item>
              </v-col>
              <v-col cols="12" md="6">
                <a-form-item label="Practitioner" 
                name="practitioner" 
                v-if="appointmentForm.appointment_for === 'Practitioner'" 
                @change="setPaymentDetails()"
                >
                  <a-select
                    v-model:value="appointmentForm.practitioner_name"
                    :options="$myresources.practitioners"
                    :fieldNames="{label: 'practitioner_name', value: 'practitioner_name'}"
                    show-search
                    @change="(value, option) => {
                      appointmentForm.practitioner = option.name
                      $emit('show-slots')
                    }"
                  ></a-select>
                </a-form-item>
                <a-form-item label="Department" 
                name="department" 
                v-if="appointmentForm.appointment_for === 'Department'" 
                @change="setPaymentDetails()"
                >
                  <a-select
                    v-model:value="appointmentForm.department"
                    :options="$myresources.departments"
                    :fieldNames="{label: 'department', value: 'department'}"
                    show-search
                  ></a-select>
                </a-form-item>
                <a-form-item label="Service Unit" 
                name="service_unit" 
                v-if="appointmentForm.appointment_for === 'Service Unit'" 
                @change="setPaymentDetails()"
                >
                  <a-select
                    v-model:value="appointmentForm.service_unit"
                    :options="$myresources.serviceUnits"
                    :fieldNames="{label: 'name', value: 'name'}"
                    show-search
                  ></a-select>
                </a-form-item>
                <a-form-item label="Appointment Date" name="appointment_date">
                  <a-date-picker 
                    v-model:value="appointmentForm.appointment_date"
                    :disabled-date="disabledDate"
                    @change="()=>{$emit('show-slots')}" 
                    format="dddd DD MMM YYYY" 
                    style="z-index: 3000"
                  />
                </a-form-item>
                <a-form-item label="Notes">
                  <a-textarea v-model:value="appointmentForm.notes" placeholder="Notes" :rows="4" />
                </a-form-item>
              </v-col>
            </v-row>
            <v-divider class="mt-2 mb-8"></v-divider>
            <h3>Patient Details</h3>
            <v-row>
              <v-col cols="12" md="6">
                <a-form-item label="Patient" name="patient">
                  <a-select
                  v-model:value="appointmentForm.patient_name"
                  :options="$myresources.patients"
                  :fieldNames="{label: 'patient_name', value: 'patient_name'}"
                  @change="(value, option) => {
                    appointmentForm.patient = option.name;
                    appointmentForm.patient_sex = option.sex;
                    appointmentForm.patient_mobile = option.mobile
                    appointmentForm.patient_age = calculateAge(option.dob)
                  }"
                  show-search
                  ></a-select>
                </a-form-item>
                <a-form-item label="Patient Mobile" v-if="appointmentForm.patient">
                  <a-input v-model:value="appointmentForm.patient_mobile" disabled/>
                </a-form-item>
              </v-col>
              <v-col cols="12" md="6">
                <a-form-item label="Patient Gender" v-if="appointmentForm.patient">
                  <a-input v-model:value="appointmentForm.patient_sex" disabled/>
                </a-form-item>
                <a-form-item label="Patient Age" v-if="appointmentForm.patient">
                  <a-input v-model:value="appointmentForm.patient_age" disabled/>
                </a-form-item>
              </v-col>
            </v-row>
            <v-divider class="mt-2 mb-8"></v-divider>
            <v-row>
              <div 
              class="text-center mb-0" 
              ref="appointmentSlots" 
              v-if="this.appointmentForm.appointment_date && (
                (this.appointmentForm.appointment_for === 'Practitioner' && this.appointmentForm.practitioner) ||
                (this.appointmentForm.appointment_for === 'Department' && this.appointmentForm.department) ||
                (this.appointmentForm.appointment_for === 'Service Unit' && this.appointmentForm.service_unit)
              )"
              >
                <div v-for="(slotInfo, index) in slots.slot_details" :key="index">
                  <div class="slot-info">
                    <span v-if="slots.fee_validity && slots.fee_validity != 'Disabled'" style="color:green">Patient has fee validity till <b>{{ getDate(slots.fee_validity.valid_till) }}</b></span>
                    <span v-else-if="slots.fee_validity != 'Disabled'" style="color:red">Patient has no fee validity</span><br/>
                    <span><b>Practitioner Schedule:  </b> {{ slotInfo.slot_name }}
                      <i v-if="slotInfo.tele_conf && !slotInfo.allow_overlap" class="fa fa-video-camera fa-1x" aria-hidden="true"></i>
                    </span><br/>
                    <span><b> Service Unit:  </b> {{slotInfo.service_unit}}</span>
                    <br v-if="slotInfo.service_unit_capacity"/>
                    <span v-if="slotInfo.service_unit_capacity"> <b> Maximum Capacity: </b> {{slotInfo.service_unit_capacity}} </span>
                  </div>
                  <br/>
                  <v-item-group selected-class="bg-blue" mandatory>
                    <v-item
                      v-for="(slot, idx) in slotInfo.avail_slot"
                      :key="idx"
                      v-slot="{ isSelected, selectedClass, toggle }"
                    >
                      <v-btn
                      class="text-center"
                      :class="selectedClass"
                      :data-name="slot.from_time"
                      :data-service-unit="slotInfo.service_unit || ''"
                      :data-day-appointment=" slot.maximum_appointments ? 1 : ''"
                      :data-duration="slot.maximum_appointments ? slot.duration : slot.interval"
                      :disabled="slot.disabled"
                      :data-tele-conf="slot.maximum_appointments ? '' : slotInfo.tele_conf || 0"
                      :data-overlap-appointments="slot.maximum_appointments ? '' : slotInfo.service_unit_capacity || 0"
                      style="margin: 0 10px 10px 0; width: auto"
                      :data-toggle="slot.maximum_appointments ? '' : 'tooltip'"
                      :title="slot.maximum_appointments ? '' : slot.tool_tip || ''"
                      @click="handleSlotClick(toggle, slot.from_time, slotInfo.service_unit)"
                      >
                        {{ slot.maximum_appointments ? `${slot.from_time} - ${slot.to_time}` : slot.from_time.substring(0, slot.from_time.length - 3)}}
                        &nbsp
                        <span v-if="slot.maximum_appointments || slotInfo.service_unit_capacity" :class="`badge ${slot.count_class}`">
                          {{slot.count}}
                        </span>
                      </v-btn>
                    </v-item>
                  </v-item-group>
                  
                  <br v-if="slotInfo.service_unit_capacity"/>
                  <small v-if="slotInfo.service_unit_capacity">Each slot indicates the capacity currently available for booking</small>
                </div>
              </div>
              <div v-else>
                <b>Appointment date</b> and <b>Healthcare Practitioner</b> are Mandatory
              </div>
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
  </v-dialog>
</template>

<script >
import dayjs from 'dayjs';
import { Form } from 'ant-design-vue';
import { reactive } from 'vue';

import { VContainer, VCol, VRow } from 'vuetify/components/VGrid';
import { VDivider } from 'vuetify/components/VDivider';
import { VItemGroup, VItem } from 'vuetify/components/VItemGroup';

export default {
	inject: ['$call'],
	components: {
		VDivider, VContainer, VCol, VRow, VItemGroup, VItem,
	},
	props: {
		isOpen: {
      type: Boolean,
      required: true,
      default: false,
    },
    form: {
      default: {
        doctype: 'Patient Appointment',
				name: 'new-patient-appointment',
				appointment_type: 'Practitioner',
				appointment_for: 'Practitioner',
				duration: '',
				custom_appointment_category: 'First Time',
        custom_payment_type: '',
				practitioner: '',
        practitioner_name: '',
				department: '',
				service_unit: '',
				patient: '',
				patient_name: '',
				patient_sex: '',
        notes: '',
        status: 'Scheduled',
				appointment_date: undefined,
				appointment_time: undefined,
      }
    },
    slots: {
      default: {}
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
    appointmentForm() {
      return reactive(this.form);
    },
    rulesRef() {
      return reactive({
        appointment_type: [{ required: true, message: 'Please choose a type!' }],
        patient: [{ required: true, message: 'Please choose a patient!' }],
        practitioner: [{ required: this.appointmentForm.appointment_for === 'Practitioner', message: 'Please choose a practitioner!' }],
        department: [{ required: this.appointmentForm.appointment_for === 'Department', message: 'Please choose a department!' }],
        service_unit: [{ required: this.appointmentForm.appointment_for === 'Service Unit', message: 'Please choose a service unit!' }],
        appointment_date: [{ required: true, message: 'Please choose a date!' }],
      });
    },
  },
  watch: {
    slots(newVal) {
      if (newVal) {
        this.$nextTick(() => {
          this.scrollToTimeSlots();
        });
      }
    },
  },
	data() {
		return {
      lodingOverlay: false,
      categoryOptions: [
        {label: 'First Time', value: 'First Time'}, 
        {label: 'Follow-up', value: 'Follow-up'}, 
        {label: 'Procedure', value: 'Procedure'},
        {label: 'Session', value: 'Session'},
      ]
		};
	},
	methods: {
    updateIsOpen(value) {
      this.$emit('update:isOpen', value);
    },
    closeDialog() {
      this.updateIsOpen(false);
    },
    getDate(date) {
      return dayjs(date).format('DD-MM-YYYY')
    },
    scrollToTimeSlots() {
      const element = this.$refs.appointmentSlots;
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    },
    onSubmit() {
      const { validate } = Form.useForm(this.appointmentForm, this.rulesRef);
      validate().then(() => {
        this.lodingOverlay = true;
        let form = {...this.appointmentForm}
        form.appointment_date = dayjs(form.appointment_date).format('YYYY-MM-DD')
        if(form.type === 'New Appointment'){
          delete form['name'];
          this.$call('healthcare_doworks.api.methods.new_doc', {form})
          .then(response => {
            this.lodingOverlay = false;
            this.closeDialog()
          }).catch(error => {
            console.error(error);
            let message = error.message.split('\n');
            message = message.find(line => line.includes('frappe.exceptions'));
            if(message){
              const firstSpaceIndex = message.indexOf(' ');
              this.$emit('show-alert', message.substring(firstSpaceIndex + 1, 10000))
            }
          });
        }
        if(form.type === 'Reschedule Appointment'){
          this.$call('healthcare_doworks.api.methods.reschedule_appointment', {form})
          .then(response => {
            this.lodingOverlay = false;
            this.closeDialog()
          }).catch(error => {
            console.error(error);
            let message = error.message.split('\n');
            message = message.find(line => line.includes('frappe.exceptions'));
            if(message){
              const firstSpaceIndex = message.indexOf(' ');
              this.$emit('show-alert', message.substring(firstSpaceIndex + 1, 10000))
            }
          });
        }
      })
      .catch(err => {
        console.log('error', err);
      });
    },
    handleSlotClick(toggle, time, service_unit){
      this.appointmentForm.appointment_time = time;
      this.appointmentForm.service_unit = service_unit;
      toggle();
    },
    setPaymentDetails() {
      console.log('hello')
      this.$call('healthcare.healthcare.utils.get_appointment_billing_item_and_rate', {doc: this.appointmentForm}).then(data => {
        console.log(data)
        if (data.message) {
          this.appointmentForm.paid_amount = data.message.practitioner_charge
          this.appointmentForm.billing_item = data.message.service_item
        }
      }).catch(error => {
        console.error(error);
        let message = error.message.split('\n');
        message = message.find(line => line.includes('frappe.exceptions'));
        if(message){
          const firstSpaceIndex = message.indexOf(' ');
          this.$emit('show-alert', message.substring(firstSpaceIndex + 1, 10000))
        }
      });
    },
    calculateAge(dob) {
      if(dob){
        const today = dayjs();
        const birthDate = dayjs(dob)
        const years = today.diff(birthDate, 'year');
        const months = today.diff(birthDate.add(years, 'year'), 'month');
        const days = today.diff(birthDate.add(years, 'year').add(months, 'month'), 'day');
        return `${years} Year(s) ${months} Month(s) ${days} Day(s)`;
      }
      return ''
    },
    disabledDate(current) {
      // Can not select days before today and today
      return current && current < dayjs().endOf('day').subtract(1, 'day');
    },
	},
};
</script>