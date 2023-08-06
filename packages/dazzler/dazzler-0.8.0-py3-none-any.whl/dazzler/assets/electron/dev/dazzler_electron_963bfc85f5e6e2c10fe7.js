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
exports.WINDOW_SET_HEIGHT = exports.WINDOW_SET_WIDTH = exports.WINDOW_SET_BOUNDS = exports.WINDOW_STATE_INIT = exports.WINDOW_FULLSCREEN = exports.WINDOW_MOVE = exports.WINDOW_RESIZE = void 0;
exports.WINDOW_RESIZE = 'WINDOW_RESIZE';
exports.WINDOW_MOVE = 'WINDOW_MOVE';
exports.WINDOW_FULLSCREEN = 'WINDOW_FULLSCREEN';
exports.WINDOW_STATE_INIT = 'WINDOW_STATE_INIT';
exports.WINDOW_SET_BOUNDS = 'WINDOW_SET_BOUNDS';
exports.WINDOW_SET_WIDTH = 'WINDOW_SET_WIDTH';
exports.WINDOW_SET_HEIGHT = 'WINDOW_SET_HEIGHT';
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
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
var react_1 = __webpack_require__(/*! react */ "react");
var ipcEvents_1 = __webpack_require__(/*! ../../common/ipcEvents */ "./src/electron/common/ipcEvents.ts");
var ipc_1 = __importDefault(__webpack_require__(/*! ../ipc */ "./src/electron/renderer/ipc.ts"));
var WindowState = function (props) {
    var updateAspects = props.updateAspects, set_height = props.set_height, height = props.height, set_width = props.set_width, width = props.width;
    react_1.useEffect(function () {
        ipc_1["default"].on(ipcEvents_1.WINDOW_RESIZE, function (event, data) {
            var size = data;
            updateAspects(__assign({}, size));
        });
        // @ts-ignore
        ipc_1["default"].on(ipcEvents_1.WINDOW_MOVE, function (event, data) {
            updateAspects(__assign({}, data));
        });
        // @ts-ignore
        ipc_1["default"].on(ipcEvents_1.WINDOW_FULLSCREEN, function (event, data) {
            updateAspects(__assign({}, data));
        });
        // @ts-ignore
        ipc_1["default"].invoke(ipcEvents_1.WINDOW_STATE_INIT).then(function (initial) {
            return updateAspects(__assign({}, initial));
        });
    }, []);
    react_1.useEffect(function () {
        if (set_width && set_width !== width) {
            ipc_1["default"].send(ipcEvents_1.WINDOW_SET_BOUNDS, { width: set_width });
            updateAspects({ width: null });
        }
    }, [set_width, width, updateAspects]);
    react_1.useEffect(function () {
        if (set_height && set_height !== height) {
            ipc_1["default"].send(ipcEvents_1.WINDOW_SET_BOUNDS, { height: set_height });
            updateAspects({ height: null });
        }
    }, [set_height, height, updateAspects]);
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

/***/ "./src/electron/renderer/ipc.ts":
/*!**************************************!*\
  !*** ./src/electron/renderer/ipc.ts ***!
  \**************************************/
/***/ ((__unused_webpack_module, exports) => {


exports.__esModule = true;
// @ts-ignore
var ipc = window.ipc;
exports.default = ipc;


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
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiZGF6emxlcl9lbGVjdHJvbl85NjNiZmM4NWY1ZTZlMmMxMGZlNy5qcyIsIm1hcHBpbmdzIjoiQUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxDQUFDO0FBQ0QsTzs7Ozs7Ozs7Ozs7OztBQ1ZhLHFCQUFhLEdBQUcsZUFBZSxDQUFDO0FBQ2hDLG1CQUFXLEdBQUcsYUFBYSxDQUFDO0FBQzVCLHlCQUFpQixHQUFHLG1CQUFtQixDQUFDO0FBQ3hDLHlCQUFpQixHQUFHLG1CQUFtQixDQUFDO0FBQ3hDLHlCQUFpQixHQUFHLG1CQUFtQixDQUFDO0FBQ3hDLHdCQUFnQixHQUFHLGtCQUFrQixDQUFDO0FBQ3RDLHlCQUFpQixHQUFHLG1CQUFtQixDQUFDO0FBR3JELDRCQUE0QjtBQUM1Qiw2QkFBNkI7QUFDN0IsMkJBQTJCO0FBQzNCLGtDQUFrQzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDWmxDLHdEQUFnQztBQUVoQywwR0FNZ0M7QUFFaEMsaUdBQXlCO0FBT3pCLElBQU0sV0FBVyxHQUFHLFVBQUMsS0FBdUI7SUFDakMsaUJBQWEsR0FBMEMsS0FBSyxjQUEvQyxFQUFFLFVBQVUsR0FBOEIsS0FBSyxXQUFuQyxFQUFFLE1BQU0sR0FBc0IsS0FBSyxPQUEzQixFQUFFLFNBQVMsR0FBVyxLQUFLLFVBQWhCLEVBQUUsS0FBSyxHQUFJLEtBQUssTUFBVCxDQUFVO0lBRXBFLGlCQUFTLENBQUM7UUFDTixnQkFBRyxDQUFDLEVBQUUsQ0FBQyx5QkFBYSxFQUFFLFVBQUMsS0FBSyxFQUFFLElBQUk7WUFDOUIsSUFBTSxJQUFJLEdBQWUsSUFBSSxDQUFDO1lBQzlCLGFBQWEsY0FBSyxJQUFJLEVBQUUsQ0FBQztRQUM3QixDQUFDLENBQUMsQ0FBQztRQUNILGFBQWE7UUFDYixnQkFBRyxDQUFDLEVBQUUsQ0FBQyx1QkFBVyxFQUFFLFVBQUMsS0FBSyxFQUFFLElBQUk7WUFDNUIsYUFBYSxjQUFLLElBQUksRUFBRSxDQUFDO1FBQzdCLENBQUMsQ0FBQyxDQUFDO1FBQ0gsYUFBYTtRQUNiLGdCQUFHLENBQUMsRUFBRSxDQUFDLDZCQUFpQixFQUFFLFVBQUMsS0FBSyxFQUFFLElBQUk7WUFDbEMsYUFBYSxjQUFLLElBQUksRUFBRSxDQUFDO1FBQzdCLENBQUMsQ0FBQyxDQUFDO1FBQ0gsYUFBYTtRQUNiLGdCQUFHLENBQUMsTUFBTSxDQUFlLDZCQUFpQixDQUFDLENBQUMsSUFBSSxDQUFDLFVBQUMsT0FBTztZQUNyRCxvQkFBYSxjQUFLLE9BQU8sRUFBRTtRQUEzQixDQUEyQixDQUM5QixDQUFDO0lBQ04sQ0FBQyxFQUFFLEVBQUUsQ0FBQyxDQUFDO0lBRVAsaUJBQVMsQ0FBQztRQUNOLElBQUksU0FBUyxJQUFJLFNBQVMsS0FBSyxLQUFLLEVBQUU7WUFDbEMsZ0JBQUcsQ0FBQyxJQUFJLENBQUMsNkJBQWlCLEVBQUUsRUFBQyxLQUFLLEVBQUUsU0FBUyxFQUFDLENBQUMsQ0FBQztZQUNoRCxhQUFhLENBQUMsRUFBQyxLQUFLLEVBQUUsSUFBSSxFQUFDLENBQUMsQ0FBQztTQUNoQztJQUNMLENBQUMsRUFBRSxDQUFDLFNBQVMsRUFBRSxLQUFLLEVBQUUsYUFBYSxDQUFDLENBQUMsQ0FBQztJQUV0QyxpQkFBUyxDQUFDO1FBQ04sSUFBSSxVQUFVLElBQUksVUFBVSxLQUFLLE1BQU0sRUFBRTtZQUNyQyxnQkFBRyxDQUFDLElBQUksQ0FBQyw2QkFBaUIsRUFBRSxFQUFDLE1BQU0sRUFBRSxVQUFVLEVBQUMsQ0FBQyxDQUFDO1lBQ2xELGFBQWEsQ0FBQyxFQUFDLE1BQU0sRUFBRSxJQUFJLEVBQUMsQ0FBQyxDQUFDO1NBQ2pDO0lBQ0wsQ0FBQyxFQUFFLENBQUMsVUFBVSxFQUFFLE1BQU0sRUFBRSxhQUFhLENBQUMsQ0FBQyxDQUFDO0lBRXhDLE9BQU8sSUFBSSxDQUFDO0FBQ2hCLENBQUMsQ0FBQztBQUVGLGtCQUFlLFdBQVcsQ0FBQzs7Ozs7Ozs7Ozs7Ozs7Ozs7QUN4RDNCLCtJQUFtRDtBQUcvQyxzQkFIRyx3QkFBVyxDQUdIOzs7Ozs7Ozs7Ozs7O0FDR2YsYUFBYTtBQUNiLElBQU0sR0FBRyxHQUFTLE1BQU0sQ0FBQyxHQUFHLENBQUM7QUFFN0Isa0JBQWUsR0FBRyxDQUFDOzs7Ozs7Ozs7OztBQ1RuQjs7Ozs7O1VDQUE7VUFDQTs7VUFFQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTs7VUFFQTtVQUNBOztVQUVBO1VBQ0E7VUFDQTs7OztVRXRCQTtVQUNBO1VBQ0E7VUFDQSIsInNvdXJjZXMiOlsid2VicGFjazovLy8vd2VicGFjay91bml2ZXJzYWxNb2R1bGVEZWZpbml0aW9uPyIsIndlYnBhY2s6Ly8vLy4vc3JjL2VsZWN0cm9uL2NvbW1vbi9pcGNFdmVudHMudHM/Iiwid2VicGFjazovLy8vLi9zcmMvZWxlY3Ryb24vcmVuZGVyZXIvY29tcG9uZW50cy9XaW5kb3dTdGF0ZS50c3g/Iiwid2VicGFjazovLy8vLi9zcmMvZWxlY3Ryb24vcmVuZGVyZXIvaW5kZXgudHM/Iiwid2VicGFjazovLy8vLi9zcmMvZWxlY3Ryb24vcmVuZGVyZXIvaXBjLnRzPyIsIndlYnBhY2s6Ly8vL2V4dGVybmFsIHtcImNvbW1vbmpzXCI6XCJyZWFjdFwiLFwiY29tbW9uanMyXCI6XCJyZWFjdFwiLFwiYW1kXCI6XCJyZWFjdFwiLFwidW1kXCI6XCJyZWFjdFwiLFwicm9vdFwiOlwiUmVhY3RcIn0/Iiwid2VicGFjazovLy8vd2VicGFjay9ib290c3RyYXA/Iiwid2VicGFjazovLy8vd2VicGFjay9iZWZvcmUtc3RhcnR1cD8iLCJ3ZWJwYWNrOi8vLy93ZWJwYWNrL3N0YXJ0dXA/Iiwid2VicGFjazovLy8vd2VicGFjay9hZnRlci1zdGFydHVwPyJdLCJzb3VyY2VzQ29udGVudCI6WyIoZnVuY3Rpb24gd2VicGFja1VuaXZlcnNhbE1vZHVsZURlZmluaXRpb24ocm9vdCwgZmFjdG9yeSkge1xuXHRpZih0eXBlb2YgZXhwb3J0cyA9PT0gJ29iamVjdCcgJiYgdHlwZW9mIG1vZHVsZSA9PT0gJ29iamVjdCcpXG5cdFx0bW9kdWxlLmV4cG9ydHMgPSBmYWN0b3J5KHJlcXVpcmUoXCJyZWFjdFwiKSk7XG5cdGVsc2UgaWYodHlwZW9mIGRlZmluZSA9PT0gJ2Z1bmN0aW9uJyAmJiBkZWZpbmUuYW1kKVxuXHRcdGRlZmluZShbXCJyZWFjdFwiXSwgZmFjdG9yeSk7XG5cdGVsc2UgaWYodHlwZW9mIGV4cG9ydHMgPT09ICdvYmplY3QnKVxuXHRcdGV4cG9ydHNbXCJkYXp6bGVyX2VsZWN0cm9uXCJdID0gZmFjdG9yeShyZXF1aXJlKFwicmVhY3RcIikpO1xuXHRlbHNlXG5cdFx0cm9vdFtcImRhenpsZXJfZWxlY3Ryb25cIl0gPSBmYWN0b3J5KHJvb3RbXCJSZWFjdFwiXSk7XG59KShzZWxmLCBmdW5jdGlvbihfX1dFQlBBQ0tfRVhURVJOQUxfTU9EVUxFX3JlYWN0X18pIHtcbnJldHVybiAiLCJleHBvcnQgY29uc3QgV0lORE9XX1JFU0laRSA9ICdXSU5ET1dfUkVTSVpFJztcbmV4cG9ydCBjb25zdCBXSU5ET1dfTU9WRSA9ICdXSU5ET1dfTU9WRSc7XG5leHBvcnQgY29uc3QgV0lORE9XX0ZVTExTQ1JFRU4gPSAnV0lORE9XX0ZVTExTQ1JFRU4nO1xuZXhwb3J0IGNvbnN0IFdJTkRPV19TVEFURV9JTklUID0gJ1dJTkRPV19TVEFURV9JTklUJztcbmV4cG9ydCBjb25zdCBXSU5ET1dfU0VUX0JPVU5EUyA9ICdXSU5ET1dfU0VUX0JPVU5EUyc7XG5leHBvcnQgY29uc3QgV0lORE9XX1NFVF9XSURUSCA9ICdXSU5ET1dfU0VUX1dJRFRIJztcbmV4cG9ydCBjb25zdCBXSU5ET1dfU0VUX0hFSUdIVCA9ICdXSU5ET1dfU0VUX0hFSUdIVCc7XG5cblxuLy8gZXhwb3J0IHR5cGUgV2luZG93RXZlbnQgPVxuLy8gICAgIHwgdHlwZW9mIFdJTkRPV19SRVNJWkVcbi8vICAgICB8IHR5cGVvZiBXSU5ET1dfTU9WRVxuLy8gICAgIHwgdHlwZW9mIFdJTkRPV19GVUxMU0NSRUVOO1xuIiwiaW1wb3J0IHt1c2VFZmZlY3R9IGZyb20gJ3JlYWN0JztcbmltcG9ydCB7RGF6emxlclByb3BzfSBmcm9tICcuLi8uLi8uLi9jb21tb25zL2pzL3R5cGVzJztcbmltcG9ydCB7XG4gICAgV0lORE9XX1JFU0laRSxcbiAgICBXSU5ET1dfTU9WRSxcbiAgICBXSU5ET1dfRlVMTFNDUkVFTixcbiAgICBXSU5ET1dfU1RBVEVfSU5JVCxcbiAgICBXSU5ET1dfU0VUX0JPVU5EUyxcbn0gZnJvbSAnLi4vLi4vY29tbW9uL2lwY0V2ZW50cyc7XG5pbXBvcnQge1dpbmRvd1NpemUsIFdpbmRvd1N0YXR1c30gZnJvbSAnLi4vLi4vY29tbW9uL3R5cGVzJztcbmltcG9ydCBpcGMgZnJvbSAnLi4vaXBjJztcblxudHlwZSBXaW5kb3dTdGF0ZVByb3BzID0gV2luZG93U3RhdHVzICYge1xuICAgIHNldF93aWR0aD86IG51bWJlcjtcbiAgICBzZXRfaGVpZ2h0PzogbnVtYmVyO1xufSAmIERhenpsZXJQcm9wcztcblxuY29uc3QgV2luZG93U3RhdGUgPSAocHJvcHM6IFdpbmRvd1N0YXRlUHJvcHMpID0+IHtcbiAgICBjb25zdCB7dXBkYXRlQXNwZWN0cywgc2V0X2hlaWdodCwgaGVpZ2h0LCBzZXRfd2lkdGgsIHdpZHRofSA9IHByb3BzO1xuXG4gICAgdXNlRWZmZWN0KCgpID0+IHtcbiAgICAgICAgaXBjLm9uKFdJTkRPV19SRVNJWkUsIChldmVudCwgZGF0YSkgPT4ge1xuICAgICAgICAgICAgY29uc3Qgc2l6ZTogV2luZG93U2l6ZSA9IGRhdGE7XG4gICAgICAgICAgICB1cGRhdGVBc3BlY3RzKHsuLi5zaXplfSk7XG4gICAgICAgIH0pO1xuICAgICAgICAvLyBAdHMtaWdub3JlXG4gICAgICAgIGlwYy5vbihXSU5ET1dfTU9WRSwgKGV2ZW50LCBkYXRhKSA9PiB7XG4gICAgICAgICAgICB1cGRhdGVBc3BlY3RzKHsuLi5kYXRhfSk7XG4gICAgICAgIH0pO1xuICAgICAgICAvLyBAdHMtaWdub3JlXG4gICAgICAgIGlwYy5vbihXSU5ET1dfRlVMTFNDUkVFTiwgKGV2ZW50LCBkYXRhKSA9PiB7XG4gICAgICAgICAgICB1cGRhdGVBc3BlY3RzKHsuLi5kYXRhfSk7XG4gICAgICAgIH0pO1xuICAgICAgICAvLyBAdHMtaWdub3JlXG4gICAgICAgIGlwYy5pbnZva2U8V2luZG93U3RhdHVzPihXSU5ET1dfU1RBVEVfSU5JVCkudGhlbigoaW5pdGlhbCkgPT5cbiAgICAgICAgICAgIHVwZGF0ZUFzcGVjdHMoey4uLmluaXRpYWx9KVxuICAgICAgICApO1xuICAgIH0sIFtdKTtcblxuICAgIHVzZUVmZmVjdCgoKSA9PiB7XG4gICAgICAgIGlmIChzZXRfd2lkdGggJiYgc2V0X3dpZHRoICE9PSB3aWR0aCkge1xuICAgICAgICAgICAgaXBjLnNlbmQoV0lORE9XX1NFVF9CT1VORFMsIHt3aWR0aDogc2V0X3dpZHRofSk7XG4gICAgICAgICAgICB1cGRhdGVBc3BlY3RzKHt3aWR0aDogbnVsbH0pO1xuICAgICAgICB9XG4gICAgfSwgW3NldF93aWR0aCwgd2lkdGgsIHVwZGF0ZUFzcGVjdHNdKTtcblxuICAgIHVzZUVmZmVjdCgoKSA9PiB7XG4gICAgICAgIGlmIChzZXRfaGVpZ2h0ICYmIHNldF9oZWlnaHQgIT09IGhlaWdodCkge1xuICAgICAgICAgICAgaXBjLnNlbmQoV0lORE9XX1NFVF9CT1VORFMsIHtoZWlnaHQ6IHNldF9oZWlnaHR9KTtcbiAgICAgICAgICAgIHVwZGF0ZUFzcGVjdHMoe2hlaWdodDogbnVsbH0pO1xuICAgICAgICB9XG4gICAgfSwgW3NldF9oZWlnaHQsIGhlaWdodCwgdXBkYXRlQXNwZWN0c10pO1xuXG4gICAgcmV0dXJuIG51bGw7XG59O1xuXG5leHBvcnQgZGVmYXVsdCBXaW5kb3dTdGF0ZTtcbiIsImltcG9ydCBXaW5kb3dTdGF0ZSBmcm9tICcuL2NvbXBvbmVudHMvV2luZG93U3RhdGUnO1xuXG5leHBvcnQge1xuICAgIFdpbmRvd1N0YXRlLFxufVxuIiwidHlwZSBJcGMgPSB7XG4gICAgb246IChrOiBzdHJpbmcsIGhhbmRsZXI6IGFueSkgPT4gdm9pZDtcbiAgICBpbnZva2U6IDxUPihrOiBzdHJpbmcpID0+IFByb21pc2U8VD47XG4gICAgc2VuZDogKGs6IHN0cmluZywgcGF5bG9hZD86IGFueSkgPT4gdm9pZDtcbn1cblxuLy8gQHRzLWlnbm9yZVxuY29uc3QgaXBjOiBJcGMgID0gd2luZG93LmlwYztcblxuZXhwb3J0IGRlZmF1bHQgaXBjO1xuIiwibW9kdWxlLmV4cG9ydHMgPSBfX1dFQlBBQ0tfRVhURVJOQUxfTU9EVUxFX3JlYWN0X187IiwiLy8gVGhlIG1vZHVsZSBjYWNoZVxudmFyIF9fd2VicGFja19tb2R1bGVfY2FjaGVfXyA9IHt9O1xuXG4vLyBUaGUgcmVxdWlyZSBmdW5jdGlvblxuZnVuY3Rpb24gX193ZWJwYWNrX3JlcXVpcmVfXyhtb2R1bGVJZCkge1xuXHQvLyBDaGVjayBpZiBtb2R1bGUgaXMgaW4gY2FjaGVcblx0dmFyIGNhY2hlZE1vZHVsZSA9IF9fd2VicGFja19tb2R1bGVfY2FjaGVfX1ttb2R1bGVJZF07XG5cdGlmIChjYWNoZWRNb2R1bGUgIT09IHVuZGVmaW5lZCkge1xuXHRcdHJldHVybiBjYWNoZWRNb2R1bGUuZXhwb3J0cztcblx0fVxuXHQvLyBDcmVhdGUgYSBuZXcgbW9kdWxlIChhbmQgcHV0IGl0IGludG8gdGhlIGNhY2hlKVxuXHR2YXIgbW9kdWxlID0gX193ZWJwYWNrX21vZHVsZV9jYWNoZV9fW21vZHVsZUlkXSA9IHtcblx0XHQvLyBubyBtb2R1bGUuaWQgbmVlZGVkXG5cdFx0Ly8gbm8gbW9kdWxlLmxvYWRlZCBuZWVkZWRcblx0XHRleHBvcnRzOiB7fVxuXHR9O1xuXG5cdC8vIEV4ZWN1dGUgdGhlIG1vZHVsZSBmdW5jdGlvblxuXHRfX3dlYnBhY2tfbW9kdWxlc19fW21vZHVsZUlkXS5jYWxsKG1vZHVsZS5leHBvcnRzLCBtb2R1bGUsIG1vZHVsZS5leHBvcnRzLCBfX3dlYnBhY2tfcmVxdWlyZV9fKTtcblxuXHQvLyBSZXR1cm4gdGhlIGV4cG9ydHMgb2YgdGhlIG1vZHVsZVxuXHRyZXR1cm4gbW9kdWxlLmV4cG9ydHM7XG59XG5cbiIsIiIsIi8vIHN0YXJ0dXBcbi8vIExvYWQgZW50cnkgbW9kdWxlIGFuZCByZXR1cm4gZXhwb3J0c1xuLy8gVGhpcyBlbnRyeSBtb2R1bGUgaXMgcmVmZXJlbmNlZCBieSBvdGhlciBtb2R1bGVzIHNvIGl0IGNhbid0IGJlIGlubGluZWRcbnZhciBfX3dlYnBhY2tfZXhwb3J0c19fID0gX193ZWJwYWNrX3JlcXVpcmVfXyhcIi4vc3JjL2VsZWN0cm9uL3JlbmRlcmVyL2luZGV4LnRzXCIpO1xuIiwiIl0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9