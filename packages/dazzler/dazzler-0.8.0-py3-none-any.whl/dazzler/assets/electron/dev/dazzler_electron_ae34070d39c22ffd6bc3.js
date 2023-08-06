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
var WindowState = function (props) {
    var updateAspects = props.updateAspects;
    react_1.useEffect(function () {
        electron_1.ipcRenderer.on(ipcEvents_1.WINDOW_RESIZE, function (event, data) {
            var size = data;
            updateAspects(__assign({}, size));
        });
        electron_1.ipcRenderer.on(ipcEvents_1.WINDOW_MOVE, function (event, data) {
            updateAspects(__assign({}, data));
        });
        electron_1.ipcRenderer.on(ipcEvents_1.WINDOW_FULLSCREEN, function (event, data) {
            updateAspects(__assign({}, data));
        });
        electron_1.ipcRenderer
            .invoke(ipcEvents_1.WINDOW_STATE_INIT)
            .then(function (initial) { return updateAspects(__assign({}, initial)); });
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
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiZGF6emxlcl9lbGVjdHJvbl9hZTM0MDcwZDM5YzIyZmZkNmJjMy5qcyIsIm1hcHBpbmdzIjoiQUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxDQUFDO0FBQ0QsTzs7Ozs7Ozs7Ozs7OztBQ1ZhLHFCQUFhLEdBQUcsZUFBZSxDQUFDO0FBQ2hDLG1CQUFXLEdBQUcsYUFBYSxDQUFDO0FBQzVCLHlCQUFpQixHQUFHLG1CQUFtQixDQUFDO0FBQ3hDLHlCQUFpQixHQUFHLG1CQUFtQixDQUFDO0FBRXJELDRCQUE0QjtBQUM1Qiw2QkFBNkI7QUFDN0IsMkJBQTJCO0FBQzNCLGtDQUFrQzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQ1JsQyxzRUFBdUM7QUFFdkMsaUVBQXFDO0FBQ3JDLDBHQUtnQztBQUtoQyxJQUFNLFdBQVcsR0FBRyxVQUFDLEtBQXVCO0lBQ2pDLGlCQUFhLEdBQUksS0FBSyxjQUFULENBQVU7SUFFOUIsaUJBQVMsQ0FBQztRQUNOLHNCQUFXLENBQUMsRUFBRSxDQUFDLHlCQUFhLEVBQUUsVUFBQyxLQUFLLEVBQUUsSUFBSTtZQUN0QyxJQUFNLElBQUksR0FBZSxJQUFJLENBQUM7WUFDOUIsYUFBYSxjQUFLLElBQUksRUFBRSxDQUFDO1FBQzdCLENBQUMsQ0FBQyxDQUFDO1FBQ0gsc0JBQVcsQ0FBQyxFQUFFLENBQUMsdUJBQVcsRUFBRSxVQUFDLEtBQUssRUFBRSxJQUFJO1lBQ3BDLGFBQWEsY0FBSyxJQUFJLEVBQUUsQ0FBQztRQUM3QixDQUFDLENBQUMsQ0FBQztRQUNILHNCQUFXLENBQUMsRUFBRSxDQUFDLDZCQUFpQixFQUFFLFVBQUMsS0FBSyxFQUFFLElBQUk7WUFDMUMsYUFBYSxjQUFLLElBQUksRUFBRSxDQUFDO1FBQzdCLENBQUMsQ0FBQyxDQUFDO1FBQ0gsc0JBQVc7YUFDTixNQUFNLENBQUMsNkJBQWlCLENBQUM7YUFDekIsSUFBSSxDQUFDLFVBQUMsT0FBTyxJQUFLLG9CQUFhLGNBQUssT0FBTyxFQUFFLEVBQTNCLENBQTJCLENBQUMsQ0FBQztJQUN4RCxDQUFDLEVBQUUsRUFBRSxDQUFDLENBQUM7SUFFUCxPQUFPLDZEQUF1QixDQUFDO0FBQ25DLENBQUMsQ0FBQztBQUVGLGtCQUFlLFdBQVcsQ0FBQzs7Ozs7Ozs7Ozs7Ozs7Ozs7QUNuQzNCLCtJQUFtRDtBQUcvQyxzQkFIRyx3QkFBVyxDQUdIOzs7Ozs7Ozs7OztBQ0hmOzs7Ozs7Ozs7O0FDQUE7Ozs7OztVQ0FBO1VBQ0E7O1VBRUE7VUFDQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7O1VBRUE7VUFDQTs7VUFFQTtVQUNBO1VBQ0E7Ozs7VUV0QkE7VUFDQTtVQUNBO1VBQ0EiLCJzb3VyY2VzIjpbIndlYnBhY2s6Ly8vL3dlYnBhY2svdW5pdmVyc2FsTW9kdWxlRGVmaW5pdGlvbj8iLCJ3ZWJwYWNrOi8vLy8uL3NyYy9lbGVjdHJvbi9jb21tb24vaXBjRXZlbnRzLnRzPyIsIndlYnBhY2s6Ly8vLy4vc3JjL2VsZWN0cm9uL3JlbmRlcmVyL2NvbXBvbmVudHMvV2luZG93U3RhdGUudHN4PyIsIndlYnBhY2s6Ly8vLy4vc3JjL2VsZWN0cm9uL3JlbmRlcmVyL2luZGV4LnRzPyIsIndlYnBhY2s6Ly8vL2V4dGVybmFsIFwiZWxlY3Ryb25cIj8iLCJ3ZWJwYWNrOi8vLy9leHRlcm5hbCB7XCJjb21tb25qc1wiOlwicmVhY3RcIixcImNvbW1vbmpzMlwiOlwicmVhY3RcIixcImFtZFwiOlwicmVhY3RcIixcInVtZFwiOlwicmVhY3RcIixcInJvb3RcIjpcIlJlYWN0XCJ9PyIsIndlYnBhY2s6Ly8vL3dlYnBhY2svYm9vdHN0cmFwPyIsIndlYnBhY2s6Ly8vL3dlYnBhY2svYmVmb3JlLXN0YXJ0dXA/Iiwid2VicGFjazovLy8vd2VicGFjay9zdGFydHVwPyIsIndlYnBhY2s6Ly8vL3dlYnBhY2svYWZ0ZXItc3RhcnR1cD8iXSwic291cmNlc0NvbnRlbnQiOlsiKGZ1bmN0aW9uIHdlYnBhY2tVbml2ZXJzYWxNb2R1bGVEZWZpbml0aW9uKHJvb3QsIGZhY3RvcnkpIHtcblx0aWYodHlwZW9mIGV4cG9ydHMgPT09ICdvYmplY3QnICYmIHR5cGVvZiBtb2R1bGUgPT09ICdvYmplY3QnKVxuXHRcdG1vZHVsZS5leHBvcnRzID0gZmFjdG9yeShyZXF1aXJlKFwicmVhY3RcIikpO1xuXHRlbHNlIGlmKHR5cGVvZiBkZWZpbmUgPT09ICdmdW5jdGlvbicgJiYgZGVmaW5lLmFtZClcblx0XHRkZWZpbmUoW1wicmVhY3RcIl0sIGZhY3RvcnkpO1xuXHRlbHNlIGlmKHR5cGVvZiBleHBvcnRzID09PSAnb2JqZWN0Jylcblx0XHRleHBvcnRzW1wiZGF6emxlcl9lbGVjdHJvblwiXSA9IGZhY3RvcnkocmVxdWlyZShcInJlYWN0XCIpKTtcblx0ZWxzZVxuXHRcdHJvb3RbXCJkYXp6bGVyX2VsZWN0cm9uXCJdID0gZmFjdG9yeShyb290W1wiUmVhY3RcIl0pO1xufSkoc2VsZiwgZnVuY3Rpb24oX19XRUJQQUNLX0VYVEVSTkFMX01PRFVMRV9yZWFjdF9fKSB7XG5yZXR1cm4gIiwiZXhwb3J0IGNvbnN0IFdJTkRPV19SRVNJWkUgPSAnV0lORE9XX1JFU0laRSc7XG5leHBvcnQgY29uc3QgV0lORE9XX01PVkUgPSAnV0lORE9XX01PVkUnO1xuZXhwb3J0IGNvbnN0IFdJTkRPV19GVUxMU0NSRUVOID0gJ1dJTkRPV19GVUxMU0NSRUVOJztcbmV4cG9ydCBjb25zdCBXSU5ET1dfU1RBVEVfSU5JVCA9ICdXSU5ET1dfU1RBVEVfSU5JVCc7XG5cbi8vIGV4cG9ydCB0eXBlIFdpbmRvd0V2ZW50ID1cbi8vICAgICB8IHR5cGVvZiBXSU5ET1dfUkVTSVpFXG4vLyAgICAgfCB0eXBlb2YgV0lORE9XX01PVkVcbi8vICAgICB8IHR5cGVvZiBXSU5ET1dfRlVMTFNDUkVFTjtcbiIsImltcG9ydCBSZWFjdCwge3VzZUVmZmVjdH0gZnJvbSAncmVhY3QnO1xuaW1wb3J0IHtEYXp6bGVyUHJvcHN9IGZyb20gJy4uLy4uLy4uL2NvbW1vbnMvanMvdHlwZXMnO1xuaW1wb3J0IHtpcGNSZW5kZXJlcn0gZnJvbSAnZWxlY3Ryb24nO1xuaW1wb3J0IHtcbiAgICBXSU5ET1dfUkVTSVpFLFxuICAgIFdJTkRPV19NT1ZFLFxuICAgIFdJTkRPV19GVUxMU0NSRUVOLFxuICAgIFdJTkRPV19TVEFURV9JTklULFxufSBmcm9tICcuLi8uLi9jb21tb24vaXBjRXZlbnRzJztcbmltcG9ydCB7V2luZG93U2l6ZSwgV2luZG93U3RhdHVzfSBmcm9tICcuLi8uLi9jb21tb24vdHlwZXMnO1xuXG50eXBlIFdpbmRvd1N0YXRlUHJvcHMgPSBXaW5kb3dTdGF0dXMgJiB7fSAmIERhenpsZXJQcm9wcztcblxuY29uc3QgV2luZG93U3RhdGUgPSAocHJvcHM6IFdpbmRvd1N0YXRlUHJvcHMpID0+IHtcbiAgICBjb25zdCB7dXBkYXRlQXNwZWN0c30gPSBwcm9wcztcblxuICAgIHVzZUVmZmVjdCgoKSA9PiB7XG4gICAgICAgIGlwY1JlbmRlcmVyLm9uKFdJTkRPV19SRVNJWkUsIChldmVudCwgZGF0YSkgPT4ge1xuICAgICAgICAgICAgY29uc3Qgc2l6ZTogV2luZG93U2l6ZSA9IGRhdGE7XG4gICAgICAgICAgICB1cGRhdGVBc3BlY3RzKHsuLi5zaXplfSk7XG4gICAgICAgIH0pO1xuICAgICAgICBpcGNSZW5kZXJlci5vbihXSU5ET1dfTU9WRSwgKGV2ZW50LCBkYXRhKSA9PiB7XG4gICAgICAgICAgICB1cGRhdGVBc3BlY3RzKHsuLi5kYXRhfSk7XG4gICAgICAgIH0pO1xuICAgICAgICBpcGNSZW5kZXJlci5vbihXSU5ET1dfRlVMTFNDUkVFTiwgKGV2ZW50LCBkYXRhKSA9PiB7XG4gICAgICAgICAgICB1cGRhdGVBc3BlY3RzKHsuLi5kYXRhfSk7XG4gICAgICAgIH0pO1xuICAgICAgICBpcGNSZW5kZXJlclxuICAgICAgICAgICAgLmludm9rZShXSU5ET1dfU1RBVEVfSU5JVClcbiAgICAgICAgICAgIC50aGVuKChpbml0aWFsKSA9PiB1cGRhdGVBc3BlY3RzKHsuLi5pbml0aWFsfSkpO1xuICAgIH0sIFtdKTtcblxuICAgIHJldHVybiA8ZGl2PldpbmRvd1N0YXRlZTwvZGl2Pjtcbn07XG5cbmV4cG9ydCBkZWZhdWx0IFdpbmRvd1N0YXRlO1xuIiwiaW1wb3J0IFdpbmRvd1N0YXRlIGZyb20gJy4vY29tcG9uZW50cy9XaW5kb3dTdGF0ZSc7XG5cbmV4cG9ydCB7XG4gICAgV2luZG93U3RhdGUsXG59XG4iLCJtb2R1bGUuZXhwb3J0cyA9IHJlcXVpcmUoXCJlbGVjdHJvblwiKTsiLCJtb2R1bGUuZXhwb3J0cyA9IF9fV0VCUEFDS19FWFRFUk5BTF9NT0RVTEVfcmVhY3RfXzsiLCIvLyBUaGUgbW9kdWxlIGNhY2hlXG52YXIgX193ZWJwYWNrX21vZHVsZV9jYWNoZV9fID0ge307XG5cbi8vIFRoZSByZXF1aXJlIGZ1bmN0aW9uXG5mdW5jdGlvbiBfX3dlYnBhY2tfcmVxdWlyZV9fKG1vZHVsZUlkKSB7XG5cdC8vIENoZWNrIGlmIG1vZHVsZSBpcyBpbiBjYWNoZVxuXHR2YXIgY2FjaGVkTW9kdWxlID0gX193ZWJwYWNrX21vZHVsZV9jYWNoZV9fW21vZHVsZUlkXTtcblx0aWYgKGNhY2hlZE1vZHVsZSAhPT0gdW5kZWZpbmVkKSB7XG5cdFx0cmV0dXJuIGNhY2hlZE1vZHVsZS5leHBvcnRzO1xuXHR9XG5cdC8vIENyZWF0ZSBhIG5ldyBtb2R1bGUgKGFuZCBwdXQgaXQgaW50byB0aGUgY2FjaGUpXG5cdHZhciBtb2R1bGUgPSBfX3dlYnBhY2tfbW9kdWxlX2NhY2hlX19bbW9kdWxlSWRdID0ge1xuXHRcdC8vIG5vIG1vZHVsZS5pZCBuZWVkZWRcblx0XHQvLyBubyBtb2R1bGUubG9hZGVkIG5lZWRlZFxuXHRcdGV4cG9ydHM6IHt9XG5cdH07XG5cblx0Ly8gRXhlY3V0ZSB0aGUgbW9kdWxlIGZ1bmN0aW9uXG5cdF9fd2VicGFja19tb2R1bGVzX19bbW9kdWxlSWRdLmNhbGwobW9kdWxlLmV4cG9ydHMsIG1vZHVsZSwgbW9kdWxlLmV4cG9ydHMsIF9fd2VicGFja19yZXF1aXJlX18pO1xuXG5cdC8vIFJldHVybiB0aGUgZXhwb3J0cyBvZiB0aGUgbW9kdWxlXG5cdHJldHVybiBtb2R1bGUuZXhwb3J0cztcbn1cblxuIiwiIiwiLy8gc3RhcnR1cFxuLy8gTG9hZCBlbnRyeSBtb2R1bGUgYW5kIHJldHVybiBleHBvcnRzXG4vLyBUaGlzIGVudHJ5IG1vZHVsZSBpcyByZWZlcmVuY2VkIGJ5IG90aGVyIG1vZHVsZXMgc28gaXQgY2FuJ3QgYmUgaW5saW5lZFxudmFyIF9fd2VicGFja19leHBvcnRzX18gPSBfX3dlYnBhY2tfcmVxdWlyZV9fKFwiLi9zcmMvZWxlY3Ryb24vcmVuZGVyZXIvaW5kZXgudHNcIik7XG4iLCIiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=