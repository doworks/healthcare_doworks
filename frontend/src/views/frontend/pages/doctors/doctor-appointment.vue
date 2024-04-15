<template>
  <!-- Main Wrapper -->
  <div class="main-wrapper mr-4">
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
                  :options="departmentsOptions"
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
            <v-btn icon="mdi mdi-plus" @click="newAppointment()" rounded="0"></v-btn>
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
                  :loading="loading"
                  ref="appointmentTabRef"
                />
              </v-window-item>
            </v-window>
          </div>
          <!-- /Appointment Tab -->

        </div>
      </div>
    </div>
    <!-- /Page Content -->    
  </div>
</template>

<script >
import { ref } from 'vue';
import Calendar from 'primevue/calendar';
import Clock from '@/components/clock/Clock.vue';
import moment from "moment";

import {VBadge} from 'vuetify/components/VBadge';
import {VTab, VTabs} from 'vuetify/components/VTabs';
import {VWindow, VWindowItem} from 'vuetify/components/VWindow';
import {VIcon} from 'vuetify/components/VIcon';
import {VToolbar, VToolbarItems} from 'vuetify/components/VToolbar';
import {VBtn} from 'vuetify/components/VBtn';


export default {
  inject: ['$socket', '$call'],
  components: {
    Clock, Calendar,VBadge, VTabs, VTab, VWindow, VWindowItem, VIcon, VToolbar, VToolbarItems, VBtn,
  },
  data() {
    return {
      tab: null,
      appointments: [],
      groupedAppointments: {Scheduled:[], Arrived:[], Ready:[], 'In Room':[], Completed:[], 'No Show':[],},
      selectedDate: new Date(),
      today: new Date(),
      searchValue: '',
      departmentsOptions: [
        {label: 'Neurology', value: 'Neurology'},
        {label: 'Dermatology', value: 'Dermatology'},
        {label: 'Orthopedics', value: 'Orthopedics'},
        {label: 'Pediatrics', value: 'Pediatrics'},
        {label: 'Ophthalmology', value: 'Ophthalmology'},
        {label: 'Endocrinology', value: 'Endocrinology'},
        {label: 'Gastroenterology', value: 'Gastroenterology'},
        {label: 'Urology', value: 'Urology'},
        {label: 'Rheumatology', value: 'Rheumatology'},
        {label: 'Dentistry', value: 'Dentistry'},
      ],
      selectedDepartments: undefined,
      loading: true,
    };
  },
  computed: {
    formattedDayOfWeek() {
      if (!this.selectedDate) return '';
      
      const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
      const selectedDay = new Date(this.selectedDate);
      const dayOfWeek = days[selectedDay.getDay()];

      return dayOfWeek;
    }
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
    fetchRecords() {
      this.loading = true;
      this.$call('healthcare_doworks.api.methods.fetch_patient_appointments')
      .then(response => {
        this.appointments = this.adjustAppointments(response)
        this.groupAppointmentsByStatus();
        this.loading = false; 
      })
      .catch(error => {
        this.loading = false;
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
    newAppointment() {
      // const appointmentTab = this.$refs.appointmentTabRef;
      // console.log(appointmentTab)
      // appointmentTab.appointmentDialog('New Appointment', true)
    },

    onDateClick(date) {
      console.log(date)
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