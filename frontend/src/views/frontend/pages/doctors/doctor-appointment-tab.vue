<template>
	<div class="tab-pane" :id="tab + '-appointments'">
		<DataTable
		v-model:filters="filters"
		size="small"
		:sortField="tab == 'arrived' ? 'arriveTime' : 'appointment_time'"
		paginator
		dataKey="id"
		filterDisplay="row"
		resizableColumns
		:sortOrder="1"
		:rows="10"
		:rowsPerPageOptions="[10, 20, 50]"
		:value="updatedAppointments"
		selectionMode="single" 
		:metaKeySelection="true" 
		@row-contextmenu="handleRowContextMenu"
		>
			<template #empty><v-empty-state title="No Appointments"></v-empty-state></template>
			<template #loading> Loading Appointments data. Please wait.</template>
			<Column header="Patient" 
			field="patient_cpr" 
			:showFilterMenu="false" 
			:showClearButton="false" 
			style="width: 20%"
			>
				<template #body="{ data }">
					<router-link style="color: unset; text-decoration: unset" :to="{ name: 'patient', params: { patientId: data.patient_details.id } }">
						<div class="flex align-items-center gap-2">
							<v-avatar>
								<img
								class="h-100 w-100"
								:src="data.patient_details.image ? 
									data.patient_details.image :
									data.patient_details.gender === 'Male' ? maleImage : femaleImage"
								/>
								<!-- <span v-if="!data.patient_details.image" class="text-h5">{{ getInitials(data.patient_name) }}</span> -->
							</v-avatar>
							<div class="position-relative vstack">
								{{ data.patient_name }}
								<span class="fw-light text-teal ms-3" style="font-size: smaller">{{ data.patient_details.cpr }}</span>
							</div><br/>
						</div>
					</router-link>
				</template>
				<template #filter="{ filterModel, filterCallback }">
					<a-input 
					v-model:value="filterModel.value"
					@change="filterCallback()"
					placeholder="Search by Patient" 
					class="p-column-filter"
					style="width: 100%; align-items: center;"
					/>
				</template>
			</Column>
			<Column header="Apt Time" 
			field="appointment_time" 
			:showFilterMenu="false" 
			:showClearButton="false" 
			filterField="appointment_time_moment" 
			style="width: 10%"
			>
				<template #body="{ data }">
					<div class="text-center">
						{{ data.appointment_date_moment }}
					</div>
					<div class="text-center">
						{{ data.appointment_time_moment }}
					</div>
				</template>
				<template #filter="{ filterModel, filterCallback }">
					<a-input 
					v-model:value="filterModel.value"
					@change="filterCallback()"
					placeholder="Search by Time" 
					class="p-column-filter"
					style="width: 100%; align-items: center;"
					/>
				</template>
			</Column>
			<Column header="Arv Time" v-if="tab == 'arrived' || tab == 'ready'"
			field="arriveTime" 
			:showFilterMenu="false" 
			:showClearButton="false" 
			style="width: 5%"
			>
				<template #body="{ data }">
					{{ data.timeSinceArrived }}
				</template>
			</Column>
			<Column header="Status" 
			field="status" 
			:showFilterMenu="false" 
			:showClearButton="false" 
			style="width: 10%"
			>
				<template #body="{ data }">
					<v-chip class="ma-2" label size="small" :color="getSeverity(data.status)">{{ data.status }}</v-chip>
				</template>
				<template #filter="{ filterModel, filterCallback }">
					<a-select
						v-model:value="filterModel.value"
						@change="(filterCallback())"
						class="p-column-filter"
						style="width: 100%; align-items: center;"
						placeholder="Any"
						:options="statuses"
						allowClear
					>
						<template #option="{ value: val }">
							<v-chip class="ma-2" label size="small" :color="getSeverity(val)">{{ val }}</v-chip>
						</template>
					</a-select>
				</template>
			</Column>
			<Column header="Mobile" 
			field="mobile" 
			filterField="patient_details.mobile" 
			:showFilterMenu="false" 
			:showClearButton="false" 
			style="width: 10%"
			>
				<template #body="{ data }">
					{{ data.patient_details.mobile }}
				</template>
				<template #filter="{ filterModel, filterCallback }">
					<a-input 
						v-model:value="filterModel.value"
						@change="filterCallback()"
						placeholder="Search by Mobile" 
						class="p-column-filter"
						style="width: 100%; align-items: center;"
					/>
				</template>
			</Column>
			<Column header="Practitioner" 
			field="practitioner_name" 
			filterField="practitioner_name" 
			:showFilterMenu="false" 
			:showClearButton="false" 
			style="width: 20%"
			>
				<template #body="{ data }">
					<div class="flex align-items-center gap-2" v-if="data.practitioner_name">
						<v-avatar :color="!data.practitioner_image ? colorCache[data.practitioner_name] || '': ''">
							<img
							v-if="data.practitioner_image"
							class="h-100 w-100"
							:src="data.practitioner_image"
							/>
							<span v-if="!data.practitioner_image && data.practitioner_name" class="text-h6">{{ data.practitioner_name[0] }}</span>
						</v-avatar>
						<span>{{ data.practitioner_name }}</span>
					</div>
				</template>
				<template #filter="{ filterModel, filterCallback }">
					<a-select
					v-model:value="filterModel.value"
					@change="(filterCallback())"
					mode="multiple"
					class="p-column-filter"
					style="width: 100%; align-items: center;"
					placeholder="Any Practitioner"
					max-tag-count="responsive"
					:options="$resources.practitioners.data?.options"
					:fieldNames="{label: 'practitioner_name', value: 'name'}"
					show-search
                    :loading="$resources.practitioners.list.loading"
                    @search="(value) => {handleSearch(
						value, 
						$resources.practitioners, 
						{status: 'Active', practitioner_name: ['like', `%${value}%`]}, 
						{status: 'Active'},
                    )}"
                    :filterOption="false"
					>
						<template #option="{ practitioner_name, image }">
							<v-avatar size="25" :color="!image ? colorCache[practitioner_name] : ''">
								<img
									v-if="image"
									class="h-100 w-100"
									:src="image"
								/>
								<span v-if="!image && practitioner_name" style="font-size: small;">{{ practitioner_name[0] }}</span>
							</v-avatar>
							<span class="ms-2">{{ practitioner_name }}</span>
						</template>
						<template #tagRender="{ option, onClose }">
							<v-chip size="small" closable @click:close="onClose">
								<v-avatar size="20" :color="!option.image ? colorCache[option.practitioner_name] : ''">
									<img
										v-if="option.image"
										class="h-100 w-100"
										:src="option.image"
									/>
									<span v-if="!option.image && option.practitioner_name" style="font-size: xx-small;">{{ option.practitioner_name[0] }}</span>
								</v-avatar>
								<span>{{ option.practitioner_name }}</span>
							</v-chip>
						</template>
					</a-select>
				</template>
			</Column>
			<Column field="department" hidden :showFilterMenu="false" :showClearButton="false">
				<template #filter="{ filterModel, filterCallback }">
					<a-select
						v-model:value="filterModel.value"
						@change="(filterCallback())"
						class="p-column-filter"
						style="width: 100%; align-items: center;"
						placeholder="Any"
						allowClear
					>
						<template #option="{ value: val }">
							<v-chip class="ma-2" label size="small">{{ val }}</v-chip>
						</template>
					</a-select>
				</template>
			</Column>
			<Column header="Room" 
			field="service_unit" 
			:showFilterMenu="false" 
			:showClearButton="false" 
			style="width: 10%"
			>
				<template #body="{ data }">
					<v-chip class="ma-2" label size="small">{{ data.service_unit }}</v-chip>
				</template>
				<template #filter="{ filterModel, filterCallback }">
					<a-select
					v-model:value="filterModel.value"
					@change="(filterCallback())"
					class="p-column-filter"
					style="width: 100%; align-items: center;"
					placeholder="Any"
					:options="$resources.serviceUnits.data?.options"
					:fieldNames="{label: 'name', value: 'name'}"
					allowClear
					show-search
                    :loading="$resources.serviceUnits.list.loading"
                    @search="(value) => {handleSearch(
						value, 
						$resources.serviceUnits, 
						{name: ['like', `%${value}%`]}, 
						{},
                    )}"
                    :filterOption="false"
					>
						<template #option="{ name: val }">
							<v-chip class="ma-2" label size="small">{{ val }}</v-chip>
						</template>
					</a-select>
				</template>
			</Column>
			<Column header="Payment Type" 
			field="custom_payment_type" 
			:showFilterMenu="false" 
			:showClearButton="false" 
			style="width: 10%"
			>

			</Column>
			<Column style="width: 5%">
				<template #body="{ data }">
					<div>
						<v-btn 
						v-if="tab == 'scheduled' || tab == 'arrived'" 
						variant="text" 
						color="green"
						icon="mdi mdi-arrow-right-bold-outline" 
						@click="() => { 
							selectedRow = data
							let next = ''
							if(tab == 'scheduled') next = 'Arrived'
							if(tab == 'arrived') next = 'Ready'
							updateStatus({label: next}) 
						}">
						</v-btn>
						<v-btn 
							v-if="data.notes || data.visit_notes.length > 0" 
							size="small" 
							variant="text" 
							icon
							@click="e => {
								selectedRow = data
								toggleOP(e)
							}"
						>
							<v-badge 
							color="success" :content="data.visit_notes.filter(val => !val.read).length + (data.notes && 1)" 
							:offset-y="5" 
							:offset-x="6"
							>
								<img :src="bellImage" width="40px" class="me-1"/>
							</v-badge>
						</v-btn>
						<!-- <i v-else class="mdi mdi-bell-outline" style="font-size: 25px; padding-left: 6px;"></i> -->
						<v-btn v-else
						icon="mdi mdi-bell-plus-outline" 
						variant="text" 
						@click="$emit('appointment-note-dialog', data)"
						>
						</v-btn>
					</div>
				</template>
			</Column>
		</DataTable>
		<ContextMenu ref="menu" :model="contextItems" @hide="selectedRow = null"/>
		<OverlayPanel ref="op">
			<div class="flex flex-column gap-3 w-min-96">
				<div v-if="selectedRow.notes">
					<span class="fw-semibold d-block mb-2">Appointment Notes</span>
					<a-textarea v-model:value="selectedRow.notes" :rows="4"/>
				</div>
				<v-btn
				icon="mdi mdi-bell-plus-outline" 
				variant="text" 
				@click="$emit('appointment-note-dialog', data)"
				>
				</v-btn>
				<div v-if="selectedRow.visit_notes.length > 0">
					<!-- <span class="fw-semibold d-block mb-2">Visit Notes</span>
					<ul class="list-none p-0 m-0 flex flex-column">
						<li v-for="(note, index) in selectedRow.visit_notes" :key="index" class="flex align-items-center gap-2 mb-3">
							<div>
								<a-textarea v-model:value="note" disabled/>
								<span>{{ note.time }}</span>
							</div>
							<div class="flex align-items-center gap-2 text-color-secondary ms-auto text-sm">
								<span>{{ note.provider }}</span>
							</div>
						</li>
					</ul> -->
					<DataTable 
					:value="selectedRow.visit_notes" 
					selectionMode="single" 
					:metaKeySelection="true" 
					dataKey="name" 
					class="max-h-72 overflow-y-auto"
					>
						<template #header>
							<div class="flex flex-wrap items-center justify-between gap-2">
								<span class="text-xl font-bold">Visit Notes</span>
							</div>
						</template>
						<Column>
							<template #body="{ data }">
								<div>
									<v-btn v-if="data.read" size="small" variant="text" icon="mdi mdi-eye" @click="() => { data.read = 0 }">
									</v-btn>
									<v-btn v-else-if="!data.read" size="small" variant="text" icon="mdi mdi-eye-off" @click="() => { data.read = 1 }">
									</v-btn>
								</div>
							</template>
						</Column>
						<Column header="Time" field="dayDate">
							<template #body="{ data }">
								<div>
									{{ data.dayDate }}
								</div>
								<div>
									{{ data.dayTime }}
								</div>
							</template>
						</Column>
						<Column header="From" field="from"></Column>
						<Column header="To" field="full_name"></Column>
						<Column header="Note" field="note"></Column>
					</DataTable>
				</div>
			</div>
		</OverlayPanel>
	</div>
</template>

<script >
import dayjs from 'dayjs';
import colors from '@/assets/json/colors.json';
import { FilterMatchMode } from 'primevue/api';
import axios from 'axios';

import { VAvatar } from 'vuetify/components/VAvatar';
import { VChip } from 'vuetify/components/VChip';
import { VListItem } from 'vuetify/components/VList';
import { VEmptyState } from 'vuetify/labs/VEmptyState';

import bellImage from '@/assets/img/animations/alarm.gif';
import maleImage from '@/assets/img/male.png';
import femaleImage from '@/assets/img/female.png';

let formatedDates =  [dayjs().format('YYYY-MM-DD')]

export default {
	inject: ['$call'],
	components: {
		VAvatar, VChip, VListItem, VEmptyState,
	},
	props: {
		appointments: {default: []},
		tab: {type: String, default: 'scheduled'},
		searchValue: {type: String, default: ''},
		selectedDates: {default: [dayjs()]},
		selectedDepartments: {default: []},
		loading: {type: Boolean, default: true},
	},
	resources: {
		practitioners() { return { 
			type: 'list', 
			doctype: 'Healthcare Practitioner', 
			fields: ['practitioner_name', 'image', 'department', 'name'], 
			filters: {status: 'Active'},
			auto: true, 
			orderBy: 'practitioner_name',
			pageLength: 10,
			url: 'frappe.desk.reportview.get',
			transform(data) {
				if(data.values.length == 0)
					data.options = []
				else{
					data.options = this.transformData(data.keys, data.values);  // Transform the result into objects
					for (let d of data.options) {
						if(!this.colorCache[d.practitioner_name])
							this.colorCache[d.practitioner_name] = this.getColorFromName(d.practitioner_name)
					}
				}
				return data
			},
		}},
		serviceUnits() { return { 
			type: 'list', 
			doctype: 'Healthcare Service Unit', 
			fields:['name'], 
			auto: true, 
			orderBy: 'name',
			pageLength: 10,
			url: 'frappe.desk.reportview.get', 
			transform(data) {
				if(data.values.length == 0)
					data.options = []
				else
					data.options = this.transformData(data.keys, data.values);  // Transform the result into objects
				return data
			}
		}},
  	},
	computed: {
		updatedAppointments() {
			return this.appointments.map(appointment => {
				const arrivalTime = dayjs(appointment.arriveTime);
				const diffInSeconds = this.currentTime.diff(arrivalTime, 'second');
				const hours = Math.floor(diffInSeconds / 3600);
				const minutes = Math.floor((diffInSeconds % 3600) / 60);
				const seconds = diffInSeconds % 60;
				return {
					...appointment,
					timeSinceArrived: `${hours}h ${minutes}m`
				};
			});
		},
	},
	mounted() {
		setInterval(() => {
			this.currentTime = dayjs();
		}, 60000); // Update every n mili seconds
	},
	data() {
		return {
			bellImage:bellImage,
			maleImage:maleImage,
			femaleImage:femaleImage,
			filters: {
				global: { value: null, matchMode: FilterMatchMode.CONTAINS },
				patient_name: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
				'patient_details.cpr': { value: null, matchMode: FilterMatchMode.STARTS_WITH },
				department: { value: null, matchMode: FilterMatchMode.IN },
				patient_cpr: { value: null, matchMode: FilterMatchMode.CONTAINS },
				practitioner_name: { value: undefined, matchMode: FilterMatchMode.IN },
				appointment_time: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
				appointment_time_moment: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
				appointment_date: { value: formatedDates, matchMode: FilterMatchMode.IN },
				service_unit: { value: null, matchMode: FilterMatchMode.EQUALS },
				status: { value: null, matchMode: FilterMatchMode.EQUALS },
				'patient_details.mobile': { value: null, matchMode: FilterMatchMode.STARTS_WITH },
				custom_payment_type: { value: null, matchMode: FilterMatchMode.EQUALS },
			},
			statuses: [{label:'Scheduled', value:'Scheduled'}, {label:'Rescheduled', value:'Rescheduled'}, {label:'Walked In', value:'Walked In'}],
			purposes: [{label:'General', value:'General'}, {label:'Follow-up', value:'Follow-up'}, {label:'Consultation', value:'Consultation'}],
			selectedRow: null,
			contextItems: [
				...(this.$route.name == 'appointments' ? [{
					label: 'New Appointment',
					icon: 'mdi mdi-account-multiple-plus-outline',
					command: () => this.$emit('appointment-dialog', 'New Appointment', false, this.selectedRow)
				}] : []),
				{
					label: 'Status',
					icon: 'mdi mdi-clipboard-edit-outline',
					items: [
						...(this.tab !== 'scheduled' ? [{label: 'Scheduled', command: ({ item }) => this.updateStatus(item)}] : []),
						...(this.tab !== 'arrived' ? [{label: 'Arrived', command: ({ item }) => this.updateStatus(item)}] : []),
						...(this.tab !== 'ready' ? [{label: 'Ready', command: ({ item }) => this.updateStatus(item)}] : []),
						...(this.tab !== 'in room' ? [{label: 'In Room', command: ({ item }) => this.updateStatus(item)}] : []),
						...(this.tab !== 'completed' ? [{label: 'Completed', command: ({ item }) => this.updateStatus(item)}] : []),
						...(this.tab !== 'transferred' ? [{label: 'Transferred', command: ({ item }) => this.updateStatus(item)}] : []),
					]
				},
				{
					label: 'Add Note',
					icon: 'mdi mdi-text',
					command: () => {this.$emit('appointment-note-dialog', this.selectedRow)}
				},
				{separator: true},
				...(this.$route.name == 'appointments' ? [{
					label: 'Reschedule Appointment',
					icon: 'mdi mdi-clock-outline',
					command: () => {this.$emit('appointment-dialog', 'Reschedule Appointment', false, this.selectedRow)}
				}] : []),
				{
					label: 'ID Card Reading',
					icon: 'mdi mdi-card-account-details-outline',
					command: () => {this.readIdCard()}
				},
				{
					label: 'Vital Signs',
					icon: 'mdi mdi-pulse',
					command: () => {this.$emit('vital-sign-dialog', this.selectedRow)}
				},
				...(this.$route.name == 'nurse-dashboard' ? [{
					label: 'Medical History',
					icon: 'mdi mdi-medical-bag',
					command: () => this.$emit('medical-history-dialog', this.selectedRow)
				}] : []),
				{
					label: 'Update Room',
					icon: 'mdi mdi-door-open',
					command: () => {this.$emit('service-unit-dialog', this.selectedRow)}
				},
				...(this.$route.name == 'appointments' ? [{
					label: 'Update Payment Type',
					icon: 'pi pi-wallet',
					command: () => {this.$emit('payment-type-dialog', this.selectedRow)}
				}] : []),
				{
					label: 'Patient Encounter',
					icon: 'mdi mdi-bandage',
					command: () => {this.goToEncounter()}
				},
				{
					label: 'Request a Service',
					icon: 'mdi mdi-needle',
					disabled: true
				},
				{
					label: 'Tranfer To Practitioner',
					icon: 'mdi mdi-transit-transfer',
					command: () => {this.$emit('transfer-practitioner-dialog', this.selectedRow)}
				},
      		],
			colorCache: {},
			currentTime: dayjs(),
			
		};
	},
	watch: {
		searchValue: {
			handler(newValue) {
				if(newValue)
					this.filters['global'].value = this.searchValue
			}
		},
		selectedDepartments: {
			handler(newValue) {
				if(newValue)
					this.filters['department'].value = this.selectedDepartments
			}
		},
		selectedDates: {
			handler(newValue) {
				if(newValue){
					const formated = this.selectedDates.map(date => date.format('YYYY-MM-DD'))
					this.filters['appointment_date'].value = formated
					formatedDates = formated
				}
			}
		},
	},
	methods: {
		getSeverity(status) {
			switch (status) {
				case 'Scheduled':
					return 'success';

				case 'Rescheduled':
					return 'info';

				case 'Walked In':
					return 'warning';

				default:
					return 'danger';
			}
		},
		handleRowContextMenu({ originalEvent, data, index }) {
			this.selectedRow = data
			this.$refs.menu.show(originalEvent);
		},
		randomColors() {
			return colors[Math.floor(Math.random() * colors.length)];
		},
		getColorFromName(name) {
			const hash = this.hashStringToNumber(name);
			const index = hash % colors.length;
			return colors[index];
		},
		hashStringToNumber(str) {
			if(!str)
				str = 'demo'
			let hash = 0;
			for (let i = 0; i < str.length; i++) {
				hash = str.charCodeAt(i) + ((hash << 5) - hash);
			}
			return Math.abs(hash);
		},
		getInitials(name) {
			if(!name)
				name = 'Undefined'
			let names = name.split(' '),
				initials = names[0].substring(0, 1).toUpperCase();
			
			if (names.length > 1) {
				initials += names[names.length - 1].substring(0, 1).toUpperCase();
			}
			return initials;
		},
		goToEncounter() {
			this.$call('healthcare_doworks.api.methods.patient_encounter_name', {appointment_id: this.selectedRow.name})
			.then(response => {
				this.$router.push({ name: 'patient-encounter', params: { encounterId: response } });
			}).catch(error => {
				console.error(error);
			});
		},
		updateStatus(item) {
			this.$call('healthcare_doworks.api.methods.change_status',
				{docname: this.selectedRow.name, status: item.label}
			)
		},
		getNotesCount(data) {
			let count = data.visit_notes.reduce((total, value) => {
				if(value.note)
					return ++total;
				return total;
			}, 0)
			if(data.notes)
				++count;
			return count;
		},
		toggleOP(event) {
			this.$refs.op.toggle(event)
		},
		transformData (keys, values) {
			return values.map(row => {
				const obj = {};
				keys.forEach((key, index) => {
					obj[key] = row[index];  // Map each key to its corresponding value
				});
				return obj;
			});
		},
		handleSearch(query, resource, filters, initialFilters) {
			// Clear the previous timeout to avoid spamming requests
			clearTimeout(this.searchTimeout);

			// Set a new timeout (300ms) for debouncing
			this.searchTimeout = setTimeout(() => {
				if (query) {
					// Update list resource options to fetch matching records from server
					resource.update({filters});

					// Fetch the updated results
					resource.reload();
				} else {
					// If no search query, load initial records
					resource.update({filters: initialFilters});
					resource.reload();
				}
			}, 300);  // Debounce delay of 300ms
		},
		async readIdCard(event) {
            // var xmlHttp = new XMLHttpRequest();
            // xmlHttp.open( "GET", "http://localhost:5000/card", false ); // false for synchronous request
            // xmlHttp.send( null );
            //xmlHttp.setRequestHeader("Authorization", "Basic "+"o6py7d5i5r53ogoac7yhn38n6rw5vcm7qfd8hqdhdms39qphvjhrehw9h94wqexufhkzykkuce7wbcto");
            const response = await axios.get('http://localhost:5000/card');
			// this.cardData = response.data;
			console.log(response)
            
            // cur_frm.set_value("full_name",xmlHttp.responseText)
            
//  			let data_string=xmlHttp.responseText;
//  			// console.info(data_string);
//  			var data = JSON.parse(data_string);
// 			if(!data){
				this.$emit('show-alert', 'Please Inser A Card!', 10000)
// 				return
// 			}
 			
//  			console.log ("Hello " + data['first_name'] + " " +data['middle_name1'] +" "+ data['middle_name2']+" "+ data['middle_name3'] +" "+ data['middle_name4'] +" "+ data['last_name'])
//  			// Full name English
// 			let first_name = data['first_name']
// 			let middle_name = ''
// 			let last_name = ''
			
// 			if (data['middle_name1'])
// 				middle_name = data['middle_name1']
// 			if (data['middle_name2'])
// 				middle_name += " " + data['middle_name2']
// 			if (data['middle_name3'])
// 				middle_name += " " + data['middle_name3']
// 			if (data['middle_name4'])
// 				middle_name += " " + data['middle_name4']
// 			if (data['last_name'])
// 				last_name = data['last_name']

// 			let patient_name = (first_name + " " + middle_name + " " + last_name).trim()
			
// 			// Full name Arabic

// 			let first_name_ar = data['first_name_ar']
// 			let custom_middle_name_ar = ''
// 			let custom_last_name_ar = ''
			
// 			if (data['middle_name1_ar'])
// 				custom_middle_name_ar = data['middle_name1_ar']
// 			if (data['middle_name2_ar'])
// 				custom_middle_name_ar += " " + data['middle_name2_ar']
// 			if (data['middle_name3_ar'])
// 				custom_middle_name_ar += " " + data['middle_name3_ar']
// 			if (data['middle_name4_ar'])
// 				custom_middle_name_ar += " " + data['middle_name4_ar']
// 			if (data['last_name_ar'])
// 				custom_last_name_ar = data['last_name_ar']

// 			let patient_name_ar = (first_name_ar + " " + custom_middle_name_ar + " " + custom_last_name_ar).trim()
		
			
// 			// gender
// 			let sex = ''
// 			if (data['gender'] == "M")
// 				sex = 'Male'
// 			if (data['gender'] == "F")
// 				sex = 'Female'
			
// 			// nationality
// 			let custom_nationality = ''
// 			if(data['nationality'])
// 				custom_nationality = data['nationality']
			
// 			// occupation_description
// 			let custom_occupation_description = ''
// 			if (data['occupation_description'])
// 				custom_occupation_description = data['occupation_description']
			
// 			//cpr
// 			let custom_cpr = ''
// 			if (data['cpr'])
// 			{
// 				custom_cpr = data['cpr'].toString()
// 				if(custom_cpr.length == 9)
// 					custom_cpr = "0" + custom_cpr

// 			}
			
// 			// email
// 			let email = ''
// 			if (data['email'])
// 				email = data['email']
			
// 			// employer
// 			let custom_employer = ''
// 			if (data['employer'])
// 				custom_employer = data['employer']
			
// 			//birthdate
// 			let dob = ''
// 			if (data['birthdate'])
// 				var birthdate = data['birthdate'].toString().substr(0,4) + "-" + data['birthdate'].toString().substr(4,2) + "-" + data['birthdate'].toString().substr(6,2)
// 				dob = birthdate
// 				// console.log(birthdate)
// 			// mobile number
// 			let mobile = ''
// 			if (data['contact_no'])
// 				mobile = "+" + data['contact_no']
			
// 			// address
// 			let address_cpr = ""
// 			if (data['building_no'])
// 				address_cpr += "Building " +data['building_no'] + " "
// 			if (data['flat_no'])
// 				address_cpr +=  ",Flat " +data['flat_no'] + " "
// 			if (data['road_no'])
// 				address_cpr += ",Road " + data['road_no'] + " "
// 			if (data['block_no'])
// 				address_cpr += ",Block "+ data['block_no'] + " "
// 			if (data['block_name'])
// 				address_cpr += data['block_name'] + " "
// 				let address = address_cpr
			
			
//  		    xmlHttp = new XMLHttpRequest();
//             xmlHttp.open( "GET", "http://localhost:5000/card_photo", false ); // false for synchronous request
//             xmlHttp.send( null );
            
            
//             // cur_frm.set_value("full_name",xmlHttp.responseText)
//             console.info(xmlHttp.responseText)
            
//  			data_string=xmlHttp.responseText;
 			
// //  			data_string=data_string.replace("[","");
// //  			data_string=data_string.replace("]","");
//  			data_string = data_string.replaceAll("'",'"')
//  			data_string = data_string.replaceAll('A"ALI',"A'ALI")
//  			data_string = data_string.replaceAll(': b"',': "')
//  			data_string = data_string.replaceAll("\\x00",'')
//  			data_string = data_string.slice(1,-2);
//  			console.info("Before parse:" + data_string)
// 			data = JSON.parse(data_string);
			
// 			// upload images
// 			let custom_personal_picture = ''
// 			if (data['image'])
// 				custom_personal_picture = "+" + data['image']
			
// 			// upload signature
// 			let signature_picture = ''
// 			if (data['signature'])
// 				signature_picture = "+" +data['signature']
 		
//  			// console.info(xmlHttp.responseText);
 			
//  			// console.info(data['first_name']);
//  			// cur_frm.set_value("full_name",data['first_name'])
			    
		},
	},
};
</script>

<style>
.ant-picker-dropdown,.ant-select-dropdown{
	z-index: 3000;
}
</style>