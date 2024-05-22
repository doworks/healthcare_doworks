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
                    &nbsp;&nbsp;->&nbsp;&nbsp;
                    <img 
                    v-if="practitionerConflict && $resources.user.image" 
                    class="me-3 avatar avatar-xl bg-primary-light rounded-circle"
                    :src="$resources.user.image" alt="..."
                    >
                    <h4 v-if="practitionerConflict" class="mb-1 text-green">{{ $resources.user.name }}</h4>
                  </div>
                  <p v-if="records.appointment.service_unit" class="mb-0">Service Unit: {{ records.appointment.service_unit }}</p>
                  <p v-if="records.appointment.department" class="mb-0">{{ records.appointment.department }}</p>
                  <h4 class="mt-2 mb-0">{{ startTime.format('h:mm A') }}</h4>
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
                      &nbsp;&nbsp;->&nbsp;&nbsp;
                      <img 
                      v-if="practitionerConflict && $resources.user.image" 
                      class="me-3 avatar avatar-xl bg-primary-light rounded-circle"
                      :src="$resources.user.image" alt="..."
                      >
                      <h4 v-if="practitionerConflict" class="mb-1 text-green">{{ $resources.user.name }}</h4>
                    </div>
                    <p v-if="records.appointment.service_unit" class="mb-0">Service Unit: {{ records.appointment.service_unit }}</p>
                    <p v-if="records.appointment.department" class="mb-0">{{ records.appointment.department }}</p>
                    <h4 class="mt-2 mb-0">{{ startTime.format('h:mm A') }}</h4>
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
              <DataTable :value="records.encounters">
                <Column field="date" header="Date"></Column>
                <Column field="practitioner_name" header="Practitioner"></Column>
                <Column field="appointment_category" header="Type"></Column>
                <Column field="diagnosis" header="Reason"></Column>
              </DataTable>
            </template>
          </Card>
        </div>
        <div class="mb-3 col-12 pe-0">
          <Card class="p-0" id="services" style="overflow: hidden;">
            <template #title>
              <span class="align-middle">Services Request / Results ({{ services.length }})</span>
              <v-btn class="float-end text-orange" prepend-icon="pi pi-plus" variant="plain">Add</v-btn>
            </template>
            <template #content>
              <DataTable :value="services">
                <Column field="service" header="Service Name"></Column>
                <Column field="prescripedOn" header="Presciped On"></Column>
                <Column field="status" header="Status"></Column>
                <Column field="prescripedBy" header="Presciped By"></Column>
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
                :class="{'border-bottom': index < attachments.length -1, 'pt-4': index > 0}"
                v-for="(doc, index) in attachments"
                :key="index"
              >
                <div class="me-4">
                  <i :class="doc.icon" style="font-size: 2.5rem"/>
                </div>
                <div class="d-flex flex-column flex-grow-1">
                  <h4>{{ doc.item }}</h4>
                </div>
                <div class="text-end fw-500">
                  <p class="text-fade mb-0">{{ doc.date }}</p>
                </div>
              </div>
            </template>
            <template #footer>
              <a v-if="attachments.length > 4" class="float-end" >View All</a>
            </template>
          </Card>
        </div>
      </div>
      <div class="col-xl-3 col-12 ps-0 right-column">
        <Card class="p-0 mb-3 gap-card" id="patient-history" style="overflow: hidden;">
          <template #title>Patient History</template>
          <template #content>
            <v-card class="p-0 mb-3" id="allergies" variant="text">
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

            <v-card class="p-0 mb-3 gap-card" id="infected-diseases" variant="text">
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

            <v-card class="p-0 mb-3 gap-card" id="surgical-history" variant="text">
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

            <v-card class="p-0 mb-3 gap-card" id="medications" variant="text">
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

            <v-card class="p-0 mb-3 gap-card" id="habits" variant="text">
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

            <v-card class="p-0 mb-3 gap-card" id="family-history" variant="text">
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

            <v-card class="p-0 mb-3 gap-card" id="risk-factors" variant="text">
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
        <!-- <v-stepper class="mb-4" v-model="currentFormStep" non-linear>
          <template v-slot:default="{ prev, next }">
            <v-stepper-header>
              <template v-for="(n, index) in diagnosisFormSteps" :key="`${n}-step`">
                <v-stepper-item
                  :complete="currentFormStep > index"
                  :step="`Step {{ index }}`"
                  :value="index"
                  editable
                  :edit-icon="`fa-solid fa-${index + 1}`"
                >{{n}}</v-stepper-item>

                <v-divider
                  v-if="index < diagnosisFormSteps.length -1"
                  :key="n"
                ></v-divider>
              </template>
            </v-stepper-header>

            <a-form layout="vertical" :model="diagnosticForm">
              <v-stepper-window>
                <v-stepper-window-item :value="0" key="Complaint-content">
                  <v-sheet>
                    <v-container>
                      <v-row>
                        <v-col>
                          <a-form-item label="Symptoms">
                            <a-select
                              v-model:value="diagnosticForm.complaint.symptoms"
                              :options="$resources.complaints"
                              :fieldNames="{label: 'complaints', value: 'complaints'}"
                              mode="multiple"
                              style="width: 100%"
                            ></a-select>
                          </a-form-item>
                          <a-form-item label="Symptoms Duration">
                            <a-input v-model:value="diagnosticForm.complaint.period" />
                          </a-form-item>
                          <a-form-item label="Note">
                            <a-textarea v-model:value="diagnosticForm.complaint.note" :rows="4" />
                          </a-form-item>
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-sheet>
                </v-stepper-window-item>
                <v-stepper-window-item :value="1" key="Investigation-content">
                  <v-sheet>
                    <v-container>
                      <v-row>
                        <v-col>
                          <a-form-item label="Physical Examination">
                            <a-input v-model:value="diagnosticForm.investigation.physicalExamination" />
                          </a-form-item>
                          <h3 class="mt-3 mb-1">Diagnostic Procedure</h3>
                          <a-form-item label="Lab Test" class="ps-15">
                            <a-input v-model:value="diagnosticForm.investigation.diagnosticProcedure.labTest" />
                          </a-form-item>
                          <a-form-item label="Radiology Test" class="ps-15">
                            <a-input v-model:value="diagnosticForm.investigation.diagnosticProcedure.radiologyTest" />
                          </a-form-item>
                          <a-form-item label="Other Examination">
                            <a-input v-model:value="diagnosticForm.investigation.otherExamination" />
                          </a-form-item>
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-sheet>
                </v-stepper-window-item>
                <v-stepper-window-item :value="2" key="Assessment And Diagnosis-content">
                  <v-sheet>
                    <v-container>
                      <v-row>
                        <v-col>
                          <a-form-item label="Diagnosis">
                            <a-select
                              v-model:value="diagnosticForm.assessmentAndDiagnosis.diagnosis"
                              :options="$resources.diagnosis"
                              :fieldNames="{label: 'diagnosis', value: 'diagnosis'}"
                              mode="multiple"
                              style="width: 100%"
                            ></a-select>
                          </a-form-item>
                          <a-form-item label="Differential Diagnosis">
                            <a-input v-model:value="diagnosticForm.assessmentAndDiagnosis.differentialDiagnosis" />
                          </a-form-item>
                          <a-form-item label="Diagnosis Note">
                            <a-textarea v-model:value="diagnosticForm.assessmentAndDiagnosis.diagnosisNote" :rows="4" />
                          </a-form-item>
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-sheet>
                </v-stepper-window-item>
                <v-stepper-window-item :value="3" key="Treatment-content">
                  <v-sheet>
                    <v-container>
                      <v-row>
                        <v-col>
                          <a-form-item label="Medications">
                            <a-input v-model:value="diagnosticForm.treatment.medications" />
                          </a-form-item>
                          <a-form-item label="Surgical Procedure">
                            <a-input v-model:value="diagnosticForm.treatment.surgicalProcedure" />
                          </a-form-item>
                          <a-form-item label="Therapeutic Procedure">
                            <a-input v-model:value="diagnosticForm.treatment.therapeuticProcedure" />
                          </a-form-item>
                          <a-form-item label="Physiotherapy Session">
                            <a-input v-model:value="diagnosticForm.treatment.physiotherapySession" />
                          </a-form-item>
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-sheet>
                </v-stepper-window-item>
                <v-stepper-window-item :value="4" key="Order-content">
                  <v-sheet>
                    <v-container>
                      <v-row>
                        <v-col>
                          <a-form-item label="Medications">
                            <a-input v-model:value="diagnosticForm.order.medications" />
                          </a-form-item>
                          <a-form-item label="Lab Test">
                            <a-input v-model:value="diagnosticForm.order.labTest" />
                          </a-form-item>
                          <a-form-item label="Radiology Test">
                            <a-input v-model:value="diagnosticForm.order.radiologyTest" />
                          </a-form-item>
                          <a-form-item label="Transfer To Other Hospital">
                            <a-input v-model:value="diagnosticForm.order.transferToOtherHospital" />
                          </a-form-item>
                          <a-form-item label="Transfer To Other Doctor">
                            <a-input v-model:value="diagnosticForm.order.transferToOtherDoctor" />
                          </a-form-item>
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-sheet>
                </v-stepper-window-item>
              </v-stepper-window>
            </a-form>
                
            <v-stepper-actions
              @click:next="next"
              @click:prev="prev"
            ></v-stepper-actions>
          </template>
        </v-stepper> -->

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

import Card from 'primevue/card';
import Divider from 'primevue/divider';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import Stepper from 'primevue/stepper';
import StepperPanel from 'primevue/stepperpanel';

import { ref, reactive } from 'vue';

import soundImage from '@/assets/img/sound.png';
import lungsImage from '@/assets/img/lungs.png';
import celsiusImage from '@/assets/img/celsius.png';

export default {
  inject: ['$call'],
  components: {
    Card, Divider, VSlideGroup, VSlideGroupItem, DataTable, Column, VBtn, VProgressCircular, VProgressLinear, VChip, VEmptyState, VContainer,
    VRow, VCol, VSelect, VDivider, VStepper, VStepperHeader, VStepperItem, VStepperActions, VStepperWindow, VStepperWindowItem, VSheet, VCard, 
    Stepper, StepperPanel, VAlert,
  }, 
  computed: {
    diagnosticForm() {
      return reactive({
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
      records: ref({
        appointment:{
          appointment_date: '',
          appointment_time: "",
          appointment_type: "",
          custom_appointment_category: "",
          custom_appointment_time_logs: [],
          custom_visit_notes: [],
          department: "",
          duration: 0,
          name: "",
          patient: "",
          patient_name: "",
          patient_sex: "",
          practitioner: "",
          practitioner_name: "",
        },
        encounters:[{
          appointment_category: null,
          date: "",
          diagnosis: "",
          medical_department: "",
          name: "",
          patient_name: "",
          practitioner_name: "",
          symptoms: [],
          time: "",
        }],
        patient:{
          age: 0,
          blood_group: "",
          custom_allergies_table: [],
          custom_infected_diseases: [],
          custom_cpr: "",
          custom_habits__social: '',
          custom_medications: '',
          custom_chronic_diseases: '',
          custom_genetic_conditions: '',
          custom_risk_factors_table: [],
          custom_surgical_history_table: [],
          image: "",
          mobile: "",
          patient_name: "",
          sex: "",
        },
        practitioner:{
          department: "",
          gender: "",
          mobile_phone: "",
          practitioner_name: "",
        },
        vitalSigns: [{
          abdomen: "",
          bmi: 0,
          bp_diastolic: "",
          bp_systolic: "",
          height: 0,
          nutrition_note: "",
          pulse: "",
          reflexes: "",
          respiratory_rate: "",
          signs_date: "",
          signs_time: "",
          temperature: "",
          tongue: "",
          vital_signs_note: null,
          weight: 0,
        }]
      }),
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
      services: [{
        service: 'Diabetes Test',
        prescripedOn: '06/03/2024',
        status: 'Pending',
        prescripedBy: 'Dr. Kevin Black',
        orderNumber: '2024DIBTT0215492',
      },
      {
        service: 'Head X-Ray',
        prescripedOn: '06/03/2024',
        status: 'In Process',
        prescripedBy: 'Dr. Kevin Black',
        orderNumber: '2024DIBTT0215492',
      }],
      attachments: [
        {item: 'Chest X-Ray', date: '02/03/2024', icon: 'pi pi-file-pdf'},
        {item: 'Ecg Test Report', date: '08/03/2024', icon: 'pi pi-file-word'},
        {item: 'Chest X-Ray', date: '12/03/2024', icon: 'pi pi-file-pdf'},
      ],
      lungsImage:lungsImage,
      celsiusImage:celsiusImage,
      soundImage:soundImage,
      diagnosisFormSteps:['Complaint', 'Investigation', 'Assessment and Diagnosis', 'Treatment', 'Order'],
      practitionerConflict: false,
      startTime: dayjs(),
      vitalSignsActive: false,
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
      this.$call('healthcare_doworks.api.methods.patient_encounter_records', {appointment: this.$route.params.appointmentId})
      .then(response => {
        response.patient.dob = dayjs(response.patient.dob).format('DD/MM/YYYY')
        response.patient.age = dayjs().diff(response.patient.dob, 'y')
        response.encounters = response.encounters.map((value, index) => {
          value.date = dayjs(value.encounter_date).format('DD/MM/YYYY')
          value.diagnosis = value.diagnosis.join(', ')
          return value
        })
        if(response.vitalSigns.length > 0){
          response.vitalSigns = response.vitalSigns.map((value, index) => {
            value.signs_date = dayjs(value.signs_date).format('DD/MM/YYYY')
            return value
          })
          this.currentVS = response.vitalSigns[0];
        }
        if(response.appointment.practitioner_name !== this.$resources.user.name){
          this.practitionerConflict = true
        }
        this.records = response
        console.log(this.records)
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