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
            <h3>Patient Details</h3>
            <v-row>
              <v-col cols="12" md="6">
                <a-form-item label="Patient" name="patient">
                  <a-input-group class="w-full" style="display: flex" compact>
                    <a-select
                    show-search
                    class="w-full"
                    v-model:value="appointmentForm.patient_name"
                    :options="$resources.patients.data"
                    :fieldNames="{label: 'patient_name', value: 'name'}"
                    :filterOption="patientFilterOption"
                    @change="(value, option) => {
                      appointmentForm.patient = option.name;
                      appointmentForm.patient_sex = option.sex;
                      appointmentForm.patient_mobile = option.mobile
                      appointmentForm.patient_age = calculateAge(option.dob)
                    }"
                    >
                      <template #option="{ patient_name, mobile, custom_cpr }">
                        <div class="flex flex-col">
                          <span v-if="patient_name" class="ms-2"><strong>Name:</strong> {{ patient_name }}</span>
                          <span v-if="custom_cpr" class="ms-2 text-xs"><strong>CPR:</strong> {{ custom_cpr }}</span>
                          <span v-if="mobile" class="ms-2 text-xs"><strong>Mobile:</strong> {{ mobile }}</span>
                        </div>
                      </template>
                    </a-select>
                    <a-button type="primary" @click="newPatientOpen = true"><i class="mdi mdi-plus" /></a-button>
                  </a-input-group>
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
                  :options="$resources.appointmentTypes.data"
                  @change="(value, option) => {
                    console.log($resources.patients)
                    appointmentForm.appointment_for = option.allow_booking_for;
                    appointmentForm.duration = option.default_duration;
                    appointmentForm.practitioner = '';
                    appointmentForm.practitioner_name = '';
                    appointmentForm.department = '';
                    appointmentForm.service_unit = '';
                    appointmentForm.appointment_time = '';
                  }"
                  :fieldNames="{label: 'appointment_type', value: 'name'}"
                  ></a-select>
                </a-form-item>
                <a-form-item label="Appointment For" v-if="appointmentForm.appointment_type">
                  <a-input v-model:value="appointmentForm.appointment_for" disabled/>
                </a-form-item>
                
                <a-form-item v-if="appointmentForm.appointment_type" label="Appointment Duration">
                  <a-input v-model:value="appointmentForm.duration" />
                </a-form-item>
              </v-col>
              <v-col cols="12" md="6">
                <a-form-item label="Branch" name="branch">
                  <a-select
                  v-model:value="appointmentForm.custom_branch"
                  :options="$resources.branches.data"
                  :fieldNames="{label: 'name', value: 'name'}"
                  show-search
                  ></a-select>
                </a-form-item>
                <a-form-item label="Practitioner" 
                name="practitioner" 
                v-if="appointmentForm.appointment_for === 'Practitioner'" 
                @change="setPaymentDetails()"
                >
                  <a-select
                  v-model:value="appointmentForm.practitioner_name"
                  :options="$resources.practitioners.data"
                  :fieldNames="{label: 'practitioner_name', value: 'name'}"
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
                  :options="$resources.departmentsdata"
                  :fieldNames="{label: 'department', value: 'name'}"
                  show-search
                  ></a-select>
                </a-form-item>
                <a-form-item label="Service Unit" 
                name="service_unit" 
                v-if="appointmentForm.appointment_for === 'Service Unit' || appointmentForm.custom_is_walked_in" 
                @change="setPaymentDetails()"
                >
                  <a-select
                  v-model:value="appointmentForm.service_unit"
                  :options="$resources.serviceUnits.data"
                  :fieldNames="{label: 'name', value: 'name'}"
                  show-search
                  ></a-select>
                </a-form-item>
                <a-form-item label="Appointment Date" name="appointment_date" v-if="!appointmentForm.custom_is_walked_in">
                  <a-date-picker 
                  v-model:value="appointmentForm.appointment_date"
                  :disabled-date="disabledDate"
                  @change="()=>{$emit('show-slots')}" 
                  format="dddd DD MMM YYYY" 
                  style="z-index: 3000; width: 100%"
                  :presets="datePresets"
                  :showToday="false"
                  />
                </a-form-item>
                <a-checkbox class="mb-3" v-model:checked="appointmentForm.custom_is_walked_in" @change="walkedIn">Walked In?</a-checkbox>
                <a-form-item label="Notes">
                  <a-textarea v-model:value="appointmentForm.notes" placeholder="Notes" :rows="4" />
                </a-form-item>
              </v-col>
            </v-row>
            <v-divider v-if="!appointmentForm.custom_is_walked_in" class="mt-2 mb-8"></v-divider>
            <v-row>
              <div 
              class="text-center mb-0" 
              ref="appointmentSlots" 
              v-if="appointmentForm.appointment_date && !appointmentForm.custom_is_walked_in && (
                (appointmentForm.appointment_for === 'Practitioner' && appointmentForm.practitioner) ||
                (appointmentForm.appointment_for === 'Department' && appointmentForm.department) ||
                (appointmentForm.appointment_for === 'Service Unit' && appointmentForm.service_unit)
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
              <div v-else-if="!appointmentForm.custom_is_walked_in">
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
    <patientQuick :isOpen="newPatientOpen" @update:isOpen="newPatientOpen = $event" @submitted="patientSubmitted"/>
  </v-dialog>
</template>

<script >
import { ref } from 'vue'
import dayjs from 'dayjs';
import { Form } from 'ant-design-vue';
import { reactive } from 'vue';

import { VContainer, VCol, VRow } from 'vuetify/components/VGrid';
import { VDivider } from 'vuetify/components/VDivider';
import { VItemGroup, VItem } from 'vuetify/components/VItemGroup';

export default {
	inject: ['$call'],
	components: {VDivider, VContainer, VCol, VRow, VItemGroup, VItem},
	props: {
		isOpen: {
      type: Boolean,
      required: true,
      default: false,
    },
    form: {
      default: {
        doctype: 'Patient Appointment',
				name: '',
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
        custom_is_walked_in: false,
				appointment_date: undefined,
				appointment_time: undefined,
      }
    },
    slots: {
      default: {}
    },
	},
  resources: {
    departments() { return { 
      type: 'list', 
      doctype: 'Medical Department', 
      fields: ['name', 'department'], 
      auto: true, 
      orderBy: 'department', 
      pageLength: null,
      cache: 'departments'
    }},
    branches() { return { 
      type: 'list', 
      doctype: 'Branch', 
      fields: ['name'], 
      auto: true, 
      orderBy: 'name', 
      pageLength: null,
      cache: 'branches'
    }},
    appointmentTypes() { return { 
      type: 'list', 
      doctype: 'Appointment Type', 
      fields: ['name', 'appointment_type', 'allow_booking_for', 'default_duration'], 
      auto: true, 
      orderBy: 'appointment_type',
      pageLength: null,
      cache: 'appointmentTypes'
    }},
    practitioners() { return { 
      type: 'list', 
      doctype: 'Healthcare Practitioner', 
      fields: ['practitioner_name', 'image', 'department', 'name'], 
      filter: {status: 'Active'},
      auto: true, 
      orderBy: 'practitioner_name',
      pageLength: null,
      cache: 'practitioners'
    }},
    serviceUnits() { return { 
      type: 'list', 
      doctype: 'Healthcare Service Unit', 
      fields:['name'], 
      filters:{'allow_appointments': 1}, 
      auto: true, 
      orderBy: 'name',
      pageLength: null,
      cache: 'serviceUnits'
    }},
    patients() { return { 
      type: 'list', 
      doctype: 'Patient', 
      fields: ['sex', 'patient_name', 'name', 'custom_cpr', 'dob', 'mobile', 'email', 'blood_group', 'inpatient_record', 'inpatient_status'], 
      auto: true, 
      orderBy: 'patient_name',
      pageLength: null,
      cache: 'patients'
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
    appointmentForm() {
      return reactive(this.form);
    },
    rulesRef() {
      return reactive({
        appointment_type: [{ required: true, message: 'Please choose a type!' }],
        patient: [{ required: true, message: 'Please choose a patient!' }],
        practitioner: [{ required: this.appointmentForm.appointment_for === 'Practitioner', message: 'Please choose a practitioner!' }],
        department: [{ required: this.appointmentForm.appointment_for === 'Department', message: 'Please choose a department!' }],
        service_unit: [{ 
          required: this.appointmentForm.appointment_for === 'Service Unit' || this.appointmentForm.custom_is_walked_in, 
          message: 'Please choose a service unit!' 
        }],
        appointment_date: [{ required: true, message: 'Please choose a date!' }],
        appointment_time: [{ required: !this.appointmentForm.custom_is_walked_in, message: 'Please choose a time!' }],
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
      newPatientOpen: false,
      categoryOptions: [
        {label: 'First Time', value: 'First Time'}, 
        {label: 'Follow-up', value: 'Follow-up'}, 
        {label: 'Procedure', value: 'Procedure'},
        {label: 'Session', value: 'Session'},
      ],
      datePresets: ref([
        { label: 'Today', value: dayjs() },
        { label: 'Tommorow', value: dayjs().add(+1, 'd') },
        { label: 'Next Week', value: dayjs().add(+7, 'd') },
        { label: 'Next Month', value: dayjs().add(+1, 'month') },
        { label: 'After 3 Months', value: dayjs().add(+3, 'month') },
        { label: 'After 6 Months', value: dayjs().add(+6, 'month') },
      ]),
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
        if(form.custom_is_walked_in){
          form.appointment_time = dayjs().format('HH:mm')
          form.status = 'Walked In'
        }
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
      this.$call('healthcare.healthcare.utils.get_appointment_billing_item_and_rate', {doc: this.appointmentForm}).then(data => {
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
    walkedIn() {
      this.appointmentForm.appointment_date = dayjs()
    },
    patientFilterOption(input, option) {
      const fieldsToSearch = ['patient_name', 'custom_cpr', 'mobile', 'email']; 

      return fieldsToSearch.some(field =>
        option[field]?.toString().toLowerCase().includes(input.toLowerCase())
      );
    },
    patientSubmitted(doc) {
      this.$resources.patients.insert.submit(doc)
      this.newPatientOpen = false
    },
	},
};
</script>