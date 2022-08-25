// Copyright (c) 2018, Verynice SRL and contributors
// For license information, please see license.txt

frappe.ui.form.on('POS Summary', {
	refresh: function(frm) {

	// },
	// onload: function(frm){
    //     // frm.add_fetch('');
    //     // frm.set_value('usuario', frappe.session.user);
    //     // frm.set_value('pos_user', );
        frm.set_query("pos_user", function(doc) {
			return {
				filters: {
					'user': doc.usuario
				},
			};
        });
		frm.set_query("usuario", function(doc) {
			return {
				query: "berenice.berenice_app.doctype.pos_summary.pos_summary.get_cashiers",
				filters: {
					'parent': doc.pos_user
				}
			};
            // frm.set_value('pos_user', pos);
    //         // return pos;
        });
    },
            
            
    setup: function(frm){
        frm.set_value('letterhead', 'Berenice B/W');
        var usuario = cur_frm.doc.usuario;
        if (frm.doc.status == 'Cancelled'){
            frm.set_value('amended_from', frm.doc.name);
        }else{
            frm.set_value('amended_from', null);
        }
    
        var df1 = frappe.meta.get_docfield("POS Summary Payment","mode_of_payment", cur_frm.doc.name); 
        var df2 = frappe.meta.get_docfield("POS Summary Payment","amount", cur_frm.doc.name);
        var df3 = frappe.meta.get_docfield("POS Summary","pos_payments", cur_frm.doc.name);
        df1.read_only = 1; 
        df2.read_only = 1; 
},
    // refresh: function(frm) {
    //     frm.refresh_field("pos_payments");
        
    // },
    usuario: function(frm){
        frm.script_manager.trigger('posting_date');
    },

    // pos_user: function(frm){
    //     frm.script_manager.trigger('posting_date');
    // },

    
    before_submit: function(frm){
        get_cust_details(frm);
    },

    posting_date: function(frm){
        let usuario = frm.doc.usuario;
        let pos_profile = frm.doc.pos_user;
        let posting_date = frm.doc.posting_date;

        // this.tableFill();
    // frm.script_manager.trigger("pos_payments");
    
    // console.log(usuario + fecha);
    if (usuario && posting_date) {
        update_short(frm);
        // console.log(usuario + fecha);            
        frappe.call({
            method: "berenice.berenice_app.doctype.pos_summary.pos_summary.get_data",
            args: {
                "owner": frm.doc.usuario,
                "posting_date": frm.doc.posting_date,
                "pos_profile": frm.doc.pos_user         
            },
            callback: function(r){
                if (r.message){
                    // console.log(r.message);
                    
                    var data = r.message[0];
                    frm.set_value("transactions",data.numb);
                    frm.set_value("total_sales",data.r_total);
                    // frm.set_value("cash_returns",data.change_amount);
                    // console.log(data);
                // frm.set_value('transactions', r.message)
            }
        }
        });
        frm.clear_table("cash_breakdown");
        // var options = {};
        // console.log(frappe.meta.get_docfield('Cash Breakdown', 'denomination', cur_frm.doc.name).options);
        var options = JSON.parse("[" + frappe.meta.get_docfield('Cash Breakdown', 'denomination', cur_frm.doc.name).options.split("\n") + "]");
        // console.log(options);
        // frm.set_value("drawer");
        $.each(options, function(i, d) {
            var c = frm.add_child("cash_breakdown");
            c.denomination = flt(options[i]);
            c.qty = 0;
            c.amount= 0.0;
            // console.log(c.amount);
            // c.amount = frappe.model.set_value("Cash Breakdown", "amount", c.denomination*c.qty);
            frm.refresh_field("cash_breakdown");
            
        });
        
        $(".grid-add-row").hide();
        $(".grid-remove-rows").hide();
        $('div[data-fieldname="service_payment"]').find('.grid-add-row').show();
        frm.clear_table("pos_payments");
       
            frappe.call({
            method: "berenice.berenice_app.doctype.pos_summary.pos_summary.get_mode_of_payment",
            args:{
                // "doc": frm.doc,
                "owner": frm.doc.usuario,
                "posting_date": frm.doc.posting_date,
                "pos_profile": frm.doc.pos_user
            },
            callback: function(r){
                // console.log('checkmic'+ usuario+ fecha);
                // console.log(r.message);
                
                $.each(r.message, function(i, d) {
                    if(d.base_amount){
                    var c = frm.add_child("pos_payments");
                    c.mode_of_payment = d.mode_of_payment;
                    c.amount = d.base_amount;
                    frm.refresh_field("pos_payments");
                    }                     
            });
            update_short(frm);
               
            }
    
});
  
    }// end if
    },

    opening_amount: function (frm) {
        update_short(frm);
    },

    drawer: function(frm) {
    var drawer = 0.0;
    $.each(frm.doc.cash_breakdown || [], function(i, row) {
        if (row.amount) {
            drawer += flt(row.amount);
            // base_total_allocated_amount += flt(flt(row.allocated_amount)*flt(row.exchange_rate),
            // 	precision("base_paid_amount"));
        }
    });
    frm.set_value("drawer", drawer);
    },

});


frappe.ui.form.on("POS Summary Services", {
amount: function(frm){
    update_short(frm);
},
mode_of_payment: function(frm){
    update_short(frm);
}
});

frappe.ui.form.on("Cash Breakdown", {
    // var d = locals[cdt][cdn];
    qty: function(frm, cdt, cdn) {
        var d = locals[cdt][cdn];
        // console.log('calculando...'+ d.qty);
        
        
        var result = d.denomination * d.qty;
        // d.amount = result;
        // console.log(result);
        frm.set_value(d.amount, result);
        d.amount = result;
        
        var drawer = 0.0;
		$.each(frm.doc.cash_breakdown || [], function(i, row) {
			if (row.amount) {
				drawer += flt(row.amount);
				// base_total_allocated_amount += flt(flt(row.allocated_amount)*flt(row.exchange_rate),
				// 	precision("base_paid_amount"));
            
            }
        });
        // console.log(drawer);
        // console.log(cur_frm.doc.payouts);
        // console.log(cur_frm.doc.payins);
        frm.refresh_field("cash_breakdown");
        // frm.set_value("cash_total", real_drawer);
        frm.set_value("drawer", drawer);
        update_short(frm);
		// frm.set_value("base_total_allocated_amount", Math.abs(base_total_allocated_amount));

		// frm.events.drawer(frm);
    // },
        
        // }
    },
    
    
});

cur_frm.cscript.custom_validate = function(doc) {
	if (doc.from_date < get_today()) {
		msgprint("You can not select past date in From Date");
		validated = false;
	}
}


var get_cust_details = function(frm) {
    frm.clear_table("invoices");
    let owner = frm.doc.usuario;
    let pos_user = frm.doc.pos_user;
	let total = 0;
	if (owner && pos_user) {//period_end_date && frm.doc.period_start_date && frm.doc.company && frm.doc.pos_profile && frm.doc.usuario) {
		frappe.call({
			method: "berenice.berenice_app.doctype.pos_summary.pos_summary.get_cust_details",
			// doc: frm.doc,
			args: {
				owner: owner,
                posting_date: frm.doc.posting_date,
                pos_profile: pos_user
				// doc: frm.doc
				// company: frm.doc.company
			},
			// customer: frm.doc.customer,
			callback: function(r) {
				
				if (r.message) {
                    // console.log(r.message);
					$.each(r.message, function(i, d) {
						var c = frm.add_child("invoices");
						c.invoice = d.invoice;
						c.customer = d.customer;
						c.mop = d.mop;
						c.rounded_amount = d.total;
						c.tax_id = d.ncf;
						c.status = d.status;
						frm.refresh_field("invoices");	 
				});
				}
			}
		});
	}

};

function update_short(frm){
    let service_amount = 0.0;
    // var drawer = 0.0;
    // console.log(frm.doc.pago_servicios);
    
    $.each(frm.doc.service_payment || [], function(i, service) {
    //     console.log('Aqui est ==>'+serv.monto);
        
        if (service.amount && service.mode_of_payment=='Efectivo') {
            service_amount += service.amount;
            // base_total_allocated_amount += flt(flt(row.allocated_amount)*flt(row.exchange_rate),
            // 	precision("base_paid_amount"));
        }
    });
    // console.log(monto_serv+'<--Monto');

    $.each(frm.doc.pos_payments || [], function(i, service) {        
        if (service.amount && service.mode_of_payment=='Efectivo'){
    // console.log(serv.mode_of_payment);
        let short = flt(frm.doc.drawer - service.amount - frm.doc.opening_amount - service_amount);
        if (short < 0) {
                frm.set_value("short", Math.round(short));
                frm.refresh_field('short');   
            }else{
                frm.set_value("short", '');
                frm.refresh_field('short');
            }
            
            var drawer = 0.0;
        }else{
            console.log('maintained drawer--->', frm.doc.short);
        }
    });
}
