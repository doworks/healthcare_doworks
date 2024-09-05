<template>
	<!-- <div>
		<button v-if="$auth.isLoggedIn" @click="$auth.logout()">Logout</button>
		<router-view />
	</div> -->
	<div id="app">
		<v-layout style="min-height: 100vh" v-if="$auth.isLoggedIn">
			<doctorsidebar/>
			<v-main class="pt-0 pt-sm-2 bg-gradient ps-20 overflow-hidden" id="body-main">
				<router-view />
			</v-main>
		</v-layout>
	</div>
</template>


<script>
import '@/assets/css/feather.css';
// import '@/assets/css/custom.css';
import 'frappe-ui/src/style.css';
import '@/assets/css/prime.css';
import { VLayout } from 'vuetify/components/VLayout'
import { VMain } from 'vuetify/components/VMain'
export default {
	inject: ['$auth'],
	components:{
		VLayout,
		VMain,
	},
	resources: {
		departments() { return { 
			type: 'list', 
			doctype: 'Medical Department', 
			fields: ['name', 'department'], 
			auto: true, 
			orderBy: 'department',
			pageLength: undefined,
			cache: 'departments'
		}},
		practitioners() { return { 
			type: 'list', 
			doctype: 'Healthcare Practitioner', 
			fields: ['practitioner_name', 'image', 'department', 'name'], 
			filter: {status: 'Active'},
			auto: true, 
			orderBy: 'practitioner_name',
			pageLength: undefined,
			cache: 'practitioners',
		}},
		serviceUnits() { return { 
			type: 'list', 
			doctype: 'Healthcare Service Unit', 
			fields:['name'], 
			filters:{'allow_appointments': 1}, 
			auto: true, 
			orderBy: 'name',
			pageLength: undefined,
			cache: 'serviceUnits',
		}},
		patients() { return { 
			type: 'list', 
			doctype: 'Patient', 
			fields: ['sex', 'patient_name', 'name', 'custom_cpr', 'dob', 'mobile', 'email', 'blood_group', 'inpatient_record', 'inpatient_status'], 
			auto: true, 
			orderBy: 'patient_name',
			pageLength: undefined,
			cache: 'patients',
		}},
		medications() { return { 
			type: 'list', 
			doctype: 'Medication', 
			fields: ['name'], 
			auto: true, 
			orderBy: 'name', 
			pageLength: undefined,
			cache: 'medications',
		}},
        items() { return { 
			type: 'list', 
			doctype: 'Item', 
			fields: ['name', 'item_name'], 
			auto: true, 
			orderBy: 'item_name', 
			pageLength: undefined,
			cache: 'items',
		}},
		complaints() { return { 
			type: 'list', 
			doctype: 'Complaint', 
			fields: ['name'], 
			auto: true,
			orderBy: 'name',
			pageLength: undefined,
			cache: 'complaints',
			// transform data before setting it
			transform(data) {
				for (let d of data) {
				d.label = d.name
				d.value = d.name
				}
				return data
			},
		}},
		diagnosis() { return { 
			type: 'list', 
			doctype: 'Diagnosis', 
			fields: ['name'], 
			auto: true,
			orderBy: 'name',
			pageLength: undefined,
			cache: 'diagnosis',
			// transform data before setting it
			transform(data) {
				for (let d of data) {
				d.label = d.name
				d.value = d.name
				}
				return data
			},
		}},
	},
	setup() {
		// loadStyles();

		// Your other setup logic
		// ...

		return {};
	},
	mounted(){
		// console.log(this.$auth)
	},
	data() {
		return {
		};
	},
	methods: {
		getColorFromName(name) {
			const hash = this.hashStringToNumber(name);
			const index = hash % colors.length;
			return colors[index];
		},
	},
	name: "App",
};
</script>

<style>
#body-main{
	background-color: papayawhip;
	padding-left: 70px;
	overflow-x: hidden;
}
.v-overlay__content{
	overflow: hidden;
}
@media (min-width: 576px) {
	#body-main{
		padding-left: 70px;
	}
}

/* Scroll bar stylings */
::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

/* Track */
::-webkit-scrollbar-track {
  background: var(--lightestgrey); 
}

/* Handle */
::-webkit-scrollbar-thumb {
  background: #888; 
  border-radius: 5px;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #555; 
}
</style>