frappe.listview_settings['Adobe Dump'] = {
    onload: function(listview) {
        $('.layout-side-section').hide();
        $('.layout-main-section-wrapper, .layout-main-section').css('margin-left', '0');
        $('.page-container').addClass('no-sidebar');

        listview.page.add_inner_button(__('Update Status'), function() {
            frappe.call({
                method: 'credlawn.scripts.create_adobe_dump_from_import.create_adobe_dump_records',
                callback: function(response) {
                    frappe.msgprint(response.message || __('No message returned.'));
                },
                error: function(err) {
                    frappe.msgprint(__('Error: ') + err.message);
                }
            });
        });
    }
};
