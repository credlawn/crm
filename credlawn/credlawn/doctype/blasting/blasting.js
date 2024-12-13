frappe.ui.form.on('Blasting', {
    onload: function(frm) {
        $(frm.wrapper).find('.help-box.small.text-muted').hide();

        if (!frm.is_new()) {
            const fields = ['lead_status', 'campaign_date', 'cr_date', 'lead_type', 'campaign_type', 'customer_name', 'mobile_no', 'city', 'data_source'];
            fields.forEach(field => {
                frm.set_df_property(field, 'read_only', frm.doc[field] ? true : false);
            });
        }
    },

    refresh: function(frm) {
        if (frm.doc.lead_assigned === 'Hold') {
            frm.add_custom_button(__('Assign This Lead'), function() {
                frappe.confirm(
                    __('Are You Sure Want to Assign this Lead?'),
                    () => {
                        frm.set_value('lead_assigned', 'No');
                        frm.save();
                    },
                    () => {}
                );
            });
        }
    }
});
