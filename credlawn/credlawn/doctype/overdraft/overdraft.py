import frappe
from frappe.model.document import Document
from frappe.utils import getdate, formatdate

class Overdraft(Document):


    def after_insert(self):
        self.calculate_amount()
        frappe.db.commit()

    def on_update(self):
        self.calculate_amount()
        frappe.db.commit()
        self.reload()

    def calculate_amount(self):
        if not self.loan_amount or not self.commission_percentage:
            frappe.throw("Please fill in Loan Amount & Commission Percentage.")

        self.commission_before_gst = self.loan_amount * self.commission_percentage / 100 - self.pf_deduction
        self.gst_amount = self.commission_before_gst * 0.18
        self.commission_with_gst = self.commission_before_gst + self.gst_amount
        self.tds_amount = self.commission_before_gst * self.tds / 100
        self.net_commission_amount = self.commission_with_gst - self.tds_amount
        self.vendor_commission_amount = self.loan_amount * self.vendor_percentage / 100 - self.pf_deduction
        self.vendor_tds_amount = self.vendor_commission_amount * self.tds / 100
        self.vendor_net_amount = self.vendor_commission_amount - self.vendor_tds_amount  
        self.earned_gst_amount = self.gst_amount
        self.extra_tds_amount = self.commission_before_gst * 0.03
        self.net_profit_amount = self.earned_gst_amount + self.extra_tds_amount

        
        if self.vendor_actual_paid_amount is None or self.vendor_actual_paid_amount == 0.00:
            self.vendor_actual_paid_amount = self.vendor_net_amount

        self.balance_amount_with_gst = self.net_commission_amount - self.vendor_actual_paid_amount
        self.balance_amount_without_gst = self.balance_amount_with_gst - self.gst_amount
        self.commission_credit_amount = self.commission_before_gst -self.tds_amount + self.extra_tds_amount

        if self.dispatch_date:
            dispatch_date = getdate(self.dispatch_date)
            self.business_month = dispatch_date.strftime("%b'%y")
        else:
            frappe.throw("Dispatch Date is required to update Business Month.")
        
        # Set the calculated values to the database
        frappe.db.set_value('Overdraft', self.name, 'commission_before_gst', self.commission_before_gst)
        frappe.db.set_value('Overdraft', self.name, 'gst_amount', self.gst_amount)
        frappe.db.set_value('Overdraft', self.name, 'commission_with_gst', self.commission_with_gst)
        frappe.db.set_value('Overdraft', self.name, 'tds_amount', self.tds_amount)
        frappe.db.set_value('Overdraft', self.name, 'net_commission_amount', self.net_commission_amount)
        frappe.db.set_value('Overdraft', self.name, 'vendor_commission_amount', self.vendor_commission_amount)
        frappe.db.set_value('Overdraft', self.name, 'vendor_tds_amount', self.vendor_tds_amount)
        frappe.db.set_value('Overdraft', self.name, 'vendor_net_amount', self.vendor_net_amount)
        frappe.db.set_value('Overdraft', self.name, 'balance_amount_with_gst', self.balance_amount_with_gst)
        frappe.db.set_value('Overdraft', self.name, 'balance_amount_without_gst', self.balance_amount_without_gst)
        frappe.db.set_value('Overdraft', self.name, 'earned_gst_amount', self.earned_gst_amount)
        frappe.db.set_value('Overdraft', self.name, 'extra_tds_amount', self.extra_tds_amount)
        frappe.db.set_value('Overdraft', self.name, 'net_profit_amount', self.net_profit_amount)
        frappe.db.set_value('Overdraft', self.name, 'business_month', self.business_month)
        frappe.db.set_value('Overdraft', self.name, 'vendor_actual_paid_amount', self.vendor_actual_paid_amount)
        frappe.db.set_value('Overdraft', self.name, 'commission_credit_amount', self.commission_credit_amount)
