<template>
	<div class="tab-pane" :id="tab + '-appointments'">
		<div class="card">
			<DataTable
				v-model:filters="filters"
				size="small"
				sortField="appointment_time"
				paginator
				stripedRows
				dataKey="id"
				filterDisplay="row"
				resizableColumns
				:loading="loading"
				:sortOrder="1"
				:rows="10"
				:rowsPerPageOptions="[10, 20, 50]"
				:value="appointments"
				@row-contextmenu="handleRowContextMenu"
			>
				<template #empty> No Appointments found. </template>
				<template #loading> Loading Appointments data. Please wait.</template>
				<Column field="patient_cpr" header="Patient" :showFilterMenu="false" :showClearButton="false" style="width: 20%">
					<template #body="{ data }">
						<!-- <router-link to="patient-profile"> -->
							<div class="d-flex align-items-center gap-2">
								<v-avatar :color="!data.patient_details.image ? currentColor : ''">
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
				<Column header="Time" field="appointment_time" :showFilterMenu="false" :showClearButton="false" filterField="appointment_time_moment" style="width: 10%">
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
				<Column field="status" header="Status" :showFilterMenu="false" :showClearButton="false" style="width: 10%">
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
				<Column header="Mobile" field="mobile" :showFilterMenu="false" :showClearButton="false" style="width: 10%">
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
				<Column header="Practitioner" field="practitioner_name" filterField="practitioner_name" :showFilterMenu="false" :showClearButton="false" style="width: 20%">
					<template #body="{ data }">
						<div class="d-flex align-items-center gap-2">
							<v-avatar :color="!data.practitioner_image ? colorCache[data.practitioner_name] || '': ''">
								<img
									v-if="data.practitioner_image"
									class="h-100 w-100"
									:src="data.practitioner_image"
								/>
								<span v-if="!data.practitioner_image" class="text-h6">{{ getInitials(data.practitioner_name) }}</span>
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
						:options="$resources.practitioners"
						:fieldNames="{label: 'practitioner_name', value: 'practitioner_name'}"
						>
							<template #option="{ practitioner_name, image }">
								<v-avatar size="25" :color="!image ? colorCache[practitioner_name] : ''">
									<img
										v-if="image"
										class="h-100 w-100"
										:src="image"
									/>
									<span v-if="!image" style="font-size: small;">{{ getInitials(practitioner_name) }}</span>
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
										<span v-if="!option.image" style="font-size: xx-small;">{{ getInitials(option.practitioner_name) }}</span>
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
				<Column field="appointment_type" header="For" :showFilterMenu="false" :showClearButton="false" style="width: 10%">
					<template #body="{ data }">
						<v-chip class="ma-2" label size="small">{{ data.appointment_type }}</v-chip>
					</template>
					<template #filter="{ filterModel, filterCallback }">
						<a-select
							v-model:value="filterModel.value"
							@change="(filterCallback())"
							class="p-column-filter"
							style="width: 100%; align-items: center;"
							placeholder="Any"
							:options="purposes"
							allowClear
						>
							<template #option="{ value: val }">
								<v-chip class="ma-2" label size="small">{{ val }}</v-chip>
							</template>
						</a-select>
					</template>
				</Column>
				<Column style="width: 5%">
					<template #body="{ data }">
						<v-btn size="small" variant="text" icon>
							<!-- <img :src="bellImage"/> -->
							<i class="mdi mdi-bell-outline" style="font-size: 25px;"></i>
							<div class="zzz zzz-zzz">Z</div>
							<div class="zzz zzz-zz">Z</div>
							<div class="zzz zzz-z">Z</div>
						</v-btn>
					</template>
				</Column>
				<ContextMenu ref="menu" :model="contextItems" @hide="selectedRow = null"/>
			</DataTable>
		</div>
	</div>
</template>

<script >
import colors from '@/assets/json/colors.json';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import ContextMenu from 'primevue/contextmenu';
import { FilterMatchMode } from 'primevue/api';

import { VBtn } from 'vuetify/components/VBtn'
import { VAvatar } from 'vuetify/components/VAvatar';
import { VChip } from 'vuetify/components/VChip';
import { VListItem } from 'vuetify/components/VList';

import bellImage from '@/assets/img/animations/alarm.gif';
import maleImage from '@/assets/img/male.png';
import femaleImage from '@/assets/img/female.png';

export default {
	inject: ['$call'],
	components: {
		DataTable, Column, ContextMenu, VBtn, VAvatar, VChip, VListItem,
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
		selectedDepartments: {
			default: []
		},
		loading: {
			type: Boolean,
			defaul: true
		}
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
				appointment_date: { value: null, matchMode: FilterMatchMode.EQUALS },
				appointment_type: { value: null, matchMode: FilterMatchMode.EQUALS },
				status: { value: null, matchMode: FilterMatchMode.EQUALS },
				mobile: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
			},
			statuses: [{label: 'Scheduled', value: 'Scheduled'}, {label: 'Rescheduled', value: 'Rescheduled'}, {label: 'Walked In', value: 'Walked In'}],
			purposes: [{label: 'General', value: 'General'}, {label: 'Follow-up', value: 'Follow-up'}, {label: 'Consultation', value: 'Consultation'}],
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
						{label: 'Arrived', command: ({ item }) => this.updateStatus(item)},
						{label: 'Ready', command: ({ item }) => this.updateStatus(item)},
						{label: 'In Room', command: ({ item }) => this.updateStatus(item)},
						{label: 'Completed', command: ({ item }) => this.updateStatus(item)},
						{label: 'Transferred', command: ({ item }) => this.updateStatus(item)},
					]
				},
				{separator: true},
				{
					label: 'Reschedule Appointment',
					icon: 'mdi mdi-pulse',
					command: () => this.$emit('appointment-dialog', 'Reschedule Appointment', false, this.selectedRow)
				},
				{
					label: 'Add CPR Reading',
					icon: 'mdi mdi-card-account-details-outline',
					disabled: true
				},
				{
					label: 'Vital Signs',
					icon: 'mdi mdi-update',
				},
				{
					label: 'Update Room',
					icon: 'mdi mdi-door-open'
				},
				{
					label: 'Update Payment Type',
					icon: 'pi pi-wallet',
					disabled: true
				},
				{
					label: 'Patient Encounter',
					icon: 'mdi mdi-bandage',
				},
				{
					label: 'Required Service',
					icon: 'mdi mdi-needle'
				},
            ],
			colorCache: {},
		};
	},
	watch: {
		'$resources.practitioners': {
			handler(newValue) {
				if(newValue)
					newValue.forEach(value => {
						if(!this.colorCache[value.practitioner_name])
							this.colorCache[value.practitioner_name] = this.randomColors()
					})
			},
			immediate: true,
		},
		searchValue() {
			this.filters['global'].value = this.searchValue
		},
		selectedDepartments() {
			this.filters['department'].value = this.selectedDepartments
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
		getInitials(name) {
			let names = name.split(' '),
				initials = names[0].substring(0, 1).toUpperCase();
			
			if (names.length > 1) {
				initials += names[names.length - 1].substring(0, 1).toUpperCase();
			}
			return initials;
		},
		updateStatus(item) {
			this.$call('frappe.client.set_value',
				{doctype: 'Patient Appointment', name: this.selectedRow.appointment_id, fieldname: 'custom_visit_status', value: item.label}
			)
		},
	},
};
</script>

<style>
.ant-picker-dropdown,.ant-select-dropdown{
	z-index: 3000;
}
</style>

<style scoped>
.zzz {
    animation-name: zzz;
    animation-duration: 1.5s;
    animation-timing-function: ease-out;
    animation-iteration-count: infinite;
    animation-direction: forwards;
    color: rgba(160,84,246,1);
    font-weight: bold;
    position: absolute;
    z-index: 100;
    transform: translateY(0%);
    font-family: 'Concert One', cursive;
}

.zzz-z {
    animation-delay: 0s;
    right: 10px;
}
.zzz-zz {
    animation-delay: 0.35s;
    right: 2.5px;
}
.zzz-zzz {
    animation-delay: 0.75s;
    right: 5;
}

@-webkit-keyframes zzz {
	0% {
        color: rgba(160,84,246,0);
        font-size: 5px;
        -webkit-transform: translateY(0%);
        transform: translateY(0%);
    }
    100% {
        color: rgba(160,84,246,1);
        font-size: 15px;
        -webkit-transform: translateY(-150%);
        transform: translateY(-150%);
    }
}

@keyframes zzz {
    0% {
        color: rgba(160,84,246,0);
        font-size: 5px;
        -webkit-transform: translateY(0%);
        transform: translateY(0%);
    }
    100% {
        color: rgba(160,84,246,1);
        font-size: 15px;
        -webkit-transform: translateY(-150%);
        transform: translateY(-150%);
    }
}
</style>