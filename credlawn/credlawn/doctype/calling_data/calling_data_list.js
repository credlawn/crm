frappe.listview_settings['Calling Data'] = {
    onload: function(listview) {
        $('.layout-side-section').hide();
        $('.layout-main-section-wrapper, .layout-main-section').css('margin-left', '0');
        $('.page-container').addClass('no-sidebar');
        
        listview.page.add_inner_button(__('Allocate Data'), function() {
            var selected_items = listview.get_checked_items();
            
            if (selected_items.length === 0) {
                frappe.msgprint(__('Please select at least one record.'));
                return;
            }

            var dialog = new frappe.ui.Dialog({
                title: __('Select Employees for Assignment'),
                fields: [
                    {
                        fieldtype: 'Table MultiSelect',
                        label: __('Select Employees'),
                        fieldname: 'employees',
                        options: 'Employee Assignment',
                        reqd: 1,
                        allow_multiple: true,
                        get_query: function() {
                            return {
                                filters: {
                                    employment_status: 'Active'
                                }
                            };
                        }
                    }
                ],
                primary_action_label: __('Assign Now'),
                primary_action: function() {
                    var selected_employees = dialog.get_value('employees');
                    
                    if (!selected_employees || selected_employees.length === 0) {
                        frappe.msgprint(__('Please select at least one employee.'));
                        return;
                    }

                    // Check if the number of selected employees is greater than or equal to the number of selected records
                    if (selected_items.length < selected_employees.length) {
                        frappe.msgprint(__('The number of records are less than employees selected.'));
                        return;
                    }

                    frappe.confirm(
                        __('Are you sure you want to assign {0} leads to the selected employees?', [selected_items.length]),
                        function() {
                            // Pass the actual record names (IDs) instead of the length
                            frappe.call({
                                method: 'credlawn.scripts.allocate_calling_data.allocate_data',
                                args: { 
                                    num_leads: JSON.stringify(selected_items.map(item => item.name)),  // Pass record names as an array
                                    employees: JSON.stringify(selected_employees)  // Pass the list of employees as a JSON string
                                },
                                callback: function(response) {
                                    frappe.msgprint(response.message);
                                    dialog.hide();
                                    location.reload();
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
