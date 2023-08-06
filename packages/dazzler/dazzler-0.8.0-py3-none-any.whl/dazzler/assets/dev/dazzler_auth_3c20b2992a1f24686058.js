(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory(require("react"));
	else if(typeof define === 'function' && define.amd)
		define(["react"], factory);
	else if(typeof exports === 'object')
		exports["dazzler_auth"] = factory(require("react"));
	else
		root["dazzler_auth"] = factory(root["React"]);
})(self, function(__WEBPACK_EXTERNAL_MODULE_react__) {
return (self["webpackChunkdazzler_name_"] = self["webpackChunkdazzler_name_"] || []).push([["auth"],{

/***/ "./src/auth/scss/index.scss":
/*!**********************************!*\
  !*** ./src/auth/scss/index.scss ***!
  \**********************************/
/***/ (() => {

// extracted by mini-css-extract-plugin

/***/ }),

/***/ "./src/auth/js/components/Login.tsx":
/*!******************************************!*\
  !*** ./src/auth/js/components/Login.tsx ***!
  \******************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
var react_1 = __importDefault(__webpack_require__(/*! react */ "react"));
var commons_1 = __webpack_require__(/*! commons */ "./src/commons/js/index.ts");
var ramda_1 = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
/**
 * A login form to include on dazzler pages.
 *
 * :CSS:
 *
 *     - ``dazzler-auth-login``
 *     - ``login-field``
 *     - ``login-label``
 *     - ``login-input``
 *     - ``login-username``
 *     - ``login-password``
 *     - ``login-button``
 *
 */
var Login = function (props) {
    var class_name = props.class_name, style = props.style, identity = props.identity, method = props.method, login_url = props.login_url, next_url = props.next_url, placeholder_labels = props.placeholder_labels, username_label = props.username_label, password_label = props.password_label, submit_label = props.submit_label, footer = props.footer, header = props.header;
    var css = commons_1.collectTruePropKeys(props, ['horizontal', 'bordered']);
    return (react_1["default"].createElement("form", { className: ramda_1.join(' ', ramda_1.concat([class_name], css)), style: style, id: identity, method: method, action: login_url },
        header && react_1["default"].createElement("div", { className: "login-header" }, header),
        react_1["default"].createElement("input", { type: "hidden", name: "next_url", value: next_url || window.location.href }),
        react_1["default"].createElement("div", { className: "login-field" },
            !placeholder_labels && (react_1["default"].createElement("label", { htmlFor: "login-username-" + identity, className: "login-label" }, username_label)),
            react_1["default"].createElement("input", { type: "text", name: "username", className: "login-field login-username", id: "login-username-" + identity, placeholder: placeholder_labels && username_label })),
        react_1["default"].createElement("div", { className: "login-field" },
            !placeholder_labels && (react_1["default"].createElement("label", { htmlFor: "login-password-" + identity, className: "login-label" }, password_label)),
            react_1["default"].createElement("input", { type: "password", name: "password", className: "login-field login-password", id: "login-password-" + identity, placeholder: placeholder_labels && password_label })),
        react_1["default"].createElement("button", { type: "submit", className: "login-button" }, submit_label),
        footer && react_1["default"].createElement("div", { className: "login-footer" }, footer)));
};
Login.defaultProps = {
    method: 'POST',
    submit_label: 'Login',
    username_label: 'Username',
    password_label: 'Password',
};
exports.default = Login;


/***/ }),

/***/ "./src/auth/js/components/Logout.tsx":
/*!*******************************************!*\
  !*** ./src/auth/js/components/Logout.tsx ***!
  \*******************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
var react_1 = __importDefault(__webpack_require__(/*! react */ "react"));
/**
 * A logout button.
 *
 * :CSS:
 *
 *     - ``dazzler-auth-logout``
 *     - ``logout-button``
 */
var Logout = function (props) {
    var logout_url = props.logout_url, label = props.label, method = props.method, class_name = props.class_name, style = props.style, identity = props.identity, next_url = props.next_url;
    return (react_1["default"].createElement("form", { action: logout_url, method: method, className: class_name, style: style, id: identity },
        react_1["default"].createElement("input", { type: "hidden", name: "next_url", value: next_url || window.location.href }),
        react_1["default"].createElement("button", { type: "submit", className: "logout-button" }, label)));
};
Logout.defaultProps = {
    method: 'POST',
    label: 'Logout',
};
exports.default = Logout;


/***/ }),

/***/ "./src/auth/js/index.ts":
/*!******************************!*\
  !*** ./src/auth/js/index.ts ***!
  \******************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
exports.Logout = exports.Login = void 0;
__webpack_require__(/*! ../scss/index.scss */ "./src/auth/scss/index.scss");
var Login_1 = __importDefault(__webpack_require__(/*! ./components/Login */ "./src/auth/js/components/Login.tsx"));
exports.Login = Login_1["default"];
var Logout_1 = __importDefault(__webpack_require__(/*! ./components/Logout */ "./src/auth/js/components/Logout.tsx"));
exports.Logout = Logout_1["default"];


/***/ }),

/***/ "react":
/*!****************************************************************************************************!*\
  !*** external {"commonjs":"react","commonjs2":"react","amd":"react","umd":"react","root":"React"} ***!
  \****************************************************************************************************/
/***/ ((module) => {

"use strict";
module.exports = __WEBPACK_EXTERNAL_MODULE_react__;

/***/ })

},
/******/ __webpack_require__ => { // webpackRuntimeModules
/******/ var __webpack_exec__ = (moduleId) => (__webpack_require__(__webpack_require__.s = moduleId))
/******/ var __webpack_exports__ = (__webpack_exec__("./src/auth/js/index.ts"));
/******/ return __webpack_exports__;
/******/ }
]);
});
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiZGF6emxlcl9hdXRoXzNjMjBiMjk5MmExZjI0Njg2MDU4LmpzIiwibWFwcGluZ3MiOiJBQUFBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBLENBQUM7QUFDRCxPOzs7Ozs7OztBQ1ZBOzs7Ozs7Ozs7Ozs7Ozs7O0FDQUEseUVBQTBCO0FBQzFCLGdGQUE0QztBQUM1QyxtRkFBbUM7QUFHbkM7Ozs7Ozs7Ozs7Ozs7R0FhRztBQUNILElBQU0sS0FBSyxHQUFHLFVBQUMsS0FBaUI7SUFFeEIsY0FBVSxHQVlWLEtBQUssV0FaSyxFQUNWLEtBQUssR0FXTCxLQUFLLE1BWEEsRUFDTCxRQUFRLEdBVVIsS0FBSyxTQVZHLEVBQ1IsTUFBTSxHQVNOLEtBQUssT0FUQyxFQUNOLFNBQVMsR0FRVCxLQUFLLFVBUkksRUFDVCxRQUFRLEdBT1IsS0FBSyxTQVBHLEVBQ1Isa0JBQWtCLEdBTWxCLEtBQUssbUJBTmEsRUFDbEIsY0FBYyxHQUtkLEtBQUssZUFMUyxFQUNkLGNBQWMsR0FJZCxLQUFLLGVBSlMsRUFDZCxZQUFZLEdBR1osS0FBSyxhQUhPLEVBQ1osTUFBTSxHQUVOLEtBQUssT0FGQyxFQUNOLE1BQU0sR0FDTixLQUFLLE9BREMsQ0FDQTtJQUVWLElBQU0sR0FBRyxHQUFHLDZCQUFtQixDQUFDLEtBQUssRUFBRSxDQUFDLFlBQVksRUFBRSxVQUFVLENBQUMsQ0FBQyxDQUFDO0lBRW5FLE9BQU8sQ0FDSCwyQ0FDSSxTQUFTLEVBQUUsWUFBSSxDQUFDLEdBQUcsRUFBRSxjQUFNLENBQUMsQ0FBQyxVQUFVLENBQUMsRUFBRSxHQUFHLENBQUMsQ0FBQyxFQUMvQyxLQUFLLEVBQUUsS0FBSyxFQUNaLEVBQUUsRUFBRSxRQUFRLEVBQ1osTUFBTSxFQUFFLE1BQU0sRUFDZCxNQUFNLEVBQUUsU0FBUztRQUVoQixNQUFNLElBQUksMENBQUssU0FBUyxFQUFDLGNBQWMsSUFBRSxNQUFNLENBQU87UUFDdkQsNENBQ0ksSUFBSSxFQUFDLFFBQVEsRUFDYixJQUFJLEVBQUMsVUFBVSxFQUNmLEtBQUssRUFBRSxRQUFRLElBQUksTUFBTSxDQUFDLFFBQVEsQ0FBQyxJQUFJLEdBQ3pDO1FBQ0YsMENBQUssU0FBUyxFQUFDLGFBQWE7WUFDdkIsQ0FBQyxrQkFBa0IsSUFBSSxDQUNwQiw0Q0FDSSxPQUFPLEVBQUUsb0JBQWtCLFFBQVUsRUFDckMsU0FBUyxFQUFDLGFBQWEsSUFFdEIsY0FBYyxDQUNYLENBQ1g7WUFDRCw0Q0FDSSxJQUFJLEVBQUMsTUFBTSxFQUNYLElBQUksRUFBQyxVQUFVLEVBQ2YsU0FBUyxFQUFDLDRCQUE0QixFQUN0QyxFQUFFLEVBQUUsb0JBQWtCLFFBQVUsRUFDaEMsV0FBVyxFQUFFLGtCQUFrQixJQUFJLGNBQWMsR0FDbkQsQ0FDQTtRQUNOLDBDQUFLLFNBQVMsRUFBQyxhQUFhO1lBQ3ZCLENBQUMsa0JBQWtCLElBQUksQ0FDcEIsNENBQ0ksT0FBTyxFQUFFLG9CQUFrQixRQUFVLEVBQ3JDLFNBQVMsRUFBQyxhQUFhLElBRXRCLGNBQWMsQ0FDWCxDQUNYO1lBQ0QsNENBQ0ksSUFBSSxFQUFDLFVBQVUsRUFDZixJQUFJLEVBQUMsVUFBVSxFQUNmLFNBQVMsRUFBQyw0QkFBNEIsRUFDdEMsRUFBRSxFQUFFLG9CQUFrQixRQUFVLEVBQ2hDLFdBQVcsRUFBRSxrQkFBa0IsSUFBSSxjQUFjLEdBQ25ELENBQ0E7UUFDTiw2Q0FBUSxJQUFJLEVBQUMsUUFBUSxFQUFDLFNBQVMsRUFBQyxjQUFjLElBQ3pDLFlBQVksQ0FDUjtRQUNSLE1BQU0sSUFBSSwwQ0FBSyxTQUFTLEVBQUMsY0FBYyxJQUFFLE1BQU0sQ0FBTyxDQUNwRCxDQUNWLENBQUM7QUFDTixDQUFDLENBQUM7QUFFRixLQUFLLENBQUMsWUFBWSxHQUFHO0lBQ2pCLE1BQU0sRUFBRSxNQUFNO0lBQ2QsWUFBWSxFQUFFLE9BQU87SUFDckIsY0FBYyxFQUFFLFVBQVU7SUFDMUIsY0FBYyxFQUFFLFVBQVU7Q0FDN0IsQ0FBQztBQUVGLGtCQUFlLEtBQUssQ0FBQzs7Ozs7Ozs7Ozs7Ozs7Ozs7QUNwR3JCLHlFQUEwQjtBQUcxQjs7Ozs7OztHQU9HO0FBQ0gsSUFBTSxNQUFNLEdBQUcsVUFBQyxLQUFrQjtJQUN2QixjQUFVLEdBQ2IsS0FBSyxXQURRLEVBQUUsS0FBSyxHQUNwQixLQUFLLE1BRGUsRUFBRSxNQUFNLEdBQzVCLEtBQUssT0FEdUIsRUFBRSxVQUFVLEdBQ3hDLEtBQUssV0FEbUMsRUFBRSxLQUFLLEdBQy9DLEtBQUssTUFEMEMsRUFBRSxRQUFRLEdBQ3pELEtBQUssU0FEb0QsRUFBRSxRQUFRLEdBQ25FLEtBQUssU0FEOEQsQ0FDN0Q7SUFFVixPQUFPLENBQ0gsMkNBQ0ksTUFBTSxFQUFFLFVBQVUsRUFDbEIsTUFBTSxFQUFFLE1BQU0sRUFDZCxTQUFTLEVBQUUsVUFBVSxFQUNyQixLQUFLLEVBQUUsS0FBSyxFQUNaLEVBQUUsRUFBRSxRQUFRO1FBRVosNENBQ0ksSUFBSSxFQUFDLFFBQVEsRUFDYixJQUFJLEVBQUMsVUFBVSxFQUNmLEtBQUssRUFBRSxRQUFRLElBQUksTUFBTSxDQUFDLFFBQVEsQ0FBQyxJQUFJLEdBQ3pDO1FBQ0YsNkNBQVEsSUFBSSxFQUFDLFFBQVEsRUFBQyxTQUFTLEVBQUMsZUFBZSxJQUMxQyxLQUFLLENBQ0QsQ0FDTixDQUNWLENBQUM7QUFDTixDQUFDLENBQUM7QUFFRixNQUFNLENBQUMsWUFBWSxHQUFHO0lBQ2xCLE1BQU0sRUFBRSxNQUFNO0lBQ2QsS0FBSyxFQUFFLFFBQVE7Q0FDbEIsQ0FBQztBQUVGLGtCQUFlLE1BQU0sQ0FBQzs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDeEN0Qiw0RUFBNEI7QUFFNUIsbUhBQXVDO0FBRy9CLGdCQUhELGtCQUFLLENBR0M7QUFGYixzSEFBeUM7QUFFMUIsaUJBRlIsbUJBQU0sQ0FFUTs7Ozs7Ozs7Ozs7O0FDTHJCIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vLy93ZWJwYWNrL3VuaXZlcnNhbE1vZHVsZURlZmluaXRpb24/Iiwid2VicGFjazovLy8uL3NyYy9hdXRoL3Njc3MvaW5kZXguc2Nzcy8uL3NyYy9hdXRoL3Njc3MvaW5kZXguc2Nzcz8iLCJ3ZWJwYWNrOi8vLy8uL3NyYy9hdXRoL2pzL2NvbXBvbmVudHMvTG9naW4udHN4PyIsIndlYnBhY2s6Ly8vLy4vc3JjL2F1dGgvanMvY29tcG9uZW50cy9Mb2dvdXQudHN4PyIsIndlYnBhY2s6Ly8vLy4vc3JjL2F1dGgvanMvaW5kZXgudHM/Iiwid2VicGFjazovLy8vZXh0ZXJuYWwge1wiY29tbW9uanNcIjpcInJlYWN0XCIsXCJjb21tb25qczJcIjpcInJlYWN0XCIsXCJhbWRcIjpcInJlYWN0XCIsXCJ1bWRcIjpcInJlYWN0XCIsXCJyb290XCI6XCJSZWFjdFwifT8iXSwic291cmNlc0NvbnRlbnQiOlsiKGZ1bmN0aW9uIHdlYnBhY2tVbml2ZXJzYWxNb2R1bGVEZWZpbml0aW9uKHJvb3QsIGZhY3RvcnkpIHtcblx0aWYodHlwZW9mIGV4cG9ydHMgPT09ICdvYmplY3QnICYmIHR5cGVvZiBtb2R1bGUgPT09ICdvYmplY3QnKVxuXHRcdG1vZHVsZS5leHBvcnRzID0gZmFjdG9yeShyZXF1aXJlKFwicmVhY3RcIikpO1xuXHRlbHNlIGlmKHR5cGVvZiBkZWZpbmUgPT09ICdmdW5jdGlvbicgJiYgZGVmaW5lLmFtZClcblx0XHRkZWZpbmUoW1wicmVhY3RcIl0sIGZhY3RvcnkpO1xuXHRlbHNlIGlmKHR5cGVvZiBleHBvcnRzID09PSAnb2JqZWN0Jylcblx0XHRleHBvcnRzW1wiZGF6emxlcl9hdXRoXCJdID0gZmFjdG9yeShyZXF1aXJlKFwicmVhY3RcIikpO1xuXHRlbHNlXG5cdFx0cm9vdFtcImRhenpsZXJfYXV0aFwiXSA9IGZhY3Rvcnkocm9vdFtcIlJlYWN0XCJdKTtcbn0pKHNlbGYsIGZ1bmN0aW9uKF9fV0VCUEFDS19FWFRFUk5BTF9NT0RVTEVfcmVhY3RfXykge1xucmV0dXJuICIsIi8vIGV4dHJhY3RlZCBieSBtaW5pLWNzcy1leHRyYWN0LXBsdWdpbiIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQge2NvbGxlY3RUcnVlUHJvcEtleXN9IGZyb20gJ2NvbW1vbnMnO1xuaW1wb3J0IHtjb25jYXQsIGpvaW59IGZyb20gJ3JhbWRhJztcbmltcG9ydCB7TG9naW5Qcm9wc30gZnJvbSAnLi4vdHlwZXMnO1xuXG4vKipcbiAqIEEgbG9naW4gZm9ybSB0byBpbmNsdWRlIG9uIGRhenpsZXIgcGFnZXMuXG4gKlxuICogOkNTUzpcbiAqXG4gKiAgICAgLSBgYGRhenpsZXItYXV0aC1sb2dpbmBgXG4gKiAgICAgLSBgYGxvZ2luLWZpZWxkYGBcbiAqICAgICAtIGBgbG9naW4tbGFiZWxgYFxuICogICAgIC0gYGBsb2dpbi1pbnB1dGBgXG4gKiAgICAgLSBgYGxvZ2luLXVzZXJuYW1lYGBcbiAqICAgICAtIGBgbG9naW4tcGFzc3dvcmRgYFxuICogICAgIC0gYGBsb2dpbi1idXR0b25gYFxuICpcbiAqL1xuY29uc3QgTG9naW4gPSAocHJvcHM6IExvZ2luUHJvcHMpID0+IHtcbiAgICBjb25zdCB7XG4gICAgICAgIGNsYXNzX25hbWUsXG4gICAgICAgIHN0eWxlLFxuICAgICAgICBpZGVudGl0eSxcbiAgICAgICAgbWV0aG9kLFxuICAgICAgICBsb2dpbl91cmwsXG4gICAgICAgIG5leHRfdXJsLFxuICAgICAgICBwbGFjZWhvbGRlcl9sYWJlbHMsXG4gICAgICAgIHVzZXJuYW1lX2xhYmVsLFxuICAgICAgICBwYXNzd29yZF9sYWJlbCxcbiAgICAgICAgc3VibWl0X2xhYmVsLFxuICAgICAgICBmb290ZXIsXG4gICAgICAgIGhlYWRlcixcbiAgICB9ID0gcHJvcHM7XG5cbiAgICBjb25zdCBjc3MgPSBjb2xsZWN0VHJ1ZVByb3BLZXlzKHByb3BzLCBbJ2hvcml6b250YWwnLCAnYm9yZGVyZWQnXSk7XG5cbiAgICByZXR1cm4gKFxuICAgICAgICA8Zm9ybVxuICAgICAgICAgICAgY2xhc3NOYW1lPXtqb2luKCcgJywgY29uY2F0KFtjbGFzc19uYW1lXSwgY3NzKSl9XG4gICAgICAgICAgICBzdHlsZT17c3R5bGV9XG4gICAgICAgICAgICBpZD17aWRlbnRpdHl9XG4gICAgICAgICAgICBtZXRob2Q9e21ldGhvZH1cbiAgICAgICAgICAgIGFjdGlvbj17bG9naW5fdXJsfVxuICAgICAgICA+XG4gICAgICAgICAgICB7aGVhZGVyICYmIDxkaXYgY2xhc3NOYW1lPVwibG9naW4taGVhZGVyXCI+e2hlYWRlcn08L2Rpdj59XG4gICAgICAgICAgICA8aW5wdXRcbiAgICAgICAgICAgICAgICB0eXBlPVwiaGlkZGVuXCJcbiAgICAgICAgICAgICAgICBuYW1lPVwibmV4dF91cmxcIlxuICAgICAgICAgICAgICAgIHZhbHVlPXtuZXh0X3VybCB8fCB3aW5kb3cubG9jYXRpb24uaHJlZn1cbiAgICAgICAgICAgIC8+XG4gICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT1cImxvZ2luLWZpZWxkXCI+XG4gICAgICAgICAgICAgICAgeyFwbGFjZWhvbGRlcl9sYWJlbHMgJiYgKFxuICAgICAgICAgICAgICAgICAgICA8bGFiZWxcbiAgICAgICAgICAgICAgICAgICAgICAgIGh0bWxGb3I9e2Bsb2dpbi11c2VybmFtZS0ke2lkZW50aXR5fWB9XG4gICAgICAgICAgICAgICAgICAgICAgICBjbGFzc05hbWU9XCJsb2dpbi1sYWJlbFwiXG4gICAgICAgICAgICAgICAgICAgID5cbiAgICAgICAgICAgICAgICAgICAgICAgIHt1c2VybmFtZV9sYWJlbH1cbiAgICAgICAgICAgICAgICAgICAgPC9sYWJlbD5cbiAgICAgICAgICAgICAgICApfVxuICAgICAgICAgICAgICAgIDxpbnB1dFxuICAgICAgICAgICAgICAgICAgICB0eXBlPVwidGV4dFwiXG4gICAgICAgICAgICAgICAgICAgIG5hbWU9XCJ1c2VybmFtZVwiXG4gICAgICAgICAgICAgICAgICAgIGNsYXNzTmFtZT1cImxvZ2luLWZpZWxkIGxvZ2luLXVzZXJuYW1lXCJcbiAgICAgICAgICAgICAgICAgICAgaWQ9e2Bsb2dpbi11c2VybmFtZS0ke2lkZW50aXR5fWB9XG4gICAgICAgICAgICAgICAgICAgIHBsYWNlaG9sZGVyPXtwbGFjZWhvbGRlcl9sYWJlbHMgJiYgdXNlcm5hbWVfbGFiZWx9XG4gICAgICAgICAgICAgICAgLz5cbiAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJsb2dpbi1maWVsZFwiPlxuICAgICAgICAgICAgICAgIHshcGxhY2Vob2xkZXJfbGFiZWxzICYmIChcbiAgICAgICAgICAgICAgICAgICAgPGxhYmVsXG4gICAgICAgICAgICAgICAgICAgICAgICBodG1sRm9yPXtgbG9naW4tcGFzc3dvcmQtJHtpZGVudGl0eX1gfVxuICAgICAgICAgICAgICAgICAgICAgICAgY2xhc3NOYW1lPVwibG9naW4tbGFiZWxcIlxuICAgICAgICAgICAgICAgICAgICA+XG4gICAgICAgICAgICAgICAgICAgICAgICB7cGFzc3dvcmRfbGFiZWx9XG4gICAgICAgICAgICAgICAgICAgIDwvbGFiZWw+XG4gICAgICAgICAgICAgICAgKX1cbiAgICAgICAgICAgICAgICA8aW5wdXRcbiAgICAgICAgICAgICAgICAgICAgdHlwZT1cInBhc3N3b3JkXCJcbiAgICAgICAgICAgICAgICAgICAgbmFtZT1cInBhc3N3b3JkXCJcbiAgICAgICAgICAgICAgICAgICAgY2xhc3NOYW1lPVwibG9naW4tZmllbGQgbG9naW4tcGFzc3dvcmRcIlxuICAgICAgICAgICAgICAgICAgICBpZD17YGxvZ2luLXBhc3N3b3JkLSR7aWRlbnRpdHl9YH1cbiAgICAgICAgICAgICAgICAgICAgcGxhY2Vob2xkZXI9e3BsYWNlaG9sZGVyX2xhYmVscyAmJiBwYXNzd29yZF9sYWJlbH1cbiAgICAgICAgICAgICAgICAvPlxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgICA8YnV0dG9uIHR5cGU9XCJzdWJtaXRcIiBjbGFzc05hbWU9XCJsb2dpbi1idXR0b25cIj5cbiAgICAgICAgICAgICAgICB7c3VibWl0X2xhYmVsfVxuICAgICAgICAgICAgPC9idXR0b24+XG4gICAgICAgICAgICB7Zm9vdGVyICYmIDxkaXYgY2xhc3NOYW1lPVwibG9naW4tZm9vdGVyXCI+e2Zvb3Rlcn08L2Rpdj59XG4gICAgICAgIDwvZm9ybT5cbiAgICApO1xufTtcblxuTG9naW4uZGVmYXVsdFByb3BzID0ge1xuICAgIG1ldGhvZDogJ1BPU1QnLFxuICAgIHN1Ym1pdF9sYWJlbDogJ0xvZ2luJyxcbiAgICB1c2VybmFtZV9sYWJlbDogJ1VzZXJuYW1lJyxcbiAgICBwYXNzd29yZF9sYWJlbDogJ1Bhc3N3b3JkJyxcbn07XG5cbmV4cG9ydCBkZWZhdWx0IExvZ2luO1xuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCB7TG9nb3V0UHJvcHN9IGZyb20gJy4uL3R5cGVzJztcblxuLyoqXG4gKiBBIGxvZ291dCBidXR0b24uXG4gKlxuICogOkNTUzpcbiAqXG4gKiAgICAgLSBgYGRhenpsZXItYXV0aC1sb2dvdXRgYFxuICogICAgIC0gYGBsb2dvdXQtYnV0dG9uYGBcbiAqL1xuY29uc3QgTG9nb3V0ID0gKHByb3BzOiBMb2dvdXRQcm9wcykgPT4ge1xuICAgIGNvbnN0IHtsb2dvdXRfdXJsLCBsYWJlbCwgbWV0aG9kLCBjbGFzc19uYW1lLCBzdHlsZSwgaWRlbnRpdHksIG5leHRfdXJsfSA9XG4gICAgICAgIHByb3BzO1xuXG4gICAgcmV0dXJuIChcbiAgICAgICAgPGZvcm1cbiAgICAgICAgICAgIGFjdGlvbj17bG9nb3V0X3VybH1cbiAgICAgICAgICAgIG1ldGhvZD17bWV0aG9kfVxuICAgICAgICAgICAgY2xhc3NOYW1lPXtjbGFzc19uYW1lfVxuICAgICAgICAgICAgc3R5bGU9e3N0eWxlfVxuICAgICAgICAgICAgaWQ9e2lkZW50aXR5fVxuICAgICAgICA+XG4gICAgICAgICAgICA8aW5wdXRcbiAgICAgICAgICAgICAgICB0eXBlPVwiaGlkZGVuXCJcbiAgICAgICAgICAgICAgICBuYW1lPVwibmV4dF91cmxcIlxuICAgICAgICAgICAgICAgIHZhbHVlPXtuZXh0X3VybCB8fCB3aW5kb3cubG9jYXRpb24uaHJlZn1cbiAgICAgICAgICAgIC8+XG4gICAgICAgICAgICA8YnV0dG9uIHR5cGU9XCJzdWJtaXRcIiBjbGFzc05hbWU9XCJsb2dvdXQtYnV0dG9uXCI+XG4gICAgICAgICAgICAgICAge2xhYmVsfVxuICAgICAgICAgICAgPC9idXR0b24+XG4gICAgICAgIDwvZm9ybT5cbiAgICApO1xufTtcblxuTG9nb3V0LmRlZmF1bHRQcm9wcyA9IHtcbiAgICBtZXRob2Q6ICdQT1NUJyxcbiAgICBsYWJlbDogJ0xvZ291dCcsXG59O1xuXG5leHBvcnQgZGVmYXVsdCBMb2dvdXQ7XG4iLCJpbXBvcnQgJy4uL3Njc3MvaW5kZXguc2Nzcyc7XG5cbmltcG9ydCBMb2dpbiBmcm9tICcuL2NvbXBvbmVudHMvTG9naW4nO1xuaW1wb3J0IExvZ291dCBmcm9tICcuL2NvbXBvbmVudHMvTG9nb3V0JztcblxuZXhwb3J0IHtMb2dpbiwgTG9nb3V0fTtcbiIsIm1vZHVsZS5leHBvcnRzID0gX19XRUJQQUNLX0VYVEVSTkFMX01PRFVMRV9yZWFjdF9fOyJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==