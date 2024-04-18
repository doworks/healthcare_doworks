<template>
  <div class="main-wrapper encounter-page">
    <div class="row w-100 mx-0">
      <div class="ps-0 pe-md-0 mt-2 mb-md-3 d-block col-12 col-md-6 d-lg-none">
        <Card :class="{
          'rounded-bottom-0': currentBreakpoint === 'sm' || currentBreakpoint === 'md',
          'rounded-end-0': currentBreakpoint !== 'sm' && currentBreakpoint !== 'md'
        }">
          <template #content>
            <div class="vital-sign-container d-flex align-items-center">
              <img class="me-3 avatar avatar-xl bg-primary-light rounded-circle" src="https://randomuser.me/api/portraits/men/1.jpg" alt="...">
              <div class="text-start d-flex flex-column gap-1">
                <h4 class="mb-0">S.Mohamed Adnan</h4>
                <p class="mb-0">01/12/1998 (25yrs), M</p>
                <p class="mb-0"><i class="pi pi-mobile align-middle"></i>32224737</p>
              </div>
            </div>
          </template>
        </Card>
      </div>
      <div class="ps-0 mb-3 mt-md-2 d-block col-12 col-md-6 d-lg-none">
        <Card :class="{
          'rounded-top-0': currentBreakpoint === 'sm' || currentBreakpoint === 'md',
          'rounded-start-0': currentBreakpoint !== 'sm' && currentBreakpoint !== 'md'
        }">
          <template #content>
            <div class="d-flex align-items-center">
              <img class="me-3 avatar avatar-xl bg-primary-light rounded-circle" src="https://randomuser.me/api/portraits/women/2.jpg" alt="...">
              <div class="text-start">
                <h4 class="mb-1">Dr. Kevin Black</h4>
                <p class="mb-0">Room: 4</p>
                <p class="mb-0">Cardiologists</p>
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
          <div class="px-0 d-none d-lg-block" style="width: unset;flex: 0 0 auto;" :class="{'ps-0': this.isAffixed}">
            <Card :class="['h-100 rounded-end-0',{'rounded-0': this.isAffixed}]">
              <template #content>
                <div class="vital-sign-container d-flex align-items-center">
                  <img class="me-3 avatar avatar-xl bg-primary-light rounded-circle" src="https://randomuser.me/api/portraits/men/1.jpg" alt="...">
                  <div class="text-start d-flex flex-column gap-1">
                    <h4 class="mb-0">S.Mohamed Adnan</h4>
                    <p class="mb-0">01/12/1998 (25yrs), M</p>
                    <p class="mb-0"><i class="pi pi-mobile align-middle"></i>32224737</p>
                  </div>
                </div>
              </template>
            </Card>
          </div>
          <div class="px-0" style="width: unset; flex-grow: 1; min-width: 0; flex-shrink: unset;">
            <Card :class="['h-100',{'rounded-0': this.isAffixed, 'rounded-start-0': currentBreakpoint === 'xxl'}]">
              <template #content>
                <v-slide-group mobile-breakpoint="sm">
                  <v-slide-group-item>
                    <div class="vital-sign-container align-self-center">
                      <div class="mb-2 gap-2 d-flex align-items-center">
                        <i class="pi pi-heart" style="font-size: 1.5rem"></i>
                        <h3 class="my-0 fw-normal">SYS</h3>
                      </div>
                      <div class="d-flex gap-1 align-items-center">
                        <h3 class="fw-normal mb-0">{{currentVS.sys}}</h3> <small class="align-self-end">mm Hg</small>
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
                      <div class="d-flex gap-1 align-items-center">
                        <h3 class="fw-normal mb-0">{{currentVS.dia}}</h3> <small class="align-self-end">mm Hg</small>
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
                      <div class="d-flex gap-1 align-items-center">
                        <h3 class="fw-normal mb-0">{{currentVS.hr}}</h3> <small class="align-self-end">BPM</small>
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
                      <div class="d-flex gap-1 align-items-center">
                        <h3 class="fw-normal mb-0">{{currentVS.rr}}</h3> <small class="align-self-end">BPM</small>
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
                      <div class="d-flex gap-1 align-items-center">
                        <h3 class="fw-normal mb-0">{{currentVS.bt + '\u00B0'}}</h3> <small class="align-self-end">C</small>
                      </div>
                    </div>
                  </v-slide-group-item>
                </v-slide-group>
                <div class="d-flex align-self-end ms-auto flex-shrink-0">
                  <v-select
                    v-model="currentVS"
                    item-title="date"
                    return-object
                    :items="vitalSigns"
                    variant="underlined"
                    class="w-full align-middle"
                  ></v-select>
                  <v-btn
                    class="ma-2 align-self-center"
                    color="blue"
                    density="comfortable"
                    icon="pi pi-pencil"
                  ></v-btn>
                </div>
              </template>
            </Card>
          </div>
          <div class="pe-0 d-none d-lg-block" style="width: 25.25%;flex: 0 0 auto;min-width: fit-content" :class="{'ps-0': this.isAffixed}">
            <Card :class="['h-100',{'rounded-0': this.isAffixed}]">
              <template #content>
                <div class="d-flex align-items-center">
                  <img class="me-3 avatar avatar-xl bg-primary-light rounded-circle" src="https://randomuser.me/api/portraits/women/2.jpg" alt="...">
                  <div class="text-start">
                    <h4 class="mb-1">Dr. Kevin Black</h4>
                    <p class="mb-0">Room: 4</p>
                    <p class="mb-0">Cardiologists</p>
                  </div>
                </div>
              </template>
            </Card>
          </div>
        </div>
      </a-affix>
      <div class="col-xl-9 col-12 ps-0 left-column row" style="margin-right: calc(.5 * var(--bs-gutter-x)); padding: 0">
        <div class="mb-3 col-12 pe-0">
          <Card class="p-0" id="past-encounters" style="overflow: hidden;">
            <template #title>Past Encounters<a class="fs-6 float-end" :class="{'d-none': pastEncounters.length <= 4}">See All</a></template>
            <template #content>
              <DataTable :value="pastEncounters">
                <Column field="date" header="Date"></Column>
                <Column field="practitioner" header="Practitioner"></Column>
                <Column field="type" header="Type"></Column>
                <Column field="reason" header="Reason"></Column>
              </DataTable>
            </template>
          </Card>
        </div>
        <div class="mb-3 col-12 pe-0">
          <Card class="p-0" id="services" style="overflow: hidden;">
            <template #title>
              <span class="align-middle">Outstanding Services ({{ services.length }})</span>
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
        <div class="col-xl-4 col-12 pe-0">
          <Card class="p-0 mb-3 border-bottom-title" id="family-history" style="overflow: hidden;">
            <template #title>Family History<a class="fs-6 float-end" :class="{'d-none': familyHistory.length <= 4}">See All</a></template>
            <template #content>
              <div
                class="d-flex align-items-center pb-4"
                :class="{'border-bottom': index < familyHistory.length -1, 'pt-4': index > 0}"
                v-for="(item, index) in familyHistory"
                :key="index"
              >
                <div class="d-flex flex-column flex-grow-1">
                  <h4 class="mb-0">{{ item.item }}</h4>
                </div>
                <div class="text-end fw-500">
                  <p class="text-fade mb-0">{{ item.relative }}</p>
                </div>
              </div>
            </template>
          </Card>
        </div>
        <div class="col-xl-4 col-12 pe-0">
          <Card class="p-0 mb-3 border-bottom-title gap-card" id="risk-factors" style="overflow: hidden;">
            <template #title>Risk Factors</template>
            <template #content>
              <div class="d-flex" v-for="(risk, index) in riskFactors" :key="index">
                <h4 class="col align-self-center">{{ risk.name }}</h4>
                <v-progress-circular
                  class="col"
                  :model-value="risk.value * 20"
                  :size="100"
                  :color="getSeverity(risk.value).color"
                >
                  {{ getSeverity(risk.value).risk }}
                </v-progress-circular>
              </div>
            </template>
          </Card>
        </div>
      </div>
      <div class="col-xl-3 col-12 ps-0 right-column">
        <Card class="p-0 mb-3 gap-card" id="allergies" style="overflow: hidden;">
          <template #title>Allergies ({{ allergies.length }})</template>
          <template #content>
            <div class="" v-for="(allergy, index) in allergies" :key="index">
              <div class="d-flex align-items-center justify-content-between mb-1">
                <h5>{{ allergy.name }}</h5>
                <v-chip :color="getSeverity(allergy.value).color" >
                  {{ getSeverity(allergy.value).severity }}
                </v-chip>
              </div>
              <v-progress-linear
                :color="getSeverity(allergy.value).color"
                :model-value="allergy.value * 20"
                rounded
              ></v-progress-linear>
            </div>
          </template>
        </Card>
        <Card class="p-0 mb-3 border-bottom-title" id="surgical-history" style="overflow: hidden;">
            <template #title>Surgical History<a class="fs-6 float-end" :class="{'d-none': surgicalHistory.length <= 4}">See All</a></template>
            <template #content>
              <div :class="{'d-none': surgicalHistory.length > 0}">
                <v-empty-state
                  icon="pi pi-question-circle"
                  text="This patient has no surgical history."
                  title="No Surgical History."
                ></v-empty-state>
              </div>
              <div
                class="d-flex pb-4"
                :class="{'border-bottom': index < surgicalHistory.length -1, 'pt-4': index > 0, 'd-none': surgicalHistory.length == 0}"
                v-for="(item, index) in surgicalHistory"
                :key="index"
              >
                <div class="d-flex flex-column flex-grow-1">
                  <h4 class="mb-0">{{ item.item }}</h4>
                  <p class="text-fade mb-0">{{ item.date }}</p>
                </div>
                <div class="text-end fw-500">
                  <h5 class="mb-0">{{ item.practitioner }}</h5>
                </div>
              </div>
            </template>
          </Card>
        <Card class="p-0 mb-3 border-bottom-title gap-card" id="medications" style="overflow: hidden;">
          <template #title>
            <span class="align-middle">Medications ({{ medications.length }})</span>
            <v-btn class="float-end text-orange" prepend-icon="pi pi-plus" variant="plain">Add</v-btn>
          </template>
          <template #content>
            <div
              class="d-flex align-items-center flex-column"
              :class="{'border-bottom': index < medications.length -1}"
              v-for="(medication, index) in medications"
              :key="index"
            >
              <div class="d-flex flex-row flex-grow-1 justify-content-between w-100">
                <h5 class="text-black mb-0 align-middle align-self-center">{{ medication.item }} <small class="text-fade">{{ medication.weight }}</small></h5>
                <div class="text-fade mb-0">
                  <v-chip :color=" medication.status == 'Active' ? 'grey-lighten-1' : 'grey-darken-2'" :variant=" medication.status == 'Active' ? 'flat' : 'tonal'">{{ medication.status }}</v-chip>
                </div>
              </div>
              <div class="d-flex flex-row justify-content-between w-100 mt-1">
                <p class="text-grey-darken-2">{{ medication.dose }}</p>
                <p class="text-grey-darken-2 text-center pe-2">{{ medication.duraion }}</p>
              </div>
            </div>
          </template>
        </Card>
      </div>
      <v-divider color="indigo" :thickness="2" inset class="my-6" style="max-width: calc(100% - 180px)"></v-divider>
      <div class="ps-0 mt-3 col-12 mb-25">
        <v-stepper class="mb-4" v-model="currentFormStep" non-linear>
          <template v-slot:default="{ prev, next }">
            <v-stepper-header>
              <template v-for="(n, index) in formSteps" :key="`${n}-step`">
                <v-stepper-item
                  :complete="currentFormStep > index"
                  :step="`Step {{ index }}`"
                  :value="index"
                  editable
                  :edit-icon="`fa-solid fa-${index + 1}`"
                >{{n}}</v-stepper-item>

                <v-divider
                  v-if="index < formSteps.length -1"
                  :key="n"
                ></v-divider>
              </template>
            </v-stepper-header>

            <v-stepper-window>
              <v-stepper-window-item
                v-for="(n, index) in formSteps"
                :key="`${n}-content`"
                :value="index"
              >
                <v-sheet>
                  <a-form layout="vertical" >
                    <v-container>
                      <v-row>
                        <v-col
                          cols="12"
                          md="6"
                        >
                          <a-form-item label="Symptoms">
                            <a-select
                              v-model:value="selectedSymptoms"
                              :options="symptomsOptions"
                              mode="multiple"
                              placeholder="Symptoms"
                              style="width: 100%"
                            ></a-select>
                          </a-form-item>
                          <a-form-item label="Duration">
                            <a-input v-model:value="duration" />
                          </a-form-item>
                          <a-form-item label="Symptoms Note">
                            <a-textarea v-model:value="symptomsNote" placeholder="Symptoms Note" :rows="4" />
                          </a-form-item>
                          <a-form-item label="Progression">
                            <a-input v-model:value="progrission" />
                          </a-form-item>
                        </v-col>
                        <v-col
                          cols="12"
                          md="6"
                        >
                          <a-form-item label="Symptoms">
                            <a-select
                              v-model:value="selectedDiagnoses"
                              :options="diagnosesOptions"
                              mode="multiple"
                              placeholder="Diagnosis"
                              style="width: 100%"
                            ></a-select>
                          </a-form-item>
                          <a-form-item label="Differential Diagnosis">
                            <a-input v-model:value="differentialDiagnosis" />
                          </a-form-item>
                          <a-form-item label="Diagnosis Note">
                            <a-textarea v-model:value="diagnosisNote" placeholder="Diagnosis Note" :rows="4" />
                          </a-form-item>
                        </v-col>
                      </v-row>
                    </v-container>
                  </a-form>
                </v-sheet>
              </v-stepper-window-item>
            </v-stepper-window>

            <v-stepper-actions
              @click:next="next"
              @click:prev="prev"
            ></v-stepper-actions>
          </template>
        </v-stepper>
      </div>
    </div>
  </div>
</template>

<script>
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

import Card from 'primevue/card';
import Divider from 'primevue/divider';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import { ref } from 'vue';

import soundImage from '@/assets/img/sound.png';
import lungsImage from '@/assets/img/lungs.png';
import celsiusImage from '@/assets/img/celsius.png';

export default {
  components: {
    Card, Divider, VSlideGroup, VSlideGroupItem, DataTable, Column, VBtn,
    VProgressCircular, VProgressLinear, VChip, VEmptyState, VContainer,
    VRow, VCol, VSelect, VDivider, VStepper, VStepperHeader, VStepperItem,
    VStepperActions, VStepperWindow, VStepperWindowItem, VSheet,
  },
  data() {
    return {
      currentBreakpoint:'',
      currentFormStep: 0,
      vitalSigns: [{
        hr: "110",
        bt: "35",
        rr: "12",
        sys: "150",
        dia: "95",
        date: '20/04/2024',
      },
      {
        hr: "140",
        bt: "37",
        rr: "15",
        sys: "120",
        dia: "80",
        date: '24/04/2024',
      }],
      currentVS: {
        hr: "-",
        bt: "-",
        rr: "-",
        sys: "-",
        dia: "-",
        date: '-',
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
      riskFactors: [{name: 'Smoking', value: 4}, {name: 'Chemical Contact', value: 1}],
      allergies: [{name: 'Peanut', value: 4}, {name: 'Local Anesthetics', value: 2}],
      medications:[
        {item: 'Aspirin', dose: 'once a Day', weight: '80 mg', status: 'Active', duraion: '1 Week'},
        {item: 'Panadol', dose: '3 Times a Day', weight: '50 mg', status: 'Inactive', duraion: '3 Days'},
      ],
      pastEncounters: [{
        date: '04/03/2024',
        type: 'Session',
        practitioner: 'Dr Ali Ahmed',
        reason: 'Chest Pain',
      },
      {
        date: '15/03/2024',
        type: 'Follow-up',
        practitioner: 'Dr S.Hassan Adnan',
        reason: 'Medicaion Refill',
      }],
      attachments: [
        {item: 'Chest X-Ray', date: '02/03/2024', icon: 'pi pi-file-pdf'},
        {item: 'Ecg Test Report', date: '08/03/2024', icon: 'pi pi-file-word'},
        {item: 'Chest X-Ray', date: '12/03/2024', icon: 'pi pi-file-pdf'},
      ],
      surgicalHistory: [],
      familyHistory: [{item: 'Cancer', relative: 'Mother',},{item: 'Diabetes', relative: 'Father',},],
      symptomsOptions: ['Abdominal pain', 'Anal Pain', 'Ankle Pain', 'Anosmia', 'Arm Pain', 'Back Pain', 'Blood Clots', 'Chest Pain', 'Cough'].map(option => ({
        label: option,
        value: option
      })),
      selectedSymptoms: ref([]),
      diagnosesOptions: ['Acne', 'Anosmia', 'Asthma', 'Cancer', 'Cataract', 'Cavities', 'Colitis'].map(option => ({
        label: option,
        value: option
      })),
      selectedDiagnoses: ref([]),
      duration: '',
      differentialDiagnosis:'',
      symptomsNote:'',
      diagnosisNote:'',
      progrission:'',
      lungsImage:lungsImage,
      celsiusImage:celsiusImage,
      soundImage:soundImage,
      formSteps:['Encounter Impression', 'Examination', 'Medical Coding', 'Prescriptions', 'Investigation', 'Clinical Procedure'],
    };
  },
  mounted() {
    this.currentVS = this.vitalSigns[this.vitalSigns.length -1];

    this.updateBreakpoint();
    window.addEventListener('resize', this.updateBreakpoint);
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.updateBreakpoint);
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
    updateBreakpoint() {
      const width = window.innerWidth;
      if (width < 576) {
        this.currentBreakpoint = 'sm';
      } else if (width < 768) {
        this.currentBreakpoint = 'md';
      } else if (width < 992) {
        this.currentBreakpoint = 'lg';
      } else if (width < 1280) {
        this.currentBreakpoint = 'xl';
      } else {
        this.currentBreakpoint = 'xxl';
      }
    },
  }
};
</script>

<style>

#patient-bar .p-card-content{
  display: flex;
  overflow: hidden;
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