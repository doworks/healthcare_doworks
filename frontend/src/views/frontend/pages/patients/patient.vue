<template>
  <!-- Main Wrapper -->
  <div class="main-wrapper mr-3 h-full overflow-hidden">
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
    <div class="card p-4 m-4" style="height: calc(100% - 50px);">
      <v-tabs
      v-model="tab"
      color="deep-purple-accent-4"
      >
        <v-tab value="details">Details</v-tab>
        <v-tab value="medicalHestory">Medical History</v-tab>
        <v-tab value="profile">Profile</v-tab>
      </v-tabs>

      <v-window v-model="tab">
        <v-window-item value="details">
          <a-form layout="vertical" :model="form">
            <v-container fluid>
              <v-row>
                <v-col cols="12" md="6">
                  <a-form-item label="First Name" name="first_name" >
                    <a-input v-model:value="form.first_name"/>
                  </a-form-item>
                  <a-form-item label="Middle Name (optional)" name="middle_name">
                    <a-input v-model:value="form.middle_name"/>
                  </a-form-item>
                  <a-form-item label="Last Name" name="last_name" >
                    <a-input v-model:value="form.last_name"/>
                  </a-form-item>
                  <a-form-item label="Full Name" name="full_name" >
                    <a-input v-model:value="form.full_name" disabled/>
                  </a-form-item>
                  <a-form-item label="CPR" name="custom_cpr" >
                    <a-input v-model:value="form.custom_cpr"/>
                  </a-form-item>
                  <a-form-item label="Gender" name="sex">
                    <a-select v-model:value="form.sex" :options="$resources.genders.data" :fieldNames="{label: 'gender', value: 'gender'}"></a-select>
                  </a-form-item>
                  <a-form-item label="Blood Group" name="blood_group">
                    <a-select v-model:value="form.blood_group" :options="bloodGroupOptions"></a-select>
                  </a-form-item>
                  <a-form-item label="Date of birth" name="dob">
                    <a-date-picker v-model:value="form.dob" format="DD/MM/YYYY" class="w-full"/>
                  </a-form-item>
                  <h6>Age: {{ form.age }}</h6>
                </v-col>
                <v-col cols="12" md="6">
                  <a-form-item label="Status" name="Status" >
                    <a-input v-model:value="form.status" disabled/>
                  </a-form-item>
                  <a-form-item label="Identification Number (UID)" name="uid">
                    <a-input v-model:value="form.uid"/>
                  </a-form-item>
                  <a-form-item label="Inpatient Record" name="inpatient_record" >
                    <a-select 
                    v-model:value="form.inpatient_record" 
                    :options="$resources.inpatientRecords.data" 
                    :fieldNames="{label: 'name', value: 'name'}"
                    >
                  </a-select>
                  </a-form-item>
                  <a-form-item label="Inpatient Status" name="inpatient_status">
                    <a-select v-model:value="form.inpatient_status" :options="inpatientStatusOptions"></a-select>
                  </a-form-item>
                  <a-form-item label="Report Preference" name="report_preference">
                    <a-select v-model:value="form.report_preference" :options="reportPreferenceOptions"></a-select>
                  </a-form-item>
                  <a-form-item label="Mobile" name="mobile">
                    <a-input v-model:value="form.mobile"/>
                  </a-form-item>
                  <a-form-item label="Phone" name="phone">
                    <a-input v-model:value="form.phone"/>
                  </a-form-item>
                  <a-form-item label="Email" name="email">
                    <a-input v-model:value="form.email"/>
                  </a-form-item>
                </v-col>
              </v-row>
              <v-divider class="m-8" :thickness="2"></v-divider>
              <h5 class="mb-4">More Information</h5>
              <v-row>
                <v-col cols="12" md="6">
                  <a-form-item 
                  label="Patient Details" 
                  name="patient_details" 
                  extra="Additional information regarding the patient"
                  >
                  <a-textarea v-model:value="form.patient_details" :rows="14" />
                  </a-form-item>
                </v-col>
              </v-row>
            </v-container>
          </a-form>
        </v-window-item>
      </v-window>
    </div>
    <!-- Page Content -->
    <v-overlay
      :model-value="loadingOverlay"
      class="align-center justify-center"
    >
      <v-progress-circular
        color="primary"
        size="64"
        indeterminate
      ></v-progress-circular>
    </v-overlay>
  </div>
</template>
  
<script >
import {VTab, VTabs} from 'vuetify/components/VTabs';
import {VWindow, VWindowItem} from 'vuetify/components/VWindow';
import dayjs from 'dayjs';

export default {
  inject: ['$socket', '$call'],
  components: {
    VTabs, VTab, VWindow, VWindowItem,
  },
  resources: {
    genders() { return { type: 'list', doctype: 'Gender', fields: ['gender'], auto: true } },
    inpatientRecords() { return { type: 'list', doctype: 'Inpatient Record', fields: ['name'], auto: true } },
  },
  data() {
    return {
      alertVisible: false,
      loadingOverlay: false,
      tab: null,
      form: {},
      bloodGroupOptions: [
        {label: '', value: ''},
        {label: 'A Positive', value: 'A Positive'},
        {label: 'A Negative', value: 'A Negative'},
        {label: 'AB Positive', value: 'AB Positive'},
        {label: 'AB Negative', value: 'AB Negative'},
        {label: 'B Positive', value: 'B Positive'},
        {label: 'B Negative', value: 'B Negative'},
        {label: 'O Positive', value: 'O Positive'},
        {label: 'O Negative', value: 'O Negative'},
      ],
      inpatientStatusOptions: [
        {label: '', value: ''},
        {label: 'Admission Scheduled', value: 'Admission Scheduled'},
        {label: 'Admitted', value: 'Admitted'},
        {label: 'Discharge Scheduled', value: 'Discharge Scheduled'},
      ],
      reportPreferenceOptions: [
        {label: '', value: ''},
        {label: 'Email', value: 'Email'},
        {label: 'Print', value: 'Print'},
      ],
    };
  },
  created() {
    this.fetchRecords();
    this.$socket.on('patients', response => {
      if(response){
        response.age = this.calculateAge(response.dob)
        this.patients = response
      }
    })
  },
  mounted() {
  },
  methods: {
    showAlert(message, duration) {
      this.message = message;
      this.alertVisible = true;
      setTimeout(() => {
        this.alertVisible = false;
      }, duration);
    },
    fetchRecords() {
      this.loadingOverlay = true;
      this.$call('healthcare_doworks.api.methods.patient', {patient: this.$route.params.patientId})
      .then(response => {
        response.doc.age = this.get_age(response.doc.dob)
        response.doc.dob = dayjs(response.doc.dob)
        this.form = response.doc
        console.log(this.form)
        this.loadingOverlay = false;
      })
      .catch(error => {
        this.loadingOverlay = false;
        console.error('Error fetching records:', error);
      });
    },
    openNew() {
      this.row = {};
      this.rowDialog = true;
    },
    openRow(row) {
      this.$router.push({ name: 'patient', params: { patientId: row.name } });
    },
    get_age(birth) {
      let ageMS = Date.parse(Date()) - Date.parse(birth);
      let age = new Date();
      age.setTime(ageMS);
      let years = age.getFullYear() - 1970;
      return years + ' Year(s) ' + age.getMonth() + ' Month(s) ' + age.getDate() + ' Day(s)';
    }
  },
  name: 'Patients List',
};
</script>
  
<style>
/* Hide the ListSelectBanner */
.editable-table .absolute.inset-x-0.bottom-6.mx-auto.w-max.text-base {
  display: none !important;
}
</style>  