/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";

publicWidget.registry.PCBuilderDashboard = publicWidget.Widget.extend({
    selector: ".s_pc_builder_dashboard",
    events: {
        "click .view-build": "_onViewBuild",
        "click .refresh-dashboard": "_onRefreshDashboard",
    },

    init: function () {
        this._super.apply(this, arguments);
        this.refreshInterval = 30000; // Refresh every 30 seconds
    },

    start: function () {
        this._super.apply(this, arguments);
        this._startAutoRefresh();
    },

    _startAutoRefresh: function () {
        const self = this;
        setInterval(function () {
            self._refreshDashboardData();
        }, this.refreshInterval);
    },

    _refreshDashboardData: function () {
        jsonrpc("/pc-builder/api/dashboard_data", {}).then((data) => {
            this._updateDashboard(data);
        });
    },

    _updateDashboard: function (data) {
        // Update key metrics
        this.$("#total-builds").text(data.total_builds);
        this.$("#builds-today").text(data.builds_today);
        this.$("#total-revenue").text("$" + data.total_revenue.toFixed(2));
        this.$("#compatibility-issues").text(data.compatibility_issues.length);

        // Update popular components
        this._updatePopularComponents(data.popular_components);

        // Update stock status
        this._updateStockStatus(data.component_stock_status);

        // Update recent builds
        this._updateRecentBuilds(data.recent_builds);
    },

    _updatePopularComponents: function (components) {
        // Implementation for updating popular components list
    },

    _updateStockStatus: function (stockStatus) {
        // Implementation for updating stock status table
    },

    _updateRecentBuilds: function (builds) {
        // Implementation for updating recent builds table
    },

    _onViewBuild: function (ev) {
        ev.preventDefault();
        const buildId = $(ev.currentTarget).data("id");
        jsonrpc("/pc-builder/api/build/" + buildId, {}).then((data) => {
            this._showBuildModal(data);
        });
    },

    _showBuildModal: function (buildData) {
        // Show a modal with build details
        const modal = `
            <div class="modal fade" id="buildModal" tabindex="-1">
                <div class="modal-dialog modal-lg">
                    <div class="modal-content bg-dark text-white">
                        <div class="modal-header">
                            <h5 class="modal-title">${buildData.name}</h5>
                            <button type="button" class="btn-close btn-close-white" data-bs-dismiss="modal"></button>
                        </div>
                        <div class="modal-body">
                            <p><strong>User:</strong> ${buildData.user}</p>
                            <p><strong>Total Price:</strong> $${buildData.total_price.toFixed(2)}</p>
                            <p><strong>Created:</strong> ${buildData.create_date}</p>
                            <hr/>
                            <h6>Components:</h6>
                            <ul>
                                ${Object.entries(buildData.components)
                                    .filter(([_, value]) => value !== null)
                                    .map(([key, value]) => `<li>${key}: ${value}</li>`)
                                    .join("")}
                            </ul>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        this.$("body").append(modal);
        const modalElement = new bootstrap.Modal(document.getElementById("buildModal"));
        modalElement.show();
    },

    _onRefreshDashboard: function (ev) {
        ev.preventDefault();
        this._refreshDashboardData();
    },
});
