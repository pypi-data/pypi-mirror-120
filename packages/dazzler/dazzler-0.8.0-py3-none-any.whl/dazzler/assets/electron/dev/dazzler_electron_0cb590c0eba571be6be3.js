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
exports.WINDOW_STATE_INIT = exports.WINDOW_FULLSCREEN = exports.WINDOW_MOVE = exports.WINDOW_RESIZE = void 0;
exports.WINDOW_RESIZE = 'WINDOW_RESIZE';
exports.WINDOW_MOVE = 'WINDOW_MOVE';
exports.WINDOW_FULLSCREEN = 'WINDOW_FULLSCREEN';
exports.WINDOW_STATE_INIT = 'WINDOW_STATE_INIT';
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
exports.__esModule = true;
var react_1 = __webpack_require__(/*! react */ "react");
var ipcEvents_1 = __webpack_require__(/*! ../../common/ipcEvents */ "./src/electron/common/ipcEvents.ts");
// @ts-ignore
console.log(window.ipc);
var WindowState = function (props) {
    var updateAspects = props.updateAspects;
    react_1.useEffect(function () {
        window.ipc.on(ipcEvents_1.WINDOW_RESIZE, function (event, data) {
            var size = data;
            updateAspects(__assign({}, size));
        });
        // @ts-ignore
        window.ipc.on(ipcEvents_1.WINDOW_MOVE, function (event, data) {
            updateAspects(__assign({}, data));
        });
        // @ts-ignore
        window.ipc.on(ipcEvents_1.WINDOW_FULLSCREEN, function (event, data) {
            updateAspects(__assign({}, data));
        });
        // @ts-ignore
        window.ipc
            .invoke(ipcEvents_1.WINDOW_STATE_INIT)
            .then(function (initial) { return updateAspects(__assign({}, initial)); });
    }, []);
    return null;
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
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiZGF6emxlcl9lbGVjdHJvbl8wY2I1OTBjMGViYTU3MWJlNmJlMy5qcyIsIm1hcHBpbmdzIjoiQUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxDQUFDO0FBQ0QsTzs7Ozs7Ozs7Ozs7OztBQ1ZhLHFCQUFhLEdBQUcsZUFBZSxDQUFDO0FBQ2hDLG1CQUFXLEdBQUcsYUFBYSxDQUFDO0FBQzVCLHlCQUFpQixHQUFHLG1CQUFtQixDQUFDO0FBQ3hDLHlCQUFpQixHQUFHLG1CQUFtQixDQUFDO0FBRXJELDRCQUE0QjtBQUM1Qiw2QkFBNkI7QUFDN0IsMkJBQTJCO0FBQzNCLGtDQUFrQzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDUmxDLHdEQUFnQztBQUVoQywwR0FLZ0M7QUFLaEMsYUFBYTtBQUNiLE9BQU8sQ0FBQyxHQUFHLENBQUMsTUFBTSxDQUFDLEdBQUcsQ0FBQztBQUV2QixJQUFNLFdBQVcsR0FBRyxVQUFDLEtBQXVCO0lBQ2pDLGlCQUFhLEdBQUksS0FBSyxjQUFULENBQVU7SUFFOUIsaUJBQVMsQ0FBQztRQUNMLE1BQWMsQ0FBQyxHQUFHLENBQUMsRUFBRSxDQUFDLHlCQUFhLEVBQUUsVUFBQyxLQUFLLEVBQUUsSUFBSTtZQUM5QyxJQUFNLElBQUksR0FBZSxJQUFJLENBQUM7WUFDOUIsYUFBYSxjQUFLLElBQUksRUFBRSxDQUFDO1FBQzdCLENBQUMsQ0FBQyxDQUFDO1FBQ0gsYUFBYTtRQUNaLE1BQWMsQ0FBQyxHQUFHLENBQUMsRUFBRSxDQUFDLHVCQUFXLEVBQUUsVUFBQyxLQUFLLEVBQUUsSUFBSTtZQUM1QyxhQUFhLGNBQUssSUFBSSxFQUFFLENBQUM7UUFDN0IsQ0FBQyxDQUFDLENBQUM7UUFDSCxhQUFhO1FBQ1osTUFBYyxDQUFDLEdBQUcsQ0FBQyxFQUFFLENBQUMsNkJBQWlCLEVBQUUsVUFBQyxLQUFLLEVBQUUsSUFBSTtZQUNsRCxhQUFhLGNBQUssSUFBSSxFQUFFLENBQUM7UUFDN0IsQ0FBQyxDQUFDLENBQUM7UUFDSCxhQUFhO1FBQ1osTUFBYyxDQUFDLEdBQUc7YUFDZCxNQUFNLENBQUMsNkJBQWlCLENBQUM7YUFDekIsSUFBSSxDQUFDLFVBQUMsT0FBTyxJQUFLLG9CQUFhLGNBQUssT0FBTyxFQUFFLEVBQTNCLENBQTJCLENBQUMsQ0FBQztJQUN4RCxDQUFDLEVBQUUsRUFBRSxDQUFDLENBQUM7SUFFUCxPQUFPLElBQUksQ0FBQztBQUNoQixDQUFDLENBQUM7QUFFRixrQkFBZSxXQUFXLENBQUM7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDeEMzQiwrSUFBbUQ7QUFHL0Msc0JBSEcsd0JBQVcsQ0FHSDs7Ozs7Ozs7Ozs7QUNIZjs7Ozs7O1VDQUE7VUFDQTs7VUFFQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTs7VUFFQTtVQUNBOztVQUVBO1VBQ0E7VUFDQTs7OztVRXRCQTtVQUNBO1VBQ0E7VUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovLy8vd2VicGFjay91bml2ZXJzYWxNb2R1bGVEZWZpbml0aW9uPyIsIndlYnBhY2s6Ly8vLy4vc3JjL2VsZWN0cm9uL2NvbW1vbi9pcGNFdmVudHMudHM/Iiwid2VicGFjazovLy8vLi9zcmMvZWxlY3Ryb24vcmVuZGVyZXIvY29tcG9uZW50cy9XaW5kb3dTdGF0ZS50c3g/Iiwid2VicGFjazovLy8vLi9zcmMvZWxlY3Ryb24vcmVuZGVyZXIvaW5kZXgudHM/Iiwid2VicGFjazovLy8vZXh0ZXJuYWwge1wiY29tbW9uanNcIjpcInJlYWN0XCIsXCJjb21tb25qczJcIjpcInJlYWN0XCIsXCJhbWRcIjpcInJlYWN0XCIsXCJ1bWRcIjpcInJlYWN0XCIsXCJyb290XCI6XCJSZWFjdFwifT8iLCJ3ZWJwYWNrOi8vLy93ZWJwYWNrL2Jvb3RzdHJhcD8iLCJ3ZWJwYWNrOi8vLy93ZWJwYWNrL2JlZm9yZS1zdGFydHVwPyIsIndlYnBhY2s6Ly8vL3dlYnBhY2svc3RhcnR1cD8iLCJ3ZWJwYWNrOi8vLy93ZWJwYWNrL2FmdGVyLXN0YXJ0dXA/Il0sInNvdXJjZXNDb250ZW50IjpbIihmdW5jdGlvbiB3ZWJwYWNrVW5pdmVyc2FsTW9kdWxlRGVmaW5pdGlvbihyb290LCBmYWN0b3J5KSB7XG5cdGlmKHR5cGVvZiBleHBvcnRzID09PSAnb2JqZWN0JyAmJiB0eXBlb2YgbW9kdWxlID09PSAnb2JqZWN0Jylcblx0XHRtb2R1bGUuZXhwb3J0cyA9IGZhY3RvcnkocmVxdWlyZShcInJlYWN0XCIpKTtcblx0ZWxzZSBpZih0eXBlb2YgZGVmaW5lID09PSAnZnVuY3Rpb24nICYmIGRlZmluZS5hbWQpXG5cdFx0ZGVmaW5lKFtcInJlYWN0XCJdLCBmYWN0b3J5KTtcblx0ZWxzZSBpZih0eXBlb2YgZXhwb3J0cyA9PT0gJ29iamVjdCcpXG5cdFx0ZXhwb3J0c1tcImRhenpsZXJfZWxlY3Ryb25cIl0gPSBmYWN0b3J5KHJlcXVpcmUoXCJyZWFjdFwiKSk7XG5cdGVsc2Vcblx0XHRyb290W1wiZGF6emxlcl9lbGVjdHJvblwiXSA9IGZhY3Rvcnkocm9vdFtcIlJlYWN0XCJdKTtcbn0pKHNlbGYsIGZ1bmN0aW9uKF9fV0VCUEFDS19FWFRFUk5BTF9NT0RVTEVfcmVhY3RfXykge1xucmV0dXJuICIsImV4cG9ydCBjb25zdCBXSU5ET1dfUkVTSVpFID0gJ1dJTkRPV19SRVNJWkUnO1xuZXhwb3J0IGNvbnN0IFdJTkRPV19NT1ZFID0gJ1dJTkRPV19NT1ZFJztcbmV4cG9ydCBjb25zdCBXSU5ET1dfRlVMTFNDUkVFTiA9ICdXSU5ET1dfRlVMTFNDUkVFTic7XG5leHBvcnQgY29uc3QgV0lORE9XX1NUQVRFX0lOSVQgPSAnV0lORE9XX1NUQVRFX0lOSVQnO1xuXG4vLyBleHBvcnQgdHlwZSBXaW5kb3dFdmVudCA9XG4vLyAgICAgfCB0eXBlb2YgV0lORE9XX1JFU0laRVxuLy8gICAgIHwgdHlwZW9mIFdJTkRPV19NT1ZFXG4vLyAgICAgfCB0eXBlb2YgV0lORE9XX0ZVTExTQ1JFRU47XG4iLCJpbXBvcnQge3VzZUVmZmVjdH0gZnJvbSAncmVhY3QnO1xuaW1wb3J0IHtEYXp6bGVyUHJvcHN9IGZyb20gJy4uLy4uLy4uL2NvbW1vbnMvanMvdHlwZXMnO1xuaW1wb3J0IHtcbiAgICBXSU5ET1dfUkVTSVpFLFxuICAgIFdJTkRPV19NT1ZFLFxuICAgIFdJTkRPV19GVUxMU0NSRUVOLFxuICAgIFdJTkRPV19TVEFURV9JTklULFxufSBmcm9tICcuLi8uLi9jb21tb24vaXBjRXZlbnRzJztcbmltcG9ydCB7V2luZG93U2l6ZSwgV2luZG93U3RhdHVzfSBmcm9tICcuLi8uLi9jb21tb24vdHlwZXMnO1xuXG50eXBlIFdpbmRvd1N0YXRlUHJvcHMgPSBXaW5kb3dTdGF0dXMgJiB7fSAmIERhenpsZXJQcm9wcztcblxuLy8gQHRzLWlnbm9yZVxuY29uc29sZS5sb2cod2luZG93LmlwYylcblxuY29uc3QgV2luZG93U3RhdGUgPSAocHJvcHM6IFdpbmRvd1N0YXRlUHJvcHMpID0+IHtcbiAgICBjb25zdCB7dXBkYXRlQXNwZWN0c30gPSBwcm9wcztcblxuICAgIHVzZUVmZmVjdCgoKSA9PiB7XG4gICAgICAgICh3aW5kb3cgYXMgYW55KS5pcGMub24oV0lORE9XX1JFU0laRSwgKGV2ZW50LCBkYXRhKSA9PiB7XG4gICAgICAgICAgICBjb25zdCBzaXplOiBXaW5kb3dTaXplID0gZGF0YTtcbiAgICAgICAgICAgIHVwZGF0ZUFzcGVjdHMoey4uLnNpemV9KTtcbiAgICAgICAgfSk7XG4gICAgICAgIC8vIEB0cy1pZ25vcmVcbiAgICAgICAgKHdpbmRvdyBhcyBhbnkpLmlwYy5vbihXSU5ET1dfTU9WRSwgKGV2ZW50LCBkYXRhKSA9PiB7XG4gICAgICAgICAgICB1cGRhdGVBc3BlY3RzKHsuLi5kYXRhfSk7XG4gICAgICAgIH0pO1xuICAgICAgICAvLyBAdHMtaWdub3JlXG4gICAgICAgICh3aW5kb3cgYXMgYW55KS5pcGMub24oV0lORE9XX0ZVTExTQ1JFRU4sIChldmVudCwgZGF0YSkgPT4ge1xuICAgICAgICAgICAgdXBkYXRlQXNwZWN0cyh7Li4uZGF0YX0pO1xuICAgICAgICB9KTtcbiAgICAgICAgLy8gQHRzLWlnbm9yZVxuICAgICAgICAod2luZG93IGFzIGFueSkuaXBjXG4gICAgICAgICAgICAuaW52b2tlKFdJTkRPV19TVEFURV9JTklUKVxuICAgICAgICAgICAgLnRoZW4oKGluaXRpYWwpID0+IHVwZGF0ZUFzcGVjdHMoey4uLmluaXRpYWx9KSk7XG4gICAgfSwgW10pO1xuXG4gICAgcmV0dXJuIG51bGw7XG59O1xuXG5leHBvcnQgZGVmYXVsdCBXaW5kb3dTdGF0ZTtcbiIsImltcG9ydCBXaW5kb3dTdGF0ZSBmcm9tICcuL2NvbXBvbmVudHMvV2luZG93U3RhdGUnO1xuXG5leHBvcnQge1xuICAgIFdpbmRvd1N0YXRlLFxufVxuIiwibW9kdWxlLmV4cG9ydHMgPSBfX1dFQlBBQ0tfRVhURVJOQUxfTU9EVUxFX3JlYWN0X187IiwiLy8gVGhlIG1vZHVsZSBjYWNoZVxudmFyIF9fd2VicGFja19tb2R1bGVfY2FjaGVfXyA9IHt9O1xuXG4vLyBUaGUgcmVxdWlyZSBmdW5jdGlvblxuZnVuY3Rpb24gX193ZWJwYWNrX3JlcXVpcmVfXyhtb2R1bGVJZCkge1xuXHQvLyBDaGVjayBpZiBtb2R1bGUgaXMgaW4gY2FjaGVcblx0dmFyIGNhY2hlZE1vZHVsZSA9IF9fd2VicGFja19tb2R1bGVfY2FjaGVfX1ttb2R1bGVJZF07XG5cdGlmIChjYWNoZWRNb2R1bGUgIT09IHVuZGVmaW5lZCkge1xuXHRcdHJldHVybiBjYWNoZWRNb2R1bGUuZXhwb3J0cztcblx0fVxuXHQvLyBDcmVhdGUgYSBuZXcgbW9kdWxlIChhbmQgcHV0IGl0IGludG8gdGhlIGNhY2hlKVxuXHR2YXIgbW9kdWxlID0gX193ZWJwYWNrX21vZHVsZV9jYWNoZV9fW21vZHVsZUlkXSA9IHtcblx0XHQvLyBubyBtb2R1bGUuaWQgbmVlZGVkXG5cdFx0Ly8gbm8gbW9kdWxlLmxvYWRlZCBuZWVkZWRcblx0XHRleHBvcnRzOiB7fVxuXHR9O1xuXG5cdC8vIEV4ZWN1dGUgdGhlIG1vZHVsZSBmdW5jdGlvblxuXHRfX3dlYnBhY2tfbW9kdWxlc19fW21vZHVsZUlkXS5jYWxsKG1vZHVsZS5leHBvcnRzLCBtb2R1bGUsIG1vZHVsZS5leHBvcnRzLCBfX3dlYnBhY2tfcmVxdWlyZV9fKTtcblxuXHQvLyBSZXR1cm4gdGhlIGV4cG9ydHMgb2YgdGhlIG1vZHVsZVxuXHRyZXR1cm4gbW9kdWxlLmV4cG9ydHM7XG59XG5cbiIsIiIsIi8vIHN0YXJ0dXBcbi8vIExvYWQgZW50cnkgbW9kdWxlIGFuZCByZXR1cm4gZXhwb3J0c1xuLy8gVGhpcyBlbnRyeSBtb2R1bGUgaXMgcmVmZXJlbmNlZCBieSBvdGhlciBtb2R1bGVzIHNvIGl0IGNhbid0IGJlIGlubGluZWRcbnZhciBfX3dlYnBhY2tfZXhwb3J0c19fID0gX193ZWJwYWNrX3JlcXVpcmVfXyhcIi4vc3JjL2VsZWN0cm9uL3JlbmRlcmVyL2luZGV4LnRzXCIpO1xuIiwiIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9