from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class CdtAlerte(models.Model):
    _name = "cdt.alerte"
    _description = "Alerte"
    _order = "traitee, date_echeance, id desc"

    name = fields.Char(string="Alerte", required=True)
    type_alerte = fields.Selection(
        [
            ("garantie", "Garantie qui expire"),
            ("visite", "Visite périodique en retard"),
            ("stock", "Pièce sous le seuil"),
        ],
        string="Type",
        required=True,
    )
    equipement_id = fields.Many2one("cdt.equipement", string="Équipement", ondelete="cascade")
    piece_id = fields.Many2one("cdt.piece", string="Pièce", ondelete="cascade")
    date_echeance = fields.Date(string="Échéance")
    traitee = fields.Boolean(string="Traitée", default=False)

    def action_traiter(self):
        self.write({"traitee": True})

    def _delai_garantie(self):
        valeur = self.env["ir.config_parameter"].sudo().get_param("cdt_maintenance.delai_garantie_jours", "30")
        return int(valeur)

    def _existe(self, type_alerte, equipement=None, piece=None):
        domaine = [("type_alerte", "=", type_alerte), ("traitee", "=", False)]
        if equipement:
            domaine.append(("equipement_id", "=", equipement.id))
        if piece:
            domaine.append(("piece_id", "=", piece.id))
        return bool(self.search(domaine, limit=1))

    @api.model
    def scanner(self):
        self = self.sudo()
        aujourdhui = fields.Date.today()
        limite = aujourdhui + relativedelta(days=self._delai_garantie())

        equipements = self.env["cdt.equipement"].search([("etat", "in", ["installe", "en_maintenance"])])
        for eq in equipements:
            if eq.fin_garantie and aujourdhui <= eq.fin_garantie <= limite:
                if not self._existe("garantie", equipement=eq):
                    self.create({
                        "name": "Garantie de %s : fin le %s" % (eq.name, eq.fin_garantie),
                        "type_alerte": "garantie",
                        "equipement_id": eq.id,
                        "date_echeance": eq.fin_garantie,
                    })
            if eq.frequence_maintenance > 0:
                derniere = self.env["cdt.intervention"].search(
                    [("equipement_id", "=", eq.id), ("statut", "=", "terminee")],
                    order="date_fin desc",
                    limit=1,
                )
                if derniere and derniere.date_fin:
                    reference = derniere.date_fin.date()
                else:
                    reference = eq.date_installation
                if reference:
                    prochaine = reference + relativedelta(months=eq.frequence_maintenance)
                    if prochaine < aujourdhui and not self._existe("visite", equipement=eq):
                        self.create({
                            "name": "Visite en retard pour %s (prévue le %s)" % (eq.name, prochaine),
                            "type_alerte": "visite",
                            "equipement_id": eq.id,
                            "date_echeance": prochaine,
                        })

        pieces = self.env["cdt.piece"].search([("en_alerte", "=", True)])
        for piece in pieces:
            if not self._existe("stock", piece=piece):
                self.create({
                    "name": "Stock bas : %s (reste %s)" % (piece.name, piece.quantite_stock),
                    "type_alerte": "stock",
                    "piece_id": piece.id,
                    "date_echeance": aujourdhui,
                })
        return True