<template>
    <v-dialog v-model="dialogVisible" width="auto" scrollable>
      <v-card rounded="lg">
        <a-form layout="vertical" :model="form" :rules="rules">
          <v-card-title class="d-flex justify-space-between align-center">
            <div class="text-h5 text-medium-emphasis ps-2">Service Request</div>
            <v-btn icon="mdi mdi-close" variant="text" @click="closeDialog"></v-btn>
          </v-card-title>
          <v-divider class="m-0"></v-divider>
          <v-card-text>
            <v-container>
              <v-row>
                <v-col cols="12" md="6">
                  <a-form-item label="Order Date" name="order_date">
                    <a-date-picker 
                      v-model:value="form.order_date"
                      format="DD/MM/YYYY" 
                      style="z-index: 3000; width: 100%;"
                    />
                  </a-form-item>
                  <a-form-item label="Order Time" name="order_time">
                    <a-time-picker v-model:value="form.order_time" use12-hours format="h:mm a" style="z-index: 3000; width: 100%;"/>
                  </a-form-item>
                </v-col>
                <v-col cols="12" md="6">
                  <a-form-item label="Status" name="status">
                    <a-select
                    v-model:value="form.status"
                    :fieldNames="{label: 'display', value: 'name'}"
                    :options="$resources.codeValues.data.filter(item => item.code_system === 'Request Status')"
                    style="width: 100%"
                    ></a-select>
                  </a-form-item>
                  <a-form-item label="Expected By" name="expected_date">
                    <a-date-picker 
                      v-model:value="form.expected_date"
                      format="DD/MM/YYYY" 
                      style="z-index: 3000; width: 100%;"
                    />
                  </a-form-item>
                </v-col>
              </v-row>
              <v-divider class="mt-2 mb-8"></v-divider>
              <h4 class="mb-4">Order Source</h4>
              <v-row>
                <v-col cols="12" md="6">
                  <a-form-item label="Ordered by Practitioner" name="practitioner">
                    <a-select
                    v-model:value="form.practitioner"
                    :options="$resources.practitioners.data"
                    :fieldNames="{label: 'practitioner_name', value: 'name'}"
                    style="width: 100%"
                    ></a-select>
                  </a-form-item>
                  <a-form-item label="Practitioner Email" name="practitioner_email" :class="{'d-none': !form.practitioner || !form.practitioner_email}">
                    <a-input v-model:value="form.practitioner_email" disabled/>
                  </a-form-item>
                  <a-form-item label="Medical Department" name="medical_department" :class="{'d-none': !form.practitioner || !form.medical_department}">
                    <a-input v-model:value="form.medical_department" disabled/>
                  </a-form-item>
                  <a-form-item label="Referred to Practitioner" name="referred_to_practitioner">
                    <a-select
                    v-model:value="form.referred_to_practitioner"
                    :options="$resources.practitioners.data"
                    :fieldNames="{label: 'practitioner_name', value: 'name'}"
                    style="width: 100%"
                    ></a-select>
                  </a-form-item>
                </v-col>
                <v-col cols="12" md="6">
                  <a-form-item label="Source Doc" name="source_doc">
                    <a-input v-model:value="form.source_doc" disabled/>
                  </a-form-item>
                  <a-form-item label="Source Doc" name="order_group">
                    <a-input v-model:value="form.order_group" disabled/>
                  </a-form-item>
                  <a-form-item label="Sequence in Order Group" name="sequence">
                    <a-input v-model:value="form.sequence"/>
                  </a-form-item>
                </v-col>
              </v-row>
              <v-divider class="mt-2 mb-8"></v-divider>
              <h4 class="mb-4">Order Details</h4>
              <v-row>
                <v-col cols="12" md="6">
                  <a-form-item label="Staff Role" name="staff_role" extra="The role responsible for performing the service">
                    <a-select
                    v-model:value="form.staff_role"
                    :options="$resources.roles.data"
                    :fieldNames="{label: 'name', value: 'name'}"
                    style="width: 100%"
                    ></a-select>
                  </a-form-item>
                  <a-form-item label="Patient Care Type" name="patient_care_type">
                    <a-select
                    v-model:value="form.patient_care_type"
                    :options="$resources.patientCareTypes.data"
                    :fieldNames="{label: 'name', value: 'name'}"
                    style="width: 100%"
                    ></a-select>
                  </a-form-item>
                </v-col>
                <v-col cols="12" md="6">
                  <a-form-item label="Intent" name="intent" extra=" ">
                    <a-select
                    v-model:value="form.intent"
                    :options="$resources.codeValues.data.filter(item => item.code_system === 'Intent')"
                    :fieldNames="{label: 'display', value: 'name'}"
                    style="width: 100%"
                    ></a-select>
                  </a-form-item>
                  <a-form-item label="Priority" name="priority">
                    <a-select
                    v-model:value="form.priority"
                    :options="$resources.codeValues.data.filter(item => item.code_system === 'Priority')"
                    :fieldNames="{label: 'display', value: 'name'}"
                    style="width: 100%"
                    ></a-select>
                  </a-form-item>
                </v-col>
              </v-row>
              <v-divider class="mt-2 mb-8"></v-divider>
              <h4 class="mb-4">Order Specifications</h4>
              <v-row>
                <v-col cols="12" md="6">
                  <a-form-item label="Quantity" name="quantity">
                    <a-input v-model:value="form.quantity"/>
                  </a-form-item>
                  <a-form-item name="as_needed" :extra="asNeededExtra">
                    <a-checkbox v-model:checked="form.as_needed">Occurrence As Needed</a-checkbox>
                  </a-form-item>
                  <a-form-item label="Occurrence Date" name="occurrence_date" :class="{'d-none': form.as_needed}">
                    <a-date-picker 
                      v-model:value="form.occurrence_date"
                      format="DD/MM/YYYY" 
                      style="z-index: 3000; width: 100%;"
                    />
                  </a-form-item>
                  <a-form-item label="Occurrence Time" name="occurrence_time" :class="{'d-none': form.as_needed}">
                    <a-time-picker v-model:value="form.occurrence_time" use12-hours format="h:mm a" style="z-index: 3000; width: 100%;"/>
                  </a-form-item>
                  <a-form-item label="Healthcare Service Unit Type" name="healthcare_service_unit_type">
                    <a-select
                    v-model:value="form.healthcare_service_unit_type"
                    :options="$resources.serviceUnitTypes.data"
                    :fieldNames="{label: 'name', value: 'name'}"
                    style="width: 100%"
                    @change="setTemplateOptions"
                    ></a-select>
                  </a-form-item>
                </v-col>
                <v-col cols="12" md="6">
                  <a-form-item label="Order Description" name="order_description">
                    <a-textarea v-model:value="form.order_description" :rows="4" />
                  </a-form-item>
                  <a-form-item label="Patient Instructions" name="patient_instructions">
                    <a-textarea v-model:value="form.patient_instructions" :rows="4" />
                  </a-form-item>
                </v-col>
              </v-row>
              <v-divider class="mt-2 mb-8"></v-divider>
              <h4 class="mb-4">Service Details</h4>
              <v-row>
                <v-col cols="12" md="6">
                  <a-form-item label="Order Template Type" name="template_dt">
                    <a-select
                    v-model:value="form.template_dt"
                    :options="template_dt_options"
                    style="width: 100%"
                    @change="setTemplateOptions"
                    ></a-select>
                  </a-form-item>
                  <a-form-item label="Order Template" name="template_dn">
                    <a-select
                    v-model:value="form.template_dn"
                    :options="template_dn_options"
                    :fieldNames="{label: 'name', value: 'name'}"
                    style="width: 100%"
                    ></a-select>
                  </a-form-item>
                  <a-form-item name="sample_collection_required">
                    <a-checkbox v-model:checked="form.sample_collection_required">Sample Collection Required</a-checkbox>
                  </a-form-item>
                  <a-form-item label="Quantity Invoiced" name="qty_invoiced">
                    <a-input v-model:value="form.qty_invoiced" disabled/>
                  </a-form-item>
                  <a-form-item label="Billing Status" name="billing_status">
                    <a-input v-model:value="form.billing_status" disabled/>
                  </a-form-item>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
          
          <v-divider class="mt-2"></v-divider>
  
          <v-card-actions class="my-2 d-flex justify-end">
            <v-btn
            class="text-none"
            text="Cancel"
            @click="closeDialog"
            ></v-btn>
            <v-btn
            class="text-none"
            color="blue"
            
            text="submit"
            variant="tonal"
            @click="onSubmit()"
            type="submit"
            ></v-btn>
          </v-card-actions>
        </a-form>
      </v-card>
    </v-dialog>
  </template>
    
  <script >
  import dayjs from 'dayjs';
  import { Form } from 'ant-design-vue';
  import { reactive } from 'vue';
  
  import '@vueup/vue-quill/dist/vue-quill.snow.css';
    
  export default {
    inject: ['$call'],
    components: {
      
    },
    props: {
      isOpen: {
        type: Boolean,
        required: true,
        default: false,
      },
      encounter: {
        default: {}
      },
      patient: {
        default: {}
      }
    },
    resources: {
      codeValues() { return { 
        type: 'list', 
        doctype: 'Code Value', 
        fields: ['name', 'display', 'code_system'], 
        auto: true, 
        orderBy: 'display',
        pageLength: 1000,
        cache: 'codeValues'
      }},
      // doctypes() { return { type: 'list', doctype: 'Doctype', fields: ['name'], auto: true, orderBy: 'name', pageLength: 1000,}},
      roles() { return { 
        type: 'list', 
        doctype: 'Role', 
        fields: ['name'], 
        filters:{'restrict_to_domain': 'Healthcare'}, 
        auto: true, 
        orderBy: 'name',
        pageLength: 1000,
        cache: 'roles'
      }},
      patientCareTypes() { return { 
        type: 'list', 
        doctype: 'Patient Care Type', 
        fields: ['name'], 
        auto: true, 
        orderBy: 'name',
        pageLength: 1000,
        cache: 'patientCareTypes'
      }},
      serviceUnitTypes() { return { 
        type: 'list', 
        doctype: 'Healthcare Service Unit Type', 
        fields: ['name'], 
        auto: true, 
        orderBy: 'name',
        pageLength: 1000,
        cache: 'serviceUnitTypes'
      }},

      therapyTypes() { return { 
        type: 'list', 
        doctype: 'Therapy Type', 
        fields: ['name'], 
        auto: true, 
        orderBy: 'name',
        pageLength: 1000,
        cache: 'therapyTypes'
      }},
      labTestTemplates() { return { 
        type: 'list', 
        doctype: 'Lab Test Template', 
        fields: ['name', 'department'], 
        auto: true, 
        orderBy: 'name',
        pageLength: 1000,
        cache: 'labTestTemplates'
      }},
      clinicalProcedureTemplates() { return { 
        type: 'list', 
        doctype: 'Clinical Procedure Template', 
        fields: ['name'], 
        auto: true, 
        orderBy: 'name',
        pageLength: 1000,
        cache: 'clinicalProcedureTemplates'
      }},
      observationTemplate() { return { 
        type: 'list', 
        doctype: 'Observation Template', 
        fields: ['name'], 
        auto: true, 
        orderBy: 'name',
        pageLength: 1000,
        cache: 'observationTemplate'
      }},
      healthcareActivity() { return { 
        type: 'list', 
        doctype: 'Healthcare Activity', 
        fields: ['name'], 
        auto: true, 
        orderBy: 'name',
        pageLength: 1000,
        cache: 'healthcareActivity'
      }},
      appointmentTypes() { return { 
        type: 'list', 
        doctype: 'Appointment Type', 
        fields: ['name', 'appointment_type', 'allow_booking_for', 'default_duration'], 
        auto: true, 
        orderBy: 'appointment_type',
        pageLength: 1000,
        cache: 'appointmentTypes'
      }},
      practitioners() { return { 
        type: 'list', 
        doctype: 'Healthcare Practitioner', 
        fields: ['practitioner_name', 'image', 'department', 'name'], 
        filters: {status: 'Active'},
        auto: true, 
        orderBy: 'practitioner_name',
        pageLength: 1000,
        cache: 'practitioners'
      }},
    },
    computed: {
      dialogVisible: {
        get() {
          return this.isOpen;
        },
        set(value) {
          this.$emit('update:isOpen', value);
        },
      },
      form() {
        return reactive({
          doctype: 'Service Request',

          order_date: dayjs(),
          order_time: dayjs(),
          status: null,
          expected_date: undefined,

          patient: this.patient.name,
          patient_name: this.patient.patient_name,
          patient_gender: this.patient.sex,
          patient_birth_date: this.patient.dob,
          patient_blood_group: this.patient.blood_group,
          patient_email: this.patient.department,
          patient_mobile: this.patient.mobile,
          inpatient_record: this.patient.inpatient_record,
          inpatient_status: this.patient.inpatient_status,

          practitioner: this.$myresources.user.practitioner,
          practitioner_email: this.$myresources.user.user,
          medical_department: this.$myresources.user.practitioner_department,
          referred_to_practitioner: null,
          source_doc: 'Patient Encounter',
          order_group: this.encounter.name,
          sequence: null,

          staff_role: null,
          item_code: null,
          patient_care_type: null,
          intent: null,
          priority: null,

          quantity: null,
          dosage_form: null,
          as_needed: false,
          dosage: null,
          period: null,
          occurrence_date: undefined,
          occurrence_time: undefined,
          order_description: null,
          patient_instructions: null,

          // order_reference_doctype: null,
          // order_reference_name: null,
          // source: false,
          // referring_practitioner: null,
          // reason_reference_doctype: null,
          // reason_reference: null,
          // order_group_doctype: 'Patient Encounter',

          template_dt: null,
          template_dn: null,
          sample_collection_required: false,
          qty_invoiced: 0,
          billing_status: 'Pending',
          auto_repeat: null,
        });
      },
      rules() {
        return reactive({
          order_date: [{ required: true, message: 'Please choose an order date!' }],
          order_time: [{ required: true, message: 'Please choose an order time!' }],
          status: [{ required: true, message: 'Please choose a status!' }],

          patient: [{ required: true, message: 'Please choose a patient!' }],

          practitioner: [{ required: true, message: 'Please choose a practitioner!' }],

          template_dt: [{ required: true, message: 'Please choose an Order Template Type!' }],
          template_dn: [{ required: true, message: 'Please choose an Order Template!' }],
        });
      },
    },
    data() {
      return {
        lodingOverlay: false,
        asNeededExtra: 'Perform the service only if there is a need. For example "pain", "on flare-up", etc.',
        template_dt_options: [
          {label: 'Therapy Type', value: 'Therapy Type'},
          {label: 'Lab Test Template', value: 'Lab Test Template'},
          {label: 'Clinical Procedure Template', value: 'Clinical Procedure Template'},
          {label: 'Appointment Type', value: 'Appointment Type'},
          {label: 'Observation Template', value: 'Observation Template'},
          {label: 'Healthcare Activity', value: 'Healthcare Activity'},
        ],
        template_dn_options: reactive([])
      };
    },
    methods: {
      updateIsOpen(value) {
        this.$emit('update:isOpen', value);
      },
      closeDialog() {
        this.updateIsOpen(false);
      },
      onSubmit() {
        const { validate } = Form.useForm(this.form, this.rules);
        validate().then(() => {
          this.lodingOverlay = true;
          let formClone = {...this.form}
          formClone.order_date = dayjs(this.form.order_date).format('YYYY-MM-DD')
          formClone.order_time = dayjs(this.form.order_time).format('HH:mm')
          if(this.form.expected_date)
            formClone.expected_date = dayjs(this.form.expected_date).format('YYYY-MM-DD')
          if(this.form.occurrence_date)
            formClone.occurrence_date = dayjs(this.form.occurrence_date).format('HH:mm')
          if(this.form.occurrence_time)
            formClone.occurrence_time = dayjs(this.form.occurrence_time).format('YYYY-MM-DD')
          this.$call('healthcare_doworks.api.methods.new_doc', {form: formClone})
          .then(response => {
            this.lodingOverlay = false;
            this.closeDialog()
          }).catch(error => {
            console.error(error);
            this.lodingOverlay = false;
            let message = error.message.split('\n');
            message = message.find(line => line.includes('frappe.exceptions'));
            if(message){
              const firstSpaceIndex = message.indexOf(' ');
              this.$emit('show-alert', message.substring(firstSpaceIndex + 1, 10000))
            }
          });
        })
        .catch(err => {
            console.log('error', err);
        });
      },
      setTemplateOptions(value) {
        if(value === 'Therapy Type')
          this.template_dn_options = this.$resources.therapyTypes.data
        else if(value === 'Lab Test Template')
          this.template_dn_options = this.$resources.labTestTemplates.data
        else if(value === 'Clinical Procedure Template')
          this.template_dn_options = this.$resources.clinicalProcedureTemplates.data
        else if(value === 'Appointment Type')
          this.template_dn_options = this.$resources.appointmentTypes.data
        else if(value === 'Observation Template')
          this.template_dn_options = this.$resources.observationTemplate.data
        else if(value === 'Healthcare Activity')
          this.template_dn_options = this.$resources.healthcareActivity.data
        else
          this.template_dn_options = []
      },
    },
  };
  </script>