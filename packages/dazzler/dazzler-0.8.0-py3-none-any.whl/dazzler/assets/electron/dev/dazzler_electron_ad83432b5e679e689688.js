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
        if (set_width) {
            ipc_1["default"].send(ipcEvents_1.WINDOW_SET_BOUNDS, { width: set_width });
            updateAspects({ width: null });
        }
    }, [set_width, updateAspects]);
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
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiZGF6emxlcl9lbGVjdHJvbl9hZDgzNDMyYjVlNjc5ZTY4OTY4OC5qcyIsIm1hcHBpbmdzIjoiQUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxDQUFDO0FBQ0QsTzs7Ozs7Ozs7Ozs7OztBQ1ZhLHFCQUFhLEdBQUcsZUFBZSxDQUFDO0FBQ2hDLG1CQUFXLEdBQUcsYUFBYSxDQUFDO0FBQzVCLHlCQUFpQixHQUFHLG1CQUFtQixDQUFDO0FBQ3hDLHlCQUFpQixHQUFHLG1CQUFtQixDQUFDO0FBQ3hDLHlCQUFpQixHQUFHLG1CQUFtQixDQUFDO0FBQ3hDLHdCQUFnQixHQUFHLGtCQUFrQixDQUFDO0FBQ3RDLHlCQUFpQixHQUFHLG1CQUFtQixDQUFDO0FBR3JELDRCQUE0QjtBQUM1Qiw2QkFBNkI7QUFDN0IsMkJBQTJCO0FBQzNCLGtDQUFrQzs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7O0FDWmxDLHdEQUFnQztBQUVoQywwR0FNZ0M7QUFFaEMsaUdBQXlCO0FBT3pCLElBQU0sV0FBVyxHQUFHLFVBQUMsS0FBdUI7SUFDakMsaUJBQWEsR0FBMEMsS0FBSyxjQUEvQyxFQUFFLFVBQVUsR0FBOEIsS0FBSyxXQUFuQyxFQUFFLE1BQU0sR0FBc0IsS0FBSyxPQUEzQixFQUFFLFNBQVMsR0FBVyxLQUFLLFVBQWhCLEVBQUUsS0FBSyxHQUFJLEtBQUssTUFBVCxDQUFVO0lBRXBFLGlCQUFTLENBQUM7UUFDTixnQkFBRyxDQUFDLEVBQUUsQ0FBQyx5QkFBYSxFQUFFLFVBQUMsS0FBSyxFQUFFLElBQUk7WUFDOUIsSUFBTSxJQUFJLEdBQWUsSUFBSSxDQUFDO1lBQzlCLGFBQWEsY0FBSyxJQUFJLEVBQUUsQ0FBQztRQUM3QixDQUFDLENBQUMsQ0FBQztRQUNILGFBQWE7UUFDYixnQkFBRyxDQUFDLEVBQUUsQ0FBQyx1QkFBVyxFQUFFLFVBQUMsS0FBSyxFQUFFLElBQUk7WUFDNUIsYUFBYSxjQUFLLElBQUksRUFBRSxDQUFDO1FBQzdCLENBQUMsQ0FBQyxDQUFDO1FBQ0gsYUFBYTtRQUNiLGdCQUFHLENBQUMsRUFBRSxDQUFDLDZCQUFpQixFQUFFLFVBQUMsS0FBSyxFQUFFLElBQUk7WUFDbEMsYUFBYSxjQUFLLElBQUksRUFBRSxDQUFDO1FBQzdCLENBQUMsQ0FBQyxDQUFDO1FBQ0gsYUFBYTtRQUNiLGdCQUFHLENBQUMsTUFBTSxDQUFlLDZCQUFpQixDQUFDLENBQUMsSUFBSSxDQUFDLFVBQUMsT0FBTztZQUNyRCxvQkFBYSxjQUFLLE9BQU8sRUFBRTtRQUEzQixDQUEyQixDQUM5QixDQUFDO0lBQ04sQ0FBQyxFQUFFLEVBQUUsQ0FBQyxDQUFDO0lBRVAsaUJBQVMsQ0FBQztRQUNOLElBQUksU0FBUyxFQUFFO1lBQ1gsZ0JBQUcsQ0FBQyxJQUFJLENBQUMsNkJBQWlCLEVBQUUsRUFBQyxLQUFLLEVBQUUsU0FBUyxFQUFDLENBQUMsQ0FBQztZQUNoRCxhQUFhLENBQUMsRUFBQyxLQUFLLEVBQUUsSUFBSSxFQUFDLENBQUMsQ0FBQztTQUNoQztJQUNMLENBQUMsRUFBRSxDQUFDLFNBQVMsRUFBRSxhQUFhLENBQUMsQ0FBQyxDQUFDO0lBRS9CLGlCQUFTLENBQUM7UUFDTixJQUFJLFVBQVUsSUFBSSxVQUFVLEtBQUssTUFBTSxFQUFFO1lBQ3JDLGdCQUFHLENBQUMsSUFBSSxDQUFDLDZCQUFpQixFQUFFLEVBQUMsTUFBTSxFQUFFLFVBQVUsRUFBQyxDQUFDLENBQUM7WUFDbEQsYUFBYSxDQUFDLEVBQUMsTUFBTSxFQUFFLElBQUksRUFBQyxDQUFDLENBQUM7U0FDakM7SUFDTCxDQUFDLEVBQUUsQ0FBQyxVQUFVLEVBQUUsTUFBTSxFQUFFLGFBQWEsQ0FBQyxDQUFDLENBQUM7SUFFeEMsT0FBTyxJQUFJLENBQUM7QUFDaEIsQ0FBQyxDQUFDO0FBRUYsa0JBQWUsV0FBVyxDQUFDOzs7Ozs7Ozs7Ozs7Ozs7OztBQ3hEM0IsK0lBQW1EO0FBRy9DLHNCQUhHLHdCQUFXLENBR0g7Ozs7Ozs7Ozs7Ozs7QUNHZixhQUFhO0FBQ2IsSUFBTSxHQUFHLEdBQVMsTUFBTSxDQUFDLEdBQUcsQ0FBQztBQUU3QixrQkFBZSxHQUFHLENBQUM7Ozs7Ozs7Ozs7O0FDVG5COzs7Ozs7VUNBQTtVQUNBOztVQUVBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTtVQUNBO1VBQ0E7VUFDQTtVQUNBOztVQUVBO1VBQ0E7O1VBRUE7VUFDQTtVQUNBOzs7O1VFdEJBO1VBQ0E7VUFDQTtVQUNBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vLy93ZWJwYWNrL3VuaXZlcnNhbE1vZHVsZURlZmluaXRpb24/Iiwid2VicGFjazovLy8vLi9zcmMvZWxlY3Ryb24vY29tbW9uL2lwY0V2ZW50cy50cz8iLCJ3ZWJwYWNrOi8vLy8uL3NyYy9lbGVjdHJvbi9yZW5kZXJlci9jb21wb25lbnRzL1dpbmRvd1N0YXRlLnRzeD8iLCJ3ZWJwYWNrOi8vLy8uL3NyYy9lbGVjdHJvbi9yZW5kZXJlci9pbmRleC50cz8iLCJ3ZWJwYWNrOi8vLy8uL3NyYy9lbGVjdHJvbi9yZW5kZXJlci9pcGMudHM/Iiwid2VicGFjazovLy8vZXh0ZXJuYWwge1wiY29tbW9uanNcIjpcInJlYWN0XCIsXCJjb21tb25qczJcIjpcInJlYWN0XCIsXCJhbWRcIjpcInJlYWN0XCIsXCJ1bWRcIjpcInJlYWN0XCIsXCJyb290XCI6XCJSZWFjdFwifT8iLCJ3ZWJwYWNrOi8vLy93ZWJwYWNrL2Jvb3RzdHJhcD8iLCJ3ZWJwYWNrOi8vLy93ZWJwYWNrL2JlZm9yZS1zdGFydHVwPyIsIndlYnBhY2s6Ly8vL3dlYnBhY2svc3RhcnR1cD8iLCJ3ZWJwYWNrOi8vLy93ZWJwYWNrL2FmdGVyLXN0YXJ0dXA/Il0sInNvdXJjZXNDb250ZW50IjpbIihmdW5jdGlvbiB3ZWJwYWNrVW5pdmVyc2FsTW9kdWxlRGVmaW5pdGlvbihyb290LCBmYWN0b3J5KSB7XG5cdGlmKHR5cGVvZiBleHBvcnRzID09PSAnb2JqZWN0JyAmJiB0eXBlb2YgbW9kdWxlID09PSAnb2JqZWN0Jylcblx0XHRtb2R1bGUuZXhwb3J0cyA9IGZhY3RvcnkocmVxdWlyZShcInJlYWN0XCIpKTtcblx0ZWxzZSBpZih0eXBlb2YgZGVmaW5lID09PSAnZnVuY3Rpb24nICYmIGRlZmluZS5hbWQpXG5cdFx0ZGVmaW5lKFtcInJlYWN0XCJdLCBmYWN0b3J5KTtcblx0ZWxzZSBpZih0eXBlb2YgZXhwb3J0cyA9PT0gJ29iamVjdCcpXG5cdFx0ZXhwb3J0c1tcImRhenpsZXJfZWxlY3Ryb25cIl0gPSBmYWN0b3J5KHJlcXVpcmUoXCJyZWFjdFwiKSk7XG5cdGVsc2Vcblx0XHRyb290W1wiZGF6emxlcl9lbGVjdHJvblwiXSA9IGZhY3Rvcnkocm9vdFtcIlJlYWN0XCJdKTtcbn0pKHNlbGYsIGZ1bmN0aW9uKF9fV0VCUEFDS19FWFRFUk5BTF9NT0RVTEVfcmVhY3RfXykge1xucmV0dXJuICIsImV4cG9ydCBjb25zdCBXSU5ET1dfUkVTSVpFID0gJ1dJTkRPV19SRVNJWkUnO1xuZXhwb3J0IGNvbnN0IFdJTkRPV19NT1ZFID0gJ1dJTkRPV19NT1ZFJztcbmV4cG9ydCBjb25zdCBXSU5ET1dfRlVMTFNDUkVFTiA9ICdXSU5ET1dfRlVMTFNDUkVFTic7XG5leHBvcnQgY29uc3QgV0lORE9XX1NUQVRFX0lOSVQgPSAnV0lORE9XX1NUQVRFX0lOSVQnO1xuZXhwb3J0IGNvbnN0IFdJTkRPV19TRVRfQk9VTkRTID0gJ1dJTkRPV19TRVRfQk9VTkRTJztcbmV4cG9ydCBjb25zdCBXSU5ET1dfU0VUX1dJRFRIID0gJ1dJTkRPV19TRVRfV0lEVEgnO1xuZXhwb3J0IGNvbnN0IFdJTkRPV19TRVRfSEVJR0hUID0gJ1dJTkRPV19TRVRfSEVJR0hUJztcblxuXG4vLyBleHBvcnQgdHlwZSBXaW5kb3dFdmVudCA9XG4vLyAgICAgfCB0eXBlb2YgV0lORE9XX1JFU0laRVxuLy8gICAgIHwgdHlwZW9mIFdJTkRPV19NT1ZFXG4vLyAgICAgfCB0eXBlb2YgV0lORE9XX0ZVTExTQ1JFRU47XG4iLCJpbXBvcnQge3VzZUVmZmVjdH0gZnJvbSAncmVhY3QnO1xuaW1wb3J0IHtEYXp6bGVyUHJvcHN9IGZyb20gJy4uLy4uLy4uL2NvbW1vbnMvanMvdHlwZXMnO1xuaW1wb3J0IHtcbiAgICBXSU5ET1dfUkVTSVpFLFxuICAgIFdJTkRPV19NT1ZFLFxuICAgIFdJTkRPV19GVUxMU0NSRUVOLFxuICAgIFdJTkRPV19TVEFURV9JTklULFxuICAgIFdJTkRPV19TRVRfQk9VTkRTLFxufSBmcm9tICcuLi8uLi9jb21tb24vaXBjRXZlbnRzJztcbmltcG9ydCB7V2luZG93U2l6ZSwgV2luZG93U3RhdHVzfSBmcm9tICcuLi8uLi9jb21tb24vdHlwZXMnO1xuaW1wb3J0IGlwYyBmcm9tICcuLi9pcGMnO1xuXG50eXBlIFdpbmRvd1N0YXRlUHJvcHMgPSBXaW5kb3dTdGF0dXMgJiB7XG4gICAgc2V0X3dpZHRoPzogbnVtYmVyO1xuICAgIHNldF9oZWlnaHQ/OiBudW1iZXI7XG59ICYgRGF6emxlclByb3BzO1xuXG5jb25zdCBXaW5kb3dTdGF0ZSA9IChwcm9wczogV2luZG93U3RhdGVQcm9wcykgPT4ge1xuICAgIGNvbnN0IHt1cGRhdGVBc3BlY3RzLCBzZXRfaGVpZ2h0LCBoZWlnaHQsIHNldF93aWR0aCwgd2lkdGh9ID0gcHJvcHM7XG5cbiAgICB1c2VFZmZlY3QoKCkgPT4ge1xuICAgICAgICBpcGMub24oV0lORE9XX1JFU0laRSwgKGV2ZW50LCBkYXRhKSA9PiB7XG4gICAgICAgICAgICBjb25zdCBzaXplOiBXaW5kb3dTaXplID0gZGF0YTtcbiAgICAgICAgICAgIHVwZGF0ZUFzcGVjdHMoey4uLnNpemV9KTtcbiAgICAgICAgfSk7XG4gICAgICAgIC8vIEB0cy1pZ25vcmVcbiAgICAgICAgaXBjLm9uKFdJTkRPV19NT1ZFLCAoZXZlbnQsIGRhdGEpID0+IHtcbiAgICAgICAgICAgIHVwZGF0ZUFzcGVjdHMoey4uLmRhdGF9KTtcbiAgICAgICAgfSk7XG4gICAgICAgIC8vIEB0cy1pZ25vcmVcbiAgICAgICAgaXBjLm9uKFdJTkRPV19GVUxMU0NSRUVOLCAoZXZlbnQsIGRhdGEpID0+IHtcbiAgICAgICAgICAgIHVwZGF0ZUFzcGVjdHMoey4uLmRhdGF9KTtcbiAgICAgICAgfSk7XG4gICAgICAgIC8vIEB0cy1pZ25vcmVcbiAgICAgICAgaXBjLmludm9rZTxXaW5kb3dTdGF0dXM+KFdJTkRPV19TVEFURV9JTklUKS50aGVuKChpbml0aWFsKSA9PlxuICAgICAgICAgICAgdXBkYXRlQXNwZWN0cyh7Li4uaW5pdGlhbH0pXG4gICAgICAgICk7XG4gICAgfSwgW10pO1xuXG4gICAgdXNlRWZmZWN0KCgpID0+IHtcbiAgICAgICAgaWYgKHNldF93aWR0aCkge1xuICAgICAgICAgICAgaXBjLnNlbmQoV0lORE9XX1NFVF9CT1VORFMsIHt3aWR0aDogc2V0X3dpZHRofSk7XG4gICAgICAgICAgICB1cGRhdGVBc3BlY3RzKHt3aWR0aDogbnVsbH0pO1xuICAgICAgICB9XG4gICAgfSwgW3NldF93aWR0aCwgdXBkYXRlQXNwZWN0c10pO1xuXG4gICAgdXNlRWZmZWN0KCgpID0+IHtcbiAgICAgICAgaWYgKHNldF9oZWlnaHQgJiYgc2V0X2hlaWdodCAhPT0gaGVpZ2h0KSB7XG4gICAgICAgICAgICBpcGMuc2VuZChXSU5ET1dfU0VUX0JPVU5EUywge2hlaWdodDogc2V0X2hlaWdodH0pO1xuICAgICAgICAgICAgdXBkYXRlQXNwZWN0cyh7aGVpZ2h0OiBudWxsfSk7XG4gICAgICAgIH1cbiAgICB9LCBbc2V0X2hlaWdodCwgaGVpZ2h0LCB1cGRhdGVBc3BlY3RzXSk7XG5cbiAgICByZXR1cm4gbnVsbDtcbn07XG5cbmV4cG9ydCBkZWZhdWx0IFdpbmRvd1N0YXRlO1xuIiwiaW1wb3J0IFdpbmRvd1N0YXRlIGZyb20gJy4vY29tcG9uZW50cy9XaW5kb3dTdGF0ZSc7XG5cbmV4cG9ydCB7XG4gICAgV2luZG93U3RhdGUsXG59XG4iLCJ0eXBlIElwYyA9IHtcbiAgICBvbjogKGs6IHN0cmluZywgaGFuZGxlcjogYW55KSA9PiB2b2lkO1xuICAgIGludm9rZTogPFQ+KGs6IHN0cmluZykgPT4gUHJvbWlzZTxUPjtcbiAgICBzZW5kOiAoazogc3RyaW5nLCBwYXlsb2FkPzogYW55KSA9PiB2b2lkO1xufVxuXG4vLyBAdHMtaWdub3JlXG5jb25zdCBpcGM6IElwYyAgPSB3aW5kb3cuaXBjO1xuXG5leHBvcnQgZGVmYXVsdCBpcGM7XG4iLCJtb2R1bGUuZXhwb3J0cyA9IF9fV0VCUEFDS19FWFRFUk5BTF9NT0RVTEVfcmVhY3RfXzsiLCIvLyBUaGUgbW9kdWxlIGNhY2hlXG52YXIgX193ZWJwYWNrX21vZHVsZV9jYWNoZV9fID0ge307XG5cbi8vIFRoZSByZXF1aXJlIGZ1bmN0aW9uXG5mdW5jdGlvbiBfX3dlYnBhY2tfcmVxdWlyZV9fKG1vZHVsZUlkKSB7XG5cdC8vIENoZWNrIGlmIG1vZHVsZSBpcyBpbiBjYWNoZVxuXHR2YXIgY2FjaGVkTW9kdWxlID0gX193ZWJwYWNrX21vZHVsZV9jYWNoZV9fW21vZHVsZUlkXTtcblx0aWYgKGNhY2hlZE1vZHVsZSAhPT0gdW5kZWZpbmVkKSB7XG5cdFx0cmV0dXJuIGNhY2hlZE1vZHVsZS5leHBvcnRzO1xuXHR9XG5cdC8vIENyZWF0ZSBhIG5ldyBtb2R1bGUgKGFuZCBwdXQgaXQgaW50byB0aGUgY2FjaGUpXG5cdHZhciBtb2R1bGUgPSBfX3dlYnBhY2tfbW9kdWxlX2NhY2hlX19bbW9kdWxlSWRdID0ge1xuXHRcdC8vIG5vIG1vZHVsZS5pZCBuZWVkZWRcblx0XHQvLyBubyBtb2R1bGUubG9hZGVkIG5lZWRlZFxuXHRcdGV4cG9ydHM6IHt9XG5cdH07XG5cblx0Ly8gRXhlY3V0ZSB0aGUgbW9kdWxlIGZ1bmN0aW9uXG5cdF9fd2VicGFja19tb2R1bGVzX19bbW9kdWxlSWRdLmNhbGwobW9kdWxlLmV4cG9ydHMsIG1vZHVsZSwgbW9kdWxlLmV4cG9ydHMsIF9fd2VicGFja19yZXF1aXJlX18pO1xuXG5cdC8vIFJldHVybiB0aGUgZXhwb3J0cyBvZiB0aGUgbW9kdWxlXG5cdHJldHVybiBtb2R1bGUuZXhwb3J0cztcbn1cblxuIiwiIiwiLy8gc3RhcnR1cFxuLy8gTG9hZCBlbnRyeSBtb2R1bGUgYW5kIHJldHVybiBleHBvcnRzXG4vLyBUaGlzIGVudHJ5IG1vZHVsZSBpcyByZWZlcmVuY2VkIGJ5IG90aGVyIG1vZHVsZXMgc28gaXQgY2FuJ3QgYmUgaW5saW5lZFxudmFyIF9fd2VicGFja19leHBvcnRzX18gPSBfX3dlYnBhY2tfcmVxdWlyZV9fKFwiLi9zcmMvZWxlY3Ryb24vcmVuZGVyZXIvaW5kZXgudHNcIik7XG4iLCIiXSwibmFtZXMiOltdLCJzb3VyY2VSb290IjoiIn0=