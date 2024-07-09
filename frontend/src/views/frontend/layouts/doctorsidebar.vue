<template>
    <v-navigation-drawer
      expand-on-hover
      rail
      color="indigo"
      mobile-breakpoint="none"
    >
      <v-list>
        <v-list-item :title="$resources.user.name">
          <template #prepend>
            <v-avatar :color="!$resources.user.image ? currenColor : ''">
              <img
                v-if="$resources.user.image"
                class="h-100 w-100"
                :src="$resources.user.image"
              />
              <span v-if="!$resources.user.image" class="text-h5">{{ $resources.user.name ? $resources.user.name[0] : '' }}</span>
            </v-avatar>
          </template>
        </v-list-item>
      </v-list>

      <v-divider></v-divider>

      <v-list nav>
        <v-list-item prepend-icon="fa fa-display" title="Dashboard" value="doctorDashboard" nav to="/doctor-dashboard"></v-list-item>
        <v-list-item prepend-icon="fa fa-display" title="Dashboard" value="nurseDashboard" nav to="/nurse-dashboard"></v-list-item>
        <v-list-item prepend-icon="fa fa-calendar-check" title="Appointments" value="appointments" to="/appointments"></v-list-item>
        <v-list-item prepend-icon="fa fa-user-injured" title="Patient Encounter" value="patientEncounter" to="/patient-encounter-list"></v-list-item>
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
    inject:['$call'],
    props:{
      drawer:{
        type: Boolean,
        default: false,
      }
    },
    components:{
      VNavigationDrawer,
      VList,
      VListItem,
      VDivider,
      VAvatar,
    },
    data() {
      return {
        currenColor: '',
      };
    },
    watch: {
      '$resources.user': {
        handler(newValue) {
          if(this.$resources.user.name)
            this.currenColor = this.getColorFromName(this.$resources.user.name)
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