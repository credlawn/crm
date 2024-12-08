frappe.ui.form.on('Employee', {
    refresh: function(frm) {
        set_readonly_fields(frm);
        add_edit_button(frm);
    },
    onload: function(frm) {
        set_readonly_fields(frm);
    }
});

function set_readonly_fields(frm) {
    const fields_to_check = ['employee_name', 'joining_date', 'date_of_birth', 'gender', 'department',
                                'designation', 'grade', 'branch', 'mobile_no', 'email', 'fixed_salary',
                                'account_no', 'ifsc_code', 'employment_status', 'last_working_date', 'payment_proof',
                                'reason_for_leaving', 'tenure', 'fnf_status', 'final_amount', 'payment_date', 'remarks'
                            ];
    
    fields_to_check.forEach(field => {
        if (frm.doc[field] && !frm.doc.__islocal) {
            frm.set_df_property(field, 'read_only', 1);
        }
    });
}

function add_edit_button(frm) {
    frm.add_custom_button(__('Edit Details'), function() {
        const fields_to_edit = ['employee_name', 'joining_date', 'date_of_birth', 'gender', 'department',
                                'designation', 'grade', 'branch', 'mobile_no', 'email', 'fixed_salary',
                                'account_no', 'ifsc_code', 'employment_status', 'last_working_date', 'reason_for_leaving',
                                'fnf_status', 'final_amount', 'payment_date', 'remarks', 'payment_proof'
                            ];

        fields_to_edit.forEach(field => {
            frm.set_df_property(field, 'read_only', 0);
        });
        
        // Optionally change the button text to indicate editing mode
        frm.set_custom_button(__('Edit Details'), __('Save Details'), function() {
            // Save the document after editing
            frm.save();
        });
    });
}
