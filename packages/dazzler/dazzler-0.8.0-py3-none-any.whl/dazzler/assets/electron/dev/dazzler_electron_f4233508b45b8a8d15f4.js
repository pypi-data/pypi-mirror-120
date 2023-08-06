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
        // @ts-ignore
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
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiZGF6emxlcl9lbGVjdHJvbl9mNDIzMzUwOGI0NWI4YThkMTVmNC5qcyIsIm1hcHBpbmdzIjoiQUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxDQUFDO0FBQ0QsTzs7Ozs7Ozs7Ozs7OztBQ1ZhLHFCQUFhLEdBQUcsZUFBZSxDQUFDO0FBQ2hDLG1CQUFXLEdBQUcsYUFBYSxDQUFDO0FBQzVCLHlCQUFpQixHQUFHLG1CQUFtQixDQUFDO0FBQ3hDLHlCQUFpQixHQUFHLG1CQUFtQixDQUFDO0FBRXJELDRCQUE0QjtBQUM1Qiw2QkFBNkI7QUFDN0IsMkJBQTJCO0FBQzNCLGtDQUFrQzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDUmxDLHdEQUFnQztBQUVoQywwR0FLZ0M7QUFLaEMsSUFBTSxXQUFXLEdBQUcsVUFBQyxLQUF1QjtJQUNqQyxpQkFBYSxHQUFJLEtBQUssY0FBVCxDQUFVO0lBRTlCLGlCQUFTLENBQUM7UUFDTixhQUFhO1FBQ2IsTUFBTSxDQUFDLEdBQUcsQ0FBQyxFQUFFLENBQUMseUJBQWEsRUFBRSxVQUFDLEtBQUssRUFBRSxJQUFJO1lBQ3JDLElBQU0sSUFBSSxHQUFlLElBQUksQ0FBQztZQUM5QixhQUFhLGNBQUssSUFBSSxFQUFFLENBQUM7UUFDN0IsQ0FBQyxDQUFDLENBQUM7UUFDSCxhQUFhO1FBQ2IsTUFBTSxDQUFDLEdBQUcsQ0FBQyxFQUFFLENBQUMsdUJBQVcsRUFBRSxVQUFDLEtBQUssRUFBRSxJQUFJO1lBQ25DLGFBQWEsY0FBSyxJQUFJLEVBQUUsQ0FBQztRQUM3QixDQUFDLENBQUMsQ0FBQztRQUNILGFBQWE7UUFDYixNQUFNLENBQUMsR0FBRyxDQUFDLEVBQUUsQ0FBQyw2QkFBaUIsRUFBRSxVQUFDLEtBQUssRUFBRSxJQUFJO1lBQ3pDLGFBQWEsY0FBSyxJQUFJLEVBQUUsQ0FBQztRQUM3QixDQUFDLENBQUMsQ0FBQztRQUNILGFBQWE7UUFDYixNQUFNLENBQUMsR0FBRzthQUNMLE1BQU0sQ0FBQyw2QkFBaUIsQ0FBQzthQUN6QixJQUFJLENBQUMsVUFBQyxPQUFPLElBQUssb0JBQWEsY0FBSyxPQUFPLEVBQUUsRUFBM0IsQ0FBMkIsQ0FBQyxDQUFDO0lBQ3hELENBQUMsRUFBRSxFQUFFLENBQUMsQ0FBQztJQUVQLE9BQU8sSUFBSSxDQUFDO0FBQ2hCLENBQUMsQ0FBQztBQUVGLGtCQUFlLFdBQVcsQ0FBQzs7Ozs7Ozs7Ozs7Ozs7Ozs7QUN0QzNCLCtJQUFtRDtBQUcvQyxzQkFIRyx3QkFBVyxDQUdIOzs7Ozs7Ozs7OztBQ0hmOzs7Ozs7VUNBQTtVQUNBOztVQUVBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTtVQUNBOztVQUVBO1VBQ0E7O1VBRUE7VUFDQTtVQUNBOzs7O1VFdEJBO1VBQ0E7VUFDQTtVQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vLy93ZWJwYWNrL3VuaXZlcnNhbE1vZHVsZURlZmluaXRpb24/Iiwid2VicGFjazovLy8vLi9zcmMvZWxlY3Ryb24vY29tbW9uL2lwY0V2ZW50cy50cz8iLCJ3ZWJwYWNrOi8vLy8uL3NyYy9lbGVjdHJvbi9yZW5kZXJlci9jb21wb25lbnRzL1dpbmRvd1N0YXRlLnRzeD8iLCJ3ZWJwYWNrOi8vLy8uL3NyYy9lbGVjdHJvbi9yZW5kZXJlci9pbmRleC50cz8iLCJ3ZWJwYWNrOi8vLy9leHRlcm5hbCB7XCJjb21tb25qc1wiOlwicmVhY3RcIixcImNvbW1vbmpzMlwiOlwicmVhY3RcIixcImFtZFwiOlwicmVhY3RcIixcInVtZFwiOlwicmVhY3RcIixcInJvb3RcIjpcIlJlYWN0XCJ9PyIsIndlYnBhY2s6Ly8vL3dlYnBhY2svYm9vdHN0cmFwPyIsIndlYnBhY2s6Ly8vL3dlYnBhY2svYmVmb3JlLXN0YXJ0dXA/Iiwid2VicGFjazovLy8vd2VicGFjay9zdGFydHVwPyIsIndlYnBhY2s6Ly8vL3dlYnBhY2svYWZ0ZXItc3RhcnR1cD8iXSwic291cmNlc0NvbnRlbnQiOlsiKGZ1bmN0aW9uIHdlYnBhY2tVbml2ZXJzYWxNb2R1bGVEZWZpbml0aW9uKHJvb3QsIGZhY3RvcnkpIHtcblx0aWYodHlwZW9mIGV4cG9ydHMgPT09ICdvYmplY3QnICYmIHR5cGVvZiBtb2R1bGUgPT09ICdvYmplY3QnKVxuXHRcdG1vZHVsZS5leHBvcnRzID0gZmFjdG9yeShyZXF1aXJlKFwicmVhY3RcIikpO1xuXHRlbHNlIGlmKHR5cGVvZiBkZWZpbmUgPT09ICdmdW5jdGlvbicgJiYgZGVmaW5lLmFtZClcblx0XHRkZWZpbmUoW1wicmVhY3RcIl0sIGZhY3RvcnkpO1xuXHRlbHNlIGlmKHR5cGVvZiBleHBvcnRzID09PSAnb2JqZWN0Jylcblx0XHRleHBvcnRzW1wiZGF6emxlcl9lbGVjdHJvblwiXSA9IGZhY3RvcnkocmVxdWlyZShcInJlYWN0XCIpKTtcblx0ZWxzZVxuXHRcdHJvb3RbXCJkYXp6bGVyX2VsZWN0cm9uXCJdID0gZmFjdG9yeShyb290W1wiUmVhY3RcIl0pO1xufSkoc2VsZiwgZnVuY3Rpb24oX19XRUJQQUNLX0VYVEVSTkFMX01PRFVMRV9yZWFjdF9fKSB7XG5yZXR1cm4gIiwiZXhwb3J0IGNvbnN0IFdJTkRPV19SRVNJWkUgPSAnV0lORE9XX1JFU0laRSc7XG5leHBvcnQgY29uc3QgV0lORE9XX01PVkUgPSAnV0lORE9XX01PVkUnO1xuZXhwb3J0IGNvbnN0IFdJTkRPV19GVUxMU0NSRUVOID0gJ1dJTkRPV19GVUxMU0NSRUVOJztcbmV4cG9ydCBjb25zdCBXSU5ET1dfU1RBVEVfSU5JVCA9ICdXSU5ET1dfU1RBVEVfSU5JVCc7XG5cbi8vIGV4cG9ydCB0eXBlIFdpbmRvd0V2ZW50ID1cbi8vICAgICB8IHR5cGVvZiBXSU5ET1dfUkVTSVpFXG4vLyAgICAgfCB0eXBlb2YgV0lORE9XX01PVkVcbi8vICAgICB8IHR5cGVvZiBXSU5ET1dfRlVMTFNDUkVFTjtcbiIsImltcG9ydCB7dXNlRWZmZWN0fSBmcm9tICdyZWFjdCc7XG5pbXBvcnQge0RhenpsZXJQcm9wc30gZnJvbSAnLi4vLi4vLi4vY29tbW9ucy9qcy90eXBlcyc7XG5pbXBvcnQge1xuICAgIFdJTkRPV19SRVNJWkUsXG4gICAgV0lORE9XX01PVkUsXG4gICAgV0lORE9XX0ZVTExTQ1JFRU4sXG4gICAgV0lORE9XX1NUQVRFX0lOSVQsXG59IGZyb20gJy4uLy4uL2NvbW1vbi9pcGNFdmVudHMnO1xuaW1wb3J0IHtXaW5kb3dTaXplLCBXaW5kb3dTdGF0dXN9IGZyb20gJy4uLy4uL2NvbW1vbi90eXBlcyc7XG5cbnR5cGUgV2luZG93U3RhdGVQcm9wcyA9IFdpbmRvd1N0YXR1cyAmIHt9ICYgRGF6emxlclByb3BzO1xuXG5jb25zdCBXaW5kb3dTdGF0ZSA9IChwcm9wczogV2luZG93U3RhdGVQcm9wcykgPT4ge1xuICAgIGNvbnN0IHt1cGRhdGVBc3BlY3RzfSA9IHByb3BzO1xuXG4gICAgdXNlRWZmZWN0KCgpID0+IHtcbiAgICAgICAgLy8gQHRzLWlnbm9yZVxuICAgICAgICB3aW5kb3cuaXBjLm9uKFdJTkRPV19SRVNJWkUsIChldmVudCwgZGF0YSkgPT4ge1xuICAgICAgICAgICAgY29uc3Qgc2l6ZTogV2luZG93U2l6ZSA9IGRhdGE7XG4gICAgICAgICAgICB1cGRhdGVBc3BlY3RzKHsuLi5zaXplfSk7XG4gICAgICAgIH0pO1xuICAgICAgICAvLyBAdHMtaWdub3JlXG4gICAgICAgIHdpbmRvdy5pcGMub24oV0lORE9XX01PVkUsIChldmVudCwgZGF0YSkgPT4ge1xuICAgICAgICAgICAgdXBkYXRlQXNwZWN0cyh7Li4uZGF0YX0pO1xuICAgICAgICB9KTtcbiAgICAgICAgLy8gQHRzLWlnbm9yZVxuICAgICAgICB3aW5kb3cuaXBjLm9uKFdJTkRPV19GVUxMU0NSRUVOLCAoZXZlbnQsIGRhdGEpID0+IHtcbiAgICAgICAgICAgIHVwZGF0ZUFzcGVjdHMoey4uLmRhdGF9KTtcbiAgICAgICAgfSk7XG4gICAgICAgIC8vIEB0cy1pZ25vcmVcbiAgICAgICAgd2luZG93LmlwY1xuICAgICAgICAgICAgLmludm9rZShXSU5ET1dfU1RBVEVfSU5JVClcbiAgICAgICAgICAgIC50aGVuKChpbml0aWFsKSA9PiB1cGRhdGVBc3BlY3RzKHsuLi5pbml0aWFsfSkpO1xuICAgIH0sIFtdKTtcblxuICAgIHJldHVybiBudWxsO1xufTtcblxuZXhwb3J0IGRlZmF1bHQgV2luZG93U3RhdGU7XG4iLCJpbXBvcnQgV2luZG93U3RhdGUgZnJvbSAnLi9jb21wb25lbnRzL1dpbmRvd1N0YXRlJztcblxuZXhwb3J0IHtcbiAgICBXaW5kb3dTdGF0ZSxcbn1cbiIsIm1vZHVsZS5leHBvcnRzID0gX19XRUJQQUNLX0VYVEVSTkFMX01PRFVMRV9yZWFjdF9fOyIsIi8vIFRoZSBtb2R1bGUgY2FjaGVcbnZhciBfX3dlYnBhY2tfbW9kdWxlX2NhY2hlX18gPSB7fTtcblxuLy8gVGhlIHJlcXVpcmUgZnVuY3Rpb25cbmZ1bmN0aW9uIF9fd2VicGFja19yZXF1aXJlX18obW9kdWxlSWQpIHtcblx0Ly8gQ2hlY2sgaWYgbW9kdWxlIGlzIGluIGNhY2hlXG5cdHZhciBjYWNoZWRNb2R1bGUgPSBfX3dlYnBhY2tfbW9kdWxlX2NhY2hlX19bbW9kdWxlSWRdO1xuXHRpZiAoY2FjaGVkTW9kdWxlICE9PSB1bmRlZmluZWQpIHtcblx0XHRyZXR1cm4gY2FjaGVkTW9kdWxlLmV4cG9ydHM7XG5cdH1cblx0Ly8gQ3JlYXRlIGEgbmV3IG1vZHVsZSAoYW5kIHB1dCBpdCBpbnRvIHRoZSBjYWNoZSlcblx0dmFyIG1vZHVsZSA9IF9fd2VicGFja19tb2R1bGVfY2FjaGVfX1ttb2R1bGVJZF0gPSB7XG5cdFx0Ly8gbm8gbW9kdWxlLmlkIG5lZWRlZFxuXHRcdC8vIG5vIG1vZHVsZS5sb2FkZWQgbmVlZGVkXG5cdFx0ZXhwb3J0czoge31cblx0fTtcblxuXHQvLyBFeGVjdXRlIHRoZSBtb2R1bGUgZnVuY3Rpb25cblx0X193ZWJwYWNrX21vZHVsZXNfX1ttb2R1bGVJZF0uY2FsbChtb2R1bGUuZXhwb3J0cywgbW9kdWxlLCBtb2R1bGUuZXhwb3J0cywgX193ZWJwYWNrX3JlcXVpcmVfXyk7XG5cblx0Ly8gUmV0dXJuIHRoZSBleHBvcnRzIG9mIHRoZSBtb2R1bGVcblx0cmV0dXJuIG1vZHVsZS5leHBvcnRzO1xufVxuXG4iLCIiLCIvLyBzdGFydHVwXG4vLyBMb2FkIGVudHJ5IG1vZHVsZSBhbmQgcmV0dXJuIGV4cG9ydHNcbi8vIFRoaXMgZW50cnkgbW9kdWxlIGlzIHJlZmVyZW5jZWQgYnkgb3RoZXIgbW9kdWxlcyBzbyBpdCBjYW4ndCBiZSBpbmxpbmVkXG52YXIgX193ZWJwYWNrX2V4cG9ydHNfXyA9IF9fd2VicGFja19yZXF1aXJlX18oXCIuL3NyYy9lbGVjdHJvbi9yZW5kZXJlci9pbmRleC50c1wiKTtcbiIsIiJdLCJuYW1lcyI6W10sInNvdXJjZVJvb3QiOiIifQ==