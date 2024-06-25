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
    <div class="row w-100 mx-0">
      <div class="ps-0 pe-md-0 mt-2 mb-md-3 d-block col-12 col-md-6 d-xl-none">
        <Card class="h-100" :class="{'rounded-bottom-0': $vuetify.display.smAndDown, 'rounded-end-0': !$vuetify.display.smAndDown}">
          <template #content>
            <div class="vital-sign-container d-flex align-items-center">
              <img v-if="records.patient.image" class="me-3 avatar avatar-xl bg-primary-light rounded-circle" :src="records.patient.image" alt="...">
              <div class="text-start d-flex flex-column">
                <h4 class="mb-0">{{ records.patient.patient_name }}</h4>
                <h6 class="mb-1">{{ records.patient.custom_cpr }}</h6>
                <p class="mb-1">{{ records.patient.dob + ' (' + records.patient.age + 'yrs), ' + (records.patient.sex.slice(0, 1) || '')}}</p>
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
              <img 
                v-if="records.practitioner && records.practitioner.image && !practitionerConflict" 
                class="me-3 avatar avatar-xl bg-primary-light rounded-circle"
                :src="records.practitioner.image" alt="..."
                >
                <div class="text-start">
                  <div class="d-flex">
                    <h4 :class="{'mb-1': true, 'text-red': practitionerConflict}">{{ records.practitioner.practitioner_name }}</h4>
                    <span v-if="practitionerConflict">&nbsp;&nbsp;->&nbsp;&nbsp;</span>
                    <img 
                    v-if="practitionerConflict && $resources.user.image" 
                    class="me-3 avatar avatar-xl bg-primary-light rounded-circle"
                    :src="$resources.user.image" alt="..."
                    >
                    <h4 v-if="practitionerConflict" class="mb-1 text-green">{{ $resources.user.name }}</h4>
                  </div>
                  <p v-if="records.appointment.service_unit" class="mb-0">Service Unit: {{ records.appointment.service_unit }}</p>
                  <p v-if="records.appointment.department" class="mb-0">{{ records.appointment.department }}</p>
                  <h4 class="mt-2 mb-0">{{ diagnosticForm.encounter_start_time.format('h:mm A') }}</h4>
                </div>
            </div>
          </template>
        </Card>
      </div>
      <a-affix 
        @change="affixChenge"
        class="pe-0"
        :style="this.isAffixed ? {left: '-20px', position: 'relative', width: 'calc(100% + 25px)', maxWidth: 'unset'} : {}"
      >
        <div class="row col-12 sticky-top flex-nowrap" :class="{'mb-3': !this.isAffixed}" id="patient-bar" style="z-index: 1000;">
          <div class="px-0 d-none d-xl-block" style="width: unset;flex: 0 0 auto;" :class="{'ps-0': this.isAffixed}">
            <Card :class="['h-100 rounded-end-0',{'rounded-0': this.isAffixed}]">
              <template #content>
                <div class="vital-sign-container d-flex align-items-center">
                  <img v-if="records.patient.image" class="me-3 avatar avatar-xl bg-primary-light rounded-circle" :src="records.patient.image" alt="...">
                  <div class="text-start d-flex flex-column">
                    <h4 class="mb-0">{{ records.patient.patient_name }}</h4>
                    <h6 class="mb-1">{{ records.patient.custom_cpr }}</h6>
                    <p class="mb-1">{{ records.patient.dob + ' (' + records.patient.age + 'yrs), ' + (records.patient.sex.slice(0, 1) || '')}}</p>
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
                  <img 
                  v-if="records.practitioner && records.practitioner.image && !practitionerConflict" 
                  class="me-3 avatar avatar-xl bg-primary-light rounded-circle"
                  :src="records.practitioner.image" alt="..."
                  >
                  <div class="text-start">
                    <div class="d-flex">
                      <h4 :class="{'mb-1': true, 'text-red': practitionerConflict}">{{ records.practitioner.practitioner_name }}</h4>
                      <span v-if="practitionerConflict">&nbsp;&nbsp;->&nbsp;&nbsp;</span>
                      <img 
                      v-if="practitionerConflict && $resources.user.image" 
                      class="me-3 avatar avatar-xl bg-primary-light rounded-circle"
                      :src="$resources.user.image" alt="..."
                      >
                      <h4 v-if="practitionerConflict" class="mb-1 text-green">{{ $resources.user.name }}</h4>
                    </div>
                    <p v-if="records.appointment.service_unit" class="mb-0">Service Unit: {{ records.appointment.service_unit }}</p>
                    <p v-if="records.appointment.department" class="mb-0">{{ records.appointment.department }}</p>
                    <h4 class="mt-2 mb-0">{{ diagnosticForm.encounter_start_time.format('h:mm A') }}</h4>
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
            <template #title>Visit Logs<a class="fs-6 float-end" :class="{'d-none': records.encounters.length <= 4}">See All</a></template>
            <template #content>
              <DataTable :value="records.encounters" selectionMode="single" :metaKeySelection="true" dataKey="id" @row-click="visitLogSelect">
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
              <v-btn class="float-end text-orange" prepend-icon="pi pi-plus" variant="plain">Add</v-btn>
            </template>
            <template #content>
              <DataTable :value="records.services">
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
              <v-btn class="float-end text-orange" prepend-icon="pi pi-plus" variant="plain">Add</v-btn>
            </template>
            <template #content>
              <div
              class="d-flex align-items-center pb-4"
              :class="{'border-bottom': index < records.attachments.length -1, 'pt-4': index > 0}"
              v-for="(doc, index) in records.attachments"
              :key="index"
              >
                <v-hover v-slot="{ isHovering, props }">
                  <div class="me-4">
                    <Image v-if="doc.type === 'image'" :src="doc.attachment" preview width="40" :maskVisible="isHovering"/>
                    <i v-else-if="doc.type === 'pdf' || doc.type === 'word'" :class="`pi pi-file-${doc.type}`" style="font-size: 2.5rem" />
                    <!-- <v-btn v-else-if="doc.type === 'pdf' || doc.type === 'word'" class="ma-2" :icon="`pi pi-file-${doc.type}`" variant="text" style="font-size: 5.5rem"></v-btn> -->
                  </div>
                  <div class="d-flex flex-column flex-grow-1">
                    <h4>{{ doc.attachment_name }}</h4>
                  </div>
                  <div class="text-end fw-500">
                    <p class="text-fade mb-0">{{ doc.creation }}</p>
                  </div>
                </v-hover>
              </div>
            </template>
            <template #footer>
              <a v-if="records.attachments.length > 4" class="float-end" >View All</a>
            </template>
          </Card>
        </div>
      </div>
      <div class="col-xl-3 col-12 ps-0 right-column">
        <Card class="p-0 mb-3 gap-card" id="patient-history" style="overflow: hidden;">
          <template #title>Patient History</template>
          <template #content>
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

            <v-card class="p-0 gap-card" id="infected-diseases" variant="tonal" color="light-green">
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

            <v-card class="p-0 gap-card" id="surgical-history" variant="tonal" color="purple">
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

            <v-card class="p-0 gap-card" id="medications" variant="tonal" color="pink">
              <template v-slot:title>
                Medications ({{ records.patient.custom_medications.length }})
              </template>
              <template v-slot:text>
                <div
                class="d-flex align-items-center flex-column py-3"
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

            <v-card class="p-0 gap-card" id="habits" variant="tonal" color="teal">
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

            <v-card class="p-0 gap-card" id="family-history" variant="tonal" color="brown">
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

            <v-card class="p-0 gap-card" id="risk-factors" variant="tonal" color="deep-orange">
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
          </template>
        </Card>
      </div> 
      <v-divider color="black" inset class="my-6" style="max-width: calc(100% - 180px)"></v-divider>
      <div class="ps-0 mt-3 col-12 mb-25">
        <Card class="mb-4">
          <template #content>
            <a-form layout="vertical" :model="diagnosticForm">
              <Stepper orientation="vertical">
                <StepperPanel header="Complaint">
                  <template #content="{ nextCallback }">
                    <v-sheet>
                      <v-container>
                        <v-row>
                          <v-col>
                            <a-form-item label="Symptoms">
                              <a-select
                                v-model:value="diagnosticForm.symptoms"
                                :options="$resources.complaints"
                                :fieldNames="{label: 'complaints', value: 'complaints'}"
                                mode="multiple"
                                style="width: 100%"
                              ></a-select>
                            </a-form-item>
                            <a-form-item label="Symptoms Duration">
                              <a-input v-model:value="diagnosticForm.period" />
                            </a-form-item>
                            <a-form-item label="Note">
                              <a-textarea v-model:value="diagnosticForm.note" :rows="4" />
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
                <StepperPanel header="Investigation">
                  <template #content="{ prevCallback, nextCallback }">
                    <v-sheet>
                      <v-container>
                        <v-row>
                          <v-col>
                            <a-form-item label="Physical Examination">
                              <a-textarea v-model:value="diagnosticForm.physicalExamination" :rows="4" />
                            </a-form-item>
                            <a-form-item label="Other Examination">
                              <a-textarea v-model:value="diagnosticForm.otherExamination" :rows="4" />
                            </a-form-item>
                            <h3 class="mt-3">Diagnostic Procedure</h3>
                            <div class="d-flex gap-2">
                              <v-btn variant="flat" color="primary" @click="() => {labTestActive = true}">Lab Test</v-btn>
                              <v-btn variant="flat" color="primary" disabled>Radiology Test</v-btn>
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
                <StepperPanel header="Assessment And Diagnosis">
                  <template #content="{ prevCallback, nextCallback }">
                    <v-sheet>
                      <v-container>
                        <v-row>
                          <v-col>
                            <a-form-item label="Diagnosis">
                              <a-select
                                v-model:value="diagnosticForm.diagnosis"
                                :options="$resources.diagnosis"
                                :fieldNames="{label: 'diagnosis', value: 'diagnosis'}"
                                mode="multiple"
                                style="width: 100%"
                              ></a-select>
                            </a-form-item>
                            <a-form-item label="Differential Diagnosis">
                              <a-select
                                v-model:value="diagnosticForm.differentialDiagnosis"
                                :options="$resources.diagnosis"
                                :fieldNames="{label: 'diagnosis', value: 'diagnosis'}"
                                mode="multiple"
                                style="width: 100%"
                              ></a-select>
                            </a-form-item>
                            <a-form-item label="Diagnosis Note">
                              <a-textarea v-model:value="diagnosticForm.diagnosisNote" :rows="4" />
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
                <StepperPanel header="Treatment">
                  <template #content="{ prevCallback, nextCallback }">
                    <v-sheet>
                      <v-container>
                        <v-row>
                          <v-col>
                            <div class="d-flex gap-2">
                              <v-btn variant="flat" color="orange" @click="() => {medicationRequestActive = true}">Medications</v-btn>
                              <v-btn variant="flat" color="orange" disabled>Surgical Procedure</v-btn>
                              <v-btn variant="flat" color="orange" disabled>Therapeutic Procedure</v-btn>
                              <v-btn variant="flat" color="orange" disabled>Physiotherapy Session</v-btn>
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
                <StepperPanel header="Order">
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
                      <v-btn variant="flat" color="purple-darken-4" @click="submitEncounter">Submit</v-btn>
                    </div>
                  </template>
                </StepperPanel>
              </Stepper>
            </a-form>
          </template>
        </Card>
      </div> 
    </div>
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
  </div>
</template>

<script>
import dayjs from 'dayjs';
import { VEmptyState } from 'vuetify/labs/VEmptyState';
import { VSlideGroup, VSlideGroupItem } from 'vuetify/components/VSlideGroup';
import { VProgressCircular } from 'vuetify/components/VProgressCircular';
import { VProgressLinear } from 'vuetify/components/VProgressLinear';
import { VBtn } from 'vuetify/components/VBtn';
import { VChip } from 'vuetify/components/VChip';
import { VContainer, VRow, VCol } from 'vuetify/components/VGrid';
import { VSelect } from 'vuetify/components/VSelect';
import { VDivider } from 'vuetify/components/VDivider';
import { VStepper, VStepperHeader, VStepperItem, VStepperActions, VStepperWindow, VStepperWindowItem } from 'vuetify/components/VStepper';
import { VSheet } from 'vuetify/components/VSheet';
import { VCard } from 'vuetify/components/VCard';
import { VAlert } from 'vuetify/components/VAlert';
import { VHover } from 'vuetify/components/VHover'

import Card from 'primevue/card';
import Divider from 'primevue/divider';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Stepper from 'primevue/stepper';
import StepperPanel from 'primevue/stepperpanel';
import Image from 'primevue/image';

import { ref, reactive } from 'vue';

import encounterRecords from '@/assets/json/encounterrecords.json'
import soundImage from '@/assets/img/sound.png';
import lungsImage from '@/assets/img/lungs.png';
import celsiusImage from '@/assets/img/celsius.png';

export default {
  inject: ['$call'],
  components: {
    Card, Divider, VSlideGroup, VSlideGroupItem, DataTable, Column, VBtn, VProgressCircular, VProgressLinear, VChip, VEmptyState, VContainer,
    VRow, VCol, VSelect, VDivider, VStepper, VStepperHeader, VStepperItem, VStepperActions, VStepperWindow, VStepperWindowItem, VSheet, VCard, 
    Stepper, StepperPanel, VAlert, Image, VHover
  }, 
  computed: {
    diagnosticForm() {
      return reactive({
        encounter_start_time: dayjs(),
        symptoms: [],
        period: 0,
        note: '',
        physicalExamination: '',
        otherExamination: '',
        diagnosis: [],
        differentialDiagnosis: [],
        diagnosisNote: '',
			});
    },
    diagnosticFormRules() {
      return reactive({
        encounter_start_time: [{ required: true, message: 'Please enter start time!' }],
        appointment_type: [{ required: true, message: 'Please choose a type!' }],
        patient: [{ required: true, message: 'Please choose a patient!' }],
        practitioner: [{ required: this.appointmentForm.appointment_for === 'Practitioner', message: 'Please choose a practitioner!' }],
        department: [{ required: this.appointmentForm.appointment_for === 'Department', message: 'Please choose a department!' }],
        service_unit: [{ required: this.appointmentForm.appointment_for === 'Service Unit', message: 'Please choose a service unit!' }],
        appointment_date: [{ required: true, message: 'Please choose a date!' }],
      });
    },
  },
  data() {
    return {
      currentFormStep: 0,
      records: ref(encounterRecords),
      currentVS: {
        name: '',
        pulse: "-",
        respiratory_rate: "-",
        bp_systolic: "-",
        bp_diastolic: "-",
        temperature: "-",
        signs_date: '-',
      },
      isAffixed:false,
      lungsImage:lungsImage,
      celsiusImage:celsiusImage,
      soundImage:soundImage,
      pastVisitEditRow: '',
      diagnosisFormSteps:['Complaint', 'Investigation', 'Assessment and Diagnosis', 'Treatment', 'Order'],
      practitionerConflict: false,
      vitalSignsActive: false,
      pastVisitsActive: false,
      labTestActive: false,
      medicationRequestActive: false,
      message: '',
      alertVisible: false,
    };
  },
  created() {
    this.fetchRecords();
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
      this.$call('healthcare_doworks.api.methods.patient_encounter_records', {appointment: this.$route.params.appointmentId}).then(response => {
        console.log(response)
        response.patient.dob = dayjs(response.patient.dob).format('DD/MM/YYYY')
        response.patient.age = dayjs().diff(response.patient.dob, 'y')
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
        if(response.appointment.practitioner !== this.$resources.user.practitioner){
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
    submitEncounter() {
      const { validate } = Form.useForm(this.form, this.rules);
      validate().then(() => {
        this.lodingOverlay = true;
        let formClone = {...this.form}
        formClone.signs_date = dayjs(this.form.signs_date).format('YYYY-MM-DD')
        formClone.signs_time = dayjs(this.form.signs_time).format('HH:mm')
        this.$call('healthcare_doworks.api.methods.new_doc', {form: formClone, submit: true})
        .then(response => {
          this.lodingOverlay = false;
          this.closeDialog()
        }).catch(error => {
          console.error(error);
          let message = error.message.split('\n');
          message = message.find(line => line.includes('frappe.exceptions'));
          if(message){
            const firstSpaceIndex = message.indexOf(' ');
            this.showAlert(message.substring(firstSpaceIndex + 1) , 10000)
          }
        });
      })
      .catch(err => {
        console.log('error', err);
      });
    },
    visitLogSelect(row) {
      this.pastVisitEditRow = row.data;
      this.pastVisitsActive = true;
    },
    hidePreview() {
      this.previewUrl = null;
    },
    openPreview(row) {
      this.previewUrl = row.url;
      this.previewType = row.type;
      this.previewVisible = true;
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