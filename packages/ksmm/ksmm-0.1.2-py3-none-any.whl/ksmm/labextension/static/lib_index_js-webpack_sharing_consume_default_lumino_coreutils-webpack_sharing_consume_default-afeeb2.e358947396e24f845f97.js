(self["webpackChunk_quansight_jupyterlab_ksmm"] = self["webpackChunk_quansight_jupyterlab_ksmm"] || []).push([["lib_index_js-webpack_sharing_consume_default_lumino_coreutils-webpack_sharing_consume_default-afeeb2"],{

/***/ "./lib/components/alerts.js":
/*!**********************************!*\
  !*** ./lib/components/alerts.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "SuccessAlertBox": () => (/* binding */ SuccessAlertBox)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react_bootstrap_Alert__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react-bootstrap/Alert */ "./node_modules/react-bootstrap/esm/Alert.js");


const SuccessAlertBox = (props) => {
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_bootstrap_Alert__WEBPACK_IMPORTED_MODULE_1__.default, { variant: "success" },
        "Success ",
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("a", { style: { textDecoration: "underline" }, onClick: () => props.handleClose() }, "Close")));
};


/***/ }),

/***/ "./lib/components/envvar.js":
/*!**********************************!*\
  !*** ./lib/components/envvar.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _keyval__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./keyval */ "./lib/components/keyval.js");


const EnvVarForm = (props) => {
    const [toggle, setToggle] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(true);
    const formData = props.formData;
    const keys = Object.keys(formData);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
        keys.map((key) => {
            return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_keyval__WEBPACK_IMPORTED_MODULE_1__.default, { formKey: key, formData: formData, key: toggle }),
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { type: "button", onClick: (e) => {
                        delete formData[key];
                        setToggle(!toggle);
                    } }, "Delete")));
        }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("button", { type: "button", onClick: (e) => {
                formData[''] = '';
                setToggle(!toggle);
            } }, "Add")));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (EnvVarForm);


/***/ }),

/***/ "./lib/components/keyval.js":
/*!**********************************!*\
  !*** ./lib/components/keyval.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);

/*
 * This function has a callback to mutate the formData to
 * add a new 'string':'string' type to the dictionary.
 *
 * Renders a widget for a dict of
 * { 'string':'string', 'string':'string' }
 */
const KeyValueWidget = (props) => {
    const [formKey, setFormKey] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(props.formKey);
    const [formVal, setFormVal] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(props.formData[formKey]);
    /*
     * Function to handle a change of key values in a key value store
     */
    const handleKeyChange = (oldKey, newKey) => {
        props.formData[newKey] = props.formData[oldKey];
        delete props.formData[oldKey];
        setFormKey(newKey);
    };
    /*
     * Function to handle any changing values
     */
    const handleValueChange = (key, newValue) => {
        props.formData[key] = newValue;
        setFormVal(newValue);
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { type: "string", placeholder: "ENV_VAR", value: formKey, onChange: (e) => {
                handleKeyChange(formKey, e.target.value);
            } }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input", { type: "string", placeholder: "MY VALUE", value: formVal, size: 75, onChange: (e) => {
                handleValueChange(formKey, e.target.value);
            } })));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (KeyValueWidget);


/***/ }),

/***/ "./lib/components/kscard.js":
/*!**********************************!*\
  !*** ./lib/components/kscard.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react_bootstrap__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! react-bootstrap */ "webpack/sharing/consume/default/react-bootstrap/react-bootstrap");
/* harmony import */ var react_bootstrap__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(react_bootstrap__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react_bootstrap_Card__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react-bootstrap/Card */ "./node_modules/react-bootstrap/esm/Card.js");
/* harmony import */ var react_icons_fa__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react-icons/fa */ "./node_modules/react-icons/fa/index.esm.js");




const KsCard = (props) => {
    var _a, _b, _c;
    const { kernelSpec, handleSelectKernelspec, handleCopyKernelspec, handleDeleteKernelspec, handleTemplateKernelspec } = props;
    const renderToolTip = (props) => react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_bootstrap__WEBPACK_IMPORTED_MODULE_1__.Tooltip, Object.assign({ id: 'card-tooltip' }, props), kernelSpec._ksmm.fs_path);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_bootstrap_Card__WEBPACK_IMPORTED_MODULE_2__.default, { style: {
            width: "12rem",
            height: "12rem",
        }, key: kernelSpec._ksmm.fs_path },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_bootstrap_Card__WEBPACK_IMPORTED_MODULE_2__.default.Body, null,
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_bootstrap__WEBPACK_IMPORTED_MODULE_1__.OverlayTrigger, { placement: "bottom", overlay: renderToolTip },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_bootstrap_Card__WEBPACK_IMPORTED_MODULE_2__.default.Title, null, kernelSpec.display_name))),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_bootstrap_Card__WEBPACK_IMPORTED_MODULE_2__.default.Footer, { className: "align-left" },
            ((_a = kernelSpec._ksmm) === null || _a === void 0 ? void 0 : _a.writeable) ? react__WEBPACK_IMPORTED_MODULE_0___default().createElement("a", { style: { cursor: "pointer" }, onClick: () => handleSelectKernelspec(kernelSpec) },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_icons_fa__WEBPACK_IMPORTED_MODULE_3__.FaRegEdit, { className: 'ksmm-button-enabled', title: 'Edit' }))
                : react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_icons_fa__WEBPACK_IMPORTED_MODULE_3__.FaRegEdit, { className: 'ksmm-button-disabled' }),
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement("a", { style: { cursor: "pointer" }, onClick: () => handleCopyKernelspec(kernelSpec) },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_icons_fa__WEBPACK_IMPORTED_MODULE_3__.FaCopy, { className: 'ksmm-button-enabled', title: 'Copy' })),
            ((_b = kernelSpec._ksmm) === null || _b === void 0 ? void 0 : _b.deletable) ? react__WEBPACK_IMPORTED_MODULE_0___default().createElement("a", { style: { cursor: "pointer" }, onClick: () => handleDeleteKernelspec(kernelSpec) },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_icons_fa__WEBPACK_IMPORTED_MODULE_3__.FaTrash, { className: 'ksmm-button-enabled', title: 'Delete' }))
                : react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_icons_fa__WEBPACK_IMPORTED_MODULE_3__.FaTrash, { className: 'ksmm-button-disabled' }),
            ((_c = kernelSpec.metadata) === null || _c === void 0 ? void 0 : _c.template) && react__WEBPACK_IMPORTED_MODULE_0___default().createElement("a", { style: { cursor: "pointer", float: 'right' }, onClick: () => handleTemplateKernelspec(kernelSpec) },
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_icons_fa__WEBPACK_IMPORTED_MODULE_3__.FaWpforms, { className: 'ksmm-button-enabled', title: 'Generate with Template' })))));
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (KsCard);


/***/ }),

/***/ "./lib/components/ksform.js":
/*!**********************************!*\
  !*** ./lib/components/ksform.js ***!
  \**********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "KsForm": () => (/* binding */ KsForm)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var react_bootstrap_Tabs__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react-bootstrap/Tabs */ "./node_modules/react-bootstrap/esm/Tabs.js");
/* harmony import */ var react_bootstrap_Tab__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! react-bootstrap/Tab */ "./node_modules/react-bootstrap/esm/Tab.js");
/* harmony import */ var react_bootstrap_Button__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! react-bootstrap/Button */ "./node_modules/react-bootstrap/esm/Button.js");
/* harmony import */ var _rjsf_bootstrap_4__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @rjsf/bootstrap-4 */ "webpack/sharing/consume/default/@rjsf/bootstrap-4/@rjsf/bootstrap-4");
/* harmony import */ var _rjsf_bootstrap_4__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_rjsf_bootstrap_4__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _envvar__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./envvar */ "./lib/components/envvar.js");
/* harmony import */ var _ksformgroup__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./ksformgroup */ "./lib/components/ksformgroup.js");







const TabMenu = (props) => {
    const [tab, setTab] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)("General Settings");
    /*
     * Generate the tab titles for the schema.
     */
    var menuHeaders = [
        "General Settings",
        "Launch Arguments",
        "Environment Variables",
    ];
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_bootstrap_Tabs__WEBPACK_IMPORTED_MODULE_2__.default, { defaultActiveKey: menuHeaders[0], onSelect: (k) => setTab(k) }, menuHeaders.map((menuHeader) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_bootstrap_Tab__WEBPACK_IMPORTED_MODULE_3__.default, { eventKey: menuHeader, key: menuHeader, title: menuHeader },
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_ksformgroup__WEBPACK_IMPORTED_MODULE_4__.default, { mainprops: props, selectedTab: tab, properties: props.properties }))))));
};
const KsForm = (props) => {
    const uiSchema = {
        "ui:ObjectFieldTemplate": TabMenu,
        env: {
            "ui:autofocus": true,
            "ui:ObjectFieldTemplate": _envvar__WEBPACK_IMPORTED_MODULE_5__.default,
            "ui:options": {
                expandable: true,
            },
        },
    };
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement((_rjsf_bootstrap_4__WEBPACK_IMPORTED_MODULE_1___default()), { schema: props.schema, uiSchema: uiSchema, formData: props.formData, onSubmit: props.onSubmit, formContext: {} }),
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_bootstrap_Button__WEBPACK_IMPORTED_MODULE_6__.default, { variant: "secondary", onClick: () => props.onCancel() }, "Cancel")));
};


/***/ }),

/***/ "./lib/components/ksformgroup.js":
/*!***************************************!*\
  !*** ./lib/components/ksformgroup.js ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);

/*
 * This is a nested component in the FieldTemplate, and
 * does all the work for rendering the different options in their
 * respective places.
 *
 * props: data -> The data to render - namely, the data as defined in the schema.
 */
const KsFormGroup = (props) => {
    const formGroupMap = generateFormGroupMap(props.properties);
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null, formGroupMap[props.selectedTab].map((index) => (react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { className: "property-wrapper", key: index }, props.properties[index].content)))));
};
/*
 * Grab the location of the element in the array,
 * returning a value of the positions in the array.
 */
function generateFormGroupMap(dataArr) {
    const QuickSettings = [];
    const GeneralSettingsArray = [];
    const LaunchArgumentsArray = [];
    const EnvironmentVariableArray = [];
    const ComputeParametersArray = [];
    const MetadataArray = [];
    dataArr.forEach((element) => {
        if (element.name == "display_name" ||
            element.name == "interrupt_mode" ||
            element.name == "language") {
            GeneralSettingsArray.push(dataArr.indexOf(element));
        }
        else if (element.name == "argv") {
            LaunchArgumentsArray.push(dataArr.indexOf(element));
        }
        else if (element.name == "env") {
            EnvironmentVariableArray.push(dataArr.indexOf(element));
        }
        else if (element.name == "parameters") {
            ComputeParametersArray.push(dataArr.indexOf(element));
        }
        else if (element.name == "metadata") {
            MetadataArray.push(dataArr.indexOf(element));
        }
        else if (element.name == "quick") {
            QuickSettings.push(dataArr.indexOf(element));
        }
        else {
            console.log("Unknown element name", element.name);
        }
    });
    return {
        ["General Settings"]: GeneralSettingsArray,
        ["Launch Arguments"]: LaunchArgumentsArray,
        ["Environment Variables"]: EnvironmentVariableArray,
        ["Compute Parameters"]: ComputeParametersArray,
        ["Quick Params"]: QuickSettings,
        ["Metadata"]: MetadataArray,
    };
}
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (KsFormGroup);


/***/ }),

/***/ "./lib/handler.js":
/*!************************!*\
  !*** ./lib/handler.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "requestAPI": () => (/* binding */ requestAPI)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__);


/**
 * Call the API extension
 *
 * @param endPoint API REST end point for the extension
 * @param init Initial values for the request
 * @returns The response body interpreted as JSON
 */
async function requestAPI(endPoint = '', init = {}) {
    // Make request to Jupyter API
    const settings = _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeSettings();
    const requestUrl = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.URLExt.join(settings.baseUrl, 'ksmm', // API Namespace
    endPoint);
    let response;
    try {
        response = await _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.makeRequest(requestUrl, init, settings);
    }
    catch (error) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.NetworkError(error);
    }
    let data = await response.text();
    if (data.length > 0) {
        try {
            data = JSON.parse(data);
        }
        catch (error) {
            console.log('Not a JSON response body.', response);
        }
    }
    if (!response.ok) {
        throw new _jupyterlab_services__WEBPACK_IMPORTED_MODULE_1__.ServerConnection.ResponseError(response, data.message || data);
    }
    return data;
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_ui_components_lib_icon_iconimports__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/ui-components/lib/icon/iconimports */ "./node_modules/@jupyterlab/ui-components/lib/icon/iconimports.js");
/* harmony import */ var _widget__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./widget */ "./lib/widget.js");




/*
 * The command IDs used by the to create a kernelspec.
 */
var CommandIDs;
(function (CommandIDs) {
    CommandIDs.create = "ksmm:create-kernelspec";
})(CommandIDs || (CommandIDs = {}));
/**
 * Initialization data for the ksmm extension.
 */
const ksmmExtension = {
    id: "jupyterlab-ksmm-plugin",
    autoStart: true,
    optional: [_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_1__.ILauncher],
    activate: (app, launcher) => {
        const { commands, serviceManager } = app;
        const command = CommandIDs.create;
        commands.addCommand(command, {
            caption: "A way to manage Kernelspecs",
            label: "Kernelspec Manager",
            icon: (args) => (args['isPalette'] ? null : _jupyterlab_ui_components_lib_icon_iconimports__WEBPACK_IMPORTED_MODULE_2__.extensionIcon),
            execute: () => {
                const content = new _widget__WEBPACK_IMPORTED_MODULE_3__.KernelspecManagerWidget(serviceManager);
                const widget = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.MainAreaWidget({ content });
                widget.title.label = "Kernelspec Manager";
                app.shell.add(widget, "main");
            }
        });
        if (launcher) {
            launcher.add({
                command
            });
        }
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (ksmmExtension);


/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "KernelspecManagerWidget": () => (/* binding */ KernelspecManagerWidget)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var react_bootstrap_Container__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! react-bootstrap/Container */ "./node_modules/react-bootstrap/esm/Container.js");
/* harmony import */ var _handler__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! ./handler */ "./lib/handler.js");
/* harmony import */ var _components_kscard__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! ./components/kscard */ "./lib/components/kscard.js");
/* harmony import */ var _components_alerts__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./components/alerts */ "./lib/components/alerts.js");
/* harmony import */ var _components_ksform__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./components/ksform */ "./lib/components/ksform.js");
/* harmony import */ var react_jsonschema_form__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! react-jsonschema-form */ "webpack/sharing/consume/default/react-jsonschema-form/react-jsonschema-form");
/* harmony import */ var react_jsonschema_form__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(react_jsonschema_form__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var bootstrap_dist_css_bootstrap_min_css__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! bootstrap/dist/css/bootstrap.min.css */ "./node_modules/bootstrap/dist/css/bootstrap.min.css");
var __rest = (undefined && undefined.__rest) || function (s, e) {
    var t = {};
    for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0)
        t[p] = s[p];
    if (s != null && typeof Object.getOwnPropertySymbols === "function")
        for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) {
            if (e.indexOf(p[i]) < 0 && Object.prototype.propertyIsEnumerable.call(s, p[i]))
                t[p[i]] = s[p[i]];
        }
    return t;
};










/**
 * React component for listing the possible
 * kernelspecs.
 *
 * @returns The React component.
 */
const KernelManagerComponent = (props) => {
    const { serviceManager } = props;
    const [data, setData] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(undefined);
    const [showForm, setShowForm] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    const [kernelFormData, setKernelFormData] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(undefined);
    const [selectedKernelName, setSelectedKernelName] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)('');
    const [schema, setSchema] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)({});
    const [alertBox, setAlertBox] = (0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(false);
    /**
     * Handles the Kernel Selection
     * at the select screen.
     */
    const handleSelectKernelspec = (kernelSpec) => {
        setSelectedKernelName(kernelSpec._ksmm.name);
        setKernelFormData(kernelSpec);
        setShowForm(true);
    };
    /**
     * Return Home on click.
     */
    const handleGoHome = () => {
        setShowForm(false);
        setAlertBox(false);
    };
    const refreshSchemas = () => {
        (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)("/schema", {
            method: "GET",
        }).then((s) => {
            setSchema(s);
        }).catch((err) => {
            return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)('Could not refresh schemas', err);
        });
    };
    const refreshKernelspecs = () => {
        (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)("/", {
            method: "GET",
        }).then((res) => {
            setData(res);
            void serviceManager.kernelspecs.refreshSpecs();
        }).catch((err) => {
            return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)('Could not refresh kernel specs', err);
        });
    };
    const handleCopyKernelspec = (kernelSpec) => {
        (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)("/copy", {
            method: "POST",
            body: JSON.stringify({ name: kernelSpec._ksmm.name }),
        }).catch((err) => {
            return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)('Could not copy kernel spec', err);
        }).then((data) => {
            refreshKernelspecs();
        });
    };
    const handleDeleteKernelspec = async (kernelSpec) => {
        const action = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showDialog)({
            title: `Are you sure you want to delete ${kernelSpec.display_name} (${kernelSpec._ksmm.name})?`,
        });
        if (!action.button.accept) {
            return;
        }
        (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)("/delete", {
            method: "POST",
            body: JSON.stringify({ name: kernelSpec._ksmm.name }),
        }).catch((err) => {
            return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)('Could not delete kernel spec', err);
        }).then((data) => {
            refreshKernelspecs();
        });
    };
    const handleTemplateKernelspec = (kernelSpec) => {
        var _a, _b;
        const buttons = [
            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.cancelButton({ label: 'Cancel' }),
            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog.okButton({ label: 'Create Kernelspec' })
        ];
        var params = {};
        const onChange = (e) => {
            params = e.formData;
        };
        const dialog = new _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.Dialog({
            title: 'Kernelspec from Template',
            body: _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget.create(react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react_jsonschema_form__WEBPACK_IMPORTED_MODULE_2___default()), { schema: {
                        "title": "",
                        "description": "",
                        "type": "object",
                        // @ts-ignore
                        "properties": (_b = (_a = kernelSpec.metadata) === null || _a === void 0 ? void 0 : _a.template) === null || _b === void 0 ? void 0 : _b.parameters
                    }, onChange: onChange },
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement("i", null,
                        "*We are not validating the form yet, please ensure you enter valid data (",
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("a", { href: "https://github.com/quansight/ksmm/issues/61", target: "blank" }, "issue"),
                        ")")))),
            buttons
        });
        void dialog.launch().then(result => {
            if (result.button.accept) {
                (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)("/params", {
                    method: "POST",
                    body: JSON.stringify({
                        name: kernelSpec._ksmm.name,
                        params: params
                    }),
                }).catch((err) => {
                    return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)('Could not generate kernel from template', err);
                })
                    .then((data) => {
                    refreshKernelspecs();
                });
            }
        });
    };
    /**
     * Handles a form submission when
     * kernels are modified in any form.
     *
     * Passed as a prop to Form.
     */
    const handleSubmitKernelspec = (e) => {
        // Drop _ksmm before submitting
        const _a = e.formData, { _ksmm } = _a, editedKernelPayload = __rest(_a, ["_ksmm"]);
        (0,_handler__WEBPACK_IMPORTED_MODULE_4__.requestAPI)("/", {
            method: "POST",
            body: JSON.stringify({
                editedKernelPayload: JSON.stringify(editedKernelPayload),
                originalKernelName: selectedKernelName,
            }),
        }).then((data) => {
            if (data.success) {
                setAlertBox(true);
                refreshKernelspecs();
                setKernelFormData(e.formData);
            }
            else {
                throw data;
            }
        }).catch((err) => {
            return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.showErrorMessage)('Could not update kernel spec', err);
        });
    };
    (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(() => {
        refreshSchemas();
        refreshKernelspecs();
    }, []);
    /**
     * Generate the package of data needed
     * to display at the card selection screen.
     *
     * This method is called on when then data is generated to
     * send into the method generating the card data.
     */
    const userKernels = {};
    const systemKernels = {};
    Object.entries(data || {}).forEach(entry => {
        const [name, kernelSpec] = entry;
        if (kernelSpec === null || kernelSpec === void 0 ? void 0 : kernelSpec._ksmm.is_user) {
            userKernels[name] = kernelSpec;
        }
        else {
            systemKernels[name] = kernelSpec;
        }
    });
    const KernelSpecCard = ({ kernelSpec }) => react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_kscard__WEBPACK_IMPORTED_MODULE_5__.default, { handleSelectKernelspec: handleSelectKernelspec, handleCopyKernelspec: handleCopyKernelspec, handleDeleteKernelspec: handleDeleteKernelspec, handleTemplateKernelspec: handleTemplateKernelspec, kernelSpec: kernelSpec, key: kernelSpec._ksmm.fs_path });
    const sortByDisplayName = (k1, k2) => {
        if (k1.display_name < k2.display_name) {
            return -1;
        }
        if (k1.display_name > k2.display_name) {
            return 1;
        }
        return 0;
    };
    const userKernelCards = Object.values(userKernels).sort(sortByDisplayName).map((kernelSpec) => react__WEBPACK_IMPORTED_MODULE_0___default().createElement(KernelSpecCard, { kernelSpec: kernelSpec }));
    const systemKernelCards = Object.values(systemKernels).sort(sortByDisplayName).map((kernelSpec) => react__WEBPACK_IMPORTED_MODULE_0___default().createElement(KernelSpecCard, { kernelSpec: kernelSpec }));
    return (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(react_bootstrap_Container__WEBPACK_IMPORTED_MODULE_6__.default, null,
        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("br", null),
        !showForm &&
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
                systemKernelCards.length > 0 ?
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("h3", null, "System Kernel Specs"),
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { style: {
                                display: "flex",
                                flexWrap: "wrap"
                            } }, systemKernelCards))
                    : null,
                react__WEBPACK_IMPORTED_MODULE_0___default().createElement("hr", null),
                userKernelCards.length > 0 ?
                    react__WEBPACK_IMPORTED_MODULE_0___default().createElement((react__WEBPACK_IMPORTED_MODULE_0___default().Fragment), null,
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("h3", null, "User Kernel Specs"),
                        react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div", { style: {
                                display: "flex",
                                flexWrap: "wrap"
                            } }, userKernelCards))
                    : null),
        alertBox &&
            react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_alerts__WEBPACK_IMPORTED_MODULE_7__.SuccessAlertBox, { handleClose: handleGoHome }),
        showForm && (react__WEBPACK_IMPORTED_MODULE_0___default().createElement(_components_ksform__WEBPACK_IMPORTED_MODULE_8__.KsForm, { schema: schema, formData: kernelFormData, onSubmit: handleSubmitKernelspec.bind(undefined), onCancel: handleGoHome.bind(undefined) }))));
};
/**
 * KernelspecManagerWidget main class.
 */
class KernelspecManagerWidget extends _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ReactWidget {
    constructor(serviceManager) {
        super();
        this._serviceManager = serviceManager;
        this.addClass("jp-Ksmm");
    }
    render() {
        return react__WEBPACK_IMPORTED_MODULE_0___default().createElement(KernelManagerComponent, { serviceManager: this._serviceManager });
    }
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js-webpack_sharing_consume_default_lumino_coreutils-webpack_sharing_consume_default-afeeb2.e358947396e24f845f97.js.map