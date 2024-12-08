frappe.ui.form.on('Cards', {
    file_type: function(frm) {
        const filters = {
            'Team': { 
                'doctype': 'Employee', 
                'status_field': 'employment_status', 
                'status_value': 'Active', 
                'name_field': 'employee_name' 
            },
            'Vendor': { 
                'doctype': 'Vendor', 
                'status_field': 'vendor_status', 
                'status_value': 'Active', 
                'name_field': 'vendor_name' 
            },
            'Campaign': { 
                'doctype': 'Campaign', 
                'status_field': 'campaign_status', 
                'status_value': 'Active', 
                'name_field': 'campaign_name' 
            }
        };

        const selected_type = frm.doc.file_type;

        if (filters[selected_type]) {
            frm.set_value('source', filters[selected_type].doctype);
            frm.set_query('sourced_by', function() {
                return {
                    filters: {
                        [filters[selected_type].status_field]: filters[selected_type].status_value
                    }
                };
            });
        }

    },
    
    refresh: function(frm) {
        // Apply filter on sourced_by when the form is loaded
        if (frm.doc.file_type) {
            frm.trigger('file_type');
        }
    }
});
