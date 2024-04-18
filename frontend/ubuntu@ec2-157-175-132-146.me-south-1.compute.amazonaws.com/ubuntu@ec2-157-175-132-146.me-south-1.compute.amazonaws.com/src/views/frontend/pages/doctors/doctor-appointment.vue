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
                  :loading="loading"
                  ref="appointmentTabRef"
                  @appointment-dialog="appointmentDialog"
                />
              </v-window-item>
            </v-window>
          </div>
          <!-- /Appointment Tab -->

        </div>
      </div>
    </div>
    <!-- /Page Content -->

    <v-dialog
			v-model="appointmentOpen"
			width="auto"
			id="new-appointment-dialog"
		>
			<template v-slot:default="{ isActive }">
				<v-card rounded="lg">
					<v-card-title class="d-flex justify-space-between align-center">
						<div class="text-h5 text-medium-emphasis ps-2">{{ appointmentForm.type }}</div>
						<v-btn icon="mdi mdi-close" variant="text" @click="isActive.value = false"></v-btn>
					</v-card-title>
					<v-divider class="m-0"></v-divider>
					<v-card-text>
						<a-form layout="vertical" >
							<v-container>
								<v-row>
									<v-col cols="12" md="6">
										<a-form-item label="Appointment Type">
											<a-select
												v-model:value="appointmentForm.appointment_type"
												:options="$resources.appointmentTypes"
												@change="(value, option) => {appointmentForm.appointment_for = option.allow_booking_for}"
												:fieldNames="{label: 'appointment_type', value: 'appointment_type'}"
											></a-select>
										</a-form-item>
										<a-form-item label="Appointment Category">
											<a-input v-model:value="appointmentForm.custom_appointment_category" />
										</a-form-item>
										<a-form-item v-if="appointmentForm.appointment_for === 'Practitioner'" label="Practitioner">
											<a-select
												v-model:value="appointmentForm.practitioner_name"
												:options="$resources.practitioners"
												:fieldNames="{label: 'practitioner_name', value: 'practitioner_name'}"
												show-search
                        @change="showSlots()"
											></a-select>
										</a-form-item>
										<a-form-item v-if="appointmentForm.appointment_for === 'Department'" label="Department">
											<a-select
												v-model:value="appointmentForm.department"
												:options="$resources.departments"
												:fieldNames="{label: 'department', value: 'department'}"
												show-search
											></a-select>
										</a-form-item>
										<a-form-item v-if="appointmentForm.appointment_for === 'Service Unit'" label="Service Unit">
											<a-input v-model:value="appointmentForm.service_unit" />
										</a-form-item>
									</v-col>
									<v-col cols="12" md="6">
										<a-form-item label="Appointment For">
											<a-input v-model:value="appointmentForm.appointment_for" disabled/>
										</a-form-item>
										<a-form-item label="Patient">
											<a-select
												v-model:value="appointmentForm.patient_name"
												:options="$resources.patients"
												:fieldNames="{label: 'patient_name', value: 'patient_name'}"
												@change="(value, option) => {appointmentForm.patient_sex = option.patient_sex;}"
												show-search
											></a-select>
										</a-form-item>
										<a-form-item label="Patient Gender">
											<a-input v-model:value="appointmentForm.patient_sex" disabled/>
										</a-form-item>
										<a-form-item label="Appointment Duration">
											<a-input v-model:value="appointmentForm.duration" />
										</a-form-item>
										<a-form-item label="Appointment Date Range">
											<a-date-picker v-model:value="dateWeek" @change="(val)=>{console.log(val.week())}" :format="customWeekStartEndFormat" style="z-index: 3000" picker="week" />
										</a-form-item>
									</v-col>
								</v-row>
							
							</v-container>
              <v-divider class="mt-2"></v-divider>
              <v-container>
                <v-row>
                  <div class="text-center mb-0" v-html="slotsHtml"></div>
                </v-row>
              </v-container>
						</a-form>
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
						color="indigo"
						
						text="submit"
						variant="tonal"
						@click="onSubmit()"
						></v-btn>
					</v-card-actions>
				</v-card>
			</template>
		</v-dialog>
  </div>
</template>

<script >
import { ref } from 'vue';
import Calendar from 'primevue/calendar';
import Clock from '@/components/clock/Clock.vue';
import moment from "moment";
import dayjs from 'dayjs';
import { message } from 'ant-design-vue';

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


export default {
  inject: ['$socket', '$call'],
  components: {
    Clock, Calendar,VBadge, VTabs, VTab, VWindow, VWindowItem, VIcon, VToolbar, VToolbarItems, VBtn,
    VDialog, VCard, VCardTitle, VCardText, VCardActions, VDivider, VContainer, VCol, VRow,
  },
  data() {
    return {
      tab: null,
      appointments: [],
      groupedAppointments: {Scheduled:[], Arrived:[], Ready:[], 'In Room':[], Completed:[], 'No Show':[],},
      selectedDate: new Date(),
      today: new Date(),
      searchValue: '',
      selectedDepartments: undefined,
      loading: true,
      dateWeek: ref(dayjs()),
      appointmentOpen: false,
			appointmentForm: {
        doctype: 'Patient Appointment',
				name: '',
				appointment_type: '',
				appointment_for: '',
				duration: '',
				custom_appointment_category: '',
				practitioner: '',
        practitioner_name: '',
				department: '',
				service_unit: '',
				patient: '',
				patient_name: '',
				patient_sex: '',
				appointment_date: new Date(),
				appointment_time: new Date(),
			},
      slotsHtml: '',
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
    appointmentDialog(formType, isNew, row) {
			if(isNew){
				this.appointmentForm.name = '';
				this.appointmentForm.duration = '';
				this.appointmentForm.appointment_type = '';
				this.appointmentForm.appointment_for = '';
				this.appointmentForm.custom_appointment_category = '';
				this.appointmentForm.practitioner = '';
				this.appointmentForm.patient = '';
				this.appointmentForm.patient_name = '';
				this.appointmentForm.patient_sex = '';
				this.appointmentForm.department = '';
				this.appointmentForm.service_unit = '';
        this.slotsHtml = '';
			}
			else{
				this.appointmentForm.name = row.appointment_id;
				this.appointmentForm.duration = row.duration;
				this.appointmentForm.appointment_type = row.appointment_type;
				this.appointmentForm.appointment_for = row.appointment_for;
				this.appointmentForm.custom_appointment_category = row.appointment_category;
        this.appointmentForm.practitioner = row.practitioner;
				this.appointmentForm.practitioner_name = row.practitioner_name;
				this.appointmentForm.patient = row.patient_details.id;
				this.appointmentForm.patient_name = row.patient_name;
				this.appointmentForm.patient_sex = row.patient_details.gender;
				this.appointmentForm.department = row.department;
				this.appointmentForm.service_unit = row.service_unit;
        this.showSlots()
			}
			this.appointmentForm.type = formType
			this.appointmentOpen = true
		},
    customWeekStartEndFormat: value => `${dayjs(value).startOf('week').format('MMMM D, YYYY')} -> ${dayjs(value).endOf('week').format('MMMM D, YYYY')}`,
    
    showSlots() {
      if (this.appointmentForm.appointment_date && this.appointmentForm.practitioner) {
        this.slotsHtml = '';
        this.$call('healthcare.healthcare.doctype.patient_appointment.patient_appointment.get_availability_data', {
          practitioner: this.appointmentForm.practitioner,
          date: this.appointmentForm.appointment_date,
          appointment: JSON.stringify(this.appointmentForm)
        }).then((r) => {
          console.log(r)
          let data = r;
          if (data.slot_details.length > 0) {
            // make buttons for each slot
            this.slotsHtml = this.getSlots(data.slot_details, data.fee_validity, this.appointmentForm.appointment_date);

          } else {
            //	fd.available_slots.html('Please select a valid date.'.bold())
            message.error('Healthcare Practitioner {0} not available on {1}', [this.appointmentForm.practitioner, this.appointmentForm.appointment_date]);
          }
        })
      } 
      else {
        this.slotsHtml = 'Appointment date and Healthcare Practitioner are Mandatory';
      }
	  },
    onSubmit(btn){
      // $wrapper.find('button').removeClass('btn-outline-primary');
      // $btn.addClass('btn-outline-primary');
      // selected_slot = $btn.attr('data-name');
      // service_unit = $btn.attr('data-service-unit');
      // appointment_based_on_check_in = $btn.attr('data-day-appointment');
      // duration = $btn.attr('data-duration');
      // add_video_conferencing = parseInt($btn.attr('data-tele-conf'));
      // overlap_appointments = parseInt($btn.attr('data-overlap-appointments'));
      // // show option to opt out of tele conferencing
      // if ($btn.attr('data-tele-conf') == 1) {
      //   if (d.$wrapper.find(".opt-out-conf-div").length) {
      //     d.$wrapper.find(".opt-out-conf-div").show();
      //   } else {
      //     overlap_appointments ?
      //       d.footer.prepend(
      //         `<div class="opt-out-conf-div ellipsis text-muted" style="vertical-align:text-bottom;">
      //           <label>
      //             <span class="label-area">
      //             ${__("Video Conferencing disabled for group consultations")}
      //             </span>
      //           </label>
      //         </div>`
      //       )
      //     :
      //       d.footer.prepend(
      //         `<div class="opt-out-conf-div ellipsis" style="vertical-align:text-bottom;">
      //         <label>
      //           <input type="checkbox" class="opt-out-check"/>
      //           <span class="label-area">
      //           ${__("Do not add Video Conferencing")}
      //           </span>
      //         </label>
      //       </div>`
      //       );
      //   }
      // } else {
      //   d.$wrapper.find(".opt-out-conf-div").hide();
      // }

      // // enable primary action 'Book'
      // d.get_primary_btn().attr('disabled', null);
    },
    getSlots(slot_details, fee_validity, appointment_date) {
      let slot_html = '';
      let appointment_count = 0;
      let disabled = false;
      let start_str, slot_start_time, slot_end_time, interval, count, count_class, tool_tip, available_slots;

      slot_details.forEach((slot_info) => {
        slot_html += `<div class="slot-info">`;
        if (fee_validity && fee_validity != 'Disabled') {
          slot_html += `
            <span style="color:green">
            Patient has fee validity till <b>${moment(fee_validity.valid_till).format('DD-MM-YYYY')}</b>
            </span><br>`;
        } else if (fee_validity != 'Disabled') {
          slot_html += `
            <span style="color:red">
            Patient has no fee validity
            </span><br>`;
        }

        slot_html += `
          <span><b>
          Practitioner Schedule:  </b> ${slot_info.slot_name}
            ${slot_info.tele_conf && !slot_info.allow_overlap ? '<i class="fa fa-video-camera fa-1x" aria-hidden="true"></i>' : ''}
          </span><br>
          <span><b> Service Unit:  </b> ${slot_info.service_unit}</span>`;
          if (slot_info.service_unit_capacity) {
            slot_html += `<br><span> <b> Maximum Capacity: </b> ${slot_info.service_unit_capacity} </span>`;
          }

          slot_html += '</div><br>';

          slot_html += slot_info.avail_slot.map(slot => {
              appointment_count = 0;
              disabled = false;
              count_class = tool_tip = '';
              start_str = slot.from_time;
              slot_start_time = moment(slot.from_time, 'HH:mm:ss');
              slot_end_time = moment(slot.to_time, 'HH:mm:ss');
              interval = (slot_end_time - slot_start_time) / 60000 | 0;

              // restrict past slots based on the current time.
              let now = moment();
              let booked_moment = ""
              if((now.format("YYYY-MM-DD") == appointment_date) && (slot_start_time.isBefore(now) && !slot.maximum_appointments)){
                disabled = true;
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
                      disabled = true;
                      return false;
                    }
                  }

                  // Check for overlaps considering appointment duration
                  if (slot_info.allow_overlap != 1) {
                    if (slot_start_time.isBefore(end_time) && slot_end_time.isAfter(booked_moment)) {
                      // There is an overlap
                      disabled = true;
                      return false;
                    }
                  } else {
                    if (slot_start_time.isBefore(end_time) && slot_end_time.isAfter(booked_moment)) {
                      appointment_count++;
                    }
                    if (appointment_count >= slot_info.service_unit_capacity) {
                      // There is an overlap
                      disabled = true;
                      return false;
                    }
                  }
                });
              }
              if (slot_info.allow_overlap == 1 && slot_info.service_unit_capacity > 1) {
                available_slots = slot_info.service_unit_capacity - appointment_count;
                count = `${(available_slots > 0 ? available_slots : 'Full')}`;
                count_class = `${(available_slots > 0 ? 'badge-success' : 'badge-danger')}`;
                tool_tip =`${available_slots} slots available for booking`;
              }

              if (slot.maximum_appointments) {
                if (appointment_count >= slot.maximum_appointments) {
                  disabled = true;
                }
                else {
                  disabled = false;
                }
                available_slots = slot.maximum_appointments - appointment_count;
                count = `${(available_slots > 0 ? available_slots : 'Full')}`;
                count_class = `${(available_slots > 0 ? 'badge-success' : 'badge-danger')}`;
                return `<button class="btn bg-grey-lighten-3" data-name=${start_str}
                  data-service-unit="${slot_info.service_unit || ''}"
                  data-day-appointment=${1}
                  data-duration=${slot.duration}
                  ${disabled ? 'disabled="disabled"' : ""}>${slot.from_time} -
                  ${slot.to_time} ${slot.maximum_appointments ?
                  `<br><span class='badge ${count_class}'>${count} </span>` : ''}</button>`
              } else {

              return `
                <button class="btn bg-grey-lighten-3" data-name=${start_str}
                  data-duration=${interval}
                  data-service-unit="${slot_info.service_unit || ''}"
                  data-tele-conf="${slot_info.tele_conf || 0}"
                  data-overlap-appointments="${slot_info.service_unit_capacity || 0}"
                  style="margin: 0 10px 10px 0; width: auto;" ${disabled ? 'disabled="disabled"' : ""}
                  data-toggle="tooltip" title="${tool_tip || ''}"
                  @click="handleSlotClick">
                  ${start_str.substring(0, start_str.length - 3)}
                  ${slot_info.service_unit_capacity ? `<br><span class='badge ${count_class}'> ${count} </span>` : ''}
                </button>`;

          }
        }).join("");

          if (slot_info.service_unit_capacity) {
            slot_html += `<br/><small>Each slot indicates the capacity currently available for booking</small>`;
          }
          slot_html += `<br/><br/>`;

      });
      return slot_html;
    },
    handleSlotClick(e){
      console.log(e)
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