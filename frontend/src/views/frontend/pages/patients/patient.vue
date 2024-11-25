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
        <v-btn v-if="tab == 'details' || tab == 'insurance'" class="ml-auto text-none" color="purple" variant="outlined" @click="save">save</v-btn>
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
                    <LinkField 
                    doctype="Gender" 
                    :value="form.sex" 
                    @change="(data) => { form.sex = data }"
                    />
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
                  <LinkField 
                    doctype="Inpatient Record" 
                    :value="form.inpatient_record" 
                    @change="(data) => { form.inpatient_record = data }"
                    />
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
                    <LinkField 
                    doctype="Customer" 
                    :filters="{customer_group: 'Medical Insurance', disabled: 0}"
                    :value="form.custom_insurance_company_name" 
                    @change="(data) => { form.custom_insurance_company_name = data }"
                    />
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
                        <a-select
                        v-model:value="row.name1"
                        :options="$resources.medicalHistories.data?.options"
                        :fieldNames="{label: 'medical_history_name', value: 'name'}"
                        style="width: 100%;"
                        show-search
                        :loading="$resources.medicalHistories.list.loading"
                        @search="(value) => {handleSearch(
                          value, 
                          $resources.medicalHistories, 
                          {medical_history_name: ['like', `%${value}%`]}, 
                          {},
                        )}"
                        :filterOption="false"
                        >
                          <template #dropdownRender="{ menuNode: menu }">
                            <v-nodes :vnodes="menu" />
                            <!-- <a-divider style="margin: 4px 0" />
                            <a-space style="padding: 4px 8px">
                              <a-input ref="inputRef" v-model:value="newMedicalHistory" placeholder="Please enter a medical History name" />
                              <a-button type="text" @click="() => {
                                addDoc({doctype: 'Medical History', medical_history_name: newMedicalHistory}, doc => {
                                  newMedicalHistory = ''
                                  $resources.medicalHistories.reload()
                                  row.name1 = doc.name
                                }); 
                              }">
                                <template #icon>
                                  <i class="mdi mdi-plus"></i>
                                </template>
                                Add Medical History
                              </a-button>
                            </a-space> -->
                          </template>
                        </a-select>
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
            <!-- <v-divider class="m-10"></v-divider> -->
            <!-- <a-form layout="vertical"> -->
            <v-row>
              <v-col cols="12" lg="6">
                <h5>Family History</h5>
                <EditableTable :columns="[
                  {label: 'Name', key: 'name1'},
                  {label: 'Note', key: 'note', width: '320px'},
                ]"
                :rows="children.custom_family_history"
                @update="(items, row, isNew) => {
                  if(items && row)
                    newChildRow({
                      fieldName: 'custom_family_history', 
                      rules: {},
                      items, row, isNew
                    })
                }"
                @delete="rows => {deleteChildRow({fieldName: 'custom_family_history', rows})}"
                title="Family History"
                >
                  <template v-slot:dialog="{ row }">
                    <a-form layout="vertical">
                      <a-form-item label="Name">
                        <a-select
                        v-model:value="row.name1"
                        :options="$resources.medicalHistories.data?.options"
                        :fieldNames="{label: 'medical_history_name', value: 'name'}"
                        style="width: 100%;"
                        show-search
                        :loading="$resources.medicalHistories.list.loading"
                        @search="(value) => {handleSearch(
                          value, 
                          $resources.medicalHistories, 
                          {medical_history_name: ['like', `%${value}%`]}, 
                          {},
                        )}"
                        :filterOption="false"
                        >
                          <template #dropdownRender="{ menuNode: menu }">
                            <v-nodes :vnodes="menu" />
                            <!-- <a-divider style="margin: 4px 0" />
                            <a-space style="padding: 4px 8px">
                              <a-input ref="inputRef" v-model:value="newMedicalHistory" placeholder="Please enter a medical History name" />
                              <a-button type="text" @click="() => {
                                addDoc({doctype: 'Medical History', medical_history_name: newMedicalHistory}, doc => {
                                  newMedicalHistory = ''
                                  $resources.medicalHistories.reload()
                                  row.name1 = doc.name
                                }); 
                              }">
                                <template #icon>
                                  <i class="mdi mdi-plus"></i>
                                </template>
                                Add Medical History
                              </a-button>
                            </a-space> -->
                          </template>
                        </a-select>
                      </a-form-item>
                      <a-form-item label="Note">
                        <a-textarea v-model:value="row.note" :rows="4" />
                      </a-form-item>
                    </a-form>
                  </template>
                </EditableTable>
              </v-col>
              <!-- <v-col cols="12" lg="6">
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
              </v-col> -->
            </v-row>
            <v-divider></v-divider>
            <!-- </a-form> -->
          </v-container>
        </v-window-item>
        <v-window-item value="records">
          <v-container fluid>
            <v-row>
              <v-col cols="12" md="6" lg="3">
                <a-range-picker v-model:value="profileRangeFilter" format="DD/MM/YYYY" class="w-full" @change="setDateFilter"/>
              </v-col>
            </v-row>
            <v-row>
              <v-col cols="12" md="6">
                <v-card id="appointments" variant="tonal" color="light-blue-darken-1">
                  <template v-slot:title>Appointments ({{ $resources.appointments.data?.length || '0' }})</template>
                  <template v-slot:text>
                    <DataTable 
                    :value="$resources.appointments.data" 
                    selectionMode="single" 
                    :metaKeySelection="true" 
                    @row-click="({data}) => {appointmentDialog('Edit Appointment', false, data)}"
                    dataKey="id" 
                    class="max-h-72 overflow-y-auto"
                    :loading="appointmentsLoading"
                    >
                      <template #empty><v-empty-state title="No Appointments"></v-empty-state></template>
                      <Column header="#">
                        <template #body="slotProps">
                          {{ slotProps.index + 1 }}
                        </template>
                      </Column>
                      <Column header="Time" field="appointment_time">
                        <template #body="{ data }">
                          <div>
                            <div>
                              {{ data.appointment_date_moment }}
                            </div>
                            <div>
                              {{ data.appointment_time_moment }}
                            </div>
                          </div>
                        </template>
                      </Column>
                      <Column header="Confirmed?" field="custom_confirmed">
                        <template #body="{ data }">
                          <div class="text-center">
                            <i v-if="data.custom_confirmed" class="mdi mdi-check"/>
                            <!-- <i v-else class="mdi mdi-close"/> -->
                          </div>
                        </template>
                      </Column>
                      <Column field="appointment_datetime" hidden></Column>
                      <Column header="Status" field="custom_visit_status"></Column>
                      <Column header="Practitioner" field="practitioner_name">
                        <template #body="{ data }">
                          <div class="flex align-items-center gap-2" v-if="data.practitioner_name">
                            <v-avatar v-if="data.practitioner_image">
                              <img
                              class="h-100 w-100"
                              :src="data.practitioner_image"
                              />
                            </v-avatar>
                            <span>{{ data.practitioner_name }}</span>
                          </div>
                        </template>
                      </Column>
                      <Column header="Type">
                        <template #body="{ data }">
                          <div>
                            <div>
                              {{ data.custom_appointment_category }}
                            </div>
                            <div v-if="data.custom_appointment_category == 'Procedure'">
                              <div v-if="data.procedure_templates.length > 0">
                                <v-chip v-for="(procedure, index) in data.procedure_templates" :key="index" class="mr-1" label size="small">{{ procedure.template }}</v-chip>
                              </div>
                              <div v-else>
                                {{ data.notes }}
                              </div>
                            </div>
                          </div>
                        </template>
                      </Column>
                      <Column header="Paid Amount" field="paid_amount">
                        <template #body="{ data }">
                          BD {{ data.paid_amount }}
                        </template>
                      </Column>
                    </DataTable>
                  </template>
                </v-card>
              </v-col>
              <v-col cols="12" md="6">
                <v-card id="consultations" variant="tonal" color="amber-darken-2">
                  <template v-slot:title>Consultations ({{ $resources.consultations.data?.length || '0' }})</template>
                  <template v-slot:text>
                    <DataTable 
                    :value="$resources.consultations.data" 
                    selectionMode="single" 
                    :metaKeySelection="true" 
                    dataKey="id" 
                    @row-click="({data}) => {encounterSelect(data.name)}"
                    class="max-h-72 overflow-y-auto"
                    :loading="consultationsLoading"
                    >
                      <template #empty><v-empty-state title="No Consultations"></v-empty-state></template>
                      <Column header="#">
                        <template #body="slotProps">
                          {{ slotProps.index + 1 }}
                        </template>
                      </Column>
                      <Column header="Date">
                        <template #body="{ data }">
                          {{ formatDate(data.encounter_date) }}
                        </template>
                      </Column>
                      <Column header="Practitioner" field="practitioner_name"></Column>
                      <Column header="Type" field="custom_appointment_category"></Column>
                      <Column header="Status">
                        <template #body="{ data }">
                          {{ data.status || 'Draft' }}
                        </template>
                      </Column>
                    </DataTable>
                  </template>
                </v-card>
              </v-col>
              <v-col cols="12" md="6">
                <v-card id="clinical-procedure" variant="tonal" color="purple">
                  <template v-slot:title>Procedures ({{ $resources.procedures.data?.length || '0' }})</template>
                  <template v-slot:text>
                    <DataTable 
                    :value="$resources.procedures.data" 
                    selectionMode="single" 
                    :metaKeySelection="true" 
                    dataKey="id" 
                    @row-click="({data}) => {encounterSelect(data.custom_patient_encounter)}"
                    class="max-h-72 overflow-y-auto"
                    :loading="proceduresLoading"
                    >
                      <template #empty><v-empty-state title="No Clinical Procedures"></v-empty-state></template>
                      <Column header="#">
                        <template #body="slotProps">
                          {{ slotProps.index + 1 }}
                        </template>
                      </Column>
                      <Column header="Start Date">
                        <template #body="{ data }">
                          {{ formatDate(data.start_date) }}
                        </template>
                      </Column>
                      <Column header="Practitioner" field="practitioner_name"></Column>
                      <Column header="Procedure" field="procedure_template"></Column>
                      <Column header="Status">
                        <template #body="{ data }">
                          {{ data.status || 'Draft' }}
                        </template>
                      </Column>
                    </DataTable>
                  </template>
                </v-card>
              </v-col>
              <v-col cols="12" md="6">
                <v-card id="vital-signs" variant="tonal" color="green-accent-4">
                  <template v-slot:title>Vital Signs ({{ $resources.vitalSigns.data?.length || '0' }})</template>
                  <template v-slot:text>
                    <DataTable 
                    :value="$resources.vitalSigns.data" 
                    selectionMode="single" 
                    :metaKeySelection="true" 
                    dataKey="id" 
                    @row-click="vitalSignSelect"
                    class="max-h-72 overflow-y-auto"
                    :loading="vitalSignsLoading"
                    >
                      <template #empty><v-empty-state title="No Vital Signs"></v-empty-state></template>
                      <Column header="#">
                        <template #body="slotProps">
                          {{ slotProps.index + 1 }}
                        </template>
                      </Column>
                      <Column header="Date">
                        <template #body="slotProps">
                          {{ formatDate(slotProps.data.signs_date + ' ' + slotProps.data.signs_time) }}
                        </template>
                      </Column>
                      <Column header="Vital Signs taken" style="width:100%">
                        <template #body="slotProps">
                          {{ vitalSigns(slotProps.data) }}
                        </template>
                      </Column>
                      <Column header="Status">
                        <template #body="{ data }">
                          {{ data.docstatus == 1 ? 'Submitted' : data.docstatus == 0 ? 'Draft' : 'Cancelled' }}
                        </template>
                      </Column>
                    </DataTable>
                  </template>
                </v-card>
              </v-col>
              <v-col cols="12" md="6">
                <v-card id="vital-signs" variant="tonal" color="brown">
                  <template v-slot:title>Invoices ({{ $resources.invoices.data?.length || '0' }})</template>
                  <template v-slot:text>
                    <DataTable 
                    :value="$resources.invoices.data" 
                    selectionMode="single" 
                    :metaKeySelection="true" 
                    dataKey="id" 
                    @row-click="invoiceSelect"
                    class="max-h-72 overflow-y-auto"
                    :loading="invoicesLoading"
                    >
                      <template #empty><v-empty-state title="No invoices"></v-empty-state></template>
                      <Column header="#">
                        <template #body="slotProps">
                          {{ slotProps.index + 1 }}
                        </template>
                      </Column>
                      <Column header="Date">
                        <template #body="{ data }">
                          {{ formatDate(data.posting_date) }}
                        </template>
                      </Column>
                      <Column header="Total Amount" field="grand_total"></Column>
                      <Column header="Paid Amount" field="paid_amount"></Column>
                      <Column header="Services" field="services"></Column>
                      <Column header="Status" field="status"></Column>
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
    <patientAppointmentDialog 
    :isOpen="appointmentOpen" 
    @update:isOpen="appointmentOpen = $event" 
    @show-alert="showAlert" 
    :form="appointmentForm"
    :adjustAppointments="adjustAppointments"
    />
    <v-overlay :model-value="loadingOverlay" class="align-center justify-center">
      <v-progress-circular color="primary" size="64" indeterminate></v-progress-circular>
    </v-overlay>
  </div>
</template>
  
<script >
import { ref, defineComponent } from 'vue';
import dayjs from 'dayjs';
import EditableTable from '@/components/editableTable.vue';
import {VTab, VTabs} from 'vuetify/components/VTabs';
import {VWindow, VWindowItem} from 'vuetify/components/VWindow';
import { VEmptyState } from 'vuetify/labs/VEmptyState';
import { Form } from 'ant-design-vue';
import { VAvatar, VChip } from 'vuetify/components';

export default {
  inject: ['$socket', '$call'],
  components: {
    VTabs, VTab, VWindow, VWindowItem, VEmptyState, VChip, VAvatar,
    VNodes: defineComponent({
      props: {
        vnodes: {
          type: Object,
          required: true,
        },
      },
      render() {
        return this.vnodes;
      },
    }),
  },
  resources: {
    medicalHistories() { return { 
      type: 'list', 
      doctype: 'Medical History', 
      fields: ['name', 'medical_history_name'], 
      auto: true, 
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
    vitalSigns() { return { 
      type: 'list', 
      doctype: 'Vital Signs', 
      fields: ['name', 'temperature', 'signs_date', 'signs_time','pulse', 'respiratory_rate', 'custom_saturation_rate', 'bp', 'height', 'weight', 'docstatus'], 
      filters: {patient: this.$route.params.patientId, ...(this.profileRangeFilter ? {signs_date: ['between', [this.startDate, this.endDate]]} : {})},
      auto: true,
      orderBy: 'signs_date desc',
      pageLength: 1000,
      onSuccess(data) {
        this.vitalSignsLoading = false
      },
    }},
    appointments() { return { 
      type: 'list', 
      doctype: 'Patient Appointment', 
      fields: ['*'], 
      filters: {patient: this.$route.params.patientId, ...(this.profileRangeFilter ? {appointment_date: ['between', [this.startDate, this.endDate]]} : {})},
      auto: true,
      orderBy: 'appointment_date desc',
      url:'healthcare_doworks.api.methods.check_availability',
      pageLength: 1000,
      transform(data) {
        return this.adjustAppointments(data)
      },
      onSuccess(data) {
        this.appointmentsLoading = false
      },
    }},
    consultations() { return { 
      type: 'list', 
      doctype: 'Patient Encounter', 
      fields: ['name', 'encounter_date', 'practitioner_name', 'custom_appointment_category', 'status'], 
      filters: {
        patient: this.$route.params.patientId, 
        custom_appointment_category: ['!=', 'Procedure'], 
        ...(this.profileRangeFilter ? {encounter_date: ['between', [this.startDate, this.endDate]]} : {})
      },
      auto: true,
      orderBy: 'encounter_date desc',
      pageLength: 1000,
      onSuccess(data) {
        this.consultationsLoading = false
      },
    }},
    procedures() { return { 
      type: 'list', 
      doctype: 'Clinical Procedure', 
      fields: ['name', 'start_date', 'practitioner_name', 'procedure_template', 'custom_patient_encounter', 'status'], 
      filters: {patient: this.$route.params.patientId, ...(this.profileRangeFilter ? {start_date: ['between', [this.startDate, this.endDate]]} : {})},
      auto: true,
      orderBy: 'start_date desc',
      pageLength: 1000,
      onSuccess(data) {
        this.proceduresLoading = false
      },
    }},
    invoices() { return { 
      type: 'list', 
      doctype: 'Sales Invoice', 
      filters: {customer: this.$route.params.patientId, ...(this.profileRangeFilter ? {posting_date: ['between', [this.startDate, this.endDate]]} : {})},
      auto: false,
      orderBy: 'posting_date desc',
      pageLength: 1000,
      url:'healthcare_doworks.api.methods.invoices',
      onSuccess(data) {
        this.invoicesLoading = false
      },
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
        custom_family_history: [],
        custom_medications: [],
        custom_risk_factors_table: [],
        custom_surgical_history_table: [],
        patient_relation: [],
      },
      profileRangeFilter: null,
      vsDialogOpen: false,
      appointmentOpen: false,
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
      startDate: null,
      endDate: null,
      appointmentForm: {},

      vitalSignsLoading: true,
      appointmentsLoading: true,
      consultationsLoading: true,
      proceduresLoading: true,
      invoicesLoading: true,

      newMedicalHistory: '',
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
        let invoicesFilters = {...this.$resources.invoices.filters}
        invoicesFilters.customer = response.doc.customer
        this.$resources.invoices.update({filters: invoicesFilters});
        this.$resources.invoices.reload()

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
    setDateFilter(date) {
      if(date){
        this.startDate = date[0].format('YYYY-MM-DD')
        this.endDate = date[1].format('YYYY-MM-DD')

        this.$resources.appointments.reload()
        this.$resources.consultations.reload()
        this.$resources.procedures.reload()
        this.$resources.vitalSigns.reload()
        this.$resources.invoices.reload()
      }
      this.appointmentsLoading = true
      this.consultationsLoading = true
      this.proceduresLoading = true
      this.vitalSignsLoading = true
      this.invoicesLoading = true
    },
    updateFullName() {
      this.form.patient_name = (this.form.first_name ? this.form.first_name : '' ) + 
      (this.form.middle_name ? ' ' + this.form.middle_name : '') + 
      (this.form.last_name ? ' ' + this.form.last_name : '')
    },
    addDoc(form, callback){
      this.$call('healthcare_doworks.api.methods.new_doc', {form})
      .then(response => {
        callback(response)
        this.$toast.add({ severity: 'success', summary: 'Success', detail: `New ${response.doctype} created`, life: 3000 });
      }).catch(error => {
        this.showAlert(error.message, 'error')
      });
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
    invoiceSelect({data}) { 
      window.open(`/app/sales-invoice/${data.name}`) 
    },
    formatDate(date) {
      return dayjs(date).format('DD/MM/YYYY')
    },
    adjustAppointments(data) {
			return [...(data || [])].map((d) => {
        d.visit_notes = d.visit_notes?.map(note => {
          note.dayDate = dayjs(note.time).format('DD/MM/YYYY')
          note.dayTime = dayjs(note.time).format('h:mm A')
          return note
        })
        d.arriveTime = '-'
        d.status_log?.forEach(value => {
          value.timeFormat = dayjs(value.time).format('h:mm a    D/MM/YYYY')
          if(value.status == 'Arrived')
            d.arriveTime = dayjs(value.time)
        })
        d.appointment_date_moment = dayjs(d.appointment_date + ' ' + d.appointment_time).format('D/MM/YYYY');
				d.appointment_time_moment = dayjs(d.appointment_date + ' ' + d.appointment_time).format('h:mm a');
				d.patient_cpr = d.patient_name + ' ' + d.patient_details?.cpr

				return d;
			});
    },
    vitalSigns(row) {
      let vitals = ''
      if(row.temperature)
        vitals += 'temperature, '
      if(row.pulse)
        vitals += 'pulse, '
      if(row.respiratory_rate)
        vitals += 'respiratory rate, '
      if(row.custom_saturation_rate)
        vitals += 'saturation rate, '
      if(row.bp)
        vitals += 'bood pressure, '
      if(row.height)
        vitals += 'height, '
      if(row.weight)
        vitals += 'weight, '
      return vitals.slice(0, -2)
    },
    save() {
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
            this.save()
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
            this.save()
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
          this.save()
          this.lodingOverlay = false;
        }).catch(error => {
          this.showAlert(error.message, 'error')
        })
        .catch(err => {
          console.log('error', err);
        });
      })
    },
    appointmentDialog(formType, isNew, row) {
      this.appointmentForm.name = row.name;
      this.appointmentForm.duration = row.duration;
      this.appointmentForm.appointment_type = row.appointment_type;
      this.appointmentForm.appointment_for = row.appointment_for;
      this.appointmentForm.custom_appointment_category = row.custom_appointment_category;
      this.appointmentForm.custom_branch = row.custom_branch;
      this.appointmentForm.procedure_templates = row.procedure_templates;
      this.appointmentForm.custom_payment_type = row.custom_payment_type;
      this.appointmentForm.custom_confirmed = row.custom_confirmed;
      this.appointmentForm.practitioner = row.practitioner;
      this.appointmentForm.practitioner_name = row.practitioner_name;
      this.appointmentForm.patient = row.patient_details.id;
      this.appointmentForm.patient_name = row.patient_name;
      this.appointmentForm.patient_sex = row.patient_details.gender;
      this.appointmentForm.patient_mobile = row.patient_details.mobile;
      this.appointmentForm.patient_age = row.patient_details.age;
      this.appointmentForm.department = row.department;
      this.appointmentForm.service_unit = row.service_unit;
      this.appointmentForm.notes = row.notes;
      this.appointmentForm.appointment_date = dayjs(row.appointment_date)
      this.appointmentForm.appointment_time = row.appointment_time;

      this.appointmentForm.doctype = 'Patient Appointment';
      // this.appointmentForm.appointment_date = this.appointmentForm.appointment_time = undefined;
			this.appointmentForm.type = formType
      this.appointmentForm.custom_is_walked_in = false;
			this.appointmentOpen = true
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