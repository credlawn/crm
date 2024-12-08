import frappe
from frappe.model.document import Document

class Database(Document):
    def before_insert(self):
        if self.customer_name: self.customer_name = self.customer_name.title().strip()
        if self.email: self.email = self.email.lower().strip()
        if self.city: self.city = self.city.title().strip()
        if self.company_name: self.company_name = self.company_name.title().strip()
        if self.mobile_no:
            self.mobile_no = ''.join(filter(str.isdigit, self.mobile_no))
            if len(self.mobile_no) != 10:
                frappe.throw("Mobile number must be 10 digits.")

    def after_insert(self):
        self.update_status()
        self.count_platform_usage()

    def on_update(self):
        self.update_status()
        self.count_platform_usage()

    def update_status(self):
        # Check platform fields for WhatsApp, SMS, RCS
        if any(platform and 'WhatsApp' in platform for platform in [self.platform_1, self.platform_2, self.platform_3, 
                                                                  self.platform_4, self.platform_5, self.platform_6, 
                                                                  self.platform_7, self.platform_8, self.platform_9, 
                                                                  self.platform_10]):
            self.db_set('whatsapp_status', 'Used')
        if any(platform and 'SMS' in platform for platform in [self.platform_1, self.platform_2, self.platform_3, 
                                                              self.platform_4, self.platform_5, self.platform_6, 
                                                              self.platform_7, self.platform_8, self.platform_9, 
                                                              self.platform_10]):
            self.db_set('sms_status', 'Used')
        if any(platform and 'RCS' in platform for platform in [self.platform_1, self.platform_2, self.platform_3, 
                                                             self.platform_4, self.platform_5, self.platform_6, 
                                                             self.platform_7, self.platform_8, self.platform_9, 
                                                             self.platform_10]):
            self.db_set('rcs_status', 'Used')


        if all([self.sms_status == 'Used', self.rcs_status == 'Used', self.whatsapp_status == 'Used']):
            self.db_set('overall_status', 'Used')
        elif any([self.sms_status == 'Used', self.rcs_status == 'Used', self.whatsapp_status == 'Used']):
            self.db_set('overall_status', 'Partial Used')
        else:
            self.db_set('overall_status', 'New')

    def count_platform_usage(self):
        platform_usage_count = sum([
            1 if self.sms_status == 'Used' else 0,
            1 if self.rcs_status == 'Used' else 0,
            1 if self.whatsapp_status == 'Used' else 0
        ])
        self.db_set('platform_usage_count', platform_usage_count)
        
        usage_count = sum([1 for platform in [self.platform_1, self.platform_2, self.platform_3, self.platform_4, 
                                              self.platform_5, self.platform_6, self.platform_7, self.platform_8, 
                                              self.platform_9, self.platform_10] if platform])
        self.db_set('usage_count', usage_count)
