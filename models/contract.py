from openerp.osv import osv, fields
from openerp.tools.translate import _
import openerp.addons.decimal_precision as dp

class hr_payslip_input(osv.osv):
    _inherit='hr.payslip.input'
    _columns={
              'qty':fields.float('Quantity'),
              'price':fields.float('Price'),
              'amount': fields.float('Amount',digits_compute=dp.get_precision('Payroll'), help="It is used in computation. For e.g. A rule for \
              sales having 1% commission of basic salary for per product can defined in expression like \
              result = inputs.SALEURO.amount * contract.wage*0.01."),
              }
    
    def onchange_qty_price(self, cr, uid, ids, qty, price,context=None):
        if context is None:
            context = {}
        if qty and price:
            amount = qty * price
        else:
            amount = 0.0
        res = {'value':{
                      'amount':amount
                      }
            }
        return res
    


def _get_nb_of_days(self, cr, uid, ids, field_names, arg=None, context=None):
    result = {}
    for slip in self.browse(cr,uid,ids, context):
        day_from = datetime.strptime(slip.date_from,"%Y-%m-%d")
        day_to = datetime.strptime(slip.date_to,"%Y-%m-%d")
        result[slip.id] = (day_to - day_from).days + 1
    return result

class hr_payslip(osv.osv):
    '''
    Employee Pay Slip
    '''
    _inherit = 'hr.payslip'
    _description = 'Pay Slips'
    _columns = {
        'nb_of_days': fields.function(_get_nb_of_days, method=True, type='integer',string='Total no. of days in month'),
         'pay_days': fields.date('Pay day'),
    }
