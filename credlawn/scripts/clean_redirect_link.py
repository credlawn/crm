import frappe

def delete_redirect_link():
    try:
        campaign_names_set = {campaign['name'] for campaign in frappe.get_all('Campaigndata', fields=['name'])}

        redirects_to_delete = frappe.get_all(
            'Website Route Redirect',
            filters={'source': ['not in', list(campaign_names_set)]},
            fields=['name', 'source']
        )

        valid_sources = {'hdfc', 'tata', 'swiggy', 'campt', 'camph', 'camps'}

        for redirect in redirects_to_delete:
            try:
                source = str(redirect['source']).strip().lower()
                if source not in valid_sources:
                    frappe.delete_doc('Website Route Redirect', redirect['name'])
            except Exception:
                pass
        
        frappe.db.commit()

    except Exception:
        pass
