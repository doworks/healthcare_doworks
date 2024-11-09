<template>
  <!-- Main Wrapper -->
  <div class="main-wrapper mr-4">
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
    <div class="appointment-tab">
      <!-- Clock And Other Filters -->
      <div class="flex-wrap flex-col flex-xxl-row gap-3 nav nav-tabs nav-tabs-solid pb-2">
        <div class="flex flex-wrap flex-col flex-lg-row gap-3 flex-auto order-2 order-xxl-1">
          <div class="flex flex-col" style="width: 17rem">
            <a-select v-if="dateFilterType === 'span'"
            v-model:value="selectedSpan"
            style="width: 100%; align-items: center; max-height: 62px; text-align: center"
            :options="spans"
            size="large"
            @change="(value) => {
              const dates = spanToDate(value)
              selectedDates = dates
              selectedRangeDates = [dates[0], dates[dates.length -1]]
              fetchRecords()
            }"
            ></a-select>
            <a-date-picker v-if="dateFilterType === 'single'"
            v-model:value="selectedDates[0]"
            format="D/M/YY"
            style="width: 100%; align-items: center; max-height: 62px; text-align: center"
            :allowClear="false"
            size="large"
            @change="(value) => {selectedDates = [value]; selectedRangeDates = [value, value]; fetchRecords()}"
            />
            <!-- <span class="d-flex justify-content-center fw-bolder text-dark me-3">{{ formattedDayOfWeek() }}</span> -->
            <a-range-picker v-if="dateFilterType === 'range'" 
            v-model:value="selectedRangeDates" 
            format="D/M/YY" 
            style="width: 100%; align-items: center; max-height: 62px; text-align: center" 
            size="large"
            :allowClear="false"
            @change="(value) => {selectedDates = getDatesInBetween(value[0], value[1]); fetchRecords()}"
            />
            <v-btn-toggle class="mt-1" v-model="dateFilterType" color="blue" mandatory density="compact">
              <v-btn size="small" class="text-none" @click="resetDates" value="span">Timespans</v-btn>
              <v-btn size="small" class="text-none"  value="single">Single</v-btn>
              <v-btn size="small" class="text-none"  value="range">Range</v-btn>
            </v-btn-toggle>
            <!-- <a-radio-group class="mt-2" v-model:value="dateFilterType">
              <a-radio-button value="span">Timespan</a-radio-button>
              <a-radio-button value="single">Single</a-radio-button>
              <a-radio-button value="range">Range</a-radio-button>
            </a-radio-group> -->
          </div>
          <div class="flex flex-col" style="width: 17rem">
            <a-select
            v-model:value="selectedDepartments"
            mode="multiple"
            style="width: 100%; align-items: center; max-height: 62px;"
            placeholder="Departments"
            max-tag-count="responsive"
            :options="$resources.departments.data?.options"
            :fieldNames="{label:'department', value: 'name'}"
            size="large"
            show-search
            :loading="$resources.departments.list.loading"
            @search="(value) => {handleSearch(
              value, 
              $resources.departments, 
              {department: ['like', `%${value}%`]}, 
              {},
            )}"
            :filterOption="false"
            >
            </a-select>
          </div>
          <div class="flex flex-col" style="width: 17rem">
            <a-input v-model:value="searchValue" placeholder="Filters" size="large">
              <template #prefix>
                <v-icon icon="mdi mdi-magnify" color="grey"></v-icon>
              </template>
            </a-input>
          </div>
          <!-- <v-btn class="text-none" elevation="1" @click="() => {
            checkAvailabilityPatient = ''
            checkAvailabilityAppointments = []
            checkAvailabilityOpen = true
          }">
            Check Availability
          </v-btn> -->
        </div>
        <div class="ms-xxl-auto order-1 order-xxl-2 w-fit">
          <Clock/>
        </div>
      </div>
      
      <!-- Toolbar Actions -->
      <v-toolbar color="blue-lighten-5">
        <v-tooltip location="bottom" open-delay="500">
          <template v-slot:activator="{ props }">
            <v-btn icon="mdi mdi-plus" v-bind="props" @click="appointmentDialog('New Appointment', true)" rounded="0"></v-btn>
          </template>
          Add a new appointment
        </v-tooltip>
        <v-tooltip location="bottom" open-delay="500">
          <template v-slot:activator="{ props }">
            <v-btn icon="mdi mdi-magnify" rounded="0" v-bind="props" @click="() => {
              checkAvailabilityPatient = ''
              checkAvailabilityAppointments = []
              checkAvailabilityOpen = true
            }"></v-btn>
          </template>
          Check appointment logs for a patient
        </v-tooltip>
      </v-toolbar>

      <!-- Appointment Tab -->
      <v-tabs v-model="tab" align-tabs="center" color="indigo" bg-color="white" show-arrows>
        <v-tab v-for="(value, key) in groupedAppointments" :key="key" :value="key" @click="() => {
          // if(this.groupedAppointments[key].length <= 0){
          // }
          this.fetchRecords();
        }">
          {{ key }}
          <v-badge :color="totalCount[key] > 0 ? 'green' : 'indigo'" :content="totalCount[key]" inline></v-badge>
        </v-tab>
      </v-tabs>
      <div class="tab-content">
        <v-window v-model="tab" disabled>
          <v-window-item v-for="(value, key) in groupedAppointments" :key="key" :value="key">
            <AppointmentTab 
            :searchValue="searchValue"
            :selectedDates="selectedDates"
            :selectedDepartments="selectedDepartments" 
            :appointments="value" 
            :tab="key.toLowerCase()"
            :loading="appointmentsLoading"
            ref="appointmentTabRef"
            @show-alert="showAlert"
            @appointment-dialog="appointmentDialog"
            @appointment-note-dialog="addAppointmentNoteDialog"
            @appointment-invoice-dialog="appointmentInvoiceItemsDialog"
            @vital-sign-dialog="vitalSignDialog"
            @service-unit-dialog="serviceUnitDialog"
            @payment-type-dialog="paymentTypeDialog"
            @transfer-practitioner-dialog="transferPractitionerDialog"
            @table-page-change="pageChanged"
            @read-card="readIdCard"
            @visit-status-log="visitStatusLogDiallog"
            @medical-history-dialog="medicalHistoryDialog"
            @checklist-form-dialog="checklistFormDialog"
            />
          </v-window-item>
        </v-window>
      </div>
      <!-- /Appointment Tab -->
      
    </div>
    <!-- /Page Content -->

    <!-- Page Dialogs -->
    <patientAppointmentDialog 
    :isOpen="appointmentOpen" 
    @update:isOpen="appointmentOpen = $event" 
    @show-alert="showAlert" 
    @show-slots="showSlots"
    :form="appointmentForm"
    :slots="slots"
    :adjustAppointments="adjustAppointments"
    />
    <vitalSignsListDialog 
    :isOpen="vitalSignsOpen" 
    @update:isOpen="vitalSignsOpen = $event" 
    @show-alert="showAlert" 
    :appointment="selectedRow"
    />
    <appointmentNoteDialog 
    :isOpen="appointmentNoteOpen" 
    @update:isOpen="appointmentNoteOpen = $event" 
    @show-alert="showAlert" 
    :appointmentId="selectedRow?.name"
    />
    <appointmentInvoiceDialog 
    :isOpen="appointmentInvoiceOpen" 
    @update:isOpen="appointmentInvoiceOpen = $event" 
    @show-alert="showAlert" 
    :appointment="selectedRow"
    />
    <patientMedicalHistoryDialog 
    :isOpen="medicalHistoryOpen" 
    @update:isOpen="medicalHistoryOpen = $event" 
    @show-alert="showAlert" 
    :patient="patient"
    />
    <checklistFormListDialog 
    :isOpen="checklistFormOpen" 
    :appointment="selectedRow"
    @update:isOpen="checklistFormOpen = $event" 
    @show-alert="showAlert" 
    />
    <biocomDialog 
    :isOpen="biocomOpen" 
    :appointment="selectedRow?.name"
    @update:isOpen="biocomOpen = $event" 
    @show-alert="showAlert" 
    />
    <v-dialog v-model="serviceUnitOpen" width="auto">
      <v-card
        rounded="lg"
        width="auto"
        prepend-icon="mdi mdi-door-open"
        title="Update Room"
      >
        <v-card-text>
          <a-select
          v-model:value="appointmentForm.service_unit"
          :options="$resources.serviceUnits.data?.options"
          :fieldNames="{label: 'name', value: 'name'}"
          style="min-width: 400px; max-width: 600px;"
          show-search
          :loading="$resources.serviceUnits.list.loading"
          @search="(value) => {handleSearch(
            value, 
            $resources.serviceUnits, 
            {allow_appointments: 1, is_group: 0, name: ['like', `%${value}%`]}, 
            {allow_appointments: 1, is_group: 0},
          )}"
          :filterOption="false"
          ></a-select>
        </v-card-text>

        <v-card-actions class="my-2 d-flex justify-end">
          <v-btn
          class="text-none"
          text="Cancel"
          @click="serviceUnitOpen = false"
          ></v-btn>

          <v-btn
          class="text-none"
          color="blue"
          
          text="Save"
          variant="tonal"
          @click="onSubmitServiceUnit()"
          ></v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="transferOpen" width="auto">
      <v-card
        rounded="lg"
        width="auto"
        prepend-icon="mdi mdi-door-open"
        title="Transfer To Practitioner"
      >
        <v-card-text>
          <a-select
          v-model:value="appointmentForm.practitioner_name"
          :options="$resources.practitioners.data?.options"
          :fieldNames="{label: 'practitioner_name', value: 'name'}"
          style="min-width: 400px; max-width: 600px;"
          show-search
          :loading="$resources.practitioners.list.loading"
          @search="(value) => {handleSearch(
            value, 
            $resources.practitioners, 
            {status: 'Active', practitioner_name: ['like', `%${value}%`]}, 
            {status: 'Active'},
          )}"
          :filterOption="false"
          ></a-select>
        </v-card-text>

        <v-card-actions class="my-2 d-flex justify-end">
          <v-btn
          class="text-none"
          text="Cancel"
          @click="transferOpen = false"
          ></v-btn>

          <v-btn
          class="text-none"
          color="blue"
          
          text="Save"
          variant="tonal"
          @click="onSubmitTransferPractitioner()"
          ></v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="paymentTypeOpen" width="auto">
      <v-card
        rounded="lg"
        width="auto"
        prepend-icon="pi pi-wallet"
        title="Update Payment Type"
      >
        <v-card-text>
          <a-form layout="vertical">
            <a-form-item label="Payment Type">
              <a-select
                v-model:value="appointmentForm.custom_payment_type"
                :options="[{label: '', value: ''}, {label: 'Self Payment', value: 'Self Payment'}, {label: 'Insurance', value: 'Insurance'}]"
                style="min-width: 400px; max-width: 600px;"
              ></a-select>
            </a-form-item>
  
            <div v-if="appointmentForm.custom_payment_type == 'Insurance'">
              <h4 class="mb-4 font-semibold">Insurance Details</h4>
              <a-checkbox class="mb-3" v-model:checked="patientInsurance.custom_active">Active</a-checkbox>
              <a-form-item label="Insurance Company Name">
                <a-select
                v-model:value="patientInsurance.custom_insurance_company_name"
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
                <a-input v-model:value="patientInsurance.custom_policy_number"/>
              </a-form-item>
              <a-form-item label="Expiration Date">
                <a-date-picker 
                v-model:value="patientInsurance.custom_expiration_date"
                format="DD MMM YYYY" 
                style="z-index: 3000; width: 100%"
                />
              </a-form-item>
              <a-form-item label="Copay Amount">
                <a-input-number class="w-full" :controls="false" v-model:value="patientInsurance.custom_copay_amount"/>
              </a-form-item>
            </div>
          </a-form>
        </v-card-text>

        <v-card-actions class="my-2 d-flex justify-end">
          <v-btn
          class="text-none"
          text="Cancel"
          @click="paymentTypeOpen = false"
          ></v-btn>

          <v-btn
          class="text-none"
          color="blue"
          
          text="Save"
          variant="tonal"
          @click="onSubmitPaymentType()"
          ></v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
    <v-dialog v-model="checkAvailabilityOpen" min-width="650" width="auto">
      <v-card
        rounded="lg"
        width="auto"
      >
        <v-card-item prepend-icon="mdi mdi-door-open" title="Appointment History">
          <template #append>
            <v-btn class="text-none" variant="outlined" color="primary" @click="() => {
              appointmentDialog('New Appointment', false, {
                patient_details: {
                  id: checkAvailabilityPatient,
                  gender: checkAvailabilityPatientGender,
                  age: checkAvailabilityPatientAge,
                  mobile: checkAvailabilityPatientMobile,
                },
				        patient_name: checkAvailabilityPatient,
              })
            }">
              New Appointment
            </v-btn>
          </template>
        </v-card-item>
        <v-card-text>
          <a-form class="w-full" layout="vertical">
            <v-container>
              <v-row>
                <v-col cols="12" md="6">
                  <v-avatar v-if="checkAvailabilityPatient && checkAvailabilityPatientImage" rounded="0" size="120" class="mb-4">
                    <v-img alt="Patient Image" :src="checkAvailabilityPatientImage" cover></v-img>
                  </v-avatar>
                  <a-form-item label="Patient">
                    <a-select
                    class="w-full"
                    ref="patientRef"
                    v-model:value="checkAvailabilityPatient"
                    :options="$resources.patients.data?.options"
                    :fieldNames="{label: 'patient_name', value: 'name'}"
                    show-search
                    :loading="$resources.patients.list.loading"
                    @search="(value) => {handleSearch(
                      value, 
                      $resources.patients, 
                      {status: 'Active'}, 
                      {status: 'Active'},
                      [
                        ['patient_name', 'like', `%${value}%`], 
                        ['mobile', 'like', `%${value}%`], 
                        ['custom_cpr', 'like', `%${value}%`], 
                        ['custom_file_number', 'like', `%${value}%`]
                      ]
                    )}"
                    @change="(value, option) => {
                      checkAvailabilityPatientMobile = option.mobile
                      checkAvailabilityPatientGender = option.sex
                      checkAvailabilityPatientAge = calculateAge(option.dob)
                      checkAvailabilityPatientImage = option.image
                      checkAvailabilityDialog(option.name)
                    }"
                    :filterOption="false"
                    >
                      <template #option="{ patient_name, mobile, custom_cpr, custom_file_number }">
                        <div class="flex flex-col">
                          <span v-if="patient_name" class="ms-2"><strong>Name:</strong> {{ patient_name }}</span>
                          <span v-if="custom_cpr" class="ms-2 text-xs"><strong>CPR:</strong> {{ custom_cpr }}</span>
                          <span v-if="mobile" class="ms-2 text-xs"><strong>Mobile:</strong> {{ mobile }}</span>
                          <span v-if="mobile" class="ms-2 text-xs"><strong>File#:</strong> {{ custom_file_number }}</span>
                        </div>
                      </template>
                    </a-select>
                  </a-form-item>
                  <a-form-item label="Patient Mobile" v-if="checkAvailabilityPatient">
                    <a-input v-model:value="checkAvailabilityPatientMobile" disabled/>
                  </a-form-item>
                </v-col>
                <v-col cols="12" md="6">
                  <v-avatar v-if="checkAvailabilityPatient && checkAvailabilityPatientImage" rounded="0" size="120" class="mb-4">
                    <v-img alt="Patient Image" :src="checkAvailabilityPatientImage" cover hidden></v-img>
                  </v-avatar>
                  <a-form-item label="Patient Gender" v-if="checkAvailabilityPatient">
                    <a-input v-model:value="checkAvailabilityPatientGender" disabled/>
                  </a-form-item>
                  <a-form-item label="Patient Age" v-if="checkAvailabilityPatient">
                    <a-input v-model:value="checkAvailabilityPatientAge" disabled/>
                  </a-form-item>
                </v-col>
              </v-row>
              <v-row v-if="checkAvailabilityPatient">
                <v-col cols="12">
                  <DataTable 
                  :value="checkAvailabilityAppointments" 
                  selectionMode="single" 
                  :metaKeySelection="true" 
                  dataKey="id" 
                  sortField="appointment_datetime"
                  @row-click="({ data }) => {appointmentDialog('Edit Appointment', false, data)}"
                  @row-contextmenu="handleAvailabilityRowContextMenu"
                  :loading="checkAvailabilityLoading"
                  >
                    <template #empty><v-empty-state title="No available appoiontments for this patient"></v-empty-state></template>
                    <Column header="Time" field="appointment_time">
                      <template #body="{ data }">
                        <div @click="() => {appointmentDialog('Edit Appointment', false, data)}">
                          <div class="text-center">
                            {{ data.appointment_date_moment }}
                          </div>
                          <div class="text-center">
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
                    <Column header="Procedures" field="procedure_templates">
                      <template #body="{ data }">
                        <div v-if="data.procedure_templates.length > 0">
                          <v-chip v-for="(procedure, index) in data.procedure_templates" :key="index" class="mr-1" label size="small">{{ procedure.template }}</v-chip>
                        </div>
                        <div v-else>
                          {{ data.notes }}
                        </div>
                      </template>
                    </Column>
                    <Column header="Paid Amount" field="paid_amount">
                      <template #body="{ data }">
                        BD {{ data.paid_amount }}
                      </template>
                    </Column>
                  </DataTable>
                </v-col>
              </v-row>
            </v-container>
          </a-form>
        </v-card-text>
        <ContextMenu 
        :pt="{
          root: {style: {zIndex: 3000}}
        }" 
        ref="menu" 
        :model="contextItems" 
        @hide="selectedRow = {name: '', patient_details: {id: ''}}"
        />
      </v-card>
    </v-dialog>
    <!-- / Page Dialogs -->
    <v-overlay
      :model-value="lodingOverlay"
      class="align-center justify-center"
    >
      <v-progress-circular
        color="primary"
        size="64"
        indeterminate
      ></v-progress-circular>
    </v-overlay>
    <v-dialog v-model="visitStatusLogOpen" width="450">
      <v-card
        rounded="lg"
        width="auto"
        prepend-icon="mdi mdi-door-open"
        title="Visit Logs"
      >
        <v-card-text>
          <div class="mt-4"></div>
          <div v-for="(status, index) in selectedRow.status_log" :key="index" class="flex flex-row justify-between mb-3">
            <h4 class="m-0">{{ status.status }} :</h4>
            <h6 class="align-self-center m-0">{{ status.timeFormat }}</h6>
          </div>
        </v-card-text>
      </v-card>
    </v-dialog>
    <!-- / Page Dialogs -->
    <v-overlay
      :model-value="lodingOverlay"
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
import { ref } from 'vue';
import moment from "moment";
import dayjs from 'dayjs';
import Clock from '@/components/clock/Clock.vue';
import axios from 'axios';

import { VIcon } from 'vuetify/components/VIcon';
import { VToolbar, VToolbarItems } from 'vuetify/components/VToolbar';
import { VBtnToggle } from 'vuetify/components/VBtnToggle';
import { VProgressLinear } from 'vuetify/components/VProgressLinear';
import { VAvatar } from 'vuetify/components/VAvatar';
import { VChip } from 'vuetify/components/VChip';
import { VEmptyState } from 'vuetify/labs/VEmptyState';

import AppointmentTab from './doctor-appointment-tab.vue'
import { VCardItem, VImg, VTooltip } from 'vuetify/components';

export default {
  inject: ['$socket', '$call'],
  components: {
    AppointmentTab, Clock, VIcon, VToolbar, VToolbarItems, VBtnToggle, VProgressLinear, VAvatar, VChip, VEmptyState, VImg,
    VCardItem, VTooltip
  },
  resources: {
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
    departments() { return { 
      type: 'list', 
      doctype: 'Medical Department', 
      fields: ['name', 'department'], 
      auto: true, 
      orderBy: 'department',
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
    appointmentTypes() { return { 
      type: 'list', 
      doctype: 'Appointment Type', 
      fields: ['name', 'appointment_type', 'allow_booking_for', 'default_duration'], 
      auto: true, 
      orderBy: 'appointment_type',
      pageLength: 10,
      url: 'frappe.desk.reportview.get', 
      transform(data) {
        if(data.values.length == 0)
          data.options = []
        else{
          data.options = this.transformData(data.keys, data.values);  // Transform the result into objects

          let defalutType = data.options.filter(value => value.appointment_type == 'Practitioner')
          if(defalutType.length == 0)
            defalutType[0] = data.options[0]

          this.appointmentForm.appointment_type = data.options[0].appointment_type
          this.appointmentForm.appointment_for = data.options[0].allow_booking_for
          this.appointmentForm.duration = defalutType[0].default_duration
        }
        return data
      }
    }},
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
    serviceUnits() { return { 
      type: 'list', 
      doctype: 'Healthcare Service Unit', 
      fields:['name'], 
      filters:{'allow_appointments': 1, 'is_group': 0}, 
      auto: true, 
      orderBy: 'name',
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
    patients() { return { 
      type: 'list', 
      doctype: 'Patient', 
      fields: [
        'sex', 'patient_name', 'name', 'custom_cpr', 'dob', 'mobile', 'email', 'blood_group', 'image',
        'inpatient_record', 'inpatient_status', 'custom_default_payment_type', 'custom_file_number'
      ], 
      filters: {status: 'Active'},
      limit_start: 0,
      pageLength: 10, 
      url: 'frappe.desk.reportview.get', 
      auto: true, 
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
      tab: 'Scheduled',
      start: 0,
      limit: {Scheduled: 20, Arrived: 20, Ready: 20, 'In Room': 20, Completed: 20, 'No Show': 20},
      appointments: [],
      groupedAppointments: {Scheduled:[], Arrived:[], Ready:[], 'In Room':[], Completed:[], 'No Show':[],},
      searchValue: '',
      selectedDepartments: undefined,
      appointmentsLoading: false,
      appointmentOpen: false,
      appointmentNoteOpen: false,
      vitalSignsOpen: false,
      serviceUnitOpen: false,
      transferOpen: false,
      paymentTypeOpen: false,
      appointmentInvoiceOpen: false,
      visitStatusLogOpen: false,
      checkAvailabilityOpen: false,
      medicalHistoryOpen: false,
      checklistFormOpen: false,
      biocomOpen: false,
      lodingOverlay: false,
      slots: {},

      patient: {
        custom_allergies_table: [],
        custom_infected_diseases: [],
        custom_surgical_history_table: [],
        custom_medications: [],
        custom_habits__social: [],
        custom_risk_factors_table: [],
        custom_chronic_diseases: [],
        custom_genetic_conditions: [],
      },

      checkAvailabilityAppointments: [],
      checkAvailabilityPatient: '',
      checkAvailabilityPatientImage: '',
      checkAvailabilityPatientMobile: '',
      checkAvailabilityPatientGender: '',
      checkAvailabilityPatientAge: '',
      checkAvailabilityLoading: false,

      alertMessage: '',
      alertType: '', // 'success' or 'error'
      alertActive: false,

      appointmentForm: {},
      patientInsurance: {},
      selectedRow: {name: '', patient_details: {id: ''}},
      dateFilterType: 'span',
      selectedSpan: 'today',
      selectedDates: ref([dayjs()]),
      selectedRangeDates: [dayjs().startOf('isoWeek').subtract(1, 'day'), dayjs().endOf('isoWeek').subtract(1, 'day')],
      spans: [
        {label: 'Yesterday', value: 'yesterday'},
        {label: 'Today', value: 'today'},
        {label: 'Tomorrow', value: 'tomorrow'},
        {label: 'Last Week', value: 'last week'},
        {label: 'This Week', value: 'this week'},
        {label: 'Next Week', value: 'next week'},
        {label: 'Last Month', value: 'last month'},
        {label: 'This Month', value: 'this month'},
        {label: 'Next Month',  value: 'next month'},
      ],
      totalRecords: 0,
      totalCount: {Scheduled: 0, Arrived: 0, Ready: 0, 'In Room': 0, Completed: 0, 'No Show': 0},
      progressValue: 0,
    };
  },
  computed: {
    contextItems() {
			return [
				{
					label: 'Reschedule Appointment',
					icon: 'mdi mdi-clock-outline',
					command: () => {this.appointmentDialog('Edit Appointment', false, this.selectedRow)}
				},
				{
					label: 'Billing Items',
					icon: 'mdi mdi-invoice-text-outline',
					command: () => {this.appointmentDialog(this.selectedRow)}
				},
				{
					label: 'ID Card Reading',
					icon: 'mdi mdi-card-account-details-outline',
					command: () => {this.readIdCard(this.selectedRow)}
				},
				{
					label: 'Update Room',
					icon: 'mdi mdi-door-open',
					command: () => {this.serviceUnitDialog(this.selectedRow)}
				},
				{
					label: 'Update Payment Type',
					icon: 'pi pi-wallet',
					command: () => {this.paymentTypeDialog(this.selectedRow)}
				},
				{
					label: 'Tranfer To Practitioner',
					icon: 'mdi mdi-transit-transfer',
					command: () => {this.transferPractitionerDialog(this.selectedRow)}
				},
      ]		
		},
  },
  created() {
    // this.$socket.on('patient_appointments_chunk', (chunk) => {
    //   this.appointmentsLoading = true;
    //   this.appointments = this.adjustAppointments([...this.appointments, ...chunk.data]);
    //   if(chunk.total)
    //     this.totalRecords = chunk.total;
    //   this.groupAppointmentsByStatus();
    //   this.updateProgress();
    //   if (this.appointments.length >= this.totalRecords) {
    //     this.appointmentsLoading = false;
    //   }
    // });

    this.$socket.on('patient_appointments_updated', updatedAppointment => {
      if (updatedAppointment) {
        const appointmentDate = dayjs(updatedAppointment.appointment_date);

        // Check if the updated appointment falls within the selected date range
        const isInDateRange = this.selectedDates.some(date => date.isSame(appointmentDate, 'day'));

        if (isInDateRange) {
          const dates = this.selectedDates.map(date => date.format('YYYY-MM-DD'))
          this.$call('healthcare_doworks.api.methods.get_tabs_count', {
            filters: {appointment_date: ['in', dates]}
          }).then(response => {
            this.totalCount = response
          })
          .catch(error => {
            this.showAlert(error.message, 'error')
            console.error('Error fetching records:', error);
          });

          const index = this.appointments.findIndex(app => app.name === updatedAppointment.name);

          if (index !== -1) {
            // Update the existing appointment
            this.appointments.splice(index, 1, this.adjustAppointments([updatedAppointment])[0]);
          } else {
            // If not in the list, add it
            this.appointments.push(this.adjustAppointments([updatedAppointment])[0]);
          }
          
          this.groupAppointmentsByStatus();  // Re-group appointments by status
        }
      }
    })
  },

  mounted() {
    this.selectedDates = ref([dayjs()])
    this.selectedRangeDates = [dayjs().startOf('isoWeek').subtract(1, 'day'), dayjs().endOf('isoWeek').subtract(1, 'day')]
    this.fetchRecords();
  },
  methods: {
    showAlert(message, type) {
      this.alertMessage = message;
      this.alertType = type;
      this.alertActive = true;
    },
    resetDates() {
      this.selectedDates = ref([dayjs()])
      this.selectedRangeDates = [dayjs().startOf('isoWeek').subtract(1, 'day'), dayjs().endOf('isoWeek').subtract(1, 'day')]
    },
    getFormatedDates() {return this.selectedDates.map(date => date.format('YYYY-MM-DD'))},
    fetchRecords(filters={appointment_date: ['in', this.getFormatedDates()], custom_visit_status: this.tab}, orFilters=undefined) {
      this.appointmentsLoading = true;
      const dates = this.selectedDates.map(date => date.format('YYYY-MM-DD'))
      this.$call('healthcare_doworks.api.methods.fetch_patient_appointments', {
        filters: filters, start: this.start, limit: this.limit[this.tab], or_filters: orFilters
      })
      .then(response => {
        if(response.total_count)
          this.totalCount = response.total_count
        const combinedAppointments = [...this.appointments, ...this.adjustAppointments(response.appointments)].reduce((acc, obj) => {
          acc.set(obj.name, obj);
          return acc;
        }, new Map());

        this.appointments = Array.from(combinedAppointments.values());
        // this.appointments = this.adjustAppointments(response.appointments)
        this.groupAppointmentsByStatus();
        this.appointmentsLoading = false;
      })
      .catch(error => {
        this.appointmentsLoading = false;
        this.showAlert(error.message, 'error')
        console.error('Error fetching records:', error);
      });
    },
    adjustAppointments(data) {
			return [...(data || [])].map((d) => {
        d.notes = this.stripHtml(d.notes)

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
    handleAvailabilityRowContextMenu({ originalEvent, data, index }) {
			this.selectedRow = data
			this.$refs.menu.show(originalEvent);
		},
    spanToDate(span) {
      if(span){
        if(span === 'yesterday')
          return [dayjs().add(-1, 'd')]
        if(span === 'today')
          return [dayjs()]
        if(span === 'tomorrow')
          return [dayjs().add(1, 'd')]
        if(span === 'last week'){
          const lwRange = [dayjs().subtract(1, 'week').startOf('isoWeek').subtract(1, 'day'), dayjs().subtract(1, 'week').endOf('isoWeek').subtract(1, 'day')]
          return this.getDatesInBetween(lwRange[0], lwRange[1])
        }
        if(span === 'this week'){
          const twRange = [dayjs().startOf('isoWeek').subtract(1, 'day'), dayjs().endOf('isoWeek').subtract(1, 'day')]
          return this.getDatesInBetween(twRange[0], twRange[1])
        }
        if(span === 'next week'){
          const nwRange = [dayjs().add(1, 'week').startOf('isoWeek').subtract(1, 'day'), dayjs().add(1, 'week').endOf('isoWeek').subtract(1, 'day')]
          return this.getDatesInBetween(nwRange[0], nwRange[1])
        }
        if(span === 'last month'){
          const lmRange = [dayjs().subtract(1, 'month').startOf('month'), dayjs().subtract(1, 'month').endOf('month')]
          return this.getDatesInBetween(lmRange[0], lmRange[1])
        }
        if(span === 'this month'){
          const tmRange = [dayjs().startOf('month'), dayjs().endOf('month')]
          return this.getDatesInBetween(tmRange[0], tmRange[1])
        }
        if(span === 'next month'){
          const nmRange = [dayjs().add(1, 'month').startOf('month'), dayjs().add(1, 'month').endOf('month')]
          return this.getDatesInBetween(nmRange[0], nmRange[1])
        }
        return undefined
      }
      return undefined
    },
    getDatesInBetween(startDate, endDate) {
      let dates = []
      
      while (startDate.isBefore(endDate) || startDate.isSame(endDate, 'day')) {
        dates.push(startDate);
        startDate = startDate.add(1, 'day');
      }
      return dates
    },
    getBadgeNumber(tab){
      let count = 0
      if(this.groupedAppointments[tab]){
        count = this.groupedAppointments[tab].reduce((total, value) => {
          let departmentFilter = true
          let dateFilter = true
          if(this.selectedDepartments)
            departmentFilter = this.selectedDepartments.some(department => {return department === value.department})
          if(this.selectedDates.length > 0)
            dateFilter = this.selectedDates.some(date => {return date.format('YYYY-MM-DD') === value.appointment_date})
          if(dateFilter && departmentFilter){
            return total + 1
          }
          return total
        },0)
      }
      return count
    },
    groupAppointmentsByStatus() {
      this.groupedAppointments = {Scheduled:[], Arrived:[], Ready:[], 'In Room':[], Completed:[], 'No Show':[],}
      this.appointments.forEach(appointment => {
        const status = appointment.custom_visit_status;
        if (!this.groupedAppointments[status])
          this.groupedAppointments[status] = [];
        this.groupedAppointments[status].push(appointment);
      });
    },
    appointmentDialog(formType, isNew, row) {
      if(isNew){
        let defalutType = this.$resources.appointmentTypes.data.options.filter(value => value.appointment_type == 'Practitioner')
        if(defalutType.length == 0)
          defalutType[0] = this.$resources.appointmentTypes.data.options[0]

        this.appointmentForm.name = '';
				this.appointmentForm.duration = defalutType[0].default_duration
				this.appointmentForm.appointment_type = defalutType[0].appointment_type;
				this.appointmentForm.appointment_for = defalutType[0].allow_booking_for;
				this.appointmentForm.custom_appointment_category = 'First Time';
        this.appointmentForm.custom_branch = this.$myresources.user.branch || '';
        this.appointmentForm.procedure_templates = [];
        this.appointmentForm.custom_payment_type = '';
        this.appointmentForm.custom_confirmed = 0;
        this.appointmentForm.practitioner = '';
				this.appointmentForm.practitioner_name = '';
				this.appointmentForm.patient = '';
				this.appointmentForm.patient_name = '';
				this.appointmentForm.patient_sex = '';
				this.appointmentForm.department = '';
				this.appointmentForm.service_unit = '';
        this.appointmentForm.notes = '';
        this.appointmentForm.appointment_date = dayjs(this.selectedDates[0]);
        this.appointmentForm.appointment_time = undefined;
			}
			else{
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
			}
      if(formType == 'Reschedule Appointment')
        this.showSlots()
      this.appointmentForm.doctype = 'Patient Appointment';
      // this.appointmentForm.appointment_date = this.appointmentForm.appointment_time = undefined;
			this.appointmentForm.type = formType
      this.appointmentForm.custom_is_walked_in = false;
			this.appointmentOpen = true
		},
    addAppointmentNoteDialog(row) {
      this.selectedRow = row
			this.appointmentNoteOpen = true;
		},
    appointmentInvoiceItemsDialog(row) {
      this.selectedRow = row
			this.appointmentInvoiceOpen = true;
		},
    visitStatusLogDiallog(row) {
      this.selectedRow = row
			this.visitStatusLogOpen = true;
		},
    vitalSignDialog(row) {
      this.selectedRow = row
			this.vitalSignsOpen = true;
		},
    transferPractitionerDialog(row) {
      this.appointmentForm.name = row.name;
      this.appointmentForm.practitioner = row.practitioner;
      this.appointmentForm.practitioner_name = row.practitioner_name;
			this.transferOpen = true
		},
    serviceUnitDialog(row) {
      this.appointmentForm.name = row.name;
      this.appointmentForm.service_unit = row.service_unit;
			this.serviceUnitOpen = true
		},
    checkAvailabilityDialog() {
      this.checkAvailabilityLoading = true
      this.$call('healthcare_doworks.api.methods.check_availability', { patient: this.checkAvailabilityPatient })
      .then((response) => {
        this.checkAvailabilityAppointments = this.adjustAppointments(response)
        this.checkAvailabilityLoading = false
      }).catch(error => {
        this.checkAvailabilityLoading = false
        this.showAlert(error.message, 'error')
      });
    },
    checklistFormDialog(row) {
      this.selectedRow = row
      this.checklistFormOpen = true;
    },
    medicalHistoryDialog(row) {
      this.$call('frappe.client.get', {doctype: 'Patient', name: row.patient_details.id})
      .then(response => {
        this.$toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Patient medical history updated',
          life: 3000 // Duration in ms
        });
        this.patient = response
        this.medicalHistoryOpen = true;
      })
      .catch(error => {
        this.appointmentsLoading = false;
        this.showAlert(error.message, 'error')
        console.error('Error fetching records:', error);
      });
    },
    paymentTypeDialog(row) {
      this.appointmentForm.name = row.name;
      this.appointmentForm.custom_payment_type = row.custom_payment_type;
      this.$call('frappe.client.get', {doctype: 'Patient', name: row.patient}).then((data) => {
        this.patientInsurance.doctype = 'Patient'
        this.patientInsurance.name = row.patient
        this.patientInsurance.custom_active = data.custom_active
        this.patientInsurance.custom_insurance_company_name = data.custom_insurance_company_name
        this.patientInsurance.custom_policy_number = data.custom_policy_number
        if(data.custom_expiration_date)
          this.patientInsurance.custom_expiration_date = dayjs(data.custom_expiration_date)
        else
          this.patientInsurance.custom_expiration_date = undefined
        this.patientInsurance.custom_copay_amount = data.custom_copay_amount
        this.paymentTypeOpen = true
      }).catch(error => {
        this.showAlert(error.message, 'error')
      });
    },
    showSlots() {
      if (this.appointmentForm.appointment_date && this.appointmentForm.practitioner) {
        this.slots = {};
        let tempForm = this.appointmentForm;
        tempForm.__islocal = 1;
        tempForm.__unsaved = 1;
        this.$call('healthcare.healthcare.doctype.patient_appointment.patient_appointment.get_availability_data', {
          practitioner: this.appointmentForm.practitioner,
          date: this.appointmentForm.appointment_date.format('YYYY/MM/DD'),
          appointment: JSON.stringify(tempForm)
        }).then((data) => {
          if (data.slot_details.length > 0) {
            // make buttons for each slot
            this.getSlots(data);
          } else {
            let message = error.message.split('\n');
            message = message.find(line => line.includes('frappe.exceptions'));
            const firstSpaceIndex = message.indexOf(' ');
            this.showAlert(message.substring(firstSpaceIndex + 1) , 10000)
          }
        }).catch(error => {
          this.showAlert(error.message, 'error')
        });
      } 
	  },
    getSlots(data) {
      let appointment_count = 0;
      let slot_start_time, slot_end_time, available_slots;
      let appointment_date = this.appointmentForm.appointment_date

      data.slot_details.forEach((slot_info) => {
        slot_info.avail_slot.map(slot => {
          appointment_count = 0;
          slot.disabled = false;
          slot.count_class = '';
          slot_start_time = moment(slot.from_time, 'HH:mm:ss');
          slot_end_time = moment(slot.to_time, 'HH:mm:ss');
          slot.interval = (slot_end_time - slot_start_time) / 60000 | 0;

          // restrict past slots based on the current time.
          let now = moment();
          let booked_moment = ""
          if((now.format("YYYY-MM-DD") == appointment_date) && (slot_start_time.isBefore(now) && !slot.maximum_appointments)){
            slot.disabled = true;
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
                  slot.disabled = true;
                  return false;
                }
              }

              // Check for overlaps considering appointment duration
              if (slot_info.allow_overlap != 1) {
                if (slot_start_time.isBefore(end_time) && slot_end_time.isAfter(booked_moment)) {
                  // There is an overlap
                  slot.disabled = true;
                  return false;
                }
              } else {
                if (slot_start_time.isBefore(end_time) && slot_end_time.isAfter(booked_moment)) {
                  appointment_count++;
                }
                if (appointment_count >= slot_info.service_unit_capacity) {
                  // There is an overlap
                  slot.disabled = true;
                  return false;
                }
              }
            });
          }
          if (slot_info.allow_overlap == 1 && slot_info.service_unit_capacity > 1) {
            available_slots = slot_info.service_unit_capacity - appointment_count;
            slot.count = `${(available_slots > 0 ? available_slots : 'Full')}`;
            slot.count_class = `${(available_slots > 0 ? 'badge-success' : 'badge-danger')}`;
            slot.tool_tip =`${available_slots} slots available for booking`;
          }

          if (slot.maximum_appointments) {
            if (appointment_count >= slot.maximum_appointments) {
              slot.disabled = true;
            }
            else {
              slot.disabled = false;
            }
            available_slots = slot.maximum_appointments - appointment_count;
            slot.count = `${(available_slots > 0 ? available_slots : 'Full')}`;
            slot.count_class = `${(available_slots > 0 ? 'badge-success' : 'badge-danger')}`;
          } 
        });
      });
      this.slots = data;
    },
    calculateAge(dob) {
      if(dob){
        const today = dayjs();
        const birthDate = dayjs(dob)
        const years = today.diff(birthDate, 'year');
        const months = today.diff(birthDate.add(years, 'year'), 'month');
        const days = today.diff(birthDate.add(years, 'year').add(months, 'month'), 'day');
        return `${years} Year(s) ${months} Month(s) ${days} Day(s)`;
      }
      return ''
    },
    onSubmitTransferPractitioner() {
      this.lodingOverlay = true;
      this.$call('healthcare_doworks.api.methods.transferToPractitioner', 
        {app: this.appointmentForm.name, practitioner: this.appointmentForm.practitioner}
      ).then(response => {
        this.$toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Appointment transformed',
          life: 3000 // Duration in ms
        });
        this.lodingOverlay = false;
        this.transferOpen = false;
      }).catch(error => {
        this.showAlert(error.message, 'error')
      });
    },
    onSubmitServiceUnit() {
      this.lodingOverlay = true;
      this.$call('frappe.client.set_value', 
        {doctype: 'Patient Appointment', name: this.appointmentForm.name, fieldname: 'service_unit', value: this.appointmentForm.service_unit}
      ).then(response => {
        this.$toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Appointment room changed',
          life: 3000 // Duration in ms
        });
        this.lodingOverlay = false;
        this.serviceUnitOpen = false;
      }).catch(error => {
        this.showAlert(error.message, 'error')
      });
    },
    onSubmitPaymentType() {
      this.lodingOverlay = true;
      if(this.appointmentForm.custom_payment_type == 'Insurance'){
        let form = {...this.patientInsurance, custom_default_payment_type: this.appointmentForm.custom_payment_type}
        form.custom_expiration_date = form.custom_expiration_date.format('YYYY-MM-DD')
        this.$call('healthcare_doworks.api.methods.edit_doc', {form}).then(response => {
          this.$toast.add({
            severity: 'success',
            summary: 'Success',
            detail: 'Patient insurance details saved',
            life: 3000 // Duration in ms
          });
          this.lodingOverlay = false;
          this.paymentTypeOpen = false;
        }).catch(error => {
          this.showAlert(error.message, 'error')
        });
      }

      this.$call('frappe.client.set_value', 
        {doctype: 'Patient Appointment', name: this.appointmentForm.name, fieldname: 'custom_payment_type', value: this.appointmentForm.custom_payment_type}
      ).then(response => {
        this.$toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Appointment payment type saved',
          life: 3000 // Duration in ms
        });
        this.lodingOverlay = false;
        this.paymentTypeOpen = false;
      }).catch(error => {
        this.showAlert(error.message, 'error')
      });
    },
    pageChanged(event) {
      this.start = event.first;
      const maxed = [20, 100, 500, 2500].some(val => this.groupedAppointments[this.tab].length == val)
      this.limit[this.tab] = event.rows;
      this.fetchRecords();
      // if(event.rows > this.limit[this.tab] && event.rows >= this.groupedAppointments[this.tab].length && maxed){
      // }
      // else
      //   this.limit[this.tab] = event.rows;
    },
    updateProgress() {
      this.progressValue = (this.appointments.length / this.totalRecords) * 100;
    },
    stripHtml(html) {
      const tempDiv = document.createElement('div');
      tempDiv.innerHTML = html;
      return tempDiv.textContent || tempDiv.innerText || "";
    },
    async readIdCard(row) {
      try {
        this.lodingOverlay = true;
        const response = await axios.get('http://localhost:5000/card', {timeout: 3000});
        console.log(response.data);
        const data = response.data;
        let form = {doctype: 'Patient', name: row.patient}

        let first_name = data['first_name']
  			let middle_name = ''
  			let last_name = ''
        
  			if (data['middle_name1'])
  				middle_name = data['middle_name1']
  			if (data['middle_name2'])
  				middle_name += " " + data['middle_name2']
  			if (data['middle_name3'])
  				middle_name += " " + data['middle_name3']
  			if (data['middle_name4'])
  				middle_name += " " + data['middle_name4']
  			if (data['last_name'])
  				last_name = data['last_name']
        
        form.first_name = first_name
        if(middle_name)
          form.middle_name = middle_name
        if(last_name)
          form.last_name = last_name
        form.patient_name = (first_name ? first_name : '' ) + (middle_name ? ' ' + middle_name : '') + (last_name ? ' ' + last_name : '')
        
  			// Full name Arabic

  			let custom_first_name_ar = data['first_name_ar']
  			let custom_middle_name_ar = ''
  			let custom_last_name_ar = ''
        
  			if (data['middle_name1_ar'])
  				custom_middle_name_ar = data['middle_name1_ar']
  			if (data['middle_name2_ar'])
  				custom_middle_name_ar += " " + data['middle_name2_ar']
  			if (data['middle_name3_ar'])
  				custom_middle_name_ar += " " + data['middle_name3_ar']
  			if (data['middle_name4_ar'])
  				custom_middle_name_ar += " " + data['middle_name4_ar']
  			if (data['last_name_ar'])
  				custom_last_name_ar = data['last_name_ar']

        if(custom_first_name_ar)
          form.custom_first_name_ar = custom_first_name_ar
        if(custom_middle_name_ar)
          form.custom_middle_name_ar = custom_middle_name_ar
        if(custom_last_name_ar)
          form.custom_last_name_ar = custom_last_name_ar
        form.patient_name_ar = (custom_first_name_ar ? custom_first_name_ar : '' ) + 
          (custom_middle_name_ar ? ' ' + custom_middle_name_ar : '') + 
          (custom_last_name_ar ? ' ' + custom_last_name_ar : '')
      
        
  			// gender
  			let sex = ''
  			if (data['gender'] == "M")
  				sex = 'Male'
  			if (data['gender'] == "F")
  				sex = 'Female'
        form.sex = sex
        
  			// nationality
  			if(data['nationality'])
          form.custom_nationality = data['nationality']
        
  			// occupation_description
  			if (data['occupation_description'])
          form.custom_occupation_description = data['occupation_description']
        
  			//cpr
  			let custom_cpr = ''
  			if (data['cpr']){
  				custom_cpr = data['cpr'].toString()
  				// if(custom_cpr.length == 9)
  				// 	custom_cpr = "0" + custom_cpr
          form.custom_cpr = custom_cpr
  			}
        
  			// email
  			if (data['email'])
  				form.email = data['email']
        
  			// employer
  			if (data['employer'])
  				form.custom_employer = data['employer']
        
  			//birthdate
  			if (data['birthdate'])
          form.dob = data['birthdate'].toString().substr(0,4) + "-" + data['birthdate'].toString().substr(4,2) + "-" + data['birthdate'].toString().substr(6,2)
  				// console.log(birthdate)
  			// mobile number
  			if (data['nationality'] == 'BAHRAIN')
  				form.mobile = "+973"
        
  			// address
  			let address_cpr = ""
  			if (data['building_no'])
  				address_cpr += "Building " +data['building_no'] + " "
  			if (data['flat_no'])
  				address_cpr +=  ",Flat " +data['flat_no'] + " "
  			if (data['road_no'])
  				address_cpr += ",Road " + data['road_no'] + " "
  			if (data['block_no'])
  				address_cpr += ",Block "+ data['block_no'] + " "
  			if (data['block_name'])
  				address_cpr += data['block_name'] + " "
        form.address = address_cpr
        
        let xmlHttp = new XMLHttpRequest();
        xmlHttp.open( "GET", "http://localhost:5000/card_photo", false ); // false for synchronous request
        xmlHttp.send( null );
        
        
        // cur_frm.set_value("full_name",xmlHttp.responseText)
        console.info(xmlHttp.responseText)
              
   			let data_string=xmlHttp.responseText;
        
  //  			data_string=data_string.replace("[","");
  //  			data_string=data_string.replace("]","");
   			data_string = data_string.replaceAll("'",'"')
   			data_string = data_string.replaceAll('A"ALI',"A'ALI")
   			data_string = data_string.replaceAll(': b"',': "')
   			data_string = data_string.replaceAll("\\x00",'')
   			data_string = data_string.slice(1,-2);
   			console.info("Before parse:" + data_string)
  			let imageDate = JSON.parse(data_string);
        
  			// upload images
  			if (imageDate['image'])
  				form.custom_personal_picture = "+" + imageDate['image']
        
  			// upload signature
  			if (imageDate['signature'])
  				form.custom_signature_picture = "+" +imageDate['signature']
      
        this.$call('healthcare_doworks.api.methods.edit_doc', {form})
        .then(response => {
          this.lodingOverlay = false;
          this.$toast.add({
            severity: 'success',
            summary: 'Success',
            detail: 'Patient saved',
            life: 3000 // Duration in ms
          });
          const url = this.$router.resolve({
            name: 'patient',
            params: { patientId: response.name }
          }).href;
          window.open(url, '_blank');
        }).catch(error => {
          this.showAlert(error.message, 'error')
          this.showAlert('Please Insert A Card!', 'error')
        });
      } catch (error) {
        this.lodingOverlay = false;
        this.showAlert('Please Insert A Card!', 'error')
      }
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
    // formattedDayOfWeek() {
    //   if (!this.selectedDates) return '';
    //   return dayjs(this.selectedDates).format('dddd');
    // },
  },
  name: 'Appointments',
};
</script>

<style>
.appointment-tab .ant-picker-input input{
  cursor: 'pointer';
  text-align: center;
}
</style>