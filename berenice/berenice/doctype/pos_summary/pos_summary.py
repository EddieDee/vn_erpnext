# -*- coding: utf-8 -*-
# Copyright (c) 2018, Verynice SRL and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class POSSummary(Document):
	def __init__(self, *args, **kwargs):
        # pass
		super(POSSummary, self).__init__(*args, **kwargs)
        # self.data = self.transactions_count('Scarlet', '2018-06-21')

	def validate(self):
        # self.get_count()
		self.clear_unallocated_mode_of_payments()
        # print 'done'

    # def on_submit(self):
    #     self.clear_unallocated_mode_of_payments()


    # @staticmethod
	def transactions_count(self, pos_user, posting_date, time='23:59'):
		data = frappe.db.sql("""select count(*) as count from `tabSales Invoice` 
                where status!='Cancelled' and pos_profile like '%{pos}%' and posting_date between '{pdate} 00:00:00' 
                and '{pdate} 23:00:00' group by pos_profile """.format(pos=pos_user, pdate=posting_date))
        # data = frappe.db.sql("""select count(*) as count, pos_profile pos from `tabSales Invoice`
        # where status!='Cancelled' and pos_profile like '%{}%' and posting_date between '%s 00:00:00'
        # and '%s %s' group by pos """.format(pos_user, date, date, time))
		return data

	def clear_unallocated_mode_of_payments(self):
		self.set("cash_breakdown", self.get("cash_breakdown", {"amount": ["not in", [0, None, ""]]}))
		frappe.db.sql("""delete from `tabPOS Summary Payment` where parent = %s
			and amount = 0""", self.name)

# @frappe.whitelist()
# def update_multi_mode_option(owner, posting_date):
#     # print '****************************',doc[0]
#     # company = 'Papelería Berenice SRL'
#     # pos_profile = get_pos_profile(company) or {}
#     # pos_profile = get_pos_profile(company, pos_profile) or {}
#     # if not pos_profile or not pos_profile.get('payments'):
#     # payments = []
#     # for payment in get_mode_of_payment(pos_profile, posting_date):
#     #     print payment.values(), '************************************'
#     #     payments.append(payment.values())
#         # payments.mode_of_payment = payment.parent
#         # payments.account = payment.default_account
#         # payments.type = payment.type

#         # payment_mode= {}
#         # payment_mode = payment_mode.as_dict()

#         # for fieldname in default_fields:
#         #     if fieldname in payment_mode:
#         #         del payment_mode[fieldname]

#         # payments.append(payment_mode)
#         # print payments
#     return get_mode_of_payment(owner, posting_date, pos_profile)
@frappe.whitelist()
def get_mode_of_payment(owner, posting_date, pos_profile):
	mop = frappe.db.sql("""select ifnull(b.mode_of_payment, '') as mode_of_payment,
                        (case when b.mode_of_payment='Efectivo' then ABS(sum(b.base_amount)-sum(a.change_amount))
                        else sum(b.base_amount) end) as base_amount
                        from `tabSales Invoice` a, `tabSales Invoice Payment` b
                        where a.name = b.parent
                        and a.docstatus = 1
                        and (a.owner=%(owner)s or a.owner='druz@berenice.com.do' 
                                        or a.owner= 'egonzalez@berenice.com.do' 
                                        or a.owner= 'jforvil@verynice.com.do' or a.owner='Administrator')
                        and a.posting_date= %(pdate)s
                        and pos_profile=%(pos)s group by b.mode_of_payment
                        union
                        select ifnull(b.mode_of_payment, '') as mode_of_payment,
                        sum(b.total_allocated_amount) as base_amount
                        from `tabSales Invoice` a, `tabPayment Entry` b,`tabPayment Entry Reference` c
                        where a.name = c.reference_name
                        and b.name = c.parent
                        and a.owner=%(owner)s 
                        and a.posting_date= %(pdate)s
                        and  b.total_allocated_amount>1
                        group by b.mode_of_payment
                        union
                        select  '' as mode_of_payment, sum(a.grand_total) as total
                        from `tabSales Invoice` a
                        where  a.owner=%(owner)s 
                        and a.posting_date= %(pdate)s
                        and (a.pos_profile is NULL or a.pos_profile=%(pos)s)
                        and a.status in ('Unpaid', 'Overdue')
                        """, ({'owner':owner, 'pdate':posting_date, 'pos':pos_profile}), as_dict=1)
        #  return frappe.db.sql(""" select mpa.default_account, mpa.parent, mp.type as type from `tabMode of Payment Account` mpa,
		#  `tabMode of Payment` mp where mpa.parent = mp.name and mpa.company = %(company)s""", {'company': doc}, as_dict=1)
	# print mop
	# print 'resultado***************'
	return mop

@frappe.whitelist()
def get_data(owner, posting_date, pos_profile,):
    data = frappe.db.sql('''select count(*) as numb, sum(rounded_total) as r_total from `tabSales Invoice`
                            where posting_date=%(pdate)s 
                            and (owner=%(owner)s or owner='druz@berenice.com.do' 
                                        or owner= 'egonzalez@berenice.com.do' 
                                        or owner= 'jforvil@verynice.com.do' or owner='Administrator')
                            and docstatus=1 
                            and pos_profile=%(pos)s ''', ({'owner':owner, 'pdate':posting_date, 'pos':pos_profile}), as_dict=1)
    # print pos_profile,'********',posting_date, owner
    # data = frappe.get_all(
    #                 'Sales Invoice', 
    #                 filters={
    #                     "posting_date": posting_date, 
    #                     "owner": ('in', (owner,'druz@berenice.com.do', 'egonzalez@berenice.com.do', 'jforvil@verynice.com.do', 'Administrator')),
    #                     "pos_profile": pos_profile,
    #                     "docstatus": 1
    #                     }, 
    #                 fields=[
    #                     'count(*) as numb', 
    #                     'sum(rounded_total) as r_total'
    #                     ])
    # print data
    return data

@frappe.whitelist()
def get_cashiers(doctype, txt, searchfield, start, page_len, filters):
	cashiers_list = frappe.get_all("POS Profile User", filters=filters, fields=['user'])
	cashiers = [cashier for cashier in set(c['user'] for c in cashiers_list)]
	return [[c] for c in cashiers]

@frappe.whitelist()
def get_cust_details(owner, posting_date, pos_profile):
    # print pos_profile,'********',posting_date
    data = frappe.db.sql('''select a.name as invoice, a.customer, 
                        ifnull(b.mode_of_payment, '') as mop, (case when b.mode_of_payment='Efectivo' 
                        then (b.base_amount-a.change_amount) else b.base_amount end) as total, a.ncf, a.status
                        from `tabSales Invoice` a, `tabSales Invoice Payment` b
                        where a.name = b.parent
                        and b.docstatus = 1
                        and a.owner=%(owner)s
                        and a.posting_date= %(pdate)s
                        and pos_profile=%(pos)s
                        union
                        select a.name as invoice, a.title as customer, ifnull(b.mode_of_payment, '') as mop,
                        b.total_allocated_amount as total, a.ncf, a.status
                        from `tabSales Invoice` a, `tabPayment Entry` b,`tabPayment Entry Reference` c
                        where a.name = c.reference_name
                        and b.name = c.parent
                        and a.owner=%(owner)s
                        and b.posting_date= %(pdate)s
                        and  b.total_allocated_amount>1
                        union
                        select a.name as invoice, a.customer, '-' as mop, a.grand_total as total, a.ncf, a.status
                        from `tabSales Invoice` a
                        where a.docstatus=1
                        and a.owner=%(owner)s
                        and a.posting_date= %(pdate)s
                        and a.pos_profile is NULL
                        and a.status in ('Unpaid', 'Overdue')
                        ''', ({'owner':owner, 'pdate':posting_date, 'pos':pos_profile}), as_dict=1)

    # )
    # data = frappe.get_all(
    #                 'Sales Invoice', 
    #                 filters={ 
    #                     'owner' : owner,
	# 					# "ncf": ("like",'B01%'),
    #                     'posting_date': posting_date,
	# 					'docstatus':1,
    #                     }, 
					
    #                 fields=[
    #                     'name as factura',
	# 					'customer',
    #                     'mode_of_payment as mop',
	# 					'rounded_amount as total',
    #                     'ncf',
	# 					'status'
	# 					],
    #                 order_by='name'    
	# 					)
    # print data
    return data
