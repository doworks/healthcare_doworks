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
              <span v-if="!$resources.user.image" class="text-h5">{{ getInitials($resources.user.name) }}</span>
            </v-avatar>
          </template>
        </v-list-item>
      </v-list>

      <v-divider></v-divider>

      <v-list nav>
        <v-list-item prepend-icon="fa fa-display" title="Dashboard" value="myfiles" nav to="/doctor-dashboard"></v-list-item>
        <v-list-item prepend-icon="fa fa-calendar-check" title="Appointments" value="shared" to="/appointments"></v-list-item>
        <!-- <v-list-item prepend-icon="fa fa-user-injured" title="Patient Encounter" value="starred" :to="{ name: 'patient-encounter' }"></v-list-item> -->
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
    mounted() {
      this.currenColor = this.randomColors()
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
      randomColors() {
        return colors[Math.floor(Math.random() * colors.length)];
      },
    }
  };
</script>

<style>
.v-list--nav > .v-list-item:hover {
  color: unset;
}
</style>