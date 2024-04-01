<template>
  <!-- Main Wrapper -->
  <div class="main-wrapper mr-4">
    <!-- Page Content -->
    <div class="row">
      <div class="col-md-12">
        <div class="appointment-tab">
          <!-- Clock And Other Filters -->
          <div class="flex-wrap flex-column flex-xxl-row gap-3 nav nav-tabs nav-tabs-solid pb-0">
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
                <span class="d-flex justify-content-center fw-bolder text-dark" style="padding-right: 1.7rem">{{ formattedDayOfWeek }}</span>
              </div>
              <div class="flex-auto" style="width: 15rem">
                <v-autocomplete
                  v-model="selectedDepartments"
                  density="compact"
                  multiple 
                  chips
                  closable-chips
                  class="w-100"
                  label="Department"
                  :items="departmentsOptions"
                  variant="outlined"
                ></v-autocomplete>
              </div>
              <div class="flex-auto" style="width: 15rem">
                <v-text-field
                  density="compact"
                  class="w-100"
                  v-model="searchValue"
                  label="Search"
                  prepend-inner-icon="pi pi-search"
                  variant="outlined"
                ></v-text-field>
              </div>
            </div>
            <div class="clock ms-xxl-auto order-1 order-xxl-2" v-if="currentHourtime != ''" style="width: fit-content">
              <div class="clock__hours">
                <span class="clock__hourtime" v-text="currentHourtime"></span>
                <span v-text="currentHour"></span>
              </div>
              <div class="clock__minutes" v-text="currentMinutes"></div>
              <div class="clock__seconds" v-text="seconds"></div>
            </div>
          </div>

          <!-- Appointment Tab -->
          <!-- <ul class="nav nav-tabs nav-tabs-solid nav-tabs-rounded">
            <li class="nav-item" v-for="(value, key) in groupedAppointments">
              <a
                :class="{'active' : key === 'Scheduled', 'nav-link': true}"
                :href="`#${key.replace(/\s+/g, '').toLowerCase()}-appointments`"
                data-bs-toggle="tab"
                >
                  {{key}}
                  <Badge :value="getBadgeNumber(key)" severity="secondary"/>
                </a
              >
            </li>
          </ul> -->
          
          <!-- status Appointment Tab -->
          <!-- <appointmenttab 
            v-for="(value, key) in groupedAppointments" 
            :searchValue="searchValue" 
            :appointment="groupedAppointments[key]" 
            :tab="key.replace(/\s+/g, '').toLowerCase()"
          /> -->
          <!-- status Appointment Tab -->

          <v-tabs v-model="tab" align-tabs="center" color="indigo" bg-color="white" show-arrows>
            <v-tab v-for="(value, key) in groupedAppointments" :key="key" :value="key">
              {{ key }}
            </v-tab>
          </v-tabs>
          <div class="tab-content">
            <v-window v-model="tab" disabled>
              <v-window-item v-for="(value, key) in groupedAppointments" :key="key" :value="key">
                <appointmenttab :searchValue="searchValue" :selectedDepartments="selectedDepartments" :appointment="value" :tab="key.toLowerCase()"/>
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
import appointment from "@/assets/json/doctor/myappointments.json";

import Calendar from 'primevue/calendar';
import IconField from 'primevue/iconfield';
import InputIcon from 'primevue/inputicon';
import InputText from 'primevue/inputtext';
import InputMask from 'primevue/inputmask';
import TabView from 'primevue/tabview';
import TabPanel from 'primevue/tabpanel';
import Badge from 'primevue/badge';
import MultiSelect from 'primevue/multiselect';
import {VTextField} from 'vuetify/components/VTextField';
import {VAutocomplete} from 'vuetify/components/VAutocomplete';
import {VTab, VTabs} from 'vuetify/components/VTabs';
import {VContainer, VCol, VRow} from 'vuetify/components/VGrid';
import {VWindow, VWindowItem} from 'vuetify/components/VWindow';


export default {
  inject: ['$socket', '$call'],
  components: {
    Calendar, IconField, InputIcon, InputText, InputMask, TabView, TabPanel,
    Badge, MultiSelect, VTextField, VAutocomplete, VTabs, VTab, VContainer,
    VCol, VRow, VWindow, VWindowItem,
  },
  data() {
    return {
      tab: null,
      appointments: appointment,
      groupedAppointments: {
        Scheduled:[],
        Arrived:[],
        Ready:[],
        'In Room':[],
        Completed:[],
        'No Show':[],
      },
      icondisplay: null,
      selectedDate: new Date(),
      today: new Date(),
      searchValue: '',
      timer: null,
      departmentsOptions: ['Neurology', 'Dermatology', 'Orthopedics', 'Pediatrics', 'Cardiology', 'Ophthalmology', 'Endocrinology', 'Gastroenterology', 'Urology', 'Rheumatology', 'Dentistry'],
      selectedDepartments: null,

      // Clock vars
      currentHour: 0,
      currentMinutes: 0,
      seconds: 0,
      currentHourtime: '',
      SECOND: 1000,
      HOUR: 12,
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
  mounted() {
    this.timer = window.setTimeout(this.updateClock, this.SECOND);
    this.groupAppointmentsByStatus();
    this.fetchRecords();
    // console.log(this.$socket)
  },
  beforeUnmount() {
    // Clear the timeout before unmounting the component
    clearTimeout(this.timer);
  },
  methods: {
    fetchRecords() {
      this.$call('healthcare_doworks.api.methods.fetch_appointments')
      .then(response => {
        console.log(response)
      })
      .catch(error => {
        console.error('Error fetching records:', error);
      });
    },
    getBadgeNumber(tab){
      if(this.groupedAppointments[tab])
        return this.groupedAppointments[tab].length
      return 0
    },

    // Clock methods
    onDateClick(date) {
      console.log(date)
    },
    groupAppointmentsByStatus() {
      this.appointments.forEach(appointment => {
        const status = appointment.visit_status;
        if (!this.groupedAppointments[status])
          this.groupedAppointments[status] = [];
        this.groupedAppointments[status].push(appointment);
      });
    },
    updateClock() {
      const now = new Date();
      this.currentHour = now.getHours();
      this.currentMinutes = this.getZeroPad(now.getMinutes());
      this.seconds = this.getZeroPad(now.getSeconds());
      this.currentHourtime = this.getHourTime(this.currentHour);
      this.currentHour = this.currentHour % this.HOUR || this.HOUR;
      this.$options.timer = window.setTimeout(this.updateClock, this.SECOND);
    },
    getHourTime(h) {
      return h >= 12 ? 'PM' : 'AM'
    },
    getZeroPad(n) {
      return (parseInt(n, 10) >= 10 ? '' : '0') + n
    }
  },
  beforeUnmount(){
    window.clearTimeout(this.timer)
  },
  name: 'Appointments',
};
</script>

<style>
.p-datepicker-trigger-icon{
  top:12.5px
}
.clock {
  background: #5fa4df;
  border: 0.3rem solid #5fa4df;
  border-radius: 0.5rem;
  display: inline-block;
}

.clock__hours,
.clock__minutes,
.clock__seconds {
  background: linear-gradient(to bottom, #26303b 50%, #2c3540 50%);
  display: inline-block;
  color: #fff;
  font-family: 'Nunito', sans-serif;
  font-size: 2rem;
  font-weight: 300;
  padding: 0.5rem 1rem;
  text-align: center;
  position: relative;
}

.clock__hours {
  border-right: 0.15rem solid #5fa4df;
  border-radius: 0.3rem 0 0 0.3rem;
}

.clock__minutes {
  border-right: 0.15rem solid #5fa4df;
}

.clock__seconds {
  border-radius: 0 0.3rem 0.3rem 0;
}

.clock__hourtime {
  font-size: 1rem;
  position: absolute;
  top: 2px;
  left: 8px;
}
</style>