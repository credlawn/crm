frappe.listview_settings['Blasting'] = {
    onload: function(listview) {
        $('.layout-side-section').hide();
        $('.layout-main-section-wrapper, .layout-main-section').css('margin-left', '0');
        $('.page-container').addClass('no-sidebar');
        
        listview.page.add_inner_button(__('Transfer Leads'), function() {
            var selected_items = listview.get_checked_items();
            
            if (selected_items.length === 0) {
                frappe.msgprint(__('Please select a record.'));
                return;
            }

            var successCount = 0;
            var existingCount = 0;

            try {
                selected_items.forEach(function(selected_item, index) {
                    if (!selected_item['mobile_no']) {
                        frappe.log_error(__('Mobile number is missing in the selected record at index ' + index), 'Transfer Lead Error');
                        return;
                    }

                    var mobile_no = selected_item['mobile_no'];
                    var customer_name = selected_item['customer_name'];

                    if (!customer_name) {
                        frappe.log_error(__('Customer name is missing in the selected record at index ' + index), 'Transfer Lead Error');
                        return;
                    }

                    frappe.call({
                        method: 'frappe.client.get_list',
                        args: {
                            doctype: 'Calling Data',
                            filters: { 'mobile_no': mobile_no },
                            fields: ['name']
                        },
                        callback: function(data) {
                            if (data.message && data.message.length === 0) {
                                frappe.call({
                                    method: 'frappe.client.insert',
                                    args: {
                                        doc: {
                                            doctype: 'Calling Data',
                                            customer_name: customer_name,
                                            mobile_no: mobile_no
                                        }
                                    },
                                    callback: function() {
                                        successCount++;

                                        if (successCount + existingCount === selected_items.length) {
                                            frappe.msgprint(__('Successfully Transferred ' + successCount + ' Records and ' + existingCount + ' Records already exist.'));
                                        }
                                    },
                                    error: function(error) {
                                        frappe.log_error(__('Error during lead transfer: ' + error.message), 'Transfer Lead Error');
                                    }
                                });
                            } else {
                                existingCount++;

                                if (successCount + existingCount === selected_items.length) {
                                    frappe.msgprint(__('Successfully Transferred ' + successCount + ' Records and ' + existingCount + ' Records already exist.'));
                                }
                            }
                        },
                        error: function(error) {
                            frappe.log_error(__('Error fetching Calling Data: ' + error.message), 'Transfer Lead Error');
                        }
                    });
                });
            } catch (error) {
                frappe.log_error(__('Unexpected error: ' + error.message), 'Transfer Lead Error');
            }
        });
    }
};
