from frappe.model.document import Document
import frappe

class AdobeDatabase(Document):
    
    def after_insert(self):
        self.update_employee_name_and_decline_code()
    
    def on_update(self):
        self.update_employee_name_and_decline_code()
        self.reload()

    def update_employee_name_and_decline_code(self):
        case_punching = frappe.db.get_all('Case Punching', filters={'reference_no': self.reference_no}, fields=['employee_name', 'mobile_no', 'case_source'])
        
        if case_punching:
            case_punching_record = case_punching[0]
            frappe.db.set_value('Adobe Database', self.name, 'employee_name', case_punching_record.get('employee_name', 'Not Mapped'))
            frappe.db.set_value('Adobe Database', self.name, 'mobile_no', case_punching_record.get('mobile_no', 'NA'))
            frappe.db.set_value('Adobe Database', self.name, 'case_source', case_punching_record.get('case_source', 'NA'))
        else:
            frappe.db.set_value('Adobe Database', self.name, 'employee_name', 'Not Mapped')
            frappe.db.set_value('Adobe Database', self.name, 'mobile_no', 'NA')
            frappe.db.set_value('Adobe Database', self.name, 'case_source', 'NA')
        
        if self.decline_code:
            decline_code_data = frappe.db.get_value('Decline Code', filters={'name': self.decline_code}, fieldname=['final_remarks', 'sales_action_required'])
            
            
            if decline_code_data:
                final_remarks, sales_action_required = decline_code_data
                frappe.db.set_value('Adobe Database', self.name, 'final_stage', final_remarks)
                frappe.db.set_value('Adobe Database', self.name, 'action_required', sales_action_required)

