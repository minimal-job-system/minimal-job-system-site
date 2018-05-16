/*!
* FormBuilder v0.0.1
* Copyright 2018 Dario Vischi
* Licensed under the MIT license
*/
"use strict";

var GlobalEventManager = new (function() {
    this.isActive = false;
    this.eventHandlers = [];
    
    this.addEventHandler = function(get_element_id, check_condition, apply_action) {
        var handler = new Map();
        handler.set('get_element_id', get_element_id);
        handler.set('check_condition', check_condition);
        handler.set('apply_action', apply_action);
        
        this.eventHandlers.push(handler);
    };
    
    this.removeEventHandler = function(handler_idx) {
        this.eventHandlers.splice(handler_idx, 1);
    };
    
    this.clearEventHandlers = function() {
        this.eventHandlers = [];
    };
    
    this.notify = function(control_element) {
        if (!this.isActive) {
            return;
        }
        
        $.each(this.eventHandlers, function(handler_idx, eventHandler) {
            var get_element_id = eventHandler.get('get_element_id');
            var check_condition = eventHandler.get('check_condition');
            var apply_action = eventHandler.get('apply_action');
            
            var element_id = get_element_id();
            
            if (control_element.attr('id') != element_id) {
                return true;
            }
            if (!check_condition(control_element)) {
                return true;
            }
            apply_action(control_element);
        });
    };
})();

$( ".form-control" ).change(function() {
    GlobalEventManager.notify($(this));
});
