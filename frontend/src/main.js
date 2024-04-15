import { createApp, reactive } from "vue";
import App from "./App.vue";

import router from './router';
import resourceManager from "../../../doppio/libs/resourceManager";
import call from "../../../doppio/libs/controllers/call";
import socket from "../../../doppio/libs/controllers/socket";
import Auth from "../../../doppio/libs/controllers/auth";

            				// My App //
// import primevue/ vutify
import PrimeVue from 'primevue/config';
import { createVuetify } from 'vuetify'

// Other UI libraries
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/reset.css';
import VueFeather from 'vue-feather';

// Import styles
import 'normalize.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import '@fortawesome/fontawesome-free/css/fontawesome.min.css';
import '@fortawesome/fontawesome-free/css/all.min.css';

import 'vuetify/styles'
import 'primevue/resources/themes/aura-light-blue/theme.css'
import 'primeicons/primeicons.css' 

import '@mdi/font/css/materialdesignicons.css'
import { fa } from 'vuetify/iconsets/fa'
import { aliases, mdi } from 'vuetify/iconsets/mdi-svg'

//Breadcrumb
import DoctorsSidebar from '@/views/frontend/layouts/doctorsidebar.vue'

//pages
import Footer from '@/views/frontend/layouts/footer.vue'
import IndexFooter from '@/views/frontend/pages/home/footer.vue'

//Patient Pages
import PatientFooter from '@/views/frontend/pages/patients/patientfooter.vue'
import patientappointment from '@/views/frontend/pages/patients/dashboard/patientappointment.vue'

import DoctorSidebar from '@/views/frontend/layouts/doctorsidebar.vue'
import Dappointment from '@/views/frontend/pages/doctors/patient-profile/dappointment.vue'
import AppointmentTab from '@/views/frontend/pages/doctors/doctor-appointment-tab.vue'
						  // My App End //


const app = createApp(App);
const auth = reactive(new Auth());

// My App (Again)
app.component('doctors-sidebar',DoctorsSidebar)
app.component('footerindex',Footer)
app.component('indexfooter',IndexFooter)
app.component('patientfooter',PatientFooter)
app.component('patientappointment',patientappointment)
app.component('doctorsidebar',DoctorSidebar)
app.component('dappointment',Dappointment)
app.component('appointmenttab',AppointmentTab)
// Use other UI libraries and plugins
app.use(Antd);

app.component(VueFeather.name, VueFeather);
const vuetify = createVuetify({
    icons: {
        defaultSet: 'fa',
        aliases,
        sets: {
          fa,
		  mdi,
        },
    },
	$reset: false
})
app.use(PrimeVue).use(vuetify);
// End Of My App (Again)

// Plugins
app.use(router);
app.use(resourceManager);

// Global Properties,
// components can inject this
app.provide("$auth", auth);
app.provide("$call", call);
app.provide("$socket", socket);


// Configure route gaurds
router.beforeEach(async (to, from, next) => {
	if (to.matched.some((record) => !record.meta.isLoginPage)) {
		// this route requires auth, check if logged in
		// if not, redirect to login page.
		if (!auth.isLoggedIn) {
			window.location.href = '/login';
		} else {
			next();
		}
	} else {
		if (auth.isLoggedIn) {
			next({ name: 'Home' });
		} else {
			next();
		}
	}
});

// Handle Global Resources
let resources = reactive({
	practitioners: [],
	patients: [],
	user: {},
	appointmentTypes: [],
});
call('frappe.auth.get_logged_user').then(user => {
	resources.user.name = user
	call('frappe.client.get', {doctype:'User', name: user}).then(response => {
		resources.user.image = response.user_image
	})
})
call('frappe.client.get_list', {doctype: 'Healthcare Practitioner', fields: ['practitioner_name', 'image', 'department', 'name']})
	.then(response => {
		if(response)
			resources.practitioners = response
	})
	.catch(error => {
		console.error('Error fetching records:', error);
	});
call('frappe.client.get_list', {doctype: 'Patient', fields: ['sex', 'patient_name', 'name', 'custom_cpr', 'dob', 'mobile']})
	.then(response => {
		if(response)
			resources.patients = response
	})
	.catch(error => {
		console.error('Error fetching records:', error);
	});
call('frappe.client.get_list', {doctype: 'Appointment Type', fields: ['appointment_type', 'allow_booking_for']})
	.then(response => {
		if(response)
			resources.appointmentTypes = response
	})
	.catch(error => {
		console.error('Error fetching records:', error);
	});
app.config.globalProperties.$resources = resources;

app.mount("#app");
