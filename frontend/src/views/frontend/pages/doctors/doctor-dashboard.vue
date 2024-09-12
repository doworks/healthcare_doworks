<template>
  <!-- Main Wrapper -->
  <div class="main-wrapper mr-3" id="doctor-dashboard" style="margin-right: -10px;">
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
              <span class="text-surface-500 dark:text-surface-400 text-sm">Walked-in Patients</span>
              <!-- <span class="font-bold text-lg">{{ val.value }}%</span>
              <h6 >Today Appointments</h6> -->
              <div class="d-flex">
                <span class="text-green font-bold text-lg">{{appointments.filter(val => val.status == 'Walked In').length}}</span>
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
    <div class="row row-cols-lg-2 cont mb-3">
      <Card class="left-col p-0" style="overflow: hidden;">
        <template #title>Upcoming Appintments</template>
        <template #content>
          <div class="table-responsive">
            <DataTable
            size="small"
            sortField="arriveTime"
            dataKey="id"
            :sortOrder="-1"
            paginator
            :rows="5"
            :value="updatedAppointments"
            selectionMode="single" 
            :metaKeySelection="true"
            @row-click="onPatientDetails"
            >
              <template #empty><v-empty-state title="No Appointments"></v-empty-state></template>
              <template #loading> Loading Appointments data. Please wait.</template>
              <Column header="Patient" field="patient">
                <template #body="{ data }">
                  <!-- <router-link to="patient-profile"> -->
                    <div class="d-flex align-items-center gap-2">
                      <v-avatar>
                        <img
                        class="h-100 w-100"
                        :src="data.patient_details.image ? data.patient_details.image :data.patient_details.gender === 'Male' ? maleImage :femaleImage"
                        />
                        <!-- <span v-if="!data.patient_details.image" class="text-h5">{{ getInitials(data.patient_name) }}</span> -->
                      </v-avatar>
                      <div style="padding: 10px 15px; vertical-align: middle; padding-right: 0;">
                        <h6 style="font-size: 16px; font-weight: 500; margin-bottom: 0">{{ data.patient_name }}</h6>
                        <span style="color: rgba(51, 52, 72, 0.5); font-size: 16px; font-weight: 500">{{ data.service_unit }}</span>
                      </div><br/>
                    </div>

                  <!-- </router-link> -->
                </template>
              </Column>
              <Column header="Apt Time" sortable field="appointment_time">
                <template #body="{ data }">
                  <Tag :value="data.appointment_time_moment" severity="info" style="width: 95px"></Tag>
                </template>
              </Column>
              <Column header="Arv Time" sortable field="arriveTime">
                <template #body="{ data }">
                  <Tag v-if="data.timeSinceArrived" :value="data.timeSinceArrived" severity="success" style="width: 95px"></Tag>
                </template>
              </Column>
              <Column header="Status" field="status_log">
                <template #body="{ data }">
                  <v-chip class="ma-2" label size="small" :color="getSeverity(visitStatus(data))">{{ visitStatus(data) }}</v-chip>
                </template>
              </Column>
              <Column style="width: 5%">
                <template #body="{ data }">
                  <div>
                    <v-btn 
                      v-if="data.notes || data.visit_notes.length > 0" 
                      size="small" 
                      variant="text" 
                      icon
                      @click="e => {
                        selectedRow = data
                        toggleOP(e)
                      }"
                    >
                      <v-badge 
                      color="success" :content="data.visit_notes.filter(val => !val.read).length + (data.notes && 1)" 
                      :offset-y="5" 
                      :offset-x="6"
                      >
                        <img :src="bellImage" width="40px" class="me-1"/>
                      </v-badge>
                    </v-btn>
                    <!-- <i v-else class="mdi mdi-bell-outline" style="font-size: 25px; padding-left: 6px;"></i> -->
                    <v-btn v-else
                    icon="mdi mdi-bell-plus-outline" 
                    variant="text" 
                    @click="$emit('appointment-note-dialog', data)"
                    >
                    </v-btn>
                  </div>
                </template>
              </Column>
            </DataTable>
            <OverlayPanel ref="op">
              <div class="flex flex-column gap-3 w-min-96">
                <div v-if="selectedRow.notes">
                  <span class="fw-semibold d-block mb-2">Appointment Notes</span>
                  <a-textarea v-model:value="selectedRow.notes" :rows="4"/>
                </div>
                <v-btn
                icon="mdi mdi-plus" 
                variant="text" 
                @click="$emit('appointment-note-dialog', selectedRow)"
                >
                </v-btn>
                <div v-if="selectedRow.visit_notes.length > 0">
                  <!-- <span class="fw-semibold d-block mb-2">Visit Notes</span>
                  <ul class="list-none p-0 m-0 flex flex-column">
                    <li v-for="(note, index) in selectedRow.visit_notes" :key="index" class="flex align-items-center gap-2 mb-3">
                      <div>
                        <a-textarea v-model:value="note" disabled/>
                        <span>{{ note.time }}</span>
                      </div>
                      <div class="flex align-items-center gap-2 text-color-secondary ms-auto text-sm">
                        <span>{{ note.provider }}</span>
                      </div>
                    </li>
                  </ul> -->
                  <DataTable 
                  :value="selectedRow.visit_notes" 
                  selectionMode="single" 
                  :metaKeySelection="true" 
                  dataKey="name" 
                  class="max-h-72 overflow-y-auto"
                  >
                    <template #header>
                      <div class="flex flex-wrap items-center justify-between gap-2">
                        <span class="text-xl font-bold">Visit Notes</span>
                      </div>
                    </template>
                    <Column>
                      <template #body="{ data }">
                        <div>
                          <v-btn v-if="data.read" size="small" variant="text" icon="mdi mdi-eye" @click="() => { data.read = 0 }">
                          </v-btn>
                          <v-btn v-else-if="!data.read" size="small" variant="text" icon="mdi mdi-eye-off" @click="() => { data.read = 1 }">
                          </v-btn>
                        </div>
                      </template>
                    </Column>
                    <Column header="Time" field="dayDate">
                      <template #body="{ data }">
                        <div>
                          {{ data.dayDate }}
                        </div>
                        <div>
                          {{ data.dayTime }}
                        </div>
                      </template>
                    </Column>
                    <Column header="From" field="from"></Column>
                    <Column header="To" field="full_name"></Column>
                    <Column header="Note" field="note"></Column>
                  </DataTable>
                </div>
              </div>
            </OverlayPanel>
          </div>
        </template>
        <template #footer>
          <div class="d-flex mt-auto">
            <Button label="See All" link href="/appointments" severity="warn"/>
            <!-- <a href="/appointments">See All</a> -->
          </div>
        </template>
      </Card>
      <div v-if="nextPatientDetails" class="col-12 col-lg-6 right-col p-0 details-card mt-4 mt-md-0" style="min-height: 550px; height: auto;" ref="containerRef">
        <div  class="flip-card-inner" :class="{ 'isFlipped': isFlipped }">
          <div class="flip-card-front">
            <patientDetailsCard :patient="nextPatientDetails" @cardRendered="adjustContainerHeight"/>
          </div>
          <div class="flip-card-back">
            <patientDetailsCard :patient="nextPatientDetails"/>
          </div>
        </div>
        <!-- <Card v-else class="h-100"></Card> -->
      </div>
      <!-- <Card class="col-12 col-lg-6 left-col p-0 mt-3" style="overflow: hidden;">
        <template #title>Waiting List</template>
        <template #content>
          <div class="table-responsive">
            <table style="table-layout: auto; min-width: 435px; border-collapse: collapse;" class="table mb-0 border-0">
              <tbody>
                <tr v-for="(appointment, index) in appointments" :key="index">
                  <td class="table-image appoint-doctor d-flex">
                    <img width="28" height="28" class="rounded-circle avatar-lg align-self-center" :src="appointment.image" alt=""/>
                    <div style="padding: 10px 15px; vertical-align: middle; padding-right: 0;">
                      <h6 style="font-size: 16px; font-weight: 500; margin-bottom: 0">{{ appointment.patient_name }}</h6>
                      <span style="color: rgba(51, 52, 72, 0.5); font-size: 16px; font-weight: 500">{{ appointment.appointment_type }}</span>
                    </div>
                  </td>
                  <td class="text-sm align-middle text-end" style="position: sticky; right: 0; z-index: 1;">
                    <Button icon="pi pi-eye" size="small" class="me-1" style="padding: 2.5px 5px; width: auto;" severity="info" aria-label="View" />
                    <Button icon="pi pi-check" size="small" class="me-1" style="padding: 2.5px 5px; width: auto;" aria-label="Accept" />
                    <Button icon="pi pi-times" size="small" severity="danger" style="padding: 2.5px 5px; width: auto;" aria-label="Cancel" />
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </template>
        <template #footer>
          <div class="d-flex mt-1">
            <a href="/appointments">See All</a>
          </div>
        </template>
      </Card> -->
    </div>
  </div>    
  <!-- /Page Content -->
  <!-- /Main Wrapper -->
</template>
<script>
import dayjs from 'dayjs';
import { ref } from 'vue'
import relativeTime from 'dayjs/plugin/relativeTime';
dayjs.extend(relativeTime);

import patientDetailsCard from './patient-details-card.vue'

import { VAvatar } from 'vuetify/components/VAvatar';
import { VChip } from 'vuetify/components/VChip';
import { VListItem } from 'vuetify/components/VList';
import { VEmptyState } from 'vuetify/labs/VEmptyState';

import bellImage from '@/assets/img/animations/alarm.gif';
import maleImage from '@/assets/img/male.png';
import femaleImage from '@/assets/img/female.png';

export default {
  inject: ['$call', '$socket'],
  components: {
    patientDetailsCard, VAvatar, VChip, VListItem, VEmptyState,
  },
  data() {
    return {
      bellImage:bellImage,
			maleImage:maleImage,
			femaleImage:femaleImage,
      walkedInPatients:0,
      appointments: ref([]),
      currentTime: dayjs(),
      nextPatientDetails: null,
      isFlipped: false,
      appointmentsLoading: false,
      totalRecords: 0,
      selectedDates: [dayjs()],
    };
  },
  created() {
    this.$socket.on('patient_appointments_chunk', (chunk) => {
      this.appointments = [...this.appointments, ...this.adjustAppointments(chunk.data)];
      if(chunk.total)
        this.totalRecords = chunk.total;
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
        }
      }
    })
    
    this.$socket.on('connect', () => {
      this.fetchRecords();  // Call fetchRecords only after the socket is connected
    });
  },
  computed: {
    updatedAppointments() {
      return this.appointments.filter(val => val.visit_status !== 'Completed' && val.visit_status !== 'No Show' && val.visit_status !== 'Cancelled')
      .map(appointment => {
        const arrivalTime = dayjs(appointment.arriveTime);
        const diffInSeconds = this.currentTime.diff(arrivalTime, 'second');
        const hours = Math.floor(diffInSeconds / 3600);
        const minutes = Math.floor((diffInSeconds % 3600) / 60);
        const seconds = diffInSeconds % 60;
        if(appointment.arriveTime)
          return {
            ...appointment,
            timeSinceArrived: `${hours}h ${minutes}m`
          };
          return appointment
        });
    },
    nextAppointmentTime() {
      if(this.appointments[0]){
        const firstValidAppointment = this.appointments
        .filter(appointment => appointment.visit_status == 'Scheduled' && appointment.visit_status == 'Arrived' && appointment.visit_status == 'Ready')
        .sort((a, b) => dayjs(a.appointment_date + ' ' + a.appointment_time) - dayjs(b.appointment_date + ' ' + b.appointment_time))[0];
        const nextappointment = dayjs(firstValidAppointment.appointment_date + ' ' + firstValidAppointment.appointment_time);
        // const diffInSeconds = this.currentTime.diff(nextappointment, 'second');
        // const hours = Math.floor(diffInSeconds / 3600);
        // const minutes = Math.floor((diffInSeconds % 3600) / 60);
        // const seconds = diffInSeconds % 60;
        // return `${hours}:${minutes}:${seconds}`
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
		}, 60000); // Update every second
    this.adjustContainerHeight();
  },
  methods: {
    getPercentage: (num1, num2) => {
      return num1 / num2 * 100
    },
    visitStatus(data) {
      if(data.status_log?.length > 0){
        return data.status_log.reduce((latest, current) => {return new Date(current.time) > new Date(latest.time) ? current : latest}).status;
      }
      return 'Scheduled'
    },
    fetchRecords() {
      this.appointments = []
      this.appointmentsLoading = true;
      this.$call('healthcare_doworks.api.methods.fetch_patient_appointments', {
        filters: {appointment_date: ['in', [dayjs().format('YYYY-MM-DD')]]},
        total_records: true  // Only get the total count once
      })
    },
    adjustAppointments(data) {
			return [...(data || [])].filter(value => {
        const practitioner = value.practitioner === this.$myresources.user.practitioner;
        const date = dayjs().isSame(dayjs(value.appointment_date), 'day')
        return date
      }).map((d) => {
        d.arriveTime = null

        d.visit_notes = d.visit_notes.map(note => {
          note.creation = dayjs(note.creation).format('h:mm A DD/MM/YYYY')
          return note
        })

        d.status_log.forEach(value => {
          if(value.status == 'Arrived')
          d.arriveTime = dayjs(value.time)
        })

				d.appointment_time_moment = dayjs(d.appointment_date + ' ' + d.appointment_time).format('h:mm a');

        return d;
			});
		},
    onPatientDetails(row) {
      this.isFlipped = !this.isFlipped;
      setTimeout(() => {
        this.nextPatientDetails = row.data
      }, 200)
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
  },
  name: "doctor-dashboard",
};
</script>

<style>
/* #doctor-dashboard .p-paginator-bottom{
  display: none;
} */
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