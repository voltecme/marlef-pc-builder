/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";

publicWidget.registry.PCBuilder = publicWidget.Widget.extend({
    selector: ".s_pc_builder",
    events: {
        "click .select-component": "_onSelectComponent",
        "click #add-to-cart-btn": "_onAddToCart",
        "click .nav-link": "_onTabClick",
        "click #generate-3d-btn": "_onGenerate3DModel",
    },

    init: function () {
        this._super.apply(this, arguments);
        this.selections = {
            motherboard: null,
            cpu: null,
            ram: null,
            storage: null,
            gpu: null,
            case: null,
            psu: null,
            cooler: null,
            fan: null,
            controller: null,
            cable: null,
            assembly: null,
        };
        this.selected_components_data = {}; // Store full data of selected components
        this.order = [
            "motherboard",
            "cpu",
            "ram",
            "storage",
            "gpu",
            "case",
            "psu",
            "cooler",
            "fan",
            "controller",
            "cable",
            "assembly",
        ];
        this.currentStepIndex = 0;
    },

    start: function () {
        this._super.apply(this, arguments);
        this._loadInitialComponents();
        this._updateSummary();
    },

    _loadInitialComponents: function () {
        // Motherboards are already rendered by Odoo template
        // Make sure the first tab is active and other tabs are disabled
        this.$("#pills-tab .nav-link").addClass("disabled");
        this.$("#step-motherboard-tab").removeClass("disabled").addClass("active");
        this.$("#step-motherboard").addClass("show active");
    },

    _onTabClick: function (ev) {
        if ($(ev.currentTarget).hasClass("disabled")) {
            ev.preventDefault();
            ev.stopPropagation();
        }
    },

    _onSelectComponent: function (ev) {
        const btn = $(ev.currentTarget);
        const card = btn.closest(".component-card");
        const id = card.data("id");
        const type = card.data("type"); // Get type from data-type attribute on card
        const name = card.find(".card-title").text();
        const price = parseFloat(card.find(".card-text.fw-bold").text().replace(/[^0-9.-]+/g, ""));

        // Deselect previously selected component of the same type
        this.$(`.component-card[data-type="${type}"]`).removeClass("selected");
        this.selections[type] = id;
        this.selected_components_data[type] = { id: id, name: name, price: price, socket_type: card.data("socket"), ram_type: card.data("ram") };
        card.addClass("selected");

        this._updateSummary();
        this._nextStep(type);
    },

    _getCurrentType: function () {
        const activeTabId = this.$("#pills-tab .nav-link.active").attr("id");
        return activeTabId.replace("step-", "").replace("-tab", "");
    },

    _updateSummary: function () {
        let total = 0;
        this.$("#build-summary-list").empty();
        for (const type of this.order) {
            const component = this.selected_components_data[type];
            if (component) {
                this.$("#build-summary-list").append(
                    `<li><strong>${type.charAt(0).toUpperCase() + type.slice(1)}:</strong> <span id="summary-${type}">${component.name} - ${this.formatCurrency(component.price)}</span></li>`
                );
                total += component.price;
            } else {
                this.$("#build-summary-list").append(
                    `<li><strong>${type.charAt(0).toUpperCase() + type.slice(1)}:</strong> <span id="summary-${type}">Not Selected</span></li>`
                );
            }
        }
        this.$("#total-price").text(this.formatCurrency(total));
        this._checkAddToCartButton();
    },

    _checkAddToCartButton: function() {
        const requiredComponents = ["motherboard", "cpu", "ram", "case", "psu"]; // Define minimum components for a valid build
        const allRequiredSelected = requiredComponents.every(type => this.selections[type] !== null);
        this.$("#add-to-cart-btn").prop("disabled", !allRequiredSelected);
        this.$("#generate-3d-btn").prop("disabled", !allRequiredSelected);
    },

    _nextStep: function (currentType) {
        const currentIndex = this.order.indexOf(currentType);
        // Clear selections for subsequent steps if a core component (motherboard, cpu, ram) is changed
        if (currentType === 'motherboard' || currentType === 'cpu' || currentType === 'ram') {
            for (let i = currentIndex + 1; i < this.order.length; i++) {
                const typeToClear = this.order[i];
                this.selections[typeToClear] = null;
                delete this.selected_components_data[typeToClear];
                this.$(`#${typeToClear}-list`).empty(); // Clear rendered components
            }
        }

        if (currentIndex < this.order.length - 1) {
            const nextType = this.order[currentIndex + 1];
            this._activateTab(nextType);
            this._loadComponents(nextType);
        } else {
            // All steps completed
            this.$("#add-to-cart-btn").prop("disabled", false);
            this.$("#generate-3d-btn").prop("disabled", false);
        }
    },

    _activateTab: function(type) {
        // Deactivate all tabs and panes
        this.$("#pills-tab .nav-link").removeClass("active");
        this.$(".tab-pane").removeClass("show active");

        // Activate the current tab and its pane, and enable it
        this.$(`#step-${type}-tab`).removeClass("disabled").addClass("active");
        this.$(`#step-${type}`).addClass("show active");

        // Enable all previous tabs
        const currentIndex = this.order.indexOf(type);
        for (let i = 0; i <= currentIndex; i++) {
            this.$(`#step-${this.order[i]}-tab`).removeClass("disabled");
        }
    },

    _loadComponents: function (type) {
        const self = this;
        const filters = {};
        if (type === "cpu" || type === "ram") {
            const motherboard = this.selected_components_data.motherboard;
            if (motherboard) {
                if (type === "cpu") {
                    filters.socket_type = motherboard.socket_type;
                }
                if (type === "ram") {
                    filters.ram_type = motherboard.ram_type;
                }
            }
        }

        jsonrpc("/pc-builder/get_components", {
            component_type: type,
            filters: filters,
        }).then(function (data) {
            self._renderComponents(type, data);
        });
    },

    _renderComponents: function (type, data) {
        const container = this.$(`#${type}-list`);
        container.empty();
        if (data.length === 0) {
            container.append(`<p class="text-warning">No ${type.charAt(0).toUpperCase() + type.slice(1)} components found matching criteria.</p>`);
            return;
        }

        data.forEach((p) => {
            const isSelected = this.selections[type] === p.id ? "selected" : "";
            container.append(`
                <div class="col-md-4 mb-3">
                    <div class="card bg-dark border-secondary h-100 component-card ${isSelected}" 
                         data-id="${p.id}" 
                         data-type="${type}"
                         data-socket="${p.socket_type || ''}"
                         data-ram="${p.ram_type || ''}">
                        <img src="${p.image_url}" class="card-img-top" alt="${p.name}"/>
                        <div class="card-body">
                            <h5 class="card-title text-white">${p.name}</h5>
                            ${p.socket_type ? `<p class="card-text text-muted">Socket: ${p.socket_type}</p>` : ''}
                            ${p.ram_type ? `<p class="card-text text-muted">RAM Type: ${p.ram_type}</p>` : ''}
                            <p class="card-text text-danger fw-bold">${this.formatCurrency(p.price)}</p>
                            <button class="btn btn-primary select-component" data-id="${p.id}">Select</button>
                        </div>
                    </div>
                </div>
            `);
        });
    },

    _onAddToCart: function () {
        const productIds = Object.values(this.selections).filter((id) => id !== null);
        jsonrpc("/pc-builder/add_to_cart", {
            product_ids: productIds,
        }).then(function () {
            window.location.href = "/shop/cart";
        });
    },

    _onGenerate3DModel: function() {
        alert("3D Model Generation is not yet implemented.");
        // This will involve calling a Python controller that interacts with an external AI 3D generator API
        // and then updating the #pc-3d-viewer div with the generated model.
    },

    formatCurrency: function(amount) {
        // Basic currency formatting, Odoo's monetary widget is more robust
        return `$${amount.toFixed(2)}`;
    },
});
