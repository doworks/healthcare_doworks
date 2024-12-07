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
            <div v-if="appointmentForm.patient" class="flex mb-4">
              <v-btn 
              class="text-none" 
              color="blue" 
              variant="tonal" 
              size="small" 
              @click="() => {$emit('open-procedure-plan', appointmentForm.patient)}"
              >
                New Procedure Plan
              </v-btn>
              <v-btn 
              class="text-none ml-4 animate-bounce" 
              color="green" 
              variant="tonal" 
              size="small" 
              v-if="procedurePlans?.length > 0"
              >
                Available Procedure Plans
              </v-btn>
            </div>
            <h3>Patient Details</h3>
            <v-row>
              <v-col cols="12" md="6">
                <a-form-item label="Patient" name="patient">
                  <a-input-group class="w-full max-w-full" style="display: flex" compact>
                    <a-select
                    style="width: 100%; max-width: calc(100% - 45.78px)"
                    ref="patientRef"
                    v-model:value="appointmentForm.patient_name"
                    :options="$resources.patients.data?.options"
                    :fieldNames="{label: 'patient_name', value: 'patient_name'}"
                    @change="(value, option) => {
                      appointmentForm.custom_payment_type = option.custom_default_payment_type
                      
                      appointmentForm.patient = option.name;
                      appointmentForm.patient_sex = option.sex;
                      appointmentForm.patient_mobile = option.mobile
                      appointmentForm.patient_age = calculateAge(option.dob)
                      // getPastAppointments(option.name)

                      $getList({doctype: 'Procedure Plan', filters: {patient: option.name}})
                      .then(response => {
                        if(response)
                          procedurePlans = response || []
                      })
                    }"
                    show-search
                    :loading="$resources.patients.list.loading"
                    @search="(value) => {handleSearch(
                      value, 
                      $resources.patients, 
                      {status: 'Active'}, 
                      {status: 'Active'},
                      [
                        ['patient_name', 'like', `%${value}%`], 
                        ['mobile', 'like', `%${value}%`], 
                        ['custom_cpr', 'like', `%${value}%`], 
                        ['custom_file_number', 'like', `%${value}%`]
                      ]
                    )}"
                    :filterOption="false"
                    :disabled="form.type === 'Reschedule Appointment'"
                    >
                      <template #option="{ patient_name, mobile, custom_cpr, custom_file_number }">
                        <div class="flex flex-col">
                          <span v-if="patient_name" class="ms-2"><strong>Name:</strong> {{ patient_name }}</span>
                          <span v-if="custom_cpr" class="ms-2 text-xs"><strong>CPR:</strong> {{ custom_cpr }}</span>
                          <span v-if="mobile" class="ms-2 text-xs"><strong>Mobile:</strong> {{ mobile }}</span>
                          <span v-if="custom_file_number" class="ms-2 text-xs"><strong>File#:</strong> {{ custom_file_number }}</span>
                        </div>
                      </template>
                    </a-select>
                    <a-button ref="addPatientRef" type="primary" @click="newPatientOpen = true" :disabled="form.type === 'Reschedule Appointment'"><i class="mdi mdi-plus" /></a-button>
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
                  @change="(value) => {
                    appointmentForm.procedure_templates = []
                    appointmentForm.duration = 0
                  }"
                  ></a-select>
                </a-form-item>
                <a-form-item 
                label="Procedure Templates" 
                name="procedure_templates" 
                v-if="appointmentForm.custom_appointment_category == 'Procedure'"
                >
                  <a-select
                  v-model:value="appointmentForm.procedure_templates"
                  mode="multiple"
                  :options="$resources.clinicalProcedureTemplates.data?.options"
                  :fieldNames="{label: 'template', value: 'name'}"
                  show-search
                  :loading="$resources.clinicalProcedureTemplates.list.loading"
                  @search="(value) => {handleSearch(
                    value, 
                    $resources.clinicalProcedureTemplates, 
                    {name: ['like', `%${value}%`]}, 
                    {},
                  )}"
                  @select="(value, option) => {
                    appointmentForm.duration += option.custom_default_duration
                  }"
                  @deselect="(value, option) => {
                    appointmentForm.duration -= option.custom_default_duration
                  }"
                  :filterOption="false"
                  ></a-select>
                </a-form-item>
                <a-form-item label="Booking For" name="appointment_type">
                  <LinkField 
                  :disabled="appointmentForm.type == 'Edit Appointment'"
                  doctype="Appointment Type" 
                  :value="appointmentForm.appointment_type" 
                  @change="(data) => { 
                    appointmentForm.appointment_type = data 
                    appointmentForm.practitioner = '';
                    appointmentForm.practitioner_name = '';
                    appointmentForm.department = '';
                    appointmentForm.service_unit = '';
                    appointmentForm.appointment_time = '';
                    $getValue({doctype: 'Appointment Type', fieldname:['allow_booking_for', 'default_duration'], filters:{name:data}})
                    .then(response => {
                      appointmentForm.appointment_for = response.allow_booking_for;
                      if(appointmentForm.custom_appointment_category != 'Procedure')
                        appointmentForm.duration = response.default_duration;
                    })
                  }"
                  />
                </a-form-item>
                <!-- <a-form-item label="Appointment For" v-if="appointmentForm.appointment_type">
                  <a-input v-model:value="appointmentForm.appointment_for" disabled/>
                </a-form-item> -->
                
                <a-form-item v-if="appointmentForm.appointment_type" label="Appointment Duration">
                  <a-input-number 
                  class="w-full"
                  :controls="false" 
                  :min="0" 
                  :step="1" 
                  :parser="value => value.replace(/\.\d*/g, '')" 
                  v-model:value="appointmentForm.duration" 
                  />
                </a-form-item>
                <a-form-item label="Notes">
                  <a-textarea v-model:value="appointmentForm.notes" placeholder="Notes" :rows="4" />
                </a-form-item>
                <a-checkbox v-model:checked="appointmentForm.custom_confirmed">confirmed?</a-checkbox>
              </v-col>
              <v-col cols="12" md="6">
                <a-form-item label="Branch" name="branch">
                  <LinkField 
                  doctype="Branch" 
                  :value="appointmentForm.custom_branch" 
                  @change="(data) => { appointmentForm.custom_branch = data }"
                  />
                </a-form-item>
                <a-form-item label="Practitioner" name="practitioner">
                  <a-select
                  v-model:value="appointmentForm.practitioner_name"
                  :options="$resources.practitioners.data?.options"
                  :fieldNames="{label: 'practitioner_name', value: 'name'}"
                  @change="(value, option) => {
                    appointmentForm.practitioner = option.name
                    $emit('show-slots')
                  }"
                  show-search
                  :loading="$resources.practitioners.list.loading"
                  @search="(value) => {handleSearch(
                    value, 
                    $resources.practitioners, 
                    {status: 'Active', practitioner_name: ['like', `%${value}%`]}, 
                    {status: 'Active'},
                  )}"
                  :filterOption="false"
                  ></a-select>
                </a-form-item>
                <a-form-item label="Department" 
                name="department" 
                v-if="appointmentForm.appointment_for === 'Department'" 
                >
                  <LinkField 
                  doctype="Medical Department" 
                  :value="appointmentForm.department" 
                  @change="(data) => { appointmentForm.department = data }"
                  />
                </a-form-item>
                <a-form-item label="Room" name="service_unit">
                  <LinkField 
                  doctype="Healthcare Service Unit" 
                  :filters="{allow_appointments: 1}"
                  query="healthcare.controllers.queries.get_healthcare_service_units"
                  :value="appointmentForm.service_unit" 
                  @change="(data) => { appointmentForm.service_unit = data }"
                  />
                </a-form-item>
                <a-form-item 
                label="Appointment Date" 
                name="appointment_date" 
                v-if="!appointmentForm.custom_is_walked_in"
                >
                  <a-date-picker 
                  v-model:value="appointmentForm.appointment_date"
                  :disabled-date="disabledDate"
                  @change="()=>{$emit('show-slots')}" 
                  format="dddd DD MMM YYYY" 
                  style="z-index: 3000; width: 100%"
                  :presets="datePresets"
                  :showToday="false"
                  :disabled="appointmentForm.type == 'Edit Appointment'"
                  />
                </a-form-item>
                <a-form-item label="Appointment Time" v-if="appointmentForm.type == 'Edit Appointment'">
                  <a-input v-model:value="appointmentForm.appointment_time" disabled/>
                </a-form-item>
                <a-form-item name="appointment_time" label="Appointment Time" v-if="freeBooking">
                  <a-time-picker v-model:value="appointmentForm.appointment_time" use12-hours format="HH:mm" style="z-index: 3000; width: 100%;"/>
                </a-form-item>
                <a-checkbox 
                class="mb-3 w-full" 
                v-model:checked="appointmentForm.custom_is_walked_in" 
                @change="walkedIn"
                :disabled="appointmentForm.type == 'Edit Appointment'"
                >
                  Walked In?
                </a-checkbox>
                <a-checkbox 
                v-if="appointmentForm.type != 'Edit Appointment'"
                class="mb-3 w-full" 
                v-model:checked="freeBooking" 
                @change="(event) => {
                  appointmentForm.custom_is_walked_in = false
                  if(event.target.checked)
                    timeToDayjs()
                }"
                >
                  Free Booking?
                </a-checkbox>
              </v-col>
            </v-row>
            <v-divider 
            v-if="appointmentForm.type != 'Edit Appointment' && !freeBooking && !appointmentForm.custom_is_walked_in" 
            class="mt-2 mb-8"
            >
            </v-divider>
            <v-row v-if="appointmentForm.type != 'Edit Appointment' && !freeBooking && !appointmentForm.custom_is_walked_in">
              <div 
              class="text-center mb-0" 
              ref="appointmentSlots" 
              v-if="appointmentForm.appointment_date && !appointmentForm.custom_is_walked_in &&
              (
                (appointmentForm.appointment_for === 'Practitioner' && appointmentForm.practitioner) ||
                (appointmentForm.appointment_for === 'Department' && appointmentForm.department) ||
                (appointmentForm.appointment_for === 'Service Unit' && appointmentForm.service_unit)
              )"
              >
                <v-item-group selected-class="bg-blue" mandatory>
                  <div v-for="(slotInfo, index) in slots.slot_details" :key="index">
                    <div class="slot-info">
                      <span v-if="slots.fee_validity && slots.fee_validity != 'Disabled'" style="color:green">Patient has fee validity till <b>{{ getDate(slots.fee_validity.valid_till) }}</b></span>
                      <span v-else-if="slots.fee_validity != 'Disabled'" style="color:red">Patient has no fee validity</span><br/>
                      <span><b>Practitioner Schedule:  </b> {{ slotInfo.slot_name }}
                        <i v-if="slotInfo.tele_conf && !slotInfo.allow_overlap" class="fa fa-video-camera fa-1x" aria-hidden="true"></i>
                      </span><br/>
                      <span><b> Room:  </b> {{slotInfo.service_unit}}</span>
                      <br v-if="slotInfo.service_unit_capacity"/>
                      <span v-if="slotInfo.service_unit_capacity"> <b> Maximum Capacity: </b> {{slotInfo.service_unit_capacity}} </span>
                    </div>
                    <br/>
                    <v-item
                      v-for="(slot, idx) in slotInfo.avail_slot"
                      :key="idx"
                      v-slot="{ isSelected, selectedClass, toggle }"
                    >
                      <v-btn
                      class="text-center text-none"
                      :class="selectedClass"
                      :data-name="slot.from_time"
                      :data-service-unit="slotInfo.service_unit || ''"
                      :data-day-appointment=" slot.maximum_appointments ? 1 : ''"
                      :data-duration="slot.maximum_appointments ? slot.duration : slot.interval"
                      :disabled="slot.disabled"
                      :data-tele-conf="slot.maximum_appointments ? '' : slotInfo.tele_conf || 0"
                      :data-overlap-appointments="slot.maximum_appointments ? '' : slotInfo.service_unit_capacity || 0"
                      style="margin: 0 10px 10px 0; width: auto"
                      rounded="lg"
                      :data-toggle="slot.maximum_appointments ? '' : 'tooltip'"
                      :title="slot.maximum_appointments ? '' : slot.tool_tip || ''"
                      @click="handleSlotClick(toggle, slot.from_time, slotInfo.service_unit)"
                      >
                      <div class="flex flex-col">

                        {{ slot.maximum_appointments ? `${slot.from_time} - ${slot.to_time}` : slot.from_time.substring(0, slot.from_time.length - 3)}}
                        <!-- <v-badge 
                        :color="slot.maximum_appointments || slotInfo.service_unit_capacity ? 'success' : 'red-accent-3'" 
                        :content="slot.count" 
                        
                        >
                        
                        </v-badge> -->
                        <span v-if="slotInfo.allow_overlap == 1" 
                        :class="{
                          'badge w-fit self-center mt-1': true,
                          'bg-success': slot.count > 0,
                          'bg-red-accent-3': slot.count == 0
                        }"
                        >
                          {{slot.count}}
                        </span>
                      </div>
                      </v-btn>
                    </v-item>
                    
                    <br v-if="slotInfo.service_unit_capacity"/>
                    <small v-if="slotInfo.service_unit_capacity">Each slot indicates the capacity currently available for booking</small>
                  </div>
                </v-item-group>
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
          
          text="Save"
          variant="tonal"
          @click="onSubmit()"
          type="submit"
          :disabled="lodingOverlay"
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
    <patientQuickDialog :isOpen="newPatientOpen" @update:isOpen="newPatientOpen = $event" @submitted="patientSubmitted"/>
  </v-dialog>
</template>

<script >
import { ref } from 'vue'
import dayjs from 'dayjs';
import { Form } from 'ant-design-vue';
import { reactive } from 'vue';
import { ListView } from 'frappe-ui'

import { VContainer, VCol, VRow } from 'vuetify/components/VGrid';
import { VDivider } from 'vuetify/components/VDivider';
import { VItemGroup, VItem } from 'vuetify/components/VItemGroup';
import { VMenu } from 'vuetify/components/VMenu'
import { VList, VListItem, VListItemTitle } from 'vuetify/components/VList'
import { VAvatar } from 'vuetify/components/VAvatar';
import { VChip } from 'vuetify/components/VChip';
import { VEmptyState } from 'vuetify/labs/VEmptyState';

export default {
	inject: ['$call', '$getValue', '$getList'],
	components: {ListView, VDivider, VContainer, VCol, VRow, VItemGroup, VItem, VMenu, VList, VListItem, VListItemTitle, VAvatar, VChip, VEmptyState},
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
				appointment_type: '',
				appointment_for: '',
				duration: '',
        custom_confirmed: 0,
				custom_appointment_category: 'First Time',
        procedure_templates: [],
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
    practitioners() { return { 
      type: 'list', 
      doctype: 'Healthcare Practitioner', 
      fields: ['practitioner_name', 'image', 'department', 'name'], 
      filters: {status: 'Active'},
      auto: true, 
      orderBy: 'practitioner_name',
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
    patients() { return { 
      type: 'list', 
      doctype: 'Patient', 
      fields: [
        'sex', 'patient_name', 'name', 'custom_cpr', 'dob', 'mobile', 'email', 'blood_group', 
        'inpatient_record', 'inpatient_status', 'custom_default_payment_type', 'custom_file_number'
      ], 
      filters: {status: 'Active'},
      limit_start: 0,
      pageLength: 10, 
      url: 'frappe.desk.reportview.get', 
      auto: true, 
      transform(data) {
        if(data.values.length == 0)
          data.options = []
        else
          data.options = this.transformData(data.keys, data.values);  // Transform the result into objects
        return data
      }
    }},
    clinicalProcedureTemplates() { return { 
      type: 'list', 
      doctype: 'Clinical Procedure Template', 
      fields: ['name', 'template', 'medical_department', 'custom_default_duration'], 
      auto: true,
      orderBy: 'name',
      pageLength: 30,
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
    appointmentForm() {
      return reactive(this.form);
    },
    rulesRef() {
      return reactive({
        appointment_type: [{ required: true, message: 'Please choose a type!' }],
        patient: [{ required: true, message: 'Please choose a patient!' }],
        practitioner: [{ required: this.appointmentForm.appointment_for === 'Practitioner', message: 'Please choose a practitioner!' }],
        department: [{ required: this.appointmentForm.appointment_for === 'Department', message: 'Please choose a department!' }],
        service_unit: [{ required: this.appointmentForm.appointment_for === 'Service Unit', message: 'Please choose a room!' }],
        appointment_date: [{ required: true, message: 'Please choose a date!' }],
        appointment_time: [{ required: !this.appointmentForm.custom_is_walked_in, message: 'Please choose a time!' }],
        procedure_templates: [{ 
          required: this.appointmentForm.custom_appointment_category == 'Procedure', 
          message: 'Please choose a procedure template!' 
        }],
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
      freeBooking: false,
      searchTimeout: null,
      popoverVisible: false,
      patientSearch: '',
      popoverPatient: '',
      pastAppointments: [],
      procedurePlans: [],
      categoryOptions: [
        {label: 'First Time', value: 'First Time'}, 
        {label: 'Follow-up', value: 'Follow-up'}, 
        {label: 'Procedure', value: 'Procedure'},
      //  {label: 'Session', value: 'Session'},
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
  mounted() {
    this.popoverPatient = ''
    this.pastAppointments = []
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
    getPastAppointments(patient) {
      this.$call('healthcare_doworks.api.methods.get_past_appointments', {patient})
      .then(response => {
        this.popoverPatient = patient
        this.pastAppointments = response.map((d) => {
            d.appointment_date_moment = dayjs(d.appointment_date + ' ' + d.appointment_time).format('D/MM/YYYY');
            d.appointment_time_moment = dayjs(d.appointment_date + ' ' + d.appointment_time).format('h:mm a');
          return d;
        })
        this.popoverVisible = true;
      }).catch(error => {
        this.$emit('show-alert', error.message, 'error')
      });
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
        if(this.freeBooking){
          form.appointment_time = form.appointment_time.format('HH:mm')
        }
        let children = {custom_procedure_templates: form.procedure_templates.filter(value => !value.name).map(value => {
          if(value.template)
            return {template: value.template}
          return {template: value}
        })}
        if(form.type === 'New Appointment'){
          delete form['name'];
          this.$call('healthcare_doworks.api.methods.new_doc', {form, children})
          .then(response => {
            this.$toast.add({
              severity: 'success',
              summary: 'Success',
              detail: 'Appointment booked successfully',
              life: 3000 // Duration in ms
            });
            this.lodingOverlay = false;
            this.closeDialog()
          }).catch(error => {
            this.$emit('show-alert', error.message, 'error')
          });
        }
        else if(form.type === 'Edit Appointment'){
          this.lodingOverlay = true;
          this.$call('healthcare_doworks.api.methods.edit_doc', {form, children})
          .then(response => {
            this.$toast.add({
              severity: 'success',
              summary: 'Success',
              detail: 'Appointment saved',
              life: 3000 // Duration in ms
            });
            this.lodingOverlay = false;
            this.closeDialog()
          }).catch(error => {
            this.$emit('show-alert', error.message, 'error')
          });
        }
        else if(form.type === 'Reschedule Appointment'){
          // children = {custom_procedure_templates: form.procedure_templates.map(value => ({template: value.template}))}
          form.status = 'Rescheduled'
          form.custom_visit_appointment_status = 'Scheduled'
          this.$call('healthcare_doworks.api.methods.edit_doc', {form, children})
          .then(response => {
            this.$toast.add({
              severity: 'success',
              summary: 'Success',
              detail: 'Appointment rescheduled successfully',
              life: 3000 // Duration in ms
            });
            this.lodingOverlay = false;
            this.closeDialog()
          }).catch(error => {
            this.$emit('show-alert', error.message, 'error')
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
    handleMouseEnter() {
      if (this.appointmentForm.patient !== this.popoverPatient) {
        this.getPastAppointments(this.appointmentForm.patient);
      } 
      else if(this.appointmentForm.patient) {
        this.popoverVisible = true; // Show the popover if data is already loaded
      }
    },
    timeToDayjs() {
      console.log(this.appointmentForm.appointment_time)
      if(this.appointmentForm.appointment_time)
        this.appointmentForm.appointment_time = dayjs(this.appointmentForm.appointment_time, "HH:mm:ss");
    },
    handleMouseLeave() {
      this.popoverVisible = false
    },
    setPaymentDetails() {
      this.$call('healthcare.healthcare.utils.get_appointment_billing_item_and_rate', {doc: this.appointmentForm}).then(data => {
        if (data.message) {
          this.appointmentForm.paid_amount = data.message.practitioner_charge
          this.appointmentForm.billing_item = data.message.service_item
        }
      }).catch(error => {
        this.$emit('show-alert', error.message, 'error')
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
      this.freeBooking = false
      this.appointmentForm.appointment_date = dayjs()
    },
    patientFilterOption(input, option) {
      const fieldsToSearch = ['patient_name', 'custom_cpr', 'mobile', 'email']; 

      return fieldsToSearch.some(field =>
        option[field]?.toString().toLowerCase().includes(input.toLowerCase())
      );
    },
    patientSubmitted(doc) {
      this.$call('healthcare_doworks.api.methods.new_doc', {form: doc})
      .then(response => {
        this.$toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'New Patient created',
          life: 3000 // Duration in ms
        });
        this.$resources.patients.reload()
        this.appointmentForm.patient = response.name
        this.appointmentForm.patient_name = response.patient_name
        this.appointmentForm.patient_sex = response.sex;
        this.appointmentForm.patient_mobile = response.mobile
        this.appointmentForm.patient_age = this.calculateAge(response.dob)
        this.newPatientOpen = false
      }).catch(error => {
        this.$emit('show-alert', error.message, 'error')
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
    handleSearch(query, resource, filters, initialFilters, orFilters) {
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