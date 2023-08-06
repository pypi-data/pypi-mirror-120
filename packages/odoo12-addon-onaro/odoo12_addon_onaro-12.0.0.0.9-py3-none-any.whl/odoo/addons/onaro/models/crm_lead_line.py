from odoo import models


class CRMLeadLine(models.Model):
    _inherit = 'crm.lead.line'

    # Create an invoice address for the partner created
    def _post_partner_creation_hook(self, partner):
        if self.lead_id.invoice_address:
            self.env["res.partner"].create({
                "type": 'invoice',
                "parent_id": partner.id,
                "street": self.lead_id.invoice_address,
                "zip": self.lead_id.zip,
                "city": self.lead_id.city,
                "state_id": self.lead_id.state_id,
            })
