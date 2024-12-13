import frappe
from frappe.model.document import Document

class Invoice(Document):
    def after_insert(self):
        self.calculate_totals()

    def on_update(self):
        self.calculate_totals()

    def calculate_totals(self):
        self.gst_amount = self.pre_gst_amount * self.gst_percentage / 100
        self.total_bill_amount = self.pre_gst_amount + self.gst_amount
        self.round_off_amount = round(self.total_bill_amount)
        self.tds_amount = self.pre_gst_amount * self.tds_percentage / 100
        self.net_amount = self.total_bill_amount - self.tds_amount
        
        frappe.db.set_value('Invoice', self.name, 'total_bill_amount', self.total_bill_amount)
        frappe.db.set_value('Invoice', self.name, 'gst_amount', self.gst_amount)
        frappe.db.set_value('Invoice', self.name, 'round_off_amount', self.round_off_amount)
        frappe.db.set_value('Invoice', self.name, 'tds_amount', self.tds_amount)
        frappe.db.set_value('Invoice', self.name, 'net_amount', self.net_amount)
        
        frappe.db.commit() 
        self.reload() 
