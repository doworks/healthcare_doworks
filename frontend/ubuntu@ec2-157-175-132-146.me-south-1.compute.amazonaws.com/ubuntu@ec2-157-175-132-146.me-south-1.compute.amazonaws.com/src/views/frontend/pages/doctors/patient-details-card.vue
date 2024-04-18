<template>
    <Card class="h-100 " ref="cardRef">
        <template #title>Next Patient Details</template>
        <template #content>
            <div class="box-body">
                <div class="table-image appoint-doctor d-flex">
                <img width="28" height="28" class="rounded-circle avatar-xl align-self-center" :src="patient.image" alt=""/>
                <div style="padding: 10px 15px; align-self: center;">
                    <h2 style="font-size: 18px; font-weight: 500; margin-bottom: 0">{{ patient.patient_name }}</h2>
                    <span style="color: rgba(51, 52, 72, 0.5); font-size: 18px; font-weight: 500">{{ patient.appointment_type }}</span>
                </div>
                </div>
                <div class="row">						
                    <div class="col-12">
                        <div class="row py-5">							
                            <div class="col-4">							  
                                <div>
                                    <h5 class="mb-0"><strong>D.O.B</strong></h5>
                                    <p class="mb-0"><small>{{patient.patientDetails.date_of_birth}}</small></p> 
                                </div>
                            </div>							
                            <div class="col-4">							  
                                <div>
                                    <h5 class=" mb-0"><strong>Gender</strong></h5>
                                    <p class="mb-0"><small>{{patient.patientDetails.gender}}</small></p> 
                                </div>
                            </div>							
                            <div class="col-4">							  
                                <div>
                                    <h5 class="mb-0"><strong>Last Visit</strong></h5>
                                    <p class="mb-0"><small>2024-01-16</small></p> 
                                </div>
                            </div>
                        </div>
                        <div class="row py-3" style="border-top: 1px solid #f3f6f9;">							
                            <div class="col-4">							  
                                <img class="img-fluid float-start det-img" src="@/assets/img/weight.png" alt="">
                                <div>
                                    <h5 class="mb-0"><strong>Weight</strong></h5>
                                    <p class="mb-0"><small>{{patient.patientDetails.weight || '--'}}</small></p> 
                                </div>
                            </div>							
                            <div class="col-4" style="border-left: 1px solid #f3f6f9; border-right: 1px solid #f3f6f9">							  
                                <img class="img-fluid float-start det-img" src="@/assets/img/human.png" alt="">
                                <div>
                                    <h5 class=" mb-0"><strong>Height</strong></h5>
                                    <p class="mb-0"><small>{{patient.patientDetails.height || '--'}}</small></p> 
                                </div>
                            </div>							
                            <div class="col-4">							  
                                <img class="img-fluid float-start det-img" src="@/assets/img/bmi.png" alt="">
                                <div>
                                    <h5 class="mb-0"><strong>BMI</strong></h5>
                                    <p class="mb-0"><small>30.34</small></p> 
                                </div>
                            </div>
                        </div>
                        <v-row align="center" justify="center" class="mt-5">
                            <v-col cols="auto">
                                <v-btn class="text-blue" prepend-icon="pi pi-phone" elevation="2">{{patient.mobile}}</v-btn>
                            </v-col>
                            <v-col cols="auto">
                                <v-btn elevation="2" class="bg-green-accent-2">Encounter</v-btn>
                            </v-col>
                        </v-row>
                    </div>
                </div>
            </div>
        </template>
    </Card>
</template>

<script>
import moment from "moment";
import Card from 'primevue/card';
import Button from 'primevue/button';
import Tag from 'primevue/tag';
import {VBtn} from 'vuetify/components/VBtn'
import {VCol, VRow} from 'vuetify/components/VGrid'


export default {
    components: {
        Card,
        Button,
        VBtn,
        VCol,
        VRow,
        Tag
    },
    props: {
        patient: {
            default: {
                "name": "HLC-APP-2024-00001",
                "appointment_type": "General",
                "patient_name": "Sayed Mohamed Adnan",
                "mobile": "1234567890",
                "practitioner_name": "Sayed Hassan",
                "cpr": 123576342,
                "department": "Neurology",
                "status": "Scheduled",
                "invoiced": 100,
                "paid_amount": 0,
                "duration": 20,
                "visit_status": "Scheduled",
                "image": "https://randomuser.me/api/portraits/men/1.jpg",
                "practitioner_image": "https://randomuser.me/api/portraits/men/30.jpg",
                "appointment_time": "09:45:00",
                "appointment_date": "2024-02-21",
                "patientDetails": {
                    "date_of_birth": "2024-02-21",
                    "gender": "Male",
                    "weight": "65 Kg",
                    "height": "180 cm",
                }
            },
        },
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