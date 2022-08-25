import frappe
from frappe.model.document import Document
from frappe.model.naming import make_autoname

@frappe.whitelist()
def ncf_autoname(doc, method):
        if doc.is_return==0:
                if doc.generate_ncf == 1:
                        customer_type = doc.customer_type
                        key=''
                        if customer_type == 'Businesses':
                                key='01'
                        elif customer_type == 'Final Clients':
                                key='02'
                        if customer_type == 'Government Entities':
                                key='15'
                        elif customer_type == 'Non-profit Organizations':
                                key='14'
                        doc.ncf = make_autoname("B"+ key + ".########", doc)
        elif doc.is_return==1 :
                if doc.generate_ncf == 1:
                        key='03'
                        doc.mncf = make_autoname("B"+ key + ".########")

# @frappe.whitelist()
def invoice_autoname(doc, method):
        # from frappe.model.naming import make_autoname
        if doc.generate_ncf == 1 :
                doc.naming_series="FPN-.#####"
        else:
                doc.naming_series="TPN-.#####"
