frappe.listview_settings['Blasting'] = {
    onload: function(listview) {
        $('.layout-side-section').hide();
        $('.layout-main-section-wrapper, .layout-main-section').css('margin-left', '0');
        $('.page-container').addClass('no-sidebar');
        
        listview.page.add_inner_button(__('Assign Lead'), function() {
            var dialog = new frappe.ui.Dialog({
                title: __('How Many Leads to Assign?'),
                fields: [
                    { fieldtype: 'Int', label: __('Number of Leads'), fieldname: 'num_leads', reqd: 1 }
                ],
                primary_action_label: __('Assign Now'),
                primary_action: function() {
                    var num_leads = dialog.get_value('num_leads');
                    frappe.confirm(
                        __('Are you sure you want to assign {0} leads?', [num_leads]),
                        function() {
                            frappe.call({
                                method: 'credlawn.scripts.assign_lead_mannually.assign_lead',
                                args: { num_leads: num_leads },
                                callback: function(response) {
                                    frappe.msgprint(response.message);
                                    dialog.hide();
                                }
                            });
                        },
                        function() {
                            dialog.hide();
                        }
                    );
                }
            });
            dialog.show();
        });
    }
};
