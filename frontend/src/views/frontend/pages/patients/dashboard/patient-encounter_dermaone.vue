<template>
  <div class="main-wrapper encounter-page">
    <v-alert
      v-if="alertActive && alertType === 'error'"
      type="error"
      position="fixed"
      location="top center"
      color="red-lighten-3"
      style="z-index: 5000; margin-top: 15px"
      border="start"
      closable
      @click:close="() => {
        alertActive = false
        alertType = ''
        alertMessage = ''
      }"
    >
      <div v-html="alertMessage"></div>
    </v-alert>
    <ConfirmDialog group="new-procedure">
      <template #container="{ message, acceptCallback, rejectCallback }">
        <div class="rounded p-4">
          <span>{{ message.message }}</span>
          <a-form layout="vertical" 
          :model="newProcedureForm" 
          :rules="{procedure_template: [{ required: true, message: 'Please choose a Procedure Template!' }]}"
          >
          <a-form-item label="Procedure Template">
            <LinkField 
            doctype="Clinical Procedure Template" 
            :value="newProcedureForm.procedure_template" 
            @change="(data) => { 
              newProcedureForm.procedure_template = data 
            }"
            />
          </a-form-item>
          </a-form>
          <div class="d-flex align-items-center gap-2 mt-4">
            <v-btn class="text-none" @click="acceptCallback" color="primary" size="small">Save</v-btn>
            <v-btn class="text-none" outlined @click="rejectCallback" size="small" text>Cancel</v-btn>
          </div>
        </div>
      </template>
    </ConfirmDialog>
    <ConfirmPopup group="delete-procedure"></ConfirmPopup>
    <Popover ref="op">
      <div class="flex flex-col min-w-80">
        <span class="font-medium block mb-2">Procedures</span>
        <Listbox 
        :options="[
          ...procedureForms, 
          ...(records.current_encounter.status != 'Completed' ? [{name: 'Add Procedure', icon: 'mdi mdi-plus'}] : [])
        ]" 
        optionLabel="name" 
        class="w-full procedures-list"
        :pt="{
          option: (props) => ({
            class: 'p-0'
          }),
        }"
        >
          <template #option="{option, index}">
            <div 
            v-if="option.name == 'Add Procedure'"
            class="flex items-center w-full" 
            style="padding: 0.5rem 0.75rem" 
            @click="newProcedure"
            >
              <i :class="option.icon"></i>
              {{ option.name }}
            </div>
            <div 
            v-else
            class="flex items-center w-full" 
            :style="selectedProcedure === index ? {padding: '0.5rem 0.75rem', background: '#020617', color: '#ffffff'} :
              {padding: '0.5rem 0.75rem'}
            " 
            @click="() => {selectedProcedure = index}"
            >
              {{ index + 1 + '. ' + option.procedure_template }}
            </div>
          </template>
        </Listbox>


        <!-- <div>
          <ul class="list-none p-0 m-0 flex flex-col">
            <li 
            v-for="(procedure, index) in procedureForms" 
            :key="index" 
            class="flex items-center gap-2 px-2 py-3 hover:bg-emphasis cursor-pointer rounded-border" 
            @click="selectedProcedure(index)"
            >
              {{ index + '. ' + procedure.name }}
            </li>
          </ul>
        </div> -->
      </div>
    </Popover>
    <SpeedDial :model="actions" :style="{ position: 'fixed', right: '10px', bottom: '10px', zIndex: 500 }">
      <template #button="{ toggleCallback }">
        <v-btn icon="mdi mdi-cog-outline" color="amber" @click="toggleCallback">
        </v-btn>
      </template>
      <template #item="{ item, toggleCallback }">
        <v-btn class="text-none" color="blue" icon size="large" @click="item.command">
          <div class="flex flex-col items-center justify-between gap-2">
            <span :class="item.icon" />
            <span>
              {{ item.label }}
            </span>
          </div>
        </v-btn>
      </template>
    </SpeedDial>
    <GifLoader v-if="isLoading" :gifSrc="gifUrl"/>
    <div v-else class="row w-100 mx-0">
      <div class="ps-0 pe-md-0 mt-2 mb-md-3 d-block col-12 col-md-6 d-xl-none">
        <Card class="h-100" :class="{'rounded-bottom-0': $vuetify.display.smAndDown, 'rounded-end-0': !$vuetify.display.smAndDown}">
          <template #content>
            <div class="vital-sign-container d-flex align-items-center">
              <a 
              :href="$router.resolve({ name: 'patient', params: { patientId: records.patient.name } }).href" 
              target="_blank" 
              style="color: unset; text-decoration: unset"
              >
                <!-- <img v-if="records.patient.image" class="me-3 avatar avatar-xl bg-primary-light rounded-circle" :src="records.patient.image" alt="..."> -->
                <v-avatar v-if="records.patient.image" size="80" :image="records.patient.image"></v-avatar>
                <div class="text-start d-flex flex-column">
                  <h5 class="mb-0">{{ records.patient.patient_name }}</h5>
                  <h6 class="mb-1">{{ records.patient.custom_cpr }}</h6>
                  <p class="mb-1">{{ records.patient.dob + getAge(records.patient.dob) + (records.patient.sex?.slice(0, 1) || '')}}</p>
                  <p class="mb-0"><i class="pi pi-mobile align-middle"></i>{{ records.patient.mobile }}</p>
                </div>
              </a>
            </div>
          </template>
        </Card>
      </div>
      <div class="ps-0 mb-3 mt-md-2 d-block col-12 col-md-6 d-xl-none">
        <Card :class="['h-100',{'rounded-0': this.isAffixed}]">
          <template #content>
            <div class="flex">
              <v-avatar 
              v-if="records.practitioner.image"
              size="80" 
              class="me-3" 
              :image="records.practitioner.image">
              </v-avatar>
              <div class="text-start">
                <h4 class="mb-1">{{ encounterForm.practitioner_name }}</h4>
                <!-- <h4 v-if="practitionerConflict || !records.appointment" class="mb-1" :class="records.appointment ? 'text-green' : ''">{{ $myresources.user.practitioner_name || $myresources.user.name }}</h4> -->
                <p v-if="encounterForm?.department" class="mb-0">Department: <span class="font-weight-bold">{{ encounterForm.department }}</span></p>
                <p v-if="records.appointment?.service_unit" class="mb-0">Room: <span class="font-weight-bold">{{ records.appointment.service_unit }}</span></p>
                <h4 class="my-2">{{ encounterForm.custom_encounter_start_time.format('h:mm A') }}</h4>
                <Tag :severity="records.current_encounter.status == 'Completed' ? 'info' : 'danger'" rounded>
                  <h5 class="m-1">{{ records.current_encounter.status || 'Draft' }}</h5>
                </Tag>
              </div>
            </div>
          </template>
        </Card>
      </div>
      <a-affix 
        @change="affixed => {isAffixed = affixed}"
        class="pe-0"
        :style="this.isAffixed ? {left: '-20px', position: 'relative', width: 'calc(100% + 25px)', maxWidth: 'unset'} : {}"
      >
        <div class="row col-12 sticky-top flex-nowrap" :class="{'mb-3': !this.isAffixed}" id="patient-bar" style="z-index: 1000;">
          <div class="px-0 d-none d-xl-block" style="width: unset;flex: 0 0 auto;" :class="{'ps-0': this.isAffixed}">
            <Card :class="['h-100 rounded-end-0',{'rounded-0': this.isAffixed}]">
              <template #content>
                <div class="vital-sign-container d-flex align-items-center">
                  <a 
                  :href="$router.resolve({ name: 'patient', params: { patientId: records.patient.name } }).href" 
                  target="_blank" 
                  style="color: unset; text-decoration: unset"
                  >
                    <!-- <img v-if="records.patient.image" class="me-3 avatar avatar-xl bg-primary-light rounded-circle" :src="records.patient.image" alt="..."> -->
                    <v-avatar v-if="records.patient.image" size="80" class="me-3" :image="records.patient.image"></v-avatar>
                    <div class="text-start d-flex flex-column">
                      <h5 class="mb-0">{{ records.patient.patient_name }}</h5>
                      <h6 class="mb-1">{{ records.patient.custom_cpr }}</h6>
                      <p class="mb-1">{{ records.patient.dob + getAge(records.patient.dob) + (records.patient.sex?.slice(0, 1) || '')}}</p>
                      <p class="mb-0"><i class="pi pi-mobile align-middle"></i>{{ records.patient.mobile }}</p>
                    </div>
                  </a>
                </div>
              </template>
            </Card>
          </div>
          <div class="px-0" style="width: unset; flex-grow: 1; min-width: 0; flex-shrink: unset;">
            <Card :class="['h-100',{'rounded-0': this.isAffixed, 'rounded-start-0': $vuetify.display.xlAndUp}]">
              <template #content>
                <v-slide-group mobile-breakpoint="sm">
                  <v-slide-group-item>
                    <div class="vital-sign-container flex flex-col gap-5 align-self-center">
                      <div>
                        <div class="mb-2 gap-2 d-flex align-items-center">
                          <i class="pi pi-heart" style="font-size: 1.5rem"></i>
                          <h6 class="my-0 fw-normal">SYS</h6>
                        </div>
                        <div class="d-flex gap-1 align-items-center justify-content-center">
                          <h6 class="fw-normal mb-0">{{currentVS?.bp_systolic || '-'}}</h6> <small class="align-self-end" v-if="currentVS?.bp_systolic">mm Hg</small>
                        </div>
                      </div>
                      <div>
                        <div class="mb-2 gap-2 d-flex align-items-center">
                          <i class="pi pi-heart" style="font-size: 1.5rem"></i>
                          <h6 class="my-0 fw-normal">DIA</h6>
                        </div>
                        <div class="d-flex gap-1 align-items-center justify-content-center">
                          <h6 class="fw-normal mb-0">{{currentVS?.bp_diastolic || '-'}}</h6> <small class="align-self-end" v-if="currentVS?.bp_diastolic">mm Hg</small>
                        </div>
                      </div>
                    </div>
                  </v-slide-group-item>
                  <Divider layout="vertical"/>
                  <v-slide-group-item>
                    <div class="vital-sign-container flex flex-col pt-1 pb-3 gap-3 align-self-center">
                      <div class="pb-3">
                        <div class="gap-1 d-flex align-items-center">
                          <i class="mdi mdi-pulse" style="font-size: 2.5rem"></i>
                          <h6 class="my-0 fw-normal">Pulse</h6>
                        </div>
                        <div class="d-flex gap-1 align-items-center justify-content-center relative -top-2.5">
                          <h6 class="fw-normal mb-0">{{currentVS?.pulse || '-'}}</h6> <small class="align-self-end" v-if="currentVS?.pulse">BPM</small>
                        </div>
                      </div>

                      <div class="pb-2">
                        <div class="gap-2 d-flex align-items-center">
                          <i class="mdi mdi-water-opacity" style="font-size: 1.5rem"></i>
                          <h6 class="my-0 fw-normal">Saturation</h6>
                        </div>
                        <div class="d-flex gap-1 align-items-center justify-content-center">
                          <h6 class="fw-normal mb-0">{{currentVS?.custom_saturation_rate || '-'}}</h6> <small class="align-self-end" v-if="currentVS?.custom_saturation_rate">%</small>
                        </div>
                      </div>
                    </div>
                  </v-slide-group-item>
                  <Divider layout="vertical" />
                  <v-slide-group-item>
                    <div class="vital-sign-container flex flex-col gap-[20px] pb-3.5 align-self-center">
                      <div class="pb-3">
                        <div class="gap-1 d-flex align-items-center">
                          <i class="mdi mdi-thermometer" style="font-size: 2rem"></i>
                          <h6 class="my-0 fw-normal">Temp</h6>
                        </div>
                        <div class="d-flex gap-1 align-items-center justify-content-center relative -top-2">
                          <h6 class="fw-normal mb-0">{{(currentVS?.temperature || '-') + '\u00B0'}}</h6> <small class="align-self-end" v-if="currentVS?.temperature">C</small>
                        </div>
                      </div>

                      <div>
                        <div class="gap-1 d-flex align-items-center">
                          <img style="width: 18px;" :src="stomachImage"/>
                          <h6 class="ml-1 my-0 fw-normal">Abd</h6>
                        </div>
                        <div class="d-flex gap-1 align-items-center justify-content-center">
                          <h6 class="fw-normal mb-0">{{currentVS?.abdomen || '-'}}</h6>
                        </div>
                      </div>
                    </div>
                  </v-slide-group-item>
                  <Divider layout="vertical" />
                  <v-slide-group-item>
                    <div class="vital-sign-container flex flex-col gap-5 align-self-center">
                      <div>
                        <div class="gap-1 d-flex align-items-center">
                          <img style="width: 18px;" :src="kneeImage"/>
                          <h6 class="ml-1 my-0 fw-normal">Reflexes</h6>
                        </div>
                        <div class="d-flex gap-1 align-items-center justify-content-center">
                          <h6 class="fw-normal mb-0">{{currentVS?.reflexes || '-'}}</h6>
                        </div>
                      </div>

                      <div>
                        <div class="gap-1 d-flex align-items-center">
                          <img style="width: 18px;" :src="tongueImage"/>
                          <h6 class="ml-1 my-0 fw-normal">Tongue</h6>
                        </div>
                        <div class="d-flex gap-1 align-items-center justify-content-center">
                          <h6 class="fw-normal mb-0">{{currentVS?.tongue || '-'}}</h6>
                        </div>
                      </div>
                    </div>
                  </v-slide-group-item>
                </v-slide-group>
                <div class="d-flex align-self-end ms-auto flex-shrink-0">
                  <v-select
                  v-model="currentVS"
                  item-title="signs_date"
                  item-value="name"
                  return-object
                  :items="records.vitalSigns"
                  variant="underlined"
                  class="w-full align-middle"
                  ></v-select>
                  <!-- <a-select
                  class="w-full align-middle"
                  v-model:value="currentVS"
                  style="width: 120px"
                  :options="records.vitalSigns"
                  :fieldNames="{label: 'signs_date', value: 'name'}"
                  @change="(value, option) => {currentVS = option}"
                  ></a-select> -->
                  <v-btn
                    class="ma-2 align-self-center"
                    color="blue"
                    density="comfortable"
                    variant="text"
                    icon="pi pi-plus"
                    @click="() => {vitalSignsActive = true}"
                  ></v-btn>
                </div>
              </template>
            </Card>
          </div>
          <div class="pe-0 d-none d-xl-block" style="width: 25.25%;flex: 0 0 auto;min-width: fit-content" :class="{'ps-0': this.isAffixed}">
            <Card :class="['h-100',{'rounded-0': this.isAffixed}]">
              <template #content>
                <div class="flex">
                  <v-avatar 
                  v-if="records.practitioner.image"
                  size="80" 
                  class="me-3" 
                  :image="records.practitioner.image">
                  </v-avatar>
                  <div class="text-start">
                    <h4 class="mb-1">{{ encounterForm.practitioner_name }}</h4>
                    <!-- <h4 v-if="practitionerConflict || !records.appointment" class="mb-1" :class="records.appointment ? 'text-green' : ''">{{ $myresources.user.practitioner_name || $myresources.user.name }}</h4> -->
                    <p v-if="encounterForm?.department" class="mb-0">Department: <span class="font-weight-bold">{{ encounterForm.department }}</span></p>
                    <p v-if="records.appointment?.service_unit" class="mb-0">Room: <span class="font-weight-bold">{{ records.appointment.service_unit }}</span></p>
                    <h4 class="my-2">{{ encounterForm.custom_encounter_start_time.format('h:mm A') }}</h4>
                    <Tag :severity="records.current_encounter.status == 'Completed' ? 'info' : 'danger'" rounded>
                      <h5 class="m-1">{{ records.current_encounter.status || 'Draft' }}</h5>
                    </Tag>
                  </div>
                </div>
              </template>
            </Card>
          </div>
        </div>
      </a-affix>
      <div class="col-xl-9 col-12 ps-0 left-column row h-100" style="margin-right: calc(.5 * var(--bs-gutter-x)); padding: 0">
        <!-- <div class="mb-3 col-6 pe-0">
          <Card class="p-0" id="past-encounters" style="overflow: hidden;">
            <template #title>Visit Logs
              <v-btn class="float-end text-orange text-none" variant="plain">See All</v-btn>
            </template>
            <template #content>
              <DataTable 
              :value="records.encounters ? records.encounters?.slice(0, 5) : records.encounters" 
              selectionMode="single" 
              :metaKeySelection="true" 
              dataKey="id" 
              @row-click="visitLogSelect"
              >
                <template #empty><v-empty-state title="This Is The First Visit"></v-empty-state></template>
                <Column field="encounter_date" header="Date"></Column>
                <Column field="practitioner_name" header="Practitioner"></Column>
                <Column field="custom_appointment_category" header="Type"></Column>
                <Column header="Reason">
                  <template #body="{ data }">
                    {{ data.custom_appointment_category == 'Procedure' ? 
                      data.procedures?.join(', ') : 
                      data.symptoms?.map(semptom => semptom.complaint).join(', ') 
                    }}
                  </template>
                </Column>
              </DataTable>
            </template>
          </Card>
        </div> -->
        <!-- <div class="mb-3 col-6 pe-0">
          <Card class="p-0" id="services" style="overflow: hidden;">
            <template #title>
              <span class="align-middle">Service Requests / Results ({{ records.services && records.services.length }})</span>
              <v-btn class="float-end text-orange text-none" prepend-icon="pi pi-plus" variant="plain" @click="()=>{serviceRequestActive = true}">Add</v-btn>
            </template>
            <template #content>
              <DataTable :value="records.services ? records.services?.slice(0, 5) : records.services">
                <template #empty><v-empty-state title="No Service Requests"></v-empty-state></template>
                <Column field="template_dn" header="Service Name"></Column>
                <Column field="order_date" header="Ordered On"></Column>
                <Column field="status" header="Status"></Column>
                <Column field="practitioner" header="Ordered By"></Column>
              </DataTable>
            </template>
          </Card>
        </div> -->
        <div class="mb-3 col-6 pe-0">
          <Card class="p-0" id="appointments" style="overflow: hidden;">
            <template #title>Appointments ({{ $resources.appointments.data?.length || '0' }})</template>
            <template #content>
              <DataTable 
              :value="$resources.appointments.data" 
              selectionMode="single" 
              :metaKeySelection="true" 
              @row-click="({data}) => {appointmentDialog('Edit Appointment', false, data)}"
              dataKey="id" 
              class="max-h-72 overflow-y-auto"
              :loading="$resources.appointments.list.loading"
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
          </Card>
        </div>
        <div class="mb-3 col-6 pe-0">
          <Card class="p-0" id="Invoices" style="overflow: hidden;">
            <template #title>Invoices ({{ $resources.invoices.data?.length || '0' }})</template>
            <template #content>
              <DataTable 
              :value="$resources.invoices.data" 
              selectionMode="single" 
              :metaKeySelection="true" 
              dataKey="id" 
              @row-click="invoiceSelect"
              class="max-h-72 overflow-y-auto"
              :loading="$resources.invoices.list.loading"
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
          </Card>
        </div>
        <div class="mb-3 col-6 pe-0">
          <Card class="p-0" id="consultations" style="overflow: hidden;">
            <template #title>Consultations ({{ $resources.consultations.data?.length || '0' }})</template>
            <template #content>
              <DataTable 
              :value="$resources.consultations.data" 
              selectionMode="single" 
              :metaKeySelection="true" 
              dataKey="id" 
              @row-click="({data}) => {encounterSelect(data.name)}"
              class="max-h-72 overflow-y-auto"
              :loading="$resources.consultations.list.loading"
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
          </Card>
        </div>
        <div class="mb-3 col-6 pe-0">
          <Card class="p-0" id="procedures" style="overflow: hidden;">
            <template #title>Procedures ({{ $resources.procedures.data?.length || '0' }})</template>
            <template #content>
              <DataTable 
              :value="$resources.procedures.data" 
              selectionMode="single" 
              :metaKeySelection="true" 
              dataKey="id" 
              @row-click="({data}) => {encounterSelect(data.custom_patient_encounter)}"
              class="max-h-72 overflow-y-auto"
              :loading="$resources.procedures.list.loading"
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
          </Card>
        </div>
        <div class="ps-0 ml-2 col-12 mb-25">
          <Card class="mb-4">
            <template #content>
              <a-form layout="vertical" :model="procedureForms[selectedProcedure]" v-if="records.current_encounter.status != 'Completed'">
                <SelectButton 
                v-model="encounterForm.custom_encounter_state" 
                :options="formOptions" 
                optionLabel="label"
                optionValue="value"
                class="!block text-center" 
                :allowEmpty="false" 
                @change="setStepperValue"
                >
                  <template #option="slotProps">
                    <span class="p-button-label" data-pc-section="label" :label="slotProps.option.label" @click="stateButtomClick">
                      {{ slotProps.option.label }} 
                      <v-badge 
                      v-if="slotProps.option.label == 'Procedure'" 
                      :label="slotProps.option.label" 
                      :content="procedureForms.filter(value => value.name).length" 
                      inline
                      >
                      </v-badge>
                    </span>
                  </template>
                </SelectButton>
                <div class="flex">
                  <h5 class="font-bold ml-2" v-if="encounterForm.custom_encounter_state == 'Procedure'">
                    {{ procedureForms[selectedProcedure]?.name }}
                  </h5>
                  <v-btn 
                  v-if="records.current_encounter.status != 'Completed' && encounterForm.custom_encounter_state == 'Procedure'"
                  class="!flex ml-auto mr-6" 
                  density="compact" 
                  size="large" 
                  color="danger" 
                  rounded="lg" 
                  icon="mdi mdi-delete-outline"
                  @click="confirmDelete"
                  >
                  </v-btn>
                </div>
                <Stepper value="1" v-if="encounterForm.custom_encounter_state === 'Procedure'">
                  <!-- Procedure Panels -->
                  <StepItem value="1">
                    <Step>Procedure Info</Step>
                    <StepPanel v-slot="{ activateCallback }">
                      <v-sheet>
                        <v-container>
                          <v-row>
                            <v-col cols="12" md="6">
                              <a-form-item label="Procedure Template">
                                <LinkField 
                                :disabled="records.current_encounter.status == 'Completed'"
                                doctype="Clinical Procedure Template" 
                                :value="procedureForms[selectedProcedure].procedure_template" 
                                @change="(data) => { 
                                  procedureForms[selectedProcedure].procedure_template = data 
                                  autoSave('Clinical Procedure', procedureForms[selectedProcedure].name, 'procedure_template', data)
                                }"
                                />
                              </a-form-item>
                              <a-form-item label="Practitioner">
                                <a-select
                                :disabled="records.current_encounter.status == 'Completed'"
                                v-model:value="procedureForms[selectedProcedure].practitioner"
                                :options="$resources.practitioners.data?.options"
                                :fieldNames="{label: 'practitioner_name', value: 'name'}"
                                style="width: 100%"
                                @change="(value, option) => {
                                  procedureForms[selectedProcedure].medical_department = option.department
                                  autoSave('Clinical Procedure', 
                                    procedureForms[selectedProcedure].name, 
                                    {practitioner: value, practitioner_name: option.practitioner_name, medical_department: option.department}
                                  )
                                }"
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
                              </a-form-item>
                              <a-form-item label="Medical Department">
                                <LinkField 
                                :disabled="records.current_encounter.status == 'Completed'"
                                doctype="Medical Department" 
                                :value="procedureForms[selectedProcedure].medical_department" 
                                @change="(data) => { 
                                  procedureForms[selectedProcedure].medical_department = data 
                                  autoSave('Clinical Procedure', procedureForms[selectedProcedure].name, 'medical_department', data)
                                }"
                                />
                              </a-form-item>
                              <a-form-item label="Room">
                                <LinkField 
                                :disabled="records.current_encounter.status == 'Completed'"
                                doctype="Medical Department" 
                                query="healthcare.controllers.queries.get_healthcare_service_units"
                                :value="procedureForms[selectedProcedure].service_unit" 
                                @change="(data) => { 
                                  procedureForms[selectedProcedure].service_unit = data 
                                  autoSave('Clinical Procedure', procedureForms[selectedProcedure].name, 'service_unit', data)
                                }"
                                />
                              </a-form-item>
                            </v-col>
                            <v-col cols="12" md="6">
                              <a-form-item label="Start Date">
                                <a-date-picker 
                                  :disabled="records.current_encounter.status == 'Completed'"
                                  v-model:value="procedureForms[selectedProcedure].start_date"
                                  format="DD/MM/YYYY" 
                                  style="width: 100%;"
                                  @change="(date, dateString) => {
                                    const day = dateString.split('/')[0]
                                    const month = dateString.split('/')[1]
                                    const year = dateString.split('/')[2]
                                    autoSave('Clinical Procedure', procedureForms[selectedProcedure].name, 'start_date', `${year}-${month}-${day}`)
                                  }"
                                />
                              </a-form-item>
                              <a-form-item label="Start Time">
                                <a-time-picker 
                                :disabled="records.current_encounter.status == 'Completed'"
                                v-model:value="procedureForms[selectedProcedure].start_time" 
                                format="h:mm a" 
                                style="width: 100%;" 
                                @change="(date, timeString) => {
                                  const [time, modifier] = timeString.split(' ');
                                  let [hours, minutes] = time.split(':');
                                  if (hours === '12')
                                    hours = '00';
                                  if (modifier === 'pm')
                                    hours = parseInt(hours, 10) + 12;
                                  autoSave('Clinical Procedure', procedureForms[selectedProcedure].name, 'start_time', `${hours}:${minutes}`)
                                }"/>
                              </a-form-item>
                              <a-form-item label="Notes">
                                <a-textarea 
                                :disabled="records.current_encounter.status == 'Completed'" 
                                :rows="4" 
                                v-model:value="procedureForms[selectedProcedure].notes" 
                                @blur="event => {
                                  autoSave('Clinical Procedure', procedureForms[selectedProcedure].name, 'notes', event.target.value)
                                }"/>
                              </a-form-item>
                            </v-col>
                          </v-row>
                        </v-container>
                      </v-sheet>
                      <div class="d-flex pt-4">
                        <v-btn class="text-none" variant="flat" color="blue-darken-2" @click="activateCallback('2')">Next</v-btn>
                      </div>
                    </StepPanel>
                  </StepItem>
                  <StepItem value="2">
                    <Step>Pre Procedure</Step>
                    <StepPanel v-slot="{ activateCallback }">
                      <v-sheet>
                        <v-container>
                          <v-row>
                            <v-col>
                              <a-form-item label="Sample">
                                <LinkField 
                                :disabled="records.current_encounter.status == 'Completed'"
                                doctype="Sample Collection" 
                                :value="procedureForms[selectedProcedure].sample" 
                                @change="(data) => { 
                                  procedureForms[selectedProcedure].sample = data 
                                  autoSave('Clinical Procedure', procedureForms[selectedProcedure].name, 'sample', data)
                                }"
                                />
                              </a-form-item>
                              <a-form-item label="Pre Operative Diagnosis">
                                <a-textarea 
                                :disabled="records.current_encounter.status == 'Completed'"
                                :rows="4" 
                                v-model:value="procedureForms[selectedProcedure].custom_pre_operative_diagnosis" 
                                @blur="event => {
                                  autoSave('Clinical Procedure', procedureForms[selectedProcedure].name, 'custom_pre_operative_diagnosis', event.target.value)
                                }"/>
                              </a-form-item>
                              <v-btn 
                              variant="flat" 
                              color="red-accent-4" 
                              class="text-none" 
                              @click="showConsentForm"
                              >
                                Consent Form
                              </v-btn>
                              <v-icon
                              v-if="!!procedureForms[selectedProcedure]?.custom_patient_consent_signature"
                              color="green"
                              icon="mdi mdi-check-decagram"
                              size="large"
                              class="ms-2"
                              ></v-icon>
                            </v-col>
                          </v-row>
                        </v-container>
                      </v-sheet>
                      <div class="d-flex py-4 gap-2">
                        <v-btn class="text-none" variant="flat" color="grey-lighten-2" @click="activateCallback('1')">Back</v-btn>
                        <v-btn class="text-none" variant="flat" color="blue-darken-2" @click="activateCallback('3')">Next</v-btn>
                      </div>
                    </StepPanel>
                  </StepItem>
                  <StepItem value="3">
                    <Step>Procedure</Step>
                    <StepPanel v-slot="{ activateCallback }">
                      <v-sheet>
                        <v-container>
                          <v-row>
                            <v-col>
                              General Data
                              <QuillEditor 
                              ref="quillEditor" 
                              contentType="html"
                              v-model:content="procedureForms[selectedProcedure].custom_general_data" 
                              :options="quillEditorOptions" 
                              style="height: 300px"
                              @blur="event => {
                                autoSave('Clinical Procedure', procedureForms[selectedProcedure].name, 'custom_general_data', procedureForms[selectedProcedure].custom_general_data)
                              }"
                              />
                            </v-col>
                          </v-row>
                          <v-divider></v-divider>
                          <v-row>
                            <v-col>
                              <div class="d-flex gap-2">
                                <v-btn class="text-none" variant="flat" color="orange" disabled>Predefined Areas</v-btn>
                                <v-btn class="text-none" variant="flat" color="orange" disabled>Predefined Annotations</v-btn>
                                <v-btn class="text-none" variant="flat" color="orange" @click="() => {
                                  annotationDoctype = procedureForms[selectedProcedure]?.doctype; 
                                  procedureActive = true
                                }">Free Drawing</v-btn>
                                <v-btn 
                                class="text-none" 
                                variant="flat" 
                                :disabled="records.current_encounter.status == 'Completed'" 
                                color="red" 
                                @click="() => {sergicalProcedureActive = true}"
                                >
                                  Surgical Procedure
                                </v-btn>
                              </div>
                            </v-col>
                          </v-row>
                          <v-row v-if="procedureForms[selectedProcedure]?.custom_annotations?.length > 0">
                            <v-col>
                              <h3 class="mt-3">Annotations</h3>
                              <Galleria 
                              :value="procedureForms[selectedProcedure].custom_annotations" 
                              :responsiveOptions="[{breakpoint: '1300px', numVisible: 4}, {breakpoint: '575px', numVisible: 1}]" 
                              :numVisible="5" 
                              :circular="true" 
                              containerStyle="max-width: 850px" 
                              :showItemNavigators="true" 
                              :showThumbnails="false"
                              :fullScreen="true"
                              v-model:visible="showProcedureAnnotations"
                              v-model:activeIndex="activeIndex"
                              >
                                <template #item="slotProps">
                                  <img 
                                  :src="slotProps.item.image" 
                                  :alt="slotProps.item.name" 
                                  style="height: 100%;"
                                  />
                                </template>
                                <template #thumbnail="slotProps">
                                  <img :src="slotProps.item.image" :alt="slotProps.item.name" style="display: block" />
                                </template>
                              </Galleria>
                              <v-slide-group
                                class="pa-4"
                                selected-class="bg-success"
                                show-arrows
                              >
                                <v-slide-group-item v-for="(doc, index) of procedureForms[selectedProcedure]?.custom_annotations" :key="index">
                                  <img 
                                  :src="doc.image" 
                                  :alt="doc.name" 
                                  style="cursor: pointer; height: 200px" 
                                  @click="() => {activeIndex = index; showProcedureAnnotations = true}"
                                  />
                                </v-slide-group-item>
                              </v-slide-group>
                            </v-col>
                          </v-row>
                        </v-container>
                      </v-sheet>
                      <div class="d-flex py-4 gap-2">
                        <v-btn class="text-none" variant="flat" color="grey-lighten-2" @click="activateCallback('2')">Back</v-btn>
                        <v-btn class="text-none" variant="flat" color="blue-darken-2" @click="activateCallback('4')">Next</v-btn>
                      </div>
                    </StepPanel>
                  </StepItem>
                  <StepItem value="4">
                    <Step>Consumables</Step>
                    <StepPanel v-slot="{ activateCallback }">
                      <v-sheet>
                        <v-container>
                          <v-row>
                            <v-col>
                              <h5>Consumables</h5>
                              <EditableTable :columns="[
                                {label: 'Item', key: 'item_code'},
                                {label: 'Item Name', key: 'item_name'},
                                {label: 'Quantity', key: 'qty'},
                                {label: 'UOM', key: 'uom'},
                                {label: 'Invoice Separately as Consumables', key: 'invoice_separately_as_consumables'},
                              ]"
                              :rows="encounterForm.items"
                              @update="(items, row, isNew) => {
                                if(items && row)
                                  newChildRow({
                                    parentDoctype: 'Clinical Procedure',
                                    prarentDocname: procedureForms[selectedProcedure]?.name,
                                    fieldName: 'items', 
                                    rules: {
                                      item_code: [{ required: true, message: 'Please choose an item!' }],
                                      qty: [{ required: true, message: 'Please choose a quantity!' }],
                                      uom: [{ required: true, message: 'Please choose a uom!' }],
                                      stock_uom: [{ required: true, message: 'Please choose a stock uom!' }],
                                    },
                                    items, row, isNew
                                  })
                              }"
                              @delete="rows => {deleteChildRow({parentDoctype: 'Clinical Procedure', fieldName: 'items', rows})}"
                              dialogWidth="fit-content"
                              title="Medication"
                              >
                                <template v-slot:dialog="{ row }">
                                  <a-form layout="vertical">
                                    <v-container>
                                      <v-row>
                                        <v-col cols="12" lg="6">
                                          <a-form-item label="Item">
                                            <LinkField 
                                            doctype="Item" 
                                            :value="row.item_code" 
                                            @change="(data) => { 
                                              row.item_code = data 
                                              $getValue({doctype: 'Item', fieldname:'item_name', filters:{name:data}})
                                              .then(response => {
                                                row.item_name = response.item_name
                                              })
                                            }"
                                            />
                                          </a-form-item>
                                          <a-form-item label="Item Name">
                                            <a-input v-model:value="row.item_name" disabled/>
                                          </a-form-item>
                                          <a-form-item label="Quantity">
                                            <a-input v-model:value="row.qty"/>
                                          </a-form-item>
                                          <a-form-item label="Barcode">
                                            <a-input v-model:value="row.barcode"/>
                                          </a-form-item>
                                          <a-form-item label="UOM">
                                            <LinkField 
                                            doctype="UOM" 
                                            :value="row.uom" 
                                            @change="(data) => { 
                                              row.uom = data 
                                            }"
                                            />
                                          </a-form-item>
                                          <a-checkbox v-model:checked="row.invoice_separately_as_consumables">
                                            Invoice Separately as Consumables
                                          </a-checkbox>
                                        </v-col>
                                        <v-col cols="12" lg="6">
                                          <a-form-item label="Batch">
                                            <LinkField 
                                            doctype="Batch" 
                                            :value="row.batch_no" 
                                            @change="(data) => { 
                                              row.batch_no = data 
                                            }"
                                            />
                                          </a-form-item>
                                          <a-form-item label="Conversion Factor">
                                            <a-input v-model:value="row.conversion_factor" disabled/>
                                          </a-form-item>
                                          <a-form-item label="Stock UOM">
                                            <a-input v-model:value="row.stock_uom" disabled/>
                                          </a-form-item>
                                          <a-form-item label="Transfer Qty">
                                            <a-input v-model:value="row.transfer_qty" disabled/>
                                          </a-form-item>
                                        </v-col>
                                      </v-row>
                                    </v-container>
                                  </a-form>
                                </template>
                              </EditableTable>
                            </v-col>
                          </v-row>
                        </v-container>
                      </v-sheet>
                      <div class="d-flex py-4 gap-2">
                        <v-btn class="text-none" variant="flat" color="grey-lighten-2" @click="activateCallback('3')">Back</v-btn>
                        <v-btn class="text-none" variant="flat" color="blue-darken-2" @click="activateCallback('5')">Next</v-btn>
                      </div>
                    </StepPanel>
                  </StepItem>
                  <StepItem value="5">
                    <Step>Post Procedure</Step>
                    <StepPanel v-slot="{ activateCallback }">
                      <v-sheet>
                        <v-container>
                          <v-row>
                            <v-col>
                              <a-form-item label="Post Operative Diagnosis">
                                <a-textarea 
                                :disabled="records.current_encounter.status == 'Completed'"
                                :rows="4" 
                                v-model:value="procedureForms[selectedProcedure].custom_post_operative_diagnosis" 
                                @blur="event => {
                                  autoSave('Clinical Procedure', procedureForms[selectedProcedure].name, 'custom_post_operative_diagnosis', event.target.value)
                                }"/>
                              </a-form-item>
                            </v-col>
                          </v-row>
                          <v-divider></v-divider>
                          <v-row>
                            <v-col>
                              <h5>Medications</h5>
                              <EditableTable :columns="[
                                {label: 'Medicine', key: 'medication'},
                                {label: 'Frequency', key: 'dosage'},
                                {label: 'Duration', key: 'period'},
                                {label: 'Note', key: 'comment'},
                              ]"
                              :rows="encounterForm.drug_prescription"
                              @update="(items, row, isNew) => {
                                if(items && row)
                                  newChildRow({
                                    fieldName: 'drug_prescription', 
                                    rules: {
                                      medication: [{ required: true, message: 'Please choose a medicine!' }],
                                      drug_code: [{ required: true, message: 'Please choose a drug code!' }],
                                      dosage_form: [{ required: true, message: 'Please choose a dosage form!' }],
                                      dosage: [{ required: !row.dosage_by_interval, message: 'Please choose a dosage!' }],
                                      interval: [{ required: row.dosage_by_interval, message: 'Please choose a interval!' }],
                                      interval_uom: [{ required: row.dosage_by_interval, message: 'Please choose a interval uom!' }],
                                      period: [{ required: true, message: 'Please choose a period!' }],
                                    },
                                    items, row, isNew
                                  })
                              }"
                              @delete="rows => {deleteChildRow({fieldName: 'drug_prescription', rows})}"
                              dialogWidth="fit-content"
                              title="Medication"
                              >
                                <template v-slot:dialog="{ row }">
                                  <a-form layout="vertical">
                                    <v-container>
                                      <v-row>
                                        <v-col cols="12">
                                          <a-form-item label="Medicine">
                                            <a-select
                                            v-model:value="row.medication"
                                            :options="$resources.medications.data?.options"
                                            :fieldNames="{label: 'name', value: 'name'}"
                                            @change="(value, option) => {
                                              row.dosage = option.default_prescription_dosage
                                              row.period = option.default_prescription_duration
                                            }"
                                            show-search
                                            :loading="$resources.medications.list.loading"
                                            @search="(value) => {handleSearch(
                                              value, 
                                              $resources.medications, 
                                              {name: ['like', `%${value}%`]}, 
                                              {},
                                            )}"
                                            :filterOption="false"
                                            ></a-select>
                                          </a-form-item>
                                          <a-form-item label="Frequency">
                                            <LinkField 
                                            doctype="Prescription Dosage" 
                                            :value="row.dosage" 
                                            @change="(data) => { row.dosage = data }"
                                            />
                                          </a-form-item>
                                          <a-form-item label="Duration">
                                            <LinkField 
                                            doctype="Prescription Duration" 
                                            :value="row.period" 
                                            @change="(data) => { row.period = data }"
                                            />
                                          </a-form-item>
                                        </v-col>
                                      </v-row>
                                      <v-divider></v-divider>
                                      <v-row>
                                        <v-col>
                                          <a-form-item label="Note">
                                            <a-textarea v-model:value="row.comment" :rows="4"/>
                                          </a-form-item>
                                        </v-col>
                                      </v-row>
                                    </v-container>
                                  </a-form>
                                </template>
                              </EditableTable>
                            </v-col>
                          </v-row>
                        </v-container>
                      </v-sheet>
                      <div class="d-flex py-4">
                        <v-btn class="text-none" variant="flat" color="grey-lighten-2" @click="activateCallback('4')">Back</v-btn>
                      </div>
                    </StepPanel>
                  </StepItem>
                </Stepper>

                <div v-if="encounterForm.custom_encounter_state === 'Consultation' || encounterForm.custom_encounter_state === 'Follow-up'">
                  <v-container>
                    <v-row>
                      <v-col>
                        <a-form-item label="Chief Complaints">
                          <a-select
                          :disabled="records.current_encounter.status == 'Completed'"
                          v-model:value="encounterForm.symptoms"
                          :options="$resources.complaints.data?.options"
                          labelInValue
                          mode="multiple"
                          style="width: 100%"
                          @select="(value, option) => {
                            newChildRow({
                              parentDoctype: 'Patient Encounter',
                              fieldName: 'symptoms', 
                              row: {complaint: option.name}, 
                              isNew: true
                            })
                            this.$toast.add({ severity: 'success', summary: 'Saved', life: 3000 });
                          }"
                          @deselect="(value, option) => {
                            deleteChildRow({
                              parentDoctype: 'Patient Encounter',
                              fieldName: 'symptoms', 
                              rows: [option.name], 
                              filterField: 'complaint'
                            })
                            this.$toast.add({ severity: 'success', summary: 'Saved', life: 3000 });
                          }"
                          show-search
                          :loading="$resources.complaints.list.loading"
                          @search="(value) => {handleSearch(
                            value, 
                            $resources.complaints, 
                            {name: ['like', `%${value}%`]}, 
                            {},
                          )}"
                          :filterOption="false"
                          >
                            <template #dropdownRender="{ menuNode: menu }">
                              <v-nodes :vnodes="menu" />
                              <a-divider style="margin: 4px 0" />
                              <a-space style="padding: 4px 8px">
                                <a-input ref="inputRef" v-model:value="newComplaint" placeholder="Please enter complaint" />
                                <a-button type="text" @click="() => {
                                  addDoc({doctype: 'Complaint', complaints: newComplaint}, doc => {
                                    newComplaint = ''
                                    $resources.complaints.reload()
                                  }); 
                                }">
                                  <template #icon>
                                    <i class="mdi mdi-plus"></i>
                                  </template>
                                  Add Complaint
                                </a-button>
                              </a-space>
                            </template>
                          </a-select>
                        </a-form-item>
                        <a-form-item label="Duration">
                          <a-select
                          :disabled="records.current_encounter.status == 'Completed'"
                          v-model:value="encounterForm.custom_symptom_duration"
                          :options="$resources.symptomDurations.data?.options"
                          :fieldNames="{label: 'duration', value: 'name'}"
                          style="width: 100%"
                          @change="value => {
                            autoSave('Patient Encounter', encounterForm.name, 'custom_symptom_duration', value)
                          }"
                          show-search
                          :loading="$resources.symptomDurations.list.loading"
                          @search="(value) => {handleSearch(
                            value, 
                            $resources.symptomDurations, 
                            {duration: ['like', `%${value}%`]}, 
                            {},
                          )}"
                          :filterOption="false"
                          >
                            <template #dropdownRender="{ menuNode: menu }">
                              <v-nodes :vnodes="menu" />
                              <a-divider style="margin: 4px 0" />
                              <a-space style="padding: 4px 8px">
                                <a-input ref="inputRef" v-model:value="newSymptomDuration" placeholder="Please enter duration" />
                                <a-button type="text" @click="() => {
                                  addDoc({doctype: 'Symptom Duration', duration: newSymptomDuration}, doc => {
                                    newSymptomDuration = ''
                                    $resources.symptomDurations.reload()
                                    encounterForm.custom_symptom_duration = doc.name
                                  }); 
                                }">
                                  <template #icon>
                                    <i class="mdi mdi-plus"></i>
                                  </template>
                                  Add Symptom Duration
                                </a-button>
                              </a-space>
                            </template>
                          </a-select>
                        </a-form-item>
                        <a-form-item label="Present Illness">
                          <a-textarea 
                          :disabled="records.current_encounter.status == 'Completed'"
                          v-model:value="encounterForm.custom_symptoms_notes" 
                          :rows="4" 
                          @blur="event => {
                            autoSave('Patient Encounter', encounterForm.name, 'custom_symptoms_notes', event.target.value)
                          }"/>
                        </a-form-item>
                      </v-col>
                    </v-row>
                    <v-row v-if="encounterForm.custom_encounter_state === 'Consultation'">
                      <v-col>
                        <a-form-item label="Past Medical History">
                          <a-textarea 
                          :disabled="records.current_encounter.status == 'Completed'"
                          v-model:value="encounterForm.custom_past_medical_history" 
                          :rows="4" 
                          @blur="event => {
                            autoSave('Patient Encounter', encounterForm.name, 'custom_past_medical_history', event.target.value)
                          }"/>
                        </a-form-item>
                        <a-form-item label="Allergies">
                          <a-textarea 
                          :disabled="records.current_encounter.status == 'Completed'"
                          v-model:value="encounterForm.custom_allergies" 
                          :rows="4" 
                          @blur="event => {
                            autoSave('Patient Encounter', encounterForm.name, 'custom_allergies', event.target.value)
                          }"/>
                        </a-form-item>
                        <a-form-item label="Social History">
                          <a-textarea 
                          :disabled="records.current_encounter.status == 'Completed'"
                          v-model:value="encounterForm.custom_social_history" 
                          :rows="4" 
                          @blur="event => {
                            autoSave('Patient Encounter', encounterForm.name, 'custom_social_history', event.target.value)
                          }"/>
                        </a-form-item>
                      </v-col>
                    </v-row>
                    <v-row>
                      <v-col>
                        <a-form-item label="Physical Examination">
                          <a-textarea 
                          :disabled="records.current_encounter.status == 'Completed'"
                          v-model:value="encounterForm.custom_physical_examination" 
                          :rows="4" 
                          @blur="event => {
                            autoSave('Patient Encounter', encounterForm.name, 'custom_physical_examination', event.target.value)
                          }"/>
                        </a-form-item>
                      </v-col>
                    </v-row>

                    <v-row v-if="encounterForm.custom_encounter_state === 'Follow-up'">
                      <v-col>
                        <a-form-item label="Illness Progression">
                          <a-textarea 
                          :disabled="records.current_encounter.status == 'Completed'"
                          v-model:value="encounterForm.custom_illness_progression" 
                          :rows="4" 
                          @blur="event => {
                            autoSave('Patient Encounter', encounterForm.name, 'custom_illness_progression', event.target.value)
                          }"/>
                        </a-form-item>
                      </v-col>
                    </v-row>

                    <v-row>
                      <v-col>
                        <a-form-item label="Diagnosis">
                          <a-select
                          :disabled="records.current_encounter.status == 'Completed'"
                          v-model:value="encounterForm.diagnosis"
                          :options="$resources.diagnosis.data?.options"
                          mode="multiple"
                          style="width: 100%"
                          @select="(value, option) => {
                            newChildRow({
                              parentDoctype: 'Patient Encounter',
                              fieldName: 'diagnosis', 
                              row: {diagnosis: option.name}, 
                              isNew: true
                            })
                            this.$toast.add({ severity: 'success', summary: 'Saved', life: 3000 });
                          }"
                          @deselect="(value, option) => {
                            deleteChildRow({
                              parentDoctype: 'Patient Encounter',
                              fieldName: 'diagnosis', 
                              rows: [option.name], 
                              filterField: 'diagnosis'
                            })
                            this.$toast.add({ severity: 'success', summary: 'Saved', life: 3000 });
                          }"
                          show-search
                          :loading="$resources.diagnosis.list.loading"
                          @search="(value) => {handleSearch(
                            value, 
                            $resources.diagnosis, 
                            {name: ['like', `%${value}%`]}, 
                            {},
                          )}"
                          :filterOption="false"
                          >
                            <template #dropdownRender="{ menuNode: menu }">
                              <v-nodes :vnodes="menu" />
                              <a-divider style="margin: 4px 0" />
                              <a-space style="padding: 4px 8px">
                                <a-input ref="inputRef" v-model:value="newDiagnosis" placeholder="Please enter diagnosis" />
                                <a-button type="text" @click="() => {
                                  addDoc({doctype: 'Diagnosis', diagnosis: newDiagnosis}, doc => {
                                    newDiagnosis = ''
                                    $resources.diagnosis.reload()
                                  }); 
                                }">
                                  <template #icon>
                                    <i class="mdi mdi-plus"></i>
                                  </template>
                                  Add Diagnosis
                                </a-button>
                              </a-space>
                            </template>
                          </a-select>
                        </a-form-item>
                        <a-form-item label="Diagnosis Notes">
                          <a-textarea 
                          :disabled="records.current_encounter.status == 'Completed'"
                          v-model:value="encounterForm.custom_diagnosis_note" 
                          :rows="4" 
                          @blur="event => {
                          autoSave('Patient Encounter', encounterForm.name, 'custom_diagnosis_note', event.target.value)
                        }"/>
                        </a-form-item>
                      </v-col>
                    </v-row>
                  </v-container>
                  
                  <Fieldset class="mb-5" legend="Annotations" :toggleable="true">
                    <v-container>
                      <v-row>
                        <v-col>
                          <div class="d-flex gap-2">
                            <v-btn class="text-none" variant="flat" color="yellow-darken-1" 
                            :disabled="records.current_encounter.status == 'Completed'"
                            @click="() => {
                              annotationDoctype = encounterForm.doctype; 
                              encounterAnnotationType='Investigation'; 
                              procedureActive = true
                            }">Investigation Annotation</v-btn>
  
                            <v-btn class="text-none" variant="flat" color="red-darken-1" 
                            :disabled="records.current_encounter.status == 'Completed'"
                            @click="() => {
                              annotationDoctype = encounterForm.doctype; 
                              encounterAnnotationType='Treatment'; 
                              procedureActive = true
                            }">Treatment Annotation</v-btn>
                          </div>
                        </v-col>
                      </v-row>
                      <v-row v-if="encounterForm.custom_annotations.some(row => row.type == 'Investigation')">
                        <v-col>
                          <h3 class="mt-3">Investigation Annotations</h3>
                          <Galleria 
                          :value="encounterForm.custom_annotations.filter(row => row.type == 'Investigation')" 
                          :responsiveOptions="[{breakpoint: '1300px', numVisible: 4}, {breakpoint: '575px', numVisible: 1}]" 
                          :numVisible="5" 
                          :circular="true" 
                          containerStyle="max-width: 850px" 
                          :showItemNavigators="true" 
                          :showThumbnails="false"
                          :fullScreen="true"
                          v-model:visible="showInvestigationAnnotations"
                          v-model:activeIndex="activeIndex"
                          >
                            <template #item="slotProps">
                              <img 
                              :src="slotProps.item.image" 
                              :alt="slotProps.item.name" 
                              style="height: 100%;"
                              />
                            </template>
                            <template #thumbnail="slotProps">
                              <img :src="slotProps.item.image" :alt="slotProps.item.name" style="display: block" />
                            </template>
                          </Galleria>
                          <v-slide-group
                            class="pa-4"
                            selected-class="bg-success"
                            show-arrows
                          >
                            <v-slide-group-item 
                            v-for="(doc, index) of encounterForm.custom_annotations.filter(row => row.type == 'Investigation')" 
                            :key="index"
                            >
                              <img 
                              :src="doc.image" 
                              :alt="doc.name" 
                              style="cursor: pointer; height: 200px" 
                              @click="() => {activeIndex = index; showInvestigationAnnotations = true}"
                              />
                            </v-slide-group-item>
                          </v-slide-group>
                        </v-col>
                      </v-row>
                      <v-row v-if="encounterForm.custom_annotations.some(row => row.type == 'Treatment')">
                        <v-col>
                          <h3 class="mt-3">Annotations</h3>
                          <Galleria 
                          :value="encounterForm.custom_annotations.filter(row => row.type == 'Treatment')" 
                          :responsiveOptions="[{breakpoint: '1300px', numVisible: 4}, {breakpoint: '575px', numVisible: 1}]" 
                          :numVisible="5" 
                          :circular="true" 
                          containerStyle="max-width: 850px" 
                          :showItemNavigators="true" 
                          :showThumbnails="false"
                          :fullScreen="true"
                          v-model:visible="showTreatmentAnnotations"
                          v-model:activeIndex="activeIndex"
                          >
                            <template #item="slotProps">
                              <img 
                              :src="slotProps.item.image" 
                              :alt="slotProps.item.name" 
                              style="height: 100%;"
                              />
                            </template>
                            <template #thumbnail="slotProps">
                              <img :src="slotProps.item.image" :alt="slotProps.item.name" style="display: block" />
                            </template>
                          </Galleria>
                          <v-slide-group
                            class="pa-4"
                            selected-class="bg-success"
                            show-arrows
                          >
                            <v-slide-group-item 
                            v-for="(doc, index) of encounterForm.custom_annotations.filter(row => row.type == 'Treatment')" 
                            :key="index"
                            >
                              <img 
                              :src="doc.image" 
                              :alt="doc.name" 
                              style="cursor: pointer; height: 200px" 
                              @click="() => {activeIndex = index; showTreatmentAnnotations = true}"
                              />
                            </v-slide-group-item>
                          </v-slide-group>
                        </v-col>
                      </v-row>
                    </v-container>
                  </Fieldset>
  
                  <Fieldset legend="Plan" :toggleable="true">
                    <v-container>
                      <v-row>
                        <v-col>
                          <h5>Medications</h5>
                          <EditableTable :columns="[
                            {label: 'Medicine', key: 'medication'},
                            {label: 'Frequency', key: 'dosage'},
                            {label: 'Duration', key: 'period'},
                            {label: 'Note', key: 'comment'},
                          ]"
                          :rows="encounterForm.drug_prescription"
                          @update="(items, row, isNew) => {
                            if(items && row)
                              newChildRow({
                                fieldName: 'drug_prescription', 
                                rules: {
                                  medication: [{ required: true, message: 'Please choose a medicine!' }],
                                  drug_code: [{ required: true, message: 'Please choose a drug code!' }],
                                  dosage_form: [{ required: true, message: 'Please choose a dosage form!' }],
                                  dosage: [{ required: !row.dosage_by_interval, message: 'Please choose a dosage!' }],
                                  interval: [{ required: row.dosage_by_interval, message: 'Please choose a interval!' }],
                                  interval_uom: [{ required: row.dosage_by_interval, message: 'Please choose a interval uom!' }],
                                  period: [{ required: true, message: 'Please choose a period!' }],
                                },
                                items, row, isNew
                              })
                          }"
                          @delete="rows => {deleteChildRow({fieldName: 'drug_prescription', rows})}"
                          dialogWidth="fit-content"
                          title="Medication"
                          >
                            <template v-slot:dialog="{ row }">
                              <a-form layout="vertical">
                                <v-container>
                                  <v-row>
                                    <v-col cols="12">
                                      <a-form-item label="Medicine">
                                        <a-select
                                        v-model:value="row.medication"
                                        :options="$resources.medications.data?.options"
                                        :fieldNames="{label: 'name', value: 'name'}"
                                        @change="(value, option) => {
                                          row.dosage = option.default_prescription_dosage
                                          row.period = option.default_prescription_duration
                                        }"
                                        show-search
                                        :loading="$resources.medications.list.loading"
                                        @search="(value) => {handleSearch(
                                          value, 
                                          $resources.medications, 
                                          {name: ['like', `%${value}%`]}, 
                                          {},
                                        )}"
                                        :filterOption="false"
                                        ></a-select>
                                      </a-form-item>
                                      <a-form-item label="Frequency">
                                        <LinkField 
                                        doctype="Prescription Dosage" 
                                        :value="row.dosage" 
                                        @change="(data) => { row.dosage = data }"
                                        />
                                      </a-form-item>
                                      <a-form-item label="Duration">
                                        <LinkField 
                                        doctype="Prescription Duration" 
                                        :value="row.period" 
                                        @change="(data) => { row.period = data }"
                                        />
                                      </a-form-item>
                                    </v-col>
                                  </v-row>
                                  <v-divider></v-divider>
                                  <v-row>
                                    <v-col>
                                      <a-form-item label="Note">
                                        <a-textarea v-model:value="row.comment" :rows="4"/>
                                      </a-form-item>
                                    </v-col>
                                  </v-row>
                                </v-container>
                              </a-form>
                            </template>
                          </EditableTable>
                        </v-col>
                      </v-row>
                      <v-divider></v-divider>
                      <v-row>
                        <v-col>
                          <h5>Thrapies</h5>
                          <EditableTable :columns="[
                            {label: 'Therapy Type', key: 'therapy_type'},
                            {label: 'No of Sessions', key: 'no_of_sessions'},
                          ]"
                          :rows="encounterForm.therapies"
                          @update="(items, row, isNew) => {
                            if(items && row)
                              newChildRow({
                                fieldName: 'custom_allergies_table', 
                                rules: {therapy_type: [{ required: true, message: 'Please choose a therapy_type!' }]},
                                items, row, isNew
                              })
                          }"
                          @delete="rows => {deleteChildRow({fieldName: 'therapies', rows})}"
                          dialogWidth="fit-content"
                          title="Therapy"
                          >
                            <template v-slot:dialog="{ row }">
                              <a-form layout="vertical">
                                <v-container>
                                  <v-row>
                                    <v-col cols="12" lg="6">
                                      <a-form-item label="Therapy Type">
                                        <LinkField 
                                        doctype="Therapy Type" 
                                        :value="row.therapy_type" 
                                        @change="(data) => { 
                                          row.therapy_type = data 
                                        }"
                                        />
                                      </a-form-item>
                                      <a-form-item label="No of Sessions">
                                        <a-input v-model:value="row.no_of_sessions"/>
                                      </a-form-item>
                                    </v-col>
                                  </v-row>
                                </v-container>
                              </a-form>
                            </template>
                          </EditableTable>
                        </v-col>
                      </v-row>
                      <v-divider></v-divider>
                      <v-row>
                        <v-col>
                          <h5>Procedures</h5>
                          <EditableTable :columns="[
                            {label: 'Clinical Procedure', key: 'procedure'},
                            {label: 'Procedure Name', key: 'procedure_name'},
                            {label: 'Referring Practitioner', key: 'practitioner'},
                            {label: 'Date', key: 'date'},
                          ]"
                          :rows="encounterForm.procedure_prescription"
                          @update="(items, row, isNew) => {
                            if(items && row)
                              newChildRow({
                                fieldName: 'procedure_prescription', 
                                rules: {procedure: [{ required: true, message: 'Please choose a procedure!' }]},
                                items, row, isNew
                              })
                          }"
                          @delete="rows => {deleteChildRow({fieldName: 'procedure_prescription', rows})}"
                          dialogWidth="fit-content"
                          title="Procedure"
                          >
                            <template v-slot:dialog="{ row }">
                              <a-form layout="vertical">
                                <v-container>
                                  <v-row>
                                    <v-col cols="12" lg="6">
                                      <a-form-item label="Clinical Procedure">
                                        <LinkField 
                                        doctype="Clinical Procedure Template" 
                                        :value="row.procedure" 
                                        @change="(data) => { 
                                          row.procedure = data 
                                          $getValue({doctype: 'Item', fieldname:['template', 'medical_department'], filters:{name:data}})
                                          .then(response => {
                                            row.procedure_name = response.template
                                            row.department = response.medical_department
                                          })
                                        }"
                                        />
                                      </a-form-item>
                                      <a-form-item label="Procedure Name">
                                        <a-input v-model:value="row.procedure_name"/>
                                      </a-form-item>
                                      <a-form-item label="Department">
                                        <LinkField 
                                        doctype="Medical Department" 
                                        :value="row.department" 
                                        @change="(data) => { 
                                          row.department = data 
                                        }"
                                        />
                                      </a-form-item>
                                      <a-form-item label="Referring Practitioner">
                                        <a-select
                                        v-model:value="row.practitioner"
                                        :options="$resources.practitioners.data?.options"
                                        :fieldNames="{label: 'practitioner_name', value: 'name'}"
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
                                      </a-form-item>
                                      <a-form-item label="Service Request" v-if="row.service_request">
                                        <a-input v-model:value="row.service_request" disabled/>
                                      </a-form-item>
                                    </v-col>
                                    <v-col cols="12" lg="6">
                                      <a-form-item label="Date">
                                        <a-date-picker v-model:value="row.date" format="DD/MM/YYYY" class="w-full"/>
                                      </a-form-item>
                                      <a-form-item label="Comments">
                                        <a-textarea v-model:value="row.comments" :rows="4"/>
                                      </a-form-item>
                                    </v-col>
                                  </v-row>
                                </v-container>
                              </a-form>
                            </template>
                          </EditableTable>
                        </v-col>
                      </v-row>
                      <v-divider></v-divider>
                      <v-row>
                        <v-col>
                          <a-form-item label="Follow Up">
                            <a-textarea 
                            :disabled="records.current_encounter.status == 'Completed'"
                            v-model:value="encounterForm.custom_follow_up" 
                            :rows="4" 
                            @blur="event => {
                              autoSave('Patient Encounter', encounterForm.name, 'custom_follow_up', event.target.value)
                            }"/>
                          </a-form-item>
                        </v-col>
                      </v-row>
                    </v-container>
                  </Fieldset>
                </div>

              </a-form>
              <div v-else>
                <Accordion :value="['0', ...(procedureForms[0].name ? ['1'] : [])]" multiple>
                  <AccordionPanel value="0">
                    <AccordionHeader>Consultation</AccordionHeader>
                    <AccordionContent>
                      <v-container>
                        <h4 class="mb-4" v-if="encounterForm.symptoms.length > 0 || encounterForm.custom_symptom_duration || encounterForm.custom_symptoms_notes">Complaints</h4>
                        <v-row v-if="encounterForm.symptoms.length > 0 || encounterForm.custom_symptom_duration || encounterForm.custom_symptoms_notes">
                          <v-col v-if="encounterForm.symptoms.length > 0">
                            <h5>Symptoms</h5>
                            <h6 class="m-0">
                              {{ encounterForm.symptoms.map(symptom => symptom.complaint).join(", ") }}
                            </h6>
                          </v-col>
                          <v-col v-if="encounterForm.custom_symptom_duration">
                            <h5>Symptoms Duration</h5>
                            <h6 class="m-0">
                              {{ encounterForm.custom_symptom_duration }}
                            </h6>
                          </v-col>
                          <v-col v-if="encounterForm.custom_symptoms_notes">
                            <h5>Symptoms Notes</h5>
                            <h6 class="m-0">
                              {{ encounterForm.custom_symptoms_notes }}
                            </h6>
                          </v-col>
                        </v-row>

                        <v-divider class="mt-4" v-if="encounterForm.custom_physical_examination || encounterForm.custom_other_examination || encounterForm.custom_annotations.some(row => row.type == 'Investigation')"></v-divider>
                        <h4 class="mb-4" v-if="encounterForm.custom_physical_examination || encounterForm.custom_other_examination || encounterForm.custom_annotations.some(row => row.type == 'Investigation')">Pysical Examination & Investigation</h4>
                        <v-row v-if="encounterForm.custom_physical_examination || encounterForm.custom_other_examination || encounterForm.custom_annotations.some(row => row.type == 'Investigation')">
                          <v-col v-if="encounterForm.custom_physical_examination">
                            <h5>Physical Examination</h5>
                            <h6 class="m-0">
                              {{ encounterForm.custom_physical_examination }}
                            </h6>
                          </v-col>
                          <v-col v-if="encounterForm.custom_other_examination">
                            <h5>Other Examination</h5>
                            <h6 class="m-0">
                              {{ encounterForm.custom_other_examination }}
                            </h6>
                          </v-col>
                          <v-col v-if="encounterForm.custom_annotations.some(row => row.type == 'Investigation')">
                            <h5>Annotations</h5>
                            <Galleria 
                            :value="encounterForm.custom_annotations.filter(row => row.type == 'Investigation')" 
                            :responsiveOptions="[{breakpoint: '1300px', numVisible: 4}, {breakpoint: '575px', numVisible: 1}]" 
                            :numVisible="5" 
                            :circular="true" 
                            containerStyle="max-width: 850px" 
                            :showItemNavigators="true" 
                            :showThumbnails="false"
                            :fullScreen="true"
                            v-model:visible="showInvestigationAnnotations"
                            v-model:activeIndex="activeIndex"
                            >
                              <template #item="slotProps">
                                <img 
                                :src="slotProps.item.image" 
                                :alt="slotProps.item.name" 
                                style="height: 100%;"
                                />
                              </template>
                              <template #thumbnail="slotProps">
                                <img :src="slotProps.item.image" :alt="slotProps.item.name" style="display: block" />
                              </template>
                            </Galleria>
                            <v-slide-group
                              class="pa-4"
                              selected-class="bg-success"
                              show-arrows
                            >
                              <v-slide-group-item 
                              v-for="(doc, index) of encounterForm.custom_annotations.filter(row => row.type == 'Investigation')" 
                              :key="index"
                              >
                                <img 
                                :src="doc.image" 
                                :alt="doc.name" 
                                style="cursor: pointer; height: 100px" 
                                @click="() => {activeIndex = index; showInvestigationAnnotations = true}"
                                />
                              </v-slide-group-item>
                            </v-slide-group>
                          </v-col>
                        </v-row>

                        <v-divider class="mt-4" v-if="encounterForm.custom_illness_progression"></v-divider>
                        <h4 class="mb-4" v-if="encounterForm.custom_illness_progression">Illness Progression</h4>
                        <v-row v-if="encounterForm.custom_illness_progression">
                          <v-col>
                            <h6 class="m-0">
                              {{ encounterForm.custom_illness_progression }}
                            </h6>
                          </v-col>
                        </v-row>

                        <v-divider class="mt-4" v-if="encounterForm.diagnosis.length > 0 || encounterForm.custom_differential_diagnosis.length > 0 || encounterForm.custom_diagnosis_note"></v-divider>
                        <h4 class="mb-4" v-if="encounterForm.diagnosis.length > 0 || encounterForm.custom_differential_diagnosis.length > 0 || encounterForm.custom_diagnosis_note">Diagnosis</h4>
                        <v-row v-if="encounterForm.diagnosis.length > 0 || encounterForm.custom_differential_diagnosis.length > 0 || encounterForm.custom_diagnosis_note">
                          <v-col v-if="encounterForm.diagnosis.length > 0">
                            <h5>Diagnosis</h5>
                            <h6 class="m-0">
                              {{ encounterForm.diagnosis.map(diagnosis => diagnosis.diagnosis).join(", ") }}
                            </h6>
                          </v-col>
                          <v-col v-if="encounterForm.custom_differential_diagnosis.length > 0">
                            <h5>Differential Diagnosis</h5>
                            <h6 class="m-0">
                              {{ encounterForm.custom_differential_diagnosis.map(diagnosis => diagnosis.diagnosis).join(", ") }}
                            </h6>
                          </v-col>
                          <v-col v-if="encounterForm.custom_diagnosis_note">
                            <h5>Diagnosis Notes</h5>
                            <h6 class="m-0">
                              {{ encounterForm.custom_diagnosis_note }}
                            </h6>
                          </v-col>
                        </v-row>
                      </v-container>
                    </AccordionContent>
                  </AccordionPanel>
                  <AccordionPanel value="1" :disabled="!procedureForms[0].name">
                    <AccordionHeader>Procedure</AccordionHeader>
                    <AccordionContent>
                      <v-container>
                        <Accordion :value="procedureForms.map((p,i) => i)" multiple>
                          <AccordionPanel v-for="(procedure, index) in procedureForms" :value="index">
                            <AccordionHeader>{{ procedure.procedure_template }}</AccordionHeader>
                            <AccordionContent>
                              <v-container>
                                <h4 class="mb-4" v-if="procedure.practitioner || procedure.service_unit || procedure.notes">Procedure Info</h4>
                                <v-row v-if="procedure.practitioner || procedure.service_unit || procedure.notes">
                                  <v-col v-if="procedure.practitioner">
                                    <h5>Practitioner</h5>
                                    <h6 class="m-0">
                                      {{ procedure.practitioner }}
                                    </h6>
                                  </v-col>
                                  <v-col v-if="procedure.service_unit">
                                    <h5>Room</h5>
                                    <h6 class="m-0">
                                      {{ procedure.service_unit }}
                                    </h6>
                                  </v-col>
                                  <v-col v-if="procedure.notes">
                                    <h5>Notes</h5>
                                    <h6 class="m-0">
                                      {{ procedure.notes }}
                                    </h6>
                                  </v-col>
                                </v-row>

                                <v-divider class="mt-4" v-if="procedure.sample || procedure.custom_pre_operative_diagnosis"></v-divider>
                                <h4 class="mb-4" v-if="procedure.sample || procedure.custom_pre_operative_diagnosis">Pre Procedure</h4>
                                <v-row v-if="procedure.sample || procedure.custom_pre_operative_diagnosis">
                                  <v-col v-if="procedure.sample">
                                    <h5>Sample</h5>
                                    <h6 class="m-0">
                                      {{ procedure.sample }}
                                    </h6>
                                  </v-col>
                                  <v-col v-if="procedure.custom_pre_operative_diagnosis">
                                    <h5>Differential Diagnosis</h5>
                                    <h6 class="m-0">
                                      {{ procedure.custom_pre_operative_diagnosis }}
                                    </h6>
                                  </v-col>
                                  <v-col>
                                    <h5>Consent Signed?</h5>
                                    <h6 class="m-0">
                                      <i class="mdi mdi-check" v-if="procedure.custom_patient_consent_signature" />
                                    </h6>
                                  </v-col>
                                </v-row>

                                <v-divider class="mt-4" v-if="procedure.custom_general_data || procedure.custom_annotations?.lenfth > 0"></v-divider>
                                <h4 class="mb-4" v-if="procedure.custom_general_data || procedure.custom_annotations?.lenfth > 0">Procedure</h4>
                                <v-row v-if="procedure.custom_general_data || procedure.custom_annotations?.lenfth > 0">
                                  <v-col v-if="procedure.custom_general_data">
                                    <h5>General Data</h5>
                                    <div v-html="procedure.custom_general_data"></div>
                                  </v-col>
                                  <v-col v-if="procedure.custom_annotations.length > 0">
                                    <h5>Annotations</h5>
                                    <Galleria 
                                    :value="procedure.custom_annotations" 
                                    :responsiveOptions="[{breakpoint: '1300px', numVisible: 4}, {breakpoint: '575px', numVisible: 1}]" 
                                    :numVisible="5" 
                                    :circular="true" 
                                    containerStyle="max-width: 850px" 
                                    :showItemNavigators="true" 
                                    :showThumbnails="false"
                                    :fullScreen="true"
                                    v-model:visible="showInvestigationAnnotations"
                                    v-model:activeIndex="activeIndex"
                                    >
                                      <template #item="slotProps">
                                        <img 
                                        :src="slotProps.item.image" 
                                        :alt="slotProps.item.name" 
                                        style="height: 100%;"
                                        />
                                      </template>
                                      <template #thumbnail="slotProps">
                                        <img :src="slotProps.item.image" :alt="slotProps.item.name" style="display: block" />
                                      </template>
                                    </Galleria>
                                    <v-slide-group
                                      class="pa-4"
                                      selected-class="bg-success"
                                      show-arrows
                                    >
                                      <v-slide-group-item 
                                      v-for="(doc, index) of procedure.custom_annotations" 
                                      :key="index"
                                      >
                                        <img 
                                        :src="doc.image" 
                                        :alt="doc.name" 
                                        style="cursor: pointer; height: 100px" 
                                        @click="() => {activeIndex = index; showInvestigationAnnotations = true}"
                                        />
                                      </v-slide-group-item>
                                    </v-slide-group>
                                  </v-col>
                                </v-row>
                              </v-container>
                            </AccordionContent>
                          </AccordionPanel>
                        </Accordion>
                      </v-container>
                    </AccordionContent>
                  </AccordionPanel>
                </Accordion>
              </div>
            </template>
          </Card>
        </div>    
      </div>
      
      <div class="col-xl-3 col-12 ps-0 right-column">
        <Card class="p-0 mb-3" id="patient-history" style="overflow: hidden;">
          <template #title>
            Patient History <v-btn icon="mdi mdi-update" variant="text" class="ms-auto" @click="() => {medicalHistoryActive = true}"></v-btn>
          </template>
          <template #subtitle>
            Last updated: <span class="text-black font-weight-bold">{{ records.patient.custom_medical_history_last_updated }}</span>
          </template>
          <template #content>
            <ScrollPanel
            style="width: 100%; height: 500px"
            :dt="{
              bar: {
                background: 'black'
              }
            }"
            >
              <v-card class="p-0" id="allergies" variant="tonal" color="light-blue">
                <template v-slot:title>
                  Allergies {{ records.patient.custom_allergies_table.length > 0 ? '(' + records.patient.custom_allergies_table.length + ')' : ''}}
                </template>
                <template v-slot:text>
                  <div :class="{'d-none': records.patient.custom_allergies_table.length > 0}">
                    <v-empty-state
                      title="No Allergies"
                    ></v-empty-state>
                  </div>
                  <div class="py-3" v-for="(allergy, index) in records.patient.custom_allergies_table" :key="index">
                    <div class="d-flex align-items-center justify-content-between mb-1">
                      <h6>{{ allergy.type }}</h6>
                      <v-chip :color="getSeverity(allergy.severity).color" >
                        {{ getSeverity(allergy.severity).severity }}
                      </v-chip>
                    </div>
                    <p>{{ allergy.note }}</p>
                    <v-progress-linear
                      :color="getSeverity(allergy.severity).color"
                      :model-value="allergy.severity * 20"
                      rounded
                    ></v-progress-linear>
                  </div>
                </template>
              </v-card>
              <v-card class="p-0 mt-4" id="infected-diseases" variant="tonal" color="light-green">
                <template v-slot:title>
                  Medical History
                </template>
                <template v-slot:text>
                  <div :class="{'d-none': records.patient.custom_infected_diseases.length > 0}">
                    <v-empty-state
                      title="No Medical History"
                    ></v-empty-state>
                  </div>
                  <div
                    class="d-flex py-2"
                    :class="{'d-none': records.patient.custom_infected_diseases.length == 0}"
                    v-for="(item, index) in records.patient.custom_infected_diseases"
                    :key="index"
                  >
                    <div class="d-flex flex-column">
                      <h6 class="mb-0">{{ item.name1 }}</h6>
                      <p class="text-fade mb-0">{{ item.note }}</p>
                    </div>
                  </div>
                </template>
              </v-card>
              <v-card class="p-0 mt-4" id="surgical-history" variant="tonal" color="purple">
                <template v-slot:title>
                  Surgical History<a class="fs-6 float-end" :class="{'d-none': records.patient.custom_surgical_history_table.length <= 4}">See All</a>
                </template>
                <template v-slot:text>
                  <div :class="{'d-none': records.patient.custom_surgical_history_table.length > 0}">
                    <v-empty-state
                      title="No Surgical History"
                    ></v-empty-state>
                  </div>
                  <div
                    class="py-3"
                    :class="{'d-none': records.patient.custom_surgical_history_table.length == 0}"
                    v-for="(item, index) in records.patient.custom_surgical_history_table"
                    :key="index"
                  >
                    <div class="d-flex">
                      <div class="d-flex flex-column flex-grow-1">
                        <h6 class="mb-0">{{ item.surgery }}</h6>
                        <p class="text-fade mb-0">{{ item.date }}</p>
                      </div>
                      <div class="text-end fw-500">
                        <h6 class="mb-0">{{ item.practitioner }}</h6>
                      </div>
                    </div>
                    <p class="pt-3 m-0">{{ item.notes }}</p>
                  </div>
                </template>
              </v-card>
              <v-card class="p-0 mt-4" id="medications" variant="tonal" color="pink">
                <template v-slot:title>
                  Medications ({{ records.patient.custom_medications.length }})
                </template>
                <template v-slot:text>
                  <div :class="{'d-none': records.patient.custom_medications.length > 0}">
                    <v-empty-state
                      title="No Medications"
                    ></v-empty-state>
                  </div>
                  <div
                  class="d-flex align-items-center flex-column py-3"
                  :class="{'d-none': records.patient.custom_medications.length == 0}"
                  v-for="(medication, index) in records.patient.custom_medications"
                  :key="index"
                  >
                    <div class="d-flex flex-row flex-grow-1 justify-content-between w-100">
                      <h6 class="text-black mb-0 align-middle align-self-center">
                        {{ medication.name1 }}
                        <!-- <small class="text-fade">{{ medication.weight }}</small> -->
                      </h6>
                      <div class="text-fade mb-0">
                        <v-chip 
                        :color=" medication.is_active ? 'grey-lighten-1' : 'grey-darken-2'" 
                        :variant=" medication.is_active ? 'flat' : 'tonal'"
                        >
                          {{ medication.is_active ? 'Active' : 'Inactive'}}
                        </v-chip>
                      </div>
                    </div>
                    <div class="d-flex flex-row justify-content-between w-100 mt-1">
                      <p class="text-grey-darken-2 mb-0">{{ medication.reason }}</p>
                      <p class="text-grey-darken-2 text-center pe-2 mb-0">{{ medication.from_date }}</p>
                    </div>
                  </div>
                </template>
              </v-card>
              <v-card class="p-0 mt-4" id="habits" variant="tonal" color="teal">
                <template v-slot:title>
                  Habits / Social
                </template>
                <template v-slot:text>
                  <div :class="{'d-none': records.patient.custom_habits__social.length > 0}">
                    <v-empty-state
                      title="No Habits / Social"
                    ></v-empty-state>
                  </div>
                  <div
                    class="d-flex py-2"
                    :class="{'d-none': records.patient.custom_habits__social.length == 0}"
                    v-for="(item, index) in records.patient.custom_habits__social"
                    :key="index"
                  >
                    <div class="d-flex flex-column">
                      <h6 class="mb-0">{{ item.habit }}</h6>
                      <p class="text-fade mb-0">{{ item.note }}</p>
                    </div>
                  </div>
                </template>
              </v-card>
              <v-card class="p-0 mt-4" id="family-history" variant="tonal" color="brown">
                <template v-slot:title>
                  Family History
                </template>
                <template v-slot:text>
                  <div :class="{'d-none': records.patient.custom_family_history.length > 0}">
                    <v-empty-state
                      title="No Family History"
                    ></v-empty-state>
                  </div>
                  <div
                    class="d-flex py-2"
                    :class="{'d-none': records.patient.custom_family_history.length == 0}"
                    v-for="(item, index) in records.patient.custom_family_history"
                    :key="index"
                  >
                    <div class="d-flex flex-column">
                      <h6 class="mb-0">{{ item.name1 }}</h6>
                      <p class="text-fade mb-0">{{ item.note }}</p>
                    </div>
                  </div>
                </template>
              </v-card>
              <v-card class="p-0 mt-4" id="risk-factors" variant="tonal" color="deep-orange">
                <template v-slot:title>
                  Risk Factors
                </template>
                <template v-slot:text>
                  <div :class="{'d-none': records.patient.custom_risk_factors_table.length > 0}">
                    <v-empty-state
                      title="No Risk Factors"
                    ></v-empty-state>
                  </div>
                  <div class="py-3" v-for="(risk, index) in records.patient.custom_risk_factors_table" :key="index">
                    <div class="d-flex ">
                      <h6>{{ risk.type }}</h6>
                      <v-chip label class="ms-auto" :color="getSeverity(risk.severity).color">
                        {{ getSeverity(risk.severity).risk }}
                      </v-chip>
                    </div>
                    <p class="mb-0">{{ risk.note }}</p>
                  </div>
                </template>
              </v-card>

            </ScrollPanel>
          </template>
        </Card>
        <div class="pe-0">
          <Card class="p-0 mb-3 border-bottom-title h-auto" id="attachments" style="overflow: hidden;">
            <template #title>
              Attachments
              <v-btn class="float-end text-orange text-none" prepend-icon="pi pi-plus" variant="plain" @click="() => {addAttachmentActive = true}">Add</v-btn>
            </template>
            <template #content>
              <div :class="{'d-none': records.attachments.length > 0}">
                <v-empty-state title="No Attachments"></v-empty-state>
              </div>
              <div class="flex flex-col">
                <v-list>
                  <v-list-item
                    v-for="(doc, index) in records.attachments"
                    :key="index"
                    :value="doc.name"
                    color="primary"
                    @click="openNewWindow(doc.attachment)"
                    :active-class="''"
                    :active="false"
                  >
                    <template v-slot:prepend>
                      <Image v-if="doc.type === 'image'" :src="doc.attachment" width="24"/>
                      <i v-else-if="doc.type === 'pdf' || doc.type === 'word'" :class="`pi pi-file-${doc.type}`" style="font-size: 1.5rem" />
                    </template>

                    <v-list-item-title class="flex ml-4" >
                      <div class="d-flex flex-column flex-grow-1">
                        <h4 class="m-0">{{ doc.attachment_name }}</h4>
                      </div>
                      <div class="text-end fw-500">
                        <p class="text-fade mb-0">{{ doc.creation }}</p>
                      </div>
                    </v-list-item-title>
                  </v-list-item>
                </v-list>
              </div>
            </template>
            <!-- <template #footer>
              <a v-if="records.attachments.length > 4" class="float-end" >View All</a>
            </template> -->
          </Card>
        </div>
      </div> 
      <!-- <v-divider color="black" inset class="my-6" style="max-width: calc(100% - 180px)"></v-divider> -->
      
    </div>

    <div class="dialogs">
      <vitalSignsDialog 
      :isOpen="vitalSignsActive" 
      @update:isOpen="vitalSignsActive = $event" 
      @show-alert="showAlert" 
      :appointment="records.appointment"
      :callback="fetchRecords"
      />
      <patientEncounterDialog 
      :isOpen="pastVisitsActive" 
      @update:isOpen="pastVisitsActive = $event" 
      @show-alert="showAlert" 
      :form="pastVisitEditRow"
      />
      <labTestDialog 
      :isOpen="labTestActive" 
      @update:isOpen="labTestActive = $event" 
      @show-alert="showAlert" 
      :appointment="records.appointment"
      />
      <medicationRequestDialog 
      :isOpen="medicationRequestActive" 
      @update:isOpen="medicationRequestActive = $event" 
      @show-alert="showAlert" 
      :appointment="records.appointment"
      />
      <addAttachmentDialog 
      :isOpen="addAttachmentActive" 
      @update:isOpen="addAttachmentActive = $event" 
      @show-alert="showAlert" 
      doctype="Patient Encounter Attachments"
      :parentType="encounterForm.doctype"
      :parent="encounterForm.name"
      fieldName="custom_attachments"
      :isChild="true"
      :callback="fetchRecords"
      />
      <procedureDialog 
      :isOpen="procedureActive" 
      @update:isOpen="procedureActive = $event" 
      @show-alert="showAlert" 
      :doctype="annotationDoctype"
      :docname="annotationDoctype == 'Patient Encounter' ? encounterForm.name : procedureForms[selectedProcedure]?.name"
      :encounterType="annotationDoctype == 'Patient Encounter' ? encounterAnnotationType : ''"
      :patient="records.patient.name"
      />
      <serviceRequestDialog 
      :isOpen="serviceRequestActive" 
      @update:isOpen="serviceRequestActive = $event" 
      @show-alert="showAlert" 
      :patient="records.patient"
      :encounter="records.current_encounter"
      />
      <patientMedicalHistoryDialog 
      :isOpen="medicalHistoryActive" 
      @update:isOpen="medicalHistoryActive = $event" 
      @show-alert="showAlert" 
      :patient="records.patient"
      />
      <appointmentNoteDialog 
      :isOpen="appointmentNoteActive" 
      @update:isOpen="appointmentNoteActive = $event" 
      @show-alert="showAlert" 
      :appointmentId="records.appointment?.name"
      />
      <appointmentInvoiceDialog 
      :isOpen="appointmentInvoiceActive" 
      @update:isOpen="appointmentInvoiceActive = $event" 
      @show-alert="showAlert" 
      :appointment="{...this.records.appointment, invoice_items: this.records.appointment?.custom_invoice_items}"
      />
      <v-dialog v-model="consentFormDialog" width="auto">
        <v-toolbar color="red-accent-4" :style="{borderTopRightRadius: '12px', borderTopLeftRadius: '12px'}">
          <v-btn variant="text" icon="mdi mdi-close" @click="consentFormDialog = false"></v-btn>
          
          <v-toolbar-title>Consent Form</v-toolbar-title>
          
          <v-spacer></v-spacer>
          
          <v-toolbar-items v-if="records.current_encounter.status != 'Completed'">
            <v-btn
              class="text-none" 
              text="Clear"
              variant="text"
              @click="clearSignature"
            ></v-btn>
            <v-btn
              class="text-none" 
              text="Save"
              variant="text"
              @click="saveSignature"
            ></v-btn>
          </v-toolbar-items>
        </v-toolbar>

        <v-card>
          <pdfSignature :html="consentFormHtml" ref="consentForm"/>
        </v-card>

      </v-dialog>

      <v-dialog v-model="sergicalProcedureActive" width="auto">
        <v-toolbar color="light-blue" :style="{borderTopRightRadius: '12px', borderTopLeftRadius: '12px'}">
          <v-btn variant="text" icon="mdi mdi-close" @click="sergicalProcedureActive = false"></v-btn>
          
          <v-toolbar-title>Sergical Procedure</v-toolbar-title>
          
          <v-spacer></v-spacer>
          
          <v-toolbar-items v-if="records.current_encounter.status != 'Completed'">
            <v-btn
              class="text-none" 
              text="Save"
              variant="text"
              @click="saveSergicalHistory"
            ></v-btn>
          </v-toolbar-items>
        </v-toolbar>

        <v-card rounded="lg">
          <v-card-text>

            <a-form layout="vertical">
              <a-form-item label="Procedure Name">
                <LinkField 
                doctype="Clinical Procedure Template" 
                :value="procedureProcedureName" 
                mode="multiple"
                :style="{minWidth: '400px', maxWidth: '600px'}"
                @change="(data) => { 
                  procedureProcedureName = data 
                }"
                />
              </a-form-item>
              <a-form-item label="Indication">
                <LinkField 
                doctype="Surgery Indication" 
                :value="procedureIndication" 
                mode="multiple"
                :style="{minWidth: '400px', maxWidth: '600px'}"
                @change="(data) => { 
                  procedureIndication = data 
                }"
                />
              </a-form-item>
              <a-form-item label="Finding">
                <a-textarea 
                :disabled="records.current_encounter.status == 'Completed'"
                :rows="4" 
                v-model:value="procedureFinding" 
                />
              </a-form-item>
              <a-form-item label="Operative Notes">
                <a-textarea 
                :disabled="records.current_encounter.status == 'Completed'"
                :rows="4" 
                v-model:value="procedureOperativeNote" 
                />
              </a-form-item>
            </a-form>
          </v-card-text>
        </v-card>

      </v-dialog>
    </div>
  </div>
</template>

<script>
import dayjs from 'dayjs';
import { VEmptyState } from 'vuetify/labs/VEmptyState';
import { VSlideGroup, VSlideGroupItem } from 'vuetify/components/VSlideGroup';
import { VProgressLinear } from 'vuetify/components/VProgressLinear';
import { VChip } from 'vuetify/components/VChip';
import { VSpacer } from 'vuetify/components/VGrid';
import { VSelect } from 'vuetify/components/VSelect';
import { VStepper, VStepperHeader, VStepperItem, VStepperActions, VStepperWindow, VStepperWindowItem } from 'vuetify/components/VStepper';
import { VSheet } from 'vuetify/components/VSheet';
import { VHover } from 'vuetify/components/VHover';
import { VAvatar } from 'vuetify/components/VAvatar';
import { VToolbar, VToolbarItems, VToolbarTitle } from 'vuetify/components/VToolbar';
import { VIcon } from 'vuetify/components/VIcon';
import { VBtnGroup } from 'vuetify/components/VBtnGroup';
import { VList, VListItem, VListItemTitle } from 'vuetify/components/VList';

import EditableTable from '@/components/editableTable.vue';

import GifLoader from "@/components/GifLoader.vue";
// import LottieLoader from "@/components/LottieLoader.vue";
import gifUrl from "@/assets/img/animations/loading-animation.gif";

import { ref, reactive, computed, defineComponent } from 'vue';
import { Form } from 'ant-design-vue';

import encounterRecords from '@/assets/json/encounterrecords.json'
import pdfSignature from '@/components/pdfSignature.vue';
// import soundImage from '@/assets/img/sound.png';
// import lungsImage from '@/assets/img/lungs.png';
// import celsiusImage from '@/assets/img/celsius.png';
import kneeImage from '@/assets/img/knee.png';
import stomachImage from '@/assets/img/stomach.png';
import tongueImage from '@/assets/img/tongue.png';

import Accordion from 'primevue/accordion';
import AccordionPanel from 'primevue/accordionpanel';
import AccordionHeader from 'primevue/accordionheader';
import AccordionContent from 'primevue/accordioncontent';

import { QuillEditor } from '@vueup/vue-quill'

export default {
  inject: ['$socket', '$call', '$getValue'],
  components: {
    VSlideGroup, VSlideGroupItem, VProgressLinear, VChip, VEmptyState, VAvatar, VIcon, VBtnGroup, QuillEditor,
    VSelect, VStepper, VStepperHeader, VStepperItem, VStepperActions, VStepperWindow, VStepperWindowItem, VSheet,
    Image, VHover, pdfSignature, VToolbar, VToolbarItems, VToolbarTitle, VSpacer, VList, VListItem, VListItemTitle,
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
    medications() { return { 
      type: 'list', 
      doctype: 'Medication', 
      fields: ['*'], 
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
    symptomDurations() { return { 
      type: 'list', 
      doctype: 'Symptom Duration', 
      fields: ['name', 'duration'], 
      auto: true,
      orderBy: 'name',
      pageLength: 30,
      url: 'frappe.desk.reportview.get', 
      transform(data) {
        if(data.values.length == 0)
          data.options = []
        else
          data.options = this.transformData(data.keys, data.values);  // Transform the result into objects
        return data
      }
    }},
    practitioners() { return { 
      type: 'list', 
      doctype: 'Healthcare Practitioner', 
      fields: ['name', 'practitioner_name', 'department'], 
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
    complaints() { return { 
      type: 'list', 
      doctype: 'Complaint', 
      fields: ['name'], 
      auto: true,
      orderBy: 'name',
      pageLength: 10,
      url: 'frappe.desk.reportview.get', 
      transform(data) {
        if(data.values.length == 0)
          data.options = []
        else{
          data.options = this.transformData(data.keys, data.values);  // Transform the result into objects
          for (let d of data.options) {
            d.label = d.name
            d.value = d.name
          }
        }
        return data
      }
    }},
    diagnosis() { return { 
      type: 'list', 
      doctype: 'Diagnosis', 
      fields: ['name'], 
      auto: true,
      orderBy: 'name',
      pageLength: 10,
      url: 'frappe.desk.reportview.get', 
      transform(data) {
        if(data.values.length == 0)
          data.options = []
        else{
          data.options = this.transformData(data.keys, data.values);  // Transform the result into objects
          for (let d of data.options) {
            d.label = d.name
            d.value = d.name
          }
        }
        return data
      }
    }},
    
    appointments() { return { 
      type: 'list', 
      doctype: 'Patient Appointment', 
      fields: ['*'], 
      filters: {patient: this.records.patient.name},
      auto: true,
      orderBy: 'appointment_date desc',
      url:'healthcare_doworks.api.methods.check_availability',
      pageLength: 1000,
      transform(data) {
        return this.adjustAppointments(data)
      },
    }},
    consultations() { return { 
      type: 'list', 
      doctype: 'Patient Encounter', 
      fields: ['name', 'encounter_date', 'practitioner_name', 'custom_appointment_category', 'status'], 
      filters: {patient: this.records.patient.name, custom_appointment_category: ['!=', 'Procedure']},
      auto: true,
      orderBy: 'encounter_date desc',
      pageLength: 1000,
    }},
    procedures() { return { 
      type: 'list', 
      doctype: 'Clinical Procedure', 
      fields: ['name', 'start_date', 'practitioner_name', 'procedure_template', 'custom_patient_encounter', 'status'], 
      filters: {patient: this.records.patient.name},
      auto: true,
      orderBy: 'start_date desc',
      pageLength: 1000,
    }},
    invoices() { return { 
      type: 'list', 
      doctype: 'Sales Invoice', 
      filters: {customer: this.records.patient.customer},
      auto: true,
      orderBy: 'posting_date desc',
      pageLength: 1000,
      url:'healthcare_doworks.api.methods.invoices',
    }},
  },
  setup() {
    let encounterForm = reactive({
      doctype: 'Patient Encounter',
      name: '',
      custom_encounter_start_time: dayjs(),
      procedure_date: dayjs(),
      symptoms: [],
      custom_symptom_duration: '',
      custom_symptoms_notes: '',
      custom_physicalExamination: '',
      custom_otherExamination: '',
      diagnosis: [],
      custom_differential_diagnosis: [],
      custom_diagnosis_note: '',
      appointment: '',
      appointment_type: '',
      custom_appointment_category: '',
      custom_encounter_state: '',
      patient: '',
      patient_name: '',
      patient_sex: '',
      patient_age: '',
      practitioner: '',
      practitioner_name: '',
      medical_department: '',
      custom_illness_progression: '',
    });

    let procedureForms = reactive([{
      doctype: 'Clinical Procedure',
      name: '',
      custom_patient_consent_signature: '',

      custom_patient_encounter: '',
      procedure_template: '',
      
      patient: '',
      patient_name: '',
      patient_sex: '',
      patient_age: '',
      inpatient_record: '',
      notes: '',
      practitioner: '',
      practitioner_name: '',
      medical_department: '',
      service_unit: '',
      start_date: dayjs(),
      start_time: dayjs(),
      sample: '',

      custom_pre_operative_diagnosis: '',
      custom_post_operative_diagnosis: '',

      custom_annotations: [],
    }]);

    return {
      encounterForm,
      procedureForms,
    };
  },
  data() {
    return {
      gifUrl:gifUrl,
      kneeImage:kneeImage,
      stomachImage:stomachImage,
      tongueImage:tongueImage,

      appointmentForm: {},
      quillEditorOptions: {
        theme: 'snow',
        modules: {
          toolbar: [
            [{ header: [1, 2, 3, false] }],
            [{ size: ['small', false, 'large', 'huge'] }],
            ['bold', 'italic', 'underline', 'strike'],
            [{ color: [] }, { background: [] }],
            ['blockquote', 'code-block'],
            [{ direction: 'rtl' }],
            ['link', 'image'],
            [{ list: 'ordered'}, { list: 'bullet' }, { list: 'check' }],
            [{ align: [] }],
            [{ indent: '-1'}, { indent: '+1' }],
          ],
        },
      },

      newSymptomDuration: '',
      newComplaint: '',
      newDiagnosis: '',

      isLoading: false,
      consentFormDialog: false,
      showProcedureAnnotations: false,
      showInvestigationAnnotations: false,
      showTreatmentAnnotations: false,
      activeIndex: 0,
      consentFormHtml: '',
      currentFormStep: 0,
      selectedProcedure: 0,
      currentVS: {
        name: '',
        pulse: "-",
        respiratory_rate: "-",
        custom_saturation_rate: '-',
        bp_systolic: "-",
        bp_diastolic: "-",
        temperature: "-",
        signs_date: '-',
      },
      newProcedureForm: {procedure_template: ''},
      records: ref(encounterRecords),
      isAffixed:false,
      pastVisitEditRow: '',
      practitionerConflict: false,
      vitalSignsActive: false,
      pastVisitsActive: false,
      serviceRequestActive: false,
      labTestActive: false,
      medicationRequestActive: false,
      addAttachmentActive: false,
      procedureActive: false,
      medicalHistoryActive: false,
      appointmentNoteActive: false,
      appointmentInvoiceActive: false,
      sergicalProcedureActive: false,

      procedureProcedureName: [],
      procedureIndication: [],
      procedureFinding: '',
      procedureOperativeNote: '',

      alertMessage: '',
      alertType: '', // 'success' or 'error'
      alertActive: false,

      formOptions: [
        {label:'Consultation', value:'Consultation'}, 
        {label:'Procedure', value:'Procedure'}, 
        {label:'Follow-up', value:'Follow-up'}, 
        {label:'Session', value:'Session'}
      ],
      previousState: '',
      annotationDoctype: '',
      encounterAnnotationType: '',
      
    };
  },
  computed: {
    actions() {
      return [
        ...(this.records.current_encounter?.status != 'Completed' ? [{
          label: 'Submit',
          icon: 'mdi mdi-check',
          command: () => {
            this.submitEncounter()
          }
        }] : [{
          label: 'Cancel',
          icon: 'mdi mdi-cancel',
          command: () => {
            this.cancelEncounter()
          }
        }]),
        {
          label: 'Invoice',
          icon: 'mdi mdi-invoice-text-outline',
          command: () => {
            this.appointmentInvoiceActive = true
          }
        },
        {
          label: 'Note',
          icon: 'mdi mdi-text',
          command: () => {
            this.appointmentNoteActive = true
          }
        },
      ]
    },
  },
  created() {
    this.isLoading = true;
    this.fetchRecords();
    this.$socket.on('patient_updated', doc => {
      if(doc.name == this.records.patient.name){
        doc.dob = dayjs(doc.dob).format('DD/MM/YYYY')
        doc.age = ' (' + dayjs().diff(doc.dob, 'y') + 'yrs), '
        this.records.patient = doc
      }
    })

    this.$socket.on('patient_encounter_updated', doc => {
      if(doc.name == this.$route.params.encounterId){
        doc.custom_encounter_start_time = dayjs(doc.custom_encounter_start_time)
        doc.diagnosis = doc.diagnosis.map(value => {
          value.label = value.diagnosis
          value.value = value.diagnosis
          return value
        })
        doc.custom_differential_diagnosis = doc.custom_differential_diagnosis.map(value => {
          value.label = value.diagnosis
          value.value = value.diagnosis
          return value
        })
        doc.symptoms = doc.symptoms.map(value => {
          value.label = value.complaint
          value.value = value.complaint
          return value
        })
        this.encounterForm = {...this.encounterForm, ...doc}
        this.previousState = this.encounterForm.custom_encounter_state
        this.records.current_encounter = doc
      }
    })

    this.$socket.on('clinical_procedure_updated', doc => {
      let index = 0
      if(this.procedureForms.some((procedure, i) => {index = i; return procedure.name == doc.name})){
        doc.start_time = dayjs(doc.start_date + ' ' + doc.start_time)
        doc.start_date = dayjs(doc.start_date)
        this.procedureForms[index] = doc
        this.records.procedures[index] = doc
      }
    })

    this.$socket.on('services', response => {
      let thisPatient = false
      this.records.services = response.filter(service => {
        thisPatient = true
        return service.patient == this.encounterForm.patient
      })
      if(thisPatient) 
        this.$toast.add({ severity: 'success', summary: 'Update', detail: 'Service Request updated', life: 3000 });
    })
  },
  mounted(){
    
  },
  methods: {
    affixChenge(affixed){
      this.isAffixed = affixed
    },
    getSeverity(value){
      if(value > 3)
        return {risk: 'High', color: 'pink-accent-3', severity: 'Severe'}
      else if( value > 1)
        return {risk: 'Mediume', color: 'orange-darken-1', severity: 'Moderate'}
      return {risk: 'Low', color: 'green', severity: 'Mild'}
    },
    fetchRecords(){
      this.$call('healthcare_doworks.api.methods.patient_encounter_records', {encounter_id: this.$route.params.encounterId})
      .then(response => {
        response.current_encounter.custom_encounter_start_time = dayjs(response.current_encounter.custom_encounter_start_time)
        if(response.procedures.length > 0 ){
          this.procedureForms = response.procedures.map(value => {
            value.start_time = dayjs(value.start_date + ' ' + value.start_time)
            value.start_date = dayjs(value.start_date)
            return value
          })
        }

        response.current_encounter.diagnosis = response.current_encounter.diagnosis.map(value => {
          value.label = value.diagnosis
          value.value = value.diagnosis
          return value
        })
        response.current_encounter.custom_differential_diagnosis = response.current_encounter.custom_differential_diagnosis.map(value => {
          value.label = value.diagnosis
          value.value = value.diagnosis
          return value
        })
        response.current_encounter.symptoms = response.current_encounter.symptoms.map(value => {
          value.label = value.complaint
          value.value = value.complaint
          return value
        })
        this.encounterForm = {...this.encounterForm, ...response.current_encounter}
        this.previousState = this.encounterForm.custom_encounter_state
        response.patient.dob = dayjs(response.patient.dob).format('DD/MM/YYYY')
        response.patient.age = ' (' + dayjs().diff(response.patient.dob, 'y') + 'yrs), '
        response.encounters = response.encounters.map((encounter, index) => {
          encounter.encounter_date = dayjs(encounter.encounter_date).format('DD/MM/YYYY')
          encounter.diagnosisArray = encounter.diagnosis.map((value, index) => {
            return value.diagnosis
          })
          encounter.symptomsArray = encounter.symptoms.map((value, index) => {
            return value.complaint
          })
          encounter.reasons = encounter.diagnosisArray.join(', ')
          return encounter
        })
        response.attachments = response.attachments.map((attachment, index) => {
          attachment.creation = dayjs(attachment.creation).format('DD/MM/YYYY')
          return attachment
        })
        if(response.vitalSigns.length > 0){
          response.vitalSigns = response.vitalSigns.map((value, index) => {
            value.signs_date = dayjs(value.signs_date).format('DD/MM/YYYY')
            return value
          })
          this.currentVS = response.vitalSigns.filter(vs => vs.appointment == response.appointment.name)[0];
        }
        if(response.appointment && response.appointment?.practitioner !== this.$myresources.user.practitioner){
          this.practitionerConflict = true
        }
        this.records = response
        this.isLoading = false;
      })
      .catch(error => {
        this.showAlert(error.message, 'error')
        console.error('Error fetching records:', error);
      });
    },
    showAlert(message, type) {
      this.alertMessage = message;
      this.alertType = type;
      this.alertActive = true;
    },
    cancelEncounter() {
      this.$call('healthcare_doworks.api.methods.cancel_encounter', {encounter: this.$route.params.encounterId})
      .then(response => {
        this.$toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Encounter cancelled',
          life: 3000 // Duration in ms
        });
      }).catch(error => {
        this.showAlert(error.message, 'error')
      });
    },
    submitEncounter() {
      this.$call('healthcare_doworks.api.methods.submit_encounter', {encounter: this.$route.params.encounterId})
      .then(response => {
        this.$toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Encounter submitted',
          life: 3000 // Duration in ms
        });
      }).catch(error => {
        this.showAlert(error.message, 'error')
      });
    },
    autoSave(doctype, name, fieldname, value) {
      this.$call('frappe.client.set_value', {doctype, name, fieldname, value})
      .then(response => {
        this.$toast.add({ severity: 'success', summary: 'Saved', life: 3000 });
      }).catch(error => {
        this.showAlert(error.message, 'error')
      });
    },
    newChildRow({parentDoctype ,prarentDocname, fieldName, rules, items, row, isNew}) {
      const { validate } = Form.useForm(row, rules);
      validate().then(() => {
        let formClone = {...row}
        formClone.date = dayjs(row.date).format('YYYY-MM-DD')
        delete formClone.modified
        delete formClone.modified_by
        delete formClone.name
        if(isNew){
          this.$call('healthcare_doworks.api.general_methods.add_child_entry', {
            parent_doctype: parentDoctype || 'Patient Encounter', 
            parent_doc_name: prarentDocname || this.encounterForm.name, 
            child_table_fieldname: fieldName, 
            child_data: formClone
          }).then(response => {
          }).catch(error => {
            this.showAlert(error.message, 'error')
          });
        }
        else{
          this.$call('healthcare_doworks.api.general_methods.modify_child_entry', {
            parent_doctype: parentDoctype || 'Patient Encounter', 
            parent_doc_name: prarentDocname || this.encounterForm.name, 
            child_table_fieldname: fieldName, 
            filters: {name: row.name}, 
            update_data: formClone
          }).then(response => {
          }).catch(error => {
            this.showAlert(error.message, 'error')
          });
        }
      })
      .catch(err => {
        console.log('error', err);
      });
    },
    deleteChildRow({parentDoctype, prarentDocname, fieldName, rows, filterField}) {
      rows.forEach(row => {
        this.$call('healthcare_doworks.api.general_methods.delete_child_entry', {
          parent_doctype: parentDoctype || 'Patient Encounter', 
          parent_doc_name: prarentDocname || this.encounterForm.name, 
          child_table_fieldname: fieldName, 
          filters: {[filterField || 'name']: row}
        }).then(response => {
        }).catch(error => {
          this.showAlert(error.message, 'error')
        })
      })
    },
    encounterSelect(encounter) {
      this.$router.push({ name: 'patient-encounter', params: { encounterId: encounter } });
      this.fetchRecords()
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
    visitLogSelect(row) {
      this.pastVisitEditRow = row.data;
      this.pastVisitsActive = true;
    },
    confirmDelete(event) {
      this.$confirm.require({
        target: event.currentTarget,
        group: 'delete-procedure',
        message: 'Are you sure you want to delete this procedure?',
        icon: 'pi pi-info-circle',
        acceptLabel: 'Delete',
        rejectLabel: 'Cancel',
        acceptProps: {
          severity: 'danger'
        },
        rejectProps: {
          severity: 'secondary'
        },
        accept: () => {
          if(this.procedureForms.length == 1){
            if(this.encounterForm.custom_appointment_category == 'Procedure' || this.encounterForm.custom_appointment_category == 'First Time'){
              this.previousState = 'Consultation'
              this.encounterForm.custom_encounter_state = 'Consultation'
            }
            else{
              this.previousState = this.encounterForm.custom_appointment_category
              this.encounterForm.custom_encounter_state = this.encounterForm.custom_appointment_category
            }
            this.autoSave('Patient Encounter', this.encounterForm.name, 'custom_encounter_state', this.encounterForm.custom_encounter_state)
          }

          this.$call('frappe.client.delete', {doctype: 'Clinical Procedure', name: this.procedureForms[this.selectedProcedure]?.name})
          .then(response => {
            this.$toast.add({ 
              severity: 'success', 
              summary: 'Deleted', 
              detail: 'Procedure: ' + this.procedureForms[this.selectedProcedure]?.name + ' was deleted successfully', 
              life: 3000 
            });

            this.selectedProcedure = 0

            this.procedureForms = [{
              doctype: 'Clinical Procedure',
              name: '',
              custom_patient_consent_signature: '',

              custom_patient_encounter: '',
              procedure_template: '',
              
              patient: '',
              patient_name: '',
              patient_sex: '',
              patient_age: '',
              inpatient_record: '',
              notes: '',
              practitioner: '',
              practitioner_name: '',
              medical_department: '',
              service_unit: '',
              start_date: dayjs(),
              start_time: dayjs(),
              sample: '',

              custom_pre_operative_diagnosis: '',
              custom_post_operative_diagnosis: '',

              custom_annotations: [],
            }]

            this.fetchRecords()
          }).catch(error => {
            this.showAlert(error.message, 'error')
          })
        },
      });
    },
    stateButtomClick(event) {
      if (
        (
          event.target.getAttribute('label') === 'Procedure' || 
          event.target.getAttribute('aria-label') === 'Procedure' || 
          event.target.localName != 'span'
        ) && this.encounterForm.custom_encounter_state === 'Procedure' && this.procedureForms[0].name
      ) {
        this.$refs.op.toggle(event); // Correct event passed for positioning
      }
    },
    setStepperValue({event, value}) {
      if(value === 'Procedure' && !this.procedureForms[this.selectedProcedure]?.name){
        if(this.records.current_encounter.status != 'Completed' && this.records.current_encounter.status != 'Cancelled'){
          this.encounterForm.custom_encounter_state = this.previousState
          this.newProcedure(event)
          return;
        }
        else{
          this.encounterForm.custom_encounter_state = this.previousState
          this.showAlert('This encounter is submitted and has no procedures' , 10000)
        }
      }
      this.previousState = value;
      if(this.records.current_encounter.status != 'Completed' && this.records.current_encounter.status != 'Cancelled')
        this.autoSave('Patient Encounter', this.encounterForm.name, 'custom_encounter_state', value)
    },
    newProcedure(event) {
      this.$confirm.require({
        target: event.currentTarget,
        group: 'new-procedure',
        message: 'Do you want to create a new clinical procedure?',
        accept: () => {
          this.previousState = 'Procedure';
          this.createProcedure()
        },
      });
    },
    createProcedure(){
      let formClone = {
        doctype: 'Clinical Procedure',

        custom_patient_encounter: this.encounterForm.name,
        procedure_template: this.newProcedureForm.procedure_template,
        
        patient: this.encounterForm.patient,
        patient_name: '',
        patient_sex: this.encounterForm.patient_sex,
        patient_age: this.encounterForm.patient_age,
        practitioner: this.encounterForm.practitioner,
        practitioner_name: this.encounterForm.practitioner_name,
        medical_department: this.encounterForm.medical_department,
        service_unit: this.records.appointment?.service_unit,
        start_date: dayjs().format('YYYY-MM-DD'),
        start_time: dayjs().format('HH:mm'),
			}
      
      this.$call('healthcare_doworks.api.methods.new_doc', {form: formClone})
      .then(response => {
        response.start_time = dayjs(response.start_date + ' ' + response.start_time)
        response.start_date = dayjs(response.start_date)
        this.procedureForms.push(response)
        this.encounterForm.custom_encounter_state = 'Procedure'
        this.autoSave('Patient Encounter', this.encounterForm.name, 'custom_encounter_state', 'Procedure')
        this.selectedProcedure = this.procedureForms.length - 1
        this.$toast.add({ severity: 'success', summary: 'Success', detail: 'Clinical Procedure created', life: 3000 });
      }).catch(error => {
        this.showAlert(error.message, 'error')
      });
    },
    saveSergicalHistory() {
      let procedureRow = ''
      let indicationRow = ''
      let findingRow = ''
      let noteRow = ''
      if(this.procedureProcedureName){
        procedureRow = '<strong>Procedure Name:</strong> '
        this.procedureProcedureName.forEach(value => {procedureRow += value + ', '})
        procedureRow = procedureRow.slice(0, -2)
        procedureRow += '<br>'
      }
      if(this.procedureIndication){
        indicationRow = '<strong>Indication:</strong> '
        this.procedureIndication.forEach(value => {indicationRow += value + ', '})
        indicationRow = indicationRow.slice(0, -2)
        indicationRow += '<br>'
      }
      if(this.procedureFinding)
        findingRow = '<strong>Finding:</strong> ' + this.procedureFinding + '<br>'
      if(this.procedureOperativeNote)
        noteRow = '<strong>Operative Note:</strong> ' + this.procedureOperativeNote
      this.procedureForms[this.selectedProcedure].custom_general_data = procedureRow + indicationRow + findingRow + noteRow
      this.procedureForms[this.selectedProcedure].custom_general_data = this.procedureForms[this.selectedProcedure]?.custom_general_data.replace(/\n/g, '<br>')
      this.$refs.quillEditor.pasteHTML(this.procedureForms[this.selectedProcedure]?.custom_general_data)
      this.autoSave('Clinical Procedure', this.procedureForms[this.selectedProcedure]?.name, 'custom_general_data', this.$refs.quillEditor.getHTML())
      this.sergicalProcedureActive = false
    },
    getAge(birth) {
      let ageMS = Date.parse(Date()) - Date.parse(birth);
      let age = new Date();
      age.setTime(ageMS);
      let years = age.getFullYear() - 1970;
      return years + ' Yrs';
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
    showConsentForm() {
      this.$call('healthcare_doworks.api.methods.get_print_html', 
      {doctype: 'Clinical Procedure', docname: this.procedureForms[this.selectedProcedure]?.name, print_format: 'Consent Form'})
      .then(response => {
        this.consentFormHtml = response
        this.consentFormDialog = true
      }).catch(error => {
        this.showAlert(error.message, 'error')
      });
    },
    clearSignature() {
      this.$refs.consentForm.clearSignature()
      this.procedureForms[this.selectedProcedure].custom_patient_consent_signature = undefined
      this.autoSave('Clinical Procedure', this.procedureForms[this.selectedProcedure].name, 'custom_patient_consent_signature', undefined)
    },
    saveSignature() {
      const signature = this.$refs.consentForm.saveSignature();

      this.$call('healthcare_doworks.api.methods.upload_signature', 
        {docname: this.procedureForms[this.selectedProcedure]?.name, doctype: 'Clinical Procedure', file_data: signature}
      )
      .then(response => {
        this.procedureForms[this.selectedProcedure].custom_patient_consent_signature = true
        this.consentFormDialog = false
        this.$toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Signature saved',
          life: 3000 // Duration in ms
        });
      }).catch(error => {
        this.showAlert(error.message, 'error')
      });
    },
    openNewWindow(href) {
      window.open(href, '_blank');
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
  }
};
</script>

<style>
#patient-bar .p-card-content{
  display: flex;
  overflow: hidden;
  height: 100%;
}

#patient-bar .p-card-body{
  height: 100%;
}

.encounter-page td{
  border: 0 !important;
}

.border-bottom-title .p-card-title{
  padding-bottom: 20px;
  border-bottom: 1px solid #e2e8f0;
}

.gap-card .p-card-content{
  display: flex;
  flex-direction: column;
  gap: 20px;
}

#risk-factors .p-card-content{
  padding-top: 10px;
}

.vital-sign-container{
  min-width: fit-content;
}

.p-dock {
  position: fixed !important;
  right: 0 !important;
  bottom: 0 !important;
  left: 0 !important;
  z-index: 1030 !important;
}

.p-dock-list-container{
  background: rgb(0 0 0 / 5%) !important;
}

.p-sidebar-visible{
  overflow: auto;
}

</style>