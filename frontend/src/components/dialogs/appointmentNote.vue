<template>
  <v-dialog v-model="dialogVisible" width="auto">
      <v-card rounded="lg" width="auto">
        <v-card-title class="d-flex justify-space-between align-center">
          <div class="text-h5 text-medium-emphasis ps-2">New Note</div>
          <v-btn icon="mdi mdi-close" variant="text" @click="closeDialog"></v-btn>
        </v-card-title>
        <v-divider class="m-0"></v-divider>
        <v-card-text>
          <a-form-item label="For">
            <a-select
            v-model:value="form.for"
            :options="[{label: 'Users', value: 'Users'}, {label: 'Roles', value: 'Roles'}]"
            style="min-width: 400px; max-width: 600px;"
            ></a-select>
          </a-form-item>
          <a-form-item label="Users" v-if="form.for == 'Users'">
            <a-select
            allow-clear
            mode="multiple"
            v-model:value="form.children.users"
            :options="$resources.users.data?.options"
            :fieldNames="{label: 'full_name', value: 'name'}"
            style="min-width: 400px; max-width: 600px;"
            show-search
            :loading="$resources.users.list.loading"
            @search="(value) => {handleSearch(
              value, 
              $resources.users, 
              {enabled: 1, full_name: ['like', `%${value}%`]}, 
              {enabled: 1},
            )}"
            :filterOption="false"
            ></a-select>
          </a-form-item>
          <a-form-item label="Roles" v-if="form.for == 'Roles'">
            <a-select
            allow-clear
            mode="multiple"
            v-model:value="form.children.roles"
            :options="$resources.roles.data?.options"
            :fieldNames="{label: 'role_name', value: 'name'}"
            style="min-width: 400px; max-width: 600px;"
            show-search
            :loading="$resources.roles.list.loading"
            @search="(value) => {handleSearch(
              value, 
              $resources.roles, 
              {disabled: 0, role_name: ['like', `%${value}%`]}, 
              {disabled: 0},
            )}"
            :filterOption="false"
            ></a-select>
          </a-form-item>
          <a-form-item label="Notes">
            <a-textarea v-model:value="form.note" placeholder="Notes" :rows="4" />
          </a-form-item>
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
      </v-card>
      <v-overlay :model-value="lodingOverlay" class="align-center justify-center">
        <v-progress-circular color="primary" size="64" indeterminate></v-progress-circular>
      </v-overlay>
    </v-dialog>
</template>

<script >
import dayjs from 'dayjs';
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
    appointmentId: {type: String, required: true, default: ''},
  },
  resources: {
    users() { return { 
      type: 'list', 
      doctype: 'User', 
      filters: {enabled: 1},
      fields: ['name', 'full_name'], 
      auto: true, 
      orderBy: 'full_name',
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
    roles() { return { 
      type: 'list', 
      doctype: 'Role', 
      filters: {disabled: 0},
      fields: ['name', 'role_name'], 
      auto: true, 
      orderBy: 'role_name',
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
        for: 'Users',
        note: '',
        children: {
          users: [],
          roles: []
        },
      },
    };
  },
  watch: {
    isOpen(newVal) {
      if (newVal) {
        this.form = {
          for: 'Users',
          note: '',
          children: {
            users: [],
            roles: []
          },
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
    onSubmit() {
      this.lodingOverlay = true;
      // let form = {
      //   doctype: 'Appointment Note Table', 
      //   parent: this.appointmentId, 
      //   parentfield: 'custom_visit_notes', 
      //   parenttype: 'Patient Appointment', 
      //   for: this.form.for, 
      //   from: this.$myresources.user.name,
      //   time: dayjs().format('YYYY-MM-DD HH:mm'), 
      //   note: this.form.note, 
      //   read: 0, 
      // }
      let children = {}
      if(this.form.children.users.length > 0){
        children.users = this.form.children.users.map(value => ({user: value}))
      }
      if(this.form.children.roles.length > 0){
        children.roles = this.form.children.roles.map(value => ({role: value}))
      }
      this.$call('healthcare_doworks.api.methods.new_doc', {form: {
        doctype: 'Appointment Note Table', 
        parent: this.appointmentId, 
        parentfield: 'custom_visit_notes', 
        parenttype: 'Patient Appointment', 
        for: this.form.for, 
        from: this.$myresources.user.name,
        time: dayjs().format('YYYY-MM-DD HH:mm'), 
        note: this.form.note, 
        read: 0, 
      }, children}).then(response => {
        this.$toast.add({
          severity: 'success',
          summary: 'Success',
          detail: 'Visit note added',
          life: 3000 // Duration in ms
        });
        this.lodingOverlay = false;
        this.closeDialog()
      }).catch(error => {
        this.$emit('show-alert', error.message, 'error')
      });
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