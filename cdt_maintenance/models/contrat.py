from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class CdtContrat(models.Model):
    _name = "cdt.contrat"
    _description = "Contrat prestataire"
    _inherit = ["mail.thread"]
    _order = "date_fin"

    name = fields.Char(string="Référence", required=True, copy=False)
    type_contrat = fields.Selection(
        [("maintenance", "Maintenance"), ("fourniture", "Fourniture de matériel")],
        string="Type",
        default="maintenance",
        required=True,
    )
    prestataire_id = fields.Many2one("res.partner", string="Prestataire", required=True, tracking=True)
    date_debut = fields.Date(string="Début", required=True)
    date_fin = fields.Date(string="Fin", required=True, tracking=True)
    montant = fields.Float(string="Montant")
    equipement_ids = fields.Many2many("cdt.equipement", string="Équipements couverts")
    jours_restants = fields.Integer(string="Jours restants", compute="_compute_jours_restants")
    evaluation_ids = fields.One2many("cdt.contrat.evaluation", "contrat_id", string="Évaluations")
    note_moyenne = fields.Float(string="Note moyenne", compute="_compute_note", digits=(3, 1))
    a_revoir = fields.Boolean(string="Prestataire à revoir", compute="_compute_note")

    @api.depends("date_fin")
    def _compute_jours_restants(self):
        aujourdhui = fields.Date.today()
        for rec in self:
            rec.jours_restants = (rec.date_fin - aujourdhui).days if rec.date_fin else 0

    @api.depends("evaluation_ids.note")
    def _compute_note(self):
        for rec in self:
            notes = [int(e.note) for e in rec.evaluation_ids]
            rec.note_moyenne = (sum(notes) / len(notes)) if notes else 0.0
            rec.a_revoir = len([n for n in notes if n <= 2]) >= 3

    def action_renouveler(self):
        for rec in self:
            rec.date_fin = rec.date_fin + relativedelta(years=1)
            rec.message_post(body="Contrat renouvelé d'un an, nouvelle fin : %s." % rec.date_fin)


class CdtContratEvaluation(models.Model):
    _name = "cdt.contrat.evaluation"
    _description = "Évaluation d'une prestation"
    _order = "date desc, id desc"

    contrat_id = fields.Many2one("cdt.contrat", string="Contrat", required=True, ondelete="cascade")
    date = fields.Date(string="Date", default=fields.Date.today)
    note = fields.Selection(
        [("1", "1 – Mauvais"), ("2", "2 – Insuffisant"), ("3", "3 – Correct"), ("4", "4 – Bien"), ("5", "5 – Excellent")],
        string="Note",
        default="3",
        required=True,
    )
    commentaire = fields.Char(string="Commentaire")