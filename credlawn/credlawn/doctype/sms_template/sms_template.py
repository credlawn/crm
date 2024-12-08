import frappe
from frappe.model.document import Document

class SMSTemplate(Document):
    
    def count_var_fields(self):
        return sum(1 for field in [self.var_1_name, self.var_2_name, self.var_3_name, self.var_4_name] if field)

    def on_update(self):
        frappe.db.set_value('SMS Template', self.name, 'variable_count', self.count_var_fields())
        self.reload()

    def after_insert(self):
        frappe.db.set_value('SMS Template', self.name, 'variable_count', self.count_var_fields())
