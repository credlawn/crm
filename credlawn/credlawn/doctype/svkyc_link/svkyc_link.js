frappe.ui.form.on('SVKYC Link', {
    refresh: function(frm) {
        frm.add_custom_button('Fetch Mobile No', function() {
            frappe.call({
                method: 'credlawn.scripts.arun.fetch_and_update_mobile_no',
                args: {
                    'record_name': frm.doc.name
                },
                callback: function(response) {
                    if(response.message) {
                        frappe.msgprint(response.message);
                    }
                }
            });
        });
    }
});
