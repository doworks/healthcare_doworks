<template>
  <!-- Main Wrapper -->
  <div class="main-wrapper mr-3" id="doctor-dashboard" style="margin-right: -10px;">
    <v-alert
      v-if="alertActive && alertType === 'error'"
      type="error"
      position="absolute"
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
              <span class="text-surface-500 dark:text-surface-400 text-sm">Today Appointments</span>
              <!-- <span class="font-bold text-lg">{{ val.value }}%</span>
              <h6 >Today Appointments</h6> -->
              <div class="d-flex" v-if="practitionerFilter.length > 0">
                <span class="text-info font-bold text-lg">
                  {{
                    appointments.filter(value => practitionerFilter.includes(value.practitioner_name)).length - 
                    appointments.filter(value => practitionerFilter.includes(value.practitioner_name)).length
                  }}
                </span>
                <span class="font-bold text-lg">
                  /{{appointments.filter(value => practitionerFilter.includes(value.practitioner_name)).length}}
                </span>
              </div>
              <div class="d-flex" v-else>
                <span class="text-info font-bold text-lg">{{appointments.length - appointments.length}}</span>
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
                <span class="text-green font-bold text-lg">
                  {{
                    appointments.filter(val => val.status == 'Walked In' && (this.practitionerFilter.length == 0 || 
                      this.practitionerFilter.includes(val.practitioner_name))).length
                  }}
                </span>
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
    <div class="columns-1 md:columns-2">
      <a-select
      v-model:value="practitionerFilter"
      @change="val => {filters.practitioner_name.value = val}"
      mode="multiple"
      class="p-column-filter mb-2"
      style="width: 100%; align-items: center;"
      placeholder="Any Practitioner"
      max-tag-count="responsive"
      :options="$resources.practitioners.data?.options"
      :fieldNames="{label: 'practitioner_name', value: 'practitioner_name'}"
      show-search
      :loading="$resources.practitioners.list.loading"
      @search="(value) => {handleSearch(
        value, 
        $resources.practitioners, 
        {status: 'Active', practitioner_name: ['like', `%${value}%`]}, 
        {status: 'Active'},
      )}"
      :filterOption="false"
      >
    </a-select>
      

    </div>
    <div class="row row-cols-lg-2 cont mb-3">
      <Card class="pat-det left-col p-0 min-h-[550px]" style="overflow: hidden;">
        <template #title>
          <ToggleButton 
          v-model="showCompleted" 
          onLabel="Completed" 
          offLabel="Upcoming" 
          onIcon="mdi mdi-check-all" 
          offIcon="mdi mdi-clock-outline" 
          class="mb-2 w-full" 
          aria-label="Show Completed" 
          />
          {{showCompleted ? 'Completed' : 'Upcoming'}} Appintments
        </template>
        <template #content>
          <div class="table-responsive">
            <DataTable
            v-model:filters="filters"
            size="small"
            sortField="arriveTime"
            dataKey="id"
            :sortOrder="-1"
            :rowClass="rowClass"
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
                  <a 
                  :href="$router.resolve({ name: 'patient', params: { patientId: data.patient_details.id } }).href" 
                  target="_blank" 
                  style="color: unset; text-decoration: unset"
                  >
                    <div class="d-flex align-items-center gap-2">
                      <v-avatar>
                        <img
                        class="h-100 w-100"
                        :src="data.patient_details.image ? data.patient_details.image :data.patient_details.gender === 'Male' ? maleImage :femaleImage"
                        />
                        <!-- <span v-if="!data.patient_details.image" class="text-h5">{{ getInitials(data.patient_name) }}</span> -->
                      </v-avatar>
                      <div style="padding: 10px 15px; vertical-align: middle; padding-right: 0;">
                        <h6 style="margin-bottom: 0">{{ data.patient_name }}</h6>
                        <span style="color: rgba(51, 52, 72, 0.5);">{{ data.service_unit }}</span>
                      </div><br/>
                    </div>
                  </a>
                  <!-- </router-link> -->
                </template>
              </Column>
              <Column header="Practitioner" field="practitioner_name" hidden>
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
                    @click="() => {appointmentNoteDialog(data)}"
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
                @click="() => {appointmentNoteDialog(selectedRow)}"
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
                          <v-btn v-if="data.read" size="small" variant="text" icon="mdi mdi-eye" @click="() => { updateSeen(data) }">
                          </v-btn>
                          <v-btn v-else-if="!data.read" size="small" variant="text" icon="mdi mdi-eye-off" @click="() => { updateSeen(data) }">
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
            <!-- <Button label="See All" link href="/appointments" severity="warn"/> -->
            <a :href="$router.resolve({ name: 'appointments' }).href" style="text-decoration: unset">
              See All
            </a>
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
    
    <!-- Dialogs -->
    <appointmentNoteDialog 
    :isOpen="appointmentNoteOpen" 
    @update:isOpen="appointmentNoteOpen = $event" 
    @show-alert="showAlert" 
    :appointmentId="selectedRow.name"
    />
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

import { FilterMatchMode } from 'primevue/api';

export default {
  inject: ['$call', '$socket'],
  components: {
    patientDetailsCard, VAvatar, VChip, VListItem, VEmptyState,
  },
  resources: {
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
      practitionerFilter: ref([]),
      walkedInPatients:0,
      appointments: ref([]),
      currentTime: dayjs(),
      nextPatientDetails: null,
      isFlipped: false,
      appointmentsLoading: false,
      totalRecords: 0,
      selectedDates: [dayjs()],
      filters: {practitioner_name: { value: undefined, matchMode: FilterMatchMode.IN }},
      selectedRow: {},
      appointmentNoteOpen: false,
      showCompleted: false,

      alertMessage: '',
      alertType: '', // 'success' or 'error'
      alertActive: false,
    };
  },
  watch: {
    '$myresources.user': {
      handler(newValue) {
        if(this.$myresources.user.practitioner_name){
          this.filters.practitioner_name.value = [this.$myresources.user.practitioner_name]
        }
      },
      immediate: true,
    },
  },
  created() {
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
  },
  computed: {
    updatedAppointments() {
      let filteredAppointments = this.appointments.filter(val => val.custom_visit_status !== 'Completed' && val.custom_visit_status !== 'Cancelled')
      if(this.showCompleted)
        filteredAppointments = this.appointments.filter(val => val.custom_visit_status == 'Completed')

      return filteredAppointments.map(appointment => {
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
        let validAppointments = this.appointments.filter(appointment => 
          ['Scheduled', 'Arrived', 'Ready'].includes(appointment.custom_visit_status) &&
          (this.practitionerFilter.length == 0 || 
          this.practitionerFilter.includes(appointment.practitioner_name))
        );

        // Reduce to find the earliest valid appointment
        let firstValidAppointment = validAppointments.reduce((earliest, current) => {
          const currentDate = dayjs(`${current.appointment_date} ${current.appointment_time}`);
          const earliestDate = dayjs(`${earliest.appointment_date} ${earliest.appointment_time}`);

          // Compare dates and return the earliest appointment
          return currentDate.isBefore(earliestDate) ? current : earliest;
        }, validAppointments[0]); // Initialize with the first valid appointment

        if(firstValidAppointment){
          let nextappointment = dayjs(firstValidAppointment.appointment_date + ' ' + firstValidAppointment.appointment_time);
          // const diffInSeconds = this.currentTime.diff(nextappointment, 'second');
          // const hours = Math.floor(diffInSeconds / 3600);
          // const minutes = Math.floor((diffInSeconds % 3600) / 60);
          // const seconds = diffInSeconds % 60;
          // return `${hours}:${minutes}:${seconds}`
          return dayjs(this.currentTime).to(nextappointment)
        }
      }
      return ''
    },
  },
  mounted() {
    if(this.$myresources.user.practitioner_name){
      this.filters.practitioner_name.value = [this.$myresources.user.practitioner_name]
    }
    
    this.fetchRecords()
    
    setInterval(() => {
			this.currentTime = dayjs();
		}, 60000); // Update every second
    this.adjustContainerHeight();
  },
  methods: {
    showAlert(message, type) {
      this.alertMessage = message;
      this.alertType = type;
      this.alertActive = true;
    },
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
      this.appointmentsLoading = true;
      const dates = this.selectedDates.map(date => date.format('YYYY-MM-DD'))
      this.$call('healthcare_doworks.api.methods.fetch_patient_appointments', {
        filters: {appointment_date: ['in', [dayjs().format('YYYY-MM-DD')]]}, start: 0, limit: 1000
      })
      .then(response => {
        if(response){
          this.appointments = this.adjustAppointments(response.appointments)
          this.appointmentsLoading = false;
        }
      })
      .catch(error => {
        this.appointmentsLoading = false;
        this.showAlert(error.message, 'error')
        console.error('Error fetching records:', error);
      });
    },
    adjustAppointments(data) {
			return [...(data || [])].filter(value => {
        const practitioner = value.practitioner === this.$myresources.user.practitioner;
        const date = dayjs().isSame(dayjs(value.appointment_date), 'day')
        return date
      }).map((d) => {
        d.notes = this.stripHtml(d.notes)
        d.arriveTime = null

        d.visit_notes = d.visit_notes.map(note => {
          note.dayDate = dayjs(note.time).format('DD/MM/YYYY')
          note.dayTime = dayjs(note.time).format('h:mm A')
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
    updateSeen(data) {
			data.read = !data.read
			this.$call('healthcare_doworks.api.general_methods.modify_child_entry', 
        {parent_doctype: 'Patient Appointment', parent_doc_name: this.selectedRow.name, child_table_fieldname: 'custom_visit_notes', filters: {name: data.name}, update_data: data}
      ).catch(error => {
        this.showAlert(error.message, 'error')
      });
		},
    appointmentNoteDialog(row) {
      this.selectedRow = row
      this.appointmentNoteOpen = true
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
    rowClass(data) {
      return [{ '!bg-green-50 hover:!bg-green-100': data.status == 'Walked In' }];
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
    handleSearch(query, resource, filters, initialFilters, orFilters) {
      // Clear the previous timeout to avoid spamming requests
      clearTimeout(this.searchTimeout);

      // Set a new timeout (300ms) for debouncing
      this.searchTimeout = setTimeout(() => {
        if (query) {
          // Update list resource options to fetch matching records from server
          resource.update({filters, orFilters});

          // Fetch the updated results
          resource.reload();
        } else {
          // If no search query, load initial records
          resource.update({filters: initialFilters, orFilters});
          resource.reload();
        }
      }, 300);  // Debounce delay of 300ms
    },
  },
  name: "doctor-dashboard",
};
</script>

<style>
/* #doctor-dashboard .p-paginator-bottom{
  display: none;
} */
.pat-det .p-card-body{
  height: 100%;
}

.pat-det .p-card-content{
  height: 100%;
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