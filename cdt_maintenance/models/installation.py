from odoo import api, fields, models
from odoo.exceptions import UserError

from .installation_etape import ETAPES


class CdtInstallation(models.Model):
    _name = "cdt.installation"
    _description = "Dossier d'installation"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_prevue desc, id desc"

    name = fields.Char(string="Référence", required=True, copy=False, readonly=True, default="Nouveau", tracking=True)
    client_id = fields.Many2one("res.partner", string="Client", required=True, tracking=True)
    equipement_id = fields.Many2one("cdt.equipement", string="Équipement", required=True, tracking=True)
    date_prevue = fields.Date(string="Date prévue", tracking=True)
    date_reception = fields.Date(string="Date de réception", readonly=True)
    technicien_ids = fields.Many2many("res.users", string="Équipe d'installation")
    etat = fields.Selection(
        [
            ("en_cours", "En cours"),
            ("receptionnee", "Réceptionnée"),
            ("annulee", "Annulée"),
        ],
        string="État",
        default="en_cours",
        required=True,
        tracking=True,
    )
    pv_signe = fields.Boolean(string="Procès-verbal signé par le client")
    etape_ids = fields.One2many("cdt.installation.etape", "installation_id", string="Étapes")
    avancement = fields.Float(string="Avancement (%)", compute="_compute_avancement", store=True)

    @api.depends("etape_ids.statut")
    def _compute_avancement(self):
        for rec in self:
            total = len(rec.etape_ids)
            faites = len(rec.etape_ids.filtered(lambda e: e.statut == "terminee"))
            rec.avancement = (faites * 100.0 / total) if total else 0.0

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("name", "Nouveau") == "Nouveau":
                vals["name"] = self.env["ir.sequence"].next_by_code("cdt.installation") or "Nouveau"
        records = super().create(vals_list)
        for rec in records:
            if not rec.etape_ids:
                self.env["cdt.installation.etape"].create([
                    {"installation_id": rec.id, "sequence": (i + 1) * 10, "name": code}
                    for i, (code, _label) in enumerate(ETAPES)
                ])
        return records

    def action_receptionner(self):
        for rec in self:
            if not rec.pv_signe:
                raise UserError("Le procès-verbal doit être signé par le client avant la réception.")
            rec.equipement_id.write({
                "etat": "installe",
                "date_installation": fields.Date.today(),
                "client_id": rec.client_id.id,
            })
        self.write({"etat": "receptionnee", "date_reception": fields.Date.today()})

    def action_annuler(self):
        self.write({"etat": "annulee"})