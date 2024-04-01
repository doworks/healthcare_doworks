<template>
  <div class="sidebar pt-5" id="sidebar">
    <div class="sidebar-inner slimscroll">
      <!-- <perfect-scrollbar
        class="scroll-area"
        :settings="settings"
        @ps-scroll-y="scrollHanle"
      > -->
        <div id="sidebar-menu" class="sidebar-menu">
          <ul>
              <li :class="{ active: isActive('/doctor-dashboard') }">
                <router-link to="/doctor-dashboard">
                  <i class="fas fa-columns"></i>
                  <span >Dashboard</span>
                </router-link>
              </li>
              <li :class="{ active: isActive('/appointments') }">
                <router-link to="/appointments">
                  <i class="fas fa-calendar-check"></i>
                  <span >Appointments</span>
                </router-link>
              </li>
              <li :class="{ active: isActive('/my-patients') }">
                <router-link to="/my-patients">
                  <i class="fas fa-user-injured"></i>
                  <span >My Patients</span>
                </router-link>
              </li>
              <li :class="{ active: isActive('/schedule-timings') }">
                <router-link to="/schedule-timings">
                  <i class="fas fa-hourglass-start"></i>
                  <span >Schedule Timings</span>
                </router-link>
              </li>
              <li :class="{ active: isActive('/available-timings') }">
                <router-link to="/available-timings">
                  <i class="fas fa-clock"></i>
                  <span >Available Timings</span>
                </router-link>
              </li>
              <li :class="{ active: isActive('/invoices') }">
                <router-link to="/invoices">
                  <i class="fas fa-file-invoice"></i>
                  <span >Invoices</span>
                </router-link>
              </li>
              <li :class="{ active: isActive('/accounts') }">
                <router-link to="/accounts">
                  <i class="fas fa-file-invoice-dollar"></i>
                  <span >Accounts</span>
                </router-link>
              </li>
              <li :class="{ active: isActive('/reviews') }">
                <router-link to="/reviews">
                  <i class="fas fa-star"></i>
                  <span >Reviews</span>
                </router-link>
              </li>
              <li :class="{ active: isActive('/chat-doctor') }">
                <router-link to="/chat-doctor">
                  <i class="fas fa-comments"></i>
                  <span >Message</span>
                  <small class="unread-msg">23</small>
                </router-link>
              </li>
              <li :class="{ active: isActive('/doctor-profile-settings') }">
                <router-link to="/doctor-profile-settings">
                  <i class="fas fa-user-cog"></i>
                  <span >Profile Settings</span>
                </router-link>
              </li>
              <li :class="{ active: isActive('/social-media') }">
                <router-link to="/social-media">
                  <i class="fas fa-share-alt"></i>
                  <span >Social Media</span>
                </router-link>
              </li>
              <li :class="{ active: isActive('/doctor-change-password') }">
                <router-link to="/doctor-change-password">
                  <i class="fas fa-lock"></i>
                  <span >Change Password</span>
                </router-link>
              </li>
              <li :class="{ active: isActive('/') }">
                <router-link to="/">
                  <i class="fas fa-sign-out-alt"></i>
                  <span >Logout</span>
                </router-link>
              </li>
            </ul>
        </div>
      <!-- </perfect-scrollbar> -->
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      activeClass: "active",
      settings: {
        suppressScrollX: true,
      },
    };
  },
  methods: {
    isActive(paths) {
      return paths.includes(this.$route.path);
    },
  },
};
</script>
