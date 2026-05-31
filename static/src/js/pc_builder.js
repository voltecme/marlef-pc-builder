/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";

publicWidget.registry.PCBuilder = publicWidget.Widget.extend({
    selector: '.s_pc_builder',
    events: {
        'click .select-component': '_onSelectComponent',
        'click #add-to-cart-btn': '_onAddToCart',
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
        this.order = ['motherboard', 'cpu', 'ram', 'storage', 'gpu', 'case', 'psu', 'cooler', 'fan', 'controller', 'cable', 'assembly'];
    },

    _onSelectComponent: function (ev) {
        const btn = $(ev.currentTarget);
        const card = btn.closest('.component-card');
        const id = card.data('id');
        const type = this._getCurrentType();
        
        this.selections[type] = id;
        this._updateSummary();
        this._nextStep(type);
    },

    _getCurrentType: function() {
        const activeTab = this.$('#pills-tab .nav-link.active').attr('id');
        return activeTab.replace('step-', '').replace('-tab', '');
    },

    _updateSummary: function() {
        let total = 0;
        // Logic to update summary UI and total price
        // This would ideally fetch prices or keep track of them
        this.$('#total-price').text('Updating...');
    },

    _nextStep: function(currentType) {
        const currentIndex = this.order.indexOf(currentType);
        if (currentIndex < this.order.length - 1) {
            const nextType = this.order[currentIndex + 1];
            this._loadComponents(nextType);
        } else {
            this.$('#add-to-cart-btn').prop('disabled', false);
        }
    },

    _loadComponents: function(type) {
        const self = this;
        const filters = {};
        if (type === 'cpu' || type === 'ram') {
            const mbCard = this.$(`.component-card[data-id="${this.selections.motherboard}"]`);
            filters.socket_type = mbCard.data('socket');
            filters.ram_type = mbCard.data('ram');
        }

        jsonrpc('/pc-builder/get_components', {
            component_type: type,
            filters: filters,
        }).then(function (data) {
            self._renderComponents(type, data);
        });
    },

    _renderComponents: function(type, data) {
        // Render the components in the next tab and switch to it
    },

    _onAddToCart: function () {
        const productIds = Object.values(this.selections).filter(id => id !== null);
        jsonrpc('/pc-builder/add_to_cart', {
            product_ids: productIds,
        }).then(function () {
            window.location.href = '/shop/cart';
        });
    },
});
