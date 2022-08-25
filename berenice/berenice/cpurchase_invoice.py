import frappe

@frappe.whitelist()
def mncf_autoname(doc, method):
	from frappe.model.naming import make_autoname

	if doc.is_return==1:	
		key='04'			
		doc.mncf = make_autoname("B"+ key + '.########')
		# doc.mncf = make_autoname("A0100100101"+ key + '.########')
