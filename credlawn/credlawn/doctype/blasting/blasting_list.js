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
                    var data_code = selected_item['campaign_date'] + selected_item['lead_type'];
                    var lead_id = selected_item['name'];  // The unique identifier for the Blasting record

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
                                // Insert new record into Calling Data
                                frappe.call({
                                    method: 'frappe.client.insert',
                                    args: {
                                        doc: {
                                            doctype: 'Calling Data',
                                            customer_name: customer_name,
                                            mobile_no: mobile_no,
                                            data_code: data_code
                                        }
                                    },
                                    callback: function() {
                                        // After the lead is successfully transferred, update lead_assigned to 'Yes'
                                        frappe.call({
                                            method: 'frappe.client.set_value',
                                            args: {
                                                doctype: 'Blasting',
                                                name: lead_id,  // The Blasting record to be updated
                                                fieldname: 'lead_assigned',
                                                value: 'Yes'
                                            },
                                            callback: function() {
                                                successCount++;

                                                // Notify user when all records have been processed
                                                if (successCount + existingCount === selected_items.length) {
                                                    frappe.msgprint(__('Successfully Transferred ' + successCount + ' Records and ' + existingCount + ' Records already exist.'));
                                                }
                                            },
                                            error: function(error) {
                                                frappe.msgprint(__('Error updating lead_assigned field: ' + error.message));
                                                frappe.log_error(__('Error updating lead_assigned field: ' + error.message), 'Transfer Lead Error');
                                            }
                                        });
                                    },
                                    error: function(error) {
                                        frappe.msgprint(__('Error during lead transfer: ' + error.message));
                                        frappe.log_error(__('Error during lead transfer: ' + error.message), 'Transfer Lead Error');
                                    }
                                });
                            } else {
                                // If the lead already exists in Calling Data
                                existingCount++;

                                if (successCount + existingCount === selected_items.length) {
                                    frappe.msgprint(__('Successfully Transferred ' + successCount + ' Records and ' + existingCount + ' Records already exist.'));
                                }
                            }
                        },
                        error: function(error) {
                            frappe.msgprint(__('Error fetching Calling Data: ' + error.message));
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
