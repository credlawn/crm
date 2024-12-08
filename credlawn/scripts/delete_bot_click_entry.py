import frappe

def delete_bot_click_records():

    redirects = frappe.get_all('Redirect', filters={'browser': ['like', '%bot%']})


    deleted_count = 0
    

    for redirect in redirects:
        redirect_doc = frappe.get_doc('Redirect', redirect.name)
        
        if redirect_doc.browser and any(bot_word in redirect_doc.browser.lower() for bot_word in ['bot', 'googlebot']):
            frappe.delete_doc('Redirect', redirect.name)
            deleted_count += 1


    frappe.log("Deleted {} Redirect records with 'bot' in the browser field.".format(deleted_count))
