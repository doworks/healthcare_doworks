<template>
  <!-- Main Wrapper -->
  <div class="main-wrapper mr-3" id="nurse-dashboard" style="margin-right: -10px;">
    <v-alert
      v-if="alertActive && alertType === 'error'"
      type="error"
      position="fixed"
      location="top center"
      color="red-lighten-3"
      style="z-index: 3000; margin-top: 15px"
      closable
      @click:close="() => {
        alertActive = false
        alertType = ''
        alertMessage = ''
      }"
    >
      <div v-html="alertMessage"></div>
    </v-alert>
    <!-- Page Content -->
    <div class="flex flex-wrap gap-4 pb-4">
      <Card class="flex-1 border border-surface shadow-none">
        <template #content>
          <div class="flex justify-between gap-8">
            <div class="flex flex-col gap-1">
              <span class="text-surface-500 dark:text-surface-400 text-sm">Orders Completed</span>
              <!-- <span class="font-bold text-lg">{{ val.value }}%</span>
              <h6 >Today Appointments</h6> -->
              <div class="d-flex">
                <span class="text-green font-bold text-lg">{{$resources.services.data?.filter(value => value.status == 'Completed').length}}</span>
                <span class="font-bold text-lg">/{{$resources.services.data?.length}}</span>
              </div>
            </div>
            <span class="w-8 h-8 rounded-full inline-flex justify-center items-center text-center bg-blue">
              <i class="mdi mdi-account-voice"/>
            </span>
          </div>
        </template>
      </Card>
      <Card class="flex-1 border border-surface shadow-none">
        <template #content>
          <div class="flex justify-between gap-8">
            <div class="flex flex-col gap-1">
              <span class="text-surface-500 dark:text-surface-400 text-sm">Nursing Tasks Completed</span>
              <!-- <span class="font-bold text-lg">{{ val.value }}%</span>
              <h6 >Today Appointments</h6> -->
              <div class="d-flex">
                <span class="text-green font-bold text-lg">{{$resources.nursingTasks.data?.filter(value => value.status == 'Completed').length}}</span>
                <span class="font-bold text-lg">/{{$resources.nursingTasks.data?.length}}</span>
              </div>
            </div>
            <span class="w-8 h-8 rounded-full inline-flex justify-center items-center text-center bg-green">
              <i class="mdi mdi-order-bool-ascending-variant" />
            </span>
          </div>
        </template>
      </Card>
      <!-- <Card class="flex-1 border border-surface shadow-none">
        <template #content>
          <div class="flex justify-between gap-8">
            <div class="flex flex-col gap-1">
              <span class="text-surface-500 dark:text-surface-400 text-sm">Next Appointment</span>
              <div class="d-flex">
                <span class="text-red font-bold text-lg">{{nextAppointmentTime}}</span>
              </div>
            </div>
            <span class="w-8 h-8 rounded-full inline-flex justify-center items-center text-center bg-red">
              <i class="mdi mdi-timer-sand" />
            </span>
          </div>
        </template>
      </Card> -->
    </div>

    <!-- Appointment Tab -->
    <div class="mb-4">
      <v-tabs v-model="tab" align-tabs="center" color="indigo" bg-color="white" show-arrows>
        <v-tab v-for="(value, key) in groupedAppointments" :key="key" :value="key" @click="() => {
          if(this.groupedAppointments[key].length <= 0){
            this.fetchRecords();
          }
        }">
          {{ key }}
          <v-badge :color="totalCount[key] > 0 ? 'green' : 'indigo'" :content="totalCount[key]" inline></v-badge>
        </v-tab>
      </v-tabs>
      <v-window v-model="tab" disabled>
        <v-window-item v-for="(value, key) in groupedAppointments" :key="key" :value="key">
        <AppointmentTab 
        :appointments="value" 
        :tab="key.toLowerCase()"
        :loading="appointmentsLoading"
        ref="appointmentTabRef"
        @appointment-note-dialog="appointmentNoteDialog"
        @vital-sign-dialog="vitalSignDialog"
        @medical-history-dialog="medicalHistoryDialog"
        @table-page-change="pageChanged"
        @service-unit-dialog="serviceUnitDialog"
        @appointment-invoice-dialog="appointmentInvoiceDialog"
        @checklist-form-dialog="checklistFormDialog"
        />
        </v-window-item>
      </v-window>
    </div>
    <div class="row row-cols-lg-2 cont mb-3" style="overflow: hidden;">
      <Card class="col-12 col-lg-6 left-col p-0" id="services" style="overflow: hidden;">
        <template #title>
          Orders ({{ $resources.services.data?.length }})
        </template>
        <template #content>
          <DataTable :value="$resources.services.data">
            <template #empty><v-empty-state title="No Service Requests"></v-empty-state></template>
            <Column field="template_dn" header="Service Name"></Column>
            <Column field="order_date" header="Ordered On"></Column>
            <Column field="status" header="Status">
              <template #body="{ data }">
                {{ data.status?.split('-')[0] }}
              </template>
            </Column>
            <Column field="practitioner" header="Ordered By"></Column>
          </DataTable>
        </template>
      </Card>
      <Card class="col-12 col-lg-6 right-col p-0" id="nursing-tasks" style="overflow: hidden;">
        <template #title>
          Nursing Tasks ({{ $resources.nursingTasks.data?.length }})
        </template>
        <template #content>
          <DataTable :value="$resources.nursingTasks.data">
            <template #empty><v-empty-state title="No Nursing Tasks"></v-empty-state></template>
            <Column field="activity" header="Activity"></Column>
            <Column field="mandatory" header="Mandatory?"></Column>
            <Column field="patient_name" header="Patient Name"></Column>
            <Column field="service_unit" header="Room"></Column>
            <Column field="requested_start_time" header="Requested Start Time"></Column>
            <Column field="requested_end_time" header="Requested EnD Time"></Column>
            <Column field="duration" header="Duration"></Column>
            <Column field="status" header="Status"></Column>
          </DataTable>
        </template>
      </Card>
    </div>  
    <!-- /Page Content -->
    <vitalSignsListDialog 
    :isOpen="vitalSignsOpen" 
    :appointment="selectedRow"
    @update:isOpen="vitalSignsOpen = $event" 
    @show-alert="showAlert" 
    />
    <patientMedicalHistoryDialog 
    :isOpen="medicalHistoryActive" 
    @update:isOpen="medicalHistoryActive = $event" 
    @show-alert="showAlert" 
    :patient="patient"
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
    <checklistFormListDialog 
    :isOpen="checklistFormOpen" 
    :appointment="selectedRow"
    @update:isOpen="checklistFormOpen = $event" 
    @show-alert="showAlert" 
    />
    <v-dialog v-model="serviceUnitOpen" width="auto">
      <v-card
        rounded="lg"
        width="auto"
        prepend-icon="mdi mdi-door-open"
        title="Update Room"
      >
        <v-card-text>
          <LinkField 
					doctype="Healthcare Service Unit" 
					query="healthcare.controllers.queries.get_healthcare_service_units"
          :filters="{allow_appointments: 1}"
					:value="appointmentForm.service_unit" 
          :style="{minWidth: '400px', maxWidth: '600px'}"
					@change="(data) => { appointmentForm.service_unit = data }"
					/>
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
          
          text="Save"
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
          
          text="Save"
          variant="tonal"
          @click="onSubmitTransferPractitioner()"
          ></v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
  <!-- /Main Wrapper -->
</template>
<script>
import dayjs from 'dayjs';
import { ref } from 'vue';
import relativeTime from 'dayjs/plugin/relativeTime';
dayjs.extend(relativeTime);

import AppointmentTab from '../doctors/doctor-appointment-tab.vue'

import { VAvatar } from 'vuetify/components/VAvatar';
import { VChip } from 'vuetify/components/VChip';
import { VListItem } from 'vuetify/components/VList';
import { VEmptyState } from 'vuetify/labs/VEmptyState';
import { VProgressLinear } from 'vuetify/components/VProgressLinear';

import bellImage from '@/assets/img/animations/alarm.gif';
import maleImage from '@/assets/img/male.png';
import femaleImage from '@/assets/img/female.png';

export default {
  inject: ['$call', '$socket'],
  components: {
    AppointmentTab, VAvatar, VChip, VListItem, VEmptyState, VProgressLinear,
  },
  resources: {
    services() { return { 
      type: 'list', 
      doctype: 'Service Request', 
      fields: [
				'status', 'order_date', 'order_time', 'practitioner', 'practitioner_email', 'medical_department', 'referred_to_practitioner', 
				'source_doc', 'order_group', 'sequence', 'staff_role', 'patient_care_type', 'intent', 'priority', 'quantity', 'dosage_form', 
				'as_needed', 'dosage', 'occurrence_date', 'occurrence_time', 'healthcare_service_unit_type', 'order_description', 'name',
				'patient_instructions', 'template_dt', 'template_dn', 'sample_collection_required', 'qty_invoiced', 'billing_status'
			], 
      filters: {staff_role: 'Nursing User'},
      auto: true, 
      pageLength: 1000,
    }},
    nursingTasks() { return { 
      type: 'list', 
      doctype: 'Nursing Task', 
      fields:[
        'name', 'date', 'service_unit', 'medical_department', 'status', 'activity', 'mandatory', 'description', 'patient', 'patient_name',
        'age', 'gender', 'inpatient_record', 'inpatient_status', 'requested_start_time', 'requested_end_time', 'duration', 'task_start_time',
        'task_end_time', 'task_duration', 'reference_doctype', 'reference_name', 'task_doctype', 'task_document_name', 'notes'
      ], 
      filters:{'requested_start_time': ['<=', dayjs().format('YYYY-MM-DD')], 'requested_end_time': ['>=', dayjs().format('YYYY-MM-DD')]}, 
      auto: true, 
      pageLength: 1000,
      transform(data) {
        if(data.values.length == 0)

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
  },
  data() {
    return {
      bellImage:bellImage,
      maleImage:maleImage,
      femaleImage:femaleImage,
      groupedAppointments: {Scheduled:[], Arrived:[], Ready:[], 'In Room':[], Completed:[], 'No Show':[],},
      walkedInPatients:0,
      tab: 'Arrived',
      appointments: [],
      currentTime: dayjs(),
      nextPatientDetails: null,
      isFlipped: false,
      appointmentsLoading: false,
      vitalSignsOpen: false,
      medicalHistoryActive: false,
      appointmentNoteOpen: false,
      serviceUnitOpen: false,
      transferOpen: false,
      paymentTypeOpen: false,
      appointmentInvoiceOpen: false,
      checklistFormOpen: false,
      services: [],
      patientInsurance: {},
      appointmentForm: {},
      selectedRow: {name: '', patient_details: {id: ''}},
      patient: {
        custom_allergies_table: [],
        custom_infected_diseases: [],
        custom_family_history: [],
        custom_surgical_history_table: [],
        custom_medications: [],
        custom_habits__social: [],
        custom_risk_factors_table: [],
        custom_chronic_diseases: [],
        custom_genetic_conditions: [],
      },
      totalRecords: 0,
      start: 0,
      limit: {Scheduled: 20, Arrived: 20, Ready: 20, 'In Room': 20, Completed: 20, 'No Show': 20},
      totalCount: {Scheduled: 0, Arrived: 0, Ready: 0, 'In Room': 0, Completed: 0, 'No Show': 0},
      selectedDates: [dayjs()],

      alertMessage: '',
      alertType: '', // 'success' or 'error'
      alertActive: false,
    };
  },
  created() {
    this.$socket.on('patient_appointments_updated', updatedAppointment => {
      if (updatedAppointment) {
        const appointmentDate = dayjs(updatedAppointment.appointment_date);

        // Check if the updated appointment falls within the selected date range
        const isInDateRange = this.selectedDates.some(date => date.isSame(appointmentDate, 'day'));

        if (isInDateRange) {
          const dates = this.selectedDates.map(date => date.format('YYYY-MM-DD'))
          this.$call('healthcare_doworks.api.methods.get_tabs_count', {
            filters: {appointment_date: ['in', dates]}
          }).then(response => {
            this.totalCount = response
          })
          .catch(error => {
            this.showAlert(error.message, 'error')
            console.error('Error fetching records:', error);
          });

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
  computed: {
    updatedAppointments() {
      return this.appointments.filter(value => value.custom_visit_status !== 'Completed' && value.custom_visit_status !== 'No Show').map(appointment => {
        const arrivalTime = dayjs(appointment.arriveTime);
        const diffInSeconds = this.currentTime.diff(arrivalTime, 'second');
        const hours = Math.floor(diffInSeconds / 3600);
        const minutes = Math.floor((diffInSeconds % 3600) / 60);
        const seconds = diffInSeconds % 60;
        if(appointment.arriveTime)
          return {
            ...appointment,
            timeSinceArrived: `${hours}h ${minutes}m ${seconds}s`
          };
        return appointment
      });
    },
    nextAppointmentTime() {
      if(this.appointments[0]){
        const firstValidAppointment = this.appointments
        .filter(appointment => appointment.custom_visit_status !== 'Completed' && appointment.custom_visit_status !== 'No Show')
        .sort((a, b) => dayjs(a.appointment_date + ' ' + a.appointment_time) - dayjs(b.appointment_date + ' ' + b.appointment_time))[0];
        const nextappointment = dayjs(firstValidAppointment.appointment_date + ' ' + firstValidAppointment.appointment_time);
        return dayjs(this.currentTime).to(nextappointment)
      }
      return ''
    },
  },
  mounted() {
    this.selectedDates = ref([dayjs()]),
    this.selectedRangeDates = [dayjs().startOf('isoWeek').subtract(1, 'day'), dayjs().endOf('isoWeek').subtract(1, 'day')],
    this.fetchRecords();
    
    setInterval(() => {
      this.currentTime = dayjs();
    }, 1000); // Update every second
    this.adjustContainerHeight();
  },
  methods: {
    getPercentage: (num1, num2) => {
      return num1 / num2 * 100
    },
    showAlert(message, type) {
      this.alertMessage = message;
      this.alertType = type;
      this.alertActive = true;
    },
    fetchRecords() {
      this.appointmentsLoading = true;
      const dates = this.selectedDates.map(date => date.format('YYYY-MM-DD'))
      this.$call('healthcare_doworks.api.methods.fetch_patient_appointments', {
        filters: {appointment_date: ['in', dates], custom_visit_status: this.tab}, start: this.start, limit: this.limit[this.tab]
      })
      .then(response => {
        if(response.total_count)
          this.totalCount = response.total_count

        const combinedAppointments = [...this.appointments, ...this.adjustAppointments(response.appointments)].reduce((acc, obj) => {
          acc.set(obj.name, obj);
          return acc;
        }, new Map());

        this.appointments = Array.from(combinedAppointments.values());
        // this.appointments = this.adjustAppointments(response.appointments)
        this.groupAppointmentsByStatus();
        this.appointmentsLoading = false;
      })
      .catch(error => {
        this.appointmentsLoading = false;
        this.showAlert(error.message, 'error')
        console.error('Error fetching records:', error);
      });
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
    appointmentNoteDialog(row) {
      this.selectedRow = row
			this.appointmentNoteOpen = true;
		},
    vitalSignDialog(row) {
      this.selectedRow = row
      this.vitalSignsOpen = true;
    },
    appointmentInvoiceDialog(row) {
      this.selectedRow = row
			this.appointmentInvoiceOpen = true;
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
    checklistFormDialog(row) {
      this.selectedRow = row
      this.checklistFormOpen = true;
    },
    paymentTypeDialog(row) {
      this.appointmentForm.name = row.name;
      this.appointmentForm.custom_payment_type = row.custom_payment_type;
      this.$call('frappe.client.get', {doctype: 'Patient', name: row.patient}).then((data) => {
        this.patientInsurance.doctype = 'Patient'
        this.patientInsurance.name = row.patient
        this.patientInsurance.custom_active = data.custom_active
        this.patientInsurance.custom_insurance_company_name = data.custom_insurance_company_name
        this.patientInsurance.custom_policy_number = data.custom_policy_number
        if(data.custom_expiration_date)
          this.patientInsurance.custom_expiration_date = dayjs(data.custom_expiration_date)
        else
          this.patientInsurance.custom_expiration_date = undefined
        this.patientInsurance.custom_copay_amount = data.custom_copay_amount
        this.paymentTypeOpen = true
      }).catch(error => {
        this.showAlert(error.message, 'error')
      });
    },
    onSubmitTransferPractitioner() {
      this.lodingOverlay = true;
      this.$call('healthcare_doworks.api.methods.transferToPractitioner', 
        {app: this.appointmentForm.name, practitioner: this.appointmentForm.practitioner}
      ).then(response => {
        this.$toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Appointment transformed',
          life: 3000 // Duration in ms
        });
        this.lodingOverlay = false;
        this.transferOpen = false;
      }).catch(error => {
        this.showAlert(error.message, 'error')
      });
    },
    onSubmitServiceUnit() {
      this.lodingOverlay = true;
      this.$call('frappe.client.set_value', 
        {doctype: 'Patient Appointment', name: this.appointmentForm.name, fieldname: 'service_unit', value: this.appointmentForm.service_unit}
      ).then(response => {
        this.$toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Appointment room changed',
          life: 3000 // Duration in ms
        });
        this.lodingOverlay = false;
        this.serviceUnitOpen = false;
      }).catch(error => {
        this.showAlert(error.message, 'error')
      });
    },
    onSubmitPaymentType() {
      this.lodingOverlay = true;
      if(this.appointmentForm.custom_payment_type == 'Insurance'){
        let form = {...this.patientInsurance, custom_default_payment_type: this.appointmentForm.custom_payment_type}
        form.custom_expiration_date = form.custom_expiration_date.format('YYYY-MM-DD')
        this.$call('healthcare_doworks.api.methods.edit_doc', {form}).then(response => {
          this.$toast.add({
            severity: 'success',
            summary: 'Success',
            detail: 'Patient insurance details saved',
            life: 3000 // Duration in ms
          });
          this.lodingOverlay = false;
          this.paymentTypeOpen = false;
        }).catch(error => {
          this.showAlert(error.message, 'error')
        });
      }

      this.$call('frappe.client.set_value', 
        {doctype: 'Patient Appointment', name: this.appointmentForm.name, fieldname: 'custom_payment_type', value: this.appointmentForm.custom_payment_type}
      ).then(response => {
        this.$toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Appointment payment type saved',
          life: 3000 // Duration in ms
        });
        this.lodingOverlay = false;
        this.paymentTypeOpen = false;
      }).catch(error => {
        this.showAlert(error.message, 'error')
      });
    },
    medicalHistoryDialog(row) {
      this.$call('frappe.client.get', {doctype: 'Patient', name: row.patient_details.id})
      .then(response => {
        this.$toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Patient medical history updated',
          life: 3000 // Duration in ms
        });
        this.patient = response
        this.medicalHistoryActive = true;
      })
      .catch(error => {
        this.appointmentsLoading = false;
        this.showAlert(error.message, 'error')
        console.error('Error fetching records:', error);
      });
    },
    adjustAppointments(data) {
			return [...(data || [])].map((d) => {
        d.notes = this.stripHtml(d.notes)
        d.patient_details.age = this.calculateAge(d.patient_details.date_of_birth)

        d.visit_notes = d.visit_notes?.map(note => {
          note.dayDate = dayjs(note.time).format('DD/MM/YYYY')
          note.dayTime = dayjs(note.time).format('h:mm A')
          return note
        })
        d.arriveTime = '-'
        d.status_log?.forEach((value, index) => {
          value.timeFormat = dayjs(value.time).format('h:mm a    D/MM/YYYY')
        })

        const arvRow = d.status_log.filter(value => value.status == 'Arrived')
				if(arvRow.length > 0){
					d.arriveTime = dayjs(arvRow[0].time)
					const difference = dayjs(arvRow[0].time).diff(dayjs(d.appointment_date + ' ' + d.appointment_time), 'minute')
					let diffHours = parseInt(difference / 60)
					let diffMinutes = difference % 60
					if(difference < 5 && difference > -5){
						d.arrivalTime = 'on time'
					}
					if(difference < 0){
						diffHours *= -1
						diffMinutes *= -1
						d.arrivalTime = (diffHours ? (diffHours + 'h ') : '') + (diffMinutes + 'm') + ' early'
					}
					else{
						d.arrivalTime = (diffHours ? (diffHours + 'h ') : '') + (diffMinutes + 'm') + ' late'
					}
				}
				const readyRow = d.status_log.filter(value => value.status == 'Ready' || value.status == 'In Room')
				if(readyRow.length > 0){
					d.readyTime = dayjs(readyRow[0].time)
				}

        d.appointment_date_moment = dayjs(d.appointment_date + ' ' + d.appointment_time).format('D/MM/YYYY');
				d.appointment_time_moment = dayjs(d.appointment_date + ' ' + d.appointment_time).format('h:mm a');
				d.patient_cpr = d.patient_name + ' ' + d.patient_details?.cpr

				return d;
			});
		},
    onPatientDetails(row) {
      this.isFlipped = !this.isFlipped;
      setTimeout(() => {
        this.nextPatientDetails = row.data
      }, 200)
    },
    getBadgeNumber(tab){
      let count = 0
      if(this.groupedAppointments[tab]){
        count = this.groupedAppointments[tab].reduce((total, value) => {
          if(dayjs().format('YYYY-MM-DD') === value.appointment_date){
            return total + 1
          }
          return total
        },0)
      }
      return count
    },
    adjustContainerHeight(cardHeight) {
      if(cardHeight)
        this.$refs.containerRef.style.minHeight = cardHeight + 'px';
    },
    getSeverity(status) {
      switch (status) {
        case 'Scheduled':
          return 'success';

        case 'Rescheduled':
          return 'info';

        case 'Walked In':
          return 'warning';

        default:
          return 'danger';
      }
    },
    toggleOP(event) {
      this.$refs.op.toggle(event)
    },
    nextAppointmentTimeDiff() {
      dayjs()
    },
    pageChanged(event) {
      this.start = event.first;
      const maxed = [20, 100, 500, 2500].some(val => this.groupedAppointments[this.tab].length == val)
      if(event.rows > this.limit[this.tab] && event.rows >= this.groupedAppointments[this.tab].length && maxed){
        this.limit[this.tab] = event.rows;
        this.fetchRecords();
      }
      else
        this.limit[this.tab] = event.rows;
    },
    updateProgress() {
      this.progressValue = (this.appointments.length / this.totalRecords) * 100;
    },
    stripHtml(html) {
      const tempDiv = document.createElement('div');
      tempDiv.innerHTML = html;
      return tempDiv.textContent || tempDiv.innerText || "";
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
  name: "nurse-dashboard",
};
</script>

<style scoped>
.details-card {
  background-color: rgba(228, 228, 228, 0.541);
  border-radius: 12px;
}

.flip-card-inner {
  position: relative;
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
  transform-origin: center right;
  transition: transform 0.8s;
}
.isFlipped {
  transform: translateX(-100%) rotateY(-180deg);
}

.flip-card-front, .flip-card-back {
  
  position: absolute;
  width: 100%;
  height: 100%;
  -webkit-backface-visibility: hidden; /* Safari */
  backface-visibility: hidden;
}
.flip-card-back {
  transform: rotateY(180deg);
}

.row-cols-lg-2{
  justify-content: center;
}
.row-cols-lg-2 > .col-lg-6 {
  flex: 0 0 calc(100% - 25px); /* Adjust the width of the columns and the horizontal gap size as needed */
}

@media (min-width: 992px) {
  .details-card {
    background-color: rgba(228, 228, 228, 0.541);
    border-radius: 12px;
    height: 475px;
  }
  .cont {
    display: flex;
    flex-wrap: wrap;
    margin: 0px
  }
  .row-cols-lg-2 {
    justify-content: start;
  }
  .row-cols-lg-2 > .col-lg-6 {
    flex: 0 0 calc(50% - 20px); /* Adjust the width of the columns and the horizontal gap size as needed */
  }
  .row-cols-lg-2 > .left-col {
    margin-right: 8px; /* Half of the horizontal gap size */
  }
  .row-cols-lg-2 > .right-col {
    margin-left: 8px; /* Half of the horizontal gap size */
  }
}
</style>