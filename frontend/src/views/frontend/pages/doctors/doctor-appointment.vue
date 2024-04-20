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
    <div class="row">
      <div class="col-md-12">
        <div class="appointment-tab">
          <!-- Clock And Other Filters -->
          <div class="flex-wrap flex-column flex-xxl-row gap-3 nav nav-tabs nav-tabs-solid pb-2">
            <div class="d-flex flex-wrap flex-column flex-lg-row gap-3 flex-auto order-2 order-xxl-1">
              <div class="flex-auto" style="width: 15rem">
                <Calendar
                  class="w-100"
                  style="height: 40px;"
                  v-model="selectedDate"
                  showIcon
                  iconDisplay="input"
                  inputId="date"
                  :manualInput="false"
                  :inputStyle="{cursor: 'pointer'}"
                  dateFormat="d/m/yy"
                  inputClass="text-center"
                  @date-select="onDateClick"
                />
                <span class="d-flex justify-content-center fw-bolder text-dark">{{ formattedDayOfWeek }}</span>
              </div>
              <div class="flex-auto" style="width: 15rem">
                <a-select
                  v-model:value="selectedDepartments"
                  mode="multiple"
                  style="width: 100%; align-items: center; max-height: 62px;"
                  placeholder="Departments"
                  max-tag-count="responsive"
                  :options="$resources.departments"
                  :fieldNames="{label:'department', value: 'department'}"
                  size="large"
                >
                </a-select>
              </div>
              <div class="flex-auto" style="width: 15rem">
                <a-input v-model:value="searchValue" placeholder="Search" size="large">
                  <template #prefix>
                    <v-icon icon="mdi mdi-magnify" color="grey"></v-icon>
                  </template>
                </a-input>
              </div>
            </div>
            <div class="ms-xxl-auto order-1 order-xxl-2" style="width: fit-content">
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
                <appointmenttab 
                  :searchValue="searchValue" 
                  :selectedDepartments="selectedDepartments" 
                  :appointments="value" 
                  :tab="key.toLowerCase()"
                  :loading="appointmentsLoading"
                  ref="appointmentTabRef"
                  @appointment-dialog="appointmentDialog"
                  @service-unit-dialog="serviceUnitDialog"
                  @payment-type-dialog="paymentTypeDialog"
                />
              </v-window-item>
            </v-window>
          </div>
          <!-- /Appointment Tab -->

        </div>
      </div>
    </div>
    <!-- /Page Content -->

    <!-- Page Dialogs -->
    <v-dialog v-model="appointmentOpen" width="auto" scrollable>
			<template v-slot:default="{ isActive }">
				<v-card rounded="lg">
          <a-form layout="vertical" :model="appointmentForm" :rules="rulesRef">
            <v-card-title class="d-flex justify-space-between align-center">
              <div class="text-h5 text-medium-emphasis ps-2">{{ appointmentForm.type }}</div>
              <v-btn icon="mdi mdi-close" variant="text" @click="isActive.value = false"></v-btn>
            </v-card-title>
            <v-divider class="m-0"></v-divider>
            <v-card-text>
              <v-container>
                <v-row>
                  <v-col cols="12" md="6">
                    <a-form-item label="Appointment Type" name="appointment_type">
                      <a-select
                        v-model:value="appointmentForm.appointment_type"
                        :options="$resources.appointmentTypes"
                        @change="(value, option) => {
                          appointmentForm.appointment_for = option.allow_booking_for;
                          appointmentForm.duration = option.default_duration
                        }"
                        :fieldNames="{label: 'appointment_type', value: 'appointment_type'}"
                      ></a-select>
                    </a-form-item>
                    <a-form-item label="Appointment Category">
                      <a-select
                        v-model:value="appointmentForm.custom_appointment_category"
                        :options="[{label: 'Primary', value: 'Primary'}, {label: 'Follow-up', value: 'Follow-up'}, {label: 'Session', value: 'Session'}]"
                      ></a-select>
                    </a-form-item>
                    <a-form-item label="Patient" name="patient">
                      <a-select
                      v-model:value="appointmentForm.patient_name"
                      :options="$resources.patients"
                      :fieldNames="{label: 'patient_name', value: 'patient_name'}"
                      @change="(value, option) => {appointmentForm.patient = option.name; appointmentForm.patient_sex = option.sex;}"
                      show-search
                      ></a-select>
                    </a-form-item>
                    <a-form-item v-if="appointmentForm.appointment_type" label="Appointment Duration">
                      <a-input disabled v-model:value="appointmentForm.duration" />
                    </a-form-item>
                  </v-col>
                  <v-col cols="12" md="6">
                    <a-form-item label="Appointment For" v-if="appointmentForm.appointment_type">
                      <a-input v-model:value="appointmentForm.appointment_for" disabled/>
                    </a-form-item>
                    <a-form-item v-if="appointmentForm.appointment_for === 'Practitioner'" label="Practitioner" name="practitioner">
                      <a-select
                        v-model:value="appointmentForm.practitioner_name"
                        :options="$resources.practitioners"
                        :fieldNames="{label: 'practitioner_name', value: 'practitioner_name'}"
                        show-search
                        @change="(value, option) => {
                          appointmentForm.practitioner = option.name
                          showSlots()
                        }"
                      ></a-select>
                    </a-form-item>
                    <a-form-item v-if="appointmentForm.appointment_for === 'Department'" label="Department" name="department">
                      <a-select
                        v-model:value="appointmentForm.department"
                        :options="$resources.departments"
                        :fieldNames="{label: 'department', value: 'department'}"
                        show-search
                      ></a-select>
                    </a-form-item>
                    <a-form-item v-if="appointmentForm.appointment_for === 'Service Unit'" label="Service Unit" name="service_unit">
                      <a-select
                        v-model:value="appointmentForm.service_unit"
                        :options="$resources.name"
                        :fieldNames="{label: 'name', value: 'name'}"
                        show-search
                      ></a-select>
                    </a-form-item>
                    <a-form-item label="Patient Gender" v-if="appointmentForm.patient">
                      <a-input v-model:value="appointmentForm.patient_sex" disabled/>
                    </a-form-item>
                    <!-- <a-form-item label="Appointment Date Range">
                      <a-date-picker v-model:value="dateWeek" @change="(val)=>{console.log(val.week())}" :format="customWeekStartEndFormat" style="z-index: 3000" picker="week" />
                    </a-form-item> -->
                    <a-form-item label="Appointment Date" name="appointment_date">
                      <a-date-picker 
                        v-model:value="appointmentForm.appointment_date"
                        :disabled-date="disabledDate"
                        @change="showSlots()" 
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

                <v-row>
                  <!-- <v-tabs
                    v-model="appointmentForm.appointment_date"
                    align-tabs="center"
                    color="deep-purple-accent-4"
                  >
                    <v-infinite-scroll
                      ref="infinite"
                      height="500"
                      side="both"
                      direction="horizontal"
                      @load="load"
                    >
                      <div>
                        <template v-for="formDate in formDates" :key="formDate">
                          <v-tab :value="formDate">{{ formDate }}</v-tab>
                        </template>
                      </div>
                    </v-infinite-scroll>
                  </v-tabs> -->

                  <!-- <div class="text-center mb-0" v-html="slotsHtml"></div> -->

                  <div class="text-center mb-0" v-if="appointmentForm.appointment_date && appointmentForm.practitioner">
                    <div v-for="(slotInfo, index) in slots.slot_details" :key="index">
                      <div class="slot-info">
                        <span v-if="slots.fee_validity && slots.fee_validity != 'Disabled'" style="color:green">Patient has fee validity till <b>{{moment(slots.fee_validity.valid_till).format('DD-MM-YYYY')}}</b></span>
                        <span v-else-if="slots.fee_validity != 'Disabled'" style="color:red">Patient has no fee validity</span><br/>
                        <span><b>Practitioner Schedule:  </b> {{ slotInfo.slot_name }}
                          <i v-if="slotInfo.tele_conf && !slotInfo.allow_overlap" class="fa fa-video-camera fa-1x" aria-hidden="true"></i>
                        </span><br/>
                        <span><b> Service Unit:  </b> {{slotInfo.service_unit}}</span>
                        <br v-if="slotInfo.service_unit_capacity"/>
                        <span v-if="slotInfo.service_unit_capacity"> <b> Maximum Capacity: </b> {{slotInfo.service_unit_capacity}} </span>
                      </div>
                      <br/>
                      <v-item-group selected-class="bg-blue">
                        <v-item
                          v-for="(slot, idx) in slotInfo.avail_slot"
                          :key="idx"
                          v-slot="{ isSelected, selectedClass, toggle }"
                        >
                          <v-btn
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
                            @click="handleSlotClick(toggle, slot.from_time)"
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
              @click="isActive.value = false"
              ></v-btn>
              <v-btn
              class="text-none"
              color="blue"
              
              text="submit"
              variant="tonal"
              @click="onSubmitAppointment()"
              type="submit"
              ></v-btn>
            </v-card-actions>
          </a-form>
				</v-card>
			</template>
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
            :options="$resources.serviceUnits"
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
import { reactive, ref } from 'vue';
import { Form } from 'ant-design-vue';
import moment from "moment";
import dayjs from 'dayjs';
import Clock from '@/components/clock/Clock.vue';
import Calendar from 'primevue/calendar';

import {VBadge} from 'vuetify/components/VBadge';
import {VTab, VTabs} from 'vuetify/components/VTabs';
import {VWindow, VWindowItem} from 'vuetify/components/VWindow';
import {VIcon} from 'vuetify/components/VIcon';
import {VToolbar, VToolbarItems} from 'vuetify/components/VToolbar';
import {VBtn} from 'vuetify/components/VBtn';
import { VDialog } from 'vuetify/components/VDialog';
import { VCard, VCardTitle, VCardText, VCardActions } from 'vuetify/components/VCard';
import { VContainer, VCol, VRow } from 'vuetify/components/VGrid';
import { VDivider } from 'vuetify/components/VDivider';
import { VInfiniteScroll } from 'vuetify/components/VInfiniteScroll';
import { VAlert } from 'vuetify/components/VAlert';
import { VItemGroup, VItem } from 'vuetify/components/VItemGroup';
import { VOverlay } from 'vuetify/components/VOverlay';
import { VProgressCircular } from 'vuetify/components/VProgressCircular';

export default {
  inject: ['$socket', '$call'],
  components: {
    Clock, Calendar,VBadge, VTabs, VTab, VWindow, VWindowItem, VIcon, VToolbar, VToolbarItems, VBtn,
    VDialog, VCard, VCardTitle, VCardText, VCardActions, VDivider, VContainer, VCol, VRow, 
    VInfiniteScroll, VAlert, VItemGroup, VItem, VOverlay, VProgressCircular, 
  },
  data() {
    return {
      tab: null,
      appointments: [],
      groupedAppointments: {Scheduled:[], Arrived:[], Ready:[], 'In Room':[], Completed:[], 'No Show':[],},
      selectedDate: new Date(),
      searchValue: '',
      selectedDepartments: undefined,
      appointmentsLoading: true,
      appointmentOpen: false,
      serviceUnitOpen: false,
      paymentTypeOpen: false,
      lodingOverlay: false,
      slots: {},
      message: '',
      alertVisible: false,
      dateWeek: ref(dayjs()),
      virtualLength: 7,
    };
  },
  computed: {
    formattedDayOfWeek() {
      if (!this.selectedDate) return '';
      
      const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
      const selectedDay = new Date(this.selectedDate);
      const dayOfWeek = days[selectedDay.getDay()];

      return dayOfWeek;
    },
    formDates() {
      const firstDateOfWeek = dayjs().startOf('week');
      const formDates = Array.from({ length: 7 }, (k, v) => firstDateOfWeek.add(v, 'day'));
      return formDates
    },
    appointmentForm() {
      return reactive({
        doctype: 'Patient Appointment',
				name: '',
				appointment_type: '',
				appointment_for: '',
				duration: '',
				custom_appointment_category: 'Primary',
        custom_payment_type: '',
				practitioner: '',
        practitioner_name: '',
				department: '',
				service_unit: '',
				patient: '',
				patient_name: '',
				patient_sex: '',
        notes: '',
				appointment_date: undefined,
				appointment_time: undefined,
			});
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
  beforeUnmount() {
    // Clear the timeout before unmounting the component
    clearTimeout(this.timer);
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
          d.patient_details = JSON.parse(d.patient_details)
          d.visit_notes = JSON.parse(d.visit_notes)
          d.status_log = JSON.parse(d.status_log)
        } catch (error) {
          console.error('Error parsing JSON:', error);
        }

				d.appointment_time_moment = moment(d.appointment_date + ' ' + d.appointment_time).format('LT');
				d.patient_cpr = d.patient_name + ' ' + d.patient_details.cpr

				return d;
			});
		},
    getBadgeNumber(tab){
      if(this.groupedAppointments[tab])
        return this.groupedAppointments[tab].length
      return 0
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
				this.appointmentForm.name = 'new-patient-appointment';
				this.appointmentForm.duration = '';
				this.appointmentForm.appointment_type = '';
				this.appointmentForm.appointment_for = '';
				this.appointmentForm.custom_appointment_category = 'Primary';
        this.appointmentForm.custom_payment_type = '';
				this.appointmentForm.practitioner = '';
				this.appointmentForm.patient = '';
				this.appointmentForm.patient_name = '';
				this.appointmentForm.patient_sex = '';
				this.appointmentForm.department = '';
				this.appointmentForm.service_unit = '';
        this.appointmentForm.notes = '';
        this.slotsHtml = '';
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
        this.showSlots()
			}
      this.appointmentForm.appointment_date = this.appointmentForm.appointment_time = undefined;
			this.appointmentForm.type = formType
			this.appointmentOpen = true
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
    customWeekStartEndFormat: value => `${dayjs(value).startOf('week').format('MMMM D, YYYY')} -> ${dayjs(value).endOf('week').format('MMMM D, YYYY')}`,
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
            const message = error.message.split('frappe.exceptions.ValidationError: ')[1]
            this.showAlert(message , 10000)
          }
        }).catch(error => {
          const message = error.message.split('frappe.exceptions.ValidationError: ')[1]
          this.showAlert(message , 10000)
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
    onSubmitAppointment(){
      const { validate } = Form.useForm(this.appointmentForm, this.rulesRef);
      this.lodingOverlay = true;
      validate()
      .then(() => {
        if(this.appointmentForm.type === 'New Appointment'){
          delete this.appointmentForm['name'];
          this.$call('healthcare_doworks.api.methods.new_appointment', {form: this.appointmentForm})
          .then(response => {
            this.lodingOverlay = false;
            this.appointmentOpen = false;
          }).catch(error => {
            const message = error.message.split('frappe.exceptions.ValidationError: ')[1]
            this.showAlert(message , 10000)
          });
        }
        if(this.appointmentForm.type === 'Reschedule Appointment'){
          this.$call('healthcare_doworks.api.methods.reschedule_appointment', {form: this.appointmentForm})
          .then(response => {
            this.lodingOverlay = false;
            this.appointmentOpen = false;
          }).catch(error => {
            const message = error.message.split('frappe.exceptions.ValidationError: ')[1]
            this.showAlert(message , 10000)
          });
        }
      })
      .catch(err => {
        console.log('error', err);
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
        const message = error.message.split('frappe.exceptions.ValidationError: ')[1]
        this.showAlert(message , 10000)
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
        const message = error.message.split('frappe.exceptions.ValidationError: ')[1]
        this.showAlert(message , 10000)
      });
    },
    handleSlotClick(toggle, value){
      this.appointmentForm.appointment_time = value;
      toggle();
    },
    onDateClick(date) {
      console.log(date)
    },
    disabledDate(current) {
      // Can not select days before today and today
      return current && current < dayjs().endOf('day').subtract(1, 'day');
    },
    createRange (length, start) {
      return Array.from({ length }).map((_, i) => i + start)
    },
    load ({ side, done }) {
      const halfVirtualLength = this.virtualLength / 2
      if (side === 'start') {
        const arr = this.createRange(halfVirtualLength, this.cards[0] - halfVirtualLength)
        this.cards = [...arr, ...this.cards.slice(0, halfVirtualLength)]
        this.$nextTick(() => {
          this.$refs.infinite.$el.scrollTop = this.$refs.infinite.$el.scrollHeight - (halfVirtualLength * this.size) - this.$refs.infinite.$el.scrollTop
        })
      } else {
        const arr = this.createRange(halfVirtualLength, this.cards.at(-1) + 1)
        this.cards = [...this.cards.slice(halfVirtualLength), ...arr]
      }

      done('ok')
    },
  },
  name: 'Appointments',
};
</script>

<style>
.p-datepicker-trigger-icon{
  top:12.5px
}

</style>