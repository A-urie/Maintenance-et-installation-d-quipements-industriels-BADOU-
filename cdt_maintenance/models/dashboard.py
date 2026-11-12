from datetime import datetime

from dateutil.relativedelta import relativedelta

from odoo import api, fields, models

MOIS = ["Janv.", "Févr.", "Mars", "Avr.", "Mai", "Juin", "Juil.", "Août", "Sept.", "Oct.", "Nov.", "Déc."]


class CdtDashboard(models.AbstractModel):
    _name = "cdt.dashboard"
    _description = "Données du tableau de bord"

    @api.model
    def _debut_jour(self, jour):
        return datetime.combine(jour, datetime.min.time())

    @api.model
    def get_data(self):
        intervention = self.env["cdt.intervention"].sudo()
        demande = self.env["cdt.demande"].sudo()
        installation = self.env["cdt.installation"].sudo()
        alerte = self.env["cdt.alerte"].sudo()

        aujourdhui = fields.Date.today()
        debut_mois = aujourdhui.replace(day=1)
        fin_mois = debut_mois + relativedelta(months=1)

        interventions_mois = intervention.search_count([
            ("date_planifiee", ">=", self._debut_jour(debut_mois)),
            ("date_planifiee", "<", self._debut_jour(fin_mois)),
            ("statut", "!=", "annulee"),
        ])

        urgences = demande.search_count([
            ("urgence", "=", "urgente"),
            ("statut", "in", ["nouvelle", "planifiee"]),
        ])

        echues = intervention.search([
            ("date_planifiee", "<", fields.Datetime.now()),
            ("statut", "!=", "annulee"),
        ])
        terminees = echues.filtered(lambda i: i.statut == "terminee")
        respect = round(len(terminees) * 100.0 / len(echues)) if echues else 0

        installations = installation.search_count([("etat", "=", "en_cours")])
        alertes = alerte.search_count([("traitee", "=", False)])

        par_mois = []
        for i in range(5, -1, -1):
            debut = debut_mois - relativedelta(months=i)
            fin = debut + relativedelta(months=1)
            nombre = intervention.search_count([
                ("date_planifiee", ">=", self._debut_jour(debut)),
                ("date_planifiee", "<", self._debut_jour(fin)),
                ("statut", "!=", "annulee"),
            ])
            par_mois.append({"label": MOIS[debut.month - 1], "valeur": nombre})

        return {
            "interventions_mois": interventions_mois,
            "urgences_ouvertes": urgences,
            "respect_planning": respect,
            "installations_en_cours": installations,
            "alertes_a_traiter": alertes,
            "par_mois": par_mois,
            "maximum": max([m["valeur"] for m in par_mois] + [1]),
        }