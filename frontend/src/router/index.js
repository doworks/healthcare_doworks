import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import authRoutes from './auth';


import PatientEncounter from '@/views/frontend/pages/patients/dashboard/patient-encounter.vue';
import PatientEncounterList from '@/views/frontend/pages/patients/dashboard/patient-encounter-list.vue';
import PatientList from '@/views/frontend/pages/patients/patient-list.vue';
import Patient from '@/views/frontend/pages/patients/patient.vue';
import DoctorDashBoard from '@/views/frontend/pages/doctors/doctor-dashboard.vue';
import NurseDashBoard from '@/views/frontend/pages/nurse/nurse-dashboard.vue';
import Appointments from '@/views/frontend/pages/doctors/doctor-appointment.vue';

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
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
    path: '/doctor-dashboard',
    name: 'doctor-dashboard',
    component: DoctorDashBoard
  },
  {
    path: '/nurse-dashboard',
    name: 'nurse-dashboard',
    component: NurseDashBoard
  },
  {
    path: '/appointments',
    name: 'appointments',
    component: Appointments 
  },
  ...authRoutes,
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
