<template>
    <Card class="h-100 " ref="cardRef">
        <template #title>Next Patient Details</template>
        <template #content>
            <div class="box-body">
                <div class="table-image appoint-doctor d-flex" v-if="patient">
                <img 
                width="28" 
                height="28" 
                class="rounded-circle avatar-xl align-self-center" 
                alt=""
                :src="patient.patient_details.image ? patient.patient_details.image :patient.patient_details.gender === 'Male' ? maleImage : femaleImage" 
                />
                <div style="padding: 10px 15px; align-self: center;">
                    <h2 style="font-size: 18px; font-weight: 500; margin-bottom: 0">{{ patient.patient_name }}</h2>
                    <span style="color: rgba(51, 52, 72, 0.5); font-size: 18px; font-weight: 500">{{ patient.service_unit }}</span>
                </div>
                </div>
                <div class="row">						
                    <div class="col-12">
                        <div class="row py-5">							
                            <div class="col-4">							  
                                <div>
                                    <h5 class="mb-0"><strong>D.O.B</strong></h5>
                                    <p class="mb-0"><small>{{patient.patient_details.date_of_birth}}</small></p> 
                                </div>
                            </div>							
                            <div class="col-4">							  
                                <div>
                                    <h5 class=" mb-0"><strong>Gender</strong></h5>
                                    <p class="mb-0"><small>{{patient.patient_details.gender}}</small></p> 
                                </div>
                            </div>							
                            <div class="col-4">							  
                                <div>
                                    <h5 class="mb-0"><strong>Last Visit</strong></h5>
                                    <p class="mb-0"><small>{{ patient.patient_details.last_visit }}</small></p> 
                                </div>
                            </div>
                        </div>
                        <div class="row py-3" style="border-top: 1px solid #f3f6f9;">							
                            <div class="col-4">							  
                                <img class="img-fluid float-start det-img" src="@/assets/img/weight.png" alt="">
                                <div>
                                    <h5 class="mb-0"><strong>Weight</strong></h5>
                                    <p class="mb-0"><small>{{patient.patient_details.weight || '--'}}</small></p> 
                                </div>
                            </div>							
                            <div class="col-4" style="border-left: 1px solid #f3f6f9; border-right: 1px solid #f3f6f9">							  
                                <img class="img-fluid float-start det-img" src="@/assets/img/human.png" alt="">
                                <div>
                                    <h5 class=" mb-0"><strong>Height</strong></h5>
                                    <p class="mb-0"><small>{{patient.patient_details.height || '--'}}</small></p> 
                                </div>
                            </div>							
                            <div class="col-4">							  
                                <img class="img-fluid float-start det-img" src="@/assets/img/bmi.png" alt="">
                                <div>
                                    <h5 class="mb-0"><strong>BMI</strong></h5>
                                    <p class="mb-0"><small>{{patient.patient_details.bmi || '--'}}</small></p> 
                                    <p class="mb-0"><small><strong>{{patient.patient_details.nutrition_note || '--'}}</strong></small></p> 
                                </div>
                            </div>
                        </div>
                        <v-row align="center" justify="center" class="mt-5">
                            <v-col cols="auto">
                                <v-btn class="text-blue" prepend-icon="pi pi-phone" elevation="2">{{patient.patient_details.mobile}}</v-btn>
                            </v-col>
                            <v-col cols="auto">
                                <v-btn 
                                elevation="2" 
                                class="bg-green-accent-2" 
                                :to="{ name: 'patient-encounter', params: { appointmentId: patient.appointment_id } }"
                                >
                                    Encounter
                                </v-btn>
                            </v-col>
                        </v-row>
                    </div>
                </div>
            </div>
        </template>
    </Card>
</template>

<script>
import {VCol, VRow} from 'vuetify/components/VGrid'

import maleImage from '@/assets/img/male.png';
import femaleImage from '@/assets/img/female.png';

export default {
    components: {
        VCol, VRow,
    },
    data: {
        maleImage:maleImage,
		femaleImage:femaleImage,
    },
    props: {
        patient: {
            default: null,
        },
    },
    mounted() {
        console.log(this.patient)
        window.addEventListener('resize', this.handleResize);
    },
    beforeUnmount() {
        window.removeEventListener('resize', this.handleResize);
    },
    methods: {
        handleResize() {
            // Handle the resize event here
            // For example, call a function
            this.updateOnResize();
        },
        updateOnResize() {
            // Your logic to update on resize
            this.$emit('cardRendered', this.$refs.cardRef.$el.querySelector('.p-card-body').offsetHeight);
        }
    }
};
</script>

<style scoped>
.det-img{
  margin-top: 10px;
  margin-right: 10px;
  width: 30px;
}
</style>