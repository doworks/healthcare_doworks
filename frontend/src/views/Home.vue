<template>
  <div>
	<h1>Home Page</h1>
	<!-- Fetch the resource on click -->
	<button @click="$myresources.ping.fetch()">Ping</button>
  </div>
</template>

<script>
export default {
  myresources: {
	ping() {
	  return {
		method: "frappe.ping", // Method to call on backend
		onSuccess(d) {
		  alert(d);
		},
	  };
	},
  },
};
</script>
