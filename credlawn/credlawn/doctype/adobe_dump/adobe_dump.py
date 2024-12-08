import frappe
from frappe.model.document import Document

class AdobeDump(Document):
    def before_save(self):
        if self.customer_name:
            self.customer_name = self.customer_name.strip().title()
        if self.city:
            self.city = self.city.strip().title()
        if self.company_name:
            self.company_name = self.company_name.strip().title()
            
