$(document).ready(function() {
    frappe.call({
        method: "healthcare_doworks.api.methods.get_redirect_url",
        async: false,  // Synchronous call to ensure it happens immediately
        callback: function(r) {
            if (r.message && r.message.redirect_to) {
                // Check if the current page is not already the target page
                if (window.location.pathname !== r.message.redirect_to) {
                    window.location.href = r.message.redirect_to;
                }
            }
        }
    });
});