(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory(require("react"));
	else if(typeof define === 'function' && define.amd)
		define(["react"], factory);
	else if(typeof exports === 'object')
		exports["dazzler_ts"] = factory(require("react"));
	else
		root["dazzler_ts"] = factory(root["React"]);
})(self, function(__WEBPACK_EXTERNAL_MODULE_react__) {
return /******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./src/internal/ts_components/components/TypedClassComponent.tsx":
/*!***********************************************************************!*\
  !*** ./src/internal/ts_components/components/TypedClassComponent.tsx ***!
  \***********************************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
var react_1 = __importDefault(__webpack_require__(/*! react */ "react"));
var defProps = {
    default_required_str: 'default required',
    default_str: 'default',
    default_num: 3,
};
/**
 * Typed class component
 */
var TypedClassComponent = /** @class */ (function (_super) {
    __extends(TypedClassComponent, _super);
    function TypedClassComponent() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TypedClassComponent.prototype.render = function () {
        var _a = this.props, children = _a.children, class_name = _a.class_name, style = _a.style, identity = _a.identity, default_str = _a.default_str, default_num = _a.default_num;
        return (react_1["default"].createElement("div", { id: identity, className: class_name, style: style },
            react_1["default"].createElement("div", { className: "children" }, children),
            react_1["default"].createElement("div", { className: "default_str" }, default_str),
            react_1["default"].createElement("div", { className: "default_num" }, default_num)));
    };
    TypedClassComponent.defaultProps = defProps;
    return TypedClassComponent;
}(react_1["default"].Component));
exports.default = TypedClassComponent;


/***/ }),

/***/ "./src/internal/ts_components/components/TypedComponent.tsx":
/*!******************************************************************!*\
  !*** ./src/internal/ts_components/components/TypedComponent.tsx ***!
  \******************************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
exports.__esModule = true;
var react_1 = __importStar(__webpack_require__(/*! react */ "react"));
/**
 * Typed Component Docstring
 */
var TypedComponent = function (props) {
    var class_name = props.class_name, identity = props.identity, style = props.style, num = props.num, text = props.text, children = props.children, arr = props.arr, arr_str = props.arr_str, arr_num = props.arr_num, default_str = props.default_str, obj = props.obj, obj_lit = props.obj_lit, required_str = props.required_str, default_required_str = props.default_required_str, enumeration = props.enumeration;
    var state = react_1.useState(1)[0];
    return (react_1["default"].createElement("div", { className: class_name, id: identity, style: style },
        react_1["default"].createElement("div", { className: "children" }, children),
        react_1["default"].createElement("div", { className: "state" }, state),
        react_1["default"].createElement("div", { className: "json-output" }, JSON.stringify({
            num: num,
            text: text,
            arr: arr,
            arr_str: arr_str,
            arr_num: arr_num,
            default_str: default_str,
            obj: obj,
            obj_lit: obj_lit,
            required_str: required_str,
            default_required_str: default_required_str,
            enumeration: enumeration,
        }))));
};
TypedComponent.defaultProps = {
    default_str: 'default',
    default_required_str: 'default required',
    default_num: 3,
};
exports.default = TypedComponent;


/***/ }),

/***/ "./src/internal/ts_components/index.ts":
/*!*********************************************!*\
  !*** ./src/internal/ts_components/index.ts ***!
  \*********************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
exports.TypedClassComponent = exports.TypedComponent = void 0;
var TypedComponent_1 = __importDefault(__webpack_require__(/*! ./components/TypedComponent */ "./src/internal/ts_components/components/TypedComponent.tsx"));
exports.TypedComponent = TypedComponent_1["default"];
var TypedClassComponent_1 = __importDefault(__webpack_require__(/*! ./components/TypedClassComponent */ "./src/internal/ts_components/components/TypedClassComponent.tsx"));
exports.TypedClassComponent = TypedClassComponent_1["default"];


/***/ }),

/***/ "react":
/*!****************************************************************************************************!*\
  !*** external {"commonjs":"react","commonjs2":"react","amd":"react","umd":"react","root":"React"} ***!
  \****************************************************************************************************/
/***/ ((module) => {

module.exports = __WEBPACK_EXTERNAL_MODULE_react__;

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		__webpack_modules__[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module is referenced by other modules so it can't be inlined
/******/ 	var __webpack_exports__ = __webpack_require__("./src/internal/ts_components/index.ts");
/******/ 	
/******/ 	return __webpack_exports__;
/******/ })()
;
});
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiZGF6emxlcl90c184MDM1NTc0ZjgwNWFlMzFjZmM1YS5qcyIsIm1hcHBpbmdzIjoiQUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxDQUFDO0FBQ0QsTzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDVkEseUVBQTBCO0FBRzFCLElBQU0sUUFBUSxHQUFHO0lBQ2Isb0JBQW9CLEVBQUUsa0JBQWtCO0lBQ3hDLFdBQVcsRUFBRSxTQUFTO0lBQ3RCLFdBQVcsRUFBRSxDQUFDO0NBQ2pCLENBQUM7QUFFRjs7R0FFRztBQUNIO0lBQWlELHVDQUFvQztJQUFyRjs7SUFvQkEsQ0FBQztJQW5CRyxvQ0FBTSxHQUFOO1FBQ1UsU0FPRixJQUFJLENBQUMsS0FBSyxFQU5WLFFBQVEsZ0JBQ1IsVUFBVSxrQkFDVixLQUFLLGFBQ0wsUUFBUSxnQkFDUixXQUFXLG1CQUNYLFdBQVcsaUJBQ0QsQ0FBQztRQUNmLE9BQU8sQ0FDSCwwQ0FBSyxFQUFFLEVBQUUsUUFBUSxFQUFFLFNBQVMsRUFBRSxVQUFVLEVBQUUsS0FBSyxFQUFFLEtBQUs7WUFDbEQsMENBQUssU0FBUyxFQUFDLFVBQVUsSUFBRSxRQUFRLENBQU87WUFDMUMsMENBQUssU0FBUyxFQUFDLGFBQWEsSUFBRSxXQUFXLENBQU87WUFDaEQsMENBQUssU0FBUyxFQUFDLGFBQWEsSUFBRSxXQUFXLENBQU8sQ0FDOUMsQ0FDVCxDQUFDO0lBQ04sQ0FBQztJQUVNLGdDQUFZLEdBQUcsUUFBUSxDQUFDO0lBQ25DLDBCQUFDO0NBQUEsQ0FwQmdELGtCQUFLLENBQUMsU0FBUyxHQW9CL0Q7a0JBcEJvQixtQkFBbUI7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDWnhDLHNFQUFzQztBQUd0Qzs7R0FFRztBQUNILElBQU0sY0FBYyxHQUFHLFVBQUMsS0FBMEI7SUFFMUMsY0FBVSxHQWVWLEtBQUssV0FmSyxFQUNWLFFBQVEsR0FjUixLQUFLLFNBZEcsRUFDUixLQUFLLEdBYUwsS0FBSyxNQWJBLEVBQ0wsR0FBRyxHQVlILEtBQUssSUFaRixFQUNILElBQUksR0FXSixLQUFLLEtBWEQsRUFDSixRQUFRLEdBVVIsS0FBSyxTQVZHLEVBQ1IsR0FBRyxHQVNILEtBQUssSUFURixFQUNILE9BQU8sR0FRUCxLQUFLLFFBUkUsRUFDUCxPQUFPLEdBT1AsS0FBSyxRQVBFLEVBQ1AsV0FBVyxHQU1YLEtBQUssWUFOTSxFQUNYLEdBQUcsR0FLSCxLQUFLLElBTEYsRUFDSCxPQUFPLEdBSVAsS0FBSyxRQUpFLEVBQ1AsWUFBWSxHQUdaLEtBQUssYUFITyxFQUNaLG9CQUFvQixHQUVwQixLQUFLLHFCQUZlLEVBQ3BCLFdBQVcsR0FDWCxLQUFLLFlBRE0sQ0FDTDtJQUNILFNBQUssR0FBSSxnQkFBUSxDQUFDLENBQUMsQ0FBQyxHQUFmLENBQWdCO0lBRTVCLE9BQU8sQ0FDSCwwQ0FBSyxTQUFTLEVBQUUsVUFBVSxFQUFFLEVBQUUsRUFBRSxRQUFRLEVBQUUsS0FBSyxFQUFFLEtBQUs7UUFDbEQsMENBQUssU0FBUyxFQUFDLFVBQVUsSUFBRSxRQUFRLENBQU87UUFDMUMsMENBQUssU0FBUyxFQUFDLE9BQU8sSUFBRSxLQUFLLENBQU87UUFDcEMsMENBQUssU0FBUyxFQUFDLGFBQWEsSUFDdkIsSUFBSSxDQUFDLFNBQVMsQ0FBQztZQUNaLEdBQUc7WUFDSCxJQUFJO1lBQ0osR0FBRztZQUNILE9BQU87WUFDUCxPQUFPO1lBQ1AsV0FBVztZQUNYLEdBQUc7WUFDSCxPQUFPO1lBQ1AsWUFBWTtZQUNaLG9CQUFvQjtZQUNwQixXQUFXO1NBQ2QsQ0FBQyxDQUNBLENBQ0osQ0FDVCxDQUFDO0FBQ04sQ0FBQyxDQUFDO0FBRUYsY0FBYyxDQUFDLFlBQVksR0FBRztJQUMxQixXQUFXLEVBQUUsU0FBUztJQUN0QixvQkFBb0IsRUFBRSxrQkFBa0I7SUFDeEMsV0FBVyxFQUFFLENBQUM7Q0FDakIsQ0FBQztBQUVGLGtCQUFlLGNBQWMsQ0FBQzs7Ozs7Ozs7Ozs7Ozs7Ozs7QUN2RDlCLDZKQUF5RDtBQUdqRCx5QkFIRCwyQkFBYyxDQUdDO0FBRnRCLDRLQUFtRTtBQUUzQyw4QkFGakIsZ0NBQW1CLENBRWlCOzs7Ozs7Ozs7OztBQ0gzQzs7Ozs7O1VDQUE7VUFDQTs7VUFFQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTs7VUFFQTtVQUNBOztVQUVBO1VBQ0E7VUFDQTs7OztVRXRCQTtVQUNBO1VBQ0E7VUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovLy8vd2VicGFjay91bml2ZXJzYWxNb2R1bGVEZWZpbml0aW9uPyIsIndlYnBhY2s6Ly8vLy4vc3JjL2ludGVybmFsL3RzX2NvbXBvbmVudHMvY29tcG9uZW50cy9UeXBlZENsYXNzQ29tcG9uZW50LnRzeD8iLCJ3ZWJwYWNrOi8vLy8uL3NyYy9pbnRlcm5hbC90c19jb21wb25lbnRzL2NvbXBvbmVudHMvVHlwZWRDb21wb25lbnQudHN4PyIsIndlYnBhY2s6Ly8vLy4vc3JjL2ludGVybmFsL3RzX2NvbXBvbmVudHMvaW5kZXgudHM/Iiwid2VicGFjazovLy8vZXh0ZXJuYWwge1wiY29tbW9uanNcIjpcInJlYWN0XCIsXCJjb21tb25qczJcIjpcInJlYWN0XCIsXCJhbWRcIjpcInJlYWN0XCIsXCJ1bWRcIjpcInJlYWN0XCIsXCJyb290XCI6XCJSZWFjdFwifT8iLCJ3ZWJwYWNrOi8vLy93ZWJwYWNrL2Jvb3RzdHJhcD8iLCJ3ZWJwYWNrOi8vLy93ZWJwYWNrL2JlZm9yZS1zdGFydHVwPyIsIndlYnBhY2s6Ly8vL3dlYnBhY2svc3RhcnR1cD8iLCJ3ZWJwYWNrOi8vLy93ZWJwYWNrL2FmdGVyLXN0YXJ0dXA/Il0sInNvdXJjZXNDb250ZW50IjpbIihmdW5jdGlvbiB3ZWJwYWNrVW5pdmVyc2FsTW9kdWxlRGVmaW5pdGlvbihyb290LCBmYWN0b3J5KSB7XG5cdGlmKHR5cGVvZiBleHBvcnRzID09PSAnb2JqZWN0JyAmJiB0eXBlb2YgbW9kdWxlID09PSAnb2JqZWN0Jylcblx0XHRtb2R1bGUuZXhwb3J0cyA9IGZhY3RvcnkocmVxdWlyZShcInJlYWN0XCIpKTtcblx0ZWxzZSBpZih0eXBlb2YgZGVmaW5lID09PSAnZnVuY3Rpb24nICYmIGRlZmluZS5hbWQpXG5cdFx0ZGVmaW5lKFtcInJlYWN0XCJdLCBmYWN0b3J5KTtcblx0ZWxzZSBpZih0eXBlb2YgZXhwb3J0cyA9PT0gJ29iamVjdCcpXG5cdFx0ZXhwb3J0c1tcImRhenpsZXJfdHNcIl0gPSBmYWN0b3J5KHJlcXVpcmUoXCJyZWFjdFwiKSk7XG5cdGVsc2Vcblx0XHRyb290W1wiZGF6emxlcl90c1wiXSA9IGZhY3Rvcnkocm9vdFtcIlJlYWN0XCJdKTtcbn0pKHNlbGYsIGZ1bmN0aW9uKF9fV0VCUEFDS19FWFRFUk5BTF9NT0RVTEVfcmVhY3RfXykge1xucmV0dXJuICIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQge1R5cGVkQ29tcG9uZW50UHJvcHN9IGZyb20gJy4uLy4uL3R5cGVzJztcblxuY29uc3QgZGVmUHJvcHMgPSB7XG4gICAgZGVmYXVsdF9yZXF1aXJlZF9zdHI6ICdkZWZhdWx0IHJlcXVpcmVkJyxcbiAgICBkZWZhdWx0X3N0cjogJ2RlZmF1bHQnLFxuICAgIGRlZmF1bHRfbnVtOiAzLFxufTtcblxuLyoqXG4gKiBUeXBlZCBjbGFzcyBjb21wb25lbnRcbiAqL1xuZXhwb3J0IGRlZmF1bHQgY2xhc3MgVHlwZWRDbGFzc0NvbXBvbmVudCBleHRlbmRzIFJlYWN0LkNvbXBvbmVudDxUeXBlZENvbXBvbmVudFByb3BzPiB7XG4gICAgcmVuZGVyKCkge1xuICAgICAgICBjb25zdCB7XG4gICAgICAgICAgICBjaGlsZHJlbixcbiAgICAgICAgICAgIGNsYXNzX25hbWUsXG4gICAgICAgICAgICBzdHlsZSxcbiAgICAgICAgICAgIGlkZW50aXR5LFxuICAgICAgICAgICAgZGVmYXVsdF9zdHIsXG4gICAgICAgICAgICBkZWZhdWx0X251bSxcbiAgICAgICAgfSA9IHRoaXMucHJvcHM7XG4gICAgICAgIHJldHVybiAoXG4gICAgICAgICAgICA8ZGl2IGlkPXtpZGVudGl0eX0gY2xhc3NOYW1lPXtjbGFzc19uYW1lfSBzdHlsZT17c3R5bGV9PlxuICAgICAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiY2hpbGRyZW5cIj57Y2hpbGRyZW59PC9kaXY+XG4gICAgICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJkZWZhdWx0X3N0clwiPntkZWZhdWx0X3N0cn08L2Rpdj5cbiAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImRlZmF1bHRfbnVtXCI+e2RlZmF1bHRfbnVtfTwvZGl2PlxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICk7XG4gICAgfVxuXG4gICAgc3RhdGljIGRlZmF1bHRQcm9wcyA9IGRlZlByb3BzO1xufVxuIiwiaW1wb3J0IFJlYWN0LCB7dXNlU3RhdGV9IGZyb20gJ3JlYWN0JztcbmltcG9ydCB7VHlwZWRDb21wb25lbnRQcm9wc30gZnJvbSAnLi4vLi4vdHlwZXMnO1xuXG4vKipcbiAqIFR5cGVkIENvbXBvbmVudCBEb2NzdHJpbmdcbiAqL1xuY29uc3QgVHlwZWRDb21wb25lbnQgPSAocHJvcHM6IFR5cGVkQ29tcG9uZW50UHJvcHMpID0+IHtcbiAgICBjb25zdCB7XG4gICAgICAgIGNsYXNzX25hbWUsXG4gICAgICAgIGlkZW50aXR5LFxuICAgICAgICBzdHlsZSxcbiAgICAgICAgbnVtLFxuICAgICAgICB0ZXh0LFxuICAgICAgICBjaGlsZHJlbixcbiAgICAgICAgYXJyLFxuICAgICAgICBhcnJfc3RyLFxuICAgICAgICBhcnJfbnVtLFxuICAgICAgICBkZWZhdWx0X3N0cixcbiAgICAgICAgb2JqLFxuICAgICAgICBvYmpfbGl0LFxuICAgICAgICByZXF1aXJlZF9zdHIsXG4gICAgICAgIGRlZmF1bHRfcmVxdWlyZWRfc3RyLFxuICAgICAgICBlbnVtZXJhdGlvbixcbiAgICB9ID0gcHJvcHM7XG4gICAgY29uc3QgW3N0YXRlXSA9IHVzZVN0YXRlKDEpO1xuXG4gICAgcmV0dXJuIChcbiAgICAgICAgPGRpdiBjbGFzc05hbWU9e2NsYXNzX25hbWV9IGlkPXtpZGVudGl0eX0gc3R5bGU9e3N0eWxlfT5cbiAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiY2hpbGRyZW5cIj57Y2hpbGRyZW59PC9kaXY+XG4gICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cInN0YXRlXCI+e3N0YXRlfTwvZGl2PlxuICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJqc29uLW91dHB1dFwiPlxuICAgICAgICAgICAgICAgIHtKU09OLnN0cmluZ2lmeSh7XG4gICAgICAgICAgICAgICAgICAgIG51bSxcbiAgICAgICAgICAgICAgICAgICAgdGV4dCxcbiAgICAgICAgICAgICAgICAgICAgYXJyLFxuICAgICAgICAgICAgICAgICAgICBhcnJfc3RyLFxuICAgICAgICAgICAgICAgICAgICBhcnJfbnVtLFxuICAgICAgICAgICAgICAgICAgICBkZWZhdWx0X3N0cixcbiAgICAgICAgICAgICAgICAgICAgb2JqLFxuICAgICAgICAgICAgICAgICAgICBvYmpfbGl0LFxuICAgICAgICAgICAgICAgICAgICByZXF1aXJlZF9zdHIsXG4gICAgICAgICAgICAgICAgICAgIGRlZmF1bHRfcmVxdWlyZWRfc3RyLFxuICAgICAgICAgICAgICAgICAgICBlbnVtZXJhdGlvbixcbiAgICAgICAgICAgICAgICB9KX1cbiAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICA8L2Rpdj5cbiAgICApO1xufTtcblxuVHlwZWRDb21wb25lbnQuZGVmYXVsdFByb3BzID0ge1xuICAgIGRlZmF1bHRfc3RyOiAnZGVmYXVsdCcsXG4gICAgZGVmYXVsdF9yZXF1aXJlZF9zdHI6ICdkZWZhdWx0IHJlcXVpcmVkJyxcbiAgICBkZWZhdWx0X251bTogMyxcbn07XG5cbmV4cG9ydCBkZWZhdWx0IFR5cGVkQ29tcG9uZW50O1xuIiwiaW1wb3J0IFR5cGVkQ29tcG9uZW50IGZyb20gJy4vY29tcG9uZW50cy9UeXBlZENvbXBvbmVudCc7XG5pbXBvcnQgVHlwZWRDbGFzc0NvbXBvbmVudCBmcm9tICcuL2NvbXBvbmVudHMvVHlwZWRDbGFzc0NvbXBvbmVudCc7XG5cbmV4cG9ydCB7VHlwZWRDb21wb25lbnQsIFR5cGVkQ2xhc3NDb21wb25lbnR9O1xuIiwibW9kdWxlLmV4cG9ydHMgPSBfX1dFQlBBQ0tfRVhURVJOQUxfTU9EVUxFX3JlYWN0X187IiwiLy8gVGhlIG1vZHVsZSBjYWNoZVxudmFyIF9fd2VicGFja19tb2R1bGVfY2FjaGVfXyA9IHt9O1xuXG4vLyBUaGUgcmVxdWlyZSBmdW5jdGlvblxuZnVuY3Rpb24gX193ZWJwYWNrX3JlcXVpcmVfXyhtb2R1bGVJZCkge1xuXHQvLyBDaGVjayBpZiBtb2R1bGUgaXMgaW4gY2FjaGVcblx0dmFyIGNhY2hlZE1vZHVsZSA9IF9fd2VicGFja19tb2R1bGVfY2FjaGVfX1ttb2R1bGVJZF07XG5cdGlmIChjYWNoZWRNb2R1bGUgIT09IHVuZGVmaW5lZCkge1xuXHRcdHJldHVybiBjYWNoZWRNb2R1bGUuZXhwb3J0cztcblx0fVxuXHQvLyBDcmVhdGUgYSBuZXcgbW9kdWxlIChhbmQgcHV0IGl0IGludG8gdGhlIGNhY2hlKVxuXHR2YXIgbW9kdWxlID0gX193ZWJwYWNrX21vZHVsZV9jYWNoZV9fW21vZHVsZUlkXSA9IHtcblx0XHQvLyBubyBtb2R1bGUuaWQgbmVlZGVkXG5cdFx0Ly8gbm8gbW9kdWxlLmxvYWRlZCBuZWVkZWRcblx0XHRleHBvcnRzOiB7fVxuXHR9O1xuXG5cdC8vIEV4ZWN1dGUgdGhlIG1vZHVsZSBmdW5jdGlvblxuXHRfX3dlYnBhY2tfbW9kdWxlc19fW21vZHVsZUlkXS5jYWxsKG1vZHVsZS5leHBvcnRzLCBtb2R1bGUsIG1vZHVsZS5leHBvcnRzLCBfX3dlYnBhY2tfcmVxdWlyZV9fKTtcblxuXHQvLyBSZXR1cm4gdGhlIGV4cG9ydHMgb2YgdGhlIG1vZHVsZVxuXHRyZXR1cm4gbW9kdWxlLmV4cG9ydHM7XG59XG5cbiIsIiIsIi8vIHN0YXJ0dXBcbi8vIExvYWQgZW50cnkgbW9kdWxlIGFuZCByZXR1cm4gZXhwb3J0c1xuLy8gVGhpcyBlbnRyeSBtb2R1bGUgaXMgcmVmZXJlbmNlZCBieSBvdGhlciBtb2R1bGVzIHNvIGl0IGNhbid0IGJlIGlubGluZWRcbnZhciBfX3dlYnBhY2tfZXhwb3J0c19fID0gX193ZWJwYWNrX3JlcXVpcmVfXyhcIi4vc3JjL2ludGVybmFsL3RzX2NvbXBvbmVudHMvaW5kZXgudHNcIik7XG4iLCIiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=