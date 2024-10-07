<template>
    <Card class="h-100 " ref="cardRef">
        <template #title>Next Patient Details</template>
        <template #content>
            <div class="box-body">
                <div class="table-image appoint-doctor d-flex" v-if="patient">
                    <a 
                    :href="$router.resolve({ name: 'patient', params: { patientId: data.patient_details.id } }).href" 
                    target="_blank" 
                    style="color: unset; text-decoration: unset"
                    >
                        <v-avatar size="large" class="self-center">
                            <img
                            class="w-20 h-20 rounded-circle"
                            :src="patient.patient_details.image ? patient.patient_details.image :patient.patient_details.gender === 'Female' ? femaleImage :maleImage"
                            />
                            <!-- <span v-if="!data.patient_details.image" class="text-h6">{{ getInitials(data.patient_name) }}</span> -->
                        </v-avatar>
                        <div style="padding: 10px 15px; align-self: center;">
                            <h4 style="margin-bottom: 0">{{ patient.patient_name }}</h4>
                            <span style="color: rgba(51, 52, 72, 0.5)">{{ patient.service_unit }}</span>
                        </div>
                    </a>
                </div>
                <div class="row">						
                    <div class="col-12">
                        <div class="row py-5">							
                            <div class="col-4">							  
                                <div>
                                    <h6 class="mb-0"><strong>D.O.B</strong></h6>
                                    <p class="mb-0"><small>{{patient.patient_details.date_of_birth}}</small></p> 
                                </div>
                            </div>							
                            <div class="col-4">							  
                                <div>
                                    <h6 class=" mb-0"><strong>Gender</strong></h6>
                                    <p class="mb-0"><small>{{patient.patient_details.gender}}</small></p> 
                                </div>
                            </div>							
                            <div class="col-4">							  
                                <div>
                                    <h6 class="mb-0"><strong>Last Visit</strong></h6>
                                    <p class="mb-0"><small>{{ patient.patient_details.last_visit }}</small></p> 
                                </div>
                            </div>
                        </div>
                        <div class="row py-3" style="border-top: 1px solid #f3f6f9;">							
                            <div class="col-4">							  
                                <img class="img-fluid float-start det-img" src="@/assets/img/weight.png" alt="">
                                <div>
                                    <h6 class="mb-0"><strong>Weight</strong></h6>
                                    <p class="mb-0"><small>{{patient.patient_details.weight || '--'}}</small></p> 
                                </div>
                            </div>							
                            <div class="col-4" style="border-left: 1px solid #f3f6f9; border-right: 1px solid #f3f6f9">							  
                                <img class="img-fluid float-start det-img" src="@/assets/img/human.png" alt="">
                                <div>
                                    <h6 class=" mb-0"><strong>Height</strong></h6>
                                    <p class="mb-0"><small>{{patient.patient_details.height || '--'}}</small></p> 
                                </div>
                            </div>							
                            <div class="col-4">							  
                                <img class="img-fluid float-start det-img" src="@/assets/img/bmi.png" alt="">
                                <div>
                                    <h6 class="mb-0"><strong>BMI</strong></h6>
                                    <p class="mb-0"><small>{{patient.patient_details.bmi || '--'}}</small></p> 
                                    <p class="mb-0"><small><strong>{{patient.patient_details.nutrition_note || '--'}}</strong></small></p> 
                                </div>
                            </div>
                        </div>
                        <v-row align="center" justify="center" class="mt-5">
                            <v-col cols="auto" v-if="patient.patient_details.mobile">
                                <v-btn class="text-blue" prepend-icon="pi pi-phone" elevation="2">{{patient.patient_details.mobile}}</v-btn>
                            </v-col>
                            <v-col cols="auto">
                                <v-btn 
                                elevation="2" 
                                class="bg-green-accent-2" 
                                @click="goToEncounter"
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
import { VAvatar } from 'vuetify/components';

import maleImage from '@/assets/img/male.png';
import femaleImage from '@/assets/img/female.png';

export default {
    inject: ['$call'],
    components: {
        VCol, VRow, VAvatar,
    },
    props: {
        patient: {
            default: null,
        },
    },
    data() {
        return {
            maleImage:maleImage,
            femaleImage:femaleImage,
        }
    },
    mounted() {
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
        },
        goToEncounter() {
			this.$call('healthcare_doworks.api.methods.patient_encounter_name', {appointment_id: this.patient.appointment_id})
			.then(response => {
				const appointmentId = this.patient.appointment_id;
				this.$router.push({ name: 'patient-encounter', params: { encounterId: response } });
			}).catch(error => {
				console.error(error);
			});
		},
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