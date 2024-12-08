import frappe
import time

@frappe.whitelist()
def update_sourced_by():
    # Fetch the records from the Approved Dump where sourced_by is either empty or "Unknown"
    approved_dump_records = frappe.db.sql("""
        SELECT name, reference_no, sourced_by
        FROM `tabApproved Dump`
        WHERE (sourced_by IS NULL OR sourced_by = 'Unknown')
    """, as_dict=True)

    for record in approved_dump_records:
        # Fetch the matching record from Case Punching based on reference_no
        case_punching = frappe.db.sql("""
            SELECT employee_name
            FROM `tabCase Punching`
            WHERE reference_no = %s
        """, (record['reference_no']), as_dict=True)

        # Check if a match is found
        if case_punching:
            # If a match is found, update sourced_by with employee_name
            employee_name = case_punching[0]['employee_name']
            frappe.db.sql("""
                UPDATE `tabApproved Dump`
                SET sourced_by = %s
                WHERE name = %s
            """, (employee_name, record['name']))
            frappe.db.commit()
        else:
            # If no match is found, update sourced_by with "Unknown"
            frappe.db.sql("""
                UPDATE `tabApproved Dump`
                SET sourced_by = 'Unknown'
                WHERE name = %s
            """, (record['name']))
            frappe.db.commit()

        # Optional: Add a small delay to prevent overwhelming the server with requests
        time.sleep(0.1)

@frappe.whitelist()
def enqueue_update_sourced_by():
    # Enqueue the function to be run asynchronously as an RQ job
    frappe.enqueue(update_sourced_by, queue='long')
