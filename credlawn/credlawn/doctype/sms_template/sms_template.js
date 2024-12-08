frappe.ui.form.on('SMS Template', {
    refresh: function(frm) {
        set_readonly_fields(frm);
    },
    onload: function(frm) {
        set_readonly_fields(frm);
    }
});

function set_readonly_fields(frm) {
    const fields_to_check = ['template_id', 'sender_id', 'dlt_template_id', 'status', 'template_id', 'template_type', 
                            'var_1', 'var_2', 'var_3', 'var_4', 'content'];

    
    fields_to_check.forEach(field => {
        if (frm.doc[field] && !frm.doc.__islocal) {
            frm.set_df_property(field, 'read_only', 1);
        }
    });
}


