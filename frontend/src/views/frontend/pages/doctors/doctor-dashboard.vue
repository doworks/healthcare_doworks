<template>
  <!-- Main Wrapper -->
  <div class="main-wrapper" style="margin-right: -10px;">
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
                          :model-value="getPercentage(finishedAppointments,totalAppointments)"
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
                        <h4 class="text-info">{{finishedAppointments}}</h4>
                        <h3>/{{totalAppointments}}</h3>
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
                          :model-value="50"
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
                      <h6>Next Appointment in</h6>
                      <h3>{{nextAppointmentTime}}</h3>
                      <p class="text-muted">today</p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="row row-cols-lg-2 cont">
        <Card class="col-12 col-lg-6 left-col p-0 " style="overflow: hidden;">
          <template #title>Upcoming Appintments</template>
          <template #content>
            <div class="table-responsive">
              <table style="table-layout: auto; min-width: 435px; border-collapse: collapse;" class="table mb-0 border-0 table-hover">
                <tbody>
                  <tr v-for="(appointment, index) in appointments" :key="index" @click="onPatientDetails(appointment)">
                    <td class="table-image appoint-doctor d-flex">
                      <img width="28" height="28" class="rounded-circle avatar-lg align-self-center" :src="appointment.image" alt=""/>
                      <div style="padding: 10px 15px; vertical-align: middle; padding-right: 0;">
                        <h6 style="font-size: 16px; font-weight: 500; margin-bottom: 0">{{ appointment.patient_name }}</h6>
                        <span style="color: rgba(51, 52, 72, 0.5); font-size: 16px; font-weight: 500">{{ appointment.appointment_type }}</span>
                      </div>
                    </td>
                    <td class="text-sm align-middle">
                      <span class="text-900 font-medium text-sm">{{ appointment.visit_status }}</span>
                    </td>
                    <td class="text-sm align-middle text-end " style="position: sticky; right: 0; z-index: 1; width: 5.5rem;">
                      <Tag :value="appointment.appointment_time_moment" severity="info" class="absolute w-100"></Tag>
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
        </Card>
        <div class="col-12 col-lg-6 right-col p-0 details-card mt-4 mt-md-0" ref="containerRef">
          <div class="flip-card-inner" :class="{ 'isFlipped': isFlipped }">
            <div class="flip-card-front">
              <patientDetailsCard :patient="nextPatientDetails" @cardRendered="adjustContainerHeight"/>
            </div>
            <div class="flip-card-back">
              <patientDetailsCard :patient="nextPatientDetails"/>
            </div>
          </div>
        </div>
        <Card class="col-12 col-lg-6 left-col p-0 mt-4" style="overflow: hidden;">
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
        </Card>
      </div>
    </div>    
    <!-- /Page Content -->
  </div>
  <!-- /Main Wrapper -->
</template>
<script>
import myappointments from "@/assets/json/doctor/myappointments.json";
import moment from "moment";

import patientDetailsCard from './patient-details-card.vue'

import {VProgressCircular} from 'vuetify/components/VProgressCircular';
import { watchEffect } from "vue";
import Card from 'primevue/card';
import Tag from 'primevue/tag';
import Button from 'primevue/button';


export default {
  components: {
    VProgressCircular,
    Card,
    Tag,
    patientDetailsCard,
    Button,
  },
  data() {
    return {
      totalAppointments: 20,
      finishedAppointments: 10,
      walkedInPatients:0,
      nextAppointmentTime: 10,
      appointments: [],
      nextPatientDetails: {
        "name": "HLC-APP-2024-00001",
        "appointment_type": "General",
        "patient_name": "Sayed Mohamed Adnan",
        "mobile": "1234567890",
        "practitioner_name": "Sayed Hassan",
        "cpr": 123576342,
        "department": "Neurology",
        "status": "Scheduled",
        "invoiced": 100,
        "paid_amount": 0,
        "duration": 20,
        "visit_status": "Scheduled",
        "image": "https://randomuser.me/api/portraits/men/1.jpg",
        "practitioner_image": "https://randomuser.me/api/portraits/men/30.jpg",
        "appointment_time": "09:45:00",
        "appointment_date": "2024-02-21",
        "patientDetails": {
          "date_of_birth": "2024-02-21",
          "gender": "Male",
          "weight": "65 Kg",
          "height": "180 cm"
        }
      },
      isFlipped: false,
    };
  },
  mounted() {
    watchEffect(() => {
      this.appointments = this.getUpcomingAppointments(myappointments)
    })
    this.adjustContainerHeight();
  },
  methods: {
    getPercentage: (num1, num2) => {
      return num1 / num2 * 100
    },
    getUpcomingAppointments: (data) => {
      const upcoming = data.slice(0, 4)
      return [...(upcoming || [])].map((d) => {
        d.appointment_time_moment = moment(d.appointment_date + ' ' + d.appointment_time).format('LT');
        return d;
      });
    },
    onPatientDetails: function(patient){
      this.isFlipped = !this.isFlipped;
      setTimeout(() => {
        this.nextPatientDetails = patient
      }, 200)
    },
    adjustContainerHeight(cardHeight) {
      if(cardHeight)
        this.$refs.containerRef.style.minHeight = cardHeight + 'px';
    }
  },
  name: "doctor-dashboard",
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