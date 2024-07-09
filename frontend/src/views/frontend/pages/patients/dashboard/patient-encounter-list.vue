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
                  <a-date-picker
                    v-model:value="selectedDate"
                    format="D/M/YY"
                    style="width: 100%; align-items: center; max-height: 62px; text-align: center"
                    :allowClear="false"
                    size="large"
                  />
                  <span class="d-flex justify-content-center fw-bolder text-dark me-3">{{ formattedDayOfWeek() }}</span>
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
                    :selectedDate="selectedDate"
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
        </div>
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
      <vitalSignsDialog 
      :isOpen="vitalSignsOpen" 
      @update:isOpen="vitalSignsOpen = $event" 
      @show-alert="showAlert" 
      :appointment="appointmentForm"
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
            
            text="submit"
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
              :options="$resources.practitioners"
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
            
            text="submit"
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
  
  import {VIcon} from 'vuetify/components/VIcon';
  import {VToolbar, VToolbarItems} from 'vuetify/components/VToolbar';
  
  export default {
    inject: ['$socket', '$call'],
    components: {
      Clock, VIcon, VToolbar, VToolbarItems,
    },
    data() {
      return {
        tab: null,
        appointments: [],
        groupedAppointments: {Scheduled:[], Arrived:[], Ready:[], 'In Room':[], Completed:[], 'No Show':[],},
        selectedDate: ref(dayjs()),
        searchValue: '',
        selectedDepartments: undefined,
        appointmentsLoading: true,
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
        dateWeek: ref(dayjs()),
        appointmentForm: {},
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
            if(typeof d.patient_details === 'string'){
              d.patient_details = JSON.parse(d.patient_details)
              d.visit_notes = JSON.parse(d.visit_notes)
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
      getBadgeNumber(tab){
        let count = 0
        if(this.groupedAppointments[tab]){
          count = this.groupedAppointments[tab].reduce((total, value) => {
            let departmentFilter = true
            if(this.selectedDepartments)
              departmentFilter = this.selectedDepartments.some(department => {return department === value.department})
            if(this.selectedDate.format('YYYY-MM-DD') === value.appointment_date && departmentFilter){
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
          this.$resources.appointmentTypes.forEach(value => {
            if(value.appointment_type === 'Practitioner')
              duration = value.default_duration
          })
          this.appointmentForm.name = 'new-patient-appointment';
                  this.appointmentForm.duration = duration;
                  this.appointmentForm.appointment_type = 'Practitioner';
                  this.appointmentForm.appointment_for = 'Practitioner';
                  this.appointmentForm.custom_appointment_category = 'Primary';
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
              this.appointmentOpen = true
          },
      appointmentNoteDialog(row) {
        this.appointmentForm.name = row.appointment_id;
              this.appointmentNoteOpen = true;
          },
      vitalSignDialog(row) {
        this.appointmentForm.name = row.appointment_id;
        this.appointmentForm.patient = row.patient_details.id;
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
      createRange (length, start) {
        return Array.from({ length }).map((_, i) => i + start)
      },
      formattedDayOfWeek() {
        if (!this.selectedDate) return '';
        return dayjs(this.selectedDate).format('dddd');
      },
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