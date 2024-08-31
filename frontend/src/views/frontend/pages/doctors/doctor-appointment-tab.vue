<template>
	<div class="tab-pane" :id="tab + '-appointments'">
		<DataTable
		v-model:filters="filters"
		size="small"
		sortField="appointment_time"
		paginator
		dataKey="id"
		filterDisplay="row"
		resizableColumns
		:loading="loading"
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
					<!-- <router-link to="patient-profile"> -->
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

					<!-- </router-link> -->
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
					{{ data.appointment_time_moment }}
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
			style="width: 10%"
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
					<div class="flex align-items-center gap-2">
						<v-avatar :color="!data.practitioner_image ? colorCache[data.practitioner_name] || '': ''">
							<img
							v-if="data.practitioner_image"
							class="h-100 w-100"
							:src="data.practitioner_image"
							/>
							<span v-if="!data.practitioner_image" class="text-h6">{{ data.practitioner_name[0] }}</span>
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
					:options="$myresources.practitioners"
					:fieldNames="{label: 'practitioner_name', value: 'practitioner_name'}"
					>
						<template #option="{ practitioner_name, image }">
							<v-avatar size="25" :color="!image ? colorCache[practitioner_name] : ''">
								<img
									v-if="image"
									class="h-100 w-100"
									:src="image"
								/>
								<span v-if="!image" style="font-size: small;">{{ practitioner_name[0] }}</span>
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
									<span v-if="!option.image" style="font-size: xx-small;">{{ option.practitioner_name[0] }}</span>
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
			<Column header="For" 
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
						:options="$myresources.serviceUnits"
						:fieldNames="{label: 'name', value: 'name'}"
						allowClear
					>
						<template #option="{ name: val }">
							<v-chip class="ma-2" label size="small">{{ val }}</v-chip>
						</template>
					</a-select>
				</template>
			</Column>
			<Column style="width: 5%">
				<template #body="{ data }">
					<v-btn 
						v-if="data.notes || data.visit_notes.length > 0" 
						size="small" 
						variant="text" 
						icon
						@click="toggleOP"
					>
						<v-badge color="success" :content="data.visit_notes.length + (data.notes && 1)" :offset-y="5" :offset-x="6">
							<img :src="bellImage" width="40px" class="me-1"/>
						</v-badge>
					</v-btn>
					<i v-else class="mdi mdi-bell-outline" style="font-size: 25px; padding-left: 6px;"></i>
					<OverlayPanel ref="op">
						<div class="flex flex-column gap-3 w-25rem">
							<div v-if="data.notes">
								<span class="fw-semibold d-block mb-2">Appointment Notes</span>
								<a-textarea v-model:value="data.notes" disabled/>
							</div>
							<div v-if="data.visit_notes.length > 0">
								<!-- <span class="fw-semibold d-block mb-2">Visit Notes</span>
								<ul class="list-none p-0 m-0 flex flex-column">
									<li v-for="(note, index) in data.visit_notes" :key="index" class="flex align-items-center gap-2 mb-3">
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
								:value="data.visit_notes" 
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
									<Column field="time"></Column>
									<Column field="provider"></Column>
									<Column field="note"></Column>
								</DataTable>
							</div>
						</div>
					</OverlayPanel>
				</template>
			</Column>
			<ContextMenu ref="menu" :model="contextItems" @hide="selectedRow = null"/>
		</DataTable>
	</div>
</template>

<script >
import dayjs from 'dayjs';
import colors from '@/assets/json/colors.json';
import { FilterMatchMode } from 'primevue/api';

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
		appointments: {
			default: []
		},
		tab:{
			type: String,
			default: 'scheduled'
		},
		searchValue: {
			type: String,
			default: ''
		},
		selectedDates: {
			default: [dayjs()]
		},
		selectedDepartments: {
			default: []
		},
		loading: {
			type: Boolean,
			defaul: true
		}
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
					timeSinceArrived: `${hours}h ${minutes}m ${seconds}s`
				};
			});
		},
	},
	mounted() {
		setInterval(() => {
			this.currentTime = dayjs();
		}, 1000); // Update every second
	},
	data() {
		return {
			bellImage:bellImage,
			maleImage:maleImage,
			femaleImage:femaleImage,
			filters: {
				global: { value: null, matchMode: FilterMatchMode.CONTAINS },
				patient_name: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
				cpr: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
				department: { value: null, matchMode: FilterMatchMode.IN },
				patient_cpr: { value: null, matchMode: FilterMatchMode.CONTAINS },
				practitioner_name: { value: undefined, matchMode: FilterMatchMode.IN },
				appointment_time: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
				appointment_time_moment: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
				appointment_date: { value: formatedDates, matchMode: FilterMatchMode.IN },
				service_unit: { value: null, matchMode: FilterMatchMode.EQUALS },
				status: { value: null, matchMode: FilterMatchMode.EQUALS },
				'patient_details.mobile': { value: null, matchMode: FilterMatchMode.STARTS_WITH },
			},
			statuses: [{label:'Scheduled', value:'Scheduled'}, {label:'Rescheduled', value:'Rescheduled'}, {label:'Walked In', value:'Walked In'}],
			purposes: [{label:'General', value:'General'}, {label:'Follow-up', value:'Follow-up'}, {label:'Consultation', value:'Consultation'}],
			selectedRow: null,
			contextItems: [
				{
					label: 'New Appointment',
					icon: 'mdi mdi-account-multiple-plus-outline',
					command: () => this.$emit('appointment-dialog', 'New Appointment', false, this.selectedRow)
				},
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
					command: () => this.$emit('appointment-note-dialog', this.selectedRow)
				},
				{separator: true},
				{
					label: 'Reschedule Appointment',
					icon: 'mdi mdi-clock-outline',
					command: () => this.$emit('appointment-dialog', 'Reschedule Appointment', false, this.selectedRow)
				},
				{
					label: 'Add CPR Reading',
					icon: 'mdi mdi-card-account-details-outline',
					disabled: true
				},
				{
					label: 'Vital Signs',
					icon: 'mdi mdi-pulse',
					command: () => this.$emit('vital-sign-dialog', this.selectedRow)
				},
				{
					label: 'Update Room',
					icon: 'mdi mdi-door-open',
					command: () => this.$emit('service-unit-dialog', this.selectedRow)
				},
				{
					label: 'Update Payment Type',
					icon: 'pi pi-wallet',
					command: () => this.$emit('payment-type-dialog', this.selectedRow)
				},
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
					command: () => this.$emit('transfer-practitioner-dialog', this.selectedRow)
				},
      		],
			colorCache: {},
			currentTime: dayjs(),
			
		};
	},
	watch: {
		'$myresources.practitioners': {
			handler(newValue) {
				if(newValue)
					newValue.forEach(value => {
						if(!this.colorCache[value.practitioner_name])
							this.colorCache[value.practitioner_name] = this.getColorFromName(value.practitioner_name)
					})
			},
			immediate: true,
		},
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
			let hash = 0;
			for (let i = 0; i < str.length; i++) {
			hash = str.charCodeAt(i) + ((hash << 5) - hash);
			}
			return Math.abs(hash);
		},
		getInitials(name) {
			let names = name.split(' '),
				initials = names[0].substring(0, 1).toUpperCase();
			
			if (names.length > 1) {
				initials += names[names.length - 1].substring(0, 1).toUpperCase();
			}
			return initials;
		},
		goToEncounter() {
			this.$call('healthcare_doworks.api.methods.patient_encounter_name', {appointment_id: this.selectedRow.appointment_id})
			.then(response => {
				this.$router.push({ name: 'patient-encounter', params: { encounterId: response } });
			}).catch(error => {
				console.error(error);
			});
		},
		updateStatus(item) {
			this.$call('healthcare_doworks.api.methods.change_status',
				{docname: this.selectedRow.appointment_id, status: item.label}
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
	},
};
</script>

<style>
.ant-picker-dropdown,.ant-select-dropdown{
	z-index: 3000;
}
</style>