import frappe
from frappe import _
from frappe.model.document import Document
import time

class Blasting(Document):

    def after_insert(self):
        # Fetch campaign data associated with this Blasting record
        campaign_data = frappe.db.get_value("Campaigndata", self.name, ["campaign_type", "campaign_date", "customer_name", "mob_no", "data_source"], as_dict=True)

        if campaign_data:
            # Assign values from the Campaign Data to the Blasting document
            self.campaign_type = campaign_data.campaign_type
            self.campaign_date = campaign_data.campaign_date
            self.customer_name = campaign_data.customer_name
            self.mobile_no = campaign_data.mob_no
            self.data_source = campaign_data.data_source
            
            self.save(ignore_permissions=True)
            frappe.db.commit()
            
        else:
            return
