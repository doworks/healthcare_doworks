import { createRouter, createWebHistory } from "vue-router";

import PatientEncounter from '@/views/frontend/pages/patients/dashboard/patient-encounter.vue';
import PatientEncounterList from '@/views/frontend/pages/patients/dashboard/patient-encounter-list.vue';
import PatientList from '@/views/frontend/pages/patients/patient-list.vue';
import Patient from '@/views/frontend/pages/patients/patient.vue';
import DoctorDashBoard from '@/views/frontend/pages/doctors/doctor-dashboard.vue';
import NurseDashBoard from '@/views/frontend/pages/nurse/nurse-dashboard.vue';
import PharmacyDashBoard from '@/views/frontend/pages/pharmacy/pharmacy-dashboard.vue';
import Appointments from '@/views/frontend/pages/doctors/doctor-appointment.vue';

const routes = [
  {
    path: "/",
    name: "Home",
    beforeEnter: (to, from, next) => {
      next('/appointments');
    },
  },
  {
    path: '/patient-encounter/',
    name: 'patient-encounter-list',
    component: PatientEncounterList
  },
  {
    path: '/patient-encounter/:encounterId',
    name: 'patient-encounter',
    component: PatientEncounter
  },
  {
    path: '/patient/',
    name: 'patient-list',
    component: PatientList
  },
  {
    path: '/patient/:patientId',
    name: 'patient',
    component: Patient
  },
  {
    path: '/practitioner-dashboard',
    name: 'practitioner-dashboard',
    component: DoctorDashBoard
  },
  {
    path: '/nurse-dashboard',
    name: 'nurse-dashboard',
    component: NurseDashBoard
  },
  {
    path: '/pharmacy-dashboard',
    name: 'pharmacy-dashboard',
    component: PharmacyDashBoard
  },
  {
    path: '/appointments',
    name: 'appointments',
    component: Appointments 
  },
];

const router = createRouter({
  base: "/frontend/",
  history: createWebHistory('/frontend/'),
  routes,
});

router.beforeEach((to, from, next) => {
  // Scroll to the top of the page
  window.scrollTo({ top: 0, behavior: 'smooth' });

  // Continue with the navigation
  next();
});

export default router;
