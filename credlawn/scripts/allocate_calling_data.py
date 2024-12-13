import frappe
import json
from frappe.utils import cint, flt, today
from frappe import _

@frappe.whitelist()
def allocate_data(num_leads, employees):
    try:
        employees = json.loads(employees)
    except json.JSONDecodeError as e:
        frappe.throw(_('Error decoding employees JSON: {0}').format(str(e)))

    try:
        if isinstance(num_leads, str):
            num_leads = json.loads(num_leads)
    except json.JSONDecodeError as e:
        frappe.throw(_('Error decoding num_leads JSON: {0}').format(str(e)))

    calling_data_records = frappe.get_all('Calling Data', 
                                          filters={'name': ['in', num_leads]}, 
                                          fields=['name', 'usage_count', 'date_1', 'date_2', 'date_3', 'date_4', 'date_5', 'date_6', 'date_7', 'date_8', 'date_9', 'date_10',
                                                  'employee_1', 'employee_2', 'employee_3', 'employee_4', 'employee_5', 'employee_6', 'employee_7', 'employee_8', 'employee_9', 'employee_10'])

    if not calling_data_records:
        frappe.throw(_('No calling data records selected.'))

    num_employees = len(employees)
    
    if num_employees == 0:
        frappe.throw(_('At least one employee must be selected.'))

    leads_per_employee = len(calling_data_records) 
    remainder = len(calling_data_records) % num_employees
    
    assigned_count = 0
    for idx, employee in enumerate(employees):
        if 'employee' not in employee:
            frappe.throw(_('Missing employee ID for assignment.'))
        
        employee_id = employee['employee']
        
        employee_details = frappe.get_value('Employee', employee_id, ['employee_name', 'email'], as_dict=True)
        
        if not employee_details:
            frappe.throw(_('Employee not found: {0}').format(employee_id))
        
        employee_name = employee_details.employee_name
        employee_email = employee_details.email
        
        if idx < remainder:
            leads_for_employee = leads_per_employee + 1
        else:
            leads_for_employee = leads_per_employee
        
        for i in range(assigned_count, assigned_count + leads_for_employee):
            lead = calling_data_records[i]

            frappe.db.set_value('Calling Data', lead['name'], 'employee', employee_id)
            frappe.db.set_value('Calling Data', lead['name'], 'employee_name', employee_name)
            frappe.db.set_value('Calling Data', lead['name'], 'email', employee_email)
            frappe.db.set_value('Calling Data', lead['name'], 'data_segment', 'Used')

            # Increment the usage_count by 1
            new_usage_count = lead['usage_count'] + 1 if lead['usage_count'] else 1
            frappe.db.set_value('Calling Data', lead['name'], 'usage_count', new_usage_count)
            
            for date_field in ['date_1', 'date_2', 'date_3', 'date_4', 'date_5', 'date_6', 'date_7', 'date_8', 'date_9', 'date_10']:
                if not lead[date_field]:
                    frappe.db.set_value('Calling Data', lead['name'], date_field, today())
                    break

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
