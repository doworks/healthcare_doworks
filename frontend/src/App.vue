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
	provide() {
    return {
      $getList: (args) => {
		`Returns a list of records by filters, fields, ordering and limit

		:param doctype: DocType of the data to be queried
		:param fields: fields to be returned. Default is 'name'
		:param filters: filter list by this dict
		:param order_by: Order by this fieldname
		:param limit_start: Start at this index
		:param limit_page_length: Number of records to be returned (default 20)`
        return this.$call('frappe.client.get_list', args)
				.then(response => response)
				.catch(error => { console.log(error) });
      },
	  $getValue: (args) => {
		`Returns a value form a document

		:param doctype: DocType to be queried
		:param fieldname: Field to be returned (default 'name')
		:param filters: dict or string for identifying the record`
        return this.$call('frappe.client.get_value', args)
				.then(response => response)
				.catch(error => { console.log(error) });
      },
	  $validateLink: (args) => {
        return this.$call('frappe.client.validate_link', args)
				.then(response => response)
				.catch(error => { console.log(error) });
      },
	  $setValue: (args) => {
		`Set a value using get_doc, group of values

		:param doctype: DocType of the document
		:param name: name of the document
		:param fieldname: fieldname string or JSON / dict with key value pair
		:param value: value if fieldname is JSON / dict`
        return this.$call('frappe.client.set_value', args)
				.then(response => response)
				.catch(error => { console.log(error) });
      },
    };
  },
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
	font-size: 75% !important;
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