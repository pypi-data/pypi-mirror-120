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
// import {DazzlerProps} from '../../../commons/js/types';
// import {ipcRenderer} from 'electron';
var ipcEvents_1 = __webpack_require__(/*! ../../common/ipcEvents */ "./src/electron/common/ipcEvents.ts");
console.log(ipcEvents_1.WINDOW_RESIZE);
var WindowState = function (props) {
    // const {} = props;
    react_1.useEffect(function () {
        // ipcRenderer.on("resize", (event, data) => {
        //     const size: WindowSize = data;
        //     updateAspects({ ...size });
        // })
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
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiZGF6emxlcl9lbGVjdHJvbl84ZTllYjI5Y2VjY2JiYjc2NTJkOC5qcyIsIm1hcHBpbmdzIjoiQUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxDQUFDO0FBQ0QsTzs7Ozs7Ozs7Ozs7OztBQ1ZhLHFCQUFhLEdBQUcsZUFBZSxDQUFDO0FBQ2hDLG1CQUFXLEdBQUcsYUFBYSxDQUFDO0FBQzVCLHlCQUFpQixHQUFHLG1CQUFtQixDQUFDO0FBRXJELDRCQUE0QjtBQUM1Qiw2QkFBNkI7QUFDN0IsMkJBQTJCO0FBQzNCLGtDQUFrQzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7QUNQbEMsc0VBQXVDO0FBQ3ZDLDBEQUEwRDtBQUMxRCx3Q0FBd0M7QUFDeEMsMEdBQXFEO0FBU3JELE9BQU8sQ0FBQyxHQUFHLENBQUMseUJBQWEsQ0FBQyxDQUFDO0FBRTNCLElBQU0sV0FBVyxHQUFHLFVBQUMsS0FBdUI7SUFDeEMsb0JBQW9CO0lBRXBCLGlCQUFTLENBQUM7UUFDTiw4Q0FBOEM7UUFDOUMscUNBQXFDO1FBQ3JDLGtDQUFrQztRQUNsQyxLQUFLO0lBQ1QsQ0FBQyxFQUFFLEVBQUUsQ0FBQyxDQUFDO0lBRVAsT0FBTyw2REFBdUIsQ0FBQztBQUNuQyxDQUFDO0FBRUQsa0JBQWUsV0FBVyxDQUFDOzs7Ozs7Ozs7Ozs7Ozs7OztBQzNCM0IsK0lBQW1EO0FBRy9DLHNCQUhHLHdCQUFXLENBR0g7Ozs7Ozs7Ozs7O0FDSGY7Ozs7OztVQ0FBO1VBQ0E7O1VBRUE7VUFDQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7O1VBRUE7VUFDQTs7VUFFQTtVQUNBO1VBQ0E7Ozs7VUV0QkE7VUFDQTtVQUNBO1VBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vL3dlYnBhY2svdW5pdmVyc2FsTW9kdWxlRGVmaW5pdGlvbj8iLCJ3ZWJwYWNrOi8vLy8uL3NyYy9lbGVjdHJvbi9jb21tb24vaXBjRXZlbnRzLnRzPyIsIndlYnBhY2s6Ly8vLy4vc3JjL2VsZWN0cm9uL3JlbmRlcmVyL2NvbXBvbmVudHMvV2luZG93U3RhdGUudHN4PyIsIndlYnBhY2s6Ly8vLy4vc3JjL2VsZWN0cm9uL3JlbmRlcmVyL2luZGV4LnRzPyIsIndlYnBhY2s6Ly8vL2V4dGVybmFsIHtcImNvbW1vbmpzXCI6XCJyZWFjdFwiLFwiY29tbW9uanMyXCI6XCJyZWFjdFwiLFwiYW1kXCI6XCJyZWFjdFwiLFwidW1kXCI6XCJyZWFjdFwiLFwicm9vdFwiOlwiUmVhY3RcIn0/Iiwid2VicGFjazovLy8vd2VicGFjay9ib290c3RyYXA/Iiwid2VicGFjazovLy8vd2VicGFjay9iZWZvcmUtc3RhcnR1cD8iLCJ3ZWJwYWNrOi8vLy93ZWJwYWNrL3N0YXJ0dXA/Iiwid2VicGFjazovLy8vd2VicGFjay9hZnRlci1zdGFydHVwPyJdLCJzb3VyY2VzQ29udGVudCI6WyIoZnVuY3Rpb24gd2VicGFja1VuaXZlcnNhbE1vZHVsZURlZmluaXRpb24ocm9vdCwgZmFjdG9yeSkge1xuXHRpZih0eXBlb2YgZXhwb3J0cyA9PT0gJ29iamVjdCcgJiYgdHlwZW9mIG1vZHVsZSA9PT0gJ29iamVjdCcpXG5cdFx0bW9kdWxlLmV4cG9ydHMgPSBmYWN0b3J5KHJlcXVpcmUoXCJyZWFjdFwiKSk7XG5cdGVsc2UgaWYodHlwZW9mIGRlZmluZSA9PT0gJ2Z1bmN0aW9uJyAmJiBkZWZpbmUuYW1kKVxuXHRcdGRlZmluZShbXCJyZWFjdFwiXSwgZmFjdG9yeSk7XG5cdGVsc2UgaWYodHlwZW9mIGV4cG9ydHMgPT09ICdvYmplY3QnKVxuXHRcdGV4cG9ydHNbXCJkYXp6bGVyX2VsZWN0cm9uXCJdID0gZmFjdG9yeShyZXF1aXJlKFwicmVhY3RcIikpO1xuXHRlbHNlXG5cdFx0cm9vdFtcImRhenpsZXJfZWxlY3Ryb25cIl0gPSBmYWN0b3J5KHJvb3RbXCJSZWFjdFwiXSk7XG59KShzZWxmLCBmdW5jdGlvbihfX1dFQlBBQ0tfRVhURVJOQUxfTU9EVUxFX3JlYWN0X18pIHtcbnJldHVybiAiLCJleHBvcnQgY29uc3QgV0lORE9XX1JFU0laRSA9ICdXSU5ET1dfUkVTSVpFJztcbmV4cG9ydCBjb25zdCBXSU5ET1dfTU9WRSA9ICdXSU5ET1dfTU9WRSc7XG5leHBvcnQgY29uc3QgV0lORE9XX0ZVTExTQ1JFRU4gPSAnV0lORE9XX0ZVTExTQ1JFRU4nO1xuXG4vLyBleHBvcnQgdHlwZSBXaW5kb3dFdmVudCA9XG4vLyAgICAgfCB0eXBlb2YgV0lORE9XX1JFU0laRVxuLy8gICAgIHwgdHlwZW9mIFdJTkRPV19NT1ZFXG4vLyAgICAgfCB0eXBlb2YgV0lORE9XX0ZVTExTQ1JFRU47XG4iLCJpbXBvcnQgUmVhY3QsIHt1c2VFZmZlY3R9IGZyb20gJ3JlYWN0Jztcbi8vIGltcG9ydCB7RGF6emxlclByb3BzfSBmcm9tICcuLi8uLi8uLi9jb21tb25zL2pzL3R5cGVzJztcbi8vIGltcG9ydCB7aXBjUmVuZGVyZXJ9IGZyb20gJ2VsZWN0cm9uJztcbmltcG9ydCB7V0lORE9XX1JFU0laRX0gZnJvbSAnLi4vLi4vY29tbW9uL2lwY0V2ZW50cyc7XG5pbXBvcnQge1dpbmRvd1NpemV9IGZyb20gJy4uLy4uL2NvbW1vbi90eXBlcyc7XG5cbnR5cGUgV2luZG93U3RhdGVQcm9wcyA9IHtcbiAgICB4PzogbnVtYmVyO1xuICAgIHk/OiBudW1iZXI7XG4gICAgZnVsbHNjcmVlbjogYm9vbGVhbjtcbn0gJiBXaW5kb3dTaXplO1xuXG5jb25zb2xlLmxvZyhXSU5ET1dfUkVTSVpFKTtcblxuY29uc3QgV2luZG93U3RhdGUgPSAocHJvcHM6IFdpbmRvd1N0YXRlUHJvcHMpID0+IHtcbiAgICAvLyBjb25zdCB7fSA9IHByb3BzO1xuXG4gICAgdXNlRWZmZWN0KCgpID0+IHtcbiAgICAgICAgLy8gaXBjUmVuZGVyZXIub24oXCJyZXNpemVcIiwgKGV2ZW50LCBkYXRhKSA9PiB7XG4gICAgICAgIC8vICAgICBjb25zdCBzaXplOiBXaW5kb3dTaXplID0gZGF0YTtcbiAgICAgICAgLy8gICAgIHVwZGF0ZUFzcGVjdHMoeyAuLi5zaXplIH0pO1xuICAgICAgICAvLyB9KVxuICAgIH0sIFtdKTtcblxuICAgIHJldHVybiA8ZGl2PldpbmRvd1N0YXRlZTwvZGl2Pjtcbn1cblxuZXhwb3J0IGRlZmF1bHQgV2luZG93U3RhdGU7XG4iLCJpbXBvcnQgV2luZG93U3RhdGUgZnJvbSAnLi9jb21wb25lbnRzL1dpbmRvd1N0YXRlJztcblxuZXhwb3J0IHtcbiAgICBXaW5kb3dTdGF0ZSxcbn1cbiIsIm1vZHVsZS5leHBvcnRzID0gX19XRUJQQUNLX0VYVEVSTkFMX01PRFVMRV9yZWFjdF9fOyIsIi8vIFRoZSBtb2R1bGUgY2FjaGVcbnZhciBfX3dlYnBhY2tfbW9kdWxlX2NhY2hlX18gPSB7fTtcblxuLy8gVGhlIHJlcXVpcmUgZnVuY3Rpb25cbmZ1bmN0aW9uIF9fd2VicGFja19yZXF1aXJlX18obW9kdWxlSWQpIHtcblx0Ly8gQ2hlY2sgaWYgbW9kdWxlIGlzIGluIGNhY2hlXG5cdHZhciBjYWNoZWRNb2R1bGUgPSBfX3dlYnBhY2tfbW9kdWxlX2NhY2hlX19bbW9kdWxlSWRdO1xuXHRpZiAoY2FjaGVkTW9kdWxlICE9PSB1bmRlZmluZWQpIHtcblx0XHRyZXR1cm4gY2FjaGVkTW9kdWxlLmV4cG9ydHM7XG5cdH1cblx0Ly8gQ3JlYXRlIGEgbmV3IG1vZHVsZSAoYW5kIHB1dCBpdCBpbnRvIHRoZSBjYWNoZSlcblx0dmFyIG1vZHVsZSA9IF9fd2VicGFja19tb2R1bGVfY2FjaGVfX1ttb2R1bGVJZF0gPSB7XG5cdFx0Ly8gbm8gbW9kdWxlLmlkIG5lZWRlZFxuXHRcdC8vIG5vIG1vZHVsZS5sb2FkZWQgbmVlZGVkXG5cdFx0ZXhwb3J0czoge31cblx0fTtcblxuXHQvLyBFeGVjdXRlIHRoZSBtb2R1bGUgZnVuY3Rpb25cblx0X193ZWJwYWNrX21vZHVsZXNfX1ttb2R1bGVJZF0uY2FsbChtb2R1bGUuZXhwb3J0cywgbW9kdWxlLCBtb2R1bGUuZXhwb3J0cywgX193ZWJwYWNrX3JlcXVpcmVfXyk7XG5cblx0Ly8gUmV0dXJuIHRoZSBleHBvcnRzIG9mIHRoZSBtb2R1bGVcblx0cmV0dXJuIG1vZHVsZS5leHBvcnRzO1xufVxuXG4iLCIiLCIvLyBzdGFydHVwXG4vLyBMb2FkIGVudHJ5IG1vZHVsZSBhbmQgcmV0dXJuIGV4cG9ydHNcbi8vIFRoaXMgZW50cnkgbW9kdWxlIGlzIHJlZmVyZW5jZWQgYnkgb3RoZXIgbW9kdWxlcyBzbyBpdCBjYW4ndCBiZSBpbmxpbmVkXG52YXIgX193ZWJwYWNrX2V4cG9ydHNfXyA9IF9fd2VicGFja19yZXF1aXJlX18oXCIuL3NyYy9lbGVjdHJvbi9yZW5kZXJlci9pbmRleC50c1wiKTtcbiIsIiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==