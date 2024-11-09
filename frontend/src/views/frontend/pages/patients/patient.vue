<template>
  <!-- Main Wrapper -->
  <div class="patient-profile main-wrapper mr-3 h-full overflow-hidden">
    <v-alert
      v-if="alertActive && alertType === 'error'"
      type="error"
      position="fixed"
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
    <div class="card p-4 m-4" style="height: calc(100% - 50px);">
      <div class="flex">
        <v-tabs
        v-model="tab"
        color="deep-purple-accent-4"
        >
          <v-tab value="details">Details</v-tab>
          <v-tab value="insurance">Insurance</v-tab>
          <v-tab v-if="!isNew" value="medicalHestory">Medical History</v-tab>
          <v-tab v-if="!isNew" value="records">Medical Records</v-tab>
        </v-tabs>
        <v-btn v-if="tab == 'details' || tab == 'insurance'" class="ml-auto text-none" color="purple" variant="outlined" @click="saveNew">save</v-btn>
      </div>

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
                    <a-input v-model:value="form.last_name" @change="updateFullName" />
                  </a-form-item>
                  <a-form-item label="Full Name" name="patient_name" >
                    <a-input v-model:value="form.patient_name" disabled/>
                  </a-form-item>
                  <a-form-item label="CPR" name="custom_cpr" >
                    <a-input v-model:value="form.custom_cpr" />
                  </a-form-item>
                  <a-form-item label="Gender" name="sex">
                    <a-select 
                    v-model:value="form.sex" 
                    :options="$resources.genders.data?.options" 
                    :fieldNames="{label: 'gender', value: 'gender'}"
                    allowClear
                    show-search
                    :loading="$resources.genders.list.loading"
                    @search="(value) => {handleSearch(
                      value, 
                      $resources.genders, 
                      {gender: ['like', `%${value}%`]}, 
                      {},
                    )}"
                    :filterOption="false"
                    ></a-select>
                  </a-form-item>
                  <a-form-item label="Blood Group" name="blood_group">
                    <a-select 
                    v-model:value="form.blood_group" 
                    :options="bloodGroupOptions"
                    ></a-select>
                  </a-form-item>
                  <a-form-item label="Date of birth" name="dob">
                    <a-date-picker 
                    v-model:value="form.dob" 
                    format="DD/MM/YYYY" 
                    class="w-full" 
                    @change="(date, dateString) => {
                      age = getAge(date)
                      const day = dateString.split('/')[0]
                      const month = dateString.split('/')[1]
                      const year = dateString.split('/')[2]
                    }"
                    />
                  </a-form-item>
                  <h6>Age: {{ age }}</h6>
                </v-col>
                <v-col cols="12" md="6">
                  <a-form-item label="Status" name="Status" >
                    <a-input v-model:value="form.status" defaultValue="Active" disabled/>
                  </a-form-item>
                  <a-form-item label="File Number" name="custom_file_number">
                    <a-input v-model:value="form.custom_file_number" />
                  </a-form-item>
                  <a-form-item label="Inpatient Record" name="inpatient_record" >
                    <a-select 
                    v-model:value="form.inpatient_record" 
                    :options="$resources.inpatientRecords.data?.options" 
                    :fieldNames="{label: 'name', value: 'name'}"
                    allowClear
                    show-search
                    :loading="$resources.inpatientRecords.list.loading"
                    @search="(value) => {handleSearch(
                      value, 
                      $resources.inpatientRecords, 
                      {name: ['like', `%${value}%`]}, 
                      {},
                    )}"
                    :filterOption="false"
                    >
                  </a-select>
                  </a-form-item>
                  <a-form-item label="Inpatient Status" name="inpatient_status">
                    <a-select 
                    v-model:value="form.inpatient_status" 
                    :options="inpatientStatusOptions"
                    ></a-select>
                  </a-form-item>
                  <a-form-item label="Report Preference" name="report_preference">
                    <a-select 
                    v-model:value="form.report_preference" 
                    :options="reportPreferenceOptions"
                    ></a-select>
                  </a-form-item>
                  <a-form-item label="Mobile" name="mobile">
                    <a-input v-model:value="form.mobile" />
                  </a-form-item>
                  <a-form-item label="Phone" name="phone">
                    <a-input v-model:value="form.phone" />
                  </a-form-item>
                  <a-form-item label="Email" name="email">
                    <a-input v-model:value="form.email" />
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
                    <a-textarea 
                    v-model:value="form.patient_details" 
                    :rows="14" 
                    />
                  </a-form-item>
                </v-col>
                <v-col cols="12" md="6">
                  <a-form-item 
                  label="Default Payment Type" 
                  name="custom_default_payment_type" 
                  >
                    <a-select 
                    v-model:value="form.custom_default_payment_type" 
                    :options="[{label: 'Self Payment', value: 'Self Payment'}, {label: 'Insurance', value: 'Insurance'}]"
                    ></a-select>
                  </a-form-item>
                  <a-form-item 
                  label="Medical History Last Updated" 
                  name="custom_medical_history_last_updated" 
                  >
                    <a-date-picker 
                    v-model:value="form.custom_medical_history_last_updated" 
                    format="DD/MM/YYYY" 
                    class="w-full" 
                    />
                  </a-form-item>
                </v-col>
              </v-row>
            </v-container>
          </a-form>
        </v-window-item>
        <v-window-item value="insurance">
          <a-form layout="vertical" :model="form">
            <v-container fluid>
              <v-row>
                <v-col cols="12">
                  <a-checkbox class="mb-3" v-model:checked="form.custom_active">Active</a-checkbox>
                  <a-form-item label="Insurance Company Name">
                    <a-select
                    v-model:value="form.custom_insurance_company_name"
                    style="width: 100%;"
                    :options="$resources.customers.data?.options"
                    :fieldNames="{label:'customer_name', value: 'name'}"
                    show-search
                    :loading="$resources.customers.list.loading"
                    @search="(value) => {handleSearch(
                      value, 
                      $resources.customers, 
                      {customer_group: 'Medical Insurance', disabled: 0, customer_name: ['like', `%${value}%`]}, 
                      {customer_group: 'Medical Insurance', disabled: 0},
                    )}"
                    :filterOption="false"
                    >
                    </a-select>
                  </a-form-item>
                  <a-form-item label="Policy Number">
                    <a-input v-model:value="form.custom_policy_number"/>
                  </a-form-item>
                  <a-form-item label="Expiration Date">
                    <a-date-picker 
                    v-model:value="form.custom_expiration_date"
                    format="DD MMM YYYY" 
                    style="width: 100%"
                    />
                  </a-form-item>
                  <a-form-item label="Copay Amount">
                    <a-input-number class="w-full" :controls="false" v-model:value="form.custom_copay_amount"/>
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
                :rows="children.custom_allergies_table"
                @update="(items, row, isNew) => {
                  if(items && row)
                    newChildRow({
                      fieldName: 'custom_allergies_table', 
                      rules: {},
                      items, row, isNew
                    })
                }"
                @delete="rows => {deleteChildRow({fieldName: 'custom_allergies_table', rows})}"
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
                      <a-form-item label="Severity">
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
                <h5>Medical History</h5>
                <EditableTable :columns="[
                  {label: 'Name', key: 'name1'},
                  {label: 'Note', key: 'note', width: '320px'},
                ]"
                :rows="children.custom_infected_diseases"
                @update="(items, row, isNew) => {
                  if(items && row)
                    newChildRow({
                      fieldName: 'custom_infected_diseases', 
                      rules: {},
                      items, row, isNew
                    })
                }"
                @delete="rows => {deleteChildRow({fieldName: 'custom_infected_diseases', rows})}"
                title="Medical History"
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
                :rows="children.custom_surgical_history_table"
                @update="(items, row, isNew) => {
                  if(items && row)
                    newChildRow({
                      fieldName: 'custom_surgical_history_table', 
                      rules: {},
                      items, row, isNew
                    })
                }"
                @delete="rows => {deleteChildRow({fieldName: 'custom_surgical_history_table', rows})}"
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
                        <a-textarea v-model:value="row.notes" :rows="4" />
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
                :rows="children.custom_medications"
                @update="(items, row, isNew) => {
                  if(items && row)
                    newChildRow({
                      fieldName: 'custom_medications', 
                      rules: {},
                      items, row, isNew
                    })
                }"
                @delete="rows => {deleteChildRow({fieldName: 'custom_medications', rows})}"
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
                :rows="children.custom_habits__social"
                @update="(items, row, isNew) => {
                  if(items && row)
                    newChildRow({
                      fieldName: 'custom_habits__social', 
                      rules: {},
                      items, row, isNew
                    })
                }"
                @delete="rows => {deleteChildRow({fieldName: 'custom_habits__social', rows})}"
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
                :rows="children.custom_risk_factors_table"
                @update="(items, row, isNew) => {
                  if(items && row)
                    newChildRow({
                      fieldName: 'custom_risk_factors_table', 
                      rules: {},
                      items, row, isNew
                    })
                }"
                @delete="rows => {deleteChildRow({fieldName: 'custom_risk_factors_table', rows})}"
                title="Risk Factors"
                >
                  <template v-slot:dialog="{ row }">
                    <a-form layout="vertical">
                      <a-form-item label="Type">
                        <a-select
                        v-model:value="row.type"
                        :options="riskFactorsOptions"
                        ></a-select>
                      </a-form-item>
                      <a-form-item label="Severity">
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
            </v-row>
            <v-divider class="m-10"></v-divider>
            <a-form layout="vertical">
              <h5 class="mb-4">Family History</h5>
              <v-row>
                <v-col cols="12" lg="6">
                  <a-form-item label="Chronic Diseases">
                    <a-textarea 
                    v-model:value="form.custom_chronic_diseases" 
                    :rows="4" 
                    />
                  </a-form-item>
                </v-col>
                <v-col cols="12" lg="6">
                  <a-form-item label="Genetic Diseases">
                    <a-textarea 
                    v-model:value="form.custom_genetic_conditions" 
                    :rows="4" 
                    />
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
                    @row-click="({data}) => {encounterSelect(data.name)}"
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
                <v-card id="clinical-procedure" variant="tonal" color="purple">
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
                    @row-click="({data}) => {encounterSelect(data.custom_patient_encounter)}"
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
    :name="selectedVitalSigns?.name"
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
import { Form } from 'ant-design-vue';

export default {
  inject: ['$socket', '$call'],
  components: {
    VTabs, VTab, VWindow, VWindowItem, VEmptyState,
  },
  resources: {
    genders() { return { 
      type: 'list', 
      doctype: 'Gender', 
      fields: ['gender'], 
      auto: true, 
      url: 'frappe.desk.reportview.get', 
      transform(data) {
        if(data.values.length == 0)
          data.options = []
        else
          data.options = this.transformData(data.keys, data.values);  // Transform the result into objects
        return data
      }
    }},
    customers() { return { 
      type: 'list', 
      doctype: 'Customer', 
      fields: ['name', 'customer_name'], 
      filters: {customer_group: 'Medical Insurance', disabled: 0},
      auto: true, 
      orderBy: 'customer_name',
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
    inpatientRecords() { return { 
      type: 'list', 
      doctype: 'Inpatient Record', 
      fields: ['name'], 
      auto: true, 
      url: 'frappe.desk.reportview.get', 
      transform(data) {
        if(data.values.length == 0)
          data.options = []
        else
          data.options = this.transformData(data.keys, data.values);  // Transform the result into objects
        return data
      }
    }},
    vitalSigns() { return { 
      type: 'list', 
      doctype: 'Vital Signs', 
      fields: ['*'], 
      filters: {patient: this.$route.params.patientId},
      auto: true,
      orderBy: 'signs_date desc',
      pageLength: 1000,
    }},
    consultations() { return { 
      type: 'list', 
      doctype: 'Patient Encounter', 
      fields: ['name', 'creation', 'medical_department', 'practitioner_name', 'custom_appointment_category'], 
      filters: {patient: this.$route.params.patientId, custom_appointment_category: ['not in', 'Procedure', 'Session']},
      auto: true,
      orderBy: 'creation desc',
      pageLength: 1000,
    }},
    procedures() { return { 
      type: 'list', 
      doctype: 'Clinical Procedure', 
      fields: ['*'], 
      filters: {patient: this.$route.params.patientId},
      auto: true,
      orderBy: 'start_date desc',
      pageLength: 1000,
    }},
  },
  data() {
    return {
      alertMessage: '',
      alertType: '', // 'success' or 'error'
      alertActive: false,

      loadingOverlay: false,
      isNew: false,
      tab: null,
      age: '',
      form: ref({doctype: 'Patient'}),
      children: {
        custom_allergies_table: [],
        custom_habits__social: [],
        custom_infected_diseases: [],
        custom_medications: [],
        custom_risk_factors_table: [],
        custom_surgical_history_table: [],
        patient_relation: [],
      },
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

      severityOptions: [
        {label: '0', value: '0'},
        {label: '1', value: '1'},
        {label: '2', value: '2'},
        {label: '3', value: '3'},
        {label: '4', value: '4'},
        {label: '5', value: '5'},
      ],
      habitsOptions: [
        {label: 'Smoking', value: 'Smoking'},
        {label: 'Alcohol', value: 'Alcohol'},
        {label: 'Vegetarian', value: 'Vegetarian'},
        {label: 'In Regime', value: 'In Regime'},
        {label: 'Exercise', value: 'Exercise'},
        {label: 'Overweight', value: 'Overweight'},
        {label: 'Other', value: 'Other'},
      ],
      allergiesOptions: [
        {label: 'Food', value: 'Food'},
        {label: 'Medication', value: 'Medication'},
        {label: 'Animal', value: 'Animal'},
        {label: 'Environmental', value: 'Environmental'},
        {label: 'Other', value: 'Other'},
      ],
      riskFactorsOptions: [
        {label: 'Occupation', value: 'Occupation'},
        {label: 'Living Place', value: 'Living Place'},
        {label: 'Others', value: 'Others'},
      ],
    };
  },
  created() {
    if(this.$route.params.patientId == 'new-patient'){
      this.isNew = true
    }
    else{
      this.isNew = false
      this.fetchRecords();
    }
  },
  mounted() {
  },
  methods: {
    showAlert(message, type) {
      this.alertMessage = message;
      this.alertType = type;
      this.alertActive = true;
    },
    fetchRecords() {
      this.loadingOverlay = true;
      this.$call('healthcare_doworks.api.methods.patient', {patient: this.$route.params.patientId})
      .then(response => {
        console.log(response)
        if(response.doc.dob){
          response.doc.dob = dayjs(response.doc.dob)
          this.age = this.getAge(response.doc.dob)
        }
        if(response.doc.custom_expiration_date)
          response.doc.custom_expiration_date = dayjs(response.doc.custom_expiration_date)
        if(response.doc.custom_medical_history_last_updated)
          response.doc.custom_medical_history_last_updated = dayjs(response.doc.custom_medical_history_last_updated)

        this.form = response.doc
        this.children = response.children
        this.loadingOverlay = false;
      })
      .catch(error => {
        this.loadingOverlay = false;
        this.showAlert(error.message, 'error')
        console.error('Error fetching records:', error);
      });
    },
    updateFullName() {
      this.form.patient_name = (this.form.first_name ? this.form.first_name : '' ) + 
      (this.form.middle_name ? ' ' + this.form.middle_name : '') + 
      (this.form.last_name ? ' ' + this.form.last_name : '')
    },
    getAge(birth) {
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
    encounterSelect(encounter) {
      this.$router.push({ name: 'patient-encounter', params: { encounterId: encounter } });
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
    saveNew() {
      let formClone = {...this.form}
      if(formClone.dob)
        formClone.dob = dayjs(this.form.dob).format('YYYY-MM-DD')
      if(formClone.custom_expiration_date)
        formClone.custom_expiration_date = dayjs(this.form.custom_expiration_date).format('YYYY-MM-DD')
      if(formClone.custom_medical_history_last_updated)
        formClone.custom_medical_history_last_updated = dayjs(this.form.custom_medical_history_last_updated).format('YYYY-MM-DD')

      if(this.isNew){
        this.$call('healthcare_doworks.api.methods.new_doc', {form: formClone})
        .then(response => {
          this.isNew = false
          this.$toast.add({
            severity: 'success',
            summary: 'Success',
            detail: 'Patient saved',
            life: 3000 // Duration in ms
          });
          this.$router.push({ name: 'patient', params: { patientId: response.name } });
          this.fetchRecords()
        }).catch(error => {
          this.showAlert(error.message, 'error')
        });
      }
      else{
        delete formClone.owner
        delete formClone.creation
        delete formClone.modified
        delete formClone.modified_by
        this.$call('healthcare_doworks.api.methods.edit_doc', {form: formClone})
        .then(response => {
          this.isNew = false
          this.$toast.add({
            severity: 'success',
            summary: 'Success',
            detail: 'Patient saved',
            life: 3000 // Duration in ms
          });
          this.$router.push({ name: 'patient', params: { patientId: response.name } });
          this.fetchRecords()
        }).catch(error => {
          this.showAlert(error.message, 'error')
        });
      }
    },
    autoSave(doctype, name, fieldname, value) {
      return;

      this.$call('frappe.client.set_value', {doctype, name, fieldname, value})
      .then(response => {
        this.$toast.add({ severity: 'success', summary: 'Saved', life: 2000 });
      }).catch(error => {
        this.showAlert(error.message, 'error')
      });
    },
    newChildRow({parentDoctype ,fieldName, rules, items, row, isNew}) {
      const { validate } = Form.useForm(row, rules);
      validate().then(() => {
        this.lodingOverlay = true;
        let formClone = {...row}
        delete formClone.modified
        delete formClone.modified_by
        delete formClone.name
        if(isNew){
          this.$call('healthcare_doworks.api.general_methods.add_child_entry', {
            parent_doctype: parentDoctype || 'Patient', 
            parent_doc_name: this.form.name, 
            child_table_fieldname: fieldName, 
            child_data: formClone
          }).then(response => {
            this.form.custom_medical_history_last_updated = dayjs()
            this.saveNew()
            this.lodingOverlay = false;
          }).catch(error => {
            this.showAlert(error.message, 'error')
          });
        }
        else{
          this.$call('healthcare_doworks.api.general_methods.modify_child_entry', {
            parent_doctype: parentDoctype || 'Patient', 
            parent_doc_name: this.form.name, 
            child_table_fieldname: fieldName, 
            filters: {name: row.name}, 
            update_data: formClone
          }).then(response => {
            this.form.custom_medical_history_last_updated = dayjs()
            this.saveNew()
            this.lodingOverlay = false;
          }).catch(error => {
            this.showAlert(error.message, 'error')
          });
        }
      })
      .catch(err => {
        console.log('error', err);
      });
    },
    deleteChildRow({parentDoctype, fieldName, rows, filterField}) {
      rows.forEach(row => {
        this.$call('healthcare_doworks.api.general_methods.delete_child_entry', {
          parent_doctype: parentDoctype || 'Patient', 
          parent_doc_name: this.form.name, 
          child_table_fieldname: fieldName, 
          filters: {[filterField || 'name']: row}
        }).then(response => {
          this.form.custom_medical_history_last_updated = dayjs()
          this.saveNew()
          this.lodingOverlay = false;
        }).catch(error => {
          this.showAlert(error.message, 'error')
        })
        .catch(err => {
          console.log('error', err);
        });
      })
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
    handleSearch(query, resource, filters, initialFilters) {
      // Clear the previous timeout to avoid spamming requests
      clearTimeout(this.searchTimeout);

      // Set a new timeout (300ms) for debouncing
      this.searchTimeout = setTimeout(() => {
        if (query) {
          // Update list resource options to fetch matching records from server
          resource.update({filters});

          // Fetch the updated results
          resource.reload();
        } else {
          // If no search query, load initial records
          resource.update({filters: initialFilters});
          resource.reload();
        }
      }, 300);  // Debounce delay of 300ms
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