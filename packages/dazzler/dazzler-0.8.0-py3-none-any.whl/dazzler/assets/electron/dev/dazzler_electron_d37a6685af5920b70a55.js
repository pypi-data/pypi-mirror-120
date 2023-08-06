(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory(require("react"));
	else if(typeof define === 'function' && define.amd)
		define(["react"], factory);
	else if(typeof exports === 'object')
		exports["dazzler_electron"] = factory(require("react"));
	else
		root["dazzler_electron"] = factory(root["React"]);
})(self, function(__WEBPACK_EXTERNAL_MODULE_react__) {
return /******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./src/electron/common/ipcEvents.ts":
/*!******************************************!*\
  !*** ./src/electron/common/ipcEvents.ts ***!
  \******************************************/
/***/ ((__unused_webpack_module, exports) => {


exports.__esModule = true;
exports.WINDOW_FULLSCREEN = exports.WINDOW_MOVE = exports.WINDOW_RESIZE = void 0;
exports.WINDOW_RESIZE = 'WINDOW_RESIZE';
exports.WINDOW_MOVE = 'WINDOW_MOVE';
exports.WINDOW_FULLSCREEN = 'WINDOW_FULLSCREEN';
// export type WindowEvent =
//     | typeof WINDOW_RESIZE
//     | typeof WINDOW_MOVE
//     | typeof WINDOW_FULLSCREEN;


/***/ }),

/***/ "./src/electron/renderer/components/WindowState.tsx":
/*!**********************************************************!*\
  !*** ./src/electron/renderer/components/WindowState.tsx ***!
  \**********************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __assign = (this && this.__assign) || function () {
    __assign = Object.assign || function(t) {
        for (var s, i = 1, n = arguments.length; i < n; i++) {
            s = arguments[i];
            for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p))
                t[p] = s[p];
        }
        return t;
    };
    return __assign.apply(this, arguments);
};
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
var electron_1 = __webpack_require__(/*! electron */ "electron");
var ipcEvents_1 = __webpack_require__(/*! ../../common/ipcEvents */ "./src/electron/common/ipcEvents.ts");
// console.log(WINDOW_RESIZE);
var WindowState = function (props) {
    var updateAspects = props.updateAspects;
    react_1.useEffect(function () {
        electron_1.ipcRenderer.on(ipcEvents_1.WINDOW_RESIZE, function (event, data) {
            var size = data;
            updateAspects(__assign({}, size));
        });
        // ipcRenderer.
    }, []);
    return react_1["default"].createElement("div", null, "WindowStatee");
};
exports.default = WindowState;


/***/ }),

/***/ "./src/electron/renderer/index.ts":
/*!****************************************!*\
  !*** ./src/electron/renderer/index.ts ***!
  \****************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
exports.WindowState = void 0;
var WindowState_1 = __importDefault(__webpack_require__(/*! ./components/WindowState */ "./src/electron/renderer/components/WindowState.tsx"));
exports.WindowState = WindowState_1["default"];


/***/ }),

/***/ "electron":
/*!***************************!*\
  !*** external "electron" ***!
  \***************************/
/***/ ((module) => {

module.exports = require("electron");

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
/******/ 	var __webpack_exports__ = __webpack_require__("./src/electron/renderer/index.ts");
/******/ 	
/******/ 	return __webpack_exports__;
/******/ })()
;
});
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiZGF6emxlcl9lbGVjdHJvbl9kMzdhNjY4NWFmNTkyMGI3MGE1NS5qcyIsIm1hcHBpbmdzIjoiQUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxDQUFDO0FBQ0QsTzs7Ozs7Ozs7Ozs7OztBQ1ZhLHFCQUFhLEdBQUcsZUFBZSxDQUFDO0FBQ2hDLG1CQUFXLEdBQUcsYUFBYSxDQUFDO0FBQzVCLHlCQUFpQixHQUFHLG1CQUFtQixDQUFDO0FBRXJELDRCQUE0QjtBQUM1Qiw2QkFBNkI7QUFDN0IsMkJBQTJCO0FBQzNCLGtDQUFrQzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQ1BsQyxzRUFBdUM7QUFFdkMsaUVBQXFDO0FBQ3JDLDBHQUFxRDtBQVVyRCw4QkFBOEI7QUFFOUIsSUFBTSxXQUFXLEdBQUcsVUFBQyxLQUF1QjtJQUNoQyxpQkFBYSxHQUFLLEtBQUssY0FBVixDQUFXO0lBRWhDLGlCQUFTLENBQUM7UUFDTixzQkFBVyxDQUFDLEVBQUUsQ0FBQyx5QkFBYSxFQUFFLFVBQUMsS0FBSyxFQUFFLElBQUk7WUFDdEMsSUFBTSxJQUFJLEdBQWUsSUFBSSxDQUFDO1lBQzlCLGFBQWEsY0FBTSxJQUFJLEVBQUcsQ0FBQztRQUMvQixDQUFDLENBQUMsQ0FBQztRQUVILGVBQWU7SUFDbkIsQ0FBQyxFQUFFLEVBQUUsQ0FBQyxDQUFDO0lBRVAsT0FBTyw2REFBdUIsQ0FBQztBQUNuQyxDQUFDO0FBRUQsa0JBQWUsV0FBVyxDQUFDOzs7Ozs7Ozs7Ozs7Ozs7OztBQzlCM0IsK0lBQW1EO0FBRy9DLHNCQUhHLHdCQUFXLENBR0g7Ozs7Ozs7Ozs7O0FDSGY7Ozs7Ozs7Ozs7QUNBQTs7Ozs7O1VDQUE7VUFDQTs7VUFFQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTs7VUFFQTtVQUNBOztVQUVBO1VBQ0E7VUFDQTs7OztVRXRCQTtVQUNBO1VBQ0E7VUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovLy8vd2VicGFjay91bml2ZXJzYWxNb2R1bGVEZWZpbml0aW9uPyIsIndlYnBhY2s6Ly8vLy4vc3JjL2VsZWN0cm9uL2NvbW1vbi9pcGNFdmVudHMudHM/Iiwid2VicGFjazovLy8vLi9zcmMvZWxlY3Ryb24vcmVuZGVyZXIvY29tcG9uZW50cy9XaW5kb3dTdGF0ZS50c3g/Iiwid2VicGFjazovLy8vLi9zcmMvZWxlY3Ryb24vcmVuZGVyZXIvaW5kZXgudHM/Iiwid2VicGFjazovLy8vZXh0ZXJuYWwgXCJlbGVjdHJvblwiPyIsIndlYnBhY2s6Ly8vL2V4dGVybmFsIHtcImNvbW1vbmpzXCI6XCJyZWFjdFwiLFwiY29tbW9uanMyXCI6XCJyZWFjdFwiLFwiYW1kXCI6XCJyZWFjdFwiLFwidW1kXCI6XCJyZWFjdFwiLFwicm9vdFwiOlwiUmVhY3RcIn0/Iiwid2VicGFjazovLy8vd2VicGFjay9ib290c3RyYXA/Iiwid2VicGFjazovLy8vd2VicGFjay9iZWZvcmUtc3RhcnR1cD8iLCJ3ZWJwYWNrOi8vLy93ZWJwYWNrL3N0YXJ0dXA/Iiwid2VicGFjazovLy8vd2VicGFjay9hZnRlci1zdGFydHVwPyJdLCJzb3VyY2VzQ29udGVudCI6WyIoZnVuY3Rpb24gd2VicGFja1VuaXZlcnNhbE1vZHVsZURlZmluaXRpb24ocm9vdCwgZmFjdG9yeSkge1xuXHRpZih0eXBlb2YgZXhwb3J0cyA9PT0gJ29iamVjdCcgJiYgdHlwZW9mIG1vZHVsZSA9PT0gJ29iamVjdCcpXG5cdFx0bW9kdWxlLmV4cG9ydHMgPSBmYWN0b3J5KHJlcXVpcmUoXCJyZWFjdFwiKSk7XG5cdGVsc2UgaWYodHlwZW9mIGRlZmluZSA9PT0gJ2Z1bmN0aW9uJyAmJiBkZWZpbmUuYW1kKVxuXHRcdGRlZmluZShbXCJyZWFjdFwiXSwgZmFjdG9yeSk7XG5cdGVsc2UgaWYodHlwZW9mIGV4cG9ydHMgPT09ICdvYmplY3QnKVxuXHRcdGV4cG9ydHNbXCJkYXp6bGVyX2VsZWN0cm9uXCJdID0gZmFjdG9yeShyZXF1aXJlKFwicmVhY3RcIikpO1xuXHRlbHNlXG5cdFx0cm9vdFtcImRhenpsZXJfZWxlY3Ryb25cIl0gPSBmYWN0b3J5KHJvb3RbXCJSZWFjdFwiXSk7XG59KShzZWxmLCBmdW5jdGlvbihfX1dFQlBBQ0tfRVhURVJOQUxfTU9EVUxFX3JlYWN0X18pIHtcbnJldHVybiAiLCJleHBvcnQgY29uc3QgV0lORE9XX1JFU0laRSA9ICdXSU5ET1dfUkVTSVpFJztcbmV4cG9ydCBjb25zdCBXSU5ET1dfTU9WRSA9ICdXSU5ET1dfTU9WRSc7XG5leHBvcnQgY29uc3QgV0lORE9XX0ZVTExTQ1JFRU4gPSAnV0lORE9XX0ZVTExTQ1JFRU4nO1xuXG4vLyBleHBvcnQgdHlwZSBXaW5kb3dFdmVudCA9XG4vLyAgICAgfCB0eXBlb2YgV0lORE9XX1JFU0laRVxuLy8gICAgIHwgdHlwZW9mIFdJTkRPV19NT1ZFXG4vLyAgICAgfCB0eXBlb2YgV0lORE9XX0ZVTExTQ1JFRU47XG4iLCJpbXBvcnQgUmVhY3QsIHt1c2VFZmZlY3R9IGZyb20gJ3JlYWN0JztcbmltcG9ydCB7RGF6emxlclByb3BzfSBmcm9tICcuLi8uLi8uLi9jb21tb25zL2pzL3R5cGVzJztcbmltcG9ydCB7aXBjUmVuZGVyZXJ9IGZyb20gJ2VsZWN0cm9uJztcbmltcG9ydCB7V0lORE9XX1JFU0laRX0gZnJvbSAnLi4vLi4vY29tbW9uL2lwY0V2ZW50cyc7XG5pbXBvcnQge1dpbmRvd1NpemV9IGZyb20gJy4uLy4uL2NvbW1vbi90eXBlcyc7XG5cbnR5cGUgV2luZG93U3RhdGVQcm9wcyA9IHtcbiAgICB4PzogbnVtYmVyO1xuICAgIHk/OiBudW1iZXI7XG4gICAgZnVsbHNjcmVlbjogYm9vbGVhbjtcbiAgICB1cGRhdGVBc3BlY3RzOiAoYTogYW55KSA9PiBhbnksXG59ICYgV2luZG93U2l6ZSAmIERhenpsZXJQcm9wcztcblxuLy8gY29uc29sZS5sb2coV0lORE9XX1JFU0laRSk7XG5cbmNvbnN0IFdpbmRvd1N0YXRlID0gKHByb3BzOiBXaW5kb3dTdGF0ZVByb3BzKSA9PiB7XG4gICAgY29uc3QgeyB1cGRhdGVBc3BlY3RzIH0gPSBwcm9wcztcblxuICAgIHVzZUVmZmVjdCgoKSA9PiB7XG4gICAgICAgIGlwY1JlbmRlcmVyLm9uKFdJTkRPV19SRVNJWkUsIChldmVudCwgZGF0YSkgPT4ge1xuICAgICAgICAgICAgY29uc3Qgc2l6ZTogV2luZG93U2l6ZSA9IGRhdGE7XG4gICAgICAgICAgICB1cGRhdGVBc3BlY3RzKHsgLi4uc2l6ZSB9KTtcbiAgICAgICAgfSk7XG5cbiAgICAgICAgLy8gaXBjUmVuZGVyZXIuXG4gICAgfSwgW10pO1xuXG4gICAgcmV0dXJuIDxkaXY+V2luZG93U3RhdGVlPC9kaXY+O1xufVxuXG5leHBvcnQgZGVmYXVsdCBXaW5kb3dTdGF0ZTtcbiIsImltcG9ydCBXaW5kb3dTdGF0ZSBmcm9tICcuL2NvbXBvbmVudHMvV2luZG93U3RhdGUnO1xuXG5leHBvcnQge1xuICAgIFdpbmRvd1N0YXRlLFxufVxuIiwibW9kdWxlLmV4cG9ydHMgPSByZXF1aXJlKFwiZWxlY3Ryb25cIik7IiwibW9kdWxlLmV4cG9ydHMgPSBfX1dFQlBBQ0tfRVhURVJOQUxfTU9EVUxFX3JlYWN0X187IiwiLy8gVGhlIG1vZHVsZSBjYWNoZVxudmFyIF9fd2VicGFja19tb2R1bGVfY2FjaGVfXyA9IHt9O1xuXG4vLyBUaGUgcmVxdWlyZSBmdW5jdGlvblxuZnVuY3Rpb24gX193ZWJwYWNrX3JlcXVpcmVfXyhtb2R1bGVJZCkge1xuXHQvLyBDaGVjayBpZiBtb2R1bGUgaXMgaW4gY2FjaGVcblx0dmFyIGNhY2hlZE1vZHVsZSA9IF9fd2VicGFja19tb2R1bGVfY2FjaGVfX1ttb2R1bGVJZF07XG5cdGlmIChjYWNoZWRNb2R1bGUgIT09IHVuZGVmaW5lZCkge1xuXHRcdHJldHVybiBjYWNoZWRNb2R1bGUuZXhwb3J0cztcblx0fVxuXHQvLyBDcmVhdGUgYSBuZXcgbW9kdWxlIChhbmQgcHV0IGl0IGludG8gdGhlIGNhY2hlKVxuXHR2YXIgbW9kdWxlID0gX193ZWJwYWNrX21vZHVsZV9jYWNoZV9fW21vZHVsZUlkXSA9IHtcblx0XHQvLyBubyBtb2R1bGUuaWQgbmVlZGVkXG5cdFx0Ly8gbm8gbW9kdWxlLmxvYWRlZCBuZWVkZWRcblx0XHRleHBvcnRzOiB7fVxuXHR9O1xuXG5cdC8vIEV4ZWN1dGUgdGhlIG1vZHVsZSBmdW5jdGlvblxuXHRfX3dlYnBhY2tfbW9kdWxlc19fW21vZHVsZUlkXS5jYWxsKG1vZHVsZS5leHBvcnRzLCBtb2R1bGUsIG1vZHVsZS5leHBvcnRzLCBfX3dlYnBhY2tfcmVxdWlyZV9fKTtcblxuXHQvLyBSZXR1cm4gdGhlIGV4cG9ydHMgb2YgdGhlIG1vZHVsZVxuXHRyZXR1cm4gbW9kdWxlLmV4cG9ydHM7XG59XG5cbiIsIiIsIi8vIHN0YXJ0dXBcbi8vIExvYWQgZW50cnkgbW9kdWxlIGFuZCByZXR1cm4gZXhwb3J0c1xuLy8gVGhpcyBlbnRyeSBtb2R1bGUgaXMgcmVmZXJlbmNlZCBieSBvdGhlciBtb2R1bGVzIHNvIGl0IGNhbid0IGJlIGlubGluZWRcbnZhciBfX3dlYnBhY2tfZXhwb3J0c19fID0gX193ZWJwYWNrX3JlcXVpcmVfXyhcIi4vc3JjL2VsZWN0cm9uL3JlbmRlcmVyL2luZGV4LnRzXCIpO1xuIiwiIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9