import frappe
from frappe.model.document import Document
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@frappe.whitelist()
def process_svkyc_link_records():
    records_to_process = frappe.get_all(
        "SVKYC Link",
        filters={"no_updated": ["is", "not set"]},
        fields=["name", "svkyc_link"]
    )
    
    for record in records_to_process:
        frappe.enqueue(
            fetch_and_update_mobile_no, 
            record_name=record.name, 
            queue='default', 
            timeout=3600  # Timeout of 1 hour (3600 seconds)
        )

@frappe.whitelist()
def fetch_and_update_mobile_no(record_name):
    try:
        svkyc_link_doc = frappe.get_doc("SVKYC Link", record_name)
        svkyc_url = svkyc_link_doc.svkyc_link

        if not svkyc_url:
            frappe.msgprint(f"No SVKYC Link found for record {record_name}.")
            return

        # Setting up the headless browser
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in headless mode (no UI)
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

        # Open the URL in the Selenium-controlled browser
        driver.get(svkyc_url)

        try:
            # Wait until the mobile number input field is loaded (up to 10 seconds)
            input_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "txtmissing_18"))
            )

            # Fetch the mobile number from the input field
            mobile_no = input_field.get_attribute("value")

            if mobile_no:
                # Mobile number found, update the no_updated field to 'Yes'
                svkyc_link_doc.mobile_no = mobile_no
                svkyc_link_doc.no_updated = "Yes"
            else:
                # Mobile number not found, update the no_updated field to 'Not Found'
                svkyc_link_doc.no_updated = "Not Found"
        except Exception as e:
            # If the element isn't found or another error occurs, mark as 'Not Found'
            svkyc_link_doc.no_updated = "Not Found"

        # Save the updated record
        svkyc_link_doc.save()

        # Close the Selenium driver
        driver.quit()

    except Exception as e:
        # In case of an unexpected error, mark as 'Not Found'
        svkyc_link_doc.no_updated = "Not Found"
        svkyc_link_doc.save()
