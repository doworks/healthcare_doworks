<template>
	<div :class="{'active' : tab === 'scheduled', ' tab-pane show' : true}" :id="tab + '-appointments'">
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
				:bodyRow="{'name': 'onImageRightClick'}"
				@row-contextmenu="handleRowContextMenu"
			>
				<template #empty> No Appointments found. </template>
				<template #loading> Loading Appointments data. Please wait.</template>
				<Column field="patient_cpr" header="Patient" :showFilterMenu="false" style="width: 20%">
					<template #body="{ data }">
						<!-- <router-link to="patient-profile"> -->
							<img
							class="float-start avatar-img rounded-circle avatar avatar-sm me-2 "
							:src="data.image"
							:alt="data.patient_name"
							/>
							<div class="float-start position-relative vstack">
								{{ data.patient_name }}
								<span class="fw-light text-secondary position-absolute ms-3 top-100" style="font-size: smaller">{{ data.cpr }}</span>
							</div><br/>

						<!-- </router-link> -->
					</template>
					<template #filter="{ filterModel, filterCallback }">
						<InputText 
							v-model="filterModel.value" 
							type="text" 
							@input="filterCallback()" 
							class="p-column-filter" 
							style="height: 35px; align-items: center;"
							placeholder="Search by Patient" 
						/>
					</template>
				</Column>
				<Column header="Time" field="appointment_time" :showFilterMenu="false" filterField="appointment_time_moment" style="width: 10%">
					<template #body="{ data }">
						{{ data.appointment_time_moment }}
					</template>
					<template #filter="{ filterModel, filterCallback }">
						<InputText 
							v-model="filterModel.value" 
							type="text" 
							@input="filterCallback()" 
							class="p-column-filter"
							style="height: 35px; align-items: center;"
							placeholder="Search by Time" 
						/>
					</template>
				</Column>
				<Column field="status" header="Status" :showFilterMenu="false"  style="width: 10%">
					<template #body="{ data }">
						<Tag :value="data.status" :severity="getSeverity(data.status)" />
					</template>
					<template #filter="{ filterModel, filterCallback }">
						<Dropdown
							v-model="filterModel.value"
							@change="filterCallback()"
							:options="statuses" 
							placeholder="Any" 
							class="p-column-filter"
							style="height: 35px; align-items: center;"
							:showClear="true"
						>
							<template #option="slotProps">
								<Tag :value="slotProps.option" :severity="getSeverity(slotProps.option)" />
							</template>
						</Dropdown>
					</template>
				</Column>
				<Column header="Mobile" field="mobile" :showFilterMenu="false" style="width: 10%">
					<template #body="{ data }">
						{{ data.mobile }}
					</template>
					<template #filter="{ filterModel, filterCallback }">
						<InputText 
							size="small" 
							v-model="filterModel.value" 
							type="text" 
							@input="filterCallback()" 
							class="p-column-filter" 
							style="height: 35px; align-items: center;"
							placeholder="Search by Mobile" />
					</template>
				</Column>
				<Column header="Practitioner" field="practitioner_name" filterField="practitioner_name" :showFilterMenu="false"  style="width: 20%">
					<template #body="{ data }">
						<div class="d-flex align-items-center gap-2">
							<img
								class="avatar-img rounded-circle avatar avatar-sm me-2"
								:src="data.practitioner_image"
								:alt="data.practitioner_name"
								style="width: 40px"
							/>
							<span>{{ data.practitioner_name }}</span>
						</div>
					</template>
					<template #filter="{ filterModel, filterCallback }">
						<MultiSelect
							filter
							v-model="filterModel.value"
							@change="filterCallback()"
							optionLabel="name"
							placeholder="Any Practitioner"
							class="p-column-filter"
							style="height: 35px; align-items: center;"
							:maxSelectedLabels="2"
							:options="representatives"
							optionValue="name"
						>
							<template #option="slotProps">
								<div class="d-flex align-items-center gap-2">
									<!-- <img
										class="avatar-img rounded-circle avatar avatar-sm me-2"
										:src="slotProps.option.image"
										:alt="slotProps.option.name"
										style="width: 32px; height: 32px"
									/> -->
									<img :alt="slotProps.option.name" :src="`https://primefaces.org/cdn/primevue/images/avatar/${slotProps.option.image}`" style="width: 32px" />
									<span>{{ slotProps.option.name }}</span>
								</div>
							</template>
						</MultiSelect>
					</template>
				</Column>
				<Column field="department" hidden :showFilterMenu="false">
					<template #filter="{ filterModel, filterCallback }">
						<MultiSelect
							v-model="filterModel.value"
							@change="filterCallback()"
							class="p-column-filter"
							style="height: 35px; align-items: center;"
						/>
					</template>
				</Column>
				<Column field="appointment_type" header="For" :showFilterMenu="false"  style="width: 10%">
					<template #body="{ data }">
						<Tag :value="data.appointment_type" severity="secondary" />
					</template>
					<template #filter="{ filterModel, filterCallback }">
						<Dropdown 
							v-model="filterModel.value" 
							@change="filterCallback()" 
							:options="purposes" 
							placeholder="Any" 
							class="p-column-filter" 
							style="height: 35px; align-items: center;"
							:showClear="true"
						>
							<template #option="slotProps">
								<Tag :value="slotProps.option" severity="secondary" />
							</template>
						</Dropdown>
					</template>
				</Column>
				<!-- <Column field="actions" frozen alignFrozen="right" style="width: 20%">
					<template #body="{ data }">
						<div class="p-buttonset" v-if="this.tab == 'scheduled'">
							<SplitButton
								label="Arrived"
								:model="scheduledStatusOptions"
								@click="save"
								:buttonProps="{style:{'padding': '.25rem .5rem', 'font-size': '.85rem'}}"
								:menuButtonProps="{style:{
									padding: '.25rem .5rem',
									'font-size': '.85rem',
									width: 'auto',
									'border-top-right-radius': 0,
									'border-bottom-right-radius': 0,
								}}"
							/>
							<Button severity="info" icon="pi pi-comment" type="button" label="Notes" badge="2" style="padding: .25rem .5rem; font-size: .85rem; border-radius: 0"/>
							<Button severity="warning" type="button" label="Room" style="padding: .25rem .5rem; font-size: .85rem"/>

							<Button
								severity="secondary"
								type="button"
								icon="pi pi-ellipsis-v"
								@click="toggleActions"
								aria-haspopup="true"
								:aria-controls="'scheduledActionsMenu'"
								style="padding: .25rem .2rem; width: auto; font-size: .85rem"
							/>
							<Menu ref="menu" :key="data.name" :id="'scheduledActionsMenu'" :model="scheduledActionsOptions" :popup="true" />
						</div>
						<div class="p-buttonset" v-if="this.tab == 'arrived'">
							<SplitButton
								label="Ready"
								:model="arrivedStatusOptions"
								@click="save"
								:buttonProps="{style:{'padding': '.25rem .5rem', 'font-size': '.85rem'}}"
								:menuButtonProps="{style:{
									padding: '.25rem .5rem',
									'font-size': '.85rem',
									width: 'auto',
									'border-top-right-radius': 0,
									'border-bottom-right-radius': 0,
								}}"
							/>
							<Button severity="info" icon="pi pi-comment" type="button" label="Notes" badge="2" style="padding: .25rem .5rem; font-size: .85rem; border-radius: 0"/>
							<Button severity="help" type="button" label="Vital Signs" style="padding: .25rem .5rem; font-size: .85rem"/>

							<Button
								severity="secondary"
								type="button"
								icon="pi pi-ellipsis-v"
								@click="toggleActions"
								aria-haspopup="true"
								:aria-controls="'arrivedActionsMenu'"
								style="padding: .25rem .2rem; width: auto; font-size: .85rem"
							/>
							<Menu ref="menu" :key="data.name" :id="'arrivedActionsMenu'" :model="arrivedActionsOptions" :popup="true" />
						</div>
						<div class="p-buttonset" v-if="this.tab == 'ready'">
							<SplitButton
								label="In Room"
								:model="readyStatusOptions"
								@click="save"
								:buttonProps="{style:{'padding': '.25rem .5rem', 'font-size': '.85rem'}}"
								:menuButtonProps="{style:{
									padding: '.25rem .5rem',
									'font-size': '.85rem',
									width: 'auto',
									'border-top-right-radius': 0,
									'border-bottom-right-radius': 0,
								}}"
							/>
							<Button severity="info" icon="pi pi-comment" type="button" label="Notes" badge="2" style="padding: .25rem .5rem; font-size: .85rem; border-radius: 0"/>
							<Button severity="help" type="button" label="Vital Signs" style="padding: .25rem .5rem; font-size: .85rem"/>

							<Button
								severity="secondary"
								type="button"
								icon="pi pi-ellipsis-v"
								@click="toggleActions"
								aria-haspopup="true"
								:aria-controls="'readyActionsMenu'"
								style="padding: .25rem .2rem; width: auto; font-size: .85rem"
							/>
							<Menu ref="menu" :key="data.name" :id="'readyActionsMenu'" :model="readyActionsOptions" :popup="true" />
						</div>
						<div class="p-buttonset" v-if="this.tab == 'inroom'">
							<SplitButton
								label="Completed"
								:model="inroomStatusOptions"
								@click="save"
								:buttonProps="{style:{'padding': '.25rem .5rem', 'font-size': '.85rem'}}"
								:menuButtonProps="{style:{
										padding: '.25rem .5rem',
										'font-size': '.85rem',
										width: 'auto',
										'border-top-right-radius': 0,
										'border-bottom-right-radius': 0,
									}}"
							/>
							<Button severity="info" type="button" label="Patient Encounter" style="padding: .25rem .5rem; font-size: .85rem; border-radius: 0"/>

							<Button
								severity="secondary"
								type="button"
								icon="pi pi-ellipsis-v"
								@click="toggleActions"
								aria-haspopup="true"
								:aria-controls="'inroomActionsMenu'"
								style="padding: .25rem .2rem; width: auto; font-size: .85rem"
							/>
							<Menu ref="menu" :key="data.name" :id="'inroomActionsMenu'" :model="inroomActionsOptions" :popup="true" />
						</div>
						<div class="p-buttonset" v-if="this.tab == 'completed'">
							<SplitButton
								label="Ready"
								:model="completedStatusOptions"
								@click="save"
								:buttonProps="{style:{'padding': '.25rem .5rem', 'font-size': '.85rem'}}"
								:menuButtonProps="{style:{
									padding: '.25rem .5rem',
									'font-size': '.85rem',
									width: 'auto',
									'border-top-right-radius': 0,
									'border-bottom-right-radius': 0,
								}}"
							/>
							<Button severity="info" type="button" label="Make Payment" style="padding: .25rem .5rem; font-size: .85rem; border-radius: 0"/>
							<Button severity="danger" type="button" label="Bill" style="padding: .25rem .5rem; font-size: .85rem"/>
							<Button severity="secondary" type="button" icon="pi pi-plus" style="padding: .25rem .5rem; font-size: .85rem"/>
						</div>
					</template>
				</Column> -->
				<ContextMenu ref="menu" :model="contextItems" field="actions"/>
				<Column style="width: 5%">
					<template #body="{ data }">
						<v-btn size="small" variant="text" icon="mdi mdi-bell-outline">
							<img :src="bellImage"/>
						</v-btn>
					</template>
				</Column>
			</DataTable>
		</div>
	</div>

</template>

<script >
import Calendar from 'primevue/calendar';
import IconField from 'primevue/iconfield';
import InputIcon from 'primevue/inputicon';
import InputText from 'primevue/inputtext';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import MultiSelect from 'primevue/multiselect';
import Tag from 'primevue/tag';
import Dropdown from 'primevue/dropdown';
import TriStateCheckbox from 'primevue/tristatecheckbox';
import SplitButton from 'primevue/splitbutton';
import Button from 'primevue/button';
import Menu from 'primevue/menu';
import ContextMenu from 'primevue/contextmenu';

import { watchEffect } from 'vue';
import { FilterMatchMode } from 'primevue/api';
import moment from "moment";
import { VBtn } from 'vuetify/components/VBtn'

import bellImage from '@/assets/img/animations/alarm.gif';

export default {
	components: {
		Calendar, IconField, InputIcon, InputText, DataTable, MultiSelect,
		Tag, Dropdown, TriStateCheckbox, Column, SplitButton, Button, Menu,
		ContextMenu, VBtn,
	},
	props: {
		appointment: {
			default: [{
				"name": "HLC-APP-2024-00001",
				"appointment_type": "General",
				"patient_name": "Sayed Mohamed Adnan",
				"mobile": "1234567890",
				"practitioner_name": "Sayed Hassan",
				"cpr": 123576342,
				"department": "Neurology",
				"status": "Scheduled",
				"invoiced": 100,
				"paid_amount": 0,
				"duration": 20,
				"visit_status": "Scheduled",
				"image": "https://randomuser.me/api/portraits/men/1.jpg",
				"practitioner_image": "https://randomuser.me/api/portraits/men/30.jpg",
				"appointment_time": "09:45:00",
				"appointment_date": "2024-02-21"
			}],
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
		}
	},
	data() {
		return {
			bellImage:bellImage,
			appointments: null,
			filters: {
				global: { value: null, matchMode: FilterMatchMode.CONTAINS },
				patient_name: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
				cpr: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
				department: { value: null, matchMode: FilterMatchMode.IN },
				patient_cpr: { value: null, matchMode: FilterMatchMode.CONTAINS },
				practitioner_name: { value: null, matchMode: FilterMatchMode.IN },
				appointment_time: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
				appointment_time_moment: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
				appointment_date: { value: null, matchMode: FilterMatchMode.EQUALS },
				appointment_type: { value: null, matchMode: FilterMatchMode.EQUALS },
				status: { value: null, matchMode: FilterMatchMode.EQUALS },
				mobile: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
			},
			representatives: [
				{ name: 'Mia Lopez', image: 'amyelsner.png' },
				{ name: 'Ella Clark', image: 'annafali.png' },
				{ name: 'Sayed Hassan', image: 'asiyajavayant.png' },
				{ name: 'Emma Wilson', image: 'bernardodominic.png' },
				{ name: 'Elwin Sharvill', image: 'elwinsharvill.png' },
				{ name: 'Ioni Bowcher', image: 'ionibowcher.png' },
				{ name: 'Ivan Magalhaes', image: 'ivanmagalhaes.png' },
				{ name: 'Onyama Limba', image: 'onyamalimba.png' },
				{ name: 'Stephen Shaw', image: 'stephenshaw.png' },
				{ name: 'XuXue Feng', image: 'xuxuefeng.png' }
			],
			statuses: ['Scheduled', 'Rescheduled', 'Walked In'],
			purposes: ['General', 'Follow-up', 'Consultation'],
			loading: true,

			// scheduledStatusOptions: [
			// 	{
			// 		label: 'Ready',
			// 		command: () => {
			// 		}
			// 	},
			// 	{
			// 		label: 'In Room',
			// 		command: () => {
			// 		}
			// 	},
			// 	{
			// 		label: 'Transferred',
			// 		command: () => {
			// 			window.location.href = 'https://vuejs.org/';
			// 		}
			// 	},
			// 	{
			// 		label: 'Completed',
			// 		command: () => {
			// 			window.location.href = 'https://vuejs.org/';
			// 		}
			// 	},
			// ],
			// arrivedStatusOptions: [
			// 	{
			// 		label: 'In Room',
			// 		command: () => {
			// 		}
			// 	},
			// 	{
			// 		label: 'Transferred',
			// 		command: () => {
			// 			window.location.href = 'https://vuejs.org/';
			// 		}
			// 	},
			// 	{
			// 		label: 'Completed',
			// 		command: () => {
			// 			window.location.href = 'https://vuejs.org/';
			// 		}
			// 	},
			// 	{
			// 		label: 'Scheduled',
			// 		command: () => {
			// 		}
			// 	},
			// ],
			// readyStatusOptions: [
			// 	{
			// 		label: 'Transferred',
			// 		command: () => {
			// 			window.location.href = 'https://vuejs.org/';
			// 		}
			// 	},
			// 	{
			// 		label: 'Completed',
			// 		command: () => {
			// 			window.location.href = 'https://vuejs.org/';
			// 		}
			// 	},
			// 	{
			// 		label: 'Scheduled',
			// 		command: () => {
			// 		}
			// 	},
			// 	{
			// 		label: 'Arrived',
			// 		command: () => {
			// 		}
			// 	},
			// ],
			// inroomStatusOptions: [
			// 	{
			// 		label: 'Transferred',
			// 		command: () => {
			// 			window.location.href = 'https://vuejs.org/';
			// 		}
			// 	},
			// 	{
			// 		label: 'Scheduled',
			// 		command: () => {
			// 		}
			// 	},
			// 	{
			// 		label: 'Arrived',
			// 		command: () => {
			// 			window.location.href = 'https://vuejs.org/';
			// 		}
			// 	},
			// 	{
			// 		label: 'Ready',
			// 		command: () => {
			// 		}
			// 	},
			// ],
			// completedStatusOptions: [
			// 	{
			// 		label: 'Transferred',
			// 		command: () => {
			// 			window.location.href = 'https://vuejs.org/';
			// 		}
			// 	},
			// 	{
			// 		label: 'Scheduled',
			// 		command: () => {
			// 		}
			// 	},
			// 	{
			// 		label: 'Arrived',
			// 		command: () => {
			// 			window.location.href = 'https://vuejs.org/';
			// 		}
			// 	},
			// 	{
			// 		label: 'In Room',
			// 		command: () => {
			// 		}
			// 	},
			// ],

			scheduledActionsOptions: [
				{
					label: 'Reschedule Appointment',
					icon: 'pi pi-history'
				},
				{
					label: 'Add CPR Reading',
					icon: 'pi pi-id-card'
				},
				{
					label: 'Update Payment Type',
					icon: 'pi pi-wallet'
				},
			],
			arrivedActionsOptions: [
				{
					label: 'Update Room',
					icon: 'pi pi-window-maximize'
				},
				{
					label: 'Add CPR Reading',
					icon: 'pi pi-id-card'
				},
				{
					label: 'Update Payment Type',
					icon: 'pi pi-wallet'
				},
			],
			readyActionsOptions: [
				{
					label: 'Patient Encounter',
					icon: 'pi pi-users'
				},
				{
					label: 'Add CPR Reading',
					icon: 'pi pi-id-card'
				},
				{
					label: 'Update Payment Type',
					icon: 'pi pi-wallet'
				},
			],
			inroomActionsOptions: [
				{
					label: 'Required Service',
					icon: 'pi pi-file-edit'
				},
				{
					label: 'Bill',
					icon: 'pi pi-money-bill'
				},
				{
					label: 'Update Payment Type',
					icon: 'pi pi-wallet'
				},
				{
					label: 'New Appointment',
					icon: 'pi pi-users'
				},
			],
			contextItems: [
				{
					label: 'Status',
					icon: 'mdi mdi-clipboard-edit-outline',
					items: [
						{
							label: 'Arrived',
							command: (e) => {
								console.log(e)
							}
						},
						{
							label: 'Ready',
							command: () => {
								selectedUser.value.role = 'Member';
							}
						},
						{
							label: 'In Room',
							command: () => {
								selectedUser.value.role = 'Member';
							}
						},
						{
							label: 'Completed',
							command: () => {
								selectedUser.value.role = 'Member';
							}
						},
						{
							label: 'Transferred',
							command: () => {
								selectedUser.value.role = 'Member';
							}
						},
					]
				},
				{
					separator: true
				},
				{
                    label: 'Favorite',
                    icon: 'pi pi-star',
                    shortcut: '⌘+D'
                },
                {
                    label: 'Add',
                    icon: 'pi pi-shopping-cart',
                    shortcut: '⌘+A'
                },
            ]
		};
	},
	created() {
		watchEffect(() => {
			this.appointments = this.getAppointments(this.appointment)
			this.loading = false;
			this.filters['global'].value = this.searchValue
			this.filters['department'].value = this.selectedDepartments
		})
	},
	mounted() {
	},
	methods: {
		getAppointments(data) {
			return [...(data || [])].map((d) => {
				d.appointment_time_moment = moment(d.appointment_date + ' ' + d.appointment_time).format('LT');
				d.patient_cpr = d.patient_name + ' ' + d.cpr

				return d;
			});
		},
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
		save() {
		},
		toggleActions(event) {
			this.$refs.menu.toggle(event);
		},
		handleRowContextMenu({ originalEvent, data, index }) {
			this.$refs.menu.show(originalEvent);
		}
	},
};
</script>