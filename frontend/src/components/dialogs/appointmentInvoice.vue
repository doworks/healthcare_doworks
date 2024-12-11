<template>
  <v-dialog v-model="dialogVisible" width="1400px" scrollable>
    <v-card rounded="lg">
        <v-card-title class="d-flex justify-space-between align-center">
          <div class="text-h5 text-medium-emphasis ps-2">
            <br>{{ appointment.patient_name }}</br> Appointment Invoice 
            <!-- <Tag severity="secondary" value="Secondary"></Tag> -->
          </div>
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
                  {label: 'Discount Percentage', key: 'discount_percentage'},
                  {label: 'Discount Amount', key: 'discount_amount'},
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
                :onRowClick="onInvoiceRowClick"
                ref="invoiceItems"
                >
                  <template v-slot:dialog="{ row }">
                    <a-form layout="vertical">
                      <a-form-item label="Service">
                        <a-select
                        v-model:value="row.item"
                        :options="$resources.items.data"
                        @change="(value, option) => {
                          row.item_name = option.item_name;
                          row.item_uom = option.weight_uom;
                          row.rate = parseFloat(option.item_price.filter(value => value.price_list == 'Standard Selling')[0]?.price_list_rate) || 0;
                          if(appointment.custom_payment_type == 'Insurance' && option.item_price.some(value => value.price_list == 'Insurance Price')){
                            row.rate = option.item_price.filter(value => value.price_list == 'Insurance Price')[0]?.price_list_rate || 0;
                          }
                          if(!row.quantity)
                            row.quantity = parseFloat(1);
                          else
                            row.quantity = parseFloat(row.quantity);
                          row.amount = parseFloat(row.rate) * parseFloat(row.quantity);
                          if(appointment.custom_payment_type == 'Insurance'){
                            row.customer_amount = 0;
                            row.insurance_amount = row.amount;
                          }
                          else{
                            row.customer_amount = row.amount;
                            row.insurance_amount = 0
                          }
                        }"
                        :fieldNames="{label: 'item_name', value: 'name'}"
                        show-search
                        :loading="$resources.items.list.loading"
                        @search="(value) => {handleSearch(
                          value, 
                          $resources.items, 
                          {disabled: 0, has_variants: 0, is_sales_item: 1}, 
                          {disabled: 0, has_variants: 0, is_sales_item: 1},
                          [
                            ['name', 'like', `%${value}%`],
                            ['item_code', 'like', `%${value}%`], 
                            ['item_name', 'like', `%${value}%`], 
                            ['item_group', 'like', `%${value}%`], 
                          ]
                        )}"
                        :filterOption="false"
                        >
                          <template #option="{ item_code, item_name, item_group, description }">
                            <div class="flex flex-col">
                              <span v-if="item_name" class="ms-2"><strong>{{ item_code }}</strong></span>
                              <span v-if="item_name || item_group || description" class="ms-2">
                                {{ item_name + (item_name && item_group ? ', ' : '') + item_group + (item_group && description ? ', ' : '') + description }}
                              </span>
                            </div>
                          </template>
                        </a-select>
                      </a-form-item>
                      <a-form-item label="Quantity">
                        <a-input-number 
                        class="w-full" 
                        :controls="false" 
                        :defaultValue="1" 
                        v-model:value="row.quantity" 
                        @change="(value, option) => {
                          row.amount = parseFloat(value) * parseFloat(row.rate)
                          if(appointment.custom_payment_type == 'Insurance')
                            row.insurance_amount = row.amount - parseFloat(row.customer_amount);
                          else
                            row.customer_amount = row.amount;
                        }"
                        />
                      </a-form-item>
                      <a-form-item label="Rate">
                        <a-input-number 
                        class="w-full" 
                        :controls="false" 
                        :defaultValue="0" 
                        :min="0"
                        v-model:value="row.rate" 
                        @change="(value, option) => {
                          if(!value){
                            row.rate = 0
                            row.amount = 0
                          }
                          else if(row.discount_amount){
                            row.amount = (parseFloat(value) - parseFloat(row.discount_amount)) * parseFloat(row.quantity)
                          }
                          else{
                            row.amount = parseFloat(value) * parseFloat(row.quantity)
                          }
                          
                          if(appointment.custom_payment_type == 'Insurance')
                            row.insurance_amount = row.amount - parseFloat(row.customer_amount);
                          else
                            row.customer_amount = row.amount;
                        }"
                        />
                      </a-form-item>
                      <a-form-item label="Discount Percentage">
                        <a-input-number 
                        class="w-full" 
                        :controls="false" 
                        v-model:value="row.discount_percentage"
                        @change="(value, option) => {
                          if(value){
                            row.discount_amount = parseFloat(value) / 100 * parseFloat(row.rate)
                            row.amount = (parseFloat(row.rate) - row.discount_amount) * parseFloat(row.quantity)
                          }
                          else{
                            row.discount_percentage = undefined
                            row.discount_amount = undefined
                            row.amount = parseFloat(row.rate) * parseFloat(row.quantity)
                          }

                          if(appointment.custom_payment_type == 'Insurance')
                            row.insurance_amount = row.amount - parseFloat(row.customer_amount);
                          else
                            row.customer_amount = row.amount;
                        }"
                        />
                      </a-form-item>
                      <a-form-item label="Discount Amount">
                        <a-input-number 
                        class="w-full" 
                        :controls="false" 
                        v-model:value="row.discount_amount"
                        @change="(value, option) => {
                          if(value){
                            row.discount_percentage = parseFloat(value) / parseFloat(row.rate) * 100
                            row.amount = (parseFloat(row.rate) - value) * parseFloat(row.quantity)
                          }
                          else{
                            row.discount_percentage = undefined
                            row.discount_amount = undefined
                            row.amount = parseFloat(row.rate) * parseFloat(row.quantity)
                          }

                          if(appointment.custom_payment_type == 'Insurance')
                            row.insurance_amount = row.amount - parseFloat(row.customer_amount);
                          else
                            row.customer_amount = row.amount;
                        }"
                        />
                      </a-form-item>
                      <a-form-item label="Amount">
                        <a-input-number class="w-full" :controls="false" v-model:value="row.amount" disabled/>
                      </a-form-item>
                      <a-form-item label="Patient Amount" v-if="appointment.custom_payment_type == 'Insurance'">
                        <a-input-number 
                        class="w-full" 
                        :controls="false" 
                        :defaultValue="0" 
                        :min="0"
                        :max="row.amount"
                        v-model:value="row.customer_amount"
                        @change="(value, option) => {row.insurance_amount = parseFloat(row.amount) - value}"
                        />
                      </a-form-item>
                      <a-form-item label="Insurance Amount" v-if="appointment.custom_payment_type == 'Insurance'">
                        <a-input-number 
                        class="w-full" 
                        :controls="false" 
                        :defaultValue="0" 
                        :min="0"
                        :max="row.amount"
                        v-model:value="row.insurance_amount"
                        @change="(value, option) => {row.customer_amount = parseFloat(row.amount) - value}"
                        />
                      </a-form-item>
                    </a-form>
                  </template>
                </EditableTable>
              </v-col>
            </v-row>
            <h5 class="mt-4 mb-2">Taxes And Discounts</h5>
            <v-row>          
              <v-col cols="12" md="6">
                <a-form layout="vertical">
                  <a-form-item label="Tax Template">
                    <LinkField 
                    doctype="Sales Taxes and Charges Template" 
                    :value="appointment.custom_invoice_tax_template" 
                    @change="(data) => { 
                      $setValue({doctype: 'Patient Appointment', name: appointment.name, fieldname:'custom_invoice_tax_template', value: data})
                      .then(response => {
                        appointment.custom_invoice_tax_template = response.custom_invoice_tax_template
                        getPrices()
                      })
                    }"
                    />
                  </a-form-item>
                  <a-form-item label="Total Taxes and Charges" v-if="mockInvoice?.total_taxes_and_charges" >
                    <a-input class="w-full" disabled v-model:value="mockInvoice.total_taxes_and_charges"/>
                  </a-form-item>
                </a-form>
              </v-col>
              <v-col cols="12" md="6">
                <a-form layout="vertical">
                  <a-form-item label="Apply Discount On">
                    <a-select
                      class="w-full"
                      v-model:value="appointment.custom_apply_discount_on"
                      :options="[
                        {label: '', value: ''}, 
                        {label: 'Grand Total', value: 'Grand Total'}, 
                        {label: 'Net Total', value: 'Net Total'}
                      ]"
                      @change="value => {
                        $setValue({
                          doctype: 'Patient Appointment', 
                          name: appointment.name, 
                          fieldname: 'custom_apply_discount_on',
                          value: value
                        })
                        .then(response => {
                          getPrices()
                        })
                      }"
                    ></a-select>
                  </a-form-item>
                  <a-form-item label="Discount Percentage">
                    <a-input-number 
                    class="w-full" 
                    :controls="false" 
                    v-model:value="appointment.custom_invoice_discount_percentage"
                    @change="(value, option) => {
                      appointment.custom_invoice_discount_amount = parseFloat(value) / 100 * parseFloat(mockInvoice?.grand_total || 1)
                      $setValue({
                        doctype: 'Patient Appointment', 
                        name: appointment.name, 
                        fieldname:{
                          custom_invoice_discount_percentage: appointment.custom_invoice_discount_percentage, 
                          custom_invoice_discount_amount: appointment.custom_invoice_discount_amount, 
                        }                    
                      })
                      .then(response => {
                        getPrices()
                      })
                    }"
                    />
                  </a-form-item>
                  <a-form-item label="Discount Amount">
                    <a-input-number 
                    class="w-full" 
                    :controls="false" 
                    v-model:value="appointment.custom_invoice_discount_amount"
                    @change="(value, option) => {
                      appointment.custom_invoice_discount_percentage = parseFloat(value) / parseFloat(mockInvoice?.grand_total || 1) * 100
                      $setValue({
                        doctype: 'Patient Appointment', 
                        name: appointment.name, 
                        fieldname:{
                          custom_invoice_discount_percentage: appointment.custom_invoice_discount_percentage, 
                          custom_invoice_discount_amount: appointment.custom_invoice_discount_amount, 
                        }                    
                      })
                      .then(response => {
                        getPrices()
                      })
                    }"
                    />
                  </a-form-item>
                </a-form>
              </v-col>
            </v-row>
            <h5 v-if="mockInvoice?.grand_total" class="mt-4 mb-2">Total</h5>
            <v-row>
              <v-col cols="12" md="6">
                <a-form layout="vertical">
                  <a-form-item label="Grand Total" v-if="mockInvoice?.grand_total" >
                    <a-input class="w-full" disabled v-model:value="mockInvoice.grand_total"/>
                  </a-form-item>
                  <a-form-item label="Outstanding Amount" v-if="mockInvoice?.outstanding_amount" >
                    <a-input class="w-full" disabled v-model:value="mockInvoice.outstanding_amount"/>
                  </a-form-item>
                </a-form>
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
                <a-form-item label="Grand Total" v-if="mockInvoice?.total" >
                  <a-input class="w-full" disabled v-model:value="mockInvoice.grand_total"/>
                </a-form-item>
                <a-form-item label="Total Taxes and Charges" v-if="mockInvoice?.total" >
                  <a-input class="w-full" disabled v-model:value="mockInvoice.total_taxes_and_charges"/>
                </a-form-item>
                <a-form-item label="Outstanding Amount" v-if="mockInvoice?.outstanding_amount" >
                  <a-input class="w-full" disabled v-model:value="mockInvoice.outstanding_amount"/>
                </a-form-item>
                <v-divider class="m-0"></v-divider>
                <a-form-item label="POS Profile">
                  <LinkField 
                  doctype="POS Profile" 
                  :value="posProfile" 
                  @change="(data) => { 
                    posProfile = data 
                    getPaymentMethods(data)
                  }"
                  />
                </a-form-item>
                <!-- <a-form-item label="Amount" v-if="paymentMethods.length > 0" >
                  <a-input-number 
                  class="w-full" 
                  :controls="false" 
                  disabled
                  v-model:value="paymentAmount"
                  />
                </a-form-item> -->
                <DataTable 
                v-if="paymentMethods.length > 0" 
                :value="paymentMethods" 
                editMode="cell" 
                @cell-edit-complete="onCellEditComplete"
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
                      <a-input-number 
                      :min="0"
                      :max="paymentAmount - paymentMethods.reduce((total, value) => total + value.amount, 0)" 
                      :controls="false" v-model:value="data[field]"
                      />
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
              
              text="Save"
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
                  <LinkField 
                  doctype="POS Profile" 
                  :value="modeOfPayment" 
                  @change="(data) => { modeOfPayment = data}"
                  />
                </a-form-item>

                <a-form-item label="Cheque/Reference No">
                  <a-input v-model:value="referenceNo" style="min-width: 400px; max-width: 600px;"/>
                </a-form-item>

                <a-form-item label="Cheque/Reference Date">
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
              
              text="Save"
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
        text="Save"
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
import { Form, Tag } from 'ant-design-vue';
import dayjs from 'dayjs';

import { VDivider } from 'vuetify/components/VDivider';
import { VInfiniteScroll } from 'vuetify/components/VInfiniteScroll';
import { VItemGroup, VItem } from 'vuetify/components/VItemGroup';
import { VOverlay } from 'vuetify/components/VOverlay';
import { VProgressCircular } from 'vuetify/components/VProgressCircular';
import EditableTable from '../editableTable.vue';

export default {
  inject: ['$call', '$setValue'],
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
      fields: ['name', 'item_code', 'item_name', 'weight_uom', 'item_group', 'description'], 
      filters: {disabled: 0, has_variants: 0, is_sales_item: 1},
      orFilters: [],
      auto: true,
      orderBy: 'name',
      pageLength: 10,
      url: 'healthcare_doworks.api.methods.get_invoice_items', 
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
    actions() {
      return [
        ...(this.invoiceItems.some(value => 
          (!value.customer_invoice && value.customer_amount != 0) || (this.appointment.custom_payment_type == 'Insurance' && !value.insurance_invoice)
        ) ? [{
          label: 'Create Invoices',
          icon: 'pi pi-plus',
          command: () => {
            this.getPrices()
            this.posProfile = '';
            this.paymentMethods = []
            this.taxTemplate = '';
            this.salesInvoiceOpen = true
          }
        }] : []),
        // ...(this.invoiceItems.some(value => value.customer_invoice && !value.paid) ? [{
        //   label: 'Make Payment',
        //   icon: 'mdi mdi-credit-card-outline',
        //   command: () => {
        //     this.posProfile = '';
        //     this.paymentMethods = []
        //     this.salesInvoiceOpen = true
        //   }
        // }] : []),
      ]
    }
  },
  data() {
    return {
      lodingOverlay: false,
      modeOfPaymentOpen: false,
      salesInvoiceOpen: false,
      editRow: true,
      modeOfPayment: null,
      paymentType: '',
      referenceNo: '',
      referenceDate: '',
      posProfile: '',
      taxTemplate: '',
      paymentMethods: [],
      paymentAmount: 0,
      mockInvoice: {},
      invoiceItems: this.appointment.invoice_items || [],
    };
  },
  mounted() {
    // console.log(this.appointment)
    // this.posProfile = '';
    // this.paymentType = '';
  },
  watch: {
    appointment: {
			handler(newValue) {
				if(newValue){
          this.invoiceItems = newValue.invoice_items
          if(newValue.name)
          this.getPrices()
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
      if(value){
        this.lodingOverlay = true;
        this.$call('healthcare_doworks.api.methods.pos_payment_method', {
          pos_profile: value
        }).then(response => {
          this.lodingOverlay = false;
          this.paymentMethods = response.map(value => {
            if(value.default){
              value.amount = this.mockInvoice.outstanding_amount
              this.paymentAmount = value.amount
            }
            else
              value.amount = 0
            return value
          })
        }).catch(error => {
          this.lodingOverlay = false;
          this.$emit('show-alert', error.message, 'error')
        });
      }
    },
    getPrices(value) {
      this.lodingOverlay = true;
      this.$call('healthcare_doworks.api.methods.create_mock_invoice', {appointment: this.appointment.name})
      .then(response => {
        this.lodingOverlay = false;
        this.mockInvoice = response
      }).catch(error => {
        this.lodingOverlay = false;
        this.$emit('show-alert', error.message, 'error')
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
        payment_methods: this.paymentMethods,
        tax: this.taxTemplate
      })
      .then(response => {
        this.lodingOverlay = false;
        this.salesInvoiceOpen = false
        if(response)
          this.$toast.add({
            severity: 'success',
            summary: 'Success',
            detail: 'Invoice created successfully',
            life: 3000 // Duration in ms
          });
          
          this.invoiceItems = this.invoiceItems.map(value => {
            if(!value.customer_invoice)
              value.customer_invoice = response.customer_invoice
            if(!value.insurance_invoice)
              value.insurance_invoice = response.insurance_invoice
            return value
          })
          this.getPrices()
      }).catch(error => {
        this.lodingOverlay = false;
        this.$emit('show-alert', error.message, 'error')
      });
    },
    onSubmitPayment() {
      this.lodingOverlay = true;
      this.$call('healthcare_doworks.api.methods.make_payment', {
        appointment: this.appointment.name,
        invoices: this.invoiceItems.filter(item => item.customer_invoice && !item.paid),
        profile: this.posProfile,
        payment_methods: this.paymentMethods
      })
      .then(response => {
        this.lodingOverlay = false;
        this.modeOfPaymentOpen = false;
        this.$toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Payment created successfully',
          life: 3000 // Duration in ms
        });
      }).catch(error => {
        this.$emit('show-alert', error.message, 'error')
      });
    },
    onInvoiceRowClick(row) {
      if(row.customer_invoice){
        window.open(`/app/sales-invoice/${row.customer_invoice}`)
      }
      else{
        this.$refs.invoiceItems.editRow(row)
      }
    },
    autoSave(doctype, name, fieldname, value) {
      if(this.isNew) return;

      this.$call('frappe.client.set_value', {doctype, name, fieldname, value})
      .then(response => {
        this.$toast.add({ severity: 'success', summary: 'Saved', life: 2000 });
      }).catch(error => {
        this.$emit('show-alert', error.message, 'error')
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
            this.$toast.add({
              severity: 'success',
              summary: 'Success',
              detail: 'Item row added',
              life: 3000 // Duration in ms
            });
            this.getPrices()
          }).catch(error => {
            this.$emit('show-alert', error.message, 'error')
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
            this.$toast.add({
              severity: 'success',
              summary: 'Success',
              detail: 'Item row saved',
              life: 3000 // Duration in ms
            });
            this.getPrices()
          }).catch(error => {
            this.$emit('show-alert', error.message, 'error')
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
          this.$toast.add({
            severity: 'success',
            summary: 'Success',
            detail: 'Item row deleted',
            life: 3000 // Duration in ms
          });
          this.getPrices()
        }).catch(error => {
          this.$emit('show-alert', error.message, 'error')
        })
        .catch(err => {
          console.log('error', err);
        });
      })
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