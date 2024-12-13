frappe.ui.form.on('Adobe Database', {
    refresh: function(frm) {
        set_readonly_fields(frm);
        add_edit_button(frm);
    },
    onload: function(frm) {
        set_readonly_fields(frm);
    }
});

function set_readonly_fields(frm) {
    const fields_to_check = [
        'creation_date', 'final_decision_date', 'customer_name', 'customer_type', 'city', 'promo_code', 
        'state', 'company_name', 'ipa_status', 'idcom_status', 'current_status', 'qde_status', 
        'dap_final_flag', 'surrogate_eligibility', 'dropoff_reason', 'inprocess_classification', 
        'kyc_type', 'bkyc_status', 'vkyc_status', 'bkyc_status_reason', 'vkyc_link', 'classification', 
        'vkyc_expire_date', 'product_code', 'decline_type', 'curable_flag', 'decline_code', 'restart_flag', 
        'decline_description', 'etb_nb_succ_flag', 'final_decision', 'pin_code', 'channel', 'lg_code', 
        'dsa_code', 'lc1_code', 'lc2_code', 'login_month', 'duplicate_finder', 'decision_month', 
        'file_type', 'sm_code', 'company_code', 'reference_no'
    ];

    fields_to_check.forEach(field => {
        if (frm.doc[field] && !frm.doc.__islocal) {
            frm.set_df_property(field, 'read_only', 1);
        }
    });
}
