<template>
  <!-- Main Wrapper -->
  <div class="patient-profile main-wrapper mr-3 h-full overflow-hidden">
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
        <v-tab value="records">Medical Records</v-tab>
      </v-tabs>

      <v-window v-model="tab">
        <v-window-item value="details">
          <a-form layout="vertical" :model="form">
            <v-container fluid>
              <v-row>
                <v-col cols="12" md="6">
                  <a-form-item label="First Name" name="first_name" >
                    <a-input v-model:value="form.first_name" @change="updateFullName"/>
                  </a-form-item>
                  <a-form-item label="Middle Name (optional)" name="middle_name">
                    <a-input v-model:value="form.middle_name" @change="updateFullName"/>
                  </a-form-item>
                  <a-form-item label="Last Name" name="last_name" >
                    <a-input v-model:value="form.last_name" @change="updateFullName"/>
                  </a-form-item>
                  <a-form-item label="Full Name" name="patient_name" >
                    <a-input v-model:value="form.patient_name" disabled/>
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
                    <a-date-picker v-model:value="form.dob" format="DD/MM/YYYY" class="w-full" @change="(date) => {form.age = get_age(date)}"/>
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
        <v-window-item value="medicalHestory">
          <v-container fluid>
            <v-row>
              <v-col cols="12" lg="6">
                <h5>Allergies</h5>
                <EditableTable :columns="[
                  {label: 'Type', key: 'type', width: 3},
                  {label: 'Severity', key: 'severity', width: 2},
                  {label: 'Note', key: 'note', width: '270px'},
                ]"
                :rows="form.custom_allergies_table"
                @update="(items) => {allergies = items}"
                title="Allergies"
                >
                  <template v-slot:dialog="{ row }">
                    <a-form layout="vertical">
                      <a-form-item label="Type">
                        <a-select
                        v-model:value="row.type"
                        :options="allergiesOptions"
                        ></a-select>
                      </a-form-item>
                      <a-form-item label="Type">
                        <a-select
                        v-model:value="row.severity"
                        :options="severityOptions"
                        ></a-select>
                      </a-form-item>
                      <a-form-item label="Note">
                        <a-textarea v-model:value="row.note" :rows="4" />
                      </a-form-item>
                    </a-form>
                  </template>
                </EditableTable>
              </v-col>
              <v-col cols="12" lg="6">
                <h5>Infected Diseases</h5>
                <EditableTable :columns="[
                  {label: 'Name', key: 'name1'},
                  {label: 'Note', key: 'note', width: '320px'},
                ]"
                :rows="form.custom_infected_diseases"
                @update="(items) => {infectedDiseases = items}"
                title="Infected Diseases"
                >
                  <template v-slot:dialog="{ row }">
                    <a-form layout="vertical">
                      <a-form-item label="Name">
                        <a-input v-model:value="row.name1"/>
                      </a-form-item>
                      <a-form-item label="Note">
                        <a-textarea v-model:value="row.note" :rows="4" />
                      </a-form-item>
                    </a-form>
                  </template>
                </EditableTable>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" lg="6">
                <h5>Surgical History</h5>
                <EditableTable :columns="[
                  {label: 'Surgery', key: 'surgery'},
                  {label: 'Date', key: 'date'},
                  {label: 'Practitioner', key: 'practitioner'},
                  {label: 'Note', key: 'notes', width: '150px'},
                ]"
                :rows="form.custom_surgical_history_table"
                @update="(items) => {surgicalHistory = items}"
                title="Surgical History"
                >
                  <template v-slot:dialog="{ row }">
                    <a-form layout="vertical">
                      <a-form-item label="Surgery">
                        <a-input v-model:value="row.surgery"/>
                      </a-form-item>
                      <a-form-item label="Date">
                        <a-date-picker 
                        v-model:value="row.dayDate"
                        format="DD/MM/YYYY" 
                        style="z-index: 3000"
                        @change="date => {row.date = date.format('YYYY-MM-DD') }"
                        />
                      </a-form-item>
                      <a-form-item label="Practitioner">
                        <a-input v-model:value="row.practitioner"/>
                      </a-form-item>
                      <a-form-item label="Note">
                        <a-textarea v-model:value="row.note" :rows="4" />
                      </a-form-item>
                    </a-form>
                  </template>
                </EditableTable>
              </v-col>
              <v-col cols="12" lg="6">
                <h5>Medications</h5>
                <EditableTable :columns="[
                  {label: 'Name', key: 'name1'},
                  {label: 'Reason', key: 'reason'},
                  {label: 'From Date', key: 'from_date'},
                  {label: 'Status', key: 'status', }
                ]"
                :rows="form.custom_medications"
                @update="(items) => {medications = items}"
                title="Medications"
                >
                  <template v-slot:dialog="{ row }">
                    <a-form layout="vertical">
                      <a-form-item label="Name">
                        <a-input v-model:value="row.name1"/>
                      </a-form-item>
                      <a-form-item label="Reason">
                        <a-input v-model:value="row.reason"/>
                      </a-form-item>
                      <a-form-item label="From Date">
                        <a-date-picker 
                        v-model:value="row.dayDate"
                        format="DD/MM/YYYY" 
                        style="z-index: 3000"
                        @change="date => {row.from_date = date.format('YYYY-MM-DD') }"
                        />
                      </a-form-item>
                      <a-form-item label="Status">
                        <a-checkbox 
                        v-model:checked="row.is_active" 
                        @change="e => {row.status = e.target.chicked ? 'Active' : 'Inactive' }"
                        />
                      </a-form-item>
                    </a-form>
                  </template>
                </EditableTable>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" lg="6">
                <h5>Habits / Social</h5>
                <EditableTable :columns="[
                  {label: 'Habit', key: 'habit', width: 3},
                  {label: 'Note', key: 'note', width: '270px'},
                ]"
                :rows="form.custom_habits__social"
                @update="(items) => {habits = items}"
                title="Habits / Social"
                >
                  <template v-slot:dialog="{ row }">
                    <a-form layout="vertical">
                      <a-form-item label="Habit">
                        <a-select
                        v-model:value="row.habit"
                        :options="habitsOptions"
                        ></a-select>
                      </a-form-item>

                      <a-form-item label="Note">
                        <a-textarea v-model:value="row.note" :rows="4" />
                      </a-form-item>
                    </a-form>
                  </template>
                </EditableTable>
              </v-col>
              <v-col cols="12" lg="6">
                <h5>Risk Factors</h5>
                <EditableTable :columns="[
                  {label: 'Type', key: 'type', width: 3},
                  {label: 'Severity', key: 'severity', width: 2},
                  {label: 'Note', key: 'note', width: '270px'},
                ]"
                :rows="form.custom_risk_factors_table"
                @update="(items) => {riskFactors = items}"
                title="Risk Factors"
                >
                  <template v-slot:dialog="{ row }">
                    <a-form layout="vertical">
                      <a-form-item label="Type">
                        <a-input v-model:value="row.type"/>
                      </a-form-item>
                      <a-form-item label="Severity">
                        <a-input v-model:value="row.severity"/>
                      </a-form-item>
                      <a-form-item label="Note">
                        <a-textarea v-model:value="row.note" :rows="4" />
                      </a-form-item>
                    </a-form>
                  </template>
                </EditableTable>
              </v-col>
            </v-row>
            <v-divider class="m-10"></v-divider>
            <a-form layout="vertical">
              <h5 class="mb-4">Family History</h5>
              <v-row>
                <v-col cols="12" lg="6">
                  <a-form-item label="Chronic Diseases">
                    <a-textarea v-model:value="form.custom_chronic_diseases" :rows="4" />
                  </a-form-item>
                </v-col>
                <v-col cols="12" lg="6">
                  <a-form-item label="Genetic Diseases">
                    <a-textarea v-model:value="form.custom_genetic_conditions" :rows="4" />
                  </a-form-item>
                </v-col>
              </v-row>
            </a-form>
        </v-container>
        </v-window-item>
        <v-window-item value="records">
          <v-container fluid>
            <v-row>
              <v-col cols="12" md="6" lg="3">
                <a-range-picker v-model:value="profileRangeFilter" format="DD/MM/YYYY" class="w-full"/>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" md="6">
                <v-card id="vital-signs" variant="tonal" color="light-blue">
                  <template v-slot:title>Vital Signs ({{ $resources.vitalSigns.data.length }})</template>
                  <template v-slot:text>
                    <div :class="{'d-none': $resources.vitalSigns.data.length > 0}">
                      <v-empty-state
                        title="No Vital Signs"
                      ></v-empty-state>
                    </div>
                    <DataTable 
                    :value="$resources.vitalSigns.data" 
                    selectionMode="single" 
                    :metaKeySelection="true" 
                    dataKey="id" 
                    @row-click="vitalSignSelect"
                    class="max-h-72 overflow-y-auto"
                    >
                      <Column headerStyle="width:3rem">
                        <template #body="slotProps">
                          {{ slotProps.index + 1 }}
                        </template>
                      </Column>
                      <Column>
                        <template #body="slotProps">
                          {{ formatDate(slotProps.data.signs_date + ' ' + slotProps.data.signs_time) }}
                        </template>
                      </Column>
                      <Column>
                        <template #body="slotProps">
                          {{ vitalSigns(slotProps.data) }}
                        </template>
                      </Column>
                    </DataTable>
                  </template>
                </v-card>
              </v-col>
              <v-col cols="12" md="6">
                <v-card id="consultations" variant="tonal" color="amber">
                  <template v-slot:title>Consultations ({{ $resources.consultations.data.length }})</template>
                  <template v-slot:text>
                    <div :class="{'d-none': $resources.consultations.data.length > 0}">
                      <v-empty-state
                        title="No Consultations"
                      ></v-empty-state>
                    </div>
                    <DataTable 
                    :value="$resources.consultations.data" 
                    selectionMode="single" 
                    :metaKeySelection="true" 
                    dataKey="id" 
                    @row-click="consultationSelect"
                    class="max-h-72 overflow-y-auto"
                    >
                      <Column headerStyle="width:3rem">
                        <template #body="slotProps">
                          {{ slotProps.index + 1 }}
                        </template>
                      </Column>
                      <Column field="creation">
                        <template #body="slotProps">
                          {{ formatDate(slotProps.data.creation) }}
                        </template>
                      </Column>
                      <Column field="medical_department"></Column>
                      <Column field="practitioner_name"></Column>
                      <Column field="custom_appointment_category"></Column>
                    </DataTable>
                  </template>
                </v-card>
              </v-col>
              <v-col cols="12" md="6">
                <v-card id="clinical-procedure" variant="tonal" color="amber">
                  <template v-slot:title>Procedures ({{ $resources.procedures.data.length }})</template>
                  <template v-slot:text>
                    <div :class="{'d-none': $resources.procedures.data.length > 0}">
                      <v-empty-state
                        title="No Clinical Procedures"
                      ></v-empty-state>
                    </div>
                    <DataTable 
                    :value="$resources.procedures.data" 
                    selectionMode="single" 
                    :metaKeySelection="true" 
                    dataKey="id" 
                    @row-click="consultationSelect"
                    class="max-h-72 overflow-y-auto"
                    >
                      <Column headerStyle="width:3rem">
                        <template #body="slotProps">
                          {{ slotProps.index + 1 }}
                        </template>
                      </Column>
                      <Column field="creation">
                        <template #body="slotProps">
                          {{ formatDate(slotProps.data.creation) }}
                        </template>
                      </Column>
                      <Column field="medical_department"></Column>
                      <Column field="practitioner_name"></Column>
                    </DataTable>
                  </template>
                </v-card>
              </v-col>
            </v-row>
          </v-container>
        </v-window-item>
      </v-window>
    </div>
    <!-- Page Content -->
    <vitalSignsDialog 
    :isOpen="vsDialogOpen" 
    @update:isOpen="vsDialogOpen = $event" 
    @show-alert="showAlert" 
    :vitalSigns="selectedVitalSigns"
    />
    <v-overlay :model-value="loadingOverlay" class="align-center justify-center">
      <v-progress-circular color="primary" size="64" indeterminate></v-progress-circular>
    </v-overlay>
  </div>
</template>
  
<script >
import { ref, reactive } from 'vue';
import dayjs from 'dayjs';
import EditableTable from '@/components/editableTable.vue';
import {VTab, VTabs} from 'vuetify/components/VTabs';
import {VWindow, VWindowItem} from 'vuetify/components/VWindow';
import { VEmptyState } from 'vuetify/labs/VEmptyState';

export default {
  inject: ['$socket', '$call'],
  components: {
    VTabs, VTab, VWindow, VWindowItem, VEmptyState,
  },
  resources: {
    genders() { return { type: 'list', doctype: 'Gender', fields: ['gender'], auto: true } },
    inpatientRecords() { return { type: 'list', doctype: 'Inpatient Record', fields: ['name'], auto: true } },
    vitalSigns() { return { 
      type: 'list', 
      doctype: 'Vital Signs', 
      fields: ['*'], 
      filters: {patient: this.$route.params.patientId},
      auto: true,
      orderBy: 'signs_date desc'
    }},
    consultations() { return { 
      type: 'list', 
      doctype: 'Patient Encounter', 
      fields: ['name', 'creation', 'medical_department', 'practitioner_name', 'custom_appointment_category'], 
      filters: {patient: this.$route.params.patientId, custom_appointment_category: ['not in', 'Procedure', 'Session']},
      auto: true,
      orderBy: 'creation desc'
    }},
    procedures() { return { 
      type: 'list', 
      doctype: 'Clinical Procedure', 
      fields: ['*'], 
      filters: {patient: this.$route.params.patientId},
      auto: true,
      orderBy: 'start_date desc'
    }},
  },
  data() {
    return {
      alertVisible: false,
      loadingOverlay: false,
      tab: null,
      form: ref({}),
      allergies: [],
      infectedDiseases: [],
      surgicalHistory: [],
      medications: [],
      habits: [],
      riskFactors: [],
      profileRangeFilter: null,
      vsDialogOpen: false,
      selectedVitalSigns: {},
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
    updateFullName() {
      this.form.patient_name = (this.form.first_name ? this.form.first_name : '' ) + 
      (this.form.middle_name ? ' ' + this.form.middle_name : '') + 
      (this.form.last_name ? ' ' + this.form.last_name : '')
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
    },
    vitalSignSelect({data}) {
      this.selectedVitalSigns = {...data}
      this.selectedVitalSigns.signs_date = dayjs(data.signs_date)
      this.selectedVitalSigns.signs_time = dayjs(data.signs_date + ' ' + data.signs_time)
      this.vsDialogOpen = true
    },
    consultationSelect({data}) {
      this.$router.push({ name: 'patient-encounter', params: { encounterId: data.name } });
    },
    formatDate(date) {
      return dayjs(date).format('hh:mm A MMM DD, YYYY')
    },
    vitalSigns(row) {
      let vitals = ''
      if(row.temperature)
        vitals += 'temperature, '
      if(row.pulse)
        vitals += 'pulse, '
      if(row.respiratory_rate)
        vitals += 'respiratory rate, '
      if(row.bp)
        vitals += 'bood pressure, '
      if(row.height)
        vitals += 'height, '
      if(row.weight)
        vitals += 'weight, '
      return vitals.slice(0, -2)
    },
  },
  name: 'Patients List',
};
</script>
  
<style>
/* Hide the ListSelectBanner */
.editable-table .absolute.inset-x-0.bottom-6.mx-auto.w-max.text-base {
  display: none !important;
}

.patient-profile td{
  border: 0 !important;
}
</style>  