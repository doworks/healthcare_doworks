<template>
	<div class="tab-pane" :id="tab + '-appointments'">
		<DataTable
		v-model:filters="filters"
		size="small"
		:sortField="tab == 'arrived' ? 'arriveTime' : 'appointment_datetime'"
		paginator
		dataKey="id"
		filterDisplay="row"
		resizableColumns
		:sortOrder="1"
		:rows="20"
		:rowsPerPageOptions="[20, 100, 500, 2500]"
		:value="filteredData"
		selectionMode="single" 
		:metaKeySelection="true" 
		@row-contextmenu="handleRowContextMenu"
		:rowClass="appointmentRowClass"
		@page="props => {$emit('table-page-change', props)}"
		paginatorTemplate="RowsPerPageDropdown"
		:loading="loading"
		>
			<template #empty><v-empty-state v-if="!loading" title="No Appointments"></v-empty-state></template>
			<template #loading> Loading Appointments data. Please wait.</template>
			<Column header="Patient" 
			field="patient_cpr" 
			:showFilterMenu="false" 
			:showClearButton="false" 
			style="width: 20%"
			>
				<template #body="{ data }">
					<a 
					:href="$router.resolve({ name: 'patient', params: { patientId: data.patient_details.id } }).href" 
					target="_blank" 
					style="color: unset; text-decoration: unset"
					>
						<div class="flex align-items-center gap-2">
							<v-avatar>
								<img
								class="h-100 w-100"
								:src="data.patient_details.image ? 
									data.patient_details.image :
									data.patient_details.gender === 'Female' ? femaleImage : maleImage"
								/>
								<!-- <span v-if="!data.patient_details.image" class="text-h5">{{ getInitials(data.patient_name) }}</span> -->
							</v-avatar>
							<div class="position-relative vstack">
								{{ data.patient_name }}
								<span class="fw-light text-teal" style="font-size: smaller">
									{{ renderPatientDetails(data) }}
								</span>
							</div><br/>
						</div>
					</a>
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
					<div @click="() => {$emit('appointment-dialog', 'Edit Appointment', false, data)}">
						<div class="text-center">
							{{ data.appointment_date_moment }}
						</div>
						<div class="text-center">
							{{ data.appointment_time_moment }}
						</div>
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
			<Column field="appointment_datetime" hidden :showFilterMenu="false" :showClearButton="false">
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
			<Column header="Procedures" 
			field="procedure_templates" 
			style="width: 10%"
			:showFilterMenu="false" 
			:showClearButton="false" 
			>
				<template #body="{ data }">
					<div v-if="data.procedure_templates.length > 0">
						<v-chip v-for="(procedure, index) in data.procedure_templates" :key="index" class="mr-1" label size="small">{{ procedure.template }}</v-chip>
					</div>
					<div v-else>
						{{ data.notes }}
					</div>
				</template>
				<template #filter="{ filterModel, filterCallback }">
					<a-select
					v-model:value="procedureFilter"
					@change="(filterCallback())"
					mode="multiple"
					class="p-column-filter"
					style="width: 100%; align-items: center;"
					placeholder="Any Procedure"
					max-tag-count="responsive"
					:options="$resources.clinicalProcedureTemplates.data?.options"
					:fieldNames="{label: 'template', value: 'name'}"
					show-search
                    :loading="$resources.clinicalProcedureTemplates.list.loading"
                    @search="(value) => {handleSearch(
						value, 
						$resources.clinicalProcedureTemplates, 
						{template: ['like', `%${value}%`]}, 
						{},
                    )}"
                    :filterOption="false"
					>
					</a-select>
				</template>
			</Column>
			<Column header="Practitioner" 
			field="practitioner_name" 
			filterField="practitioner" 
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
						<!-- <template #tagRender="{ option, onClose }">
							<v-chip size="small" closable @click:close="onClose" v-if="option">
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
						</template> -->
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
			:pt="{
				bodycell: ({instance}) => ({
					onClick: () => {$emit('service-unit-dialog', instance.rowData)}
				})
			}"
			>
				<template #body="{ data }">
					{{ data.service_unit }}
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
						{allow_appointments: 1, is_group: 0, name: ['like', `%${value}%`]}, 
						{allow_appointments: 1, is_group: 0}, 
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
			:pt="{
				bodycell: ({instance}) => ({
					onClick: () => {$emit('payment-type-dialog', instance.rowData)}
				})
			}"
			>
			</Column>
			<Column style="width: 5%">
				<template #body="{ data }">
					<div>
						<v-btn 
						v-if="tab == 'arrived'" 
						variant="text" 
						color="pink"
						icon="mdi mdi-medical-bag" 
						@click="(event) => { 
							event.stopPropagation()
							$emit('medical-history-dialog', data)
						}">
						</v-btn>
						<v-btn 
						v-if="tab == 'arrived'" 
						variant="text" 
						color="blue"
						icon="mdi mdi-pulse" 
						@click="(event) => { 
							event.stopPropagation()
							$emit('vital-sign-dialog', data)
						}">
						</v-btn>
						<v-btn 
						v-if="tab == 'arrived'" 
						variant="text" 
						color="purple"
						icon="mdi mdi-format-list-checks" 
						@click="(event) => { 
							event.stopPropagation()
							$emit('checklist-form-dialog', data)
						}">
						</v-btn>
						<v-btn 
						v-if="tab == 'scheduled' || tab == 'arrived'" 
						variant="text" 
						color="green"
						icon="mdi mdi-arrow-right-bold-outline" 
						@click="(event) => { 
							event.stopPropagation()
							selectedRow = data
							let next = ''
							if(tab == 'scheduled') next = 'Arrived'
							if(tab == 'arrived') next = 'Ready'
							updateStatus({label: next}) 
						}">
						</v-btn>
						<v-btn 
						v-if="tab == 'no show'" 
						variant="text" 
						color="blue"
						icon="mdi mdi-walk" 
						@click="(event) => { 
							event.stopPropagation()
							selectedRow = data
							updateStatus({label: 'Arrived'}) 
						}">
						</v-btn>
						<v-btn 
						v-if="tab == 'no show'" 
						variant="text" 
						color="amber"
						icon="mdi mdi-clock-outline" 
						@click="(event) => { 
							event.stopPropagation()
							$emit('appointment-dialog', 'Reschedule Appointment', false, data)
						}">
						</v-btn>
						<v-btn 
						v-if="this.$myresources.user.roles.some(value => value.role == 'Practitioner') && 
							(tab == 'ready' || tab == 'in room' || tab == 'completed')" 
						variant="text" 
						color="blue"
						icon="mdi mdi-bandage" 
						@click="(event) => { 
							event.stopPropagation()
							selectedRow = data
							goToEncounter()
						}">
						</v-btn>
						<v-btn 
						v-if="isIOS"
						variant="text" 
						icon="mdi mdi-dots-vertical" 
						@click="(event) => { 
							event.stopPropagation()
							handleRowContextMenu({originalEvent: event, data})
						}">
						</v-btn>
						<v-btn 
							v-if="data.notes || data.visit_notes.length > 0" 
							size="small" 
							variant="text" 
							icon
							@click="e => {
								e.stopPropagation()
								selectedRow = data
								toggleOP(e)
							}"
						>
							<v-badge 
							color="success" :content="data.visit_notes.filter(val => !val.read).length + (data.notes && 1)" 
							:offset-y="-1" 
							:offset-x="6"
							>
								<img :src="bellImage" width="30px" class="me-1"/>
							</v-badge>
						</v-btn>
						<v-btn v-else
						icon="mdi mdi-bell-plus-outline" 
						variant="text" 
						@click="event => {
							event.stopPropagation()
							$emit('appointment-note-dialog', data)
						}"
						>
						</v-btn>
					</div>
				</template>
			</Column>
		</DataTable>
		<ContextMenu ref="menu" :model="contextItems" @hide="selectedRow = null"/>
		<Popover ref="op">
			<div class="flex flex-column gap-3 w-min-96">
				<div v-if="selectedRow.notes">
					<span class="fw-semibold d-block mb-2">Appointment Notes</span>
					<a-textarea v-model:value="selectedRow.notes" :rows="4"/>
				</div>
				<v-btn
				icon="mdi mdi-plus" 
				variant="text" 
				@click="$emit('appointment-note-dialog', selectedRow)"
				>
				</v-btn>
				<div v-if="selectedRow.visit_notes.length > 0">
					<DataTable 
					:value="selectedRow.visit_notes" 
					size="small"
					selectionMode="single" 
					:metaKeySelection="true" 
					dataKey="name" 
					class="max-h-72 overflow-y-auto"
					:rowClass="noteRowClass"
					>
						<template #header>
							<div class="flex flex-wrap items-center justify-between gap-2">
								<span class="text-xl font-bold">Visit Notes</span>
							</div>
						</template>
						<Column>
							<template #body="{ data }">
								<div>
									<v-btn v-if="data.read" size="small" variant="text" icon="mdi mdi-eye" @click="() => { updateSeen(data) }">
									</v-btn>
									<v-btn v-else-if="!data.read" size="small" variant="text" icon="mdi mdi-eye-off" @click="() => { updateSeen(data) }">
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
						<Column header="For" field="for"></Column>
						<Column header="Users/Roles" field="names"></Column>
						<Column header="Note" field="note"></Column>
					</DataTable>
				</div>
			</div>
		</Popover>
	</div>
</template>

<script >
import dayjs from 'dayjs';
import colors from '@/assets/json/colors.json';
import { FilterMatchMode } from '@primevue/core/api';

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
			filters:{'allow_appointments': 1, 'is_group': 0}, 
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
		clinicalProcedureTemplates() { return { 
			type: 'list', 
			doctype: 'Clinical Procedure Template', 
			fields: ['name', 'template', 'medical_department'], 
			auto: true,
			orderBy: 'name',
			pageLength: 30,
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
		filteredData() {
			return this.updatedAppointments.filter(item => {
				const procedureFilter = this.procedureTemplatesFilter(item.procedure_templates, this.procedureFilter);
				// Include other filter checks for different fields as needed
				return procedureFilter; // Add more conditions as per your filter logic
			});
		},
		contextItems() {
			return [
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
						...(this.tab !== 'cancelled' ? [{label: 'Cancelled', command: ({ item }) => this.updateStatus(item)}] : []),
					]
				},
				...(this.$route.name == 'appointments' && (this.tab == 'scheduled' || this.tab !== 'no show') ? [{
					label: 'Visit Logs',
					icon: 'mdi mdi-timetable',
					disabled: this.selectedRow?.status_log.length == 0,
					command: () => {this.$emit('visit-status-log', this.selectedRow)}
				}] : []),
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
				...(this.$route.name == 'appointments' ? [{
					label: 'Billing Items',
					icon: 'mdi mdi-invoice-text-outline',
					command: () => {this.$emit('appointment-invoice-dialog', this.selectedRow)}
				}] : []),
				{
					label: 'ID Card Reading',
					icon: 'mdi mdi-card-account-details-outline',
					command: () => {this.$emit('read-card', this.selectedRow)}
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
				...(this.$route.name == 'nurse-dashboard' ? [{
					label: 'Checklist Form',
					icon: 'mdi mdi-format-list-checks',
					command: () => this.$emit('checklist-form-dialog', this.selectedRow)
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
				...(this.$myresources.user.roles.some(value => value.role == 'Practitioner') && this.tab != 'scheduled' && this.tab != 'no show' ? [{
					label: 'Patient Encounter',
					icon: 'mdi mdi-bandage',
					command: () => {this.goToEncounter()}
				}] : []),
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
				{
					label: 'Cancel',
					icon: 'mdi mdi-cancel',
					command: () => {this.cancelAppointment()}
				},
				{
					label: 'Delete',
					icon: 'mdi mdi-delete',
					command: () => {this.deleteAppointment()}
				},
      		]		
		},
		isIOS() {
			return /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;
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
			procedureFilter: undefined,
			filters: {
				global: { value: null, matchMode: FilterMatchMode.CONTAINS },
				patient_name: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
				'patient_details.cpr': { value: null, matchMode: FilterMatchMode.STARTS_WITH },
				department: { value: null, matchMode: FilterMatchMode.IN },
				patient_cpr: { value: null, matchMode: FilterMatchMode.CONTAINS },
				procedure_templates: { value: undefined, matchMode: FilterMatchMode.IN },
				practitioner: { value: undefined, matchMode: FilterMatchMode.IN },
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
			selectedRow: null,
			// contextItems: [
			// 	...(this.$route.name == 'appointments' ? [{
			// 		label: 'New Appointment',
			// 		icon: 'mdi mdi-account-multiple-plus-outline',
			// 		command: () => this.$emit('appointment-dialog', 'New Appointment', false, this.selectedRow)
			// 	}] : []),
			// 	...(this.$route.name == 'appointments' ? [{
			// 		label: 'Visit Logs',
			// 		icon: 'mdi mdi-timetable',
			// 		disabled: this.selectedRow?.status_log.length == 0,
			// 		command: () => {this.$emit('visit-status-log', this.selectedRow)}
			// 	}] : []),
			// 	{
			// 		label: 'Status',
			// 		icon: 'mdi mdi-clipboard-edit-outline',
			// 		items: [
			// 			...(this.tab !== 'scheduled' ? [{label: 'Scheduled', command: ({ item }) => this.updateStatus(item)}] : []),
			// 			...(this.tab !== 'arrived' ? [{label: 'Arrived', command: ({ item }) => this.updateStatus(item)}] : []),
			// 			...(this.tab !== 'ready' ? [{label: 'Ready', command: ({ item }) => this.updateStatus(item)}] : []),
			// 			...(this.tab !== 'in room' ? [{label: 'In Room', command: ({ item }) => this.updateStatus(item)}] : []),
			// 			...(this.tab !== 'completed' ? [{label: 'Completed', command: ({ item }) => this.updateStatus(item)}] : []),
			// 			...(this.tab !== 'transferred' ? [{label: 'Transferred', command: ({ item }) => this.updateStatus(item)}] : []),
			// 		]
			// 	},
			// 	{
			// 		label: 'Add Note',
			// 		icon: 'mdi mdi-text',
			// 		command: () => {this.$emit('appointment-note-dialog', this.selectedRow)}
			// 	},
			// 	{separator: true},
			// 	...(this.$route.name == 'appointments' ? [{
			// 		label: 'Reschedule Appointment',
			// 		icon: 'mdi mdi-clock-outline',
			// 		command: () => {this.$emit('appointment-dialog', 'Reschedule Appointment', false, this.selectedRow)}
			// 	}] : []),
			// 	...(this.$route.name == 'appointments' ? [{
			// 		label: 'Billing Items',
			// 		icon: 'mdi mdi-invoice-text-outline',
			// 		command: () => {this.$emit('appointment-invoice-dialog', this.selectedRow)}
			// 	}] : []),
			// 	{
			// 		label: 'ID Card Reading',
			// 		icon: 'mdi mdi-card-account-details-outline',
			// 		command: () => {this.$emit('read-card', this.selectedRow)}
			// 	},
			// 	{
			// 		label: 'Vital Signs',
			// 		icon: 'mdi mdi-pulse',
			// 		command: () => {this.$emit('vital-sign-dialog', this.selectedRow)}
			// 	},
			// 	...(this.$route.name == 'nurse-dashboard' ? [{
			// 		label: 'Medical History',
			// 		icon: 'mdi mdi-medical-bag',
			// 		command: () => this.$emit('medical-history-dialog', this.selectedRow)
			// 	}] : []),
			// 	{
			// 		label: 'Update Room',
			// 		icon: 'mdi mdi-door-open',
			// 		command: () => {this.$emit('service-unit-dialog', this.selectedRow)}
			// 	},
			// 	...(this.$route.name == 'appointments' ? [{
			// 		label: 'Update Payment Type',
			// 		icon: 'pi pi-wallet',
			// 		command: () => {this.$emit('payment-type-dialog', this.selectedRow)}
			// 	}] : []),
			// 	...(this.$myresources.user.roles.some(value => value.role == 'Practitioner') ? [{
			// 		label: 'Patient Encounter',
			// 		icon: 'mdi mdi-bandage',
			// 		command: () => {this.goToEncounter()}
			// 	}] : []),
			// 	{
			// 		label: 'Request a Service',
			// 		icon: 'mdi mdi-needle',
			// 		disabled: true
			// 	},
			// 	{
			// 		label: 'Tranfer To Practitioner',
			// 		icon: 'mdi mdi-transit-transfer',
			// 		command: () => {this.$emit('transfer-practitioner-dialog', this.selectedRow)}
			// 	},
      		// ],
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
		procedureTemplatesFilter(value, filter) {
			if (!filter || filter.length == 0 || !Array.isArray(value)) return true; // If there's no filter or value isn't an array, include all

			// Check if any object in the array matches the filter value
			return value.some(item => {
				return item.template && filter.includes(item.template);
			});
		},
		renderPatientDetails(data) {
			let age = `Age: ${ data.patient_age?.split(' ')[0] } | `
			let file = `File: ${ data.patient_details.file_number } | `
			let cpr = `CPR: ${ data.patient_details.cpr } | `
			let mobile = `${ data.patient_details.mobile } | `
			let details = ''
			if(data.patient_age)
				details += age
			if(data.patient_details.file_number)
				details += file
			if(data.patient_details.cpr)
				details += cpr
			if(data.patient_details.mobile)
				details += mobile

			return details.slice(0, -2)
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
				this.$emit('show-alert', error.message, 'error')
			});
		},
		cancelAppointment() {
			this.$call('frappe.client.set_value', 
			{doctype: 'Patient Appointment', name: this.selectedRow.name, fieldname: {status: 'Cancelled', custom_visit_status: 'Cancelled'}}
			).then(response => {
				this.$toast.add({
					severity: 'success',
					summary: 'Success',
					detail: 'Appointment cancelled',
					life: 3000 // Duration in ms
				});
			}).catch(error => {
				this.$emit('show-alert', error.message, 'error')
			});
		},
		deleteAppointment() {
			this.$call('frappe.client.delete', {doctype: 'Patient Appointment', name: this.selectedRow.name}).then(response => {
				this.$toast.add({
					severity: 'success',
					summary: 'Success',
					detail: 'Appointment deleted',
					life: 3000 // Duration in ms
				});
			}).catch(error => {
				this.$emit('show-alert', error.message, 'error')
			});
		},
		updateStatus(item) {
			this.$call('healthcare_doworks.api.methods.change_status',
				{docname: this.selectedRow.name, status: item.label}
			).then(response => {
				this.$toast.add({
					severity: 'success',
					summary: 'Success',
					detail: 'Appointment status changed',
					life: 3000 // Duration in ms
				});
			}).catch(error => {
				this.$emit('show-alert', error.message, 'error')
			});
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
		appointmentRowClass(data) {
            return [{ '!bg-rose-50 hover:!bg-rose-100': data.custom_confirmed == 0 && (this.tab == 'scheduled' || this.tab == 'no show')}];
        },
		noteRowClass(data) {
            return [{ '!bg-yellow-100 hover:!bg-yellow-200': data.read}];
        },
		updateSeen(data) {
			this.$call('healthcare_doworks.api.general_methods.modify_child_entry', {
				parent_doctype: 'Patient Appointment', 
				parent_doc_name: this.selectedRow.name, 
				child_table_fieldname: 'custom_visit_notes', 
				filters: {name: data.name}, 
				update_data: {read: !data.read}
			}).then(response => {
				this.$toast.add({
					severity: 'success',
					summary: 'Success',
					detail: 'Note updated',
					life: 3000 // Duration in ms
				});
			}).catch(error => {
				this.$emit('show-alert', error.message, 'error')
			});
		},
		pageChanged(props) {
			console.log(props)
		},
	},
};
</script>

<style>
.ant-picker-dropdown,.ant-select-dropdown{
	z-index: 3000;
}
</style>