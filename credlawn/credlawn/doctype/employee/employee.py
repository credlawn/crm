import frappe
from frappe.model.document import Document

class Employee(Document):
    def after_insert(self):
        # Removed age calculation
        pass

    def on_update(self):
        # Removed age calculation
        self.refresh()

    def refresh(self):
        self.reload()
