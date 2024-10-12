<template>
    <v-navigation-drawer
      expand-on-hover
      rail
      color="indigo"
      mobile-breakpoint="none"
      theme="dark"
      @update:rail="value => {rail = value}"
    >
      <v-list>
        <v-list-item :title="$myresources.user.name" :subtitle="$myresources.user.user">
          <template #prepend>
            <v-avatar :color="!$myresources.user.image ? currenColor : ''">
              <img
                v-if="$myresources.user.image"
                class="h-100 w-100"
                :src="$myresources.user.image"
              />
              <span v-if="!$myresources.user.image" class="text-h5">{{ $myresources.user.name ? $myresources.user.name[0] : '' }}</span>
            </v-avatar>
          </template>
        </v-list-item>

        <v-divider></v-divider>

        <v-list-item 
        v-if="isHealthcareAdministrator" 
        prepend-icon="fa fa-display" 
        title="Practitioner Dashboard" 
        value="practitionerDashboard"  
        to="/practitioner-dashboard"
        :class="{ 'v-list-item--active': $route.name == 'practitioner-dashboard' }"
        ></v-list-item>
        <v-list-item 
        v-if="isNurse" 
        prepend-icon="fa fa-display" 
        title="Nurse Dashboard" 
        value="nurseDashboard"  
        to="/nurse-dashboard"
        :class="{ 'v-list-item--active': $route.name == 'nurse-dashboard' }"
        ></v-list-item>
        <v-list-item 
        v-if="isPharmacist" 
        prepend-icon="fa fa-display" 
        title="Pharmacy Dashboard" 
        value="pharmacyDashboard"  
        to="/pharmacy-dashboard"
        :class="{ 'v-list-item--active': $route.name == 'pharmacy-dashboard' }"
        ></v-list-item>
        <v-list-item 
        prepend-icon="fa fa-calendar-check" 
        title="Appointments" 
        value="appointments" 
        to="/appointments"
        :class="{ 'v-list-item--active': $route.name == 'appointments' }"
        ></v-list-item>
        <v-list-item 
        prepend-icon="fa fa-user" 
        title="Patient" 
        value="patient" 
        to="/patient" 
        :class="{ 'v-list-item--active': $route.name == 'patient' || $route.name == 'patient-list' }"
        ></v-list-item>
        <v-list-item 
        prepend-icon="fa fa-user-injured" 
        title="Patient Encounter" 
        value="patientEncounter" 
        to="/patient-encounter/"
        :class="{ 'v-list-item--active': $route.name == 'patient-encounter' || $route.name == 'patient-encounter-list' }"
        ></v-list-item>
      </v-list>

      <template v-slot:append>
        <div class="pa-2">
          <v-btn class="mb-2 text-none" color="deep-purple" block href="/apps">
            <i class="mdi mdi-apps" :class="{'mr-2': !rail}"></i>
            {{!rail ? 'Apps' : ''}}
          </v-btn>
          <v-btn block class="text-none" @click="logout">
            <i class="fa fa-sign-out" :class="{'mr-2': !rail}"></i>
            {{!rail ? 'Logout' : ''}}
          </v-btn>
        </div>
      </template>

    </v-navigation-drawer>
</template>

<script>
  import colors from '@/assets/json/colors.json';
  import { VNavigationDrawer } from 'vuetify/components/VNavigationDrawer';
  import { VList, VListItem } from 'vuetify/components/VList';
  import { VDivider } from 'vuetify/components/VDivider';
  import { VAvatar } from 'vuetify/components/VAvatar';

  export default{
    inject:['$auth', '$call'],
    components:{
      VNavigationDrawer, VList, VListItem, VDivider, VAvatar,
    },
    data() {
      return {
        rail: true,
        currenColor: '',
        isNurse: false,
        isPharmacist: false,
        isHealthcareAdministrator: false
      };
    },
    mounted() {
    },
    watch: {
      '$myresources.user': {
        handler(newValue) {
          if(this.$myresources.user.name){
            this.currenColor = this.getColorFromName(this.$myresources.user.name)
            this.isHealthcareAdministrator = this.$myresources.user.roles.some(value => value.role == 'Practitioner')
            this.isNurse = this.$myresources.user.roles.some(value => value.role == 'Nursing User')
            this.isPharmacist = this.$myresources.user.roles.some(value => value.role == 'Pharmacist')
          }
        },
        immediate: true,
      },
    },
    methods:{
      getInitials(name) {
        if(name){
          let names = name.split(' '),
            initials = names[0].substring(0, 1).toUpperCase();
          
          if (names.length > 1) {
            initials += names[names.length - 1].substring(0, 1).toUpperCase();
          }
          return initials;
        }
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
      logout() {
        this.$call('frappe.handler.logout').then(() => {
          window.open('/', '_self')
        })
      },
    }
  };
</script>

<style>
.v-list--nav > .v-list-item:hover {
  color: unset;
}
</style>