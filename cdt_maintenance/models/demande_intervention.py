from odoo import fields, models


class CdtDemande(models.Model):
    _name = "cdt.demande"
    _description = "Demande d'intervention"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "date_demande desc"

    name = fields.Char(string="Référence", required=True, copy=False, tracking=True)
    equipement_id = fields.Many2one("cdt.equipement", string="Équipement", required=True, tracking=True)
    client_id = fields.Many2one(related="equipement_id.client_id", string="Client", store=True, readonly=True)
    date_demande = fields.Datetime(string="Date de la demande", default=fields.Datetime.now)
    description = fields.Text(string="Description de la panne")
    urgence = fields.Selection(
        [
            ("urgente", "Urgente"),
            ("haute", "Haute"),
            ("normale", "Normale"),
            ("basse", "Basse"),
        ],
        string="Urgence",
        default="normale",
        required=True,
        tracking=True,
    )
    origine = fields.Selection(
        [("appel", "Appel du client"), ("periodique", "Visite périodique")],
        string="Origine",
        default="appel",
        required=True,
    )
    statut = fields.Selection(
        [
            ("nouvelle", "Nouvelle"),
            ("planifiee", "Planifiée"),
            ("terminee", "Terminée"),
            ("annulee", "Annulée"),
        ],
        string="Statut",
        default="nouvelle",
        required=True,
        tracking=True,
    )
    intervention_ids = fields.One2many("cdt.intervention", "demande_id", string="Interventions")

    def action_planifier(self):
        for rec in self:
            self.env["cdt.intervention"].create({
                "name": "Intervention " + rec.name,
                "demande_id": rec.id,
                "equipement_id": rec.equipement_id.id,
            })
        self.write({"statut": "planifiee"})

    def action_annuler(self):
        self.write({"statut": "annulee"})