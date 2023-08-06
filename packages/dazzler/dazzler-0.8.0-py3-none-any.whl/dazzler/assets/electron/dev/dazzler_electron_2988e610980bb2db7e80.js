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
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiZGF6emxlcl9lbGVjdHJvbl8yOTg4ZTYxMDk4MGJiMmRiN2U4MC5qcyIsIm1hcHBpbmdzIjoiQUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxDQUFDO0FBQ0QsTzs7Ozs7Ozs7Ozs7OztBQ1ZhLHFCQUFhLEdBQUcsZUFBZSxDQUFDO0FBQ2hDLG1CQUFXLEdBQUcsYUFBYSxDQUFDO0FBQzVCLHlCQUFpQixHQUFHLG1CQUFtQixDQUFDO0FBQ3hDLHlCQUFpQixHQUFHLG1CQUFtQixDQUFDO0FBRXJELDRCQUE0QjtBQUM1Qiw2QkFBNkI7QUFDN0IsMkJBQTJCO0FBQzNCLGtDQUFrQzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDUmxDLHdEQUFnQztBQUVoQywwR0FLZ0M7QUFLaEMsSUFBTSxXQUFXLEdBQUcsVUFBQyxLQUF1QjtJQUNqQyxpQkFBYSxHQUFJLEtBQUssY0FBVCxDQUFVO0lBRTlCLGlCQUFTLENBQUM7UUFDTCxNQUFjLENBQUMsR0FBRyxDQUFDLEVBQUUsQ0FBQyx5QkFBYSxFQUFFLFVBQUMsS0FBSyxFQUFFLElBQUk7WUFDOUMsSUFBTSxJQUFJLEdBQWUsSUFBSSxDQUFDO1lBQzlCLGFBQWEsY0FBSyxJQUFJLEVBQUUsQ0FBQztRQUM3QixDQUFDLENBQUMsQ0FBQztRQUNILGFBQWE7UUFDWixNQUFjLENBQUMsR0FBRyxDQUFDLEVBQUUsQ0FBQyx1QkFBVyxFQUFFLFVBQUMsS0FBSyxFQUFFLElBQUk7WUFDNUMsYUFBYSxjQUFLLElBQUksRUFBRSxDQUFDO1FBQzdCLENBQUMsQ0FBQyxDQUFDO1FBQ0gsYUFBYTtRQUNaLE1BQWMsQ0FBQyxHQUFHLENBQUMsRUFBRSxDQUFDLDZCQUFpQixFQUFFLFVBQUMsS0FBSyxFQUFFLElBQUk7WUFDbEQsYUFBYSxjQUFLLElBQUksRUFBRSxDQUFDO1FBQzdCLENBQUMsQ0FBQyxDQUFDO1FBQ0gsYUFBYTtRQUNaLE1BQWMsQ0FBQyxHQUFHO2FBQ2QsTUFBTSxDQUFDLDZCQUFpQixDQUFDO2FBQ3pCLElBQUksQ0FBQyxVQUFDLE9BQU8sSUFBSyxvQkFBYSxjQUFLLE9BQU8sRUFBRSxFQUEzQixDQUEyQixDQUFDLENBQUM7SUFDeEQsQ0FBQyxFQUFFLEVBQUUsQ0FBQyxDQUFDO0lBRVAsT0FBTyxJQUFJLENBQUM7QUFDaEIsQ0FBQyxDQUFDO0FBRUYsa0JBQWUsV0FBVyxDQUFDOzs7Ozs7Ozs7Ozs7Ozs7OztBQ3JDM0IsK0lBQW1EO0FBRy9DLHNCQUhHLHdCQUFXLENBR0g7Ozs7Ozs7Ozs7O0FDSGY7Ozs7OztVQ0FBO1VBQ0E7O1VBRUE7VUFDQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7O1VBRUE7VUFDQTs7VUFFQTtVQUNBO1VBQ0E7Ozs7VUV0QkE7VUFDQTtVQUNBO1VBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vL3dlYnBhY2svdW5pdmVyc2FsTW9kdWxlRGVmaW5pdGlvbj8iLCJ3ZWJwYWNrOi8vLy8uL3NyYy9lbGVjdHJvbi9jb21tb24vaXBjRXZlbnRzLnRzPyIsIndlYnBhY2s6Ly8vLy4vc3JjL2VsZWN0cm9uL3JlbmRlcmVyL2NvbXBvbmVudHMvV2luZG93U3RhdGUudHN4PyIsIndlYnBhY2s6Ly8vLy4vc3JjL2VsZWN0cm9uL3JlbmRlcmVyL2luZGV4LnRzPyIsIndlYnBhY2s6Ly8vL2V4dGVybmFsIHtcImNvbW1vbmpzXCI6XCJyZWFjdFwiLFwiY29tbW9uanMyXCI6XCJyZWFjdFwiLFwiYW1kXCI6XCJyZWFjdFwiLFwidW1kXCI6XCJyZWFjdFwiLFwicm9vdFwiOlwiUmVhY3RcIn0/Iiwid2VicGFjazovLy8vd2VicGFjay9ib290c3RyYXA/Iiwid2VicGFjazovLy8vd2VicGFjay9iZWZvcmUtc3RhcnR1cD8iLCJ3ZWJwYWNrOi8vLy93ZWJwYWNrL3N0YXJ0dXA/Iiwid2VicGFjazovLy8vd2VicGFjay9hZnRlci1zdGFydHVwPyJdLCJzb3VyY2VzQ29udGVudCI6WyIoZnVuY3Rpb24gd2VicGFja1VuaXZlcnNhbE1vZHVsZURlZmluaXRpb24ocm9vdCwgZmFjdG9yeSkge1xuXHRpZih0eXBlb2YgZXhwb3J0cyA9PT0gJ29iamVjdCcgJiYgdHlwZW9mIG1vZHVsZSA9PT0gJ29iamVjdCcpXG5cdFx0bW9kdWxlLmV4cG9ydHMgPSBmYWN0b3J5KHJlcXVpcmUoXCJyZWFjdFwiKSk7XG5cdGVsc2UgaWYodHlwZW9mIGRlZmluZSA9PT0gJ2Z1bmN0aW9uJyAmJiBkZWZpbmUuYW1kKVxuXHRcdGRlZmluZShbXCJyZWFjdFwiXSwgZmFjdG9yeSk7XG5cdGVsc2UgaWYodHlwZW9mIGV4cG9ydHMgPT09ICdvYmplY3QnKVxuXHRcdGV4cG9ydHNbXCJkYXp6bGVyX2VsZWN0cm9uXCJdID0gZmFjdG9yeShyZXF1aXJlKFwicmVhY3RcIikpO1xuXHRlbHNlXG5cdFx0cm9vdFtcImRhenpsZXJfZWxlY3Ryb25cIl0gPSBmYWN0b3J5KHJvb3RbXCJSZWFjdFwiXSk7XG59KShzZWxmLCBmdW5jdGlvbihfX1dFQlBBQ0tfRVhURVJOQUxfTU9EVUxFX3JlYWN0X18pIHtcbnJldHVybiAiLCJleHBvcnQgY29uc3QgV0lORE9XX1JFU0laRSA9ICdXSU5ET1dfUkVTSVpFJztcbmV4cG9ydCBjb25zdCBXSU5ET1dfTU9WRSA9ICdXSU5ET1dfTU9WRSc7XG5leHBvcnQgY29uc3QgV0lORE9XX0ZVTExTQ1JFRU4gPSAnV0lORE9XX0ZVTExTQ1JFRU4nO1xuZXhwb3J0IGNvbnN0IFdJTkRPV19TVEFURV9JTklUID0gJ1dJTkRPV19TVEFURV9JTklUJztcblxuLy8gZXhwb3J0IHR5cGUgV2luZG93RXZlbnQgPVxuLy8gICAgIHwgdHlwZW9mIFdJTkRPV19SRVNJWkVcbi8vICAgICB8IHR5cGVvZiBXSU5ET1dfTU9WRVxuLy8gICAgIHwgdHlwZW9mIFdJTkRPV19GVUxMU0NSRUVOO1xuIiwiaW1wb3J0IHt1c2VFZmZlY3R9IGZyb20gJ3JlYWN0JztcbmltcG9ydCB7RGF6emxlclByb3BzfSBmcm9tICcuLi8uLi8uLi9jb21tb25zL2pzL3R5cGVzJztcbmltcG9ydCB7XG4gICAgV0lORE9XX1JFU0laRSxcbiAgICBXSU5ET1dfTU9WRSxcbiAgICBXSU5ET1dfRlVMTFNDUkVFTixcbiAgICBXSU5ET1dfU1RBVEVfSU5JVCxcbn0gZnJvbSAnLi4vLi4vY29tbW9uL2lwY0V2ZW50cyc7XG5pbXBvcnQge1dpbmRvd1NpemUsIFdpbmRvd1N0YXR1c30gZnJvbSAnLi4vLi4vY29tbW9uL3R5cGVzJztcblxudHlwZSBXaW5kb3dTdGF0ZVByb3BzID0gV2luZG93U3RhdHVzICYge30gJiBEYXp6bGVyUHJvcHM7XG5cbmNvbnN0IFdpbmRvd1N0YXRlID0gKHByb3BzOiBXaW5kb3dTdGF0ZVByb3BzKSA9PiB7XG4gICAgY29uc3Qge3VwZGF0ZUFzcGVjdHN9ID0gcHJvcHM7XG5cbiAgICB1c2VFZmZlY3QoKCkgPT4ge1xuICAgICAgICAod2luZG93IGFzIGFueSkuaXBjLm9uKFdJTkRPV19SRVNJWkUsIChldmVudCwgZGF0YSkgPT4ge1xuICAgICAgICAgICAgY29uc3Qgc2l6ZTogV2luZG93U2l6ZSA9IGRhdGE7XG4gICAgICAgICAgICB1cGRhdGVBc3BlY3RzKHsuLi5zaXplfSk7XG4gICAgICAgIH0pO1xuICAgICAgICAvLyBAdHMtaWdub3JlXG4gICAgICAgICh3aW5kb3cgYXMgYW55KS5pcGMub24oV0lORE9XX01PVkUsIChldmVudCwgZGF0YSkgPT4ge1xuICAgICAgICAgICAgdXBkYXRlQXNwZWN0cyh7Li4uZGF0YX0pO1xuICAgICAgICB9KTtcbiAgICAgICAgLy8gQHRzLWlnbm9yZVxuICAgICAgICAod2luZG93IGFzIGFueSkuaXBjLm9uKFdJTkRPV19GVUxMU0NSRUVOLCAoZXZlbnQsIGRhdGEpID0+IHtcbiAgICAgICAgICAgIHVwZGF0ZUFzcGVjdHMoey4uLmRhdGF9KTtcbiAgICAgICAgfSk7XG4gICAgICAgIC8vIEB0cy1pZ25vcmVcbiAgICAgICAgKHdpbmRvdyBhcyBhbnkpLmlwY1xuICAgICAgICAgICAgLmludm9rZShXSU5ET1dfU1RBVEVfSU5JVClcbiAgICAgICAgICAgIC50aGVuKChpbml0aWFsKSA9PiB1cGRhdGVBc3BlY3RzKHsuLi5pbml0aWFsfSkpO1xuICAgIH0sIFtdKTtcblxuICAgIHJldHVybiBudWxsO1xufTtcblxuZXhwb3J0IGRlZmF1bHQgV2luZG93U3RhdGU7XG4iLCJpbXBvcnQgV2luZG93U3RhdGUgZnJvbSAnLi9jb21wb25lbnRzL1dpbmRvd1N0YXRlJztcblxuZXhwb3J0IHtcbiAgICBXaW5kb3dTdGF0ZSxcbn1cbiIsIm1vZHVsZS5leHBvcnRzID0gX19XRUJQQUNLX0VYVEVSTkFMX01PRFVMRV9yZWFjdF9fOyIsIi8vIFRoZSBtb2R1bGUgY2FjaGVcbnZhciBfX3dlYnBhY2tfbW9kdWxlX2NhY2hlX18gPSB7fTtcblxuLy8gVGhlIHJlcXVpcmUgZnVuY3Rpb25cbmZ1bmN0aW9uIF9fd2VicGFja19yZXF1aXJlX18obW9kdWxlSWQpIHtcblx0Ly8gQ2hlY2sgaWYgbW9kdWxlIGlzIGluIGNhY2hlXG5cdHZhciBjYWNoZWRNb2R1bGUgPSBfX3dlYnBhY2tfbW9kdWxlX2NhY2hlX19bbW9kdWxlSWRdO1xuXHRpZiAoY2FjaGVkTW9kdWxlICE9PSB1bmRlZmluZWQpIHtcblx0XHRyZXR1cm4gY2FjaGVkTW9kdWxlLmV4cG9ydHM7XG5cdH1cblx0Ly8gQ3JlYXRlIGEgbmV3IG1vZHVsZSAoYW5kIHB1dCBpdCBpbnRvIHRoZSBjYWNoZSlcblx0dmFyIG1vZHVsZSA9IF9fd2VicGFja19tb2R1bGVfY2FjaGVfX1ttb2R1bGVJZF0gPSB7XG5cdFx0Ly8gbm8gbW9kdWxlLmlkIG5lZWRlZFxuXHRcdC8vIG5vIG1vZHVsZS5sb2FkZWQgbmVlZGVkXG5cdFx0ZXhwb3J0czoge31cblx0fTtcblxuXHQvLyBFeGVjdXRlIHRoZSBtb2R1bGUgZnVuY3Rpb25cblx0X193ZWJwYWNrX21vZHVsZXNfX1ttb2R1bGVJZF0uY2FsbChtb2R1bGUuZXhwb3J0cywgbW9kdWxlLCBtb2R1bGUuZXhwb3J0cywgX193ZWJwYWNrX3JlcXVpcmVfXyk7XG5cblx0Ly8gUmV0dXJuIHRoZSBleHBvcnRzIG9mIHRoZSBtb2R1bGVcblx0cmV0dXJuIG1vZHVsZS5leHBvcnRzO1xufVxuXG4iLCIiLCIvLyBzdGFydHVwXG4vLyBMb2FkIGVudHJ5IG1vZHVsZSBhbmQgcmV0dXJuIGV4cG9ydHNcbi8vIFRoaXMgZW50cnkgbW9kdWxlIGlzIHJlZmVyZW5jZWQgYnkgb3RoZXIgbW9kdWxlcyBzbyBpdCBjYW4ndCBiZSBpbmxpbmVkXG52YXIgX193ZWJwYWNrX2V4cG9ydHNfXyA9IF9fd2VicGFja19yZXF1aXJlX18oXCIuL3NyYy9lbGVjdHJvbi9yZW5kZXJlci9pbmRleC50c1wiKTtcbiIsIiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==