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
          <div class="flex flex-col" style="width: 15rem">
            <a-select v-if="dateFilterType === 'span'"
            v-model:value="selectedSpan"
            style="width: 100%; align-items: center; max-height: 62px; text-align: center"
            :options="spans"
            size="large"
            @change="(value) => {
              const dates = spanToDate(value)
              selectedDates = dates
              selectedRangeDates = [dates[0], dates[dates.length -1]]
            }"
            ></a-select>
            <a-date-picker v-if="dateFilterType === 'single'"
            v-model:value="selectedDates[0]"
            format="D/M/YY"
            style="width: 100%; align-items: center; max-height: 62px; text-align: center"
            :allowClear="false"
            size="large"
            @change="(value) => {selectedDates = [value]; selectedRangeDates = [value, value]}"
            />
            <!-- <span class="d-flex justify-content-center fw-bolder text-dark me-3">{{ formattedDayOfWeek() }}</span> -->
            <a-range-picker v-if="dateFilterType === 'range'" 
            v-model:value="selectedRangeDates" 
            format="D/M/YY" 
            style="width: 100%; align-items: center; max-height: 62px; text-align: center" 
            size="large"
            :allowClear="false"
            @change="(value) => {selectedDates = getDatesInBetween(value[0], value[1])}"
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
          <div class="flex flex-col" style="width: 15rem">
            <a-select
              v-model:value="selectedDepartments"
              mode="multiple"
              style="width: 100%; align-items: center; max-height: 62px;"
              placeholder="Departments"
              max-tag-count="responsive"
              :options="$myresources.departments"
              :fieldNames="{label:'department', value: 'department'}"
              size="large"
            >
            </a-select>
          </div>
          <div class="flex flex-col" style="width: 15rem">
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
          <v-badge color="indigo" :content="getBadgeNumber(key)" inline></v-badge>
        </v-tab>
      </v-tabs>
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
            @appointment-dialog="appointmentDialog"
            @appointment-note-dialog="appointmentNoteDialog"
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
    :appointment="{'name': selectedRow.appointment_id, 'patient': selectedRow.patient_details.id}"
    />
    <v-dialog v-model="appointmentNoteOpen" width="auto">
      <v-card
        rounded="lg"
        width="auto"
        prepend-icon="mdi mdi-door-open"
        title="Add Note"
      >
        <v-card-text>
          <a-form-item label="Provider">
            <a-input v-model:value="newNote.provider" />
          </a-form-item>
          <a-form-item label="Notes">
            <a-textarea v-model:value="newNote.note" placeholder="Notes" :rows="4" />
          </a-form-item>
        </v-card-text>

        <v-card-actions class="my-2 d-flex justify-end">
          <v-btn
          class="text-none"
          text="Cancel"
          @click="isActive.value = false"
          ></v-btn>

          <v-btn
          class="text-none"
          color="blue"
          
          text="Submit"
          variant="tonal"
          @click="onSubmitAppointmentNote()"
          ></v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
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
            :options="$myresources.serviceUnits"
            :fieldNames="{label: 'name', value: 'name'}"
            show-search
            style="min-width: 400px; max-width: 600px;"
          ></a-select>
        </v-card-text>

        <v-card-actions class="my-2 d-flex justify-end">
          <v-btn
          class="text-none"
          text="Cancel"
          @click="isActive.value = false"
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
            :options="$myresources.practitioners"
            :fieldNames="{label: 'practitioner_name', value: 'name'}"
            show-search
            style="min-width: 400px; max-width: 600px;"
          ></a-select>
        </v-card-text>

        <v-card-actions class="my-2 d-flex justify-end">
          <v-btn
          class="text-none"
          text="Cancel"
          @click="isActive.value = false"
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
          @click="isActive.value = false"
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

import AppointmentTab from './doctor-appointment-tab.vue'

export default {
  inject: ['$socket', '$call'],
  components: {
    AppointmentTab, Clock, VIcon, VToolbar, VToolbarItems, VBtnToggle,
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
      lodingOverlay: false,
      slots: {},
      newNote: {},
      message: '',
      alertVisible: false,
      appointmentForm: {},
      selectedRow: {appointment_id: '', patient_details: {id: ''}},
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
    };
  },
  created() {
    this.fetchRecords();
    this.$socket.on('patient_appointments', response => {
      if(response){
        this.appointments = this.adjustAppointments(response)
        this.groupAppointmentsByStatus();
      }
    })
  },
  mounted() {
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
      this.appointmentsLoading = true;
      this.$call('healthcare_doworks.api.methods.fetch_patient_appointments')
      .then(response => {
        console.log(response)
        this.appointments = this.adjustAppointments(response)
        this.groupAppointmentsByStatus();
        this.appointmentsLoading = false;
      })
      .catch(error => {
        this.appointmentsLoading = false;
        console.error('Error fetching records:', error);
      });
    },
    adjustAppointments(data) {
			return [...(data || [])].map((d) => {
        try {
          if(typeof d.patient_details === 'string'){
            d.patient_details = JSON.parse(d.patient_details)    
          }
          if(typeof d.visit_notes === 'string'){
            let notes = JSON.parse(d.visit_notes).map(note => {
              note.time = dayjs(note.time).format('h:mm A DD/MM/YYYY')
              return note
            })
            d.visit_notes = notes
          }
          if(typeof d.status_log === 'string'){
            d.status_log = JSON.parse(d.status_log)
            d.arriveTime = '-'
            d.status_log.forEach(value => {
              if(value.status == 'Arrived')
              d.arriveTime = dayjs(value.time)
            })
          }
          
        } catch (error) {
          console.error('Error parsing JSON:', error);
        }

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
        const status = appointment.visit_status;
        if (!this.groupedAppointments[status])
          this.groupedAppointments[status] = [];
        this.groupedAppointments[status].push(appointment);
      });
    },
    appointmentDialog(formType, isNew, row) {
      if(isNew){
        let duration = 0
        this.$myresources.appointmentTypes.forEach(value => {
          if(value.appointment_type === 'Practitioner')
            duration = value.default_duration
        })
        this.appointmentForm.name = '';
				this.appointmentForm.duration = duration;
				this.appointmentForm.appointment_type = 'Practitioner';
				this.appointmentForm.appointment_for = 'Practitioner';
				this.appointmentForm.custom_appointment_category = 'First Time';
        this.appointmentForm.custom_payment_type = '';
        this.appointmentForm.practitioner = '';
				this.appointmentForm.practitioner_name = '';
				this.appointmentForm.patient = '';
				this.appointmentForm.patient_name = '';
				this.appointmentForm.patient_sex = '';
				this.appointmentForm.department = '';
				this.appointmentForm.service_unit = '';
        this.appointmentForm.notes = '';
			}
			else{
        this.appointmentForm.name = row.appointment_id;
				this.appointmentForm.duration = row.duration;
				this.appointmentForm.appointment_type = row.appointment_type;
				this.appointmentForm.appointment_for = row.appointment_for;
				this.appointmentForm.custom_appointment_category = row.appointment_category;
        this.appointmentForm.custom_payment_type = row.payment_type;
        this.appointmentForm.practitioner = row.practitioner;
				this.appointmentForm.practitioner_name = row.practitioner_name;
				this.appointmentForm.patient = row.patient_details.id;
				this.appointmentForm.patient_name = row.patient_name;
				this.appointmentForm.patient_sex = row.patient_details.gender;
				this.appointmentForm.department = row.department;
				this.appointmentForm.service_unit = row.service_unit;
        this.appointmentForm.notes = row.notes;
			}
      this.showSlots()
      this.appointmentForm.doctype = 'Patient Appointment';
      this.appointmentForm.appointment_date = this.appointmentForm.appointment_time = undefined;
			this.appointmentForm.type = formType
      this.appointmentForm.custom_is_walked_in = false;
			this.appointmentOpen = true
		},
    appointmentNoteDialog(row) {
      this.appointmentForm.name = row.appointment_id;
			this.appointmentNoteOpen = true;
		},
    vitalSignDialog(row) {
      this.selectedRow = row
			this.vitalSignsOpen = true;
		},
    transferPractitionerDialog(row) {
      this.appointmentForm.name = row.appointment_id;
      this.appointmentForm.practitioner = row.practitioner;
      this.appointmentForm.practitioner_name = row.practitioner_name;
			this.transferOpen = true
		},
    serviceUnitDialog(row) {
      this.appointmentForm.name = row.appointment_id;
      this.appointmentForm.service_unit = row.service_unit;
			this.serviceUnitOpen = true
		},
    paymentTypeDialog(row) {
      this.appointmentForm.name = row.appointment_id;
      this.appointmentForm.custom_payment_type = row.payment_type;
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
    onSubmitAppointmentNote() {
      this.lodingOverlay = true;
      this.$call('frappe.client.insert', 
        {doc: {
          doctype: 'Appointment Note Table', 
          parent: this.appointmentForm.name, 
          parentfield: 'custom_visit_notes', 
          parenttype: 'Patient Appointment', 
          provider: this.newNote.provider, 
          note: this.newNote.note, 
          time: dayjs().format('YYYY/MM/DD hh:mm:ss')
        }}
      ).then(response => {
        this.lodingOverlay = false;
        this.appointmentNoteOpen = false;
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