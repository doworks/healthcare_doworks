import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import authRoutes from './auth';


import PatientEncounter from '@/views/frontend/pages/patients/dashboard/patient-encounter.vue';
import DoctorDashBoard from '@/views/frontend/pages/doctors/doctor-dashboard.vue';
import Appointments from '@/views/frontend/pages/doctors/doctor-appointment.vue';

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: '/patient-encounter/:appointmentId?',
    name: 'patient-encounter',
    component: PatientEncounter
  },
  {
    path: '/doctor-dashboard',
    name: 'doctor-dashboard',
    component: DoctorDashBoard
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
