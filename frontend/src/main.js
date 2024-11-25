import { createApp, reactive } from "vue";
import App from "./App.vue";

import router from './router';
import call from "./utils/call";
import { initSocket } from './utils/socket'
import Auth from "./utils/auth";

import io from 'socket.io-client'; 

// Import Frappe UI
import { FrappeUI, setConfig, frappeRequest, resourcesPlugin } from 'frappe-ui'
            				// My App //
// import primevue/ vutify
import PrimeVue from 'primevue/config';
import ConfirmationService from 'primevue/confirmationservice';
import ToastService from 'primevue/toastservice';
import Aura from '@primevue/themes/aura';
import { createVuetify } from 'vuetify';
import {
	VDivider, VDialog, VBtn, VAlert, VOverlay, VProgressCircular, VBadge, VCard, VCardTitle, 
	VCardText, VCardActions, VWindow, VWindowItem, VTab, VTabs, VContainer, VRow, VCol,
} from 'vuetify/components'

// Other UI libraries
import Antd from 'ant-design-vue';
import 'ant-design-vue/dist/reset.css';
import VueFeather from 'vue-feather';

// Import styles
// import 'normalize.css';
import 'vuetify/styles'
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap-vue/dist/bootstrap-vue.css';
import '@fortawesome/fontawesome-free/css/fontawesome.min.css';
import '@fortawesome/fontawesome-free/css/all.min.css';

// import 'primevue/resources/themes/aura-light-blue/theme.css'
import 'primeicons/primeicons.css' 

import '@mdi/font/css/materialdesignicons.css'
import { fa } from 'vuetify/iconsets/fa'
import { aliases, mdi } from 'vuetify/iconsets/mdi-svg'

//pages

//Patient Pages

import patientappointment from '@/views/frontend/pages/patients/dashboard/patientappointment.vue'
import DoctorSidebar from '@/views/frontend/layouts/doctorsidebar.vue'

// Link Field
import Link from '@/components/controls/Link.vue'

//Dialogs
import PatientAppointmentDialog from '@/components/dialogs/patientAppointment.vue'
import VitalSignsDialog from '@/components/dialogs/vitalSigns.vue'
import VitalSignsListDialog from '@/components/dialogs/vitalSigns-list.vue'
import MedicationRequestDialog from '@/components/dialogs/medicationRequest.vue'
import LabTestDialog from '@/components/dialogs/labTest.vue'
import AddAttachmentDialog from '@/components/dialogs/addAttachment.vue'
import PatientEncounterDialog from '@/components/dialogs/patientEncounter.vue'
import ProcedureDialog from '@/components/dialogs/procedure.vue'
import ServiceRequestDialog from '@/components/dialogs/serviceRequest.vue'
import PatientMedicalHistoryDialog from '@/components/dialogs/patientMedicalHistory.vue'
import PatientQuickDialog from '@/components/dialogs/patient-quick.vue'
import AppointmentNoteDialog from '@/components/dialogs/appointmentNote.vue'
import AppointmentInvoiceDialog from '@/components/dialogs/appointmentInvoice.vue'
import ChecklistFormDialog from '@/components/dialogs/checklistForm.vue'
import ChecklistFormListDialog from '@/components/dialogs/checklistForm-list.vue'
import BiocomDialog from '@/components/dialogs/biocom.vue'
						  // My App End //


const app = createApp(App);
const auth = reactive(new Auth());

// My App (Again)
app.component('LinkField',Link)

app.component('patientappointment',patientappointment)
app.component('doctorsidebar',DoctorSidebar)

// Dialogs
// app.component('PatientAppointmentDialog', () => import('@/components/dialogs/patientAppointment.vue'));
// app.component('vitalSignsListDialog', () => import('@/components/dialogs/vitalSigns-list.vue'));
// app.component('VitalSignsDialog', () => import('@/components/dialogs/vitalSigns.vue'));
// app.component('medicationRequestDialog', () => import('@/components/dialogs/medicationRequest.vue'));
// app.component('LabTestDialog', () => import('@/components/dialogs/labTest.vue'));
// app.component('addAttachmentDialog', () => import('@/components/dialogs/addAttachment.vue'));
// app.component('patientEncounterDialog', () => import('@/components/dialogs/patientEncounter.vue'));
// app.component('ProcedureDialog', () => import('@/components/dialogs/procedure.vue'));
// app.component('ServiceRequestDialog', () => import('@/components/dialogs/serviceRequest.vue'));
// app.component('PatientMedicalHistoryDialog', () => import('@/components/dialogs/patientMedicalHistory.vue'));
app.component('patientAppointmentDialog',PatientAppointmentDialog)
app.component('vitalSignsListDialog',VitalSignsListDialog)
app.component('vitalSignsDialog',VitalSignsDialog)
app.component('medicationRequestDialog',MedicationRequestDialog)
app.component('labTestDialog',LabTestDialog)
app.component('addAttachmentDialog',AddAttachmentDialog)
app.component('patientEncounterDialog',PatientEncounterDialog)
app.component('procedureDialog',ProcedureDialog)
app.component('serviceRequestDialog',ServiceRequestDialog)
app.component('patientMedicalHistoryDialog',PatientMedicalHistoryDialog)
app.component('patientQuickDialog',PatientQuickDialog)
app.component('appointmentNoteDialog',AppointmentNoteDialog)
app.component('appointmentInvoiceDialog',AppointmentInvoiceDialog)
app.component('checklistFormDialog',ChecklistFormDialog)
app.component('checklistFormListDialog',ChecklistFormListDialog)
app.component('biocomDialog',BiocomDialog)
// Use other UI libraries and plugins
app.use(Antd);

app.component(VueFeather.name, VueFeather);
const vuetify = createVuetify({
	components: {
		VDivider, VDialog, VBtn, VAlert, VOverlay, VProgressCircular, VBadge, VCard, VCardTitle, VCardText, 
		VCardActions, VWindow, VWindowItem, VTab, VTabs, VContainer, VRow, VCol,
	},
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
app.use(PrimeVue, {
    // Default theme configuration
    theme: {
        preset: Aura,
        options: {
            prefix: 'p',
            darkModeSelector: 'system',
            // cssLayer: false
        }
    }
}).use(ConfirmationService).use(ToastService);
app.use(vuetify);
// End Of My App (Again)

// Plugins
app.use(router);
setConfig('resourceFetcher', frappeRequest)
app.use(FrappeUI)

// Configure route gaurds
router.beforeEach(async (to, from, next) => {
    try {
        if (!auth.isLoggedIn && !to.meta.isLoginPage) {
            window.location.href = `${window.location.origin}/login`;
            return;
        } else if (auth.isLoggedIn && to.meta.isLoginPage) {
            return next({ name: 'Home' });
        }
        next();
    } catch (error) {
        console.error('Error in route guard:', error);
        next('/error'); // or handle error appropriately
    }
});

// Handle Global Resources
let resources = reactive({user: {}, siteName: '', colorCache: {}});

// Card Reader Socket
// let cardReader = io('http://localhost:5000', {reconnectionAttempts: 3})
// app.provide("$cardReader", cardReader);

// Global Properties,
// components can inject this
app.provide("$auth", auth);
app.provide("$call", call);
call('healthcare_doworks.api.methods.fetch_resources').then(response => {
	if(response){
		for (let key in resources) {
			resources[key] = response[key]
		}
		app.provide("$socket", initSocket(response.siteName));
		app.mount("#app");
	}
}).catch(error => {
	console.error('Error fetching records:', error);
});

app.config.globalProperties.$myresources = resources;