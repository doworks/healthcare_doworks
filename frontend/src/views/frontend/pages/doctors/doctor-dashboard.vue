<template>
  <!-- Main Wrapper -->
  <div class="main-wrapper" id="doctor-dashboard" style="margin-right: -10px;">
    <!-- Page Content -->
    <div class="row">
      <div class="row">
        <div class="col-md-12">
          <div class="card dash-card">
            <div class="card-body">
              <div class="row">
                <div class="col-md-12 col-lg-4">
                  <div class="dash-widget dct-border-rht">
                    <div class="circle-bar circle-bar1">
                      <div class="circle-graph1">
                        <v-progress-circular
                          class="col"
                          :model-value="getPercentage(appointments.length - updatedAppointments.length,appointments.length)"
                          :size="100"
                          :width="7"
                          color="blue"
                        >
                          <img
                            src="@/assets/img/icon-03.png"
                            class="img-fluid"
                            alt="Patient"
                          />
                        </v-progress-circular>
                      </div>
                    </div>
                    <div class="dash-widget-info">
                      <h6 >Today Appointments</h6>
                      <div class="d-flex">
                        <h4 class="text-info">{{appointments.length - updatedAppointments.length}}</h4>
                        <h3>/{{appointments.length}}</h3>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="col-md-12 col-lg-4">
                  <div class="dash-widget dct-border-rht">
                    <div class="circle-bar circle-bar2">
                      <div class="circle-graph2">
                        <v-progress-circular
                          class="col"
                          :model-value="100"
                          :size="100"
                          :width="7"
                          color="green"
                        >
                          <img
                            src="@/assets/img/icon-01.png"
                            class="img-fluid"
                            alt="Patient"
                          />
                        </v-progress-circular>
                      </div>
                    </div>
                    <div class="dash-widget-info">
                      <h6>Walked In Patients</h6>
                      <h3>{{walkedInPatients}}</h3>
                    </div>
                  </div>
                </div>

                <div class="col-md-12 col-lg-4">
                  <div class="dash-widget">
                    <div class="circle-bar circle-bar3">
                      <div class="circle-graph3">
                        <v-progress-circular
                          class="col"
                          :model-value="100"
                          :size="100"
                          :width="7"
                          color="red"
                        >
                          <img
                            src="@/assets/img/icon-04.png"
                            class="img-fluid"
                            alt="Patient"
                            style="width: 36px; height: 36px;"
                          />
                        </v-progress-circular>
                      </div>
                    </div>
                    <div class="dash-widget-info">
                      <h6>Next Appointment</h6>
                      <h3>{{ nextAppointmentTime }}</h3>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="row row-cols-lg-2 cont mb-3">
        <Card class="col-12 col-lg-6 left-col p-0" style="overflow: hidden;">
          <template #title>Upcoming Appintments</template>
          <template #content>
            <div class="table-responsive">
              <DataTable
              size="small"
              sortField="arriveTime"
              dataKey="id"
              :loading="appointmentsLoading"
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
                            :src="data.patient_details.image ? 
                              data.patient_details.image :
                              data.patient_details.gender === 'Male' ? maleImage : femaleImage"
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
                    <Tag :value="data.appointment_time_moment" severity="info" style="width: 95px" class="absolute"></Tag>
                  </template>
                </Column>
                <Column header="Arv Time" sortable field="arriveTime">
                  <template #body="{ data }">
                    <Tag v-if="data.timeSinceArrived" :value="data.timeSinceArrived" severity="success" style="width: 95px" class="absolute"></Tag>
                  </template>
                </Column>
                <Column header="Status" field="status_log">
                  <template #body="{ data }">
                    <v-chip class="ma-2" label size="small" :color="getSeverity(visitStatus(data))">{{ visitStatus(data) }}</v-chip>
                  </template>
                </Column>
                <Column style="width: 5%">
                  <template #body="{ data }">
                    <v-btn 
                      v-if="data.notes || (data.visit_notes.length > 0 && data.visit_notes[0]?.note)" 
                      size="small" 
                      variant="text" 
                      icon
                      @click="toggleOP"
                    >
                      <v-badge color="success" :content="data.visit_notes.length + (data.notes && 1)" :offset-y="5" :offset-x="6">
                        <img :src="bellImage"/>
                      </v-badge>
                    </v-btn>
                    <i v-else class="mdi mdi-bell-outline" style="font-size: 25px; padding-left: 6px;"></i>
                    <OverlayPanel ref="op">
                      <div class="d-flex flex-column gap-3 w-25rem">
                        <div v-if="data.notes">
                          <span class="fw-semibold d-block mb-2">Appointment Notes</span>
                          <a-textarea v-model:value="data.notes" disabled/>
                        </div>
                        <div v-if="data.visit_notes.length > 0 && data.visit_notes[0]?.note">
                          <span class="fw-semibold d-block mb-2">Visit Notes</span>
                          <ul class="list-none p-0 m-0 flex flex-column">
                            <li v-for="(note, index) in data.visit_notes" :key="index" class="d-flex align-items-center gap-2 mb-3">
                              <div>
                                <a-textarea v-model:value="note.note" disabled/>
                                <span>{{ note.time }}</span>
                              </div>
                              <div class="d-flex align-items-center gap-2 text-color-secondary ms-auto text-sm">
                                <span>{{ note.provider }}</span>
                              </div>
                            </li>
                          </ul>
                        </div>
                      </div>
                    </OverlayPanel>
                  </template>
                </Column>
              </DataTable>
            </div>
          </template>
          <template #footer>
            <div class="d-flex mt-1">
              <a href="/appointments">See All</a>
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
  </div>
  <!-- /Main Wrapper -->
</template>
<script>
import dayjs from 'dayjs';
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
      appointments: [],
      currentTime: dayjs(),
      nextPatientDetails: null,
      isFlipped: false,
      appointmentsLoading: false,
    };
  },
  created() {
    this.fetchRecords();
    this.$socket.on('patient_appointments', response => {
      if(response){
        this.appointments = this.adjustAppointments(response)
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
    setInterval(() => {
			this.currentTime = dayjs();
		}, 1000); // Update every second
    this.adjustContainerHeight();
  },
  methods: {
    getPercentage: (num1, num2) => {
      return num1 / num2 * 100
    },
    visitStatus(data) {
      if(data.status_log.length > 0 && data.status_log[data.status_log.length -1].status){
        return data.status_log.reduce((latest, current) => {return new Date(current.time) > new Date(latest.time) ? current : latest}).status;
      }
      return 'Scheduled'
    },
    fetchRecords() {
      this.appointmentsLoading = true;
      this.$call('healthcare_doworks.api.methods.fetch_patient_appointments')
      .then(response => {
        this.appointments = this.adjustAppointments(response)
        this.appointmentsLoading = false;
      })
      .catch(error => {
        this.appointmentsLoading = false;
        console.error('Error fetching records:', error);
      });
    },
    adjustAppointments(data) {
			return [...(data || [])].filter(value => {
        const practitioner = value.practitioner === this.$resources.user.practitioner;
        const date = dayjs().isSame(dayjs(value.appointment_date), 'day')
        return date
      }).map((d) => {
        try {
          if(typeof d.patient_details === 'string'){
            d.patient_details = JSON.parse(d.patient_details)
            d.visit_notes = JSON.parse(d.visit_notes)
            d.status_log = JSON.parse(d.status_log)
            d.arriveTime = null
            d.status_log.forEach(value => {
              if(value.status == 'Arrived')
                d.arriveTime = dayjs(value.time)
            })
          }
        } catch (error) {
          console.error('Error parsing JSON:', error);
        }
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