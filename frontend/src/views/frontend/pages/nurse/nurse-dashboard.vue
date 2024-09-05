<template>
  <!-- Main Wrapper -->
  <div class="main-wrapper mr-3" id="doctor-dashboard" style="margin-right: -10px;">
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
    <div class="flex flex-wrap gap-4 pb-4">
      <Card class="flex-1 border border-surface shadow-none">
        <template #content>
          <div class="flex justify-between gap-8">
            <div class="flex flex-col gap-1">
              <span class="text-surface-500 dark:text-surface-400 text-sm">Today Appointments</span>
              <!-- <span class="font-bold text-lg">{{ val.value }}%</span>
              <h6 >Today Appointments</h6> -->
              <div class="d-flex">
                <span class="text-info font-bold text-lg">{{appointments.length - updatedAppointments.length}}</span>
                <span class="font-bold text-lg">/{{appointments.length}}</span>
              </div>
            </div>
            <span class="w-8 h-8 rounded-full inline-flex justify-center items-center text-center bg-blue">
              <i class="mdi mdi-calendar-account" />
            </span>
          </div>
        </template>
      </Card>
      <Card class="flex-1 border border-surface shadow-none">
        <template #content>
          <div class="flex justify-between gap-8">
            <div class="flex flex-col gap-1">
              <span class="text-surface-500 dark:text-surface-400 text-sm">Orders Completed</span>
              <!-- <span class="font-bold text-lg">{{ val.value }}%</span>
              <h6 >Today Appointments</h6> -->
              <div class="d-flex">
                <span class="text-green font-bold text-lg">{{services.filter(value => value.status == 'Completed').length}}</span>
                <span class="font-bold text-lg">/{{services.length}}</span>
              </div>
            </div>
            <span class="w-8 h-8 rounded-full inline-flex justify-center items-center text-center bg-green">
              <i class="mdi mdi-walk" />
            </span>
          </div>
        </template>
      </Card>
      <Card class="flex-1 border border-surface shadow-none">
        <template #content>
          <div class="flex justify-between gap-8">
            <div class="flex flex-col gap-1">
              <span class="text-surface-500 dark:text-surface-400 text-sm">Next Appointment</span>
              <!-- <span class="font-bold text-lg">{{ val.value }}%</span>
              <h6 >Today Appointments</h6> -->
              <div class="d-flex">
                <span class="text-red font-bold text-lg">{{nextAppointmentTime}}</span>
              </div>
            </div>
            <span class="w-8 h-8 rounded-full inline-flex justify-center items-center text-center bg-red">
              <i class="mdi mdi-timer-sand" />
            </span>
          </div>
        </template>
      </Card>
    </div>

    <!-- Appointment Tab -->
    <div class="mb-4">
      <v-tabs v-model="tab" class="" align-tabs="center" color="indigo" bg-color="white" show-arrows>
        <v-tab v-for="(value, key) in groupedAppointments" :key="key" :value="key">
          {{ key }}
          <v-badge color="indigo" :content="getBadgeNumber(key)" inline></v-badge>
        </v-tab>
      </v-tabs>
      <div v-if="appointmentsLoading">
        <v-progress-linear :value="(appointments.length / totalRecords) * 100" height="4"></v-progress-linear>
      </div>
      <v-window v-model="tab" disabled>
        <v-window-item v-for="(value, key) in groupedAppointments" :key="key" :value="key">
        <AppointmentTab 
        :appointments="value" 
        :tab="key.toLowerCase()"
        ref="appointmentTabRef"
        @appointment-note-dialog="appointmentNoteDialog"
        @vital-sign-dialog="vitalSignDialog"
        @medical-history-dialog="medicalHistoryDialog"
        />
        </v-window-item>
      </v-window>
    </div>
    <div class="row row-cols-lg-2 cont mb-3" style="overflow: hidden;">
      <Card class="col-12 col-lg-6 left-col p-0" id="services" style="overflow: hidden;">
        <template #title>
          Orders ({{ services && services.length }})
        </template>
        <template #content>
          <DataTable :value="services">
            <template #empty><v-empty-state title="No Service Requests"></v-empty-state></template>
            <Column field="template_dn" header="Service Name"></Column>
            <Column field="order_date" header="Ordered On"></Column>
            <Column field="status" header="Status">
              <template #body="{ data }">
                {{ data.status.split('-')[0] }}
              </template>
            </Column>
            <Column field="practitioner" header="Ordered By"></Column>
          </DataTable>
        </template>
      </Card>
    </div>  
    <!-- /Page Content -->
    <vitalSignsListDialog 
    :isOpen="vitalSignsOpen" 
    :appointment="{'name': selectedRow.name, 'patient': selectedRow.patient}"
    @update:isOpen="vitalSignsOpen = $event" 
    @show-alert="showAlert" 
    />
    <patientMedicalHistoryDialog 
    :isOpen="medicalHistoryActive" 
    @update:isOpen="medicalHistoryActive = $event" 
    @show-alert="showAlert" 
    :patient="patient"
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
  </div>
  <!-- /Main Wrapper -->
</template>
<script>
import dayjs from 'dayjs';
import relativeTime from 'dayjs/plugin/relativeTime';
dayjs.extend(relativeTime);

import AppointmentTab from './nurse-appointment-tab.vue'
import patientDetailsCard from '../doctors/patient-details-card.vue'

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
    AppointmentTab, patientDetailsCard, VAvatar, VChip, VListItem, VEmptyState, VProgressLinear,
  },
  resources: {
    services() { return { 
      type: 'list', 
      doctype: 'Service Request', 
      fields: [
				'status', 'order_date', 'order_time', 'practitioner', 'practitioner_email', 'medical_department', 'referred_to_practitioner', 
				'source_doc', 'order_group', 'sequence', 'staff_role', 'patient_care_type', 'intent', 'priority', 'quantity', 'dosage_form', 
				'as_needed', 'dosage', 'occurrence_date', 'occurrence_time', 'healthcare_service_unit_type', 'order_description', 
				'patient_instructions', 'template_dt', 'template_dn', 'sample_collection_required', 'qty_invoiced', 'billing_status'
			], 
      filters: {staff_role: 'Nursing User'},
      auto: true, 
      pageLength: undefined,
      transform(data) {
        this.services = data
        return data
      },
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
      alertVisible: false,
      services: [],
      newNote: {},
      selectedRow: {patient: ''},
      patient: {
        custom_allergies_table: [],
        custom_infected_diseases: [],
        custom_surgical_history_table: [],
        custom_medications: [],
        custom_habits__social: [],
        custom_risk_factors_table: [],
        custom_chronic_diseases: [],
        custom_genetic_conditions: [],
      },
      totalRecords: 0,
      selectedDates: [dayjs()],
    };
  },
  created() {
    this.$socket.on('patient_appointments_chunk', (chunk) => {
      this.appointmentsLoading = true;
      this.appointments = [...this.appointments, ...this.adjustAppointments(chunk.data)];
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
    this.$socket.on('service_request', response => {
      if(response){
        this.services = this.adjustAppointments(response)
      }
    })
  },
  computed: {
    updatedAppointments() {
      return this.appointments.filter(value => value.visit_status !== 'Completed' && value.visit_status !== 'No Show').map(appointment => {
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
        .filter(appointment => appointment.visit_status !== 'Completed' && appointment.visit_status !== 'No Show')
        .sort((a, b) => dayjs(a.appointment_date + ' ' + a.appointment_time) - dayjs(b.appointment_date + ' ' + b.appointment_time))[0];
        const nextappointment = dayjs(firstValidAppointment.appointment_date + ' ' + firstValidAppointment.appointment_time);
        return dayjs(this.currentTime).to(nextappointment)
      }
      return ''
    },
  },
  mounted() {
    if (this.$socket.connected) {
      this.fetchRecords();  // Fetch appointments if socket is already connected
    } else {
      this.$socket.on('connect', () => {
        this.fetchRecords();  // Fetch records when the socket connects
      });
    }
    
    setInterval(() => {
      this.currentTime = dayjs();
    }, 1000); // Update every second
    this.adjustContainerHeight();
  },
  methods: {
    getPercentage: (num1, num2) => {
      return num1 / num2 * 100
    },
    showAlert(message, duration) {
      this.message = message;
      this.alertVisible = true;
      setTimeout(() => {
        this.alertVisible = false;
      }, duration);
    },
    fetchRecords() {
      this.appointments = []
      this.$call('healthcare_doworks.api.methods.fetch_patient_appointments', {
        filters: {appointment_date: ['in', [dayjs().format('YYYY-MM-DD')]]},
        total_records: true  // Only get the total count once
      })
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
      this.appointmentForm.name = row.appointment_id;
			this.appointmentNoteOpen = true;
		},
    vitalSignDialog(row) {
      this.selectedRow = row
      this.vitalSignsOpen = true;
    },
    medicalHistoryDialog(row) {
      this.$call('frappe.client.get', {doctype: 'Patient', name: row.patient_details.id})
      .then(response => {
        this.patient = response
        this.medicalHistoryActive = true;
      })
      .catch(error => {
        this.appointmentsLoading = false;
        console.error('Error fetching records:', error);
      });
    },
    adjustAppointments(data) {
      return [...(data || [])].filter(value => {
        const practitioner = value.practitioner === this.$myresources.user.practitioner;
        const date = dayjs().isSame(dayjs(value.appointment_date), 'day')
        return date
      }).map((d) => {

        d.visit_notes = d.visit_notes.map(note => {
          note.creation = dayjs(note.creation).format('h:mm A DD/MM/YYYY')
          return note
        })
        
        d.arriveTime = '-'
        d.status_log.forEach(value => {
          if(value.status == 'Arrived')
          d.arriveTime = dayjs(value.time)
        })

        d.appointment_time_moment = dayjs(d.appointment_date + ' ' + d.appointment_time).format('h:mm a');
        d.patient_cpr = d.patient_name + ' ' + d.patient_details.cpr
        return d;

      });
    },
    onSubmitAppointmentNote() {
      this.$call('frappe.client.insert', 
        {doc: {
          doctype: 'Appointment Note Table', 
          parent: this.appointmentForm.name, 
          parentfield: 'custom_visit_notes', 
          parenttype: 'Patient Appointment', 
          to: this.newNote.to, 
          full_name: this.newNote.full_name,
          note: this.newNote.note, 
          read: 0, 
        }}
      ).then(response => {
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
    updateProgress() {
      this.progressValue = (this.appointments.length / this.totalRecords) * 100;
    },
  },
  name: "doctor-dashboard",
};
</script>

<style>
#doctor-dashboard .p-paginator-bottom{
  display: none;
}
</style>
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