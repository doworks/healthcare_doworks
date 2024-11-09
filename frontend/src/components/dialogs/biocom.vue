<template>
  <v-dialog v-model="dialogVisible" width="auto" scrollable>
    <v-card rounded="lg">
      <v-card-title class="d-flex justify-space-between align-center">
        <div class="text-h5 text-medium-emphasis ps-2">BIOCOM</div>
        <v-btn icon="mdi mdi-close" variant="text" @click="closeDialog"></v-btn>
      </v-card-title>
      <v-divider class="m-0"></v-divider>
      <v-card-text>
        <a-form layout="vertical" :model="form" :rules="rules">
          <v-container>
            <v-row>
              <v-col cols="12">
                <DataTable :value="sales" tableStyle="min-width: 50rem">
                  <ColumnGroup type="header">
                    <Row>
                      <Column header="Datw" :rowspan="2" />
                      <Column header="Pressure" :rowspan="2" />
                      <Column :rowspan="2" />
                    </Row>
                    <Row>
                      <Column header="Left" :colspan="2" />
                      <Column header="Right" :colspan="2" />
                    </Row>
                    <Row>
                      <Column header="Before" field="lastYearSale"/>
                      <Column header="After" field="thisYearSale"/>
                      <Column header="Before" field="lastYearProfit"/>
                      <Column header="After" field="thisYearProfit"/>
                    </Row>
                  </ColumnGroup>
                  <Column field="product" />
                  <Column field="lastYearSale">
                      <template #body="slotProps">
                          {{slotProps.data.lastYearSale}}%
                      </template>
                  </Column>
                  <Column field="thisYearSale">
                      <template #body="slotProps">
                          {{slotProps.data.thisYearSale}}%
                      </template>
                  </Column>
                  <Column field="lastYearProfit">
                      <template #body="slotProps">
                          {{formatCurrency(slotProps.data.lastYearProfit)}}
                      </template>
                  </Column>
                  <Column field="thisYearProfit">
                      <template #body="slotProps">
                          {{formatCurrency(slotProps.data.thisYearProfit)}}
                      </template>
                  </Column>
                  <ColumnGroup type="footer">
                      <Row>
                          <Column footer="Totals:" :colspan="3" footerStyle="text-align:right"/>
                          <Column :footer="lastYearTotal" />
                          <Column :footer="thisYearTotal" />
                      </Row>
                  </ColumnGroup>
              </DataTable>
              </v-col>
            </v-row> 
          </v-container>
        </a-form>
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
      
      text="Save"
      variant="tonal"
      @click="onSubmit()"
      type="submit"
      ></v-btn>
      </v-card-actions>
    </v-card>
    <v-overlay :model-value="lodingOverlay" class="align-center justify-center">
    <v-progress-circular color="primary" size="64" indeterminate></v-progress-circular>
    </v-overlay>
  </v-dialog>
</template>

<script >
import { Form } from 'ant-design-vue';

import { VDivider } from 'vuetify/components/VDivider';
import { VInfiniteScroll } from 'vuetify/components/VInfiniteScroll';
import { VItemGroup, VItem } from 'vuetify/components/VItemGroup';
import { VOverlay } from 'vuetify/components/VOverlay';
import { VProgressCircular } from 'vuetify/components/VProgressCircular';

export default {
  inject: ['$call'],
  components: {VInfiniteScroll, VItemGroup, VItem, VOverlay, VProgressCircular},
  props: {
    isOpen: {type: Boolean, required: true, default: false},
  },
  resources: {
    genders() { return { 
      type: 'list', 
      doctype: 'Gender', 
      fields: ['gender', 'name'], 
      auto: true, 
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
  },
  data() {
    return {
      lodingOverlay: false,
      form: {

      },
      rules: {

      },
    };
  },
  watch: {
    isOpen(newVal) {
      if (newVal) {

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
    onSubmit() {
      const { validate } = Form.useForm(this.form, this.rules);
      validate().then(() => {
        this.$emit('submitted', this.form)
        // this.lodingOverlay = true;
        // this.$call('healthcare_doworks.api.methods.new_doc', {form: this.form})
        // .then(response => {
        //   this.lodingOverlay = false;
        //   this.$emit('submitted', response)
        //   this.closeDialog()
        // }).catch(error => {
        //   console.error(error);
        //   let message = error.message.split('\n');
        //   message = message.find(line => line.includes('frappe.exceptions'));
        //   if(message){
        //     const firstSpaceIndex = message.indexOf(' ');
        //     this.$emit('show-alert', message.substring(firstSpaceIndex + 1, 10000))
        //   }
        // });
      })
      .catch(err => {
        console.log('error', err);
      });
    },
    updateFullName() {
      this.form.patient_name = (this.form.first_name ? this.form.first_name : '' ) + 
      (this.form.middle_name ? ' ' + this.form.middle_name : '') + 
      (this.form.last_name ? ' ' + this.form.last_name : '')
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
  },
};
</script>