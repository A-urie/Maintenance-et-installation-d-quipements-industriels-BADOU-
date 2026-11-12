/** @odoo-module **/

import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, useState } from "@odoo/owl";

export class CdtDashboard extends Component {
    static template = "cdt_maintenance.Dashboard";

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({ data: null });
        onWillStart(async () => {
            this.state.data = await this.orm.call("cdt.dashboard", "get_data", []);
        });
    }

    barHeight(valeur) {
        return Math.round((valeur * 140) / this.state.data.maximum);
    }

    ouvrirAlertes() {
        this.action.doAction("cdt_maintenance.action_cdt_alerte");
    }

    ouvrirPlanning() {
        this.action.doAction("cdt_maintenance.action_cdt_planning");
    }
}

registry.category("actions").add("cdt_maintenance.dashboard", CdtDashboard);