<!-- <template>
    <div :class="tab === 'scheduled' ? 'tab-pane show active' : 'tab-pane show'" :id="tab + '-appointments'">
        <div class="card card-table mb-0">
        <div class="card-body">
            <div class="table-responsive">
                <table class="table table-hover table-center mb-0">
                    <thead>
                    <tr></tr>
                    <tr>
                        <th>Patient Name</th>
                        <th>Appt Date</th>
                        <th>Purpose</th>
                        <th>Type</th>
                        <th class="text-center">Paid Amount</th>
                        <th></th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr v-for="item in appointment" :key="item.id">
                        <td>
                        <h2 class="table-avatar">
                            <router-link
                            to="patient-profile"
                            class="avatar avatar-sm me-2"
                            ><img
                                class="avatar-img rounded-circle"
                                :src="
                                require(`@/assets/img/patients/${item.Image}`)
                                "
                                alt="User Image"
                            /></router-link>
                            <router-link to="patient-profile"
                            >{{ item.PatientName }}
                            <span>{{ item.PatientId }}</span></router-link
                            >
                        </h2>
                        </td>
                        <td>
                        {{ item.ApptDate }}
                        <span class="d-block text-info">{{
                            item.ApptTime
                        }}</span>
                        </td>
                        <td>{{ item.Purpose }}</td>
                        <td>{{ item.Type }}</td>
                        <td class="text-center">{{ item.PaidAmount }}</td>
                        <td class="text-end">
                        <div class="table-action">
                            <a
                            href="javascript:void(0);"
                            class="btn btn-sm bg-info-light me-2"
                            >
                            <i class="far fa-eye"></i> View
                            </a>

                            <a
                            href="javascript:void(0);"
                            class="btn btn-sm bg-success-light me-2"
                            >
                            <i class="fas fa-check"></i> Accept
                            </a>
                            <a
                            href="javascript:void(0);"
                            class="btn btn-sm bg-danger-light"
                            >
                            <i class="fas fa-times"></i> Cancel
                            </a>
                        </div>
                        </td>
                    </tr>
                    </tbody>
                </table>
            </div>
        </div>
        </div>
    </div>
</template>

<script>
import { arrayType, stringType } from 'ant-design-vue/es/_util/type';

export default {
    props: {
        appointment: {
            default: [{
                "PatientName": "Richard Wilson",
                "PatientId": " #PT0016",
                "ApptDate": "11 Nov 2023",
                "ApptTime": "10.00 AM",
                "Purpose": "General",
                "Type": "New Patient",
                "PaidAmount": "$150",
                "Image": "patient.jpg"
            }],
        },
        tab:{
            type: String,
            default: 'scheduled'
        }
    }  
}
</script> -->

<template>
    <div class="card">
        <DataTable v-model:filters="filters" :value="customers" dataKey="id" filterDisplay="row" :loading="loading"
                >
            <template #header>
                <div class="flex justify-content-end">
                    <IconField iconPosition="left">
                        <InputIcon>
                            <i class="pi pi-search" />
                        </InputIcon>
                        <InputText v-model="filters['global'].value" placeholder="Keyword Search" />
                    </IconField>
                </div>
            </template>
            <template #empty> No customers found. </template>
            <template #loading> Loading customers data. Please wait. </template>
            <Column field="PatientName" header="Patient Name" style="min-width: 12rem">
                <template #body="{ data }">
                    {{ data.PatientName }}
                </template>
                <template #filter="{ filterModel, filterCallback }">
                    <InputText v-model="filterModel.value" type="text" @input="filterCallback()" class="p-column-filter" placeholder="Search by name" />
                </template>
            </Column>
            <!-- <Column header="Appt Date" filterField="ApptDate" style="min-width: 12rem">
                <template #body="{ data }">
                    <div class="flex align-items-center gap-2">
                        <img alt="flag" src="https://primefaces.org/cdn/primevue/images/flag/flag_placeholder.png" :class="`flag flag-${data.country.code}`" style="width: 24px" />
                        <span>{{ data.ApptDate }}</span>
                    </div>
                </template>
                <template #filter="{ filterModel, filterCallback }">
                    <InputText v-model="filterModel.value" type="text" @input="filterCallback()" class="p-column-filter" placeholder="Search by country" />
                </template>
            </Column>
            <Column header="Agent" filterField="representative" :showFilterMenu="false" :filterMenuStyle="{ width: '14rem' }" style="min-width: 14rem">
                <template #body="{ data }">
                    <div class="flex align-items-center gap-2">
                        <img :alt="data.representative.name" :src="`https://primefaces.org/cdn/primevue/images/avatar/${data.representative.image}`" style="width: 32px" />
                        <span>{{ data.representative.name }}</span>
                    </div>
                </template>
                <template #filter="{ filterModel, filterCallback }">
                    <MultiSelect v-model="filterModel.value" @change="filterCallback()" :options="representatives" optionLabel="name" placeholder="Any" class="p-column-filter" style="min-width: 14rem" :maxSelectedLabels="1">
                        <template #option="slotProps">
                            <div class="flex align-items-center gap-2">
                                <img :alt="slotProps.option.name" :src="`https://primefaces.org/cdn/primevue/images/avatar/${slotProps.option.image}`" style="width: 32px" />
                                <span>{{ slotProps.option.name }}</span>
                            </div>
                        </template>
                    </MultiSelect>
                </template>
            </Column>
            <Column field="status" header="Status" :showFilterMenu="false" :filterMenuStyle="{ width: '14rem' }" style="min-width: 12rem">
                <template #body="{ data }">
                    <Tag :value="data.status" :severity="getSeverity(data.status)" />
                </template>
                <template #filter="{ filterModel, filterCallback }">
                    <Dropdown v-model="filterModel.value" @change="filterCallback()" :options="statuses" placeholder="Select One" class="p-column-filter" style="min-width: 12rem" :showClear="true">
                        <template #option="slotProps">
                            <Tag :value="slotProps.option" :severity="getSeverity(slotProps.option)" />
                        </template>
                    </Dropdown>
                </template>
            </Column>
            <Column field="verified" header="Verified" dataType="boolean" style="min-width: 6rem">
                <template #body="{ data }">
                    <i class="pi" :class="{ 'pi-check-circle text-green-500': data.verified, 'pi-times-circle text-red-400': !data.verified }"></i>
                </template>
                <template #filter="{ filterModel, filterCallback }">
                    <TriStateCheckbox v-model="filterModel.value" @change="filterCallback()" />
                </template>
            </Column> -->
        </DataTable>
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

import { ref, onMounted } from 'vue';
import { FilterMatchMode } from 'primevue/api';
import { props } from 'vue3-tags-input';

export default {
    components: {
        Calendar,
        IconField,
        InputIcon,
        InputText,
        DataTable,
        MultiSelect,
        Tag,
        Dropdown,
        TriStateCheckbox,
        Column,
    },
    props: {
        appointment: {
            default: [{
                "PatientName": "Richard Wilson",
                "PatientId": " #PT0016",
                "ApptDate": "11 Nov 2023",
                "ApptTime": "10.00 AM",
                "Purpose": "General",
                "Type": "New Patient",
                "PaidAmount": "$150",
                "Image": "patient.jpg"
            }],
        },
        tab:{
            type: String,
            default: 'scheduled'
        }
    },
    data() {
        return {
            customers: null,
            filters: {
                global: { value: null, matchMode: FilterMatchMode.CONTAINS },
                PatientName: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
                ApptDate: { value: null, matchMode: FilterMatchMode.STARTS_WITH },
                Purpose: { value: null, matchMode: FilterMatchMode.IN },
                Type: { value: null, matchMode: FilterMatchMode.EQUALS },
                ApptTime: { value: null, matchMode: FilterMatchMode.EQUALS }
            },
            representatives: [
                { name: 'Amy Elsner', image: 'amyelsner.png' },
                { name: 'Anna Fali', image: 'annafali.png' },
                { name: 'Asiya Javayant', image: 'asiyajavayant.png' },
                { name: 'Bernardo Dominic', image: 'bernardodominic.png' },
                { name: 'Elwin Sharvill', image: 'elwinsharvill.png' },
                { name: 'Ioni Bowcher', image: 'ionibowcher.png' },
                { name: 'Ivan Magalhaes', image: 'ivanmagalhaes.png' },
                { name: 'Onyama Limba', image: 'onyamalimba.png' },
                { name: 'Stephen Shaw', image: 'stephenshaw.png' },
                { name: 'XuXue Feng', image: 'xuxuefeng.png' }
            ],
            statuses: ['unqualified', 'qualified', 'new', 'negotiation', 'renewal', 'proposal'],
            loading: true
        };
    },
    mounted() {
        this.customers = this.getCustomers(this.appointment)
        console.log(this.customers)
        this.loading = false;
    },
    methods: {
        getCustomers(data) {
            return [...(data || [])].map((d) => {
                d.ApptDate = new Date(d.ApptDate);

                return d;
            });
        },
        formatDate(value) {
            return value.toLocaleDateString('en-US', {
                day: '2-digit',
                month: '2-digit',
                year: 'numeric'
            });
        },
        formatCurrency(value) {
            return value.toLocaleString('en-US', { style: 'currency', currency: 'USD' });
        },
        getSeverity(status) {
            switch (status) {
                case 'unqualified':
                    return 'danger';

                case 'qualified':
                    return 'success';

                case 'new':
                    return 'info';

                case 'negotiation':
                    return 'warning';

                case 'renewal':
                    return null;
            }
        }
    }
};
</script>