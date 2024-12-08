frappe.query_reports["Employee Birthday"] = {
	"filters": [
		{
			"fieldname": "birthday_month",
			"label": __("Birthday Month"),
			"fieldtype": "Select",
			"options": "\nJanuary\nFebruary\nMarch\nApril\nMay\nJune\nJuly\nAugust\nSeptember\nOctober\nNovember\nDecember",
			"reqd": 1, 
		},
		{
			"fieldname": "employment_status",
			"label": __("Employee Status"),
			"fieldtype": "Select",
			"options": "\nActive\nInactive",
		}
	],
	
	validate: function() {
		if (!this.get_values().birthday_month) {
			frappe.msgprint(__("Please select a birthday month"));
			return false; 
		}
	}
};
