import frappe
import json
from frappe.utils import today
from frappe import _

@frappe.whitelist()
def allocate_data(num_leads, employees):
    try:
        # Decode input data safely
        employees = json.loads(employees)
        if isinstance(num_leads, str):
            num_leads = json.loads(num_leads)
    except json.JSONDecodeError as e:
        frappe.throw(_('Error decoding input data: {0}').format(str(e)))

    # Fetch calling data records
    calling_data_records = frappe.get_all('Calling Data', 
                                          filters={'name': ['in', num_leads]}, 
                                          fields=['name', 'usage_count', 'date_1', 'date_2', 'date_3', 'date_4', 'date_5', 'date_6', 'date_7', 'date_8', 'date_9', 'date_10',
                                                  'employee_1', 'employee_2', 'employee_3', 'employee_4', 'employee_5', 'employee_6', 'employee_7', 'employee_8', 'employee_9', 'employee_10'],
                                          limit_page_length=10000)

    # Ensure there are calling data records
    if not calling_data_records:
        frappe.throw(_('No calling data records found for the provided leads.'))

    num_employees = len(employees)
    if num_employees == 0:
        frappe.throw(_('At least one employee must be selected.'))

    # Calculate leads per employee
    leads_per_employee = len(calling_data_records) // num_employees
    remainder = len(calling_data_records) % num_employees

    assigned_count = 0
    for idx, employee in enumerate(employees):
        if 'employee' not in employee:
            frappe.throw(_('Missing employee ID for assignment.'))

        employee_id = employee['employee']
        
        # Fetch employee details
        employee_details = frappe.get_value('Employee', employee_id, ['employee_name', 'email'], as_dict=True)
        if not employee_details:
            frappe.throw(_('Employee not found: {0}').format(employee_id))
        
        employee_name = employee_details.employee_name
        employee_email = employee_details.email
        
        # Assign leads to the employee
        leads_for_employee = leads_per_employee + 1 if idx < remainder else leads_per_employee
        
        for i in range(assigned_count, assigned_count + leads_for_employee):
            if i >= len(calling_data_records):
                frappe.throw(_('Not enough leads available to allocate to all employees.'))
            
            lead = calling_data_records[i]

            # Update lead with employee details
            frappe.db.set_value('Calling Data', lead['name'], 'employee', employee_id)
            frappe.db.set_value('Calling Data', lead['name'], 'employee_name', employee_name)
            frappe.db.set_value('Calling Data', lead['name'], 'email', employee_email)
            frappe.db.set_value('Calling Data', lead['name'], 'data_segment', 'Used')

            # Increment usage count
            new_usage_count = (lead['usage_count'] or 0) + 1
            frappe.db.set_value('Calling Data', lead['name'], 'usage_count', new_usage_count)
            
            # Set date fields if not already set
            for date_field in ['date_1', 'date_2', 'date_3', 'date_4', 'date_5', 'date_6', 'date_7', 'date_8', 'date_9', 'date_10']:
                if not lead[date_field]:
                    frappe.db.set_value('Calling Data', lead['name'], date_field, today())
                    break

            # Set employee fields if not already set
            for employee_field in ['employee_1', 'employee_2', 'employee_3', 'employee_4', 'employee_5', 'employee_6', 'employee_7', 'employee_8', 'employee_9', 'employee_10']:
                if not lead[employee_field]:
                    frappe.db.set_value('Calling Data', lead['name'], employee_field, employee_name)
                    break
        
        assigned_count += leads_for_employee

    try:
        frappe.db.commit()
    except Exception as e:
        frappe.throw(_('Error while committing the data: {0}').format(str(e)))

    return {
        'message': _('Leads successfully allocated to the selected employees.')
    }
