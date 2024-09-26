<template>
  <v-dialog v-model="dialogVisible" width="1400px" scrollable>
    <v-card rounded="lg">
        <v-card-title class="d-flex justify-space-between align-center">
          <div class="text-h5 text-medium-emphasis ps-2"><br>{{ appointment.patient_name }}</br> Appointment Invoice</div>
          <v-btn icon="mdi mdi-close" variant="text" @click="closeDialog"></v-btn>
        </v-card-title>
        <v-divider class="m-0"></v-divider>
        <v-card-text>
          <v-container fluid>
            <!-- <v-row>
              <v-col cols="12" md="6">
                <a-form layout="vertical">
                  <a-form-item label="Payment Type">
                    <a-select
                      class="w-full"
                      v-model:value="appointment.custom_payment_type"
                      :options="[{label: '', value: ''}, {label: 'Self Payment', value: 'Self Payment'}, {label: 'Insurance', value: 'Insurance'}]"
                      @blur="event => {autoSave('Patient Appointment', appointment.name, 'custom_payment_type', event.target.value)}"
                    ></a-select>
                  </a-form-item>
                </a-form>
              </v-col>
            </v-row> -->
            <v-row>
              <Menubar v-if="actions.length > 0" :model="actions" class="w-full"/>
              <v-col cols="12">
                <h5>Invoice Items</h5>
                <EditableTable :columns="[
                  {label: 'Service', key: 'item'},
                  {label: 'Quantity', key: 'quantity'},
                  {label: 'Rate', key: 'rate'},
                  {label: 'Amount', key: 'amount'},
                  ...(appointment.custom_payment_type == 'Insurance' ? [
                    {label: 'Patient Amount', key: 'customer_amount'},
                    {label: 'Insurance Amount', key: 'insurance_amount'}
                  ] : []),
                  {label: appointment.custom_payment_type == 'Insurance' ? 'Customer Invoice' : 'Invoice', key: 'customer_invoice'},
                  ...(appointment.custom_payment_type == 'Insurance' ? [{label: 'Insurance Invoice', key: 'insurance_invoice'}] : []),
                ]"
                :rows="invoiceItems"
                @update="(items, row, isNew) => {
                  invoiceItems = items
                  if(items && row)
                    newChildRow({
                      fieldName: 'custom_invoice_items', 
                      rules: {item: [{ required: true, message: 'Please choose an item!' }]},
                      items, row, isNew
                    })
                }"
                @delete="rows => {deleteChildRow({fieldName: 'custom_invoice_items', rows})}"
                title="Invoice Items"
                >
                  <template v-slot:dialog="{ row }">
                    <a-form layout="vertical">
                      <a-form-item label="Service">
                        <a-select
                        v-model:value="row.item"
                        :options="$resources.items.data?.options"
                        @change="(value, option) => {
                          row.item_name = option.item_name;
                          row.item_uom = option.weight_uom;
                          row.rate = option.valuation_rate;
                          if(!row.quantity)
                            row.quantity = 1;
                          row.amount = parseFloat(option.valuation_rate) * parseFloat(row.quantity);
                        }"
                        :fieldNames="{label: 'item_name', value: 'name'}"
                        show-search
                        :loading="$resources.items.list.loading"
                        @search="(value) => {handleSearch(
                          value, 
                          $resources.items, 
                          {item_name: ['like', `%${value}%`]}, 
                          {},
                        )}"
                        :filterOption="false"
                        ></a-select>
                      </a-form-item>
                      <a-form-item label="Quantity">
                        <a-input-number 
                        class="w-full" 
                        :controls="false" 
                        :defaultValue="1" 
                        v-model:value="row.quantity" 
                        @change="(value, option) => {row.amount = parseFloat(value) * parseFloat(row.rate)}"
                        />
                      </a-form-item>
                      <a-form-item label="Rate">
                        <a-input-number 
                        class="w-full" 
                        :controls="false" 
                        :defaultValue="0" 
                        v-model:value="row.rate" 
                        @change="(value, option) => {row.amount = parseFloat(value) * parseFloat(row.quantity)}"
                        />
                      </a-form-item>
                      <a-form-item label="Amount">
                        <a-input-number class="w-full" :controls="false" v-model:value="row.amount" disabled/>
                      </a-form-item>
                      <a-form-item label="Patient Amount" v-if="appointment.custom_payment_type == 'Insurance'">
                        <a-input-number class="w-full" :controls="false" v-model:value="row.customer_amount"/>
                      </a-form-item>
                      <a-form-item label="Insurance Amount" v-if="appointment.custom_payment_type == 'Insurance'">
                        <a-input-number class="w-full" :controls="false" v-model:value="row.insurance_amount"/>
                      </a-form-item>
                    </a-form>
                  </template>
                </EditableTable>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        
        <v-divider class="m-0"></v-divider>
        <v-dialog v-model="salesInvoiceOpen" width="auto">
          <v-card
          rounded="lg"
          width="auto"
          >
          <v-card-title class="d-flex justify-space-between align-center">
            <div class="text-h5 text-medium-emphasis ps-2">Sales Invoice</div>
            <v-btn icon="mdi mdi-close" variant="text" @click="salesInvoiceOpen = false"></v-btn>
          </v-card-title>
          <v-divider class="m-0"></v-divider>
            <v-card-text>
              <a-form layout="vertical">
                <a-form-item label="POS Profile">
                  <a-select
                  v-model:value="posProfile"
                  :options="$resources.posProfiles.data?.options"
                  @change="value => {getPaymentMethods(value)}"
                  :fieldNames="{label: 'name', value: 'name'}"
                  style="min-width: 400px; max-width: 600px;"
                  show-search
                  :loading="$resources.posProfiles.list.loading"
                  @search="(value) => {handleSearch(
                    value, 
                    $resources.posProfiles, 
                    {item_name: ['like', `%${value}%`]}, 
                    {},
                  )}"
                  :filterOption="false"
                  ></a-select>
                </a-form-item>

                <DataTable v-if="paymentMethods.length > 0" :value="paymentMethods" editMode="cell" @cell-edit-complete="onCellEditComplete"
                  :pt="{
                    table: { style: 'min-width: 50rem' },
                    column: {
                      bodycell: ({ state }) => ({
                        class: [{ 'pt-0 pb-0': state['d_editing'] }]
                      })
                    }
                  }"
                >
                  <Column field="mode_of_payment" header="Mode of Payment">
                  </Column>
                  <Column field="amount" header="Amount">
                    <template #body="{ data, field }">
                      {{ data[field] ? data[field].toString() : '0' }}
                    </template>
                    <template #editor="{ data, field }">
                      <a-input-number :controls="false" v-model:value="data[field]"/>
                    </template>
                  </Column>
                  <Column field="reference_no" header="Reference No">
                    <template #editor="{ data, field }">
                      <a-input v-model:value="data[field]"/>
                    </template>
                  </Column>
                </DataTable>
              </a-form>
            </v-card-text>

            <v-card-actions class="my-2 d-flex justify-end">
              <v-btn
              class="text-none"
              text="Cancel"
              @click="salesInvoiceOpen = false"
              ></v-btn>

              <v-btn
              class="text-none"
              color="blue"
              
              text="submit"
              variant="tonal"
              @click="onSubmitInvoice"
              ></v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>

        <v-dialog v-model="modeOfPaymentOpen" width="auto">
          <v-card
          rounded="lg"
          width="auto"
          >
          <v-card-title class="d-flex justify-space-between align-center">
            <div class="text-h5 text-medium-emphasis ps-2">Make Payment</div>
            <v-btn icon="mdi mdi-close" variant="text" @click="modeOfPaymentOpen = false"></v-btn>
          </v-card-title>
          <v-divider class="m-0"></v-divider>
            <v-card-text>
              <a-form layout="vertical">
                <a-form-item label="Mode of Payment">
                  <a-select
                  v-model:value="modeOfPayment"
                  :options="$resources.modeOfPayments.data?.options"
                  @change="(value, option) => {paymentType = option.type}"
                  :fieldNames="{label: 'name', value: 'name'}"
                  style="min-width: 400px; max-width: 600px;"
                  show-search
                  :loading="$resources.modeOfPayments.list.loading"
                  @search="(value) => {handleSearch(
                    value, 
                    $resources.modeOfPayments, 
                    {item_name: ['like', `%${value}%`]}, 
                    {},
                  )}"
                  :filterOption="false"
                  ></a-select>
                </a-form-item>

                <a-form-item label="Cheque/Reference No" v-if="paymentType == 'Bank'">
                  <a-input v-model:value="referenceNo" style="min-width: 400px; max-width: 600px;"/>
                </a-form-item>

                <a-form-item label="Cheque/Reference Date" v-if="paymentType == 'Bank'">
                  <a-input v-model:value="referenceDate" style="min-width: 400px; max-width: 600px;"/>
                </a-form-item>
              </a-form>
            </v-card-text>

            <v-card-actions class="my-2 d-flex justify-end">
              <v-btn
              class="text-none"
              text="Cancel"
              @click="modeOfPaymentOpen = false"
              ></v-btn>

              <v-btn
              class="text-none"
              color="blue"
              
              text="submit"
              variant="tonal"
              @click="onSubmitPayment"
              ></v-btn>
            </v-card-actions>
          </v-card>
        </v-dialog>
        
        <!-- <v-card-actions class="my-2 d-flex justify-end">
        <v-btn
        class="text-none"
        text="Cancel"
        @click="closeDialog"
        ></v-btn>
        <v-btn
        class="text-none"
        color="blue"
        text="Submit"
        variant="tonal"
        @click="onSubmit()"
        type="submit"
        ></v-btn>
        </v-card-actions> -->
    </v-card>
    <v-overlay
    :model-value="lodingOverlay"
    class="align-center justify-center"
    >
      <v-progress-circular
        color="primary"
        size="64"
        indeterminate
      ></v-progress-circular>
    </v-overlay>
  </v-dialog>
</template>

<script >
import { Form } from 'ant-design-vue';
import dayjs from 'dayjs';

import { VDivider } from 'vuetify/components/VDivider';
import { VInfiniteScroll } from 'vuetify/components/VInfiniteScroll';
import { VItemGroup, VItem } from 'vuetify/components/VItemGroup';
import { VOverlay } from 'vuetify/components/VOverlay';
import { VProgressCircular } from 'vuetify/components/VProgressCircular';
import EditableTable from '../editableTable.vue';

export default {
  inject: ['$call'],
  components: {
    VDivider, VInfiniteScroll, VItemGroup, VItem, VOverlay, VProgressCircular,
  },
  props: {
    isOpen: {
      type: Boolean,
      required: true,
      default: false,
    },
    appointment: {
      required: true,
      default: {
        name: '',
      }
    },
  },
  resources: {
    items() { return { 
      type: 'list', 
      doctype: 'Item', 
      fields: ['name', 'item_code', 'item_name', 'valuation_rate', 'weight_uom'], 
      filters: {},
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
    modeOfPayments() { return { 
      type: 'list', 
      doctype: 'Mode of Payment', 
      fields: ['name', 'type'], 
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
    posProfiles() { return { 
      type: 'list', 
      doctype: 'POS Profile', 
      fields: ['name'], 
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
    dialogVisible: {
      get() {
        return this.isOpen;
      },
      set(value) {
        this.$emit('update:isOpen', value);
      },
    },
    invoiceItems() {
      return this.appointment.invoice_items;
    },
    actions() {
      return [
        ...(this.invoiceItems.some(value => !value.customer_invoice) ? [{
          label: 'Create Invoices',
          icon: 'pi pi-plus',
          command: () => {
            this.posProfile = '';
            this.paymentMethods = []
            this.salesInvoiceOpen = true
          }
        }] : []),
        // {
        //   label: 'Make Payment',
        //   icon: 'mdi mdi-credit-card-outline',
        //   command: () => {
        //     this.paymentType = '';
        //     this.modeOfPaymentOpen = true
        //   }
        // },
      ]
    }
  },
  data() {
    return {
      lodingOverlay: false,
      modeOfPaymentOpen: false,
      salesInvoiceOpen: false,
      modeOfPayment: null,
      paymentType: '',
      referenceNo: '',
      referenceDate: '',
      posProfile: '',
      paymentMethods: [],
      invoiceItems: this.appointment.invoice_items,
      // actions: [
      //   ...(this.invoiceItems.some(value => !value.customer_invoice) ? [{
      //     label: 'Create Invoices',
      //     icon: 'pi pi-plus',
      //     command: () => {
      //       this.posProfile = '';
      //       this.paymentMethods = []
      //       this.salesInvoiceOpen = true
      //     }
      //   }] : []),
      //   {
      //     label: 'Make Payment',
      //     icon: 'mdi mdi-credit-card-outline',
      //     command: () => {
      //       this.paymentType = '';
      //       this.modeOfPaymentOpen = true
      //     }
      //   },
      // ],
    };
  },
  mounted() {
    // console.log(this.appointment)
    this.posProfile = '';
    this.paymentType = '';
  },
  watch: {
    appointment: {
			handler(newValue) {
				if(newValue){
          this.invoiceItems = newValue.invoice_items
        }
			}
		},
  },
  methods: {
    updateIsOpen(value) {
      this.$emit('update:isOpen', value);
    },
    closeDialog() {
      this.updateIsOpen(false);
    },
    getPaymentMethods(value) {
      if(value)
        this.$call('healthcare_doworks.api.methods.pos_payment_method', {
          pos_profile: value
        }).then(response => {
          
          this.paymentMethods = response.map(value => {
            if(value.default){
              value.amount = this.invoiceItems.filter(val => !val.customer_invoice)
              .reduce((total, val) => total + (parseFloat(val.amount) - (val.invoice_amount ? parseFloat(val.invoice_amount) : 0)), 0)
            }
            else
              value.amount = 0
            return value
          })
          console.log(this.paymentMethods)
        }).catch(error => {
          console.error(error);
          let message = error.message.split('\n');
          message = message.find(line => line.includes('frappe.exceptions'));
          if(message){
            const firstSpaceIndex = message.indexOf(' ');
            this.$emit('show-alert', message.substring(firstSpaceIndex + 1, 10000))
          }
        });
    },
    onCellEditComplete(event) {
      let { data, newValue, field } = event;
      data[field] = newValue;
    },
    onSubmitInvoice() {
      this.lodingOverlay = true;
      this.$call('healthcare_doworks.api.methods.create_invoice', {
        appointment: this.appointment.name,
        profile: this.posProfile,
        payment_methods: this.paymentMethods
      })
      .then(response => {
        this.lodingOverlay = false;
        this.salesInvoiceOpen = false
        if(response)
          this.invoiceItems = this.invoiceItems.map(value => {
            if(!value.customer_invoice)
              value.customer_invoice = response.customer_invoice
            if(!value.insurance_invoice)
              value.insurance_invoice = response.insurance_invoice
            return value
          })
      }).catch(error => {
        console.error(error);
        let message = error.message.split('\n');
        message = message.find(line => line.includes('frappe.exceptions'));
        if(message){
          const firstSpaceIndex = message.indexOf(' ');
          this.$emit('show-alert', message.substring(firstSpaceIndex + 1, 10000))
        }
      });
    },
    onSubmitPayment() {
      this.lodingOverlay = true;
      this.$call('healthcare_doworks.api.methods.make_payment', {
        appointment: this.appointment.name,
        mode_of_payment: this.modeOfPayment,
        reference_no: this.referenceNo,
        reference_date: this.referenceDate
      })
      .then(response => {
        this.lodingOverlay = false;
        this.modeOfPaymentOpen = false;
      }).catch(error => {
        console.error(error);
        let message = error.message.split('\n');
        message = message.find(line => line.includes('frappe.exceptions'));
        if(message){
          const firstSpaceIndex = message.indexOf(' ');
          this.$emit('show-alert', message.substring(firstSpaceIndex + 1, 10000))
        }
      });
    },
    autoSave(doctype, name, fieldname, value) {
      if(this.isNew) return;

      this.$call('frappe.client.set_value', {doctype, name, fieldname, value})
      .then(response => {
        this.$toast.add({ severity: 'success', summary: 'Saved', life: 2000 });
      }).catch(error => {
        console.error(error);
        let message = error.message.split('\n');
        message = message.find(line => line.includes('frappe.exceptions'));
        if(message){
          const firstSpaceIndex = message.indexOf(' ');
          this.showAlert(message.substring(firstSpaceIndex + 1) , 10000)
        }
        else
          this.showAlert('Sorry. There is an error!' , 10000)
      });
    },
    newChildRow({parentDoctype ,prarentDocname, fieldName, rules, items, row, isNew}) {
      const { validate } = Form.useForm(row, rules);
      validate().then(() => {
        let formClone = {...row}
        delete formClone.modified
        delete formClone.modified_by
        delete formClone.name
        if(isNew){
          this.$call('healthcare_doworks.api.general_methods.add_child_entry', {
            parent_doctype: parentDoctype || 'Patient Appointment', 
            parent_doc_name: prarentDocname || this.appointment.name, 
            child_table_fieldname: fieldName, 
            child_data: formClone
          }).then(response => {
          }).catch(error => {
            console.error(error);
            let message = error.message.split('\n');
            message = message.find(line => line.includes('frappe.exceptions'));
            if(message){
              const firstSpaceIndex = message.indexOf(' ');
              this.showAlert(message.substring(firstSpaceIndex + 1) , 10000)
            }
            else
              this.showAlert('Sorry. There is an error!' , 10000)
          });
        }
        else{
          this.$call('healthcare_doworks.api.general_methods.modify_child_entry', {
            parent_doctype: parentDoctype || 'Patient Appointment', 
            parent_doc_name: prarentDocname || this.appointment.name, 
            child_table_fieldname: fieldName, 
            filters: {name: row.name}, 
            update_data: formClone
          }).then(response => {
          }).catch(error => {
            console.error(error);
            let message = error.message.split('\n');
            message = message.find(line => line.includes('frappe.exceptions'));
            if(message){
              const firstSpaceIndex = message.indexOf(' ');
              this.showAlert(message.substring(firstSpaceIndex + 1) , 10000)
            }
            else
              this.showAlert('Sorry. There is an error!' , 10000)
          });
        }
      })
      .catch(err => {
        console.log('error', err);
      });
    },
    deleteChildRow({parentDoctype, prarentDocname, fieldName, rows, filterField}) {
      rows.forEach(row => {
        this.$call('healthcare_doworks.api.general_methods.delete_child_entry', {
          parent_doctype: parentDoctype || 'Patient Appointment', 
          parent_doc_name: prarentDocname || this.appointment.name, 
          child_table_fieldname: fieldName, 
          filters: {[filterField || 'name']: row}
        }).then(response => {
        }).catch(error => {
          console.error(error);
          let message = error.message.split('\n');
          message = message.find(line => line.includes('frappe.exceptions'));
          if(message){
            const firstSpaceIndex = message.indexOf(' ');
            this.showAlert(message.substring(firstSpaceIndex + 1) , 10000)
          }
          else
            this.showAlert('Sorry. There is an error!' , 10000)
        })
        .catch(err => {
          console.log('error', err);
        });
      })
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
    handleSearch(query, resource, filters, initialFilters, orFilters) {
      // Clear the previous timeout to avoid spamming requests
      clearTimeout(this.searchTimeout);

      // Set a new timeout (300ms) for debouncing
      this.searchTimeout = setTimeout(() => {
        if (query) {
          // Update list resource options to fetch matching records from server
          resource.update({filters, orFilters});

          // Fetch the updated results
          resource.reload();
        } else {
          // If no search query, load initial records
          resource.update({filters: initialFilters, orFilters});
          resource.reload();
        }
      }, 300);  // Debounce delay of 300ms
    },
  },
};
</script>