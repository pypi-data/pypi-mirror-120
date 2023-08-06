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
console.log(ipcEvents_1.WINDOW_RESIZE);
var WindowState = function (props) {
    var updateAspects = props.updateAspects;
    react_1.useEffect(function () {
        electron_1.ipcRenderer.on(ipcEvents_1.WINDOW_RESIZE, function (event, data) {
            var size = data;
            updateAspects(__assign({}, size));
        });
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
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiZGF6emxlcl9lbGVjdHJvbl8zYzI4ODUwYjRiMzUxNWM2MzJiOS5qcyIsIm1hcHBpbmdzIjoiQUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxDQUFDO0FBQ0QsTzs7Ozs7Ozs7Ozs7OztBQ1ZhLHFCQUFhLEdBQUcsZUFBZSxDQUFDO0FBQ2hDLG1CQUFXLEdBQUcsYUFBYSxDQUFDO0FBQzVCLHlCQUFpQixHQUFHLG1CQUFtQixDQUFDO0FBRXJELDRCQUE0QjtBQUM1Qiw2QkFBNkI7QUFDN0IsMkJBQTJCO0FBQzNCLGtDQUFrQzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQ1BsQyxzRUFBdUM7QUFFdkMsaUVBQXFDO0FBQ3JDLDBHQUFxRDtBQVNyRCxPQUFPLENBQUMsR0FBRyxDQUFDLHlCQUFhLENBQUMsQ0FBQztBQUUzQixJQUFNLFdBQVcsR0FBRyxVQUFDLEtBQXVCO0lBQ2hDLGlCQUFhLEdBQUssS0FBSyxjQUFWLENBQVc7SUFFaEMsaUJBQVMsQ0FBQztRQUNOLHNCQUFXLENBQUMsRUFBRSxDQUFDLHlCQUFhLEVBQUUsVUFBQyxLQUFLLEVBQUUsSUFBSTtZQUN0QyxJQUFNLElBQUksR0FBZSxJQUFJLENBQUM7WUFDOUIsYUFBYSxjQUFNLElBQUksRUFBRyxDQUFDO1FBQy9CLENBQUMsQ0FBQyxDQUFDO0lBQ1AsQ0FBQyxFQUFFLEVBQUUsQ0FBQyxDQUFDO0lBRVAsT0FBTyw2REFBdUIsQ0FBQztBQUNuQyxDQUFDO0FBRUQsa0JBQWUsV0FBVyxDQUFDOzs7Ozs7Ozs7Ozs7Ozs7OztBQzNCM0IsK0lBQW1EO0FBRy9DLHNCQUhHLHdCQUFXLENBR0g7Ozs7Ozs7Ozs7O0FDSGY7Ozs7Ozs7Ozs7QUNBQTs7Ozs7O1VDQUE7VUFDQTs7VUFFQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTs7VUFFQTtVQUNBOztVQUVBO1VBQ0E7VUFDQTs7OztVRXRCQTtVQUNBO1VBQ0E7VUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovLy8vd2VicGFjay91bml2ZXJzYWxNb2R1bGVEZWZpbml0aW9uPyIsIndlYnBhY2s6Ly8vLy4vc3JjL2VsZWN0cm9uL2NvbW1vbi9pcGNFdmVudHMudHM/Iiwid2VicGFjazovLy8vLi9zcmMvZWxlY3Ryb24vcmVuZGVyZXIvY29tcG9uZW50cy9XaW5kb3dTdGF0ZS50c3g/Iiwid2VicGFjazovLy8vLi9zcmMvZWxlY3Ryb24vcmVuZGVyZXIvaW5kZXgudHM/Iiwid2VicGFjazovLy8vZXh0ZXJuYWwgXCJlbGVjdHJvblwiPyIsIndlYnBhY2s6Ly8vL2V4dGVybmFsIHtcImNvbW1vbmpzXCI6XCJyZWFjdFwiLFwiY29tbW9uanMyXCI6XCJyZWFjdFwiLFwiYW1kXCI6XCJyZWFjdFwiLFwidW1kXCI6XCJyZWFjdFwiLFwicm9vdFwiOlwiUmVhY3RcIn0/Iiwid2VicGFjazovLy8vd2VicGFjay9ib290c3RyYXA/Iiwid2VicGFjazovLy8vd2VicGFjay9iZWZvcmUtc3RhcnR1cD8iLCJ3ZWJwYWNrOi8vLy93ZWJwYWNrL3N0YXJ0dXA/Iiwid2VicGFjazovLy8vd2VicGFjay9hZnRlci1zdGFydHVwPyJdLCJzb3VyY2VzQ29udGVudCI6WyIoZnVuY3Rpb24gd2VicGFja1VuaXZlcnNhbE1vZHVsZURlZmluaXRpb24ocm9vdCwgZmFjdG9yeSkge1xuXHRpZih0eXBlb2YgZXhwb3J0cyA9PT0gJ29iamVjdCcgJiYgdHlwZW9mIG1vZHVsZSA9PT0gJ29iamVjdCcpXG5cdFx0bW9kdWxlLmV4cG9ydHMgPSBmYWN0b3J5KHJlcXVpcmUoXCJyZWFjdFwiKSk7XG5cdGVsc2UgaWYodHlwZW9mIGRlZmluZSA9PT0gJ2Z1bmN0aW9uJyAmJiBkZWZpbmUuYW1kKVxuXHRcdGRlZmluZShbXCJyZWFjdFwiXSwgZmFjdG9yeSk7XG5cdGVsc2UgaWYodHlwZW9mIGV4cG9ydHMgPT09ICdvYmplY3QnKVxuXHRcdGV4cG9ydHNbXCJkYXp6bGVyX2VsZWN0cm9uXCJdID0gZmFjdG9yeShyZXF1aXJlKFwicmVhY3RcIikpO1xuXHRlbHNlXG5cdFx0cm9vdFtcImRhenpsZXJfZWxlY3Ryb25cIl0gPSBmYWN0b3J5KHJvb3RbXCJSZWFjdFwiXSk7XG59KShzZWxmLCBmdW5jdGlvbihfX1dFQlBBQ0tfRVhURVJOQUxfTU9EVUxFX3JlYWN0X18pIHtcbnJldHVybiAiLCJleHBvcnQgY29uc3QgV0lORE9XX1JFU0laRSA9ICdXSU5ET1dfUkVTSVpFJztcbmV4cG9ydCBjb25zdCBXSU5ET1dfTU9WRSA9ICdXSU5ET1dfTU9WRSc7XG5leHBvcnQgY29uc3QgV0lORE9XX0ZVTExTQ1JFRU4gPSAnV0lORE9XX0ZVTExTQ1JFRU4nO1xuXG4vLyBleHBvcnQgdHlwZSBXaW5kb3dFdmVudCA9XG4vLyAgICAgfCB0eXBlb2YgV0lORE9XX1JFU0laRVxuLy8gICAgIHwgdHlwZW9mIFdJTkRPV19NT1ZFXG4vLyAgICAgfCB0eXBlb2YgV0lORE9XX0ZVTExTQ1JFRU47XG4iLCJpbXBvcnQgUmVhY3QsIHt1c2VFZmZlY3R9IGZyb20gJ3JlYWN0JztcbmltcG9ydCB7RGF6emxlclByb3BzfSBmcm9tICcuLi8uLi8uLi9jb21tb25zL2pzL3R5cGVzJztcbmltcG9ydCB7aXBjUmVuZGVyZXJ9IGZyb20gJ2VsZWN0cm9uJztcbmltcG9ydCB7V0lORE9XX1JFU0laRX0gZnJvbSAnLi4vLi4vY29tbW9uL2lwY0V2ZW50cyc7XG5pbXBvcnQge1dpbmRvd1NpemV9IGZyb20gJy4uLy4uL2NvbW1vbi90eXBlcyc7XG5cbnR5cGUgV2luZG93U3RhdGVQcm9wcyA9IHtcbiAgICB4PzogbnVtYmVyO1xuICAgIHk/OiBudW1iZXI7XG4gICAgZnVsbHNjcmVlbjogYm9vbGVhbjtcbn0gJiBXaW5kb3dTaXplICYgRGF6emxlclByb3BzO1xuXG5jb25zb2xlLmxvZyhXSU5ET1dfUkVTSVpFKTtcblxuY29uc3QgV2luZG93U3RhdGUgPSAocHJvcHM6IFdpbmRvd1N0YXRlUHJvcHMpID0+IHtcbiAgICBjb25zdCB7IHVwZGF0ZUFzcGVjdHMgfSA9IHByb3BzO1xuXG4gICAgdXNlRWZmZWN0KCgpID0+IHtcbiAgICAgICAgaXBjUmVuZGVyZXIub24oV0lORE9XX1JFU0laRSwgKGV2ZW50LCBkYXRhKSA9PiB7XG4gICAgICAgICAgICBjb25zdCBzaXplOiBXaW5kb3dTaXplID0gZGF0YTtcbiAgICAgICAgICAgIHVwZGF0ZUFzcGVjdHMoeyAuLi5zaXplIH0pO1xuICAgICAgICB9KTtcbiAgICB9LCBbXSk7XG5cbiAgICByZXR1cm4gPGRpdj5XaW5kb3dTdGF0ZWU8L2Rpdj47XG59XG5cbmV4cG9ydCBkZWZhdWx0IFdpbmRvd1N0YXRlO1xuIiwiaW1wb3J0IFdpbmRvd1N0YXRlIGZyb20gJy4vY29tcG9uZW50cy9XaW5kb3dTdGF0ZSc7XG5cbmV4cG9ydCB7XG4gICAgV2luZG93U3RhdGUsXG59XG4iLCJtb2R1bGUuZXhwb3J0cyA9IHJlcXVpcmUoXCJlbGVjdHJvblwiKTsiLCJtb2R1bGUuZXhwb3J0cyA9IF9fV0VCUEFDS19FWFRFUk5BTF9NT0RVTEVfcmVhY3RfXzsiLCIvLyBUaGUgbW9kdWxlIGNhY2hlXG52YXIgX193ZWJwYWNrX21vZHVsZV9jYWNoZV9fID0ge307XG5cbi8vIFRoZSByZXF1aXJlIGZ1bmN0aW9uXG5mdW5jdGlvbiBfX3dlYnBhY2tfcmVxdWlyZV9fKG1vZHVsZUlkKSB7XG5cdC8vIENoZWNrIGlmIG1vZHVsZSBpcyBpbiBjYWNoZVxuXHR2YXIgY2FjaGVkTW9kdWxlID0gX193ZWJwYWNrX21vZHVsZV9jYWNoZV9fW21vZHVsZUlkXTtcblx0aWYgKGNhY2hlZE1vZHVsZSAhPT0gdW5kZWZpbmVkKSB7XG5cdFx0cmV0dXJuIGNhY2hlZE1vZHVsZS5leHBvcnRzO1xuXHR9XG5cdC8vIENyZWF0ZSBhIG5ldyBtb2R1bGUgKGFuZCBwdXQgaXQgaW50byB0aGUgY2FjaGUpXG5cdHZhciBtb2R1bGUgPSBfX3dlYnBhY2tfbW9kdWxlX2NhY2hlX19bbW9kdWxlSWRdID0ge1xuXHRcdC8vIG5vIG1vZHVsZS5pZCBuZWVkZWRcblx0XHQvLyBubyBtb2R1bGUubG9hZGVkIG5lZWRlZFxuXHRcdGV4cG9ydHM6IHt9XG5cdH07XG5cblx0Ly8gRXhlY3V0ZSB0aGUgbW9kdWxlIGZ1bmN0aW9uXG5cdF9fd2VicGFja19tb2R1bGVzX19bbW9kdWxlSWRdLmNhbGwobW9kdWxlLmV4cG9ydHMsIG1vZHVsZSwgbW9kdWxlLmV4cG9ydHMsIF9fd2VicGFja19yZXF1aXJlX18pO1xuXG5cdC8vIFJldHVybiB0aGUgZXhwb3J0cyBvZiB0aGUgbW9kdWxlXG5cdHJldHVybiBtb2R1bGUuZXhwb3J0cztcbn1cblxuIiwiIiwiLy8gc3RhcnR1cFxuLy8gTG9hZCBlbnRyeSBtb2R1bGUgYW5kIHJldHVybiBleHBvcnRzXG4vLyBUaGlzIGVudHJ5IG1vZHVsZSBpcyByZWZlcmVuY2VkIGJ5IG90aGVyIG1vZHVsZXMgc28gaXQgY2FuJ3QgYmUgaW5saW5lZFxudmFyIF9fd2VicGFja19leHBvcnRzX18gPSBfX3dlYnBhY2tfcmVxdWlyZV9fKFwiLi9zcmMvZWxlY3Ryb24vcmVuZGVyZXIvaW5kZXgudHNcIik7XG4iLCIiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=