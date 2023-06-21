from odoo import models, fields, api, _, exceptions


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def action_view_sale_order(self):
        sale = self.sale_id
        if not sale:
            return self.create_so_btn()        

        action = self.env.ref('sale.action_quotations_with_onboarding').read()[0]
        action['views'] = [(self.env.ref('sale.view_order_form').id, 'form')]
        action['res_id'] = sale and sale.id 

        return action

    def create_so_btn(self):
        self.ensure_one()

        if self.sale_id:
            return self.action_view_sale_order()
        so_obj = self.env['sale.order']
        order_line_obj = self.env['sale.order.line']
        fiscal_position_id = self.env['account.fiscal.position'].sudo().with_context(company_id=self.company_id.id).get_fiscal_position(self.partner_id.id)
        sale_order = so_obj.create( {
            'partner_id': self.partner_id.id,
            'currency_id': self.partner_id.currency_id.id or self.env.user.company_id.currency_id.id or False,
            'payment_term_id': self.partner_id.property_payment_term_id.id or False,
            'fiscal_position_id': fiscal_position_id,
            'origin': self.name,
            'company_id': self.company_id.id,
            'date_order': self.scheduled_date or '',
            
        })
        self.sale_id = sale_order

        for line in self.move_ids_without_package or self.move_lines :
            unit_price = line.product_id.lst_price or 1
            qty = line.product_uom_qty or 1
            fpos = sale_order.fiscal_position_id
            taxes = fpos.map_tax(line.product_id.supplier_taxes_id) if fpos else line.product_id.supplier_taxes_id
            if taxes:
                taxes = taxes.filtered(lambda t: t.company_id.id == self.company_id.id)

            
            name = '[%s] %s' % (line.product_id.default_code, line.product_id.display_name)

            so_order_line = order_line_obj.create( {
                'name': line.name,
                'product_uom_qty': qty,
                'product_id': line.product_id.id,
                'product_uom': line.product_id.uom_id.id,
                'price_unit': unit_price,
                'order_id' : sale_order.id,
                # 'price_subtotal': unit_price * qty,
                'tax_id': [(6, 0, taxes.ids)],
            })
            so_order_line.product_id_change()
            so_order_line.picking_lines = line

        result = self.env.ref('sale.action_quotations_with_onboarding').read()[0]
        res = self.env.ref('sale.view_order_form', False)
        result['views'] = [(res and res.id or False, 'form')]
        result['res_id'] = sale_order.id or False

        return result