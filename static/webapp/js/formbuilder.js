/*!
* FormBuilder v0.0.1
* Copyright 2018 Group P. Liberali, Friedrich Miescher Institute, Basel
* Licensed under the MIT license
*/
"use strict";

// HTML Base Classes

function HtmlElement(tag, attributes, htmlText, innerHtmlElements) {
    if (! tag) {
        throw new Error("Can't instantiate a html element without a tag!");
    }

    this.tag = tag;
    this.attributes = attributes || {};
    this.htmlText = htmlText  || null;
    this.innerHtmlElements = innerHtmlElements || [];
}
HtmlElement.prototype.getJQueryElement = function() {
    var htmlElement = $('<' + this.tag + '/>');
    $.each(this.attributes, function(name, value) {
        htmlElement.attr(name, value);
    });
    $.each(this.innerHtmlElements, function(idx, innerHtmlElement) {
        htmlElement.append(innerHtmlElement.getJQueryElement());
    });
    if (this.htmlText) {
        htmlElement.html(this.htmlText);
    }
    return htmlElement;
};

function HtmlFormElement(tag, attributes, htmlText, innerHtmlElements) {
    HtmlElement.call(this, tag, attributes, htmlText, innerHtmlElements);
}
HtmlFormElement.prototype = Object.create(  // simulate inheritance
    HtmlElement.prototype, {'constructor': HtmlFormElement}
);

function HtmlStructuralElement(tag, attributes, htmlText, innerHtmlElements) {
    HtmlElement.call(this, tag, attributes, htmlText, innerHtmlElements);
}
HtmlStructuralElement.prototype = Object.create(  // simulate inheritance
    HtmlElement.prototype, {'constructor': HtmlStructuralElement}
);

// HTML Form Classes

function FormElement(attributes, innerHtmlElements) {
    HtmlFormElement.call(this, 'form', attributes, null, innerHtmlElements);
}
FormElement.prototype = Object.create(  // simulate inheritance
    HtmlFormElement.prototype, {'constructor': FormElement}
);

function InputElement(attributes, htmlText) {
    HtmlFormElement.call(this, 'input', attributes, htmlText, null);
}
InputElement.prototype = Object.create(  // simulate inheritance
    HtmlFormElement.prototype, {'constructor': InputElement}
);

function TextAreaElement(attributes, htmlText) {
    HtmlFormElement.call(this, 'textarea', attributes, htmlText, null);
}
TextAreaElement.prototype = Object.create(  // simulate inheritance
    HtmlFormElement.prototype, {'constructor': TextAreaElement}
);

function LabelElement(attributes, htmlText) {
    HtmlFormElement.call(this, 'label', attributes, htmlText, null);
}
LabelElement.prototype = Object.create(  // simulate inheritance
    HtmlFormElement.prototype, {'constructor': LabelElement}
);

function FieldSetElement(attributes, htmlText, innerHtmlElements) {
    HtmlFormElement.call(this, 'fieldset', attributes, null, innerHtmlElements);
}
FieldSetElement.prototype = Object.create(  // simulate inheritance
    HtmlFormElement.prototype, {'constructor': FieldSetElement}
);

function LegendElement(attributes, htmlText) {
    HtmlFormElement.call(this, 'legend', attributes, htmlText, null);
}
LegendElement.prototype = Object.create(  // simulate inheritance
    HtmlFormElement.prototype, {'constructor': LegendElement}
);

function SelectElement(attributes, optionElements) {
    HtmlFormElement.call(this, 'select', attributes, null, optionElements);
}
SelectElement.prototype = Object.create(  // simulate inheritance
    HtmlFormElement.prototype, {'constructor': SelectElement}
);

function OptionElement(attributes, htmlText) {
    HtmlFormElement.call(this, 'option', attributes, htmlText, null);
}
OptionElement.prototype = Object.create(  // simulate inheritance
    HtmlFormElement.prototype, {'constructor': OptionElement}
);

function ButtonElement(attributes, htmlText) {
    HtmlFormElement.call(this, 'button', attributes, htmlText, null);
}
ButtonElement.prototype = Object.create(  // simulate inheritance
    HtmlFormElement.prototype, {'constructor': ButtonElement}
);

// HTML Structural Classes

function FormGroupControl(labelElement, formElement, helpMessage) {
    this.labelElement = labelElement || null;
    this.formElement = formElement || null;
    this.helpMessage = helpMessage || "";

    this.getJQueryElement = function() {
        var formGroupControl = $('<div/>');
        if (this.helpMessage === "") {
            formGroupControl.attr('class', 'form-group');
        } else {
            formGroupControl.attr('class', 'form-group has-error');
        }

        if (this.labelElement) {
            if (!("class" in this.labelElement.attributes)) {
                this.labelElement.attributes.class = "control-label";
            }
            if (this.labelElement.attributes["class"].indexOf("control-label") === -1) {
                this.labelElement.attributes.class += " control-label";
            }
            formGroupControl.append(this.labelElement.getJQueryElement());
        }

        if (this.formElement) {
            if (!("class" in this.formElement.attributes)) {
                this.formElement.attributes.class = "form-control";
            }
            if (this.formElement.attributes["class"].indexOf("form-control") === -1) {
                this.formElement.attributes.class += " form-control";
            }
            formGroupControl.append(this.formElement.getJQueryElement());
        }

        if (this.helpMessage !== "") {
            var helpBlock = $('<span/>');
            helpBlock.attr('class', 'help-block');
            helpBlock.html(this.helpMessage);
            formGroupControl.append(helpBlock);
        }
        return formGroupControl;
    };
}
FormGroupControl.prototype = Object.create(  // simulate inheritance
    HtmlStructuralElement.prototype, {'constructor': FormGroupControl}
);

function GridCellControl(htmlElement, widthWeight, isHidden) {
    this.htmlElement = htmlElement || null;
    this.widthWeight = widthWeight || null;
    this.isHidden = isHidden || false;

    this.getJQueryElement = function() {
        var gridCellControl = $('<div/>');
        if (this.widthWeight) {
            gridCellControl.attr('class', 'col-lg-' + this.widthWeight);
        } else {
            gridCellControl.attr('class', 'col-lg');
        }
        if (this.isHidden) {
            gridCellControl.addClass('hidden');
        }
        if (this.htmlElement) {
            gridCellControl.append(this.htmlElement.getJQueryElement());
        }
        return gridCellControl;
    };
}
GridCellControl.prototype = Object.create(  // simulate inheritance
    HtmlStructuralElement.prototype, {'constructor': GridCellControl}
);

function GridRowControl(gridCellControls, isHeader) {
    this.gridCellControls = gridCellControls || [];
    this.isHeader = isHeader || false;

    this.getJQueryElement = function() {
        var gridRowControl = $('<div/>');
        gridRowControl.attr('class', 'row');
        if (this.isHeader) {
            formColumn.addClass('title');
        }
        $.each(this.gridCellControls, function(idx, gridCellControl) {
            gridRowControl.append(gridCellControl.getJQueryElement());
        });
        return gridRowControl;
    };
}
GridRowControl.prototype = Object.create(  // simulate inheritance
    HtmlStructuralElement.prototype, {'constructor': GridRowControl}
);

// FieldSet Build Functions

function buildJobTemplateFieldSet(jobTemplates) {
    var fieldSetElement = new FieldSetElement({'id': 'id_job_template_fieldset'});
    fieldSetElement.innerHtmlElements.push(
        new LegendElement(null, "Job Template:")
    );

    var optionElements = [new OptionElement({'value': ''}, '---------')];
    $.each(jobTemplates, function(idx, jobTemplate) {
        optionElements.push(new OptionElement({'value': jobTemplate.id, 'selected': jobTemplate.isSelected}, jobTemplate.name));
    });
    fieldSetElement.innerHtmlElements.push(
        new GridRowControl([
            new GridCellControl(
                new FormGroupControl(
                    new LabelElement({}, 'Please choose a job template:'),
                    new SelectElement(
                        {
                            "id": "id_job_templates", "name": "job_templates",
                            "onchange": "reload_job($(this).val())", "size": "1"
                        }, optionElements
                    )
                ),
                12, false
            )
        ])
    );

    return fieldSetElement;
}

function buildJobFieldSet(job) {
    var fieldSetElement = new FieldSetElement({'id': 'id_job_fieldset'});
    fieldSetElement.innerHtmlElements.push(
        new LegendElement(null, "Job Details:")
    );

    var modelFields = [
        {'id': 'type', 'name': 'type', 'widthWeight': 0, 'readonly': true, 'isHidden': true},
        {'id': 'status', 'name': 'status', 'widthWeight': 0, 'readonly': true, 'isHidden': true},
        {'id': 'progress', 'name': 'progress', 'widthWeight': 0, 'readonly': true, 'isHidden': true},
        {'id': 'owner', 'name': 'owner', 'widthWeight': 0, 'readonly': true, 'isHidden': true},
        {'id': 'namespace', 'name': 'namespace', 'widthWeight': 2, 'readonly': true, 'isHidden': false},
        {'id': 'name', 'name': 'name', 'widthWeight': 9, 'readonly': true, 'isHidden': false},
        {'id': '', 'name': '&nbsp;', 'widthWeight': 1, 'readonly': true, 'isHidden': false}
    ]

    var rowHeaders = [];
    $.each(modelFields, function(field_idx, modelField) {
        rowHeaders.push(
            new GridCellControl(
                new FormGroupControl(
                    new LabelElement({'style': 'text-transform: capitalize;'}, modelField.name),
                    null
                ),
                modelField.widthWeight, modelField.isHidden
            )
        );
    });
    fieldSetElement.innerHtmlElements.push(new GridRowControl(rowHeaders));

    var rowCells = [];
    $.each(modelFields, function(field_idx, modelField) {
        var formElement = null;
        if (field_idx < modelFields.length - 1) {
            formElement = new InputElement(
                {
                    'id': 'id_' + modelField.id,
                    'name': modelField.id,
                    'value': job[modelField.name],
                    'type': 'text',
                    'readonly': modelField.readonly
                }, null
            );
        } else {
            formElement = new ButtonElement(
                {
                    'class': 'btn btn-link no-form-control',
                    'data-toggle': 'tooltip',
                    'data-container': 'body',
                    'data-placement': 'right',
                    'data-title': job['description'],
                    'type': 'button',
                    'style': 'width: auto; border-color: white; color: #337ab7;'
                }, '<span class="glyphicon glyphicon-info-sign icon-info"></span>'
            );
        }

        rowCells.push(
            new GridCellControl(
                new FormGroupControl(
                    null,
                    formElement
                ),
                modelField.widthWeight, modelField.isHidden
            )
        );
    });
    fieldSetElement.innerHtmlElements.push(new GridRowControl(rowCells));

    return fieldSetElement;
}

function buildJobParamsFieldSet(jobParams, initForms=0, minNumForms=0, maxNumForms=1000) {
    var fieldSetElement = new FieldSetElement({'id': 'id_job_parameters_fieldset'});
    fieldSetElement.innerHtmlElements.push(
        new LegendElement(null, "Job Parameters:")
    );
    fieldSetElement.innerHtmlElements.push(
        new InputElement({'id': 'id_parameters-TOTAL_FORMS', 'name': 'parameters-TOTAL_FORMS', 'type': 'hidden', 'value': jobParams.length.toString()}, null)
    );
    fieldSetElement.innerHtmlElements.push(
        new InputElement({'id': 'id_parameters-INITIAL_FORMS', 'name': 'parameters-INITIAL_FORMS', 'type': 'hidden', 'value': '0'}, null)
    );
    fieldSetElement.innerHtmlElements.push(
        new InputElement({'id': 'id_parameters-MIN_NUM_FORMS', 'name': 'parameters-MIN_NUM_FORMS', 'type': 'hidden', 'value': '0'}, null)
    );
    fieldSetElement.innerHtmlElements.push(
        new InputElement({'id': 'id_parameters-MAX_NUM_FORMS', 'name': 'parameters-MAX_NUM_FORMS', 'type': 'hidden', 'value': '1000'}, null)
    );

    var modelFields = [
        {'id': 'id', 'name': 'id', 'widthWeight': 0, 'readonly': true, 'isHidden': true},
        {'id': 'type', 'name': 'type', 'widthWeight': 0, 'readonly': true, 'isHidden': true},
        {'id': 'value', 'name': 'value', 'widthWeight': 0, 'readonly': true, 'isHidden': true},
        {'id': 'name', 'name': 'name', 'widthWeight': 3, 'readonly': true, 'isHidden': false},
        {'id': 'type-str', 'name': 'type', 'widthWeight': 2, 'readonly': true, 'isHidden': false},
        {'id': 'value-str', 'name': 'value', 'widthWeight': 6, 'readonly': false, 'isHidden': false},
        {'id': '', 'name': '&nbsp;', 'widthWeight': 1, 'readonly': true, 'isHidden': false}
    ]

    var rowHeaders = [];
    $.each(modelFields, function(field_idx, modelField) {
        rowHeaders.push(
            new GridCellControl(
                new FormGroupControl(
                    new LabelElement({'style': 'text-transform: capitalize;'}, modelField.name),
                    null
                ),
                modelField.widthWeight, modelField.isHidden
            )
        );
    });
    fieldSetElement.innerHtmlElements.push(new GridRowControl(rowHeaders));

    $.each(jobParams, function(param_idx, jobParam) {
        var rowCells = [];
        $.each(modelFields, function(field_idx, modelField) {
            var formElement = null;
            if (field_idx < modelFields.length - 1) {
                if (modelField.id == 'value-str' && jobParam['type-str'] == "Boolean") {
                    formElement = new InputElement(
                        {
                            'id': 'id_parameters-' + param_idx.toString() + '-' + modelField.id,
                            'class': 'pull-left',
                            'name': 'parameters-' + param_idx.toString() + '-' + modelField.id,
                            'type': 'checkbox',
                            'readonly': modelField.readonly,
                            'onchange':
                                (! modelField.isHidden) ?
                                '$(\'#id_parameters-' + param_idx.toString() + '-' + modelField.name + '\').attr(\'value\', $(this).is(\':checked\').toString());'
                                :
                                '',
                            'style': 'width: auto;',
                            'checked': jobParam[modelField.name].toLowerCase() == 'true'
                        }, null
                    );
                } else {
                    formElement = new InputElement(
                        {
                            'id': 'id_parameters-' + param_idx.toString() + '-' + modelField.id,
                            'name': 'parameters-' + param_idx.toString() + '-' + modelField.id,
                            'value': jobParam[modelField.id],
                            'type': 'text',
                            'readonly': modelField.readonly,
                            'onchange':
                                (! modelField.isHidden) ?
                                '$(\'#id_parameters-' + param_idx.toString() + '-' + modelField.name + '\').attr(\'value\', $(this).val());'
                                :
                                ''
                        }, null
                    );
                }
            } else {
                formElement = new ButtonElement(
                    {
                        'class': 'btn btn-link no-form-control',
                        'data-toggle': 'tooltip',
                        'data-container': 'body',
                        'data-placement': 'right',
                        'data-title': jobParam['description'],
                        'type': 'button',
                        'style': 'width: auto; border-color: white; color: #337ab7;'
                    }, '<span class="glyphicon glyphicon-info-sign icon-info"></span>'
                );
            }

            rowCells.push(
                new GridCellControl(
                    new FormGroupControl(
                        null,
                        formElement,
                        (modelField.id == 'value-str') ? jobParam['errors'].join('\r\n') : null
                    ),
                    modelField.widthWeight, modelField.isHidden
                )
            );
        });
        fieldSetElement.innerHtmlElements.push(new GridRowControl(rowCells));
    });

    return fieldSetElement;
}

// Form Build Functions

function buildJobRegisterForm(csrfToken, jobTemplates, jobs, jobParams) {
    var formElement = new FormElement({'class': 'form', 'action': '', 'method': 'post'}, null);
    formElement.innerHtmlElements.push(
        new InputElement({'type': 'hidden', 'name': 'csrfmiddlewaretoken', 'value': csrfToken}, null)
    );

    formElement.innerHtmlElements.push(buildJobTemplateFieldSet(jobTemplates));
    formElement.innerHtmlElements.push(buildJobFieldSet(jobs));
    formElement.innerHtmlElements.push(buildJobParamsFieldSet(jobParams));

    formElement.innerHtmlElements.push(
        new GridRowControl([
            new GridCellControl(
                new HtmlElement('hr'),
                12, false
            )
        ])
    );

    formElement.innerHtmlElements.push(
        new HtmlElement('div', {'class': 'form-actions'}, null,
            [
                new ButtonElement({'class': 'btn btn-primary', 'type': 'submit'}, 'Submit'),
                new HtmlElement('div', {'style': 'display:inline-block; margin-left: 30px;'}, '&nbsp;'),
                new HtmlElement('a', {'href': '/jobs/'}, 'back to the list'),
            ]
        )
    );

    return formElement;
}
