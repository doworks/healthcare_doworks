<template>
	<!-- <div>
		<button v-if="$auth.isLoggedIn" @click="$auth.logout()">Logout</button>
		<router-view />
	</div> -->
	<div id="app">
		<v-layout style="min-height: 100vh" v-if="$auth.isLoggedIn">
			<doctorsidebar/>
			<v-main class="pt-0 pt-sm-2 bg-gradient ps-20 overflow-hidden" id="body-main">
				<Toast position="bottom-right"/>
				<router-view />
			</v-main>
		</v-layout>
	</div>
</template>


<script>
import '@/assets/css/feather.css';
import 'frappe-ui/src/style.css';
// import '@/assets/css/prime.css';
// import '@/assets/css/custom.css';
import { VLayout } from 'vuetify/components/VLayout'
import { VMain } from 'vuetify/components/VMain'
export default {
	inject: ['$auth', '$socket'],
	components:{
		VLayout,
		VMain,
	},
	setup() {
		// loadStyles();

		// Your other setup logic
		// ...

		return {};
	},
	mounted(){
		// console.log(this.$auth)
		// console.log(this.$cardReader)
		// this.$cardReader.on('card_data', (data) => {
		// 	console.log('Received card data:', data);
		// });

		// this.$socket.on('session_logout', (data) => {
		// 	window.open('/');
		// });
	},
	data() {
		return {
		};
	},
	methods: {
	},
	name: "App",
};
</script>

<style>
html {
	font-size: 70% !important;
}
#body-main{
	background-color: papayawhip;
	padding-left: 70px;
	overflow-x: hidden;
}
.v-overlay__content{
	overflow: hidden;
}
@media (min-width: 576px) {
	#body-main{
		padding-left: 70px;
	}
}

/* Scroll bar stylings */
::-webkit-scrollbar {
  width: 10px;
  height: 10px;
}

/* Track */
::-webkit-scrollbar-track {
  background: var(--lightestgrey); 
}

/* Handle */
::-webkit-scrollbar-thumb {
  background: #888; 
  border-radius: 5px;
}

/* Handle on hover */
::-webkit-scrollbar-thumb:hover {
  background: #555; 
}
</style>