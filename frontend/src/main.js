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
import 'vuetify/styles'
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import '@fortawesome/fontawesome-free/css/fontawesome.min.css';
import '@fortawesome/fontawesome-free/css/all.min.css';

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
import Attachments from '@/components/attachments.vue'

//Dialogs
import PatientAppointmentDialog from '@/components/dialogs/patientAppointment.vue'
import VitalSignsDialog from '@/components/dialogs/vitalSigns.vue'
import MedicationRequestDialog from '@/components/dialogs/medicationRequest.vue'
import LabTestDialog from '@/components/dialogs/labTest.vue'
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
app.component('attachments',Attachments)
app.component('appointmenttab',AppointmentTab)
app.component('patientAppointmentDialog',PatientAppointmentDialog)
app.component('vitalSignsDialog',VitalSignsDialog)
app.component('medicationRequestDialog',MedicationRequestDialog)
app.component('labTestDialog',LabTestDialog)
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
	display: {
		mobileBreakpoint: 'sm',
		thresholds: {
			xs: 0,
			sm: 576,
			md: 768,
			lg: 992,
			xl: 1200,
  			xxl: 1400
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
	user: {},
	practitioners: [],
	patients: [],
	appointmentTypes: [],
	departments: [],
	serviceUnits: [],
	complaints: [],
	diagnosis: [],
	medications: [],
	items: [],
	dosageForms: [],
	prescriptionDosages: [],
	prescriptionDurations: [],
	labTestTemplates: [],
});

call('healthcare_doworks.api.methods.fetch_resources').then(response => {
	if(response){
		for (let key in resources) {
			resources[key] = response[key]
		}
	}
}).catch(error => {
	console.error('Error fetching records:', error);
});

app.config.globalProperties.$resources = resources;

app.mount("#app");
