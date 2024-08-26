<template>
  <div class="main-wrapper encounter-page">
    <v-alert
      v-if="alertVisible"
      position="fixed"
      location="top center"
      color="red-lighten-3"
      icon="$error"
      style="z-index: 3000; margin-top: 15px"
      border="start"
      closable
      @click:close="()=>{alertVisible = false}"
    >
      <div v-html="message"></div>
    </v-alert>
    <Toast position="bottom-right"/>
    <ConfirmPopup group="headless">
      <template #container="{ message, acceptCallback, rejectCallback }">
        <div class="rounded p-4">
          <span>{{ message.message }}</span>
          <div class="d-flex align-items-center gap-2 mt-4">
            <v-btn @click="acceptCallback" color="primary" size="small">Save</v-btn>
            <v-btn outlined @click="rejectCallback" size="small" text>Cancel</v-btn>
          </div>
        </div>
      </template>
    </ConfirmPopup>
    <div class="row w-100 mx-0">
      <div class="ps-0 pe-md-0 mt-2 mb-md-3 d-block col-12 col-md-6 d-xl-none">
        <Card class="h-100" :class="{'rounded-bottom-0': $vuetify.display.smAndDown, 'rounded-end-0': !$vuetify.display.smAndDown}">
          <template #content>
            <div class="vital-sign-container d-flex align-items-center">
              <!-- <img v-if="records.patient.image" class="me-3 avatar avatar-xl bg-primary-light rounded-circle" :src="records.patient.image" alt="..."> -->
              <v-avatar v-if="records.patient.image" size="80" :image="records.patient.image"></v-avatar>
              <div class="text-start d-flex flex-column">
                <h4 class="mb-0">{{ records.patient.patient_name }}</h4>
                <h6 class="mb-1">{{ records.patient.custom_cpr }}</h6>
                <p class="mb-1">{{ records.patient.dob + records.patient.age + (records.patient.sex.slice(0, 1) || '')}}</p>
                <p class="mb-0"><i class="pi pi-mobile align-middle"></i>{{ records.patient.mobile }}</p>
              </div>
            </div>
          </template>
        </Card>
      </div>
      <div class="ps-0 mb-3 mt-md-2 d-block col-12 col-md-6 d-xl-none">
        <Card class="h-100" :class="{'rounded-top-0': $vuetify.display.smAndDown, 'rounded-start-0': !$vuetify.display.smAndDown}">
          <template #content>
            <div class="d-flex align-items-center">
              <v-avatar 
              v-if="records.practitioner.image"
              size="80" 
              class="me-3" 
              :image="records.practitioner.image">
              </v-avatar>
              <div class="text-start">
                <h4 :class="{'mb-1': true, 'text-red': practitionerConflict}">{{ records.appointment.practitioner_name }}</h4>
                <h4 v-if="practitionerConflict" class="mb-1 text-green">{{ $myresources.user.practitioner_name || $myresources.user.name }}</h4>
                <p v-if="records.appointment.department" class="mb-0">Department: {{ records.appointment.department }}</p>
                <p v-if="records.appointment.service_unit" class="mb-0">Service Unit: {{ records.appointment.service_unit }}</p>
                <h4 class="mt-2 mb-0">{{ encounterForm.custom_encounter_start_time.format('h:mm A') }}</h4>
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
                  <!-- <img v-if="records.patient.image" class="me-3 avatar avatar-xl bg-primary-light rounded-circle" :src="records.patient.image" alt="..."> -->
                  <v-avatar v-if="records.patient.image" size="80" class="me-3" :image="records.patient.image"></v-avatar>
                  <div class="text-start d-flex flex-column">
                    <h4 class="mb-0">{{ records.patient.patient_name }}</h4>
                    <h6 class="mb-1">{{ records.patient.custom_cpr }}</h6>
                    <p class="mb-1">{{ records.patient.dob + records.patient.age + (records.patient.sex.slice(0, 1) || '')}}</p>
                    <p class="mb-0"><i class="pi pi-mobile align-middle"></i>{{ records.patient.mobile }}</p>
                  </div>
                </div>
              </template>
            </Card>
          </div>
          <div class="px-0" style="width: unset; flex-grow: 1; min-width: 0; flex-shrink: unset;">
            <Card :class="['h-100',{'rounded-0': this.isAffixed, 'rounded-start-0': $vuetify.display.xlAndUp}]">
              <template #content>
                <v-slide-group mobile-breakpoint="sm">
                  <v-slide-group-item>
                    <div class="vital-sign-container align-self-center">
                      <div class="mb-2 gap-2 d-flex align-items-center">
                        <i class="pi pi-heart" style="font-size: 1.5rem"></i>
                        <h3 class="my-0 fw-normal">SYS</h3>
                      </div>
                      <div class="d-flex gap-1 align-items-center justify-content-center">
                        <h3 class="fw-normal mb-0">{{currentVS.bp_systolic || '-'}}</h3> <small class="align-self-end" v-if="currentVS.bp_systolic">mm Hg</small>
                      </div>
                    </div>
                  </v-slide-group-item>
                  <Divider layout="vertical"/>
                  <v-slide-group-item>
                    <div class="vital-sign-container align-self-center">
                      <div class="mb-2 gap-2 d-flex align-items-center">
                        <i class="pi pi-heart" style="font-size: 1.5rem"></i>
                        <h3 class="my-0 fw-normal">DIA</h3>
                      </div>
                      <div class="d-flex gap-1 align-items-center justify-content-center">
                        <h3 class="fw-normal mb-0">{{currentVS.bp_diastolic || '-'}}</h3> <small class="align-self-end" v-if="currentVS.bp_diastolic">mm Hg</small>
                      </div>
                    </div>
                  </v-slide-group-item>
                  <Divider layout="vertical"/>
                  <v-slide-group-item>
                    <div class="vital-sign-container align-self-center">
                      <div class="mb-2 gap-1 d-flex align-items-center">
                        <img style="width: 30px;" :src="soundImage"/>
                        <h3 class="my-0 fw-normal">Pulse</h3>
                      </div>
                      <div class="d-flex gap-1 align-items-center justify-content-center">
                        <h3 class="fw-normal mb-0">{{currentVS.pulse || '-'}}</h3> <small class="align-self-end" v-if="currentVS.pulse">BPM</small>
                      </div>
                    </div>
                  </v-slide-group-item>
                  <Divider layout="vertical" />
                  <v-slide-group-item>
                    <div class="vital-sign-container align-self-center">
                      <div class="mb-2 gap-2 d-flex align-items-center">
                        <img style="width: 25px;" :src="lungsImage"/>
                        <h3 class="my-0 fw-normal">Risp</h3>
                      </div>
                      <div class="d-flex gap-1 align-items-center justify-content-center">
                        <h3 class="fw-normal mb-0">{{currentVS.respiratory_rate || '-'}}</h3> <small class="align-self-end" v-if="currentVS.respiratory_rate">BPM</small>
                      </div>
                    </div>
                  </v-slide-group-item>
                  <Divider layout="vertical" />
                  <v-slide-group-item>
                    <div class="vital-sign-container align-self-center">
                      <div class="mb-2 gap-1 d-flex align-items-center">
                        <img style="width: 30px;" :src="celsiusImage"/>
                        <h3 class="my-0 fw-normal">Temp</h3>
                      </div>
                      <div class="d-flex gap-1 align-items-center justify-content-center">
                        <h3 class="fw-normal mb-0">{{currentVS.temperature + '\u00B0' || '-'}}</h3> <small class="align-self-end" v-if="currentVS.temperature">C</small>
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
                <div class="d-flex align-items-center">
                  <v-avatar 
                  v-if="records.practitioner.image"
                  size="80" 
                  class="me-3" 
                  :image="records.practitioner.image">
                  </v-avatar>
                  <div class="text-start">
                    <h4 :class="{'mb-1': true, 'text-red': practitionerConflict}">{{ records.appointment.practitioner_name }}</h4>
                    <h4 v-if="practitionerConflict" class="mb-1 text-green">{{ $myresources.user.practitioner_name || $myresources.user.name }}</h4>
                    <p v-if="records.appointment.department" class="mb-0">Department: <span class="font-weight-bold">{{ records.appointment.department }}</span></p>
                    <p v-if="records.appointment.service_unit" class="mb-0">Service Unit: <span class="font-weight-bold">{{ records.appointment.service_unit }}</span></p>
                    <h4 class="mt-2 mb-0">{{ encounterForm.custom_encounter_start_time.format('h:mm A') }}</h4>
                  </div>
                </div>
              </template>
            </Card>
          </div>
        </div>
      </a-affix>
      <div class="col-xl-9 col-12 ps-0 left-column row h-100" style="margin-right: calc(.5 * var(--bs-gutter-x)); padding: 0">
        <div class="mb-3 col-12 pe-0">
          <Card class="p-0" id="past-encounters" style="overflow: hidden;">
            <template #title>Visit Logs<a class="fs-6 float-end" :class="{'d-none': records.encounters.length <= 5}">See All</a></template>
            <template #content>
              <DataTable 
              :value="records.encounters ? records.encounters.slice(0, 5) : records.encounters" 
              selectionMode="single" 
              :metaKeySelection="true" 
              dataKey="id" 
              @row-click="visitLogSelect"
              >
                <template #empty><v-empty-state title="This Is The First Visit"></v-empty-state></template>
                <Column field="encounter_date" header="Date"></Column>
                <Column field="practitioner_name" header="Practitioner"></Column>
                <Column field="custom_appointment_category" header="Type"></Column>
                <Column field="reasons" header="Reason"></Column>
              </DataTable>
            </template>
          </Card>
        </div>
        <div class="mb-3 col-12 pe-0">
          <Card class="p-0" id="services" style="overflow: hidden;">
            <template #title>
              <span class="align-middle">Service Requests / Results ({{ records.services && records.services.length }})</span>
              <v-btn class="float-end text-orange" prepend-icon="pi pi-plus" variant="plain" @click="()=>{serviceRequestActive = true}">Add</v-btn>
            </template>
            <template #content>
              <DataTable :value="records.services ? records.services.slice(0, 5) : records.services">
                <template #empty><v-empty-state title="No Service Requests"></v-empty-state></template>
                <Column field="template_dn" header="Service Name"></Column>
                <Column field="order_date" header="Ordered On"></Column>
                <Column field="status" header="Status"></Column>
                <Column field="practitioner" header="Ordered By"></Column>
              </DataTable>
            </template>
          </Card>
        </div> 
        <div class="col-xl-4 col-12 pe-0">
          <Card class="p-0 mb-3 border-bottom-title" id="attachments" style="overflow: hidden;">
            <template #title>
              Attachments
              <v-btn class="float-end text-orange" prepend-icon="pi pi-plus" variant="plain" @click="() => {addAttachmentActive = true}">Add</v-btn>
            </template>
            <template #content>
              <div :class="{'d-none': records.attachments.length > 0}">
                <v-empty-state
                  title="No Attachments"
                  ></v-empty-state>
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
            <template #footer>
              <a v-if="records.attachments.length > 4" class="float-end" >View All</a>
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
            style="width: 100%; height: 750px"
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
                      <h5>{{ allergy.type }}</h5>
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
                  Infected Diseases
                </template>
                <template v-slot:text>
                  <div :class="{'d-none': records.patient.custom_infected_diseases.length > 0}">
                    <v-empty-state
                      title="No Infected Diseases"
                    ></v-empty-state>
                  </div>
                  <div
                    class="d-flex py-2"
                    :class="{'d-none': records.patient.custom_infected_diseases.length == 0}"
                    v-for="(item, index) in records.patient.custom_infected_diseases"
                    :key="index"
                  >
                    <div class="d-flex flex-column">
                      <h5 class="mb-0">{{ item.name1 }}</h5>
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
                        <h5 class="mb-0">{{ item.surgery }}</h5>
                        <p class="text-fade mb-0">{{ item.date }}</p>
                      </div>
                      <div class="text-end fw-500">
                        <h5 class="mb-0">{{ item.practitioner }}</h5>
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
                      <h5 class="text-black mb-0 align-middle align-self-center">
                        {{ medication.name1 }}
                        <!-- <small class="text-fade">{{ medication.weight }}</small> -->
                      </h5>
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
                      <h5 class="mb-0">{{ item.habit }}</h5>
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
                  <div :class="{'d-none': records.patient.custom_chronic_diseases || records.patient.custom_genetic_conditions}">
                    <v-empty-state
                      title="No Family History"
                    ></v-empty-state>
                  </div>
                  <div class="d-flex flex-column">
                    <div class="d-flex flex-row flex-grow-1 pb-3">
                      <h4 class="mb-0">Chronic Diseases:&nbsp;</h4>
                      <p class="text-fade mb-0">{{ records.patient.custom_chronic_diseases }}</p>
                    </div>
                    <div class="d-flex flex-row flex-grow-1 pb-3">
                      <h4 class="mb-0">Genetic Diseases:&nbsp;</h4>
                      <p class="text-fade mb-0">{{ records.patient.custom_genetic_conditions }}</p>
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
                      <h5>{{ risk.type }}</h5>
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
      </div> 
      <v-divider color="black" inset class="my-6" style="max-width: calc(100% - 180px)"></v-divider>
      <div class="ps-0 mt-3 col-12 mb-25">
        <Card class="mb-4">
          <template #content>
            <a-form layout="vertical" :model="procedureForm">
              <SelectButton v-model="encounterForm.custom_encounter_state" :options="formOptions" class="text-center" :allowEmpty="false" @change="setStepperValue"/>
              <Stepper orientation="vertical">
                <!-- Procedure Panels -->
                <StepperPanel value="Procedure Info" header="Procedure Info" v-if="encounterForm.custom_encounter_state === 'Procedure'">
                  <template #content="{ nextCallback }">
                    <v-sheet>
                      <v-container>
                        <v-row>
                          <v-col cols="12" md="6">
                            <a-form-item label="Procedure Template">
                              <a-select
                              v-model:value="procedureForm.procedure_template"
                              :options="$myresources.clinicalProcedureTemplate"
                              :fieldNames="{label: 'name', value: 'name'}"
                              style="width: 100%"
                              @change="value => {
                                autoSave('Clinical Procedure', procedureForm.name, 'procedure_template', value)
                              }"
                              ></a-select>
                            </a-form-item>
                            <a-form-item label="Practitioner">
                              <a-select
                              v-model:value="procedureForm.practitioner"
                              :options="$resources.practitioners.data"
                              :fieldNames="{label: 'practitioner_name', value: 'name'}"
                              style="width: 100%"
                              @change="(value, option) => {
                                procedureForm.medical_department = option.department
                                autoSave('Clinical Procedure', procedureForm.name, {practitioner: value, medical_department: option.department})
                              }"
                              ></a-select>
                            </a-form-item>
                            <a-form-item label="Medical Department">
                              <a-select
                              allowClear
                              v-model:value="procedureForm.medical_department"
                              :options="$myresources.departments"
                              :fieldNames="{label: 'department', value: 'department'}"
                              style="width: 100%"
                              @change="value => {
                                autoSave('Clinical Procedure', procedureForm.name, 'medical_department', value)
                              }"
                              ></a-select>
                            </a-form-item>
                            <a-form-item label="Service Unit">
                              <a-select
                              allowClear
                              v-model:value="procedureForm.service_unit"
                              :options="$myresources.serviceUnits"
                              :fieldNames="{label: 'name', value: 'name'}"
                              style="width: 100%"
                              @change="value => {
                                autoSave('Clinical Procedure', procedureForm.name, 'service_unit', value)
                              }"
                              ></a-select>
                            </a-form-item>
                          </v-col>
                          <v-col cols="12" md="6">
                            <a-form-item label="Start Date">
                              <a-date-picker 
                                v-model:value="procedureForm.start_date"
                                format="DD/MM/YYYY" 
                                style="width: 100%;"
                                @change="(date, dateString) => {
                                  const day = dateString.split('/')[0]
                                  const month = dateString.split('/')[1]
                                  const year = dateString.split('/')[2]
                                  autoSave('Clinical Procedure', procedureForm.name, 'start_date', `${year}-${month}-${day}`)
                                }"
                              />
                            </a-form-item>
                            <a-form-item label="Start Time">
                              <a-time-picker 
                              v-model:value="procedureForm.start_time" 
                              format="h:mm a" 
                              style="width: 100%;" 
                              @change="(date, timeString) => {
                                const [time, modifier] = timeString.split(' ');
                                let [hours, minutes] = time.split(':');
                                if (hours === '12')
                                  hours = '00';
                                if (modifier === 'pm')
                                  hours = parseInt(hours, 10) + 12;
                                autoSave('Clinical Procedure', procedureForm.name, 'start_time', `${hours}:${minutes}`)
                              }"/>
                            </a-form-item>
                            <a-form-item label="Notes">
                              <a-textarea :rows="4" v-model:value="procedureForm.notes" @blur="event => {
                                autoSave('Clinical Procedure', procedureForm.name, 'notes', event.target.value)
                              }"/>
                            </a-form-item>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-sheet>
                    <div class="d-flex pt-4">
                      <v-btn variant="flat" color="blue-darken-2" @click="nextCallback">Next</v-btn>
                    </div>
                  </template>
                </StepperPanel>
                <StepperPanel value="Pre Procedure" header="Pre Procedure" v-if="encounterForm.custom_encounter_state === 'Procedure'">
                  <template #content="{ prevCallback, nextCallback }">
                    <v-sheet>
                      <v-container>
                        <v-row>
                          <v-col>
                            <a-form-item label="Sample">
                              <a-select
                              allowClear
                              v-model:value="procedureForm.sample"
                              :options="$myresources.sampleCollections"
                              :fieldNames="{label: 'name', value: 'name'}"
                              style="width: 100%"
                              @change="value => {
                                autoSave('Clinical Procedure', procedureForm.name, 'sample', value)
                              }"
                              ></a-select>
                            </a-form-item>
                            <a-form-item label="Pre Operative Diagnosis">
                              <a-textarea :rows="4" v-model:value="procedureForm.custom_pre_operative_diagnosis" @blur="event => {
                                autoSave('Clinical Procedure', procedureForm.name, 'custom_pre_operative_diagnosis', event.target.value)
                              }"/>
                            </a-form-item>
                            <v-btn 
                            variant="flat" 
                            color="red-accent-4" 
                            
                            @click="showConsentForm"
                            >
                              Consent Form
                            </v-btn>
                            <v-icon
                            v-if="!!procedureForm.custom_patient_consent_signature"
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
                      <v-btn variant="flat" color="grey-lighten-2" @click="prevCallback">Back</v-btn>
                      <v-btn variant="flat" color="blue-darken-2" @click="nextCallback">Next</v-btn>
                    </div>
                  </template>
                </StepperPanel>
                <StepperPanel value="Procedure" header="Procedure" v-if="encounterForm.custom_encounter_state === 'Procedure'">
                  <template #content="{ prevCallback, nextCallback }">
                    <v-sheet>
                      <v-container>
                        <v-row>
                          <v-col>
                            <div class="d-flex gap-2">
                              <v-btn variant="flat" color="orange" disabled>Predefined Areas</v-btn>
                              <v-btn variant="flat" color="orange" disabled>Predefined Annotations</v-btn>
                              <v-btn variant="flat" color="orange" @click="() => {
                                annotationDoctype = procedureForm.doctype; 
                                procedureActive = true
                              }">Free Drawing</v-btn>
                            </div>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-sheet>
                    <div class="d-flex py-4 gap-2">
                      <v-btn variant="flat" color="grey-lighten-2" @click="prevCallback">Back</v-btn>
                      <v-btn variant="flat" color="blue-darken-2" @click="nextCallback">Next</v-btn>
                    </div>
                  </template>
                </StepperPanel>
                <StepperPanel value="Consumables" header="Consumables" v-if="encounterForm.custom_encounter_state === 'Procedure'">
                  <template #content="{ prevCallback, nextCallback }">
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
                                          <a-select
                                          v-model:value="row.item_code"
                                          :options="$resources.items.data.filter(item => item.is_stock_item)"
                                          :fieldNames="{label: 'item_code', value: 'name'}"
                                          @change="(value, option) => {row.item_name = option.item_name}"
                                          ></a-select>
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
                                          <a-select
                                          v-model:value="row.uom"
                                          :options="$resources.uoms.data"
                                          :fieldNames="{label: 'name', value: 'name'}"
                                          ></a-select>
                                        </a-form-item>
                                        <a-checkbox v-model:checked="row.invoice_separately_as_consumables">
                                          Invoice Separately as Consumables
                                        </a-checkbox>
                                      </v-col>
                                      <v-col cols="12" lg="6">
                                        <a-form-item label="Batch">
                                          <a-select
                                          v-model:value="row.batch_no"
                                          :options="$resources.batches.data.filter(batch => batch.item == row.item_code)"
                                          :fieldNames="{label: 'name', value: 'name'}"
                                          ></a-select>
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
                      <v-btn variant="flat" color="grey-lighten-2" @click="prevCallback">Back</v-btn>
                      <v-btn variant="flat" color="blue-darken-2" @click="nextCallback">Next</v-btn>
                    </div>
                  </template>
                </StepperPanel>
                <StepperPanel value="Post Procedure" header="Post Procedure" v-if="encounterForm.custom_encounter_state === 'Procedure'">
                  <template #content="{ prevCallback }">
                    <v-sheet>
                      <v-container>
                        <v-row>
                          <v-col>
                            <a-form-item label="Post Operative Diagnosis">
                              <a-textarea :rows="4" v-model:value="procedureForm.custom_post_operative_diagnosis" @blur="event => {
                                autoSave('Clinical Procedure', procedureForm.name, 'custom_post_operative_diagnosis', event.target.value)
                              }"/>
                            </a-form-item>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-sheet>
                    <div class="d-flex py-4">
                      <v-btn variant="flat" color="grey-lighten-2" @click="prevCallback">Back</v-btn>
                    </div>
                  </template>
                </StepperPanel>
                
                <!-- Consultation & Follow-up Panels -->
                <StepperPanel value="Complaint" header="Complaint" v-if="encounterForm.custom_encounter_state === 'Consultation' || encounterForm.custom_encounter_state === 'Follow-up'">
                  <template #content="{ nextCallback }">
                    <v-sheet>
                      <v-container>
                        <v-row>
                          <v-col>
                            <a-form-item label="Symptoms">
                              <a-select
                                v-model:value="encounterForm.symptoms"
                                :options="$resources.complaints.data"
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
                                  this.$toast.add({ severity: 'success', summary: 'Saved', life: 2000 });
                                }"
                                @deselect="(value, option) => {
                                  deleteChildRow({
                                    parentDoctype: 'Patient Encounter',
                                    fieldName: 'symptoms', 
                                    rows: [option.name], 
                                    filterField: 'complaint'
                                  })
                                  this.$toast.add({ severity: 'success', summary: 'Saved', life: 2000 });
                                }"
                              ></a-select>
                            </a-form-item>
                            <a-form-item label="Symptoms Duration">
                              <a-input-number class="w-full" :min="0" v-model:value="encounterForm.custom_symptoms_duration" @blur="event => {
                                autoSave('Patient Encounter', encounterForm.name, 'custom_symptoms_duration', parseInt(event.target.value))
                              }"/>
                            </a-form-item>
                            <a-form-item label="Note">
                              <a-textarea v-model:value="encounterForm.custom_symptoms_notes" :rows="4" @blur="event => {
                                autoSave('Patient Encounter', encounterForm.name, 'custom_symptoms_notes', event.target.value)
                              }"/>
                            </a-form-item>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-sheet>
                    <div class="d-flex pt-4">
                      <v-btn variant="flat" color="blue-darken-2" @click="nextCallback">Next</v-btn>
                    </div>
                  </template>
                </StepperPanel>
                <StepperPanel value="Pysical Examination & Investigation" header="Pysical Examination & Investigation" v-if="encounterForm.custom_encounter_state === 'Consultation' || encounterForm.custom_encounter_state === 'Follow-up'">
                  <template #content="{ prevCallback, nextCallback }">
                    <v-sheet>
                      <v-container>
                        <v-row>
                          <v-col>
                            <a-form-item label="Physical Examination">
                              <a-textarea v-model:value="encounterForm.custom_physical_examination" :rows="4" @blur="event => {
                                autoSave('Patient Encounter', encounterForm.name, 'custom_physical_examination', event.target.value)
                              }"/>
                            </a-form-item>
                            <a-form-item label="Other Examination">
                              <a-textarea v-model:value="encounterForm.custom_other_examination" :rows="4" @blur="event => {
                                autoSave('Patient Encounter', encounterForm.name, 'custom_other_examination', event.target.value)
                              }"/>
                            </a-form-item>
                          </v-col>
                        </v-row>
                        <v-row>
                          <v-col>
                            <h3 class="my-3">Investigation Procedure</h3>
                            <h5>Lab Tests</h5>
                            <EditableTable :columns="[
                              {label: 'Observation', key: 'observation_template'},
                              {label: 'Comments', key: 'lab_test_comment'},
                            ]"
                            :rows="encounterForm.lab_test_prescription"
                            @update="(items, row, isNew) => {
                              if(items && row)
                                newChildRow({fieldName: 'lab_test_prescription', rules: {}, items, row, isNew})
                            }"
                            @delete="rows => {deleteChildRow({fieldName: 'lab_test_prescription', rows})}"
                            dialogWidth="fit-content"
                            title="Lab Test"
                            >
                              <template v-slot:dialog="{ row }">
                                <a-form layout="vertical">
                                  <v-container>
                                    <v-row>
                                      <v-col cols="12" lg="6">
                                        <a-form-item label="Lab Test">
                                          <a-select
                                          v-model:value="row.lab_test_code"
                                          :options="$resources.labTests.data"
                                          :fieldNames="{label: 'name', value: 'name'}"
                                          ></a-select>
                                        </a-form-item>
                                        <a-form-item label="Observation">
                                          <a-select
                                          v-model:value="row.observation_template"
                                          :options="$resources.observationTemplate.data"
                                          :fieldNames="{label: 'name', value: 'name'}"
                                          ></a-select>
                                        </a-form-item>
                                      </v-col>
                                      <v-col cols="12" lg="6">
                                        <a-form-item label="Comments">
                                          <a-textarea v-model:value="row.lab_test_comment" :rows="4"/>
                                        </a-form-item>
                                      </v-col>
                                    </v-row>
                                    <v-divider></v-divider>
                                    <v-row>
                                      <v-col cols="12" lg="6">
                                        <a-form-item label="Patient Care Type">
                                          <a-select
                                          v-model:value="row.patient_care_type"
                                          :options="$resources.patientCareTypes.data"
                                          :fieldNames="{label: 'name', value: 'name'}"
                                          ></a-select>
                                        </a-form-item>
                                      </v-col>
                                      <v-col cols="12" lg="6">
                                        <a-form-item label="Intent">
                                          <a-select
                                          v-model:value="row.intent"
                                          :options="$resources.codeValues.data.filter(value => value.code_system == 'Intent')"
                                          :fieldNames="{label: 'name', value: 'name'}"
                                          ></a-select>
                                        </a-form-item>
                                        <a-form-item label="Priority">
                                          <a-select
                                          v-model:value="row.priority"
                                          :options="$resources.codeValues.data.filter(value => value.code_system == 'Priority')"
                                          :fieldNames="{label: 'name', value: 'name'}"
                                          ></a-select>
                                        </a-form-item>
                                      </v-col>
                                    </v-row>
                                  </v-container>
                                </a-form>
                              </template>
                            </EditableTable>
                            <div class="d-flex gap-2 mt-10">
                              <v-btn variant="flat" color="primary" disabled>Radiology Test</v-btn>
                              <v-btn variant="flat" color="yellow-darken-1" @click="() => {
                                annotationDoctype = encounterForm.doctype; 
                                encounterAnnotationType='Investigation'; 
                                procedureActive = true
                              }">Annotation</v-btn>
                            </div>
                          </v-col>
                        </v-row>
                        <v-row>
                          <v-col>
                            <h3 class="mt-3">Annotations</h3>
                            <!-- <div class="card">
                              <Galleria 
                              :value="records.current_encounter.custom_annotations.filter(a => a.type == 'Investigation')" 
                              :responsiveOptions="[{breakpoint: '1300px', numVisible: 4}, {breakpoint: '575px', numVisible: 1}]" 
                              :numVisible="5" 
                              containerStyle="max-width: 640px"
                              >
                                <template #item="slotProps">
                                  <img :src="slotProps.item.itemImageSrc" :alt="slotProps.item.alt" style="width: 100%" />
                                </template>
                                <template #thumbnail="slotProps">
                                  <img :src="slotProps.item.thumbnailImageSrc" :alt="slotProps.item.alt" />
                                </template>
                              </Galleria>
                            </div> -->
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-sheet>
                    <div class="d-flex py-4 gap-2">
                      <v-btn variant="flat" color="grey-lighten-2" @click="prevCallback">Back</v-btn>
                      <v-btn variant="flat" color="blue-darken-2" @click="nextCallback">Next</v-btn>
                    </div>
                  </template>
                </StepperPanel>
                <StepperPanel value="Illness Progression" header="Illness Progression" v-if="encounterForm.custom_encounter_state === 'Follow-up'">
                  <template #content="{ nextCallback }">
                    <v-sheet>
                      <v-container>
                        <v-row>
                          <v-col>
                            <a-textarea v-model:value="encounterForm.custom_illness_progression" :rows="4" @blur="event => {
                              autoSave('Patient Encounter', encounterForm.name, 'custom_illness_progression', event.target.value)
                            }"/>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-sheet>
                    <div class="d-flex pt-4">
                      <v-btn variant="flat" color="blue-darken-2" @click="nextCallback">Next</v-btn>
                    </div>
                  </template>
                </StepperPanel>
                <StepperPanel value="Diagnosis" header="Diagnosis" v-if="encounterForm.custom_encounter_state === 'Consultation' || encounterForm.custom_encounter_state === 'Follow-up'">
                  <template #content="{ prevCallback, nextCallback }">
                    <v-sheet>
                      <v-container>
                        <v-row>
                          <v-col>
                            <a-form-item label="Diagnosis">
                              <a-select
                                v-model:value="encounterForm.diagnosis"
                                label-in-value
                                :options="$resources.diagnosis.data"
                                mode="multiple"
                                style="width: 100%"
                                @select="(value, option) => {
                                  newChildRow({
                                    parentDoctype: 'Patient Encounter',
                                    fieldName: 'diagnosis', 
                                    row: {diagnosis: option.name}, 
                                    isNew: true
                                  })
                                  this.$toast.add({ severity: 'success', summary: 'Saved', life: 2000 });
                                }"
                                @deselect="(value, option) => {
                                  deleteChildRow({
                                    parentDoctype: 'Patient Encounter',
                                    fieldName: 'diagnosis', 
                                    rows: [option.name], 
                                    filterField: 'diagnosis'
                                  })
                                  this.$toast.add({ severity: 'success', summary: 'Saved', life: 2000 });
                                }"
                              ></a-select>
                            </a-form-item>
                            <a-form-item label="Differential Diagnosis">
                              <a-select
                                v-model:value="encounterForm.custom_differential_diagnosis"
                                label-in-value
                                :options="$resources.diagnosis.data"
                                mode="multiple"
                                style="width: 100%"
                                @select="(value, option) => {
                                  newChildRow({
                                    parentDoctype: 'Patient Encounter',
                                    fieldName: 'custom_differential_diagnosis', 
                                    row: {diagnosis: option.name}, 
                                    isNew: true
                                  })
                                  this.$toast.add({ severity: 'success', summary: 'Saved', life: 2000 });
                                }"
                                @deselect="(value, option) => {
                                  deleteChildRow({
                                    parentDoctype: 'Patient Encounter',
                                    fieldName: 'custom_differential_diagnosis', 
                                    rows: [option.name], 
                                    filterField: 'diagnosis'
                                  })
                                  this.$toast.add({ severity: 'success', summary: 'Saved', life: 2000 });
                                }"
                              ></a-select>
                            </a-form-item>
                            <a-form-item label="Diagnosis Note">
                              <a-textarea v-model:value="encounterForm.custom_diagnosis_note" :rows="4" @blur="event => {
                              autoSave('Patient Encounter', encounterForm.name, 'custom_diagnosis_note', event.target.value)
                            }"/>
                            </a-form-item>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-sheet>
                    <div class="d-flex py-4 gap-2">
                      <v-btn variant="flat" color="grey-lighten-2" @click="prevCallback">Back</v-btn>
                      <v-btn variant="flat" color="blue-darken-2" @click="nextCallback">Next</v-btn>
                    </div>
                  </template>
                </StepperPanel>
                <StepperPanel value="Treatment" header="Treatment" v-if="encounterForm.custom_encounter_state === 'Consultation' || encounterForm.custom_encounter_state === 'Follow-up'">
                  <template #content="{ prevCallback, nextCallback }">
                    <v-sheet>
                      <v-container>
                        <v-row>
                          <v-col>
                            <h5>Medications</h5>
                            <EditableTable :columns="[
                              {label: 'Medication', key: 'medication'},
                              {label: 'Drug Code', key: 'drug_code'},
                              {label: 'Dosage', key: 'dosage'},
                              {label: 'Period', key: 'period'},
                              {label: 'Dosage Form', key: 'dosage_form'},
                            ]"
                            :rows="encounterForm.drug_prescription"
                            @update="(items, row, isNew) => {
                              if(items && row)
                                newChildRow({
                                  fieldName: 'drug_prescription', 
                                  rules: {
                                    medication: [{ required: true, message: 'Please choose a medication!' }],
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
                                      <v-col cols="12" lg="6">
                                        <a-form-item label="Medication">
                                          <a-select
                                          v-model:value="row.medication"
                                          :options="$resources.medications.data"
                                          :fieldNames="{label: 'name', value: 'name'}"
                                          @change="(value, option) => {
                                            row.strength = option.strength
                                            row.strength_uom = option.strength_uom
                                            row.dosage_form = option.dosage_form
                                            row.dosage = option.default_prescription_dosage
                                            row.period = option.default_prescription_duration
                                          }"
                                          ></a-select>
                                        </a-form-item>
                                        <a-form-item label="Drug Code">
                                          <a-select
                                          v-model:value="row.drug_code"
                                          :options="$resources.items.data.filter(item => item.name = row.medication)"
                                          :fieldNames="{label: 'name', value: 'name'}"
                                          ></a-select>
                                        </a-form-item>
                                        <a-form-item label="Drug Name / Description">
                                          <a-input v-model:value="row.drug_name" disabled/>
                                        </a-form-item>
                                        <a-form-item label="Strength">
                                          <a-input v-model:value="row.strength" disabled/>
                                        </a-form-item>
                                        <a-form-item label="Strength UOM">
                                          <a-input v-model:value="row.strength_uom" disabled/>
                                        </a-form-item>
                                        <a-form-item label="Dosage Form">
                                          <a-select
                                          v-model:value="row.dosage_form"
                                          :options="$resources.dosageForms.data"
                                          :fieldNames="{label: 'name', value: 'name'}"
                                          ></a-select>
                                        </a-form-item>
                                      </v-col>
                                      <v-col cols="12" lg="6">
                                        <a-checkbox v-model:checked="row.dosage_by_interval">Dosage by Time Interval</a-checkbox>
                                        <a-form-item label="Dosage" v-if="!row.dosage_by_interval">
                                          <a-select
                                          v-model:value="row.dosage"
                                          :options="$resources.dosages.data"
                                          :fieldNames="{label: 'name', value: 'name'}"
                                          ></a-select>
                                        </a-form-item>
                                        <a-form-item label="Interval" v-if="row.dosage_by_interval">
                                          <a-input v-model:value="row.interval"/>
                                        </a-form-item>
                                        <a-form-item label="Interval UOM" v-if="row.dosage_by_interval">
                                          <a-select
                                          v-model:value="row.interval_uom"
                                          :options="[{label: '', value: ''}, {label: 'Hour', value: 'Hour'}, {label: 'Day', value: 'Day'}]"
                                          ></a-select>
                                        </a-form-item>
                                        <a-form-item label="Period">
                                          <a-select
                                          v-model:value="row.period"
                                          :options="$resources.prescriptionDurations.data"
                                          :fieldNames="{label: 'name', value: 'name'}"
                                          ></a-select>
                                        </a-form-item>
                                        <a-form-item label="Number Of Repeats Allowed">
                                          <a-input v-model:value="row.number_of_repeats_allowed"/>
                                        </a-form-item>
                                      </v-col>
                                    </v-row>
                                    <v-divider></v-divider>
                                    <v-row>
                                      <v-col cols="12" lg="6">
                                        <a-form-item label="Intent">
                                          <a-select
                                          v-model:value="row.intent"
                                          :options="$resources.codeValues.data.filter(value => value.code_system == 'Intent')"
                                          :fieldNames="{label: 'name', value: 'name'}"
                                          ></a-select>
                                        </a-form-item>
                                        <a-form-item label="Priority">
                                          <a-select
                                          v-model:value="row.priority"
                                          :options="$resources.codeValues.data.filter(value => value.code_system == 'Priority')"
                                          :fieldNames="{label: 'name', value: 'name'}"
                                          ></a-select>
                                        </a-form-item>
                                        <a-form-item label="Medication Request" v-if="row.medication_request">
                                          <a-input v-model:value="row.medication_request" disabled/>
                                        </a-form-item>
                                      </v-col>
                                    </v-row>
                                    <v-divider></v-divider>
                                    <v-row>
                                      <v-col>
                                        <a-form-item label="Comment">
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
                                          <a-select
                                          v-model:value="row.procedure"
                                          :options="$resources.clinicalProcedureTemplates.data"
                                          :fieldNames="{label: 'name', value: 'name'}"
                                          @change="(value, option) => {
                                            row.procedure_name = option.template
                                            row.department = medical_department
                                          }"
                                          ></a-select>
                                        </a-form-item>
                                        <a-form-item label="Procedure Name">
                                          <a-input v-model:value="row.procedure_name"/>
                                        </a-form-item>
                                        <a-form-item label="Department">
                                          <a-select
                                          v-model:value="row.department"
                                          :options="$resources.departments.data"
                                          :fieldNames="{label: 'name', value: 'name'}"
                                          ></a-select>
                                        </a-form-item>
                                        <a-form-item label="Referring Practitioner">
                                          <a-select
                                          v-model:value="row.practitioner"
                                          :options="$resources.practitioners.data"
                                          :fieldNames="{label: 'practitioner_name', value: 'name'}"
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
                                    <v-divider></v-divider>
                                    <v-row>
                                      <v-col cols="12" lg="6">
                                        <a-form-item label="Patient Care Type">
                                          <a-select
                                          v-model:value="row.patient_care_type"
                                          :options="$resources.patientCareTypes.data"
                                          :fieldNames="{label: 'name', value: 'name'}"
                                          ></a-select>
                                        </a-form-item>
                                      </v-col>
                                      <v-col cols="12" lg="6">
                                        <a-form-item label="Intent">
                                          <a-select
                                          v-model:value="row.intent"
                                          :options="$resources.codeValues.data.filter(value => value.code_system == 'Intent')"
                                          :fieldNames="{label: 'name', value: 'name'}"
                                          ></a-select>
                                        </a-form-item>
                                        <a-form-item label="Priority">
                                          <a-select
                                          v-model:value="row.priority"
                                          :options="$resources.codeValues.data.filter(value => value.code_system == 'Priority')"
                                          :fieldNames="{label: 'name', value: 'name'}"
                                          ></a-select>
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
                                  fieldName: 'therapies', 
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
                                          <a-select
                                          v-model:value="row.therapy_type"
                                          :options="$resources.therapyTypes.data"
                                          :fieldNames="{label: 'name', value: 'name'}"
                                          ></a-select>
                                        </a-form-item>
                                        <a-form-item label="No of Sessions">
                                          <a-input v-model:value="row.no_of_sessions"/>
                                        </a-form-item>
                                      </v-col>
                                    </v-row>
                                    <v-divider></v-divider>
                                    <v-row>
                                      <v-col cols="12" lg="6">
                                        <a-form-item label="Patient Care Type">
                                          <a-select
                                          v-model:value="row.patient_care_type"
                                          :options="$resources.patientCareTypes.data"
                                          :fieldNames="{label: 'name', value: 'name'}"
                                          ></a-select>
                                        </a-form-item>
                                      </v-col>
                                      <v-col cols="12" lg="6">
                                        <a-form-item label="Intent">
                                          <a-select
                                          v-model:value="row.intent"
                                          :options="$resources.codeValues.data.filter(value => value.code_system == 'Intent')"
                                          :fieldNames="{label: 'name', value: 'name'}"
                                          ></a-select>
                                        </a-form-item>
                                        <a-form-item label="Priority">
                                          <a-select
                                          v-model:value="row.priority"
                                          :options="$resources.codeValues.data.filter(value => value.code_system == 'Priority')"
                                          :fieldNames="{label: 'name', value: 'name'}"
                                          ></a-select>
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
                            <div class="d-flex gap-2">
                              <v-btn variant="flat" color="yellow-darken-1" @click="() => {
                                annotationDoctype = encounterForm.doctype; 
                                encounterAnnotationType='Investigation'; 
                                procedureActive = true
                              }">Annotation</v-btn>
                            </div>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-sheet>
                    <div class="d-flex py-4 gap-2">
                      <v-btn variant="flat" color="grey-lighten-2" @click="prevCallback">Back</v-btn>
                      <v-btn variant="flat" color="blue-darken-2" @click="nextCallback">Next</v-btn>
                    </div>
                  </template>
                </StepperPanel>
                <StepperPanel value="Order" header="Order" v-if="encounterForm.custom_encounter_state === 'Consultation' || encounterForm.custom_encounter_state === 'Follow-up'">
                  <template #content="{ prevCallback }">
                    <v-sheet>
                      <v-container>
                        <v-row>
                          <v-col>
                            <div class="d-flex gap-2">
                              <v-btn variant="flat" color="pink" @click="() => {medicationRequestActive = true}">Medications</v-btn>
                              <v-btn variant="flat" color="pink" @click="() => {labTestActive = true}">Lab Test</v-btn>
                              <v-btn variant="flat" color="pink" disabled>Radiology Test</v-btn>
                              <v-btn variant="flat" color="pink" disabled>Transfer To Other Hospital</v-btn>
                              <v-btn variant="flat" color="pink" disabled>Transfer To Other Doctor</v-btn>
                            </div>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-sheet>
                    <div class="d-flex py-4">
                      <v-btn variant="flat" color="grey-lighten-2" @click="prevCallback">Back</v-btn>
                    </div>
                  </template>
                </StepperPanel>

                <!-- Session Panels -->

              </Stepper>
              <div class="d-flex py-4 gap-2">
                <!-- <v-btn variant="flat" color="lime" @click="submitEncounter()">Save</v-btn>
                <v-btn variant="flat" color="amber" @click="submitEncounter(true)">Submit</v-btn> -->
              </div>
            </a-form>
          </template>
        </Card>
      </div> 
    </div>

    <div class="dialogs">
      <vitalSignsDialog 
      :isOpen="vitalSignsActive" 
      @update:isOpen="vitalSignsActive = $event" 
      @show-alert="showAlert" 
      :appointment="records.appointment"
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
      />
      <procedureDialog 
      :isOpen="procedureActive" 
      @update:isOpen="procedureActive = $event" 
      @show-alert="showAlert" 
      :doctype="annotationDoctype"
      :docname="annotationDoctype == 'Patient Encounter' ? encounterForm.name : procedureForm.name"
      :encounterType="annotationDoctype == 'Patient Encounter' ? encounterAnnotationType : ''"
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
      <v-dialog v-model="consentFormDialog" width="auto">
        <v-toolbar color="red-accent-4" :style="{borderTopRightRadius: '12px', borderTopLeftRadius: '12px'}">
          <v-btn variant="text" icon="mdi mdi-close" @click="consentFormDialog = false"></v-btn>

          <v-toolbar-title>Consent Form</v-toolbar-title>

          <v-spacer></v-spacer>
          
          <v-toolbar-items>
            <v-btn
              text="Save"
              variant="text"
              @click="saveSignature"
            ></v-btn>
          </v-toolbar-items>
        </v-toolbar>

        <v-card>
          <pdfSignature :html="consentFormHtml" ref="consentFrom"/>
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

import { ref, reactive } from 'vue';
import { Form } from 'ant-design-vue';

import encounterRecords from '@/assets/json/encounterrecords.json'
import pdfSignature from '@/components/pdfSignature.vue';
import soundImage from '@/assets/img/sound.png';
import lungsImage from '@/assets/img/lungs.png';
import celsiusImage from '@/assets/img/celsius.png';

export default {
  inject: ['$socket', '$call'],
  components: {
    VSlideGroup, VSlideGroupItem, VProgressLinear, VChip, VEmptyState, VAvatar, VIcon, VBtnGroup,
    VSelect, VStepper, VStepperHeader, VStepperItem, VStepperActions, VStepperWindow, VStepperWindowItem, VSheet,
    Image, VHover, pdfSignature, VToolbar, VToolbarItems, VToolbarTitle, VSpacer, VList, VListItem, VListItemTitle,
  },
  resources: {
    medications() { return { 
      type: 'list', 
      doctype: 'Medication', 
      fields: ['*'], 
      auto: true,
      orderBy: 'name'
    }},
    items() { return { 
      type: 'list', 
      doctype: 'Item', 
      fields: ['name', 'item_code', 'item_name'], 
      auto: true,
      orderBy: 'name'
    }},
    dosageForms() { return { 
      type: 'list', 
      doctype: 'Dosage Form', 
      fields: ['name'], 
      auto: true,
      orderBy: 'name'
    }},
    dosages() { return { 
      type: 'list', 
      doctype: 'Prescription Dosage', 
      fields: ['name'], 
      auto: true,
      orderBy: 'name'
    }},
    prescriptionDurations() { return { 
      type: 'list', 
      doctype: 'Prescription Duration', 
      fields: ['name'], 
      auto: true,
      orderBy: 'name'
    }},
    codeValues() { return { 
      type: 'list', 
      doctype: 'Code Value', 
      fields: ['name', 'code_system'], 
      auto: true,
      orderBy: 'name'
    }},
    clinicalProcedureTemplates() { return { 
      type: 'list', 
      doctype: 'Clinical Procedure Template', 
      fields: ['name', 'template', 'medical_department'], 
      auto: true,
      orderBy: 'name'
    }},
    departments() { return { 
      type: 'list', 
      doctype: 'Department', 
      fields: ['name'], 
      auto: true,
      orderBy: 'name'
    }},
    practitioners() { return { 
      type: 'list', 
      doctype: 'Healthcare Practitioner', 
      fields: ['name', 'practitioner_name', 'department'], 
      auto: true,
      orderBy: 'practitioner_name'
    }},
    patientCareTypes() { return { 
      type: 'list', 
      doctype: 'Patient Care Type', 
      fields: ['name'], 
      auto: true,
      orderBy: 'name'
    }},
    therapyTypes() { return { 
      type: 'list', 
      doctype: 'Therapy Type', 
      fields: ['name'], 
      auto: true,
      orderBy: 'name'
    }},
    labTests() { return { 
      type: 'list', 
      doctype: 'Lab Test Template', 
      fields: ['name'], 
      filters: {is_billable: 1},
      auto: true,
      orderBy: 'name'
    }},
    observationTemplate() { return { 
      type: 'list', 
      doctype: 'Observation Template', 
      fields: ['name'], 
      auto: true,
      orderBy: 'name'
    }},
    uoms() { return { 
      type: 'list', 
      doctype: 'UOM', 
      fields: ['name'], 
      auto: true,
      orderBy: 'name'
    }},
    batches() { return { 
      type: 'list', 
      doctype: 'Batch', 
      fields: ['name'], 
      auto: true,
      orderBy: 'name'
    }},
    complaints() { return { 
      type: 'list', 
      doctype: 'Complaint', 
      fields: ['name'], 
      auto: true,
      orderBy: 'name',
      // transform data before setting it
      transform(data) {
        for (let d of data) {
          d.label = d.name
          d.value = d.name
        }
        return data
      },
    }},
    diagnosis() { return { 
      type: 'list', 
      doctype: 'Diagnosis', 
      fields: ['name'], 
      auto: true,
      orderBy: 'name',
      // transform data before setting it
      transform(data) {
        for (let d of data) {
          d.label = d.name
          d.value = d.name
        }
        return data
      },
    }},
  },
  data() {
    return {
      consentFormDialog: false,
      consentFormHtml: '',
      currentFormStep: 0,
      currentVS: {
        name: '',
        pulse: "-",
        respiratory_rate: "-",
        bp_systolic: "-",
        bp_diastolic: "-",
        temperature: "-",
        signs_date: '-',
      },
      records: ref(encounterRecords),
      isAffixed:false,
      lungsImage:lungsImage,
      celsiusImage:celsiusImage,
      soundImage:soundImage,
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
      message: '',
      alertVisible: false,
      formOptions: ['Consultation', 'Procedure', 'Follow-up', 'Session'],
      previousState: '',
      annotationDoctype: '',
      encounterAnnotationType: '',
      encounterForm: reactive({
        doctype: 'Patient Encounter',
        name: '',
        custom_encounter_start_time: dayjs(),
        procedure_date: dayjs(),
        symptoms: [],
        custom_symptoms_duration: 0,
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
			}),

      procedureForm: reactive({
        doctype: 'Clinical Procedure',
        name: '',
        custom_patient_consent_signature: '',

        custom_patient_encounter: '',
        procedure_template: 'Botox Injection',
        
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
			}),
    };
  },
  created() {
    this.fetchRecords();
    this.$socket.on('services', response => {
      let thisPatient = false
      this.records.services = response.filter(service => {
        thisPatient = true
        return service.patient == this.encounterForm.patient
      })
      if(thisPatient) 
        this.$toast.add({ severity: 'success', summary: 'Update', detail: 'Service Requests have been updated', life: 2000 });
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
      this.lodingOverlay = true;
      this.$call('healthcare_doworks.api.methods.patient_encounter_records', {encounter_id: this.$route.params.encounterId})
      .then(response => {
        console.log(response)
        response.current_encounter.custom_encounter_start_time = dayjs(response.current_encounter.custom_encounter_start_time)
        if(response.current_procedure){
          response.current_procedure.start_time = dayjs(response.current_procedure.start_date + ' ' + response.current_procedure.start_time)
          response.current_procedure.start_date = dayjs(response.current_procedure.start_date)
          this.procedureForm = {...this.procedureForm, ...response.current_procedure}
        }
        response.current_encounter.diagnosis = response.current_encounter.diagnosis.map(value => {
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
          this.currentVS = response.vitalSigns[0];
        }
        if(response.appointment.practitioner !== this.$myresources.user.practitioner){
          this.practitionerConflict = true
        }
        this.records = response
      })
      .catch(error => {
        console.error('Error fetching records:', error);
      });
    },
    showAlert(message, duration) {
      this.message = message;
      this.alertVisible = true;
      // setTimeout(() => {
      //   this.alertVisible = false;
      // }, duration);
    },
    submitEncounter(submit = false) {
      const { validate } = Form.useForm(this.encounterForm, this.rules);
      validate().then(() => {
        this.lodingOverlay = true;
        let formClone = {...this.encounterForm}
        formClone.encounter_date = dayjs().format('YYYY-MM-DD')
        formClone.encounter_time = dayjs().format('HH:mm')
        formClone.custom_encounter_start_time = dayjs(this.encounterForm.custom_encounter_start_time).format('YYYY-MM-DD HH:mm')
        this.$call('healthcare_doworks.api.methods.edit_doc', {form: formClone, submit: submit})
        .then(response => {
          this.lodingOverlay = false;
          
        }).catch(error => {
          console.error(error);
          let message = error.message.split('\n');
          message = message.find(line => line.includes('frappe.exceptions'));
          if(message){
            const firstSpaceIndex = message.indexOf(' ');
            this.showAlert(message.substring(firstSpaceIndex + 1) , 10000)
          }
          else
            this.showAlert('Sorry. There is an error!' , 10000)
        });
      })
      .catch(err => {
        console.log('error', err);
      });
    },
    autoSave(doctype, name, fieldname, value) {
      this.lodingOverlay = true;
      
      this.$call('frappe.client.set_value', {doctype, name, fieldname, value})
      .then(response => {
        this.lodingOverlay = false;
        this.$toast.add({ severity: 'success', summary: 'Saved', life: 2000 });
      }).catch(error => {
        console.error(error);
        let message = error.message.split('\n');
        message = message.find(line => line.includes('frappe.exceptions'));
        if(message){
          const firstSpaceIndex = message.indexOf(' ');
          this.showAlert(message.substring(firstSpaceIndex + 1) , 10000)
        }
        else
          this.showAlert('Sorry. There is an error!' , 10000)
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
          console.log(formClone)
          this.$call('healthcare_doworks.api.general_methods.add_child_entry', {
            parent_doctype: parentDoctype || 'Patient Encounter', 
            parent_doc_name: this.encounterForm.name, 
            child_table_fieldname: fieldName, 
            child_data: formClone
          }).then(response => {
            this.lodingOverlay = false;
          }).catch(error => {
            console.error(error);
            let message = error.message.split('\n');
            message = message.find(line => line.includes('frappe.exceptions'));
            if(message){
              const firstSpaceIndex = message.indexOf(' ');
              this.showAlert(message.substring(firstSpaceIndex + 1) , 10000)
            }
            else
              this.showAlert('Sorry. There is an error!' , 10000)
          });
        }
        else{
          this.$call('healthcare_doworks.api.general_methods.modify_child_entry', {
            parent_doctype: parentDoctype || 'Patient Encounter', 
            parent_doc_name: this.encounterForm.name, 
            child_table_fieldname: fieldName, 
            filters: {name: row.name}, 
            update_data: formClone
          }).then(response => {
            this.lodingOverlay = false;
          }).catch(error => {
            console.error(error);
            let message = error.message.split('\n');
            message = message.find(line => line.includes('frappe.exceptions'));
            if(message){
              const firstSpaceIndex = message.indexOf(' ');
              this.showAlert(message.substring(firstSpaceIndex + 1) , 10000)
            }
            else
              this.showAlert('Sorry. There is an error!' , 10000)
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
          parent_doctype: parentDoctype || 'Patient Encounter', 
          parent_doc_name: this.encounterForm.name, 
          child_table_fieldname: fieldName, 
          filters: {[filterField || 'name']: row}
        }).then(response => {
          this.lodingOverlay = false;
        }).catch(error => {
          console.error(error);
          let message = error.message.split('\n');
          message = message.find(line => line.includes('frappe.exceptions'));
          if(message){
            const firstSpaceIndex = message.indexOf(' ');
            this.showAlert(message.substring(firstSpaceIndex + 1) , 10000)
          }
          else
            this.showAlert('Sorry. There is an error!' , 10000)
        })
        .catch(err => {
          console.log('error', err);
        });
      })
    },
    visitLogSelect(row) {
      this.pastVisitEditRow = row.data;
      this.pastVisitsActive = true;
    },
    setStepperValue({event, value}) {
      if(value === 'Procedure' && !this.procedureForm.name){
        this.requireConfirmation(event, value)
        this.encounterForm.custom_encounter_state = this.previousState
        return;
      }
      this.previousState = value;
      this.autoSave('Patient Encounter', this.encounterForm.name, 'custom_encounter_state', value)
    },
    requireConfirmation(event) {
      this.$confirm.require({
        target: event.currentTarget,
        group: 'headless',
        message: 'Do you want to create a clinical procedure?',
        accept: () => {
          this.createProcedure()
        },
      });
    },
    createProcedure(){
      this.lodingOverlay = true;
      let formClone = {...this.procedureForm}
      formClone.start_date = dayjs().format('YYYY-MM-DD')
      formClone.start_time = dayjs().format('HH:mm')
      formClone.custom_patient_encounter = this.encounterForm.name
      formClone.patient = this.encounterForm.patient
      formClone.patient_sex = this.encounterForm.patient_sex
      formClone.patient_age = this.encounterForm.patient_age
      formClone.practitioner = this.encounterForm.practitioner
      formClone.practitioner_name = this.encounterForm.practitioner_name
      formClone.medical_department = this.encounterForm.medical_department
      formClone.service_unit = this.records.appointment.service_unit
      
      this.$call('healthcare_doworks.api.methods.new_doc', {form: formClone})
      .then(response => {
        this.lodingOverlay = false;
        this.procedureForm = response
        this.encounterForm.custom_encounter_state = 'Procedure'
        this.$toast.add({ severity: 'success', summary: 'Success', detail: 'A new Clinical Procedure has been created', life: 2000 });
      }).catch(error => {
        console.error(error);
        let message = error.message.split('\n');
        message = message.find(line => line.includes('frappe.exceptions'));
        if(message){
          const firstSpaceIndex = message.indexOf(' ');
          this.showAlert(message.substring(firstSpaceIndex + 1) , 10000)
        }
        else
          this.showAlert('Sorry. There is an error!' , 10000)
      });
    },
    showConsentForm() {
      this.$call('healthcare_doworks.api.methods.get_print_html', 
      {doctype: 'Clinical Procedure', docname: this.procedureForm.name, print_format: 'Consent Form'})
      .then(response => {
        this.consentFormHtml = response
        this.consentFormDialog = true

      }).catch(error => {
        console.error(error);
        let message = error.message.split('\n');
        message = message.find(line => line.includes('frappe.exceptions'));
        if(message){
          const firstSpaceIndex = message.indexOf(' ');
          this.showAlert(message.substring(firstSpaceIndex + 1) , 10000)
        }
        else
          this.showAlert('Sorry. There is an error!' , 10000)
      });
    },
    saveSignature() {
      const signature = this.$refs.consentFrom.saveSignature();

      this.$call('healthcare_doworks.api.methods.upload_signature', 
        {docname: this.procedureForm.name, doctype: 'Clinical Procedure', file_data: signature}
      )
      .then(response => {
        this.procedureForm.custom_patient_consent_signature = true
        this.consentFormDialog = false
        this.$toast.add({ severity: 'success', summary: 'Saved', life: 2000 });
      }).catch(error => {
        console.error(error);
        let message = error.message.split('\n');
        message = message.find(line => line.includes('frappe.exceptions'));
        if(message){
          const firstSpaceIndex = message.indexOf(' ');
          this.showAlert(message.substring(firstSpaceIndex + 1) , 10000)
        }
        else
          this.showAlert('Sorry. There is an error!' , 10000)
      });
    },
    openNewWindow(href) {
      window.open(href, '_blank');
    }
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