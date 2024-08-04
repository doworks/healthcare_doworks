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
              <!-- <img 
              v-if="records.practitioner && records.practitioner.image && !practitionerConflict" 
              class="me-3 avatar avatar-xl bg-primary-light rounded-circle"
              :src="records.practitioner.image" alt="..."
              > -->
              <v-avatar 
              v-if="records.practitioner && records.practitioner.image && !practitionerConflict" 
              size="80" 
              class="me-3" 
              :image="records.practitioner.image">
              </v-avatar>
              <div class="text-start">
                <div class="d-flex">
                  <h4 :class="{'mb-1': true, 'text-red': practitionerConflict}">{{ records.practitioner.practitioner_name }}</h4>
                  <span v-if="practitionerConflict">&nbsp;&nbsp;->&nbsp;&nbsp;</span>
                  <v-avatar 
                  v-if="practitionerConflict && $resources.user.practitioner_image" 
                  size="80" 
                  class="me-3" 
                  :image="$resources.user.practitioner_image">
                  </v-avatar>
                  <!-- <img 
                  v-if="practitionerConflict && $resources.user.practitioner_image" 
                  class="me-3 avatar avatar-xl bg-primary-light rounded-circle"
                  :src="$resources.user.practitioner_image" alt="..."
                  /> -->
                  <h4 v-if="practitionerConflict" class="mb-1 text-green">{{ $resources.user.practitioner_name || $resources.user.name }}</h4>
                </div>
                <p v-if="records.appointment.service_unit" class="mb-0">Service Unit: {{ records.appointment.service_unit }}</p>
                <p v-if="records.appointment.department" class="mb-0">{{ records.appointment.department }}</p>
                <h4 class="mt-2 mb-0">{{ form.custom_encounter_start_time.format('h:mm A') }}</h4>
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
                  <!-- <img 
                  v-if="records.practitioner && records.practitioner.image && !practitionerConflict" 
                  class="me-3 avatar avatar-xl bg-primary-light rounded-circle"
                  :src="records.practitioner.image" alt="..."
                  > -->
                  <v-avatar 
                  v-if="records.practitioner && records.practitioner.image && !practitionerConflict" 
                  size="80" 
                  class="me-3" 
                  :image="records.practitioner.image">
                  </v-avatar>
                  <div class="text-start">
                    <div class="d-flex">
                      <h4 :class="{'mb-1': true, 'text-red': practitionerConflict}">{{ records.practitioner.practitioner_name }}</h4>
                      <span v-if="practitionerConflict">&nbsp;&nbsp;->&nbsp;&nbsp;</span>
                      <v-avatar 
                      v-if="practitionerConflict && $resources.user.practitioner_image" 
                      size="80" 
                      class="me-3" 
                      :image="$resources.user.practitioner_image">
                      </v-avatar>
                      <!-- <img 
                      v-if="practitionerConflict && $resources.user.practitioner_image" 
                      class="me-3 avatar avatar-xl bg-primary-light rounded-circle"
                      :src="$resources.user.practitioner_image" alt="..."
                      /> -->
                      <h4 v-if="practitionerConflict" class="mb-1 text-green">{{ $resources.user.practitioner_name || $resources.user.name }}</h4>
                    </div>
                    <p v-if="records.appointment.service_unit" class="mb-0">Service Unit: {{ records.appointment.service_unit }}</p>
                    <p v-if="records.appointment.department" class="mb-0">{{ records.appointment.department }}</p>
                    <h4 class="mt-2 mb-0">{{ form.custom_encounter_start_time.format('h:mm A') }}</h4>
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
              <DataTable :value="records.encounters ? records.encounters.slice(0, 5) : records.encounters" selectionMode="single" :metaKeySelection="true" dataKey="id" @row-click="visitLogSelect">
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
              <v-btn class="float-end text-orange" prepend-icon="pi pi-plus" variant="plain">Add</v-btn>
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
              <div
              class="d-flex align-items-center pb-4"
              :class="{'border-bottom': index < records.attachments.length -1, 'pt-4': index > 0, 'd-none': records.attachments.length == 0}"
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
        <Card class="p-0 mb-3" id="patient-history" style="overflow: hidden;">
          <template #title>Patient History</template>
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
            <a-form layout="vertical" :model="form">
              <SelectButton v-model="formState" :options="formOptions" class="text-center" :allowEmpty="false" @change="setStepperValue"/>
              <Stepper orientation="vertical" v-model:value="stepperValue">
                <!-- Procedural Panels -->
                <StepperPanel value="Procedure Info" header="Procedure Info" v-if="formState === 'Procedural'">
                  <template #content="{ nextCallback }">
                    <v-sheet>
                      <v-container>
                        <v-row>
                          <v-col cols="12" md="6">
                            <a-form-item label="Clinical Procedure Category">
                              <a-select
                                allowClear
                                v-model:value="form.symptoms"
                                :options="$resources.complaints"
                                :fieldNames="{label: 'complaints', value: 'complaints'}"
                                style="width: 100%"
                              ></a-select>
                            </a-form-item>
                            <a-form-item label="Practitioner">
                              <a-select
                                allowClear
                                v-model:value="form.practitioner"
                                :options="$resources.practitioners"
                                :fieldNames="{label: 'practitioner_name', value: 'name'}"
                                style="width: 100%"
                              ></a-select>
                            </a-form-item>
                            <a-form-item label="Medical Department">
                              <a-select
                                allowClear
                                v-model:value="form.medical_department"
                                :options="$resources.departments"
                                :fieldNames="{label: 'department', value: 'department'}"
                                style="width: 100%"
                              ></a-select>
                            </a-form-item>
                            <a-form-item label="Medical Department">
                              <a-select
                                allowClear
                                v-model:value="records.appointment.service_unit"
                                :options="$resources.serviceUnits"
                                :fieldNames="{label: 'name', value: 'name'}"
                                style="width: 100%"
                              ></a-select>
                            </a-form-item>
                          </v-col>
                          <v-col cols="12" md="6">
                            <a-form-item label="Procedure Template">
                              <a-select
                                allowClear
                                v-model:value="form.symptoms"
                                :options="$resources.complaints"
                                :fieldNames="{label: 'complaints', value: 'complaints'}"
                                style="width: 100%"
                              ></a-select>
                            </a-form-item>
                            <a-form-item label="Start Date">
                              <a-date-picker 
                                v-model:value="form.procedure_date"
                                @change="()=>{$emit('show-slots')}" 
                                format="DD-MM-YYYY" 
                                style="width: 100%;"
                              />
                            </a-form-item>
                            <a-form-item label="Start Time">
                              <a-time-picker v-model:value="form.procedure_date" use12-hours format="h:mm a" style="width: 100%;"/>
                            </a-form-item>
                            <a-form-item label="Notes">
                              <a-textarea :rows="4" />
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
                <StepperPanel value="Pre Procedure" header="Pre Procedure" v-if="formState === 'Procedural'">
                  <template #content="{ nextCallback }">
                    <v-sheet>
                      <v-container>
                        <v-row>
                          <v-col>
                            <a-form-item label="Sample">
                              <a-select
                                allowClear
                                v-model:value="form.symptoms"
                                :options="$resources.complaints"
                                :fieldNames="{label: 'complaints', value: 'complaints'}"
                                style="width: 100%"
                              ></a-select>
                            </a-form-item>
                            <a-form-item label="Pre Operative Diagnosis">
                              <a-textarea :rows="4" />
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
                <StepperPanel value="Procedure" header="Procedure" v-if="formState === 'Procedural'">
                  <template #content="{ nextCallback }">
                    <v-sheet>
                      <v-container>
                        <v-row>
                          <v-col>
                            <div class="d-flex gap-2">
                              <v-btn variant="flat" color="orange" disabled>Predefined Areas</v-btn>
                              <v-btn variant="flat" color="orange" disabled>Predefined Annotations</v-btn>
                              <v-btn variant="flat" color="orange" @click="() => {procedureActive = true}">Free Drawing</v-btn>
                            </div>
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-sheet>
                    <div class="d-flex pt-4">
                      <v-btn variant="flat" color="blue-darken-2" @click="nextCallback">Next</v-btn>
                    </div>
                  </template>
                </StepperPanel>
                <StepperPanel value="Post Procedure" header="Post Procedure" v-if="formState === 'Procedural'">
                  <template #content="{ nextCallback }">
                    <v-sheet>
                      <v-container>
                        <v-row>
                          <v-col>
                            <a-form-item label="Post Operative Diagnosis">
                              <a-textarea :rows="4" />
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
                
                <!-- Diagnostic & Follow-up Panels -->
                <StepperPanel value="Complaint" header="Complaint" v-if="formState === 'Diagnostic' || formState === 'Follow-up'">
                  <template #content="{ nextCallback }">
                    <v-sheet>
                      <v-container>
                        <v-row>
                          <v-col>
                            <a-form-item label="Symptoms">
                              <a-select
                                v-model:value="form.symptoms"
                                :options="$resources.complaints"
                                :fieldNames="{label: 'complaints', value: 'complaints'}"
                                mode="multiple"
                                style="width: 100%"
                              ></a-select>
                            </a-form-item>
                            <a-form-item label="Symptoms Duration">
                              <a-input v-model:value="form.period" />
                            </a-form-item>
                            <a-form-item label="Note">
                              <a-textarea v-model:value="form.note" :rows="4" />
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
                <StepperPanel value="Investigation" header="Investigation" v-if="formState === 'Diagnostic' || formState === 'Follow-up'">
                  <template #content="{ prevCallback, nextCallback }">
                    <v-sheet>
                      <v-container>
                        <v-row>
                          <v-col>
                            <a-form-item label="Physical Examination">
                              <a-textarea v-model:value="form.physicalExamination" :rows="4" />
                            </a-form-item>
                            <a-form-item label="Other Examination">
                              <a-textarea v-model:value="form.otherExamination" :rows="4" />
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
                <StepperPanel value="Illness Progression" header="Illness Progression" v-if="formState === 'Follow-up'">
                  <template #content="{ nextCallback }">
                    <v-sheet>
                      <v-container>
                        <v-row>
                          <v-col>
                            <a-textarea v-model:value="form.illness_progression" :rows="4" />
                          </v-col>
                        </v-row>
                      </v-container>
                    </v-sheet>
                    <div class="d-flex pt-4">
                      <v-btn variant="flat" color="blue-darken-2" @click="nextCallback">Next</v-btn>
                    </div>
                  </template>
                </StepperPanel>
                <StepperPanel value="Assessment And Diagnosis" header="Assessment And Diagnosis" v-if="formState === 'Diagnostic' || formState === 'Follow-up'">
                  <template #content="{ prevCallback, nextCallback }">
                    <v-sheet>
                      <v-container>
                        <v-row>
                          <v-col>
                            <a-form-item label="Diagnosis">
                              <a-select
                                v-model:value="form.diagnosis"
                                :options="$resources.diagnosis"
                                :fieldNames="{label: 'diagnosis', value: 'diagnosis'}"
                                mode="multiple"
                                style="width: 100%"
                              ></a-select>
                            </a-form-item>
                            <a-form-item label="Differential Diagnosis">
                              <a-select
                                v-model:value="form.differentialDiagnosis"
                                :options="$resources.diagnosis"
                                :fieldNames="{label: 'diagnosis', value: 'diagnosis'}"
                                mode="multiple"
                                style="width: 100%"
                              ></a-select>
                            </a-form-item>
                            <a-form-item label="Diagnosis Note">
                              <a-textarea v-model:value="form.diagnosisNote" :rows="4" />
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
                <StepperPanel value="Treatment" header="Treatment" v-if="formState === 'Diagnostic' || formState === 'Follow-up'">
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
                              <v-btn variant="flat" color="orange" @click="() => {procedureActive = true}">Chartings</v-btn>
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
                <StepperPanel value="Order" header="Order" v-if="formState === 'Diagnostic' || formState === 'Follow-up'">
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
                <v-btn variant="flat" color="lime" @click="submitEncounter()">Save</v-btn>
                <v-btn variant="flat" color="amber" @click="submitEncounter(true)">Submit</v-btn>
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
      :parentType="form.doctype"
      :parent="form.name"
      fieldName="custom_attachments"
      :isChild="true"
      />
      <procedureDialog 
      :isOpen="procedureActive" 
      @update:isOpen="procedureActive = $event" 
      @show-alert="showAlert" 
      />
    </div>
  </div>
</template>

<script>
import dayjs from 'dayjs';
import { VEmptyState } from 'vuetify/labs/VEmptyState';
import { VSlideGroup, VSlideGroupItem } from 'vuetify/components/VSlideGroup';
import { VProgressLinear } from 'vuetify/components/VProgressLinear';
import { VChip } from 'vuetify/components/VChip';
import { VContainer, VRow, VCol } from 'vuetify/components/VGrid';
import { VSelect } from 'vuetify/components/VSelect';
import { VDivider } from 'vuetify/components/VDivider';
import { VStepper, VStepperHeader, VStepperItem, VStepperActions, VStepperWindow, VStepperWindowItem } from 'vuetify/components/VStepper';
import { VSheet } from 'vuetify/components/VSheet';
import { VHover } from 'vuetify/components/VHover';
import { VAvatar } from 'vuetify/components/VAvatar';
import ExcalidrawWrapper from '@/components/ExcalidrawWrapper.vue';

import { ref, reactive } from 'vue';
import { Form } from 'ant-design-vue';

import encounterRecords from '@/assets/json/encounterrecords.json'
import soundImage from '@/assets/img/sound.png';
import lungsImage from '@/assets/img/lungs.png';
import celsiusImage from '@/assets/img/celsius.png';

export default {
  inject: ['$call'],
  components: {
    VSlideGroup, VSlideGroupItem, VProgressLinear, VChip, VEmptyState, VContainer, VAvatar,
    VRow, VCol, VSelect, VDivider, VStepper, VStepperHeader, VStepperItem, VStepperActions, VStepperWindow, VStepperWindowItem, VSheet,
    Image, VHover, ExcalidrawWrapper,
  }, 
  computed: {
    
  },
  data() {
    return {
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
      labTestActive: false,
      medicationRequestActive: false,
      addAttachmentActive: false,
      procedureActive: false,
      message: '',
      alertVisible: false,
      formOptions: ['Procedural', 'Diagnostic', 'Follow-up', 'Session'],
      stepperValue: 'Complaint',
      formState: 'Diagnostic',
      form: reactive({
        doctype: 'Patient Encounter',
        name: '',
        custom_encounter_start_time: dayjs(),
        procedure_date: dayjs(),
        symptoms: [],
        period: 0,
        note: '',
        physicalExamination: '',
        otherExamination: '',
        diagnosis: [],
        differentialDiagnosis: [],
        diagnosisNote: '',
        appointment: '',
        appointment_type: '',
        custom_appointment_category: '',
        patient: '',
        patient_name: '',
        patient_sex: '',
        patient_age: '',
        original_practitioner: '',
        original_practitioner_name: '',
        practitioner: '',
        practitioner_name: '',
        medical_department: '',
        illness_progression: '',
			}),
    };
  },
  created() {
    this.fetchRecords();
  },
  mounted() {
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
      this.$call('healthcare_doworks.api.methods.patient_encounter_records', {appointment_id: this.$route.params.appointmentId})
      .then(response => {
        console.log(response)
        response.current_encounter.custom_encounter_start_time = dayjs(response.current_encounter.custom_encounter_start_time)
        this.form = {...this.form, ...response.current_encounter}
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
    submitEncounter(submit = false) {
      const { validate } = Form.useForm(this.form, this.rules);
      validate().then(() => {
        this.lodingOverlay = true;
        let formClone = {...this.form}
        formClone.encounter_date = dayjs().format('YYYY-MM-DD')
        formClone.encounter_time = dayjs().format('HH:mm')
        formClone.custom_encounter_start_time = dayjs().format('YYYY-MM-DD HH:mm')
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
    },
    setStepperValue() {
      if(this.formState === 'Diagnostic'){
        this.stepperValue = 'Complaint';
        return;
      }
      if(this.formState === 'Follow-up'){
        this.stepperValue = 'Illness Progression';
        return;
      }
      if(this.formState === 'Procedural'){
        this.stepperValue = 'Procedure Info';
        return;
      }
      this.stepperValue = 'Complaint';
    },
    // saveImage() {
    //   if (window.ExcalidrawAPI && window.ExcalidrawAPI.saveCanvasAsImage) {
    //     window.ExcalidrawAPI.saveCanvasAsImage();
    //   } else {
    //     console.error('Save function is not yet registered by React component');
    //   }
    // },
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