<template>
  <v-dialog v-model="dialogVisible" width="auto" scrollable>
    <OverlayPanel ref="popover" :dismissable="false" :baseZIndex="2000">
      <v-card min-width="300" >
        <ListView
        class="max-h-[250px]"
        :columns="[
          {label: 'Practitioner', key: 'practitioner_name'},
          {label: 'Date', key: 'appointment_date'},
          {label: 'Time', key: 'appointment_time'},
          {label: 'Visit Status', key: 'custom_visit_status'},
          {label: 'Category', key: 'custom_appointment_category'},
          {label: 'Procedures', key: 'procedure_templates', getLabel: ({ row }) => row.procedure_templates.templates},
        ]"
        :rows="pastAppointments"
        :options="{
          selectable: true,
          showTooltip: true,
          resizeColumn: true,
          emptyState: {
            title: 'No appointment',
            description: 'This patient has no past appointments',
          },
        }"
        row-key="name"
        />
      </v-card>
    </OverlayPanel>
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
                  <a-input-group class="w-full max-w-full" style="display: flex" compact>
                    <a-select
                    class="w-full"
                    ref="patientRef"
                    v-model:value="appointmentForm.patient_name"
                    :options="$resources.patients.data?.options"
                    :fieldNames="{label: 'patient_name', value: 'name'}"
                    @change="(value, option) => {
                      appointmentForm.custom_payment_type = option.custom_default_payment_type
                      
                      appointmentForm.patient = option.name;
                      appointmentForm.patient_sex = option.sex;
                      appointmentForm.patient_mobile = option.mobile
                      appointmentForm.patient_age = calculateAge(option.dob)
                      getPastAppointments(option.name)
                    }"
                    show-search
                    :loading="$resources.patients.list.loading"
                    @search="(value) => {handleSearch(
                      value, 
                      $resources.patients, 
                      {status: 'Active'}, 
                      {status: 'Active'},
                      [['patient_name', 'like', `%${value}%`], ['mobile', 'like', `%${value}%`], ['custom_cpr', 'like', `%${value}%`]]
                    )}"
                    :filterOption="false"
                    @mouseenter="showPopover" 
                    @mouseleave="hidePopover"
                    >
                      <template #option="{ patient_name, mobile, custom_cpr }">
                        <div class="flex flex-col">
                          <span v-if="patient_name" class="ms-2"><strong>Name:</strong> {{ patient_name }}</span>
                          <span v-if="custom_cpr" class="ms-2 text-xs"><strong>CPR:</strong> {{ custom_cpr }}</span>
                          <span v-if="mobile" class="ms-2 text-xs"><strong>Mobile:</strong> {{ mobile }}</span>
                        </div>
                      </template>
                    </a-select>
                    <a-button ref="addPatientRef" type="primary" @click="newPatientOpen = true"><i class="mdi mdi-plus" /></a-button>
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
                  :filterOption="false"
                  :disabled="appointmentForm.type == 'Edit Appointment'"
                  ></a-select>
                </a-form-item>
                <a-form-item label="Appointment Type" name="appointment_type">
                  <a-select
                  v-model:value="appointmentForm.appointment_type"
                  :options="$resources.appointmentTypes.data?.options"
                  @change="(value, option) => {
                    appointmentForm.appointment_for = option.allow_booking_for;
                    appointmentForm.duration = option.default_duration;
                    appointmentForm.practitioner = '';
                    appointmentForm.practitioner_name = '';
                    appointmentForm.department = '';
                    appointmentForm.service_unit = '';
                    appointmentForm.appointment_time = '';
                  }"
                  :fieldNames="{label: 'appointment_type', value: 'name'}"
                  show-search
                  :loading="$resources.appointmentTypes.list.loading"
                  @search="(value) => {handleSearch(
                    value, 
                    $resources.appointmentTypes, 
                    {appointment_type: ['like', `%${value}%`]}, 
                    {},
                  )}"
                  :filterOption="false"
                  :disabled="appointmentForm.type == 'Edit Appointment'"
                  ></a-select>
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
                  <a-select
                  v-model:value="appointmentForm.custom_branch"
                  :options="$resources.branches.data?.options"
                  :fieldNames="{label: 'name', value: 'name'}"
                  show-search
                  :loading="$resources.branches.list.loading"
                  @search="(value) => {handleSearch(
                    value, 
                    $resources.branches, 
                    {name: ['like', `%${value}%`]}, 
                    {},
                  )}"
                  :filterOption="false"
                  ></a-select>
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
                  <a-select
                  v-model:value="appointmentForm.department"
                  :options="$resources.departments.data?.options"
                  :fieldNames="{label: 'department', value: 'name'}"
                  show-search
                  :loading="$resources.departments.list.loading"
                  @search="(value) => {handleSearch(
                    value, 
                    $resources.departments, 
                    {department: ['like', `%${value}%`]}, 
                    {},
                  )}"
                  :filterOption="false"
                  ></a-select>
                </a-form-item>
                <a-form-item label="Room" 
                name="service_unit" 
                v-if="appointmentForm.appointment_for === 'Service Unit' || appointmentForm.custom_is_walked_in || freeBooking" 
                >
                  <a-select
                  v-model:value="appointmentForm.service_unit"
                  :options="$resources.serviceUnits.data?.options"
                  :fieldNames="{label: 'name', value: 'name'}"
                  show-search
                  :loading="$resources.serviceUnits.list.loading"
                  @search="(value) => {handleSearch(
                    value, 
                    $resources.serviceUnits, 
                    {allow_appointments: 1, is_group: 0, name: ['like', `%${value}%`]}, 
                    {allow_appointments: 1, is_group: 0},
                  )}"
                  :filterOption="false"
                  ></a-select>
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
                @change="() => {
                  appointmentForm.custom_is_walked_in = false
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
          
          text="submit"
          variant="tonal"
          @click="onSubmit()"
          type="submit"
          ></v-btn>
        </v-card-actions>
      </a-form>
    </v-card>
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

export default {
	inject: ['$call'],
	components: {ListView, VDivider, VContainer, VCol, VRow, VItemGroup, VItem, VMenu, VList, VListItem, VListItemTitle},
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
    departments() { return { 
      type: 'list', 
      doctype: 'Medical Department', 
      fields: ['name', 'department'], 
      auto: true, 
      orderBy: 'department', 
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
    branches() { return { 
      type: 'list', 
      doctype: 'Branch', 
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
    appointmentTypes() { return { 
      type: 'list', 
      doctype: 'Appointment Type', 
      fields: ['name', 'appointment_type', 'allow_booking_for', 'default_duration'], 
      auto: true, 
      orderBy: 'appointment_type',
      pageLength: 10,
      url: 'frappe.desk.reportview.get', 
      transform(data) {
        if(data.values.length == 0)
          data.options = []
        else{
          data.options = this.transformData(data.keys, data.values);  // Transform the result into objects
          this.appointmentForm.appointment_type = data.options[0].appointment_type
          this.appointmentForm.appointment_for = data.options[0].allow_booking_for
        }
        return data
			},
    }},
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
    serviceUnits() { return { 
      type: 'list', 
      doctype: 'Healthcare Service Unit', 
      fields:['name'], 
      filters:{'allow_appointments': 1, 'is_group': 0}, 
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
    patients() { return { 
      type: 'list', 
      doctype: 'Patient', 
      fields: [
        'sex', 'patient_name', 'name', 'custom_cpr', 'dob', 'mobile', 'email', 'blood_group', 
        'inpatient_record', 'inpatient_status', 'custom_default_payment_type',
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
      fields: ['name', 'template', 'medical_department'], 
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
    appointmentForm() {
      return reactive(this.form);
    },
    rulesRef() {
      return reactive({
        appointment_type: [{ required: true, message: 'Please choose a type!' }],
        patient: [{ required: true, message: 'Please choose a patient!' }],
        practitioner: [{ required: this.appointmentForm.appointment_for === 'Practitioner', message: 'Please choose a practitioner!' }],
        department: [{ required: this.appointmentForm.appointment_for === 'Department', message: 'Please choose a department!' }],
        service_unit: [{ required: true, message: 'Please choose a room!' }],
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
      patientSearch: '',
      pastAppointments: [],
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
  mounted() {
    
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
        this.pastAppointments = response
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
          children = {custom_procedure_templates: form.procedure_templates.map(value => ({template: value.template}))}
          this.$call('healthcare_doworks.api.methods.reschedule_appointment', {form, children})
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
    showPopover(event) {
      if(this.appointmentForm.patient)
        this.$refs.popover.toggle(event); // Show the popover
    },
    hidePopover() {
      this.$refs.popover.hide(); // Hide the popover
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