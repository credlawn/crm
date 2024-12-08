frappe.ui.form.on('SMS Delivery', {
    refresh: function(frm) {
        // Add a custom button to the form
        frm.add_custom_button(__('Send SMS'), function() {
            // Call the send_sms function from the server-side when the button is clicked
            send_sms_api(frm);
        });
    }
});

// Function to call the server-side method send_sms
function send_sms_api(frm) {
    // Make the server-side call to the send_sms function
    frappe.call({
        method: "credlawn.scripts.send_sms_campaign.send_sms",  // Replace with the actual path to the send_sms method
        args: {},  // No arguments needed as the values are static in the Python code
        callback: function(response) {
            if (response.message === "success") {
                frappe.msgprint(__('SMS Sent Successfully'));
            } else {
                frappe.msgprint(__('Failed to Send SMS'));
            }
        }
    });
}
