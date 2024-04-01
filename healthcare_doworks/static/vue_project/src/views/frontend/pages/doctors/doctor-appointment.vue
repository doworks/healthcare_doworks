<template>
  <!-- Main Wrapper -->
  <div class="main-wrapper">
    <layoutheader></layoutheader>
    <doctorsidebar></doctorsidebar>
    

    <!-- Page Content -->
    <div class="page-wrapper">
      <div class="content container-fluid">
        <breadcrumb1 :title="title" />
        <div class="row">
          <div class="col-md-12">
            <!-- <h4 class="mb-4">Patient Appoinment</h4> -->
            <div class="appointment-tab">
              <!-- Appointment Tab -->
              <ul class="nav nav-tabs nav-tabs-solid nav-tabs-rounded">
                <li class="nav-item">
                  <a
                    class="nav-link active"
                    href="#scheduled-appointments"
                    data-bs-toggle="tab"
                    >Scheduled</a
                  >
                </li>
                <li class="nav-item">
                  <a
                    class="nav-link"
                    href="#arrived-appointments"
                    data-bs-toggle="tab"
                    >Arrived</a
                  >
                </li>
                <li class="nav-item">
                  <a
                    class="nav-link"
                    href="#ready-appointments"
                    data-bs-toggle="tab"
                    >Ready</a
                  >
                </li>
                <li class="nav-item">
                  <a
                    class="nav-link"
                    href="#done-appointments"
                    data-bs-toggle="tab"
                    >Done</a
                  >
                </li>
              </ul>
              <!-- /Appointment Tab -->

              <div class="tab-content">
                <!-- status Appointment Tab -->
                <appointmenttab :appointment="appointmentUp" :tab="'scheduled'"/>
                <!-- <appointmenttab :appointment="appointment" :tab="'arrived'"/>
                <appointmenttab  :tab="'ready'"/> -->
                <!-- status Appointment Tab -->
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <!-- /Page Content -->
  </div>
  <!-- /Main Wrapper -->
  <!-- Appointment Details Modal -->
  <div class="modal fade custom-modal" id="appt_details">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Appointment Details</h5>
          <b-button
            type="button"
            class="btn-close"
            data-bs-dismiss="modal"
            aria-label="Close"
          ></b-button>
        </div>
        <div class="modal-body">
          <ul class="info-details">
            <li>
              <div class="details-header">
                <div class="row">
                  <div class="col-md-6">
                    <span class="title">#APT0001</span>
                    <span class="text">21 Oct 2023 10:00 AM</span>
                  </div>
                  <div class="col-md-6">
                    <div class="text-end">
                      <b-button
                        type="button"
                        class="btn bg-success-light btn-sm"
                        id="topup_status"
                      >
                        Completed
                      </b-button>
                    </div>
                  </div>
                </div>
              </div>
            </li>
            <li>
              <span class="title">Status:</span>
              <span class="text">Completed</span>
            </li>
            <li>
              <span class="title">Confirm Date:</span>
              <span class="text">29 Jun 2023</span>
            </li>
            <li>
              <span class="title">Paid Amount</span>
              <span class="text">$450</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
  <!-- /Appointment Details Modal -->
  <indexfooter />
</template>

<script setup>

import { ref, onMounted } from 'vue';
import { FilterMatchMode } from 'primevue/api';

const icondisplay = ref();
const customers = ref();
const filters = ref({
  global: { value: null, matchMode: FilterMatchMode.CONTAINS },
  name: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
  'country.name': { value: null, matchMode: FilterMatchMode.STARTS_WITH },
  representative: { value: null, matchMode: FilterMatchMode.IN },
  status: { value: null, matchMode: FilterMatchMode.EQUALS },
  verified: { value: null, matchMode: FilterMatchMode.EQUALS }
});
const loading = ref(false);

</script>

<script >
import appointmentUp from "@/assets/json/doctor/doctorupcoming.json";
import appointment from "@/assets/json/doctor/doctortoday.json";

import Calendar from 'primevue/calendar';
import IconField from 'primevue/iconfield';
import InputIcon from 'primevue/inputicon';
import InputText from 'primevue/inputtext';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import ColumnGroup from 'primevue/columngroup';   // optional
import Row from 'primevue/row';                   // optional

export default {
  components: {
    Calendar,
    IconField,
    InputIcon,
    InputText,
    DataTable,
  },
  data() {
    return {
      title: "Appointments",
      text: "Home",
      text1: "Appointments",
      appointment: appointment,
      appointmentUp: appointmentUp,
      docs: ["A-", "A+", "B-", "B+", "AB-", "AB+", "O-", "O+"],
      todayDate: new Date(),
      menu: false,
      modal: false,
      menu2: false,
    };
  },
};
</script>
