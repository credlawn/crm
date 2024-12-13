frappe.ui.form.on('Database', {
    refresh: function(frm) {
        set_fields_readonly(frm);
        frm.add_custom_button(__('Edit Details'), function() {
            toggle_edit_mode(frm);
        });
    }
});

function set_fields_readonly(frm) {
    ['customer_name', 'email', 'city', 'company_name', 'mobile_no', 'data_source', 'ctc'].forEach(field => {
        if (frm.doc[field]) frm.fields_dict[field].$input.prop('readonly', true);
    });
}

function toggle_edit_mode(frm) {
    const is_readonly = frm.fields_dict['customer_name'].$input.prop('readonly');
    const fields = ['customer_name', 'email', 'city', 'company_name', 'mobile_no', 'data_source', 'ctc'];
    
    fields.forEach(field => frm.fields_dict[field].$input.prop('readonly', !is_readonly));
    if (!is_readonly) set_fields_readonly(frm);
}
