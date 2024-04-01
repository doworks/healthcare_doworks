<template>
    <v-navigation-drawer
      expand-on-hover
      rail
      color="indigo"
      mobile-breakpoint="none"
    >
      <v-list>
        <v-list-item
          prepend-avatar="https://randomuser.me/api/portraits/women/85.jpg"
          title="Sandra Adams"
        >
        </v-list-item>
      </v-list>

      <v-divider></v-divider>

      <v-list nav>
        <v-list-item prepend-icon="fa fa-display" title="Dashboard" value="myfiles" nav to="/doctor-dashboard"></v-list-item>
        <v-list-item prepend-icon="fa fa-calendar-check" title="Appointments" value="shared" to="/appointments"></v-list-item>
        <v-list-item prepend-icon="fa fa-user-injured" title="Patient Encounter" value="starred" to="/patient-encounter"></v-list-item>
      </v-list>
    </v-navigation-drawer>
</template>

<script>
  import { VNavigationDrawer } from 'vuetify/components/VNavigationDrawer'
  import { VList, VListItem } from 'vuetify/components/VList'
  import { VDivider } from 'vuetify/components/VDivider'

  export default{
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
    },
    data() {
      return {
      };
    },
  };
</script>

<style>
.v-list--nav > .v-list-item:hover {
  color: unset;
}
</style>