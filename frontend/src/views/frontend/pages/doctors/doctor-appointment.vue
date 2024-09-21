<template>
  <!-- Main Wrapper -->
  <div class="main-wrapper mr-4">
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
    <!-- Page Content -->
    <div class="appointment-tab">
      <!-- Clock And Other Filters -->
      <div class="flex-wrap flex-col flex-xxl-row gap-3 nav nav-tabs nav-tabs-solid pb-2">
        <div class="flex flex-wrap flex-col flex-lg-row gap-3 flex-auto order-2 order-xxl-1">
          <div class="flex flex-col" style="width: 17rem">
            <a-select v-if="dateFilterType === 'span'"
            v-model:value="selectedSpan"
            style="width: 100%; align-items: center; max-height: 62px; text-align: center"
            :options="spans"
            size="large"
            @change="(value) => {
              const dates = spanToDate(value)
              selectedDates = dates
              selectedRangeDates = [dates[0], dates[dates.length -1]]
              fetchRecords()
            }"
            ></a-select>
            <a-date-picker v-if="dateFilterType === 'single'"
            v-model:value="selectedDates[0]"
            format="D/M/YY"
            style="width: 100%; align-items: center; max-height: 62px; text-align: center"
            :allowClear="false"
            size="large"
            @change="(value) => {selectedDates = [value]; selectedRangeDates = [value, value]; fetchRecords()}"
            />
            <!-- <span class="d-flex justify-content-center fw-bolder text-dark me-3">{{ formattedDayOfWeek() }}</span> -->
            <a-range-picker v-if="dateFilterType === 'range'" 
            v-model:value="selectedRangeDates" 
            format="D/M/YY" 
            style="width: 100%; align-items: center; max-height: 62px; text-align: center" 
            size="large"
            :allowClear="false"
            @change="(value) => {selectedDates = getDatesInBetween(value[0], value[1]); fetchRecords()}"
            />
            <v-btn-toggle class="mt-1" v-model="dateFilterType" color="blue" mandatory density="compact">
              <v-btn size="small" value="span">Timespans</v-btn>
              <v-btn size="small" value="single">Single</v-btn>
              <v-btn size="small" value="range">Range</v-btn>
            </v-btn-toggle>
            <!-- <a-radio-group class="mt-2" v-model:value="dateFilterType">
              <a-radio-button value="span">Timespan</a-radio-button>
              <a-radio-button value="single">Single</a-radio-button>
              <a-radio-button value="range">Range</a-radio-button>
            </a-radio-group> -->
          </div>
          <div class="flex flex-col" style="width: 17rem">
            <a-select
            v-model:value="selectedDepartments"
            mode="multiple"
            style="width: 100%; align-items: center; max-height: 62px;"
            placeholder="Departments"
            max-tag-count="responsive"
            :options="$resources.departments.data?.options"
            :fieldNames="{label:'department', value: 'name'}"
            size="large"
            show-search
            :loading="$resources.departments.list.loading"
            @search="(value) => {handleSearch(
              value, 
              $resources.departments, 
              {department: ['like', `%${value}%`]}, 
              {},
            )}"
            :filterOption="false"
            >
            </a-select>
          </div>
          <div class="flex flex-col" style="width: 17rem">
            <a-input v-model:value="searchValue" placeholder="Search" size="large">
              <template #prefix>
                <v-icon icon="mdi mdi-magnify" color="grey"></v-icon>
              </template>
            </a-input>
          </div>
        </div>
        <div class="ms-xxl-auto order-1 order-xxl-2 w-fit">
          <Clock/>
        </div>
      </div>
      
      <!-- Toolbar Actions -->
      <v-toolbar color="blue-lighten-5">
        <v-btn icon="mdi mdi-plus" @click="appointmentDialog('New Appointment', true)" rounded="0"></v-btn>
      </v-toolbar>

      <!-- Appointment Tab -->
      <v-tabs v-model="tab" align-tabs="center" color="indigo" bg-color="white" show-arrows>
        <v-tab v-for="(value, key) in groupedAppointments" :key="key" :value="key">
          {{ key }}
          <v-badge :color="getBadgeNumber(key) > 0 ? 'green' : 'indigo'" :content="getBadgeNumber(key)" inline></v-badge>
        </v-tab>
      </v-tabs>
      <div v-if="appointmentsLoading">
        <v-progress-linear v-model="progressValue" color="purple" height="4"></v-progress-linear>
      </div>
      <div class="tab-content">
        <v-window v-model="tab" disabled>
          <v-window-item v-for="(value, key) in groupedAppointments" :key="key" :value="key">
            <AppointmentTab 
            :searchValue="searchValue"
            :selectedDates="selectedDates"
            :selectedDepartments="selectedDepartments" 
            :appointments="value" 
            :tab="key.toLowerCase()"
            :loading="appointmentsLoading"
            ref="appointmentTabRef"
            @show-alert="showAlert"
            @appointment-dialog="appointmentDialog"
            @appointment-note-dialog="appointmentNoteDialog"
            @appointment-invoice-dialog="appointmentInvoiceDialog"
            @vital-sign-dialog="vitalSignDialog"
            @service-unit-dialog="serviceUnitDialog"
            @payment-type-dialog="paymentTypeDialog"
            @transfer-practitioner-dialog="transferPractitionerDialog"
            />
          </v-window-item>
        </v-window>
      </div>
      <!-- /Appointment Tab -->
      
    </div>
    <!-- /Page Content -->

    <!-- Page Dialogs -->
    <patientAppointmentDialog 
    :isOpen="appointmentOpen" 
    @update:isOpen="appointmentOpen = $event" 
    @show-alert="showAlert" 
    @show-slots="showSlots"
    :form="appointmentForm"
    :slots="slots"
    />
    <vitalSignsListDialog 
    :isOpen="vitalSignsOpen" 
    @update:isOpen="vitalSignsOpen = $event" 
    @show-alert="showAlert" 
    :appointment="selectedRow"
    />
    <appointmentNoteDialog 
    :isOpen="appointmentNoteOpen" 
    @update:isOpen="appointmentNoteOpen = $event" 
    @show-alert="showAlert" 
    :appointmentId="selectedRow.name"
    />
    <appointmentInvoiceDialog 
    :isOpen="appointmentInvoiceOpen" 
    @update:isOpen="appointmentInvoiceOpen = $event" 
    @show-alert="showAlert" 
    :appointment="selectedRow"
    />
    <v-dialog v-model="serviceUnitOpen" width="auto">
      <v-card
        rounded="lg"
        width="auto"
        prepend-icon="mdi mdi-door-open"
        title="Update Room"
      >
        <v-card-text>
          <a-select
          v-model:value="appointmentForm.service_unit"
          :options="$resources.serviceUnits.data?.options"
          :fieldNames="{label: 'name', value: 'name'}"
          style="min-width: 400px; max-width: 600px;"
          show-search
          :loading="$resources.serviceUnits.list.loading"
          @search="(value) => {handleSearch(
            value, 
            $resources.serviceUnits, 
            {allow_appointments: 1, name: ['like', `%${value}%`]}, 
            {allow_appointments: 1},
          )}"
          :filterOption="false"
          ></a-select>
        </v-card-text>

        <v-card-actions class="my-2 d-flex justify-end">
          <v-btn
          class="text-none"
          text="Cancel"
          @click="serviceUnitOpen = false"
          ></v-btn>

          <v-btn
          class="text-none"
          color="blue"
          
          text="submit"
          variant="tonal"
          @click="onSubmitServiceUnit()"
          ></v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="transferOpen" width="auto">
      <v-card
        rounded="lg"
        width="auto"
        prepend-icon="mdi mdi-door-open"
        title="Transfer To Practitioner"
      >
        <v-card-text>
          <a-select
          v-model:value="appointmentForm.practitioner_name"
          :options="$resources.practitioners.data?.options"
          :fieldNames="{label: 'practitioner_name', value: 'name'}"
          style="min-width: 400px; max-width: 600px;"
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
        </v-card-text>

        <v-card-actions class="my-2 d-flex justify-end">
          <v-btn
          class="text-none"
          text="Cancel"
          @click="transferOpen = false"
          ></v-btn>

          <v-btn
          class="text-none"
          color="blue"
          
          text="Submit"
          variant="tonal"
          @click="onSubmitTransferPractitioner()"
          ></v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="paymentTypeOpen" width="auto">
      <v-card
        rounded="lg"
        width="auto"
        prepend-icon="pi pi-wallet"
        title="Update Payment Type"
      >
        <v-card-text>
          <a-select
            v-model:value="appointmentForm.custom_payment_type"
            :options="[{label: '', value: ''}, {label: 'Self Payment', value: 'Self Payment'}, {label: 'Insurance', value: 'Insurance'}]"
            style="min-width: 400px; max-width: 600px;"
          ></a-select>
        </v-card-text>

        <v-card-actions class="my-2 d-flex justify-end">
          <v-btn
          class="text-none"
          text="Cancel"
          @click="paymentTypeOpen = false"
          ></v-btn>

          <v-btn
          class="text-none"
          color="blue"
          
          text="submit"
          variant="tonal"
          @click="onSubmitPaymentType()"
          ></v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <!-- / Page Dialogs -->
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
  </div>
</template>

<script >
import { ref } from 'vue';
import moment from "moment";
import dayjs from 'dayjs';
import Clock from '@/components/clock/Clock.vue';

import { VIcon } from 'vuetify/components/VIcon';
import { VToolbar, VToolbarItems } from 'vuetify/components/VToolbar';
import { VBtnToggle } from 'vuetify/components/VBtnToggle';
import { VProgressLinear } from 'vuetify/components/VProgressLinear';

import AppointmentTab from './doctor-appointment-tab.vue'

export default {
  inject: ['$socket', '$call'],
  components: {
    AppointmentTab, Clock, VIcon, VToolbar, VToolbarItems, VBtnToggle, VProgressLinear,
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
      }
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
      filters:{'allow_appointments': 1}, 
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
      fields: ['sex', 'patient_name', 'name', 'custom_cpr', 'dob', 'mobile', 'email', 'blood_group', 'inpatient_record', 'inpatient_status'], 
      filters: {status: 'Active'},
      auto: true, 
      orderBy: 'patient_name',
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
  data() {
    return {
      tab: 'Scheduled',
      appointments: [],
      groupedAppointments: {Scheduled:[], Arrived:[], Ready:[], 'In Room':[], Completed:[], 'No Show':[],},
      searchValue: '',
      selectedDepartments: undefined,
      appointmentsLoading: false,
      appointmentOpen: false,
      appointmentNoteOpen: false,
      vitalSignsOpen: false,
      serviceUnitOpen: false,
      transferOpen: false,
      paymentTypeOpen: false,
      appointmentInvoiceOpen: false,
      lodingOverlay: false,
      slots: {},
      message: '',
      alertVisible: false,
      appointmentForm: {},
      selectedRow: {name: '', patient_details: {id: ''}},
      dateFilterType: 'span',
      selectedSpan: 'today',
      selectedDates: ref([dayjs()]),
      selectedRangeDates: [dayjs().startOf('isoWeek').subtract(1, 'day'), dayjs().endOf('isoWeek').subtract(1, 'day')],
      spans: [
        {label: 'Yesterday', value: 'yesterday'},
        {label: 'Today', value: 'today'},
        {label: 'Tomorrow', value: 'tomorrow'},
        {label: 'Last Week', value: 'last week'},
        {label: 'This Week', value: 'this week'},
        {label: 'Next Week', value: 'next week'},
        {label: 'Last Month', value: 'last month'},
        {label: 'This Month', value: 'this month'},
        {label: 'Next Month',  value: 'next month'},
      ],
      totalRecords: 0,
      progressValue: 0,
    };
  },
  created() {
    this.$socket.on('patient_appointments_chunk', (chunk) => {
      this.appointmentsLoading = true;
      this.appointments = this.adjustAppointments([...this.appointments, ...chunk.data]);
      if(chunk.total)
        this.totalRecords = chunk.total;
      this.groupAppointmentsByStatus();
      this.updateProgress();
      if (this.appointments.length >= this.totalRecords) {
        this.appointmentsLoading = false;
      }
    });

    this.$socket.on('patient_appointments_updated', updatedAppointment => {
      if (updatedAppointment) {
        const appointmentDate = dayjs(updatedAppointment.appointment_date);

        // Check if the updated appointment falls within the selected date range
        const isInDateRange = this.selectedDates.some(date => date.isSame(appointmentDate, 'day'));

        if (isInDateRange) {
          const index = this.appointments.findIndex(app => app.name === updatedAppointment.name);

          if (index !== -1) {
            // Update the existing appointment
            this.appointments.splice(index, 1, this.adjustAppointments([updatedAppointment])[0]);
          } else {
            // If not in the list, add it
            this.appointments.push(this.adjustAppointments([updatedAppointment])[0]);
          }

          this.groupAppointmentsByStatus();  // Re-group appointments by status
        }
      }
    })
  },

  mounted() {
    if (this.$socket.connected) {
      this.fetchRecords();  // Fetch appointments if socket is already connected
    } else {
      this.$socket.on('connect', () => {
        this.fetchRecords();  // Fetch records when the socket connects
      });
    }
  },
  methods: {
    showAlert(message, duration) {
      this.message = message;
      this.alertVisible = true;
      setTimeout(() => {
        this.alertVisible = false;
      }, duration);
    },
    fetchRecords() {
      this.appointments = []
      const dates = this.selectedDates.map(date => date.format('YYYY-MM-DD'));
      this.$call('healthcare_doworks.api.methods.fetch_patient_appointments', {
        filters: {appointment_date: ['in', dates]},
        total_records: true  // Only get the total count once
      })
    },
    adjustAppointments(data) {
			return [...(data || [])].map((d) => {
        d.visit_notes = d.visit_notes.map(note => {
          note.dayDate = dayjs(note.time).format('DD/MM/YYYY')
          note.dayTime = dayjs(note.time).format('h:mm A')
          return note
        })
        d.arriveTime = '-'
        d.status_log.forEach(value => {
          if(value.status == 'Arrived')
            d.arriveTime = dayjs(value.time)
        })
        d.appointment_date_moment = dayjs(d.appointment_date + ' ' + d.appointment_time).format('D/MM/YYYY');
				d.appointment_time_moment = dayjs(d.appointment_date + ' ' + d.appointment_time).format('h:mm a');
				d.patient_cpr = d.patient_name + ' ' + d.patient_details.cpr

				return d;
			});
		},
    spanToDate(span) {
      if(span){
        if(span === 'yesterday')
          return [dayjs().add(-1, 'd')]
        if(span === 'today')
          return [dayjs()]
        if(span === 'tomorrow')
          return [dayjs().add(1, 'd')]
        if(span === 'last week'){
          const lwRange = [dayjs().subtract(1, 'week').startOf('isoWeek').subtract(1, 'day'), dayjs().subtract(1, 'week').endOf('isoWeek').subtract(1, 'day')]
          return this.getDatesInBetween(lwRange[0], lwRange[1])
        }
        if(span === 'this week'){
          const twRange = [dayjs().startOf('isoWeek').subtract(1, 'day'), dayjs().endOf('isoWeek').subtract(1, 'day')]
          return this.getDatesInBetween(twRange[0], twRange[1])
        }
        if(span === 'next week'){
          const nwRange = [dayjs().add(1, 'week').startOf('isoWeek').subtract(1, 'day'), dayjs().add(1, 'week').endOf('isoWeek').subtract(1, 'day')]
          return this.getDatesInBetween(nwRange[0], nwRange[1])
        }
        if(span === 'last month'){
          const lmRange = [dayjs().subtract(1, 'month').startOf('month'), dayjs().subtract(1, 'month').endOf('month')]
          return this.getDatesInBetween(lmRange[0], lmRange[1])
        }
        if(span === 'this month'){
          const tmRange = [dayjs().startOf('month'), dayjs().endOf('month')]
          return this.getDatesInBetween(tmRange[0], tmRange[1])
        }
        if(span === 'next month'){
          const nmRange = [dayjs().add(1, 'month').startOf('month'), dayjs().add(1, 'month').endOf('month')]
          return this.getDatesInBetween(nmRange[0], nmRange[1])
        }
        return undefined
      }
      return undefined
    },
    getDatesInBetween(startDate, endDate) {
      let dates = []
      
      while (startDate.isBefore(endDate) || startDate.isSame(endDate, 'day')) {
        dates.push(startDate);
        startDate = startDate.add(1, 'day');
      }
      return dates
    },
    getBadgeNumber(tab){
      let count = 0
      if(this.groupedAppointments[tab]){
        count = this.groupedAppointments[tab].reduce((total, value) => {
          let departmentFilter = true
          let dateFilter = true
          if(this.selectedDepartments)
            departmentFilter = this.selectedDepartments.some(department => {return department === value.department})
          if(this.selectedDates.length > 0)
            dateFilter = this.selectedDates.some(date => {return date.format('YYYY-MM-DD') === value.appointment_date})
          if(dateFilter && departmentFilter){
            return total + 1
          }
          return total
        },0)
      }
      return count
    },
    groupAppointmentsByStatus() {
      this.groupedAppointments = {Scheduled:[], Arrived:[], Ready:[], 'In Room':[], Completed:[], 'No Show':[],}
      this.appointments.forEach(appointment => {
        const status = appointment.custom_visit_status;
        if (!this.groupedAppointments[status])
          this.groupedAppointments[status] = [];
        this.groupedAppointments[status].push(appointment);
      });
    },
    appointmentDialog(formType, isNew, row) {
      if(isNew){
        this.appointmentForm.name = '';
				this.appointmentForm.duration = this.$resources.appointmentTypes.data.options[0].default_duration;
				this.appointmentForm.appointment_type = this.$resources.appointmentTypes.data.options[0].appointment_type;
				this.appointmentForm.appointment_for = this.$resources.appointmentTypes.data.options[0].allow_booking_for;
				this.appointmentForm.custom_appointment_category = 'First Time';
        this.appointmentForm.custom_procedure_template = '';
        this.appointmentForm.custom_payment_type = '';
        this.appointmentForm.practitioner = '';
				this.appointmentForm.practitioner_name = '';
				this.appointmentForm.patient = '';
				this.appointmentForm.patient_name = '';
				this.appointmentForm.patient_sex = '';
				this.appointmentForm.department = '';
				this.appointmentForm.service_unit = '';
        this.appointmentForm.notes = '';
        this.appointmentForm.appointment_date = this.appointmentForm.appointment_time = undefined;
			}
			else{
        this.appointmentForm.name = row.name;
				this.appointmentForm.duration = row.duration;
				this.appointmentForm.appointment_type = row.appointment_type;
				this.appointmentForm.appointment_for = row.appointment_for;
				this.appointmentForm.custom_appointment_category = row.custom_appointment_category;
        this.appointmentForm.custom_procedure_template = row.custom_procedure_template;
        this.appointmentForm.custom_payment_type = row.custom_payment_type;
        this.appointmentForm.practitioner = row.practitioner;
				this.appointmentForm.practitioner_name = row.practitioner_name;
				this.appointmentForm.patient = row.patient_details.id;
				this.appointmentForm.patient_name = row.patient_name;
				this.appointmentForm.patient_sex = row.patient_details.gender;
				this.appointmentForm.department = row.department;
				this.appointmentForm.service_unit = row.service_unit;
        this.appointmentForm.notes = row.notes;
        this.appointmentForm.appointment_date = dayjs(row.appointment_date)
        this.appointmentForm.appointment_time = undefined;
			}
      this.showSlots()
      this.appointmentForm.doctype = 'Patient Appointment';
      // this.appointmentForm.appointment_date = this.appointmentForm.appointment_time = undefined;
			this.appointmentForm.type = formType
      this.appointmentForm.custom_is_walked_in = false;
			this.appointmentOpen = true
		},
    appointmentNoteDialog(row) {
      this.selectedRow = row
			this.appointmentNoteOpen = true;
		},
    appointmentInvoiceDialog(row) {
      console.log(row)
      this.selectedRow = row
			this.appointmentInvoiceOpen = true;
		},
    vitalSignDialog(row) {
      this.selectedRow = row
			this.vitalSignsOpen = true;
		},
    transferPractitionerDialog(row) {
      this.appointmentForm.name = row.name;
      this.appointmentForm.practitioner = row.practitioner;
      this.appointmentForm.practitioner_name = row.practitioner_name;
			this.transferOpen = true
		},
    serviceUnitDialog(row) {
      this.appointmentForm.name = row.name;
      this.appointmentForm.service_unit = row.service_unit;
			this.serviceUnitOpen = true
		},
    paymentTypeDialog(row) {
      this.appointmentForm.name = row.name;
      this.appointmentForm.custom_payment_type = row.custom_payment_type;
			this.paymentTypeOpen = true
    },
    showSlots() {
      if (this.appointmentForm.appointment_date && this.appointmentForm.practitioner) {
        this.slots = {};
        let tempForm = this.appointmentForm;
        tempForm.__islocal = 1;
        tempForm.__unsaved = 1;
        this.$call('healthcare.healthcare.doctype.patient_appointment.patient_appointment.get_availability_data', {
          practitioner: this.appointmentForm.practitioner,
          date: this.appointmentForm.appointment_date.format('YYYY/MM/DD'),
          appointment: JSON.stringify(tempForm)
        }).then((data) => {
          if (data.slot_details.length > 0) {
            // make buttons for each slot
            this.getSlots(data);
          } else {
            let message = error.message.split('\n');
            message = message.find(line => line.includes('frappe.exceptions'));
            const firstSpaceIndex = message.indexOf(' ');
            this.showAlert(message.substring(firstSpaceIndex + 1) , 10000)
          }
        }).catch(error => {
          let message = error.message.split('\n');
          message = message.find(line => line.includes('frappe.exceptions'));
          const firstSpaceIndex = message.indexOf(' ');
          this.showAlert(message.substring(firstSpaceIndex + 1) , 10000)
        });
      } 
	  },
    getSlots(data) {
      let appointment_count = 0;
      let slot_start_time, slot_end_time, available_slots;
      let appointment_date = this.appointmentForm.appointment_date

      data.slot_details.forEach((slot_info) => {
        slot_info.avail_slot.map(slot => {
          appointment_count = 0;
          slot.disabled = false;
          slot.count_class = '';
          slot_start_time = moment(slot.from_time, 'HH:mm:ss');
          slot_end_time = moment(slot.to_time, 'HH:mm:ss');
          slot.interval = (slot_end_time - slot_start_time) / 60000 | 0;

          // restrict past slots based on the current time.
          let now = moment();
          let booked_moment = ""
          if((now.format("YYYY-MM-DD") == appointment_date) && (slot_start_time.isBefore(now) && !slot.maximum_appointments)){
            slot.disabled = true;
          } else {
            // iterate in all booked appointments, update the start time and duration
            slot_info.appointments.forEach((booked) => {
              booked_moment = moment(booked.appointment_time, 'HH:mm:ss');
              let end_time = booked_moment.clone().add(booked.duration, 'minutes');

              // to get apointment count for all day appointments
              if (slot.maximum_appointments) {
                if (booked.appointment_date == appointment_date) {
                  appointment_count++;
                }
              }
              // Deal with 0 duration appointments
              if (booked_moment.isSame(slot_start_time) || booked_moment.isBetween(slot_start_time, slot_end_time)) {
                if (booked.duration == 0) {
                  slot.disabled = true;
                  return false;
                }
              }

              // Check for overlaps considering appointment duration
              if (slot_info.allow_overlap != 1) {
                if (slot_start_time.isBefore(end_time) && slot_end_time.isAfter(booked_moment)) {
                  // There is an overlap
                  slot.disabled = true;
                  return false;
                }
              } else {
                if (slot_start_time.isBefore(end_time) && slot_end_time.isAfter(booked_moment)) {
                  appointment_count++;
                }
                if (appointment_count >= slot_info.service_unit_capacity) {
                  // There is an overlap
                  slot.disabled = true;
                  return false;
                }
              }
            });
          }
          if (slot_info.allow_overlap == 1 && slot_info.service_unit_capacity > 1) {
            available_slots = slot_info.service_unit_capacity - appointment_count;
            slot.count = `${(available_slots > 0 ? available_slots : 'Full')}`;
            slot.count_class = `${(available_slots > 0 ? 'badge-success' : 'badge-danger')}`;
            slot.tool_tip =`${available_slots} slots available for booking`;
          }

          if (slot.maximum_appointments) {
            if (appointment_count >= slot.maximum_appointments) {
              slot.disabled = true;
            }
            else {
              slot.disabled = false;
            }
            available_slots = slot.maximum_appointments - appointment_count;
            slot.count = `${(available_slots > 0 ? available_slots : 'Full')}`;
            slot.count_class = `${(available_slots > 0 ? 'badge-success' : 'badge-danger')}`;
          } 
        });
      });
      this.slots = data;
    },
    onSubmitTransferPractitioner() {
      this.lodingOverlay = true;
      this.$call('healthcare_doworks.api.methods.transferToPractitioner', 
        {app: this.appointmentForm.name, practitioner: this.appointmentForm.practitioner}
      ).then(response => {
        this.lodingOverlay = false;
        this.transferOpen = false;
      }).catch(error => {
        console.error(error);
        let message = error.message.split('\n');
        message = message.find(line => line.includes('frappe.exceptions'));
        if(message){
          const firstSpaceIndex = message.indexOf(' ');
          this.showAlert(message.substring(firstSpaceIndex + 1) , 10000)
        }
      });
    },
    onSubmitServiceUnit() {
      this.lodingOverlay = true;
      this.$call('frappe.client.set_value', 
        {doctype: 'Patient Appointment', name: this.appointmentForm.name, fieldname: 'service_unit', value: this.appointmentForm.service_unit}
      ).then(response => {
        this.lodingOverlay = false;
        this.serviceUnitOpen = false;
      }).catch(error => {
        console.error(error);
        let message = error.message.split('\n');
        message = message.find(line => line.includes('frappe.exceptions'));
        if(message){
          const firstSpaceIndex = message.indexOf(' ');
          this.showAlert(message.substring(firstSpaceIndex + 1) , 10000)
        }
      });
    },
    onSubmitPaymentType() {
      this.lodingOverlay = true;
      this.$call('frappe.client.set_value', 
        {doctype: 'Patient Appointment', name: this.appointmentForm.name, fieldname: 'custom_payment_type', value: this.appointmentForm.custom_payment_type}
      ).then(response => {
        this.lodingOverlay = false;
        this.paymentTypeOpen = false;
      }).catch(error => {
        console.error(error);
        let message = error.message.split('\n');
        message = message.find(line => line.includes('frappe.exceptions'));
        if(message){
          const firstSpaceIndex = message.indexOf(' ');
          this.showAlert(message.substring(firstSpaceIndex + 1) , 10000)
        }
      });
    },
    onPage(event) {
      const page = event.page + 1;  // PrimeVue pages start from 0, adjust accordingly
      const limit = event.rows;
      this.fetchRecords(page, limit);
    },
    updateProgress() {
      this.progressValue = (this.appointments.length / this.totalRecords) * 100;
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
    // formattedDayOfWeek() {
    //   if (!this.selectedDates) return '';
    //   return dayjs(this.selectedDates).format('dddd');
    // },
  },
  name: 'Appointments',
};
</script>

<style>
.appointment-tab .ant-picker-input input{
  cursor: 'pointer';
  text-align: center;
}
</style>