<template>
    <v-navigation-drawer
      expand-on-hover
      rail
      color="indigo"
      mobile-breakpoint="none"
    >
      <v-list>
        <v-list-item :title="$myresources.user.name">
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
      </v-list>

      <v-divider></v-divider>

      <v-list nav>
        <v-list-item v-if="isHealthcareAdministrator" prepend-icon="fa fa-display" title="Doctor Dashboard" value="doctorDashboard" nav to="/doctor-dashboard"></v-list-item>
        <v-list-item v-if="isNurse" prepend-icon="fa fa-display" title="Nurse Dashboard" value="nurseDashboard" nav to="/nurse-dashboard"></v-list-item>
        <v-list-item 
        prepend-icon="fa fa-user" 
        title="Patient" 
        value="patient" 
        to="/patient" 
        :class="{ 'v-list-item--active': $route.path.startsWith('/patient/') || $route.path == '/patient/' }"
        ></v-list-item>
        <v-list-item prepend-icon="fa fa-calendar-check" title="Appointments" value="appointments" to="/appointments"></v-list-item>
        <v-list-item 
        prepend-icon="fa fa-user-injured" 
        title="Patient Encounter" 
        value="patientEncounter" 
        to="/patient-encounter/"
        :class="{ 'v-list-item--active': $route.path.startsWith('/patient-encounter/') }"
        ></v-list-item>
      </v-list>
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
    props:{
      drawer:{
        type: Boolean,
        default: false,
      }
    },
    components:{
      VNavigationDrawer, VList, VListItem, VDivider, VAvatar,
    },
    data() {
      return {
        currenColor: '',
        isNurse: false,
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
            this.isHealthcareAdministrator = this.$myresources.user.roles.some(value => value.role == 'Healthcare Administrator')
            this.isNurse = this.$myresources.user.roles.some(value => value.role == 'Nursing User')
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
    }
  };
</script>

<style>
.v-list--nav > .v-list-item:hover {
  color: unset;
}
</style>