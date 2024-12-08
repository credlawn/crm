import frappe

@frappe.whitelist()
def assign_lead(num_leads):

    leads = frappe.get_all('Blasting', filters={'lead_assigned': 'Hold'}, fields=['name'], limit=num_leads, order_by='creation asc')

    if leads:

        lead_names = [lead.name for lead in leads]
        frappe.db.set_value('Blasting', lead_names, 'lead_assigned', 'No')

        return {
            'message': f'{len(leads)} leads have been successfully assigned.'
        }
    else:
        return {
            'message': 'No leads found to assign.'
        }
