(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory(require("react"));
	else if(typeof define === 'function' && define.amd)
		define(["react"], factory);
	else if(typeof exports === 'object')
		exports["dazzler_extra"] = factory(require("react"));
	else
		root["dazzler_extra"] = factory(root["React"]);
})(self, function(__WEBPACK_EXTERNAL_MODULE_react__) {
return (self["webpackChunkdazzler_name_"] = self["webpackChunkdazzler_name_"] || []).push([["extra"],{

/***/ "./src/extra/scss/index.scss":
/*!***********************************!*\
  !*** ./src/extra/scss/index.scss ***!
  \***********************************/
/***/ (() => {

// extracted by mini-css-extract-plugin

/***/ }),

/***/ "./node_modules/react-colorful/dist/index.module.js":
/*!**********************************************************!*\
  !*** ./node_modules/react-colorful/dist/index.module.js ***!
  \**********************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "HexColorInput": () => (/* binding */ Me),
/* harmony export */   "HexColorPicker": () => (/* binding */ G),
/* harmony export */   "HslColorPicker": () => (/* binding */ re),
/* harmony export */   "HslStringColorPicker": () => (/* binding */ oe),
/* harmony export */   "HslaColorPicker": () => (/* binding */ V),
/* harmony export */   "HslaStringColorPicker": () => (/* binding */ Z),
/* harmony export */   "HsvColorPicker": () => (/* binding */ ie),
/* harmony export */   "HsvStringColorPicker": () => (/* binding */ fe),
/* harmony export */   "HsvaColorPicker": () => (/* binding */ ae),
/* harmony export */   "HsvaStringColorPicker": () => (/* binding */ ue),
/* harmony export */   "RgbColorPicker": () => (/* binding */ pe),
/* harmony export */   "RgbStringColorPicker": () => (/* binding */ _e),
/* harmony export */   "RgbaColorPicker": () => (/* binding */ de),
/* harmony export */   "RgbaStringColorPicker": () => (/* binding */ me),
/* harmony export */   "setNonce": () => (/* binding */ X)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);
function l(){return(l=Object.assign||function(e){for(var r=1;r<arguments.length;r++){var t=arguments[r];for(var o in t)Object.prototype.hasOwnProperty.call(t,o)&&(e[o]=t[o])}return e}).apply(this,arguments)}function u(e,r){if(null==e)return{};var t,o,n={},a=Object.keys(e);for(o=0;o<a.length;o++)r.indexOf(t=a[o])>=0||(n[t]=e[t]);return n}var c="undefined"!=typeof window?react__WEBPACK_IMPORTED_MODULE_0__.useLayoutEffect:react__WEBPACK_IMPORTED_MODULE_0__.useEffect;function i(e){var r=(0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(e);return (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(function(){r.current=e}),(0,react__WEBPACK_IMPORTED_MODULE_0__.useCallback)(function(e){return r.current&&r.current(e)},[])}var s,f=function(e,r,t){return void 0===r&&(r=0),void 0===t&&(t=1),e>t?t:e<r?r:e},v=function(e){return"touches"in e},d=function(e,r){var t=e.getBoundingClientRect(),o=v(r)?r.touches[0]:r;return{left:f((o.pageX-(t.left+window.pageXOffset))/t.width),top:f((o.pageY-(t.top+window.pageYOffset))/t.height)}},h=function(e){!v(e)&&e.preventDefault()},m=react__WEBPACK_IMPORTED_MODULE_0___default().memo(function(r){var t=r.onMove,s=r.onKey,f=u(r,["onMove","onKey"]),m=(0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(null),g=(0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)(!1),p=(0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(!1),b=p[0],_=p[1],C=i(t),x=i(s),E=(0,react__WEBPACK_IMPORTED_MODULE_0__.useCallback)(function(e){h(e),(v(e)?e.touches.length>0:e.buttons>0)&&m.current?C(d(m.current,e)):_(!1)},[C]),H=(0,react__WEBPACK_IMPORTED_MODULE_0__.useCallback)(function(e){var r,t=e.nativeEvent,o=m.current;h(t),r=t,g.current&&!v(r)||(g.current||(g.current=v(r)),0)||!o||(o.focus(),C(d(o,t)),_(!0))},[C]),M=(0,react__WEBPACK_IMPORTED_MODULE_0__.useCallback)(function(e){var r=e.which||e.keyCode;r<37||r>40||(e.preventDefault(),x({left:39===r?.05:37===r?-.05:0,top:40===r?.05:38===r?-.05:0}))},[x]),N=(0,react__WEBPACK_IMPORTED_MODULE_0__.useCallback)(function(){return _(!1)},[]),w=(0,react__WEBPACK_IMPORTED_MODULE_0__.useCallback)(function(e){var r=e?window.addEventListener:window.removeEventListener;r(g.current?"touchmove":"mousemove",E),r(g.current?"touchend":"mouseup",N)},[E,N]);return c(function(){return w(b),function(){b&&w(!1)}},[b,w]),react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div",l({},f,{className:"react-colorful__interactive",ref:m,onTouchStart:H,onMouseDown:H,onKeyDown:M,tabIndex:0,role:"slider"}))}),g=function(e){return e.filter(Boolean).join(" ")},p=function(r){var t=r.color,o=r.left,n=r.top,a=void 0===n?.5:n,l=g(["react-colorful__pointer",r.className]);return react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div",{className:l,style:{top:100*a+"%",left:100*o+"%"}},react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div",{className:"react-colorful__pointer-fill",style:{backgroundColor:t}}))},b=function(e,r,t){return void 0===r&&(r=0),void 0===t&&(t=Math.pow(10,r)),Math.round(t*e)/t},_={grad:.9,turn:360,rad:360/(2*Math.PI)},C=function(e){return"#"===e[0]&&(e=e.substr(1)),e.length<6?{r:parseInt(e[0]+e[0],16),g:parseInt(e[1]+e[1],16),b:parseInt(e[2]+e[2],16),a:1}:{r:parseInt(e.substr(0,2),16),g:parseInt(e.substr(2,2),16),b:parseInt(e.substr(4,2),16),a:1}},x=function(e,r){return void 0===r&&(r="deg"),Number(e)*(_[r]||1)},E=function(e){var r=/hsla?\(?\s*(-?\d*\.?\d+)(deg|rad|grad|turn)?[,\s]+(-?\d*\.?\d+)%?[,\s]+(-?\d*\.?\d+)%?,?\s*[/\s]*(-?\d*\.?\d+)?(%)?\s*\)?/i.exec(e);return r?M({h:x(r[1],r[2]),s:Number(r[3]),l:Number(r[4]),a:void 0===r[5]?1:Number(r[5])/(r[6]?100:1)}):{h:0,s:0,v:0,a:1}},H=E,M=function(e){var r=e.s,t=e.l;return{h:e.h,s:(r*=(t<50?t:100-t)/100)>0?2*r/(t+r)*100:0,v:t+r,a:e.a}},N=function(e){var r=e.s,t=e.v,o=e.a,n=(200-r)*t/100;return{h:b(e.h),s:b(n>0&&n<200?r*t/100/(n<=100?n:200-n)*100:0),l:b(n/2),a:b(o,2)}},w=function(e){var r=N(e);return"hsl("+r.h+", "+r.s+"%, "+r.l+"%)"},y=function(e){var r=N(e);return"hsla("+r.h+", "+r.s+"%, "+r.l+"%, "+r.a+")"},q=function(e){var r=e.h,t=e.s,o=e.v,n=e.a;r=r/360*6,t/=100,o/=100;var a=Math.floor(r),l=o*(1-t),u=o*(1-(r-a)*t),c=o*(1-(1-r+a)*t),i=a%6;return{r:b(255*[o,u,l,l,c,o][i]),g:b(255*[c,o,o,u,l,l][i]),b:b(255*[l,l,c,o,o,u][i]),a:b(n,2)}},k=function(e){var r=/hsva?\(?\s*(-?\d*\.?\d+)(deg|rad|grad|turn)?[,\s]+(-?\d*\.?\d+)%?[,\s]+(-?\d*\.?\d+)%?,?\s*[/\s]*(-?\d*\.?\d+)?(%)?\s*\)?/i.exec(e);return r?K({h:x(r[1],r[2]),s:Number(r[3]),v:Number(r[4]),a:void 0===r[5]?1:Number(r[5])/(r[6]?100:1)}):{h:0,s:0,v:0,a:1}},O=k,I=function(e){var r=/rgba?\(?\s*(-?\d*\.?\d+)(%)?[,\s]+(-?\d*\.?\d+)(%)?[,\s]+(-?\d*\.?\d+)(%)?,?\s*[/\s]*(-?\d*\.?\d+)?(%)?\s*\)?/i.exec(e);return r?B({r:Number(r[1])/(r[2]?100/255:1),g:Number(r[3])/(r[4]?100/255:1),b:Number(r[5])/(r[6]?100/255:1),a:void 0===r[7]?1:Number(r[7])/(r[8]?100:1)}):{h:0,s:0,v:0,a:1}},j=I,z=function(e){var r=e.toString(16);return r.length<2?"0"+r:r},B=function(e){var r=e.r,t=e.g,o=e.b,n=e.a,a=Math.max(r,t,o),l=a-Math.min(r,t,o),u=l?a===r?(t-o)/l:a===t?2+(o-r)/l:4+(r-t)/l:0;return{h:b(60*(u<0?u+6:u)),s:b(a?l/a*100:0),v:b(a/255*100),a:n}},K=function(e){return{h:b(e.h),s:b(e.s),v:b(e.v),a:b(e.a,2)}},A=react__WEBPACK_IMPORTED_MODULE_0___default().memo(function(r){var t=r.hue,o=r.onChange,n=g(["react-colorful__hue",r.className]);return react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div",{className:n},react__WEBPACK_IMPORTED_MODULE_0___default().createElement(m,{onMove:function(e){o({h:360*e.left})},onKey:function(e){o({h:f(t+360*e.left,0,360)})},"aria-label":"Hue","aria-valuetext":b(t)},react__WEBPACK_IMPORTED_MODULE_0___default().createElement(p,{className:"react-colorful__hue-pointer",left:t/360,color:w({h:t,s:100,v:100,a:1})})))}),L=react__WEBPACK_IMPORTED_MODULE_0___default().memo(function(r){var t=r.hsva,o=r.onChange,n={backgroundColor:w({h:t.h,s:100,v:100,a:1})};return react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div",{className:"react-colorful__saturation",style:n},react__WEBPACK_IMPORTED_MODULE_0___default().createElement(m,{onMove:function(e){o({s:100*e.left,v:100-100*e.top})},onKey:function(e){o({s:f(t.s+100*e.left,0,100),v:f(t.v-100*e.top,0,100)})},"aria-label":"Color","aria-valuetext":"Saturation "+b(t.s)+"%, Brightness "+b(t.v)+"%"},react__WEBPACK_IMPORTED_MODULE_0___default().createElement(p,{className:"react-colorful__saturation-pointer",top:1-t.v/100,left:t.s/100,color:w(t)})))}),D=function(e,r){if(e===r)return!0;for(var t in e)if(e[t]!==r[t])return!1;return!0},F=function(e,r){return e.replace(/\s/g,"")===r.replace(/\s/g,"")};function S(e,r,l){var u=i(l),c=(0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(function(){return e.toHsva(r)}),s=c[0],f=c[1],v=(0,react__WEBPACK_IMPORTED_MODULE_0__.useRef)({color:r,hsva:s});(0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(function(){if(!e.equal(r,v.current.color)){var t=e.toHsva(r);v.current={hsva:t,color:r},f(t)}},[r,e]),(0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(function(){var r;D(s,v.current.hsva)||e.equal(r=e.fromHsva(s),v.current.color)||(v.current={hsva:s,color:r},u(r))},[s,e,u]);var d=(0,react__WEBPACK_IMPORTED_MODULE_0__.useCallback)(function(e){f(function(r){return Object.assign({},r,e)})},[]);return[s,d]}var P,T=function(){return s||( true?__webpack_require__.nc:0)},X=function(e){s=e},Y=function(){c(function(){if("undefined"!=typeof document&&!P){(P=document.createElement("style")).innerHTML='.react-colorful{position:relative;display:flex;flex-direction:column;width:200px;height:200px;-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none;cursor:default}.react-colorful__saturation{position:relative;flex-grow:1;border-color:transparent;border-bottom:12px solid #000;border-radius:8px 8px 0 0;background-image:linear-gradient(0deg,#000,transparent),linear-gradient(90deg,#fff,hsla(0,0%,100%,0))}.react-colorful__alpha-gradient,.react-colorful__pointer-fill{content:"";position:absolute;left:0;top:0;right:0;bottom:0;pointer-events:none;border-radius:inherit}.react-colorful__alpha-gradient,.react-colorful__saturation{box-shadow:inset 0 0 0 1px rgba(0,0,0,.05)}.react-colorful__alpha,.react-colorful__hue{position:relative;height:24px}.react-colorful__hue{background:linear-gradient(90deg,red 0,#ff0 17%,#0f0 33%,#0ff 50%,#00f 67%,#f0f 83%,red)}.react-colorful__last-control{border-radius:0 0 8px 8px}.react-colorful__interactive{position:absolute;left:0;top:0;right:0;bottom:0;border-radius:inherit;outline:none;touch-action:none}.react-colorful__pointer{position:absolute;z-index:1;box-sizing:border-box;width:28px;height:28px;transform:translate(-50%,-50%);background-color:#fff;border:2px solid #fff;border-radius:50%;box-shadow:0 2px 4px rgba(0,0,0,.2)}.react-colorful__interactive:focus .react-colorful__pointer{transform:translate(-50%,-50%) scale(1.1)}.react-colorful__alpha,.react-colorful__alpha-pointer{background-color:#fff;background-image:url(\'data:image/svg+xml;charset=utf-8,<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill-opacity=".05"><path d="M8 0h8v8H8zM0 8h8v8H0z"/></svg>\')}.react-colorful__saturation-pointer{z-index:3}.react-colorful__hue-pointer{z-index:2}';var e=T();e&&P.setAttribute("nonce",e),document.head.appendChild(P)}},[])},$=function(r){var t=r.className,o=r.colorModel,n=r.color,a=void 0===n?o.defaultColor:n,c=r.onChange,i=u(r,["className","colorModel","color","onChange"]);Y();var s=S(o,a,c),f=s[0],v=s[1],d=g(["react-colorful",t]);return react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div",l({},i,{className:d}),react__WEBPACK_IMPORTED_MODULE_0___default().createElement(L,{hsva:f,onChange:v}),react__WEBPACK_IMPORTED_MODULE_0___default().createElement(A,{hue:f.h,onChange:v,className:"react-colorful__last-control"}))},R={defaultColor:"000",toHsva:function(e){return B(C(e))},fromHsva:function(e){return t=(r=q(e)).g,o=r.b,"#"+z(r.r)+z(t)+z(o);var r,t,o},equal:function(e,r){return e.toLowerCase()===r.toLowerCase()||D(C(e),C(r))}},G=function(r){return react__WEBPACK_IMPORTED_MODULE_0___default().createElement($,l({},r,{colorModel:R}))},J=function(r){var t=r.className,o=r.hsva,n=r.onChange,a={backgroundImage:"linear-gradient(90deg, "+y(Object.assign({},o,{a:0}))+", "+y(Object.assign({},o,{a:1}))+")"},l=g(["react-colorful__alpha",t]);return react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div",{className:l},react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div",{className:"react-colorful__alpha-gradient",style:a}),react__WEBPACK_IMPORTED_MODULE_0___default().createElement(m,{onMove:function(e){n({a:e.left})},onKey:function(e){n({a:f(o.a+e.left)})},"aria-label":"Alpha","aria-valuetext":b(100*o.a)+"%"},react__WEBPACK_IMPORTED_MODULE_0___default().createElement(p,{className:"react-colorful__alpha-pointer",left:o.a,color:y(o)})))},Q=function(r){var t=r.className,o=r.colorModel,n=r.color,a=void 0===n?o.defaultColor:n,c=r.onChange,i=u(r,["className","colorModel","color","onChange"]);Y();var s=S(o,a,c),f=s[0],v=s[1],d=g(["react-colorful",t]);return react__WEBPACK_IMPORTED_MODULE_0___default().createElement("div",l({},i,{className:d}),react__WEBPACK_IMPORTED_MODULE_0___default().createElement(L,{hsva:f,onChange:v}),react__WEBPACK_IMPORTED_MODULE_0___default().createElement(A,{hue:f.h,onChange:v}),react__WEBPACK_IMPORTED_MODULE_0___default().createElement(J,{hsva:f,onChange:v,className:"react-colorful__last-control"}))},U={defaultColor:{h:0,s:0,l:0,a:1},toHsva:M,fromHsva:N,equal:D},V=function(r){return react__WEBPACK_IMPORTED_MODULE_0___default().createElement(Q,l({},r,{colorModel:U}))},W={defaultColor:"hsla(0, 0%, 0%, 1)",toHsva:E,fromHsva:y,equal:F},Z=function(r){return react__WEBPACK_IMPORTED_MODULE_0___default().createElement(Q,l({},r,{colorModel:W}))},ee={defaultColor:{h:0,s:0,l:0},toHsva:function(e){return M({h:e.h,s:e.s,l:e.l,a:1})},fromHsva:function(e){return{h:(r=N(e)).h,s:r.s,l:r.l};var r},equal:D},re=function(r){return react__WEBPACK_IMPORTED_MODULE_0___default().createElement($,l({},r,{colorModel:ee}))},te={defaultColor:"hsl(0, 0%, 0%)",toHsva:H,fromHsva:w,equal:F},oe=function(r){return react__WEBPACK_IMPORTED_MODULE_0___default().createElement($,l({},r,{colorModel:te}))},ne={defaultColor:{h:0,s:0,v:0,a:1},toHsva:function(e){return e},fromHsva:K,equal:D},ae=function(r){return react__WEBPACK_IMPORTED_MODULE_0___default().createElement(Q,l({},r,{colorModel:ne}))},le={defaultColor:"hsva(0, 0%, 0%, 1)",toHsva:k,fromHsva:function(e){var r=K(e);return"hsva("+r.h+", "+r.s+"%, "+r.v+"%, "+r.a+")"},equal:F},ue=function(r){return react__WEBPACK_IMPORTED_MODULE_0___default().createElement(Q,l({},r,{colorModel:le}))},ce={defaultColor:{h:0,s:0,v:0},toHsva:function(e){return{h:e.h,s:e.s,v:e.v,a:1}},fromHsva:function(e){var r=K(e);return{h:r.h,s:r.s,v:r.v}},equal:D},ie=function(r){return react__WEBPACK_IMPORTED_MODULE_0___default().createElement($,l({},r,{colorModel:ce}))},se={defaultColor:"hsv(0, 0%, 0%)",toHsva:O,fromHsva:function(e){var r=K(e);return"hsv("+r.h+", "+r.s+"%, "+r.v+"%)"},equal:F},fe=function(r){return react__WEBPACK_IMPORTED_MODULE_0___default().createElement($,l({},r,{colorModel:se}))},ve={defaultColor:{r:0,g:0,b:0,a:1},toHsva:B,fromHsva:q,equal:D},de=function(r){return react__WEBPACK_IMPORTED_MODULE_0___default().createElement(Q,l({},r,{colorModel:ve}))},he={defaultColor:"rgba(0, 0, 0, 1)",toHsva:I,fromHsva:function(e){var r=q(e);return"rgba("+r.r+", "+r.g+", "+r.b+", "+r.a+")"},equal:F},me=function(r){return react__WEBPACK_IMPORTED_MODULE_0___default().createElement(Q,l({},r,{colorModel:he}))},ge={defaultColor:{r:0,g:0,b:0},toHsva:function(e){return B({r:e.r,g:e.g,b:e.b,a:1})},fromHsva:function(e){return{r:(r=q(e)).r,g:r.g,b:r.b};var r},equal:D},pe=function(r){return react__WEBPACK_IMPORTED_MODULE_0___default().createElement($,l({},r,{colorModel:ge}))},be={defaultColor:"rgb(0, 0, 0)",toHsva:j,fromHsva:function(e){var r=q(e);return"rgb("+r.r+", "+r.g+", "+r.b+")"},equal:F},_e=function(r){return react__WEBPACK_IMPORTED_MODULE_0___default().createElement($,l({},r,{colorModel:be}))},Ce=/^#?[0-9A-F]{3}$/i,xe=/^#?[0-9A-F]{6}$/i,Ee=function(e){return xe.test(e)||Ce.test(e)},He=function(e){return e.replace(/([^0-9A-F]+)/gi,"").substr(0,6)},Me=function(r){var n=r.color,c=void 0===n?"":n,s=r.onChange,f=r.onBlur,v=r.prefixed,d=u(r,["color","onChange","onBlur","prefixed"]),h=(0,react__WEBPACK_IMPORTED_MODULE_0__.useState)(function(){return He(c)}),m=h[0],g=h[1],p=i(s),b=i(f),_=(0,react__WEBPACK_IMPORTED_MODULE_0__.useCallback)(function(e){var r=He(e.target.value);g(r),Ee(r)&&p("#"+r)},[p]),C=(0,react__WEBPACK_IMPORTED_MODULE_0__.useCallback)(function(e){Ee(e.target.value)||g(He(c)),b(e)},[c,b]);return (0,react__WEBPACK_IMPORTED_MODULE_0__.useEffect)(function(){g(He(c))},[c]),react__WEBPACK_IMPORTED_MODULE_0___default().createElement("input",l({},d,{value:(v?"#":"")+m,spellCheck:"false",onChange:_,onBlur:C}))};
//# sourceMappingURL=index.module.js.map


/***/ }),

/***/ "./src/extra/js/components/ColorPicker.tsx":
/*!*************************************************!*\
  !*** ./src/extra/js/components/ColorPicker.tsx ***!
  \*************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

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
var __rest = (this && this.__rest) || function (s, e) {
    var t = {};
    for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0)
        t[p] = s[p];
    if (s != null && typeof Object.getOwnPropertySymbols === "function")
        for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) {
            if (e.indexOf(p[i]) < 0 && Object.prototype.propertyIsEnumerable.call(s, p[i]))
                t[p[i]] = s[p[i]];
        }
    return t;
};
exports.__esModule = true;
var react_1 = __importStar(__webpack_require__(/*! react */ "react"));
var react_colorful_1 = __webpack_require__(/*! react-colorful */ "./node_modules/react-colorful/dist/index.module.js");
var commons_1 = __webpack_require__(/*! commons */ "./src/commons/js/index.ts");
/**
 * A color picker powered by react-colorful
 *
 * A toggle button is included or can be disabled with ``toggleable=False``
 * and then it be activated by binding, tie or initial value.
 *
 * Common style aspects goes on the container of the picker, hidden by default.
 *
 * :CSS:
 *
 *      - ``dazzler-extra-color-picker`` - Top level container
 *      - ``dazzler-color-picker-toggle`` - Toggle button
 *      - ``dazzler-color-picker`` - Picker container.
 *
 * .. literalinclude:: ../../tests/components/pages/color_picker.py
 */
var ColorPicker = function (props) {
    var identity = props.identity, class_name = props.class_name, style = props.style, type = props.type, toggleable = props.toggleable, toggle_button = props.toggle_button, toggle_on_choose = props.toggle_on_choose, toggle_on_choose_delay = props.toggle_on_choose_delay, toggle_button_color = props.toggle_button_color, toggle_direction = props.toggle_direction, active = props.active, value = props.value, updateAspects = props.updateAspects, as_string = props.as_string, rest = __rest(props, ["identity", "class_name", "style", "type", "toggleable", "toggle_button", "toggle_on_choose", "toggle_on_choose_delay", "toggle_button_color", "toggle_direction", "active", "value", "updateAspects", "as_string"]);
    var css = react_1.useMemo(function () {
        return commons_1.getPresetsClassNames(rest, 'dazzler-color-picker', "toggle-direction-" + toggle_direction);
    }, [rest, active]);
    var className = react_1.useMemo(function () {
        var c = [class_name];
        if (active) {
            c.push('active');
        }
        return c.join(' ');
    }, [class_name, active]);
    var styling = react_1.useMemo(function () { return commons_1.getCommonStyles(rest, style); }, [rest, style]);
    var autoClose = react_1.useCallback(commons_1.throttle(function () { return updateAspects({ active: false }); }, toggle_on_choose_delay, true), []);
    var picker = react_1.useMemo(function () {
        var onChange = function (newColor) {
            var payload = { value: newColor };
            if (toggle_on_choose) {
                autoClose();
            }
            updateAspects(payload);
        };
        switch (type) {
            case 'rgb':
                if (as_string) {
                    return (react_1["default"].createElement(react_colorful_1.RgbStringColorPicker, { onChange: onChange, color: value }));
                }
                return (react_1["default"].createElement(react_colorful_1.RgbColorPicker, { onChange: onChange, color: value }));
            case 'rgba':
                if (as_string) {
                    return (react_1["default"].createElement(react_colorful_1.RgbaStringColorPicker, { onChange: onChange, color: value }));
                }
                return (react_1["default"].createElement(react_colorful_1.RgbaColorPicker, { onChange: onChange, color: value }));
            case 'hsl':
                if (as_string) {
                    return (react_1["default"].createElement(react_colorful_1.HslStringColorPicker, { onChange: onChange, color: value }));
                }
                return (react_1["default"].createElement(react_colorful_1.HslColorPicker, { onChange: onChange, color: value }));
            case 'hsla':
                if (as_string) {
                    return (react_1["default"].createElement(react_colorful_1.HslaStringColorPicker, { onChange: onChange, color: value }));
                }
                return (react_1["default"].createElement(react_colorful_1.HslaColorPicker, { onChange: onChange, color: value }));
            case 'hsv':
                if (as_string) {
                    return (react_1["default"].createElement(react_colorful_1.HsvStringColorPicker, { onChange: onChange, color: value }));
                }
                return (react_1["default"].createElement(react_colorful_1.HsvColorPicker, { onChange: onChange, color: value }));
            case 'hsva':
                if (as_string) {
                    return (react_1["default"].createElement(react_colorful_1.HsvaStringColorPicker, { onChange: onChange, color: value }));
                }
                return (react_1["default"].createElement(react_colorful_1.HsvaColorPicker, { onChange: onChange, color: value }));
            case 'hex':
            default:
                return (react_1["default"].createElement(react_colorful_1.HexColorPicker, { onChange: onChange, color: value }));
        }
    }, [
        type,
        value,
        updateAspects,
        toggle_on_choose,
        toggle_on_choose_delay,
        as_string,
    ]);
    var toggleButton = react_1.useMemo(function () {
        if (toggle_button_color) {
            return (react_1["default"].createElement("div", { className: "toggle-button-color", 
                // @ts-ignore
                style: { backgroundColor: value } }));
        }
        return toggle_button;
    }, [toggle_button, toggle_button_color, value]);
    var onToggle = react_1.useCallback(function () {
        updateAspects({ active: !active });
    }, [active, updateAspects]);
    return (react_1["default"].createElement("div", { id: identity, className: className },
        toggleable && (react_1["default"].createElement("div", { className: "dazzler-color-picker-toggle", onClick: onToggle }, toggleButton)),
        react_1["default"].createElement("div", { className: css, style: styling }, picker)));
};
ColorPicker.defaultProps = {
    type: 'hex',
    toggle_button: '🎨',
    toggleable: true,
    toggle_on_choose: true,
    toggle_on_choose_delay: 2500,
    toggle_direction: 'top-left',
};
exports.default = ColorPicker;


/***/ }),

/***/ "./src/extra/js/components/Drawer.tsx":
/*!********************************************!*\
  !*** ./src/extra/js/components/Drawer.tsx ***!
  \********************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
var react_1 = __importDefault(__webpack_require__(/*! react */ "react"));
var ramda_1 = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
var Caret = function (_a) {
    var side = _a.side, opened = _a.opened;
    switch (side) {
        case 'top':
            return opened ? react_1["default"].createElement("span", null, "\u25B2") : react_1["default"].createElement("span", null, "\u25BC");
        case 'right':
            return opened ? react_1["default"].createElement("span", null, "\u25B8") : react_1["default"].createElement("span", null, "\u25C2");
        case 'left':
            return opened ? react_1["default"].createElement("span", null, "\u25C2") : react_1["default"].createElement("span", null, "\u25B8");
        case 'bottom':
            return opened ? react_1["default"].createElement("span", null, "\u25BC") : react_1["default"].createElement("span", null, "\u25B2");
        default:
            return null;
    }
};
/**
 * Draw content from the sides of the screen.
 *
 * :CSS:
 *
 *     - ``dazzler-extra-drawer``
 *     - ``drawer-content``
 *     - ``drawer-control``
 *     - ``vertical``
 *     - ``horizontal``
 *     - ``right``
 *     - ``bottom``
 */
var Drawer = function (props) {
    var class_name = props.class_name, identity = props.identity, style = props.style, children = props.children, opened = props.opened, side = props.side, updateAspects = props.updateAspects;
    var css = [side];
    if (side === 'top' || side === 'bottom') {
        css.push('horizontal');
    }
    else {
        css.push('vertical');
    }
    return (react_1["default"].createElement("div", { className: ramda_1.join(' ', ramda_1.concat(css, [class_name])), id: identity, style: style },
        opened && (react_1["default"].createElement("div", { className: ramda_1.join(' ', ramda_1.concat(css, ['drawer-content'])) }, children)),
        react_1["default"].createElement("div", { className: ramda_1.join(' ', ramda_1.concat(css, ['drawer-control'])), onClick: function () { return updateAspects({ opened: !opened }); } },
            react_1["default"].createElement(Caret, { opened: opened, side: side }))));
};
Drawer.defaultProps = {
    side: 'top',
};
exports.default = Drawer;


/***/ }),

/***/ "./src/extra/js/components/Notice.tsx":
/*!********************************************!*\
  !*** ./src/extra/js/components/Notice.tsx ***!
  \********************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
var react_1 = __importDefault(__webpack_require__(/*! react */ "react"));
var commons_1 = __webpack_require__(/*! commons */ "./src/commons/js/index.ts");
var ramda_1 = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
/**
 * Browser notifications with permissions handling.
 */
var Notice = /** @class */ (function (_super) {
    __extends(Notice, _super);
    function Notice(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            lastMessage: props.body,
            notification: null,
        };
        _this.onPermission = _this.onPermission.bind(_this);
        return _this;
    }
    Notice.prototype.componentDidMount = function () {
        var updateAspects = this.props.updateAspects;
        if (!('Notification' in window) && updateAspects) {
            updateAspects({ permission: 'unsupported' });
        }
        else if (Notification.permission === 'default') {
            Notification.requestPermission().then(this.onPermission);
        }
        else {
            this.onPermission(window.Notification.permission);
        }
    };
    Notice.prototype.componentDidUpdate = function (prevProps) {
        if (!prevProps.displayed && this.props.displayed) {
            this.sendNotification(this.props.permission);
        }
    };
    Notice.prototype.sendNotification = function (permission) {
        var _this = this;
        var _a = this.props, updateAspects = _a.updateAspects, body = _a.body, title = _a.title, icon = _a.icon, require_interaction = _a.require_interaction, lang = _a.lang, badge = _a.badge, tag = _a.tag, image = _a.image, vibrate = _a.vibrate;
        if (permission === 'granted') {
            var options = {
                requireInteraction: require_interaction,
                body: body,
                icon: icon,
                lang: lang,
                badge: badge,
                tag: tag,
                image: image,
                vibrate: vibrate,
            };
            var notification = new Notification(title, options);
            notification.onclick = function () {
                if (updateAspects) {
                    updateAspects(ramda_1.merge({ displayed: false }, commons_1.timestampProp('clicks', _this.props.clicks + 1)));
                }
            };
            notification.onclose = function () {
                if (updateAspects) {
                    updateAspects(ramda_1.merge({ displayed: false }, commons_1.timestampProp('closes', _this.props.closes + 1)));
                }
            };
        }
    };
    Notice.prototype.onPermission = function (permission) {
        var _a = this.props, displayed = _a.displayed, updateAspects = _a.updateAspects;
        if (updateAspects) {
            updateAspects({ permission: permission });
        }
        if (displayed) {
            this.sendNotification(permission);
        }
    };
    Notice.prototype.render = function () {
        return null;
    };
    return Notice;
}(react_1["default"].Component));
exports.default = Notice;


/***/ }),

/***/ "./src/extra/js/components/PageMap.tsx":
/*!*********************************************!*\
  !*** ./src/extra/js/components/PageMap.tsx ***!
  \*********************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

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
/**
 * List of links to other page in the app.
 *
 * :CSS:
 *
 *     - ``dazzler-extra-page-map``
 */
var PageMap = function (props) {
    var class_name = props.class_name, style = props.style, identity = props.identity;
    var _a = react_1.useState(null), pageMap = _a[0], setPageMap = _a[1];
    react_1.useEffect(function () {
        // @ts-ignore
        fetch(window.dazzler_base_url + "/dazzler/page-map").then(function (rep) {
            return rep.json().then(setPageMap);
        });
    }, []);
    return (react_1["default"].createElement("ul", { className: class_name, style: style, id: identity }, pageMap &&
        pageMap.map(function (page) { return (react_1["default"].createElement("li", { key: page.name },
            react_1["default"].createElement("a", { href: page.url }, page.title))); })));
};
PageMap.defaultProps = {};
exports.default = PageMap;


/***/ }),

/***/ "./src/extra/js/components/Pager.tsx":
/*!*******************************************!*\
  !*** ./src/extra/js/components/Pager.tsx ***!
  \*******************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
var react_1 = __importDefault(__webpack_require__(/*! react */ "react"));
var ramda_1 = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
var startOffset = function (page, itemPerPage) {
    return (page - 1) * (page > 1 ? itemPerPage : 0);
};
var endOffset = function (start, itemPerPage, page, total, leftOver) {
    return page !== total
        ? start + itemPerPage
        : leftOver !== 0
            ? start + leftOver
            : start + itemPerPage;
};
var showList = function (page, total, n) {
    if (total > n) {
        var middle = n / 2;
        var first = page >= total - middle
            ? total - n + 1
            : page > middle
                ? page - middle
                : 1;
        var last = page < total - middle ? first + n : total + 1;
        return ramda_1.range(first, last);
    }
    return ramda_1.range(1, total + 1);
};
var Page = function (_a) {
    var style = _a.style, class_name = _a.class_name, on_change = _a.on_change, text = _a.text, page = _a.page;
    return (react_1["default"].createElement("span", { style: style, className: class_name, onClick: function () { return on_change(page); } }, text || page));
};
/**
 * Paging for dazzler apps.
 *
 * :CSS:
 *
 *     - ``dazzler-extra-pager``
 *     - ``page``
 */
var Pager = /** @class */ (function (_super) {
    __extends(Pager, _super);
    function Pager(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            current_page: null,
            start_offset: null,
            end_offset: null,
            pages: [],
            total_pages: Math.ceil(props.total_items / props.items_per_page),
        };
        _this.onChangePage = _this.onChangePage.bind(_this);
        return _this;
    }
    Pager.prototype.UNSAFE_componentWillMount = function () {
        this.onChangePage(this.props.current_page);
    };
    Pager.prototype.onChangePage = function (page) {
        var _a = this.props, items_per_page = _a.items_per_page, total_items = _a.total_items, updateAspects = _a.updateAspects, pages_displayed = _a.pages_displayed;
        var total_pages = this.state.total_pages;
        var start_offset = startOffset(page, items_per_page);
        var leftOver = total_items % items_per_page;
        var end_offset = endOffset(start_offset, items_per_page, page, total_pages, leftOver);
        var payload = {
            current_page: page,
            start_offset: start_offset,
            end_offset: end_offset,
            pages: showList(page, total_pages, pages_displayed),
        };
        this.setState(payload);
        if (updateAspects) {
            if (this.state.total_pages !== this.props.total_pages) {
                payload.total_pages = this.state.total_pages;
            }
            updateAspects(payload);
        }
    };
    Pager.prototype.UNSAFE_componentWillReceiveProps = function (props) {
        if (props.current_page !== this.state.current_page) {
            this.onChangePage(props.current_page);
        }
    };
    Pager.prototype.render = function () {
        var _this = this;
        var _a = this.state, current_page = _a.current_page, pages = _a.pages, total_pages = _a.total_pages;
        var _b = this.props, class_name = _b.class_name, identity = _b.identity, page_style = _b.page_style, page_class_name = _b.page_class_name;
        var css = ['page'];
        if (page_class_name) {
            css.push(page_class_name);
        }
        var pageCss = ramda_1.join(' ', css);
        return (react_1["default"].createElement("div", { className: class_name, id: identity },
            current_page > 1 && (react_1["default"].createElement(Page, { page: 1, text: 'first', style: page_style, class_name: pageCss, on_change: this.onChangePage })),
            current_page > 1 && (react_1["default"].createElement(Page, { page: current_page - 1, text: 'previous', style: page_style, class_name: pageCss, on_change: this.onChangePage })),
            pages.map(function (e) { return (react_1["default"].createElement(Page, { page: e, key: "page-" + e, style: page_style, class_name: pageCss, on_change: _this.onChangePage })); }),
            current_page < total_pages && (react_1["default"].createElement(Page, { page: current_page + 1, text: 'next', style: page_style, class_name: pageCss, on_change: this.onChangePage })),
            current_page < total_pages && (react_1["default"].createElement(Page, { page: total_pages, text: 'last', style: page_style, class_name: pageCss, on_change: this.onChangePage }))));
    };
    Pager.defaultProps = {
        current_page: 1,
        items_per_page: 10,
        pages_displayed: 10,
    };
    return Pager;
}(react_1["default"].Component));
exports.default = Pager;


/***/ }),

/***/ "./src/extra/js/components/PopUp.tsx":
/*!*******************************************!*\
  !*** ./src/extra/js/components/PopUp.tsx ***!
  \*******************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
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
var react_1 = __importDefault(__webpack_require__(/*! react */ "react"));
function getMouseX(e, popup) {
    return (e.clientX -
        e.target.getBoundingClientRect().left -
        popup.getBoundingClientRect().width / 2);
}
/**
 * Wraps a component/text to render a popup when hovering
 * over the children or clicking on it.
 *
 * :CSS:
 *
 *     - ``dazzler-extra-pop-up``
 *     - ``popup-content``
 *     - ``visible``
 */
var PopUp = /** @class */ (function (_super) {
    __extends(PopUp, _super);
    function PopUp(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            pos: null,
        };
        return _this;
    }
    PopUp.prototype.render = function () {
        var _this = this;
        var _a = this.props, class_name = _a.class_name, style = _a.style, identity = _a.identity, children = _a.children, content = _a.content, mode = _a.mode, updateAspects = _a.updateAspects, active = _a.active, content_style = _a.content_style, children_style = _a.children_style;
        return (react_1["default"].createElement("div", { className: class_name, style: style, id: identity },
            react_1["default"].createElement("div", { className: 'popup-content' + (active ? ' visible' : ''), style: __assign(__assign({}, (content_style || {})), { left: this.state.pos || 0 }), ref: function (r) { return (_this.popupRef = r); } }, content),
            react_1["default"].createElement("div", { className: "popup-children", onMouseEnter: function (e) {
                    if (mode === 'hover') {
                        _this.setState({ pos: getMouseX(e, _this.popupRef) }, function () { return updateAspects({ active: true }); });
                    }
                }, onMouseLeave: function () {
                    return mode === 'hover' && updateAspects({ active: false });
                }, onClick: function (e) {
                    if (mode === 'click') {
                        _this.setState({ pos: getMouseX(e, _this.popupRef) }, function () { return updateAspects({ active: !active }); });
                    }
                }, style: children_style }, children)));
    };
    PopUp.defaultProps = {
        mode: 'hover',
        active: false,
    };
    return PopUp;
}(react_1["default"].Component));
exports.default = PopUp;


/***/ }),

/***/ "./src/extra/js/components/Spinner.tsx":
/*!*********************************************!*\
  !*** ./src/extra/js/components/Spinner.tsx ***!
  \*********************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
var react_1 = __importDefault(__webpack_require__(/*! react */ "react"));
/**
 * Simple html/css spinner.
 */
var Spinner = function (props) {
    var class_name = props.class_name, style = props.style, identity = props.identity;
    return react_1["default"].createElement("div", { id: identity, className: class_name, style: style });
};
exports.default = Spinner;


/***/ }),

/***/ "./src/extra/js/components/Sticky.tsx":
/*!********************************************!*\
  !*** ./src/extra/js/components/Sticky.tsx ***!
  \********************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
var react_1 = __importDefault(__webpack_require__(/*! react */ "react"));
var ramda_1 = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
/**
 * A shorthand component for a sticky div.
 */
var Sticky = function (props) {
    var class_name = props.class_name, identity = props.identity, style = props.style, children = props.children, top = props.top, left = props.left, right = props.right, bottom = props.bottom;
    var styles = ramda_1.mergeAll([style, { top: top, left: left, right: right, bottom: bottom }]);
    return (react_1["default"].createElement("div", { className: class_name, id: identity, style: styles }, children));
};
exports.default = Sticky;


/***/ }),

/***/ "./src/extra/js/components/Toast.tsx":
/*!*******************************************!*\
  !*** ./src/extra/js/components/Toast.tsx ***!
  \*******************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

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
var ramda_1 = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
/**
 * Display a message over the ui that will disappears after a delay.
 *
 * :CSS:
 *
 *     - ``dazzler-extra-toast``
 *     - ``opened``
 *     - ``toast-inner``
 *     - ``top``
 *     - ``top-left``
 *     - ``top-right``
 *     - ``bottom``
 *     - ``bottom-left``
 *     - ``bottom-right``
 *     - ``right``
 */
var Toast = function (props) {
    var class_name = props.class_name, style = props.style, identity = props.identity, message = props.message, position = props.position, opened = props.opened, delay = props.delay, updateAspects = props.updateAspects;
    var _a = react_1.useState(false), displayed = _a[0], setDisplayed = _a[1];
    var css = react_1.useMemo(function () {
        var c = [class_name, position];
        if (opened) {
            c.push('opened');
        }
        return ramda_1.join(' ', c);
    }, [class_name, opened, position]);
    react_1.useEffect(function () {
        if (opened && !displayed) {
            setTimeout(function () {
                updateAspects({ opened: false });
                setDisplayed(false);
            }, delay);
            setDisplayed(true);
        }
    }, [opened, displayed, delay]);
    return (react_1["default"].createElement("div", { className: css, style: style, id: identity }, message));
};
Toast.defaultProps = {
    delay: 3000,
    position: 'top',
    opened: true,
};
exports.default = Toast;


/***/ }),

/***/ "./src/extra/js/components/TreeView.tsx":
/*!**********************************************!*\
  !*** ./src/extra/js/components/TreeView.tsx ***!
  \**********************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

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
var __rest = (this && this.__rest) || function (s, e) {
    var t = {};
    for (var p in s) if (Object.prototype.hasOwnProperty.call(s, p) && e.indexOf(p) < 0)
        t[p] = s[p];
    if (s != null && typeof Object.getOwnPropertySymbols === "function")
        for (var i = 0, p = Object.getOwnPropertySymbols(s); i < p.length; i++) {
            if (e.indexOf(p[i]) < 0 && Object.prototype.propertyIsEnumerable.call(s, p[i]))
                t[p[i]] = s[p[i]];
        }
    return t;
};
exports.__esModule = true;
var react_1 = __importStar(__webpack_require__(/*! react */ "react"));
var ramda_1 = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
var TreeViewElement = function (_a) {
    var label = _a.label, onClick = _a.onClick, identifier = _a.identifier, items = _a.items, level = _a.level, selected = _a.selected, expanded_items = _a.expanded_items, nest_icon_expanded = _a.nest_icon_expanded, nest_icon_collapsed = _a.nest_icon_collapsed;
    var isSelected = react_1.useMemo(function () { return selected && ramda_1.includes(identifier, selected); }, [selected, identifier]);
    var isExpanded = react_1.useMemo(function () { return ramda_1.includes(identifier, expanded_items); }, [expanded_items, expanded_items]);
    var css = ['tree-item-label', "level-" + level];
    if (isSelected) {
        css.push('selected');
    }
    return (react_1["default"].createElement("div", { className: "tree-item level-" + level, style: { marginLeft: level + "rem" } },
        react_1["default"].createElement("div", { className: ramda_1.join(' ', css), onClick: function (e) { return onClick(e, identifier, Boolean(items)); } },
            items && (react_1["default"].createElement("span", { className: "tree-caret" }, isExpanded ? nest_icon_expanded : nest_icon_collapsed)),
            label || identifier),
        items && isExpanded && (react_1["default"].createElement("div", { className: "tree-sub-items" }, items.map(function (item) {
            return renderItem({
                parent: identifier,
                onClick: onClick,
                item: item,
                level: level + 1,
                selected: selected,
                nest_icon_expanded: nest_icon_expanded,
                nest_icon_collapsed: nest_icon_collapsed,
                expanded_items: expanded_items,
            });
        })))));
};
var renderItem = function (_a) {
    var parent = _a.parent, item = _a.item, level = _a.level, rest = __rest(_a, ["parent", "item", "level"]);
    if (ramda_1.is(String, item)) {
        return (react_1["default"].createElement(TreeViewElement, __assign({ label: item, identifier: parent ? ramda_1.join('.', [parent, item]) : item, level: level || 0, key: item }, rest)));
    }
    return (react_1["default"].createElement(TreeViewElement, __assign({}, item, { level: level || 0, key: item.identifier, identifier: parent ? ramda_1.join('.', [parent, item.identifier]) : item.identifier }, rest)));
};
/**
 * A tree of nested items.
 *
 * :CSS:
 *
 *     - ``dazzler-extra-tree-view``
 *     - ``tree-item``
 *     - ``tree-item-label``
 *     - ``tree-sub-items``
 *     - ``tree-caret``
 *     - ``selected``
 *     - ``level-{n}``
 *
 * :example:
 *
 * .. literalinclude:: ../../tests/components/pages/treeview.py
 */
var TreeView = function (_a) {
    var class_name = _a.class_name, style = _a.style, identity = _a.identity, updateAspects = _a.updateAspects, items = _a.items, selected = _a.selected, expanded_items = _a.expanded_items, nest_icon_expanded = _a.nest_icon_expanded, nest_icon_collapsed = _a.nest_icon_collapsed;
    var onClick = function (e, identifier, expand) {
        e.stopPropagation();
        var payload = {};
        if (selected && ramda_1.includes(identifier, selected)) {
            var last = ramda_1.split('.', identifier);
            last = ramda_1.slice(0, last.length - 1, last);
            if (last.length === 0) {
                payload.selected = null;
            }
            else if (last.length === 1) {
                payload.selected = last[0];
            }
            else {
                payload.selected = ramda_1.join('.', last);
            }
        }
        else {
            payload.selected = identifier;
        }
        if (expand) {
            if (ramda_1.includes(identifier, expanded_items)) {
                payload.expanded_items = ramda_1.without([identifier], expanded_items);
            }
            else {
                payload.expanded_items = ramda_1.concat(expanded_items, [identifier]);
            }
        }
        updateAspects(payload);
    };
    return (react_1["default"].createElement("div", { className: class_name, style: style, id: identity }, items.map(function (item) {
        return renderItem({
            item: item,
            onClick: onClick,
            selected: selected,
            nest_icon_expanded: nest_icon_expanded,
            nest_icon_collapsed: nest_icon_collapsed,
            expanded_items: expanded_items,
        });
    })));
};
TreeView.defaultProps = {
    nest_icon_collapsed: '⏵',
    nest_icon_expanded: '⏷',
    expanded_items: [],
};
exports.default = TreeView;


/***/ }),

/***/ "./src/extra/js/index.ts":
/*!*******************************!*\
  !*** ./src/extra/js/index.ts ***!
  \*******************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
exports.ColorPicker = exports.PageMap = exports.Toast = exports.TreeView = exports.PopUp = exports.Drawer = exports.Sticky = exports.Spinner = exports.Pager = exports.Notice = void 0;
__webpack_require__(/*! ../scss/index.scss */ "./src/extra/scss/index.scss");
var Notice_1 = __importDefault(__webpack_require__(/*! ./components/Notice */ "./src/extra/js/components/Notice.tsx"));
exports.Notice = Notice_1["default"];
var Pager_1 = __importDefault(__webpack_require__(/*! ./components/Pager */ "./src/extra/js/components/Pager.tsx"));
exports.Pager = Pager_1["default"];
var Spinner_1 = __importDefault(__webpack_require__(/*! ./components/Spinner */ "./src/extra/js/components/Spinner.tsx"));
exports.Spinner = Spinner_1["default"];
var Sticky_1 = __importDefault(__webpack_require__(/*! ./components/Sticky */ "./src/extra/js/components/Sticky.tsx"));
exports.Sticky = Sticky_1["default"];
var Drawer_1 = __importDefault(__webpack_require__(/*! ./components/Drawer */ "./src/extra/js/components/Drawer.tsx"));
exports.Drawer = Drawer_1["default"];
var PopUp_1 = __importDefault(__webpack_require__(/*! ./components/PopUp */ "./src/extra/js/components/PopUp.tsx"));
exports.PopUp = PopUp_1["default"];
var TreeView_1 = __importDefault(__webpack_require__(/*! ./components/TreeView */ "./src/extra/js/components/TreeView.tsx"));
exports.TreeView = TreeView_1["default"];
var Toast_1 = __importDefault(__webpack_require__(/*! ./components/Toast */ "./src/extra/js/components/Toast.tsx"));
exports.Toast = Toast_1["default"];
var PageMap_1 = __importDefault(__webpack_require__(/*! ./components/PageMap */ "./src/extra/js/components/PageMap.tsx"));
exports.PageMap = PageMap_1["default"];
var ColorPicker_1 = __importDefault(__webpack_require__(/*! ./components/ColorPicker */ "./src/extra/js/components/ColorPicker.tsx"));
exports.ColorPicker = ColorPicker_1["default"];


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
/******/ var __webpack_exports__ = (__webpack_exec__("./src/extra/js/index.ts"));
/******/ return __webpack_exports__;
/******/ }
]);
});
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiZGF6emxlcl9leHRyYV8yYzMxMjMyMjEwNmE5OTA5OGQzYS5qcyIsIm1hcHBpbmdzIjoiQUFBQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQSxDQUFDO0FBQ0QsTzs7Ozs7Ozs7QUNWQTs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQ0FxRyxhQUFhLG9DQUFvQyxZQUFZLG1CQUFtQixLQUFLLG1CQUFtQixzRUFBc0UsU0FBUyx3QkFBd0IsZ0JBQWdCLG9CQUFvQixZQUFZLGtCQUFrQixRQUFRLFdBQVcsc0NBQXNDLFNBQVMsaUNBQWlDLGtEQUFDLENBQUMsNENBQUMsQ0FBQyxjQUFjLE1BQU0sNkNBQUMsSUFBSSxPQUFPLGdEQUFDLFlBQVksWUFBWSxFQUFFLGtEQUFDLGFBQWEsK0JBQStCLEtBQUssd0JBQXdCLHlEQUF5RCxlQUFlLG9CQUFvQixpQkFBaUIsc0RBQXNELE9BQU8sNEdBQTRHLGVBQWUsMEJBQTBCLEdBQUcsaURBQU0sYUFBYSxxREFBcUQsNkNBQUMsU0FBUyw2Q0FBQyxPQUFPLCtDQUFDLG1DQUFtQyxrREFBQyxhQUFhLDhFQUE4RSxRQUFRLGtEQUFDLGFBQWEsa0NBQWtDLDRGQUE0RixRQUFRLGtEQUFDLGFBQWEseUJBQXlCLG1DQUFtQywyREFBMkQsR0FBRyxRQUFRLGtEQUFDLFlBQVksYUFBYSxPQUFPLGtEQUFDLGFBQWEsMkRBQTJELDJFQUEyRSxRQUFRLG9CQUFvQix1QkFBdUIsVUFBVSxRQUFRLDBEQUFlLFdBQVcsSUFBSSxnSEFBZ0gsR0FBRyxnQkFBZ0IsbUNBQW1DLGVBQWUsOEZBQThGLE9BQU8sMERBQWUsUUFBUSxtQkFBbUIsOEJBQThCLENBQUMsMERBQWUsUUFBUSxnREFBZ0QsbUJBQW1CLEdBQUcsbUJBQW1CLDBFQUEwRSxJQUFJLHFDQUFxQyxlQUFlLDhDQUE4QywrRUFBK0UsRUFBRSw0RkFBNEYsaUJBQWlCLGlEQUFpRCxlQUFlLDJJQUEySSxZQUFZLHlGQUF5RixHQUFHLGlCQUFp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SyxTQUFTLEVBQUUsVUFBVSxFQUFFLEtBQUssRUFBRSxLQUFLLEVBQUUsRUFBRSxFQUFFLFFBQVEsSUFDakQsS0FBSyxDQUFDLEdBQUcsQ0FBQyxVQUFDLElBQUk7UUFDWixpQkFBVSxDQUFDO1lBQ1AsSUFBSTtZQUNKLE9BQU87WUFDUCxRQUFRO1lBQ1Isa0JBQWtCO1lBQ2xCLG1CQUFtQjtZQUNuQixjQUFjO1NBQ2pCLENBQUM7SUFQRixDQU9FLENBQ0wsQ0FDQyxDQUNULENBQUM7QUFDTixDQUFDLENBQUM7QUFFRixRQUFRLENBQUMsWUFBWSxHQUFHO0lBQ3BCLG1CQUFtQixFQUFFLEdBQUc7SUFDeEIsa0JBQWtCLEVBQUUsR0FBRztJQUN2QixjQUFjLEVBQUUsRUFBRTtDQUNyQixDQUFDO0FBRUYsa0JBQWUsUUFBUSxDQUFDOzs7Ozs7Ozs7Ozs7Ozs7Ozs7QUN0S3hCLDZFQUE0QjtBQUU1Qix1SEFBeUM7QUFZckMsaUJBWkcsbUJBQU0sQ0FZSDtBQVhWLG9IQUF1QztBQVluQyxnQkFaRyxrQkFBSyxDQVlIO0FBWFQsMEhBQTJDO0FBWXZDLGtCQVpHLG9CQUFPLENBWUg7QUFYWCx1SEFBeUM7QUFZckMsaUJBWkcsbUJBQU0sQ0FZSDtBQVhWLHVIQUF5QztBQVlyQyxpQkFaRyxtQkFBTSxDQVlIO0FBWFYsb0hBQXVDO0FBWW5DLGdCQVpHLGtCQUFLLENBWUg7QUFYVCw2SEFBNkM7QUFZekMsbUJBWkcscUJBQVEsQ0FZSDtBQVhaLG9IQUF1QztBQVluQyxnQkFaRyxrQkFBSyxDQVlIO0FBWFQsMEhBQTJDO0FBWXZDLGtCQVpHLG9CQUFPLENBWUg7QUFYWCxzSUFBbUQ7QUFZL0Msc0JBWkcsd0JBQVcsQ0FZSDs7Ozs7Ozs7Ozs7O0FDdkJmIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vLy93ZWJwYWNrL3VuaXZlcnNhbE1vZHVsZURlZmluaXRpb24/Iiwid2VicGFjazovLy8uL3NyYy9leHRyYS9zY3NzL2luZGV4LnNjc3MvLi9zcmMvZXh0cmEvc2Nzcy9pbmRleC5zY3NzPyIsIndlYnBhY2s6Ly8vLi9ub2RlX21vZHVsZXMvcmVhY3QtY29sb3JmdWwvZGlzdC9pbmRleC5tb2R1bGUuanMvLi9ub2RlX21vZHVsZXMvcmVhY3QtY29sb3JmdWwvZGlzdC9pbmRleC5tb2R1bGUuanM/Iiwid2VicGFjazovLy8vLi9zcmMvZXh0cmEvanMvY29tcG9uZW50cy9Db2xvclBpY2tlci50c3g/Iiwid2VicGFjazovLy8vLi9zcmMvZXh0cmEvanMvY29tcG9uZW50cy9EcmF3ZXIudHN4PyIsIndlYnBhY2s6Ly8vLy4vc3JjL2V4dHJhL2pzL2NvbXBvbmVudHMvTm90aWNlLnRzeD8iLCJ3ZWJwYWNrOi8vLy8uL3NyYy9leHRyYS9qcy9jb21wb25lbnRzL1BhZ2VNYXAudHN4PyIsIndlYnBhY2s6Ly8vLy4vc3JjL2V4dHJhL2pzL2NvbXBvbmVudHMvUGFnZXIudHN4PyIsIndlYnBhY2s6Ly8vLy4vc3JjL2V4dHJhL2pzL2NvbXBvbmVudHMvUG9wVXAudHN4PyIsIndlYnBhY2s6Ly8vLy4vc3JjL2V4dHJhL2pzL2NvbXBvbmVudHMvU3Bpbm5lci50c3g/Iiwid2VicGFjazovLy8vLi9zcmMvZXh0cmEvanMvY29tcG9uZW50cy9TdGlja3kudHN4PyIsIndlYnBhY2s6Ly8vLy4vc3JjL2V4dHJhL2pzL2NvbXBvbmVudHMvVG9hc3QudHN4PyIsIndlYnBhY2s6Ly8vLy4vc3JjL2V4dHJhL2pzL2NvbXBvbmVudHMvVHJlZVZpZXcudHN4PyIsIndlYnBhY2s6Ly8vLy4vc3JjL2V4dHJhL2pzL2luZGV4LnRzPyIsIndlYnBhY2s6Ly8vL2V4dGVybmFsIHtcImNvbW1vbmpzXCI6XCJyZWFjdFwiLFwiY29tbW9uanMyXCI6XCJyZWFjdFwiLFwiYW1kXCI6XCJyZWFjdFwiLFwidW1kXCI6XCJyZWFjdFwiLFwicm9vdFwiOlwiUmVhY3RcIn0/Il0sInNvdXJjZXNDb250ZW50IjpbIihmdW5jdGlvbiB3ZWJwYWNrVW5pdmVyc2FsTW9kdWxlRGVmaW5pdGlvbihyb290LCBmYWN0b3J5KSB7XG5cdGlmKHR5cGVvZiBleHBvcnRzID09PSAnb2JqZWN0JyAmJiB0eXBlb2YgbW9kdWxlID09PSAnb2JqZWN0Jylcblx0XHRtb2R1bGUuZXhwb3J0cyA9IGZhY3RvcnkocmVxdWlyZShcInJlYWN0XCIpKTtcblx0ZWxzZSBpZih0eXBlb2YgZGVmaW5lID09PSAnZnVuY3Rpb24nICYmIGRlZmluZS5hbWQpXG5cdFx0ZGVmaW5lKFtcInJlYWN0XCJdLCBmYWN0b3J5KTtcblx0ZWxzZSBpZih0eXBlb2YgZXhwb3J0cyA9PT0gJ29iamVjdCcpXG5cdFx0ZXhwb3J0c1tcImRhenpsZXJfZXh0cmFcIl0gPSBmYWN0b3J5KHJlcXVpcmUoXCJyZWFjdFwiKSk7XG5cdGVsc2Vcblx0XHRyb290W1wiZGF6emxlcl9leHRyYVwiXSA9IGZhY3Rvcnkocm9vdFtcIlJlYWN0XCJdKTtcbn0pKHNlbGYsIGZ1bmN0aW9uKF9fV0VCUEFDS19FWFRFUk5BTF9NT0RVTEVfcmVhY3RfXykge1xucmV0dXJuICIsIi8vIGV4dHJhY3RlZCBieSBtaW5pLWNzcy1leHRyYWN0LXBsdWdpbiIsImltcG9ydCBlLHt1c2VMYXlvdXRFZmZlY3QgYXMgcix1c2VFZmZlY3QgYXMgdCx1c2VDYWxsYmFjayBhcyBvLHVzZVJlZiBhcyBuLHVzZVN0YXRlIGFzIGF9ZnJvbVwicmVhY3RcIjtmdW5jdGlvbiBsKCl7cmV0dXJuKGw9T2JqZWN0LmFzc2lnbnx8ZnVuY3Rpb24oZSl7Zm9yKHZhciByPTE7cjxhcmd1bWVudHMubGVuZ3RoO3IrKyl7dmFyIHQ9YXJndW1lbnRzW3JdO2Zvcih2YXIgbyBpbiB0KU9iamVjdC5wcm90b3R5cGUuaGFzT3duUHJvcGVydHkuY2FsbCh0LG8pJiYoZVtvXT10W29dKX1yZXR1cm4gZX0pLmFwcGx5KHRoaXMsYXJndW1lbnRzKX1mdW5jdGlvbiB1KGUscil7aWYobnVsbD09ZSlyZXR1cm57fTt2YXIgdCxvLG49e30sYT1PYmplY3Qua2V5cyhlKTtmb3Iobz0wO288YS5sZW5ndGg7bysrKXIuaW5kZXhPZih0PWFbb10pPj0wfHwoblt0XT1lW3RdKTtyZXR1cm4gbn12YXIgYz1cInVuZGVmaW5lZFwiIT10eXBlb2Ygd2luZG93P3I6dDtmdW5jdGlvbiBpKGUpe3ZhciByPW4oZSk7cmV0dXJuIHQoZnVuY3Rpb24oKXtyLmN1cnJlbnQ9ZX0pLG8oZnVuY3Rpb24oZSl7cmV0dXJuIHIuY3VycmVudCYmci5jdXJyZW50KGUpfSxbXSl9dmFyIHMsZj1mdW5jdGlvbihlLHIsdCl7cmV0dXJuIHZvaWQgMD09PXImJihyPTApLHZvaWQgMD09PXQmJih0PTEpLGU+dD90OmU8cj9yOmV9LHY9ZnVuY3Rpb24oZSl7cmV0dXJuXCJ0b3VjaGVzXCJpbiBlfSxkPWZ1bmN0aW9uKGUscil7dmFyIHQ9ZS5nZXRCb3VuZGluZ0NsaWVudFJlY3QoKSxvPXYocik/ci50b3VjaGVzWzBdOnI7cmV0dXJue2xlZnQ6Zigoby5wYWdlWC0odC5sZWZ0K3dpbmRvdy5wYWdlWE9mZnNldCkpL3Qud2lkdGgpLHRvcDpmKChvLnBhZ2VZLSh0LnRvcCt3aW5kb3cucGFnZVlPZmZzZXQpKS90LmhlaWdodCl9fSxoPWZ1bmN0aW9uKGUpeyF2KGUpJiZlLnByZXZlbnREZWZhdWx0KCl9LG09ZS5tZW1vKGZ1bmN0aW9uKHIpe3ZhciB0PXIub25Nb3ZlLHM9ci5vbktleSxmPXUocixbXCJvbk1vdmVcIixcIm9uS2V5XCJdKSxtPW4obnVsbCksZz1uKCExKSxwPWEoITEpLGI9cFswXSxfPXBbMV0sQz1pKHQpLHg9aShzKSxFPW8oZnVuY3Rpb24oZSl7aChlKSwodihlKT9lLnRvdWNoZXMubGVuZ3RoPjA6ZS5idXR0b25zPjApJiZtLmN1cnJlbnQ/QyhkKG0uY3VycmVudCxlKSk6XyghMSl9LFtDXSksSD1vKGZ1bmN0aW9uKGUpe3ZhciByLHQ9ZS5uYXRpdmVFdmVudCxvPW0uY3VycmVudDtoKHQpLHI9dCxnLmN1cnJlbnQmJiF2KHIpfHwoZy5jdXJyZW50fHwoZy5jdXJyZW50PXYocikpLDApfHwhb3x8KG8uZm9jdXMoKSxDKGQobyx0KSksXyghMCkpfSxbQ10pLE09byhmdW5jdGlvbihlKXt2YXIgcj1lLndoaWNofHxlLmtleUNvZGU7cjwzN3x8cj40MHx8KGUucHJldmVudERlZmF1bHQoKSx4KHtsZWZ0OjM5PT09cj8uMDU6Mzc9PT1yPy0uMDU6MCx0b3A6NDA9PT1yPy4wNTozOD09PXI/LS4wNTowfSkpfSxbeF0pLE49byhmdW5jdGlvbigpe3JldHVybiBfKCExKX0sW10pLHc9byhmdW5jdGlvbihlKXt2YXIgcj1lP3dpbmRvdy5hZGRFdmVudExpc3RlbmVyOndpbmRvdy5yZW1vdmVFdmVudExpc3RlbmVyO3IoZy5jdXJyZW50P1widG91Y2htb3ZlXCI6XCJtb3VzZW1vdmVcIixFKSxyKGcuY3VycmVudD9cInRvdWNoZW5kXCI6XCJtb3VzZXVwXCIsTil9LFtFLE5dKTtyZXR1cm4gYyhmdW5jdGlvbigpe3JldHVybiB3KGIpLGZ1bmN0aW9uKCl7YiYmdyghMSl9fSxbYix3XSksZS5jcmVhdGVFbGVtZW50KFwiZGl2XCIsbCh7fSxmLHtjbGFzc05hbWU6XCJyZWFjdC1jb2xvcmZ1bF9faW50ZXJhY3RpdmVcIixyZWY6bSxvblRvdWNoU3RhcnQ6SCxvbk1vdXNlRG93bjpILG9uS2V5RG93bjpNLHRhYkluZGV4OjAscm9sZTpcInNsaWRlclwifSkpfSksZz1mdW5jdGlvbihlKXtyZXR1cm4gZS5maWx0ZXIoQm9vbGVhbikuam9pbihcIiBcIil9LHA9ZnVuY3Rpb24ocil7dmFyIHQ9ci5jb2xvcixvPXIubGVmdCxuPXIudG9wLGE9dm9pZCAwPT09bj8uNTpuLGw9ZyhbXCJyZWFjdC1jb2xvcmZ1bF9fcG9pbnRlclwiLHIuY2xhc3NOYW1lXSk7cmV0dXJuIGUuY3JlYXRlRWxlbWVudChcImRpdlwiLHtjbGFzc05hbWU6bCxzdHlsZTp7dG9wOjEwMCphK1wiJVwiLGxlZnQ6MTAwKm8rXCIlXCJ9fSxlLmNyZWF0ZUVsZW1lbnQoXCJkaXZcIix7Y2xhc3NOYW1lOlwicmVhY3QtY29sb3JmdWxfX3BvaW50ZXItZmlsbFwiLHN0eWxlOntiYWNrZ3JvdW5kQ29sb3I6dH19KSl9LGI9ZnVuY3Rpb24oZSxyLHQpe3JldHVybiB2b2lkIDA9PT1yJiYocj0wKSx2b2lkIDA9PT10JiYodD1NYXRoLnBvdygxMCxyKSksTWF0aC5yb3VuZCh0KmUpL3R9LF89e2dyYWQ6LjksdHVybjozNjAscmFkOjM2MC8oMipNYXRoLlBJKX0sQz1mdW5jdGlvbihlKXtyZXR1cm5cIiNcIj09PWVbMF0mJihlPWUuc3Vic3RyKDEpKSxlLmxlbmd0aDw2P3tyOnBhcnNlSW50KGVbMF0rZVswXSwxNiksZzpwYXJzZUludChlWzFdK2VbMV0sMTYpLGI6cGFyc2VJbnQoZVsyXStlWzJdLDE2KSxhOjF9OntyOnBhcnNlSW50KGUuc3Vic3RyKDAsMiksMTYpLGc6cGFyc2VJbnQoZS5zdWJzdHIoMiwyKSwxNiksYjpwYXJzZUludChlLnN1YnN0cig0LDIpLDE2KSxhOjF9fSx4PWZ1bmN0aW9uKGUscil7cmV0dXJuIHZvaWQgMD09PXImJihyPVwiZGVnXCIpLE51bWJlcihlKSooX1tyXXx8MSl9LEU9ZnVuY3Rpb24oZSl7dmFyIHI9L2hzbGE/XFwoP1xccyooLT9cXGQqXFwuP1xcZCspKGRlZ3xyYWR8Z3JhZHx0dXJuKT9bLFxcc10rKC0/XFxkKlxcLj9cXGQrKSU/WyxcXHNdKygtP1xcZCpcXC4/XFxkKyklPyw/XFxzKlsvXFxzXSooLT9cXGQqXFwuP1xcZCspPyglKT9cXHMqXFwpPy9pLmV4ZWMoZSk7cmV0dXJuIHI/TSh7aDp4KHJbMV0sclsyXSksczpOdW1iZXIoclszXSksbDpOdW1iZXIocls0XSksYTp2b2lkIDA9PT1yWzVdPzE6TnVtYmVyKHJbNV0pLyhyWzZdPzEwMDoxKX0pOntoOjAsczowLHY6MCxhOjF9fSxIPUUsTT1mdW5jdGlvbihlKXt2YXIgcj1lLnMsdD1lLmw7cmV0dXJue2g6ZS5oLHM6KHIqPSh0PDUwP3Q6MTAwLXQpLzEwMCk+MD8yKnIvKHQrcikqMTAwOjAsdjp0K3IsYTplLmF9fSxOPWZ1bmN0aW9uKGUpe3ZhciByPWUucyx0PWUudixvPWUuYSxuPSgyMDAtcikqdC8xMDA7cmV0dXJue2g6YihlLmgpLHM6YihuPjAmJm48MjAwP3IqdC8xMDAvKG48PTEwMD9uOjIwMC1uKSoxMDA6MCksbDpiKG4vMiksYTpiKG8sMil9fSx3PWZ1bmN0aW9uKGUpe3ZhciByPU4oZSk7cmV0dXJuXCJoc2woXCIrci5oK1wiLCBcIityLnMrXCIlLCBcIityLmwrXCIlKVwifSx5PWZ1bmN0aW9uKGUpe3ZhciByPU4oZSk7cmV0dXJuXCJoc2xhKFwiK3IuaCtcIiwgXCIrci5zK1wiJSwgXCIrci5sK1wiJSwgXCIrci5hK1wiKVwifSxxPWZ1bmN0aW9uKGUpe3ZhciByPWUuaCx0PWUucyxvPWUudixuPWUuYTtyPXIvMzYwKjYsdC89MTAwLG8vPTEwMDt2YXIgYT1NYXRoLmZsb29yKHIpLGw9byooMS10KSx1PW8qKDEtKHItYSkqdCksYz1vKigxLSgxLXIrYSkqdCksaT1hJTY7cmV0dXJue3I6YigyNTUqW28sdSxsLGwsYyxvXVtpXSksZzpiKDI1NSpbYyxvLG8sdSxsLGxdW2ldKSxiOmIoMjU1KltsLGwsYyxvLG8sdV1baV0pLGE6YihuLDIpfX0saz1mdW5jdGlvbihlKXt2YXIgcj0vaHN2YT9cXCg/XFxzKigtP1xcZCpcXC4/XFxkKykoZGVnfHJhZHxncmFkfHR1cm4pP1ssXFxzXSsoLT9cXGQqXFwuP1xcZCspJT9bLFxcc10rKC0/XFxkKlxcLj9cXGQrKSU/LD9cXHMqWy9cXHNdKigtP1xcZCpcXC4/XFxkKyk/KCUpP1xccypcXCk/L2kuZXhlYyhlKTtyZXR1cm4gcj9LKHtoOngoclsxXSxyWzJdKSxzOk51bWJlcihyWzNdKSx2Ok51bWJlcihyWzRdKSxhOnZvaWQgMD09PXJbNV0/MTpOdW1iZXIocls1XSkvKHJbNl0/MTAwOjEpfSk6e2g6MCxzOjAsdjowLGE6MX19LE89ayxJPWZ1bmN0aW9uKGUpe3ZhciByPS9yZ2JhP1xcKD9cXHMqKC0/XFxkKlxcLj9cXGQrKSglKT9bLFxcc10rKC0/XFxkKlxcLj9cXGQrKSglKT9bLFxcc10rKC0/XFxkKlxcLj9cXGQrKSglKT8sP1xccypbL1xcc10qKC0/XFxkKlxcLj9cXGQrKT8oJSk/XFxzKlxcKT8vaS5leGVjKGUpO3JldHVybiByP0Ioe3I6TnVtYmVyKHJbMV0pLyhyWzJdPzEwMC8yNTU6MSksZzpOdW1iZXIoclszXSkvKHJbNF0/MTAwLzI1NToxKSxiOk51bWJlcihyWzVdKS8ocls2XT8xMDAvMjU1OjEpLGE6dm9pZCAwPT09cls3XT8xOk51bWJlcihyWzddKS8ocls4XT8xMDA6MSl9KTp7aDowLHM6MCx2OjAsYToxfX0saj1JLHo9ZnVuY3Rpb24oZSl7dmFyIHI9ZS50b1N0cmluZygxNik7cmV0dXJuIHIubGVuZ3RoPDI/XCIwXCIrcjpyfSxCPWZ1bmN0aW9uKGUpe3ZhciByPWUucix0PWUuZyxvPWUuYixuPWUuYSxhPU1hdGgubWF4KHIsdCxvKSxsPWEtTWF0aC5taW4ocix0LG8pLHU9bD9hPT09cj8odC1vKS9sOmE9PT10PzIrKG8tcikvbDo0KyhyLXQpL2w6MDtyZXR1cm57aDpiKDYwKih1PDA/dSs2OnUpKSxzOmIoYT9sL2EqMTAwOjApLHY6YihhLzI1NSoxMDApLGE6bn19LEs9ZnVuY3Rpb24oZSl7cmV0dXJue2g6YihlLmgpLHM6YihlLnMpLHY6YihlLnYpLGE6YihlLmEsMil9fSxBPWUubWVtbyhmdW5jdGlvbihyKXt2YXIgdD1yLmh1ZSxvPXIub25DaGFuZ2Usbj1nKFtcInJlYWN0LWNvbG9yZnVsX19odWVcIixyLmNsYXNzTmFtZV0pO3JldHVybiBlLmNyZWF0ZUVsZW1lbnQoXCJkaXZcIix7Y2xhc3NOYW1lOm59LGUuY3JlYXRlRWxlbWVudChtLHtvbk1vdmU6ZnVuY3Rpb24oZSl7byh7aDozNjAqZS5sZWZ0fSl9LG9uS2V5OmZ1bmN0aW9uKGUpe28oe2g6Zih0KzM2MCplLmxlZnQsMCwzNjApfSl9LFwiYXJpYS1sYWJlbFwiOlwiSHVlXCIsXCJhcmlhLXZhbHVldGV4dFwiOmIodCl9LGUuY3JlYXRlRWxlbWVudChwLHtjbGFzc05hbWU6XCJyZWFjdC1jb2xvcmZ1bF9faHVlLXBvaW50ZXJcIixsZWZ0OnQvMzYwLGNvbG9yOncoe2g6dCxzOjEwMCx2OjEwMCxhOjF9KX0pKSl9KSxMPWUubWVtbyhmdW5jdGlvbihyKXt2YXIgdD1yLmhzdmEsbz1yLm9uQ2hhbmdlLG49e2JhY2tncm91bmRDb2xvcjp3KHtoOnQuaCxzOjEwMCx2OjEwMCxhOjF9KX07cmV0dXJuIGUuY3JlYXRlRWxlbWVudChcImRpdlwiLHtjbGFzc05hbWU6XCJyZWFjdC1jb2xvcmZ1bF9fc2F0dXJhdGlvblwiLHN0eWxlOm59LGUuY3JlYXRlRWxlbWVudChtLHtvbk1vdmU6ZnVuY3Rpb24oZSl7byh7czoxMDAqZS5sZWZ0LHY6MTAwLTEwMCplLnRvcH0pfSxvbktleTpmdW5jdGlvbihlKXtvKHtzOmYodC5zKzEwMCplLmxlZnQsMCwxMDApLHY6Zih0LnYtMTAwKmUudG9wLDAsMTAwKX0pfSxcImFyaWEtbGFiZWxcIjpcIkNvbG9yXCIsXCJhcmlhLXZhbHVldGV4dFwiOlwiU2F0dXJhdGlvbiBcIitiKHQucykrXCIlLCBCcmlnaHRuZXNzIFwiK2IodC52KStcIiVcIn0sZS5jcmVhdGVFbGVtZW50KHAse2NsYXNzTmFtZTpcInJlYWN0LWNvbG9yZnVsX19zYXR1cmF0aW9uLXBvaW50ZXJcIix0b3A6MS10LnYvMTAwLGxlZnQ6dC5zLzEwMCxjb2xvcjp3KHQpfSkpKX0pLEQ9ZnVuY3Rpb24oZSxyKXtpZihlPT09cilyZXR1cm4hMDtmb3IodmFyIHQgaW4gZSlpZihlW3RdIT09clt0XSlyZXR1cm4hMTtyZXR1cm4hMH0sRj1mdW5jdGlvbihlLHIpe3JldHVybiBlLnJlcGxhY2UoL1xccy9nLFwiXCIpPT09ci5yZXBsYWNlKC9cXHMvZyxcIlwiKX07ZnVuY3Rpb24gUyhlLHIsbCl7dmFyIHU9aShsKSxjPWEoZnVuY3Rpb24oKXtyZXR1cm4gZS50b0hzdmEocil9KSxzPWNbMF0sZj1jWzFdLHY9bih7Y29sb3I6cixoc3ZhOnN9KTt0KGZ1bmN0aW9uKCl7aWYoIWUuZXF1YWwocix2LmN1cnJlbnQuY29sb3IpKXt2YXIgdD1lLnRvSHN2YShyKTt2LmN1cnJlbnQ9e2hzdmE6dCxjb2xvcjpyfSxmKHQpfX0sW3IsZV0pLHQoZnVuY3Rpb24oKXt2YXIgcjtEKHMsdi5jdXJyZW50LmhzdmEpfHxlLmVxdWFsKHI9ZS5mcm9tSHN2YShzKSx2LmN1cnJlbnQuY29sb3IpfHwodi5jdXJyZW50PXtoc3ZhOnMsY29sb3I6cn0sdShyKSl9LFtzLGUsdV0pO3ZhciBkPW8oZnVuY3Rpb24oZSl7ZihmdW5jdGlvbihyKXtyZXR1cm4gT2JqZWN0LmFzc2lnbih7fSxyLGUpfSl9LFtdKTtyZXR1cm5bcyxkXX12YXIgUCxUPWZ1bmN0aW9uKCl7cmV0dXJuIHN8fChcInVuZGVmaW5lZFwiIT10eXBlb2YgX193ZWJwYWNrX25vbmNlX18/X193ZWJwYWNrX25vbmNlX186dm9pZCAwKX0sWD1mdW5jdGlvbihlKXtzPWV9LFk9ZnVuY3Rpb24oKXtjKGZ1bmN0aW9uKCl7aWYoXCJ1bmRlZmluZWRcIiE9dHlwZW9mIGRvY3VtZW50JiYhUCl7KFA9ZG9jdW1lbnQuY3JlYXRlRWxlbWVudChcInN0eWxlXCIpKS5pbm5lckhUTUw9Jy5yZWFjdC1jb2xvcmZ1bHtwb3NpdGlvbjpyZWxhdGl2ZTtkaXNwbGF5OmZsZXg7ZmxleC1kaXJlY3Rpb246Y29sdW1uO3dpZHRoOjIwMHB4O2hlaWdodDoyMDBweDstd2Via2l0LXVzZXItc2VsZWN0Om5vbmU7LW1vei11c2VyLXNlbGVjdDpub25lOy1tcy11c2VyLXNlbGVjdDpub25lO3VzZXItc2VsZWN0Om5vbmU7Y3Vyc29yOmRlZmF1bHR9LnJlYWN0LWNvbG9yZnVsX19zYXR1cmF0aW9ue3Bvc2l0aW9uOnJlbGF0aXZlO2ZsZXgtZ3JvdzoxO2JvcmRlci1jb2xvcjp0cmFuc3BhcmVudDtib3JkZXItYm90dG9tOjEycHggc29saWQgIzAwMDtib3JkZXItcmFkaXVzOjhweCA4cHggMCAwO2JhY2tncm91bmQtaW1hZ2U6bGluZWFyLWdyYWRpZW50KDBkZWcsIzAwMCx0cmFuc3BhcmVudCksbGluZWFyLWdyYWRpZW50KDkwZGVnLCNmZmYsaHNsYSgwLDAlLDEwMCUsMCkpfS5yZWFjdC1jb2xvcmZ1bF9fYWxwaGEtZ3JhZGllbnQsLnJlYWN0LWNvbG9yZnVsX19wb2ludGVyLWZpbGx7Y29udGVudDpcIlwiO3Bvc2l0aW9uOmFic29sdXRlO2xlZnQ6MDt0b3A6MDtyaWdodDowO2JvdHRvbTowO3BvaW50ZXItZXZlbnRzOm5vbmU7Ym9yZGVyLXJhZGl1czppbmhlcml0fS5yZWFjdC1jb2xvcmZ1bF9fYWxwaGEtZ3JhZGllbnQsLnJlYWN0LWNvbG9yZnVsX19zYXR1cmF0aW9ue2JveC1zaGFkb3c6aW5zZXQgMCAwIDAgMXB4IHJnYmEoMCwwLDAsLjA1KX0ucmVhY3QtY29sb3JmdWxfX2FscGhhLC5yZWFjdC1jb2xvcmZ1bF9faHVle3Bvc2l0aW9uOnJlbGF0aXZlO2hlaWdodDoyNHB4fS5yZWFjdC1jb2xvcmZ1bF9faHVle2JhY2tncm91bmQ6bGluZWFyLWdyYWRpZW50KDkwZGVnLHJlZCAwLCNmZjAgMTclLCMwZjAgMzMlLCMwZmYgNTAlLCMwMGYgNjclLCNmMGYgODMlLHJlZCl9LnJlYWN0LWNvbG9yZnVsX19sYXN0LWNvbnRyb2x7Ym9yZGVyLXJhZGl1czowIDAgOHB4IDhweH0ucmVhY3QtY29sb3JmdWxfX2ludGVyYWN0aXZle3Bvc2l0aW9uOmFic29sdXRlO2xlZnQ6MDt0b3A6MDtyaWdodDowO2JvdHRvbTowO2JvcmRlci1yYWRpdXM6aW5oZXJpdDtvdXRsaW5lOm5vbmU7dG91Y2gtYWN0aW9uOm5vbmV9LnJlYWN0LWNvbG9yZnVsX19wb2ludGVye3Bvc2l0aW9uOmFic29sdXRlO3otaW5kZXg6MTtib3gtc2l6aW5nOmJvcmRlci1ib3g7d2lkdGg6MjhweDtoZWlnaHQ6MjhweDt0cmFuc2Zvcm06dHJhbnNsYXRlKC01MCUsLTUwJSk7YmFja2dyb3VuZC1jb2xvcjojZmZmO2JvcmRlcjoycHggc29saWQgI2ZmZjtib3JkZXItcmFkaXVzOjUwJTtib3gtc2hhZG93OjAgMnB4IDRweCByZ2JhKDAsMCwwLC4yKX0ucmVhY3QtY29sb3JmdWxfX2ludGVyYWN0aXZlOmZvY3VzIC5yZWFjdC1jb2xvcmZ1bF9fcG9pbnRlcnt0cmFuc2Zvcm06dHJhbnNsYXRlKC01MCUsLTUwJSkgc2NhbGUoMS4xKX0ucmVhY3QtY29sb3JmdWxfX2FscGhhLC5yZWFjdC1jb2xvcmZ1bF9fYWxwaGEtcG9pbnRlcntiYWNrZ3JvdW5kLWNvbG9yOiNmZmY7YmFja2dyb3VuZC1pbWFnZTp1cmwoXFwnZGF0YTppbWFnZS9zdmcreG1sO2NoYXJzZXQ9dXRmLTgsPHN2ZyB4bWxucz1cImh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnXCIgd2lkdGg9XCIxNlwiIGhlaWdodD1cIjE2XCIgZmlsbC1vcGFjaXR5PVwiLjA1XCI+PHBhdGggZD1cIk04IDBoOHY4SDh6TTAgOGg4djhIMHpcIi8+PC9zdmc+XFwnKX0ucmVhY3QtY29sb3JmdWxfX3NhdHVyYXRpb24tcG9pbnRlcnt6LWluZGV4OjN9LnJlYWN0LWNvbG9yZnVsX19odWUtcG9pbnRlcnt6LWluZGV4OjJ9Jzt2YXIgZT1UKCk7ZSYmUC5zZXRBdHRyaWJ1dGUoXCJub25jZVwiLGUpLGRvY3VtZW50LmhlYWQuYXBwZW5kQ2hpbGQoUCl9fSxbXSl9LCQ9ZnVuY3Rpb24ocil7dmFyIHQ9ci5jbGFzc05hbWUsbz1yLmNvbG9yTW9kZWwsbj1yLmNvbG9yLGE9dm9pZCAwPT09bj9vLmRlZmF1bHRDb2xvcjpuLGM9ci5vbkNoYW5nZSxpPXUocixbXCJjbGFzc05hbWVcIixcImNvbG9yTW9kZWxcIixcImNvbG9yXCIsXCJvbkNoYW5nZVwiXSk7WSgpO3ZhciBzPVMobyxhLGMpLGY9c1swXSx2PXNbMV0sZD1nKFtcInJlYWN0LWNvbG9yZnVsXCIsdF0pO3JldHVybiBlLmNyZWF0ZUVsZW1lbnQoXCJkaXZcIixsKHt9LGkse2NsYXNzTmFtZTpkfSksZS5jcmVhdGVFbGVtZW50KEwse2hzdmE6ZixvbkNoYW5nZTp2fSksZS5jcmVhdGVFbGVtZW50KEEse2h1ZTpmLmgsb25DaGFuZ2U6dixjbGFzc05hbWU6XCJyZWFjdC1jb2xvcmZ1bF9fbGFzdC1jb250cm9sXCJ9KSl9LFI9e2RlZmF1bHRDb2xvcjpcIjAwMFwiLHRvSHN2YTpmdW5jdGlvbihlKXtyZXR1cm4gQihDKGUpKX0sZnJvbUhzdmE6ZnVuY3Rpb24oZSl7cmV0dXJuIHQ9KHI9cShlKSkuZyxvPXIuYixcIiNcIit6KHIucikreih0KSt6KG8pO3ZhciByLHQsb30sZXF1YWw6ZnVuY3Rpb24oZSxyKXtyZXR1cm4gZS50b0xvd2VyQ2FzZSgpPT09ci50b0xvd2VyQ2FzZSgpfHxEKEMoZSksQyhyKSl9fSxHPWZ1bmN0aW9uKHIpe3JldHVybiBlLmNyZWF0ZUVsZW1lbnQoJCxsKHt9LHIse2NvbG9yTW9kZWw6Un0pKX0sSj1mdW5jdGlvbihyKXt2YXIgdD1yLmNsYXNzTmFtZSxvPXIuaHN2YSxuPXIub25DaGFuZ2UsYT17YmFja2dyb3VuZEltYWdlOlwibGluZWFyLWdyYWRpZW50KDkwZGVnLCBcIit5KE9iamVjdC5hc3NpZ24oe30sbyx7YTowfSkpK1wiLCBcIit5KE9iamVjdC5hc3NpZ24oe30sbyx7YToxfSkpK1wiKVwifSxsPWcoW1wicmVhY3QtY29sb3JmdWxfX2FscGhhXCIsdF0pO3JldHVybiBlLmNyZWF0ZUVsZW1lbnQoXCJkaXZcIix7Y2xhc3NOYW1lOmx9LGUuY3JlYXRlRWxlbWVudChcImRpdlwiLHtjbGFzc05hbWU6XCJyZWFjdC1jb2xvcmZ1bF9fYWxwaGEtZ3JhZGllbnRcIixzdHlsZTphfSksZS5jcmVhdGVFbGVtZW50KG0se29uTW92ZTpmdW5jdGlvbihlKXtuKHthOmUubGVmdH0pfSxvbktleTpmdW5jdGlvbihlKXtuKHthOmYoby5hK2UubGVmdCl9KX0sXCJhcmlhLWxhYmVsXCI6XCJBbHBoYVwiLFwiYXJpYS12YWx1ZXRleHRcIjpiKDEwMCpvLmEpK1wiJVwifSxlLmNyZWF0ZUVsZW1lbnQocCx7Y2xhc3NOYW1lOlwicmVhY3QtY29sb3JmdWxfX2FscGhhLXBvaW50ZXJcIixsZWZ0Om8uYSxjb2xvcjp5KG8pfSkpKX0sUT1mdW5jdGlvbihyKXt2YXIgdD1yLmNsYXNzTmFtZSxvPXIuY29sb3JNb2RlbCxuPXIuY29sb3IsYT12b2lkIDA9PT1uP28uZGVmYXVsdENvbG9yOm4sYz1yLm9uQ2hhbmdlLGk9dShyLFtcImNsYXNzTmFtZVwiLFwiY29sb3JNb2RlbFwiLFwiY29sb3JcIixcIm9uQ2hhbmdlXCJdKTtZKCk7dmFyIHM9UyhvLGEsYyksZj1zWzBdLHY9c1sxXSxkPWcoW1wicmVhY3QtY29sb3JmdWxcIix0XSk7cmV0dXJuIGUuY3JlYXRlRWxlbWVudChcImRpdlwiLGwoe30saSx7Y2xhc3NOYW1lOmR9KSxlLmNyZWF0ZUVsZW1lbnQoTCx7aHN2YTpmLG9uQ2hhbmdlOnZ9KSxlLmNyZWF0ZUVsZW1lbnQoQSx7aHVlOmYuaCxvbkNoYW5nZTp2fSksZS5jcmVhdGVFbGVtZW50KEose2hzdmE6ZixvbkNoYW5nZTp2LGNsYXNzTmFtZTpcInJlYWN0LWNvbG9yZnVsX19sYXN0LWNvbnRyb2xcIn0pKX0sVT17ZGVmYXVsdENvbG9yOntoOjAsczowLGw6MCxhOjF9LHRvSHN2YTpNLGZyb21Ic3ZhOk4sZXF1YWw6RH0sVj1mdW5jdGlvbihyKXtyZXR1cm4gZS5jcmVhdGVFbGVtZW50KFEsbCh7fSxyLHtjb2xvck1vZGVsOlV9KSl9LFc9e2RlZmF1bHRDb2xvcjpcImhzbGEoMCwgMCUsIDAlLCAxKVwiLHRvSHN2YTpFLGZyb21Ic3ZhOnksZXF1YWw6Rn0sWj1mdW5jdGlvbihyKXtyZXR1cm4gZS5jcmVhdGVFbGVtZW50KFEsbCh7fSxyLHtjb2xvck1vZGVsOld9KSl9LGVlPXtkZWZhdWx0Q29sb3I6e2g6MCxzOjAsbDowfSx0b0hzdmE6ZnVuY3Rpb24oZSl7cmV0dXJuIE0oe2g6ZS5oLHM6ZS5zLGw6ZS5sLGE6MX0pfSxmcm9tSHN2YTpmdW5jdGlvbihlKXtyZXR1cm57aDoocj1OKGUpKS5oLHM6ci5zLGw6ci5sfTt2YXIgcn0sZXF1YWw6RH0scmU9ZnVuY3Rpb24ocil7cmV0dXJuIGUuY3JlYXRlRWxlbWVudCgkLGwoe30scix7Y29sb3JNb2RlbDplZX0pKX0sdGU9e2RlZmF1bHRDb2xvcjpcImhzbCgwLCAwJSwgMCUpXCIsdG9Ic3ZhOkgsZnJvbUhzdmE6dyxlcXVhbDpGfSxvZT1mdW5jdGlvbihyKXtyZXR1cm4gZS5jcmVhdGVFbGVtZW50KCQsbCh7fSxyLHtjb2xvck1vZGVsOnRlfSkpfSxuZT17ZGVmYXVsdENvbG9yOntoOjAsczowLHY6MCxhOjF9LHRvSHN2YTpmdW5jdGlvbihlKXtyZXR1cm4gZX0sZnJvbUhzdmE6SyxlcXVhbDpEfSxhZT1mdW5jdGlvbihyKXtyZXR1cm4gZS5jcmVhdGVFbGVtZW50KFEsbCh7fSxyLHtjb2xvck1vZGVsOm5lfSkpfSxsZT17ZGVmYXVsdENvbG9yOlwiaHN2YSgwLCAwJSwgMCUsIDEpXCIsdG9Ic3ZhOmssZnJvbUhzdmE6ZnVuY3Rpb24oZSl7dmFyIHI9SyhlKTtyZXR1cm5cImhzdmEoXCIrci5oK1wiLCBcIityLnMrXCIlLCBcIityLnYrXCIlLCBcIityLmErXCIpXCJ9LGVxdWFsOkZ9LHVlPWZ1bmN0aW9uKHIpe3JldHVybiBlLmNyZWF0ZUVsZW1lbnQoUSxsKHt9LHIse2NvbG9yTW9kZWw6bGV9KSl9LGNlPXtkZWZhdWx0Q29sb3I6e2g6MCxzOjAsdjowfSx0b0hzdmE6ZnVuY3Rpb24oZSl7cmV0dXJue2g6ZS5oLHM6ZS5zLHY6ZS52LGE6MX19LGZyb21Ic3ZhOmZ1bmN0aW9uKGUpe3ZhciByPUsoZSk7cmV0dXJue2g6ci5oLHM6ci5zLHY6ci52fX0sZXF1YWw6RH0saWU9ZnVuY3Rpb24ocil7cmV0dXJuIGUuY3JlYXRlRWxlbWVudCgkLGwoe30scix7Y29sb3JNb2RlbDpjZX0pKX0sc2U9e2RlZmF1bHRDb2xvcjpcImhzdigwLCAwJSwgMCUpXCIsdG9Ic3ZhOk8sZnJvbUhzdmE6ZnVuY3Rpb24oZSl7dmFyIHI9SyhlKTtyZXR1cm5cImhzdihcIityLmgrXCIsIFwiK3IucytcIiUsIFwiK3IuditcIiUpXCJ9LGVxdWFsOkZ9LGZlPWZ1bmN0aW9uKHIpe3JldHVybiBlLmNyZWF0ZUVsZW1lbnQoJCxsKHt9LHIse2NvbG9yTW9kZWw6c2V9KSl9LHZlPXtkZWZhdWx0Q29sb3I6e3I6MCxnOjAsYjowLGE6MX0sdG9Ic3ZhOkIsZnJvbUhzdmE6cSxlcXVhbDpEfSxkZT1mdW5jdGlvbihyKXtyZXR1cm4gZS5jcmVhdGVFbGVtZW50KFEsbCh7fSxyLHtjb2xvck1vZGVsOnZlfSkpfSxoZT17ZGVmYXVsdENvbG9yOlwicmdiYSgwLCAwLCAwLCAxKVwiLHRvSHN2YTpJLGZyb21Ic3ZhOmZ1bmN0aW9uKGUpe3ZhciByPXEoZSk7cmV0dXJuXCJyZ2JhKFwiK3IucitcIiwgXCIrci5nK1wiLCBcIityLmIrXCIsIFwiK3IuYStcIilcIn0sZXF1YWw6Rn0sbWU9ZnVuY3Rpb24ocil7cmV0dXJuIGUuY3JlYXRlRWxlbWVudChRLGwoe30scix7Y29sb3JNb2RlbDpoZX0pKX0sZ2U9e2RlZmF1bHRDb2xvcjp7cjowLGc6MCxiOjB9LHRvSHN2YTpmdW5jdGlvbihlKXtyZXR1cm4gQih7cjplLnIsZzplLmcsYjplLmIsYToxfSl9LGZyb21Ic3ZhOmZ1bmN0aW9uKGUpe3JldHVybntyOihyPXEoZSkpLnIsZzpyLmcsYjpyLmJ9O3ZhciByfSxlcXVhbDpEfSxwZT1mdW5jdGlvbihyKXtyZXR1cm4gZS5jcmVhdGVFbGVtZW50KCQsbCh7fSxyLHtjb2xvck1vZGVsOmdlfSkpfSxiZT17ZGVmYXVsdENvbG9yOlwicmdiKDAsIDAsIDApXCIsdG9Ic3ZhOmosZnJvbUhzdmE6ZnVuY3Rpb24oZSl7dmFyIHI9cShlKTtyZXR1cm5cInJnYihcIityLnIrXCIsIFwiK3IuZytcIiwgXCIrci5iK1wiKVwifSxlcXVhbDpGfSxfZT1mdW5jdGlvbihyKXtyZXR1cm4gZS5jcmVhdGVFbGVtZW50KCQsbCh7fSxyLHtjb2xvck1vZGVsOmJlfSkpfSxDZT0vXiM/WzAtOUEtRl17M30kL2kseGU9L14jP1swLTlBLUZdezZ9JC9pLEVlPWZ1bmN0aW9uKGUpe3JldHVybiB4ZS50ZXN0KGUpfHxDZS50ZXN0KGUpfSxIZT1mdW5jdGlvbihlKXtyZXR1cm4gZS5yZXBsYWNlKC8oW14wLTlBLUZdKykvZ2ksXCJcIikuc3Vic3RyKDAsNil9LE1lPWZ1bmN0aW9uKHIpe3ZhciBuPXIuY29sb3IsYz12b2lkIDA9PT1uP1wiXCI6bixzPXIub25DaGFuZ2UsZj1yLm9uQmx1cix2PXIucHJlZml4ZWQsZD11KHIsW1wiY29sb3JcIixcIm9uQ2hhbmdlXCIsXCJvbkJsdXJcIixcInByZWZpeGVkXCJdKSxoPWEoZnVuY3Rpb24oKXtyZXR1cm4gSGUoYyl9KSxtPWhbMF0sZz1oWzFdLHA9aShzKSxiPWkoZiksXz1vKGZ1bmN0aW9uKGUpe3ZhciByPUhlKGUudGFyZ2V0LnZhbHVlKTtnKHIpLEVlKHIpJiZwKFwiI1wiK3IpfSxbcF0pLEM9byhmdW5jdGlvbihlKXtFZShlLnRhcmdldC52YWx1ZSl8fGcoSGUoYykpLGIoZSl9LFtjLGJdKTtyZXR1cm4gdChmdW5jdGlvbigpe2coSGUoYykpfSxbY10pLGUuY3JlYXRlRWxlbWVudChcImlucHV0XCIsbCh7fSxkLHt2YWx1ZToodj9cIiNcIjpcIlwiKSttLHNwZWxsQ2hlY2s6XCJmYWxzZVwiLG9uQ2hhbmdlOl8sb25CbHVyOkN9KSl9O2V4cG9ydHtNZSBhcyBIZXhDb2xvcklucHV0LEcgYXMgSGV4Q29sb3JQaWNrZXIscmUgYXMgSHNsQ29sb3JQaWNrZXIsb2UgYXMgSHNsU3RyaW5nQ29sb3JQaWNrZXIsViBhcyBIc2xhQ29sb3JQaWNrZXIsWiBhcyBIc2xhU3RyaW5nQ29sb3JQaWNrZXIsaWUgYXMgSHN2Q29sb3JQaWNrZXIsZmUgYXMgSHN2U3RyaW5nQ29sb3JQaWNrZXIsYWUgYXMgSHN2YUNvbG9yUGlja2VyLHVlIGFzIEhzdmFTdHJpbmdDb2xvclBpY2tlcixwZSBhcyBSZ2JDb2xvclBpY2tlcixfZSBhcyBSZ2JTdHJpbmdDb2xvclBpY2tlcixkZSBhcyBSZ2JhQ29sb3JQaWNrZXIsbWUgYXMgUmdiYVN0cmluZ0NvbG9yUGlja2VyLFggYXMgc2V0Tm9uY2V9O1xuLy8jIHNvdXJjZU1hcHBpbmdVUkw9aW5kZXgubW9kdWxlLmpzLm1hcFxuIiwiaW1wb3J0IFJlYWN0LCB7dXNlQ2FsbGJhY2ssIHVzZU1lbW99IGZyb20gJ3JlYWN0JztcbmltcG9ydCB7XG4gICAgSHNsYUNvbG9yLFxuICAgIEhzbENvbG9yLFxuICAgIEhzdmFDb2xvcixcbiAgICBIc3ZDb2xvcixcbiAgICBSZ2JhQ29sb3IsXG4gICAgUmdiQ29sb3IsXG4gICAgSGV4Q29sb3JQaWNrZXIsXG4gICAgUmdiYUNvbG9yUGlja2VyLFxuICAgIFJnYmFTdHJpbmdDb2xvclBpY2tlcixcbiAgICBIc2xDb2xvclBpY2tlcixcbiAgICBIc2xTdHJpbmdDb2xvclBpY2tlcixcbiAgICBSZ2JDb2xvclBpY2tlcixcbiAgICBSZ2JTdHJpbmdDb2xvclBpY2tlcixcbiAgICBIc2xhQ29sb3JQaWNrZXIsXG4gICAgSHNsYVN0cmluZ0NvbG9yUGlja2VyLFxuICAgIEhzdkNvbG9yUGlja2VyLFxuICAgIEhzdmFTdHJpbmdDb2xvclBpY2tlcixcbiAgICBIc3ZhQ29sb3JQaWNrZXIsXG4gICAgSHN2U3RyaW5nQ29sb3JQaWNrZXIsXG59IGZyb20gJ3JlYWN0LWNvbG9yZnVsJztcblxuaW1wb3J0IHtcbiAgICBBbnlEaWN0LFxuICAgIENvbW1vblByZXNldHNQcm9wcyxcbiAgICBDb21tb25TdHlsZVByb3BzLFxuICAgIERhenpsZXJQcm9wcyxcbn0gZnJvbSAnLi4vLi4vLi4vY29tbW9ucy9qcy90eXBlcyc7XG5pbXBvcnQge2dldENvbW1vblN0eWxlcywgZ2V0UHJlc2V0c0NsYXNzTmFtZXMsIHRocm90dGxlfSBmcm9tICdjb21tb25zJztcbmltcG9ydCB7QW55Q29sb3J9IGZyb20gJ3JlYWN0LWNvbG9yZnVsL2Rpc3QvdHlwZXMnO1xuXG50eXBlIENvbG9yUGlja2VyUHJvcHMgPSB7XG4gICAgLyoqXG4gICAgICogQ3VycmVudCBjb2xvciB2YWx1ZVxuICAgICAqL1xuICAgIHZhbHVlPzogQW55Q29sb3I7XG4gICAgLyoqXG4gICAgICogVHlwZSBvZiBjb2xvclxuICAgICAqL1xuICAgIHR5cGU/OiAnaGV4JyB8ICdyZ2InIHwgJ3JnYmEnIHwgJ2hzbCcgfCAnaHNsYScgfCAnaHN2JyB8ICdoc3ZhJztcbiAgICAvKipcbiAgICAgKiBBZGQgYSB0b2dnbGUgYnV0dG9uIHRvIGFjdGl2YXRlIHRoZSBjb2xvciBwaWNrZXIuXG4gICAgICovXG4gICAgdG9nZ2xlYWJsZT86IGJvb2xlYW47XG4gICAgLyoqXG4gICAgICogQ29udGVudCBvZiB0aGUgdG9nZ2xlIGJ1dHRvbi5cbiAgICAgKi9cbiAgICB0b2dnbGVfYnV0dG9uPzogSlNYLkVsZW1lbnQ7XG4gICAgLyoqXG4gICAgICogQ2xvc2UgdGhlIGNvbG9yIHBpY2tlciB3aGVuIGEgdmFsdWUgaXMgc2VsZWN0ZWQuXG4gICAgICovXG4gICAgdG9nZ2xlX29uX2Nob29zZT86IGJvb2xlYW47XG4gICAgLyoqXG4gICAgICogRGVsYXkgYmVmb3JlIGNsb3NpbmcgdGhlIG1vZGFsIHdoZW4gdGhlXG4gICAgICovXG4gICAgdG9nZ2xlX29uX2Nob29zZV9kZWxheT86IG51bWJlcjtcbiAgICAvKipcbiAgICAgKiBEaXJlY3Rpb24gdG8gb3BlbiB0aGUgY29sb3IgcGlja2VyIG9uIHRvZ2dsZS5cbiAgICAgKi9cbiAgICB0b2dnbGVfZGlyZWN0aW9uPzpcbiAgICAgICAgfCAndG9wJ1xuICAgICAgICB8ICd0b3AtbGVmdCdcbiAgICAgICAgfCAndG9wLXJpZ2h0J1xuICAgICAgICB8ICdsZWZ0J1xuICAgICAgICB8ICdyaWdodCdcbiAgICAgICAgfCAnYm90dG9tJ1xuICAgICAgICB8ICdib3R0b20tbGVmdCdcbiAgICAgICAgfCAnYm90dG9tLXJpZ2h0JztcbiAgICAvKipcbiAgICAgKiBTaG93IHRoZSBjb2xvciBwaWNrZXIuXG4gICAgICovXG4gICAgYWN0aXZlPzogYm9vbGVhbjtcbiAgICAvKipcbiAgICAgKiBVc2UgYSBzcXVhcmUgd2l0aCBiYWNrZ3JvdW5kIGNvbG9yIGZyb20gdGhlIHZhbHVlIGFzIHRoZSB0b2dnbGUgYnV0dG9uLlxuICAgICAqL1xuICAgIHRvZ2dsZV9idXR0b25fY29sb3I/OiBib29sZWFuO1xuICAgIC8qKlxuICAgICAqIFRoZSB2YWx1ZSB3aWxsIGFsd2F5cyBiZSBhIHN0cmluZywgdXNhYmxlIGRpcmVjdGx5IGluIHN0eWxlcy5cbiAgICAgKlxuICAgICAqIGBgdG9nZ2xlX2J1dHRvbl9jb2xvcmBgIHJlcXVpcmVzIGEgc3RyaW5nIHZhbHVlIG9yIGhleCB0eXBlLlxuICAgICAqL1xuICAgIGFzX3N0cmluZz86IGJvb2xlYW47XG59ICYgQ29tbW9uU3R5bGVQcm9wcyAmXG4gICAgQ29tbW9uUHJlc2V0c1Byb3BzICZcbiAgICBEYXp6bGVyUHJvcHM7XG5cbi8qKlxuICogQSBjb2xvciBwaWNrZXIgcG93ZXJlZCBieSByZWFjdC1jb2xvcmZ1bFxuICpcbiAqIEEgdG9nZ2xlIGJ1dHRvbiBpcyBpbmNsdWRlZCBvciBjYW4gYmUgZGlzYWJsZWQgd2l0aCBgYHRvZ2dsZWFibGU9RmFsc2VgYFxuICogYW5kIHRoZW4gaXQgYmUgYWN0aXZhdGVkIGJ5IGJpbmRpbmcsIHRpZSBvciBpbml0aWFsIHZhbHVlLlxuICpcbiAqIENvbW1vbiBzdHlsZSBhc3BlY3RzIGdvZXMgb24gdGhlIGNvbnRhaW5lciBvZiB0aGUgcGlja2VyLCBoaWRkZW4gYnkgZGVmYXVsdC5cbiAqXG4gKiA6Q1NTOlxuICpcbiAqICAgICAgLSBgYGRhenpsZXItZXh0cmEtY29sb3ItcGlja2VyYGAgLSBUb3AgbGV2ZWwgY29udGFpbmVyXG4gKiAgICAgIC0gYGBkYXp6bGVyLWNvbG9yLXBpY2tlci10b2dnbGVgYCAtIFRvZ2dsZSBidXR0b25cbiAqICAgICAgLSBgYGRhenpsZXItY29sb3ItcGlja2VyYGAgLSBQaWNrZXIgY29udGFpbmVyLlxuICpcbiAqIC4uIGxpdGVyYWxpbmNsdWRlOjogLi4vLi4vdGVzdHMvY29tcG9uZW50cy9wYWdlcy9jb2xvcl9waWNrZXIucHlcbiAqL1xuY29uc3QgQ29sb3JQaWNrZXIgPSAocHJvcHM6IENvbG9yUGlja2VyUHJvcHMpID0+IHtcbiAgICBjb25zdCB7XG4gICAgICAgIGlkZW50aXR5LFxuICAgICAgICBjbGFzc19uYW1lLFxuICAgICAgICBzdHlsZSxcbiAgICAgICAgdHlwZSxcbiAgICAgICAgdG9nZ2xlYWJsZSxcbiAgICAgICAgdG9nZ2xlX2J1dHRvbixcbiAgICAgICAgdG9nZ2xlX29uX2Nob29zZSxcbiAgICAgICAgdG9nZ2xlX29uX2Nob29zZV9kZWxheSxcbiAgICAgICAgdG9nZ2xlX2J1dHRvbl9jb2xvcixcbiAgICAgICAgdG9nZ2xlX2RpcmVjdGlvbixcbiAgICAgICAgYWN0aXZlLFxuICAgICAgICB2YWx1ZSxcbiAgICAgICAgdXBkYXRlQXNwZWN0cyxcbiAgICAgICAgYXNfc3RyaW5nLFxuICAgICAgICAuLi5yZXN0XG4gICAgfSA9IHByb3BzO1xuICAgIGNvbnN0IGNzcyA9IHVzZU1lbW8oXG4gICAgICAgICgpID0+XG4gICAgICAgICAgICBnZXRQcmVzZXRzQ2xhc3NOYW1lcyhcbiAgICAgICAgICAgICAgICByZXN0LFxuICAgICAgICAgICAgICAgICdkYXp6bGVyLWNvbG9yLXBpY2tlcicsXG4gICAgICAgICAgICAgICAgYHRvZ2dsZS1kaXJlY3Rpb24tJHt0b2dnbGVfZGlyZWN0aW9uIGFzIHN0cmluZ31gXG4gICAgICAgICAgICApLFxuICAgICAgICBbcmVzdCwgYWN0aXZlXVxuICAgICk7XG5cbiAgICBjb25zdCBjbGFzc05hbWUgPSB1c2VNZW1vKCgpID0+IHtcbiAgICAgICAgY29uc3QgYyA9IFtjbGFzc19uYW1lXTtcbiAgICAgICAgaWYgKGFjdGl2ZSkge1xuICAgICAgICAgICAgYy5wdXNoKCdhY3RpdmUnKTtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gYy5qb2luKCcgJyk7XG4gICAgfSwgW2NsYXNzX25hbWUsIGFjdGl2ZV0pO1xuXG4gICAgY29uc3Qgc3R5bGluZyA9IHVzZU1lbW8oKCkgPT4gZ2V0Q29tbW9uU3R5bGVzKHJlc3QsIHN0eWxlKSwgW3Jlc3QsIHN0eWxlXSk7XG5cbiAgICBjb25zdCBhdXRvQ2xvc2UgPSB1c2VDYWxsYmFjayhcbiAgICAgICAgdGhyb3R0bGU8dm9pZD4oXG4gICAgICAgICAgICAoKSA9PiB1cGRhdGVBc3BlY3RzKHthY3RpdmU6IGZhbHNlfSksXG4gICAgICAgICAgICB0b2dnbGVfb25fY2hvb3NlX2RlbGF5LFxuICAgICAgICAgICAgdHJ1ZVxuICAgICAgICApLFxuICAgICAgICBbXVxuICAgICk7XG5cbiAgICBjb25zdCBwaWNrZXIgPSB1c2VNZW1vKCgpID0+IHtcbiAgICAgICAgY29uc3Qgb25DaGFuZ2UgPSAobmV3Q29sb3IpID0+IHtcbiAgICAgICAgICAgIGNvbnN0IHBheWxvYWQ6IEFueURpY3QgPSB7dmFsdWU6IG5ld0NvbG9yfTtcbiAgICAgICAgICAgIGlmICh0b2dnbGVfb25fY2hvb3NlKSB7XG4gICAgICAgICAgICAgICAgYXV0b0Nsb3NlKCk7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICB1cGRhdGVBc3BlY3RzKHBheWxvYWQpO1xuICAgICAgICB9O1xuICAgICAgICBzd2l0Y2ggKHR5cGUpIHtcbiAgICAgICAgICAgIGNhc2UgJ3JnYic6XG4gICAgICAgICAgICAgICAgaWYgKGFzX3N0cmluZykge1xuICAgICAgICAgICAgICAgICAgICByZXR1cm4gKFxuICAgICAgICAgICAgICAgICAgICAgICAgPFJnYlN0cmluZ0NvbG9yUGlja2VyXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgb25DaGFuZ2U9e29uQ2hhbmdlfVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGNvbG9yPXt2YWx1ZSBhcyBzdHJpbmd9XG4gICAgICAgICAgICAgICAgICAgICAgICAvPlxuICAgICAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICByZXR1cm4gKFxuICAgICAgICAgICAgICAgICAgICA8UmdiQ29sb3JQaWNrZXJcbiAgICAgICAgICAgICAgICAgICAgICAgIG9uQ2hhbmdlPXtvbkNoYW5nZX1cbiAgICAgICAgICAgICAgICAgICAgICAgIGNvbG9yPXt2YWx1ZSBhcyBSZ2JDb2xvcn1cbiAgICAgICAgICAgICAgICAgICAgLz5cbiAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgY2FzZSAncmdiYSc6XG4gICAgICAgICAgICAgICAgaWYgKGFzX3N0cmluZykge1xuICAgICAgICAgICAgICAgICAgICByZXR1cm4gKFxuICAgICAgICAgICAgICAgICAgICAgICAgPFJnYmFTdHJpbmdDb2xvclBpY2tlclxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIG9uQ2hhbmdlPXtvbkNoYW5nZX1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBjb2xvcj17dmFsdWUgYXMgc3RyaW5nfVxuICAgICAgICAgICAgICAgICAgICAgICAgLz5cbiAgICAgICAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgcmV0dXJuIChcbiAgICAgICAgICAgICAgICAgICAgPFJnYmFDb2xvclBpY2tlclxuICAgICAgICAgICAgICAgICAgICAgICAgb25DaGFuZ2U9e29uQ2hhbmdlfVxuICAgICAgICAgICAgICAgICAgICAgICAgY29sb3I9e3ZhbHVlIGFzIFJnYmFDb2xvcn1cbiAgICAgICAgICAgICAgICAgICAgLz5cbiAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgY2FzZSAnaHNsJzpcbiAgICAgICAgICAgICAgICBpZiAoYXNfc3RyaW5nKSB7XG4gICAgICAgICAgICAgICAgICAgIHJldHVybiAoXG4gICAgICAgICAgICAgICAgICAgICAgICA8SHNsU3RyaW5nQ29sb3JQaWNrZXJcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBvbkNoYW5nZT17b25DaGFuZ2V9XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgY29sb3I9e3ZhbHVlIGFzIHN0cmluZ31cbiAgICAgICAgICAgICAgICAgICAgICAgIC8+XG4gICAgICAgICAgICAgICAgICAgICk7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIHJldHVybiAoXG4gICAgICAgICAgICAgICAgICAgIDxIc2xDb2xvclBpY2tlclxuICAgICAgICAgICAgICAgICAgICAgICAgb25DaGFuZ2U9e29uQ2hhbmdlfVxuICAgICAgICAgICAgICAgICAgICAgICAgY29sb3I9e3ZhbHVlIGFzIEhzbENvbG9yfVxuICAgICAgICAgICAgICAgICAgICAvPlxuICAgICAgICAgICAgICAgICk7XG4gICAgICAgICAgICBjYXNlICdoc2xhJzpcbiAgICAgICAgICAgICAgICBpZiAoYXNfc3RyaW5nKSB7XG4gICAgICAgICAgICAgICAgICAgIHJldHVybiAoXG4gICAgICAgICAgICAgICAgICAgICAgICA8SHNsYVN0cmluZ0NvbG9yUGlja2VyXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgb25DaGFuZ2U9e29uQ2hhbmdlfVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGNvbG9yPXt2YWx1ZSBhcyBzdHJpbmd9XG4gICAgICAgICAgICAgICAgICAgICAgICAvPlxuICAgICAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICByZXR1cm4gKFxuICAgICAgICAgICAgICAgICAgICA8SHNsYUNvbG9yUGlja2VyXG4gICAgICAgICAgICAgICAgICAgICAgICBvbkNoYW5nZT17b25DaGFuZ2V9XG4gICAgICAgICAgICAgICAgICAgICAgICBjb2xvcj17dmFsdWUgYXMgSHNsYUNvbG9yfVxuICAgICAgICAgICAgICAgICAgICAvPlxuICAgICAgICAgICAgICAgICk7XG4gICAgICAgICAgICBjYXNlICdoc3YnOlxuICAgICAgICAgICAgICAgIGlmIChhc19zdHJpbmcpIHtcbiAgICAgICAgICAgICAgICAgICAgcmV0dXJuIChcbiAgICAgICAgICAgICAgICAgICAgICAgIDxIc3ZTdHJpbmdDb2xvclBpY2tlclxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIG9uQ2hhbmdlPXtvbkNoYW5nZX1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBjb2xvcj17dmFsdWUgYXMgc3RyaW5nfVxuICAgICAgICAgICAgICAgICAgICAgICAgLz5cbiAgICAgICAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgcmV0dXJuIChcbiAgICAgICAgICAgICAgICAgICAgPEhzdkNvbG9yUGlja2VyXG4gICAgICAgICAgICAgICAgICAgICAgICBvbkNoYW5nZT17b25DaGFuZ2V9XG4gICAgICAgICAgICAgICAgICAgICAgICBjb2xvcj17dmFsdWUgYXMgSHN2Q29sb3J9XG4gICAgICAgICAgICAgICAgICAgIC8+XG4gICAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgIGNhc2UgJ2hzdmEnOlxuICAgICAgICAgICAgICAgIGlmIChhc19zdHJpbmcpIHtcbiAgICAgICAgICAgICAgICAgICAgcmV0dXJuIChcbiAgICAgICAgICAgICAgICAgICAgICAgIDxIc3ZhU3RyaW5nQ29sb3JQaWNrZXJcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBvbkNoYW5nZT17b25DaGFuZ2V9XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgY29sb3I9e3ZhbHVlIGFzIHN0cmluZ31cbiAgICAgICAgICAgICAgICAgICAgICAgIC8+XG4gICAgICAgICAgICAgICAgICAgICk7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIHJldHVybiAoXG4gICAgICAgICAgICAgICAgICAgIDxIc3ZhQ29sb3JQaWNrZXJcbiAgICAgICAgICAgICAgICAgICAgICAgIG9uQ2hhbmdlPXtvbkNoYW5nZX1cbiAgICAgICAgICAgICAgICAgICAgICAgIGNvbG9yPXt2YWx1ZSBhcyBIc3ZhQ29sb3J9XG4gICAgICAgICAgICAgICAgICAgIC8+XG4gICAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgIGNhc2UgJ2hleCc6XG4gICAgICAgICAgICBkZWZhdWx0OlxuICAgICAgICAgICAgICAgIHJldHVybiAoXG4gICAgICAgICAgICAgICAgICAgIDxIZXhDb2xvclBpY2tlclxuICAgICAgICAgICAgICAgICAgICAgICAgb25DaGFuZ2U9e29uQ2hhbmdlfVxuICAgICAgICAgICAgICAgICAgICAgICAgY29sb3I9e3ZhbHVlIGFzIHN0cmluZ31cbiAgICAgICAgICAgICAgICAgICAgLz5cbiAgICAgICAgICAgICAgICApO1xuICAgICAgICB9XG4gICAgfSwgW1xuICAgICAgICB0eXBlLFxuICAgICAgICB2YWx1ZSxcbiAgICAgICAgdXBkYXRlQXNwZWN0cyxcbiAgICAgICAgdG9nZ2xlX29uX2Nob29zZSxcbiAgICAgICAgdG9nZ2xlX29uX2Nob29zZV9kZWxheSxcbiAgICAgICAgYXNfc3RyaW5nLFxuICAgIF0pO1xuXG4gICAgY29uc3QgdG9nZ2xlQnV0dG9uID0gdXNlTWVtbygoKSA9PiB7XG4gICAgICAgIGlmICh0b2dnbGVfYnV0dG9uX2NvbG9yKSB7XG4gICAgICAgICAgICByZXR1cm4gKFxuICAgICAgICAgICAgICAgIDxkaXZcbiAgICAgICAgICAgICAgICAgICAgY2xhc3NOYW1lPVwidG9nZ2xlLWJ1dHRvbi1jb2xvclwiXG4gICAgICAgICAgICAgICAgICAgIC8vIEB0cy1pZ25vcmVcbiAgICAgICAgICAgICAgICAgICAgc3R5bGU9e3tiYWNrZ3JvdW5kQ29sb3I6IHZhbHVlfX1cbiAgICAgICAgICAgICAgICAvPlxuICAgICAgICAgICAgKTtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gdG9nZ2xlX2J1dHRvbjtcbiAgICB9LCBbdG9nZ2xlX2J1dHRvbiwgdG9nZ2xlX2J1dHRvbl9jb2xvciwgdmFsdWVdKTtcblxuICAgIGNvbnN0IG9uVG9nZ2xlID0gdXNlQ2FsbGJhY2soKCkgPT4ge1xuICAgICAgICB1cGRhdGVBc3BlY3RzKHthY3RpdmU6ICFhY3RpdmV9KTtcbiAgICB9LCBbYWN0aXZlLCB1cGRhdGVBc3BlY3RzXSk7XG5cbiAgICByZXR1cm4gKFxuICAgICAgICA8ZGl2IGlkPXtpZGVudGl0eX0gY2xhc3NOYW1lPXtjbGFzc05hbWV9PlxuICAgICAgICAgICAge3RvZ2dsZWFibGUgJiYgKFxuICAgICAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiZGF6emxlci1jb2xvci1waWNrZXItdG9nZ2xlXCIgb25DbGljaz17b25Ub2dnbGV9PlxuICAgICAgICAgICAgICAgICAgICB7dG9nZ2xlQnV0dG9ufVxuICAgICAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgKX1cbiAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPXtjc3N9IHN0eWxlPXtzdHlsaW5nfT5cbiAgICAgICAgICAgICAgICB7cGlja2VyfVxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgIDwvZGl2PlxuICAgICk7XG59O1xuXG5Db2xvclBpY2tlci5kZWZhdWx0UHJvcHMgPSB7XG4gICAgdHlwZTogJ2hleCcsXG4gICAgdG9nZ2xlX2J1dHRvbjogJ/CfjqgnLFxuICAgIHRvZ2dsZWFibGU6IHRydWUsXG4gICAgdG9nZ2xlX29uX2Nob29zZTogdHJ1ZSxcbiAgICB0b2dnbGVfb25fY2hvb3NlX2RlbGF5OiAyNTAwLFxuICAgIHRvZ2dsZV9kaXJlY3Rpb246ICd0b3AtbGVmdCcsXG59O1xuXG5leHBvcnQgZGVmYXVsdCBDb2xvclBpY2tlcjtcbiIsImltcG9ydCBSZWFjdCBmcm9tICdyZWFjdCc7XG5pbXBvcnQge2pvaW4sIGNvbmNhdH0gZnJvbSAncmFtZGEnO1xuaW1wb3J0IHtDYXJldFByb3BzLCBEcmF3ZXJQcm9wc30gZnJvbSAnLi4vdHlwZXMnO1xuXG5jb25zdCBDYXJldCA9ICh7c2lkZSwgb3BlbmVkfTogQ2FyZXRQcm9wcykgPT4ge1xuICAgIHN3aXRjaCAoc2lkZSkge1xuICAgICAgICBjYXNlICd0b3AnOlxuICAgICAgICAgICAgcmV0dXJuIG9wZW5lZCA/IDxzcGFuPiYjOTY1MDs8L3NwYW4+IDogPHNwYW4+JiM5NjYwOzwvc3Bhbj47XG4gICAgICAgIGNhc2UgJ3JpZ2h0JzpcbiAgICAgICAgICAgIHJldHVybiBvcGVuZWQgPyA8c3Bhbj4mIzk2NTY7PC9zcGFuPiA6IDxzcGFuPiYjOTY2Njs8L3NwYW4+O1xuICAgICAgICBjYXNlICdsZWZ0JzpcbiAgICAgICAgICAgIHJldHVybiBvcGVuZWQgPyA8c3Bhbj4mIzk2NjY7PC9zcGFuPiA6IDxzcGFuPiYjOTY1Njs8L3NwYW4+O1xuICAgICAgICBjYXNlICdib3R0b20nOlxuICAgICAgICAgICAgcmV0dXJuIG9wZW5lZCA/IDxzcGFuPiYjOTY2MDs8L3NwYW4+IDogPHNwYW4+JiM5NjUwOzwvc3Bhbj47XG4gICAgICAgIGRlZmF1bHQ6XG4gICAgICAgICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG59O1xuXG4vKipcbiAqIERyYXcgY29udGVudCBmcm9tIHRoZSBzaWRlcyBvZiB0aGUgc2NyZWVuLlxuICpcbiAqIDpDU1M6XG4gKlxuICogICAgIC0gYGBkYXp6bGVyLWV4dHJhLWRyYXdlcmBgXG4gKiAgICAgLSBgYGRyYXdlci1jb250ZW50YGBcbiAqICAgICAtIGBgZHJhd2VyLWNvbnRyb2xgYFxuICogICAgIC0gYGB2ZXJ0aWNhbGBgXG4gKiAgICAgLSBgYGhvcml6b250YWxgYFxuICogICAgIC0gYGByaWdodGBgXG4gKiAgICAgLSBgYGJvdHRvbWBgXG4gKi9cbmNvbnN0IERyYXdlciA9IChwcm9wczogRHJhd2VyUHJvcHMpID0+IHtcbiAgICBjb25zdCB7Y2xhc3NfbmFtZSwgaWRlbnRpdHksIHN0eWxlLCBjaGlsZHJlbiwgb3BlbmVkLCBzaWRlLCB1cGRhdGVBc3BlY3RzfSA9XG4gICAgICAgIHByb3BzO1xuXG4gICAgY29uc3QgY3NzOiBzdHJpbmdbXSA9IFtzaWRlXTtcblxuICAgIGlmIChzaWRlID09PSAndG9wJyB8fCBzaWRlID09PSAnYm90dG9tJykge1xuICAgICAgICBjc3MucHVzaCgnaG9yaXpvbnRhbCcpO1xuICAgIH0gZWxzZSB7XG4gICAgICAgIGNzcy5wdXNoKCd2ZXJ0aWNhbCcpO1xuICAgIH1cblxuICAgIHJldHVybiAoXG4gICAgICAgIDxkaXZcbiAgICAgICAgICAgIGNsYXNzTmFtZT17am9pbignICcsIGNvbmNhdChjc3MsIFtjbGFzc19uYW1lXSkpfVxuICAgICAgICAgICAgaWQ9e2lkZW50aXR5fVxuICAgICAgICAgICAgc3R5bGU9e3N0eWxlfVxuICAgICAgICA+XG4gICAgICAgICAgICB7b3BlbmVkICYmIChcbiAgICAgICAgICAgICAgICA8ZGl2IGNsYXNzTmFtZT17am9pbignICcsIGNvbmNhdChjc3MsIFsnZHJhd2VyLWNvbnRlbnQnXSkpfT5cbiAgICAgICAgICAgICAgICAgICAge2NoaWxkcmVufVxuICAgICAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgKX1cbiAgICAgICAgICAgIDxkaXZcbiAgICAgICAgICAgICAgICBjbGFzc05hbWU9e2pvaW4oJyAnLCBjb25jYXQoY3NzLCBbJ2RyYXdlci1jb250cm9sJ10pKX1cbiAgICAgICAgICAgICAgICBvbkNsaWNrPXsoKSA9PiB1cGRhdGVBc3BlY3RzKHtvcGVuZWQ6ICFvcGVuZWR9KX1cbiAgICAgICAgICAgID5cbiAgICAgICAgICAgICAgICA8Q2FyZXQgb3BlbmVkPXtvcGVuZWR9IHNpZGU9e3NpZGV9IC8+XG4gICAgICAgICAgICA8L2Rpdj5cbiAgICAgICAgPC9kaXY+XG4gICAgKTtcbn07XG5cbkRyYXdlci5kZWZhdWx0UHJvcHMgPSB7XG4gICAgc2lkZTogJ3RvcCcsXG59O1xuXG5leHBvcnQgZGVmYXVsdCBEcmF3ZXI7XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IHt0aW1lc3RhbXBQcm9wfSBmcm9tICdjb21tb25zJztcbmltcG9ydCB7bWVyZ2V9IGZyb20gJ3JhbWRhJztcbmltcG9ydCB7Tm90aWNlUHJvcHN9IGZyb20gJy4uL3R5cGVzJztcblxuLyoqXG4gKiBCcm93c2VyIG5vdGlmaWNhdGlvbnMgd2l0aCBwZXJtaXNzaW9ucyBoYW5kbGluZy5cbiAqL1xuZXhwb3J0IGRlZmF1bHQgY2xhc3MgTm90aWNlIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50PE5vdGljZVByb3BzPiB7XG4gICAgY29uc3RydWN0b3IocHJvcHMpIHtcbiAgICAgICAgc3VwZXIocHJvcHMpO1xuICAgICAgICB0aGlzLnN0YXRlID0ge1xuICAgICAgICAgICAgbGFzdE1lc3NhZ2U6IHByb3BzLmJvZHksXG4gICAgICAgICAgICBub3RpZmljYXRpb246IG51bGwsXG4gICAgICAgIH07XG4gICAgICAgIHRoaXMub25QZXJtaXNzaW9uID0gdGhpcy5vblBlcm1pc3Npb24uYmluZCh0aGlzKTtcbiAgICB9XG5cbiAgICBjb21wb25lbnREaWRNb3VudCgpIHtcbiAgICAgICAgY29uc3Qge3VwZGF0ZUFzcGVjdHN9ID0gdGhpcy5wcm9wcztcbiAgICAgICAgaWYgKCEoJ05vdGlmaWNhdGlvbicgaW4gd2luZG93KSAmJiB1cGRhdGVBc3BlY3RzKSB7XG4gICAgICAgICAgICB1cGRhdGVBc3BlY3RzKHtwZXJtaXNzaW9uOiAndW5zdXBwb3J0ZWQnfSk7XG4gICAgICAgIH0gZWxzZSBpZiAoTm90aWZpY2F0aW9uLnBlcm1pc3Npb24gPT09ICdkZWZhdWx0Jykge1xuICAgICAgICAgICAgTm90aWZpY2F0aW9uLnJlcXVlc3RQZXJtaXNzaW9uKCkudGhlbih0aGlzLm9uUGVybWlzc2lvbik7XG4gICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICB0aGlzLm9uUGVybWlzc2lvbih3aW5kb3cuTm90aWZpY2F0aW9uLnBlcm1pc3Npb24pO1xuICAgICAgICB9XG4gICAgfVxuXG4gICAgY29tcG9uZW50RGlkVXBkYXRlKHByZXZQcm9wcykge1xuICAgICAgICBpZiAoIXByZXZQcm9wcy5kaXNwbGF5ZWQgJiYgdGhpcy5wcm9wcy5kaXNwbGF5ZWQpIHtcbiAgICAgICAgICAgIHRoaXMuc2VuZE5vdGlmaWNhdGlvbih0aGlzLnByb3BzLnBlcm1pc3Npb24pO1xuICAgICAgICB9XG4gICAgfVxuXG4gICAgc2VuZE5vdGlmaWNhdGlvbihwZXJtaXNzaW9uKSB7XG4gICAgICAgIGNvbnN0IHtcbiAgICAgICAgICAgIHVwZGF0ZUFzcGVjdHMsXG4gICAgICAgICAgICBib2R5LFxuICAgICAgICAgICAgdGl0bGUsXG4gICAgICAgICAgICBpY29uLFxuICAgICAgICAgICAgcmVxdWlyZV9pbnRlcmFjdGlvbixcbiAgICAgICAgICAgIGxhbmcsXG4gICAgICAgICAgICBiYWRnZSxcbiAgICAgICAgICAgIHRhZyxcbiAgICAgICAgICAgIGltYWdlLFxuICAgICAgICAgICAgdmlicmF0ZSxcbiAgICAgICAgfSA9IHRoaXMucHJvcHM7XG4gICAgICAgIGlmIChwZXJtaXNzaW9uID09PSAnZ3JhbnRlZCcpIHtcbiAgICAgICAgICAgIGNvbnN0IG9wdGlvbnMgPSB7XG4gICAgICAgICAgICAgICAgcmVxdWlyZUludGVyYWN0aW9uOiByZXF1aXJlX2ludGVyYWN0aW9uLFxuICAgICAgICAgICAgICAgIGJvZHksXG4gICAgICAgICAgICAgICAgaWNvbixcbiAgICAgICAgICAgICAgICBsYW5nLFxuICAgICAgICAgICAgICAgIGJhZGdlLFxuICAgICAgICAgICAgICAgIHRhZyxcbiAgICAgICAgICAgICAgICBpbWFnZSxcbiAgICAgICAgICAgICAgICB2aWJyYXRlLFxuICAgICAgICAgICAgfTtcbiAgICAgICAgICAgIGNvbnN0IG5vdGlmaWNhdGlvbiA9IG5ldyBOb3RpZmljYXRpb24odGl0bGUsIG9wdGlvbnMpO1xuICAgICAgICAgICAgbm90aWZpY2F0aW9uLm9uY2xpY2sgPSAoKSA9PiB7XG4gICAgICAgICAgICAgICAgaWYgKHVwZGF0ZUFzcGVjdHMpIHtcbiAgICAgICAgICAgICAgICAgICAgdXBkYXRlQXNwZWN0cyhcbiAgICAgICAgICAgICAgICAgICAgICAgIG1lcmdlKFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHtkaXNwbGF5ZWQ6IGZhbHNlfSxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB0aW1lc3RhbXBQcm9wKCdjbGlja3MnLCB0aGlzLnByb3BzLmNsaWNrcyArIDEpXG4gICAgICAgICAgICAgICAgICAgICAgICApXG4gICAgICAgICAgICAgICAgICAgICk7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfTtcbiAgICAgICAgICAgIG5vdGlmaWNhdGlvbi5vbmNsb3NlID0gKCkgPT4ge1xuICAgICAgICAgICAgICAgIGlmICh1cGRhdGVBc3BlY3RzKSB7XG4gICAgICAgICAgICAgICAgICAgIHVwZGF0ZUFzcGVjdHMoXG4gICAgICAgICAgICAgICAgICAgICAgICBtZXJnZShcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB7ZGlzcGxheWVkOiBmYWxzZX0sXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgdGltZXN0YW1wUHJvcCgnY2xvc2VzJywgdGhpcy5wcm9wcy5jbG9zZXMgKyAxKVxuICAgICAgICAgICAgICAgICAgICAgICAgKVxuICAgICAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH07XG4gICAgICAgIH1cbiAgICB9XG5cbiAgICBvblBlcm1pc3Npb24ocGVybWlzc2lvbikge1xuICAgICAgICBjb25zdCB7ZGlzcGxheWVkLCB1cGRhdGVBc3BlY3RzfSA9IHRoaXMucHJvcHM7XG4gICAgICAgIGlmICh1cGRhdGVBc3BlY3RzKSB7XG4gICAgICAgICAgICB1cGRhdGVBc3BlY3RzKHtwZXJtaXNzaW9ufSk7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKGRpc3BsYXllZCkge1xuICAgICAgICAgICAgdGhpcy5zZW5kTm90aWZpY2F0aW9uKHBlcm1pc3Npb24pO1xuICAgICAgICB9XG4gICAgfVxuXG4gICAgcmVuZGVyKCkge1xuICAgICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG5cbiAgICBzdGF0aWMgZGVmYXVsdFByb3BzOiB7XG4gICAgICAgIHJlcXVpcmVfaW50ZXJhY3Rpb246IGZhbHNlO1xuICAgICAgICBjbGlja3M6IDA7XG4gICAgICAgIGNsaWNrc190aW1lc3RhbXA6IC0xO1xuICAgICAgICBjbG9zZXM6IDA7XG4gICAgICAgIGNsb3Nlc190aW1lc3RhbXA6IC0xO1xuICAgIH07XG59XG4iLCJpbXBvcnQgUmVhY3QsIHt1c2VFZmZlY3QsIHVzZVN0YXRlfSBmcm9tICdyZWFjdCc7XG5pbXBvcnQge0RhenpsZXJQcm9wc30gZnJvbSAnLi4vLi4vLi4vY29tbW9ucy9qcy90eXBlcyc7XG5cbi8qKlxuICogTGlzdCBvZiBsaW5rcyB0byBvdGhlciBwYWdlIGluIHRoZSBhcHAuXG4gKlxuICogOkNTUzpcbiAqXG4gKiAgICAgLSBgYGRhenpsZXItZXh0cmEtcGFnZS1tYXBgYFxuICovXG5jb25zdCBQYWdlTWFwID0gKHByb3BzOiBEYXp6bGVyUHJvcHMpID0+IHtcbiAgICBjb25zdCB7Y2xhc3NfbmFtZSwgc3R5bGUsIGlkZW50aXR5fSA9IHByb3BzO1xuICAgIGNvbnN0IFtwYWdlTWFwLCBzZXRQYWdlTWFwXSA9IHVzZVN0YXRlKG51bGwpO1xuXG4gICAgdXNlRWZmZWN0KCgpID0+IHtcbiAgICAgICAgLy8gQHRzLWlnbm9yZVxuICAgICAgICBmZXRjaChgJHt3aW5kb3cuZGF6emxlcl9iYXNlX3VybH0vZGF6emxlci9wYWdlLW1hcGApLnRoZW4oKHJlcCkgPT5cbiAgICAgICAgICAgIHJlcC5qc29uKCkudGhlbihzZXRQYWdlTWFwKVxuICAgICAgICApO1xuICAgIH0sIFtdKTtcblxuICAgIHJldHVybiAoXG4gICAgICAgIDx1bCBjbGFzc05hbWU9e2NsYXNzX25hbWV9IHN0eWxlPXtzdHlsZX0gaWQ9e2lkZW50aXR5fT5cbiAgICAgICAgICAgIHtwYWdlTWFwICYmXG4gICAgICAgICAgICAgICAgcGFnZU1hcC5tYXAoKHBhZ2UpID0+IChcbiAgICAgICAgICAgICAgICAgICAgPGxpIGtleT17cGFnZS5uYW1lfT5cbiAgICAgICAgICAgICAgICAgICAgICAgIDxhIGhyZWY9e3BhZ2UudXJsfT57cGFnZS50aXRsZX08L2E+XG4gICAgICAgICAgICAgICAgICAgIDwvbGk+XG4gICAgICAgICAgICAgICAgKSl9XG4gICAgICAgIDwvdWw+XG4gICAgKTtcbn07XG5cblBhZ2VNYXAuZGVmYXVsdFByb3BzID0ge307XG5cbmV4cG9ydCBkZWZhdWx0IFBhZ2VNYXA7XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IHtyYW5nZSwgam9pbn0gZnJvbSAncmFtZGEnO1xuaW1wb3J0IHtQYWdlclBhZ2VQcm9wcywgUGFnZXJQcm9wcywgUGFnZXJTdGF0ZX0gZnJvbSAnLi4vdHlwZXMnO1xuXG5jb25zdCBzdGFydE9mZnNldCA9IChwYWdlLCBpdGVtUGVyUGFnZSkgPT5cbiAgICAocGFnZSAtIDEpICogKHBhZ2UgPiAxID8gaXRlbVBlclBhZ2UgOiAwKTtcblxuY29uc3QgZW5kT2Zmc2V0ID0gKHN0YXJ0LCBpdGVtUGVyUGFnZSwgcGFnZSwgdG90YWwsIGxlZnRPdmVyKSA9PlxuICAgIHBhZ2UgIT09IHRvdGFsXG4gICAgICAgID8gc3RhcnQgKyBpdGVtUGVyUGFnZVxuICAgICAgICA6IGxlZnRPdmVyICE9PSAwXG4gICAgICAgID8gc3RhcnQgKyBsZWZ0T3ZlclxuICAgICAgICA6IHN0YXJ0ICsgaXRlbVBlclBhZ2U7XG5cbmNvbnN0IHNob3dMaXN0ID0gKHBhZ2UsIHRvdGFsLCBuKSA9PiB7XG4gICAgaWYgKHRvdGFsID4gbikge1xuICAgICAgICBjb25zdCBtaWRkbGUgPSBuIC8gMjtcbiAgICAgICAgY29uc3QgZmlyc3QgPVxuICAgICAgICAgICAgcGFnZSA+PSB0b3RhbCAtIG1pZGRsZVxuICAgICAgICAgICAgICAgID8gdG90YWwgLSBuICsgMVxuICAgICAgICAgICAgICAgIDogcGFnZSA+IG1pZGRsZVxuICAgICAgICAgICAgICAgID8gcGFnZSAtIG1pZGRsZVxuICAgICAgICAgICAgICAgIDogMTtcbiAgICAgICAgY29uc3QgbGFzdCA9IHBhZ2UgPCB0b3RhbCAtIG1pZGRsZSA/IGZpcnN0ICsgbiA6IHRvdGFsICsgMTtcbiAgICAgICAgcmV0dXJuIHJhbmdlKGZpcnN0LCBsYXN0KTtcbiAgICB9XG4gICAgcmV0dXJuIHJhbmdlKDEsIHRvdGFsICsgMSk7XG59O1xuXG5jb25zdCBQYWdlID0gKHtzdHlsZSwgY2xhc3NfbmFtZSwgb25fY2hhbmdlLCB0ZXh0LCBwYWdlfTogUGFnZXJQYWdlUHJvcHMpID0+IChcbiAgICA8c3BhbiBzdHlsZT17c3R5bGV9IGNsYXNzTmFtZT17Y2xhc3NfbmFtZX0gb25DbGljaz17KCkgPT4gb25fY2hhbmdlKHBhZ2UpfT5cbiAgICAgICAge3RleHQgfHwgcGFnZX1cbiAgICA8L3NwYW4+XG4pO1xuXG4vKipcbiAqIFBhZ2luZyBmb3IgZGF6emxlciBhcHBzLlxuICpcbiAqIDpDU1M6XG4gKlxuICogICAgIC0gYGBkYXp6bGVyLWV4dHJhLXBhZ2VyYGBcbiAqICAgICAtIGBgcGFnZWBgXG4gKi9cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIFBhZ2VyIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50PFBhZ2VyUHJvcHMsIFBhZ2VyU3RhdGU+IHtcbiAgICBjb25zdHJ1Y3Rvcihwcm9wcykge1xuICAgICAgICBzdXBlcihwcm9wcyk7XG4gICAgICAgIHRoaXMuc3RhdGUgPSB7XG4gICAgICAgICAgICBjdXJyZW50X3BhZ2U6IG51bGwsXG4gICAgICAgICAgICBzdGFydF9vZmZzZXQ6IG51bGwsXG4gICAgICAgICAgICBlbmRfb2Zmc2V0OiBudWxsLFxuICAgICAgICAgICAgcGFnZXM6IFtdLFxuICAgICAgICAgICAgdG90YWxfcGFnZXM6IE1hdGguY2VpbChwcm9wcy50b3RhbF9pdGVtcyAvIHByb3BzLml0ZW1zX3Blcl9wYWdlKSxcbiAgICAgICAgfTtcbiAgICAgICAgdGhpcy5vbkNoYW5nZVBhZ2UgPSB0aGlzLm9uQ2hhbmdlUGFnZS5iaW5kKHRoaXMpO1xuICAgIH1cblxuICAgIFVOU0FGRV9jb21wb25lbnRXaWxsTW91bnQoKSB7XG4gICAgICAgIHRoaXMub25DaGFuZ2VQYWdlKHRoaXMucHJvcHMuY3VycmVudF9wYWdlKTtcbiAgICB9XG5cbiAgICBvbkNoYW5nZVBhZ2UocGFnZSkge1xuICAgICAgICBjb25zdCB7aXRlbXNfcGVyX3BhZ2UsIHRvdGFsX2l0ZW1zLCB1cGRhdGVBc3BlY3RzLCBwYWdlc19kaXNwbGF5ZWR9ID1cbiAgICAgICAgICAgIHRoaXMucHJvcHM7XG4gICAgICAgIGNvbnN0IHt0b3RhbF9wYWdlc30gPSB0aGlzLnN0YXRlO1xuXG4gICAgICAgIGNvbnN0IHN0YXJ0X29mZnNldCA9IHN0YXJ0T2Zmc2V0KHBhZ2UsIGl0ZW1zX3Blcl9wYWdlKTtcbiAgICAgICAgY29uc3QgbGVmdE92ZXIgPSB0b3RhbF9pdGVtcyAlIGl0ZW1zX3Blcl9wYWdlO1xuXG4gICAgICAgIGNvbnN0IGVuZF9vZmZzZXQgPSBlbmRPZmZzZXQoXG4gICAgICAgICAgICBzdGFydF9vZmZzZXQsXG4gICAgICAgICAgICBpdGVtc19wZXJfcGFnZSxcbiAgICAgICAgICAgIHBhZ2UsXG4gICAgICAgICAgICB0b3RhbF9wYWdlcyxcbiAgICAgICAgICAgIGxlZnRPdmVyXG4gICAgICAgICk7XG5cbiAgICAgICAgY29uc3QgcGF5bG9hZDogUGFnZXJTdGF0ZSA9IHtcbiAgICAgICAgICAgIGN1cnJlbnRfcGFnZTogcGFnZSxcbiAgICAgICAgICAgIHN0YXJ0X29mZnNldDogc3RhcnRfb2Zmc2V0LFxuICAgICAgICAgICAgZW5kX29mZnNldDogZW5kX29mZnNldCxcbiAgICAgICAgICAgIHBhZ2VzOiBzaG93TGlzdChwYWdlLCB0b3RhbF9wYWdlcywgcGFnZXNfZGlzcGxheWVkKSxcbiAgICAgICAgfTtcbiAgICAgICAgdGhpcy5zZXRTdGF0ZShwYXlsb2FkKTtcblxuICAgICAgICBpZiAodXBkYXRlQXNwZWN0cykge1xuICAgICAgICAgICAgaWYgKHRoaXMuc3RhdGUudG90YWxfcGFnZXMgIT09IHRoaXMucHJvcHMudG90YWxfcGFnZXMpIHtcbiAgICAgICAgICAgICAgICBwYXlsb2FkLnRvdGFsX3BhZ2VzID0gdGhpcy5zdGF0ZS50b3RhbF9wYWdlcztcbiAgICAgICAgICAgIH1cbiAgICAgICAgICAgIHVwZGF0ZUFzcGVjdHMocGF5bG9hZCk7XG4gICAgICAgIH1cbiAgICB9XG5cbiAgICBVTlNBRkVfY29tcG9uZW50V2lsbFJlY2VpdmVQcm9wcyhwcm9wcykge1xuICAgICAgICBpZiAocHJvcHMuY3VycmVudF9wYWdlICE9PSB0aGlzLnN0YXRlLmN1cnJlbnRfcGFnZSkge1xuICAgICAgICAgICAgdGhpcy5vbkNoYW5nZVBhZ2UocHJvcHMuY3VycmVudF9wYWdlKTtcbiAgICAgICAgfVxuICAgIH1cblxuICAgIHJlbmRlcigpIHtcbiAgICAgICAgY29uc3Qge2N1cnJlbnRfcGFnZSwgcGFnZXMsIHRvdGFsX3BhZ2VzfSA9IHRoaXMuc3RhdGU7XG4gICAgICAgIGNvbnN0IHtjbGFzc19uYW1lLCBpZGVudGl0eSwgcGFnZV9zdHlsZSwgcGFnZV9jbGFzc19uYW1lfSA9IHRoaXMucHJvcHM7XG5cbiAgICAgICAgY29uc3QgY3NzOiBzdHJpbmdbXSA9IFsncGFnZSddO1xuICAgICAgICBpZiAocGFnZV9jbGFzc19uYW1lKSB7XG4gICAgICAgICAgICBjc3MucHVzaChwYWdlX2NsYXNzX25hbWUpO1xuICAgICAgICB9XG4gICAgICAgIGNvbnN0IHBhZ2VDc3MgPSBqb2luKCcgJywgY3NzKTtcblxuICAgICAgICByZXR1cm4gKFxuICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9e2NsYXNzX25hbWV9IGlkPXtpZGVudGl0eX0+XG4gICAgICAgICAgICAgICAge2N1cnJlbnRfcGFnZSA+IDEgJiYgKFxuICAgICAgICAgICAgICAgICAgICA8UGFnZVxuICAgICAgICAgICAgICAgICAgICAgICAgcGFnZT17MX1cbiAgICAgICAgICAgICAgICAgICAgICAgIHRleHQ9eydmaXJzdCd9XG4gICAgICAgICAgICAgICAgICAgICAgICBzdHlsZT17cGFnZV9zdHlsZX1cbiAgICAgICAgICAgICAgICAgICAgICAgIGNsYXNzX25hbWU9e3BhZ2VDc3N9XG4gICAgICAgICAgICAgICAgICAgICAgICBvbl9jaGFuZ2U9e3RoaXMub25DaGFuZ2VQYWdlfVxuICAgICAgICAgICAgICAgICAgICAvPlxuICAgICAgICAgICAgICAgICl9XG4gICAgICAgICAgICAgICAge2N1cnJlbnRfcGFnZSA+IDEgJiYgKFxuICAgICAgICAgICAgICAgICAgICA8UGFnZVxuICAgICAgICAgICAgICAgICAgICAgICAgcGFnZT17Y3VycmVudF9wYWdlIC0gMX1cbiAgICAgICAgICAgICAgICAgICAgICAgIHRleHQ9eydwcmV2aW91cyd9XG4gICAgICAgICAgICAgICAgICAgICAgICBzdHlsZT17cGFnZV9zdHlsZX1cbiAgICAgICAgICAgICAgICAgICAgICAgIGNsYXNzX25hbWU9e3BhZ2VDc3N9XG4gICAgICAgICAgICAgICAgICAgICAgICBvbl9jaGFuZ2U9e3RoaXMub25DaGFuZ2VQYWdlfVxuICAgICAgICAgICAgICAgICAgICAvPlxuICAgICAgICAgICAgICAgICl9XG4gICAgICAgICAgICAgICAge3BhZ2VzLm1hcCgoZSkgPT4gKFxuICAgICAgICAgICAgICAgICAgICA8UGFnZVxuICAgICAgICAgICAgICAgICAgICAgICAgcGFnZT17ZX1cbiAgICAgICAgICAgICAgICAgICAgICAgIGtleT17YHBhZ2UtJHtlfWB9XG4gICAgICAgICAgICAgICAgICAgICAgICBzdHlsZT17cGFnZV9zdHlsZX1cbiAgICAgICAgICAgICAgICAgICAgICAgIGNsYXNzX25hbWU9e3BhZ2VDc3N9XG4gICAgICAgICAgICAgICAgICAgICAgICBvbl9jaGFuZ2U9e3RoaXMub25DaGFuZ2VQYWdlfVxuICAgICAgICAgICAgICAgICAgICAvPlxuICAgICAgICAgICAgICAgICkpfVxuICAgICAgICAgICAgICAgIHtjdXJyZW50X3BhZ2UgPCB0b3RhbF9wYWdlcyAmJiAoXG4gICAgICAgICAgICAgICAgICAgIDxQYWdlXG4gICAgICAgICAgICAgICAgICAgICAgICBwYWdlPXtjdXJyZW50X3BhZ2UgKyAxfVxuICAgICAgICAgICAgICAgICAgICAgICAgdGV4dD17J25leHQnfVxuICAgICAgICAgICAgICAgICAgICAgICAgc3R5bGU9e3BhZ2Vfc3R5bGV9XG4gICAgICAgICAgICAgICAgICAgICAgICBjbGFzc19uYW1lPXtwYWdlQ3NzfVxuICAgICAgICAgICAgICAgICAgICAgICAgb25fY2hhbmdlPXt0aGlzLm9uQ2hhbmdlUGFnZX1cbiAgICAgICAgICAgICAgICAgICAgLz5cbiAgICAgICAgICAgICAgICApfVxuICAgICAgICAgICAgICAgIHtjdXJyZW50X3BhZ2UgPCB0b3RhbF9wYWdlcyAmJiAoXG4gICAgICAgICAgICAgICAgICAgIDxQYWdlXG4gICAgICAgICAgICAgICAgICAgICAgICBwYWdlPXt0b3RhbF9wYWdlc31cbiAgICAgICAgICAgICAgICAgICAgICAgIHRleHQ9eydsYXN0J31cbiAgICAgICAgICAgICAgICAgICAgICAgIHN0eWxlPXtwYWdlX3N0eWxlfVxuICAgICAgICAgICAgICAgICAgICAgICAgY2xhc3NfbmFtZT17cGFnZUNzc31cbiAgICAgICAgICAgICAgICAgICAgICAgIG9uX2NoYW5nZT17dGhpcy5vbkNoYW5nZVBhZ2V9XG4gICAgICAgICAgICAgICAgICAgIC8+XG4gICAgICAgICAgICAgICAgKX1cbiAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICApO1xuICAgIH1cbiAgICBzdGF0aWMgZGVmYXVsdFByb3BzID0ge1xuICAgICAgICBjdXJyZW50X3BhZ2U6IDEsXG4gICAgICAgIGl0ZW1zX3Blcl9wYWdlOiAxMCxcbiAgICAgICAgcGFnZXNfZGlzcGxheWVkOiAxMCxcbiAgICB9O1xufVxuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCB7UG9wVXBQcm9wc30gZnJvbSAnLi4vdHlwZXMnO1xuXG5mdW5jdGlvbiBnZXRNb3VzZVgoZSwgcG9wdXApIHtcbiAgICByZXR1cm4gKFxuICAgICAgICBlLmNsaWVudFggLVxuICAgICAgICBlLnRhcmdldC5nZXRCb3VuZGluZ0NsaWVudFJlY3QoKS5sZWZ0IC1cbiAgICAgICAgcG9wdXAuZ2V0Qm91bmRpbmdDbGllbnRSZWN0KCkud2lkdGggLyAyXG4gICAgKTtcbn1cblxudHlwZSBQb3BVcFN0YXRlID0ge1xuICAgIHBvcz86IG51bWJlcjtcbn07XG5cbi8qKlxuICogV3JhcHMgYSBjb21wb25lbnQvdGV4dCB0byByZW5kZXIgYSBwb3B1cCB3aGVuIGhvdmVyaW5nXG4gKiBvdmVyIHRoZSBjaGlsZHJlbiBvciBjbGlja2luZyBvbiBpdC5cbiAqXG4gKiA6Q1NTOlxuICpcbiAqICAgICAtIGBgZGF6emxlci1leHRyYS1wb3AtdXBgYFxuICogICAgIC0gYGBwb3B1cC1jb250ZW50YGBcbiAqICAgICAtIGBgdmlzaWJsZWBgXG4gKi9cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIFBvcFVwIGV4dGVuZHMgUmVhY3QuQ29tcG9uZW50PFBvcFVwUHJvcHMsIFBvcFVwU3RhdGU+IHtcbiAgICBwb3B1cFJlZj86IGFueTtcblxuICAgIGNvbnN0cnVjdG9yKHByb3BzKSB7XG4gICAgICAgIHN1cGVyKHByb3BzKTtcbiAgICAgICAgdGhpcy5zdGF0ZSA9IHtcbiAgICAgICAgICAgIHBvczogbnVsbCxcbiAgICAgICAgfTtcbiAgICB9XG4gICAgcmVuZGVyKCkge1xuICAgICAgICBjb25zdCB7XG4gICAgICAgICAgICBjbGFzc19uYW1lLFxuICAgICAgICAgICAgc3R5bGUsXG4gICAgICAgICAgICBpZGVudGl0eSxcbiAgICAgICAgICAgIGNoaWxkcmVuLFxuICAgICAgICAgICAgY29udGVudCxcbiAgICAgICAgICAgIG1vZGUsXG4gICAgICAgICAgICB1cGRhdGVBc3BlY3RzLFxuICAgICAgICAgICAgYWN0aXZlLFxuICAgICAgICAgICAgY29udGVudF9zdHlsZSxcbiAgICAgICAgICAgIGNoaWxkcmVuX3N0eWxlLFxuICAgICAgICB9ID0gdGhpcy5wcm9wcztcblxuICAgICAgICByZXR1cm4gKFxuICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9e2NsYXNzX25hbWV9IHN0eWxlPXtzdHlsZX0gaWQ9e2lkZW50aXR5fT5cbiAgICAgICAgICAgICAgICA8ZGl2XG4gICAgICAgICAgICAgICAgICAgIGNsYXNzTmFtZT17J3BvcHVwLWNvbnRlbnQnICsgKGFjdGl2ZSA/ICcgdmlzaWJsZScgOiAnJyl9XG4gICAgICAgICAgICAgICAgICAgIHN0eWxlPXt7XG4gICAgICAgICAgICAgICAgICAgICAgICAuLi4oY29udGVudF9zdHlsZSB8fCB7fSksXG4gICAgICAgICAgICAgICAgICAgICAgICBsZWZ0OiB0aGlzLnN0YXRlLnBvcyB8fCAwLFxuICAgICAgICAgICAgICAgICAgICB9fVxuICAgICAgICAgICAgICAgICAgICByZWY9eyhyKSA9PiAodGhpcy5wb3B1cFJlZiA9IHIpfVxuICAgICAgICAgICAgICAgID5cbiAgICAgICAgICAgICAgICAgICAge2NvbnRlbnR9XG4gICAgICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgICAgICAgPGRpdlxuICAgICAgICAgICAgICAgICAgICBjbGFzc05hbWU9XCJwb3B1cC1jaGlsZHJlblwiXG4gICAgICAgICAgICAgICAgICAgIG9uTW91c2VFbnRlcj17KGUpID0+IHtcbiAgICAgICAgICAgICAgICAgICAgICAgIGlmIChtb2RlID09PSAnaG92ZXInKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy5zZXRTdGF0ZShcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAge3BvczogZ2V0TW91c2VYKGUsIHRoaXMucG9wdXBSZWYpfSxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgKCkgPT4gdXBkYXRlQXNwZWN0cyh7YWN0aXZlOiB0cnVlfSlcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgICAgICB9fVxuICAgICAgICAgICAgICAgICAgICBvbk1vdXNlTGVhdmU9eygpID0+XG4gICAgICAgICAgICAgICAgICAgICAgICBtb2RlID09PSAnaG92ZXInICYmIHVwZGF0ZUFzcGVjdHMoe2FjdGl2ZTogZmFsc2V9KVxuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgIG9uQ2xpY2s9eyhlKSA9PiB7XG4gICAgICAgICAgICAgICAgICAgICAgICBpZiAobW9kZSA9PT0gJ2NsaWNrJykge1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMuc2V0U3RhdGUoXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHtwb3M6IGdldE1vdXNlWChlLCB0aGlzLnBvcHVwUmVmKX0sXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICgpID0+IHVwZGF0ZUFzcGVjdHMoe2FjdGl2ZTogIWFjdGl2ZX0pXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgfX1cbiAgICAgICAgICAgICAgICAgICAgc3R5bGU9e2NoaWxkcmVuX3N0eWxlfVxuICAgICAgICAgICAgICAgID5cbiAgICAgICAgICAgICAgICAgICAge2NoaWxkcmVufVxuICAgICAgICAgICAgICAgIDwvZGl2PlxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICk7XG4gICAgfVxuXG4gICAgc3RhdGljIGRlZmF1bHRQcm9wcyA9IHtcbiAgICAgICAgbW9kZTogJ2hvdmVyJyxcbiAgICAgICAgYWN0aXZlOiBmYWxzZSxcbiAgICB9O1xufVxuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCB7RGF6emxlclByb3BzfSBmcm9tICcuLi8uLi8uLi9jb21tb25zL2pzL3R5cGVzJztcblxuLyoqXG4gKiBTaW1wbGUgaHRtbC9jc3Mgc3Bpbm5lci5cbiAqL1xuY29uc3QgU3Bpbm5lciA9IChwcm9wczogRGF6emxlclByb3BzKSA9PiB7XG4gICAgY29uc3Qge2NsYXNzX25hbWUsIHN0eWxlLCBpZGVudGl0eX0gPSBwcm9wcztcbiAgICByZXR1cm4gPGRpdiBpZD17aWRlbnRpdHl9IGNsYXNzTmFtZT17Y2xhc3NfbmFtZX0gc3R5bGU9e3N0eWxlfSAvPjtcbn07XG5cbmV4cG9ydCBkZWZhdWx0IFNwaW5uZXI7XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IHttZXJnZUFsbH0gZnJvbSAncmFtZGEnO1xuaW1wb3J0IHtTdGlja3lQcm9wc30gZnJvbSAnLi4vdHlwZXMnO1xuXG4vKipcbiAqIEEgc2hvcnRoYW5kIGNvbXBvbmVudCBmb3IgYSBzdGlja3kgZGl2LlxuICovXG5jb25zdCBTdGlja3kgPSAocHJvcHM6IFN0aWNreVByb3BzKSA9PiB7XG4gICAgY29uc3Qge2NsYXNzX25hbWUsIGlkZW50aXR5LCBzdHlsZSwgY2hpbGRyZW4sIHRvcCwgbGVmdCwgcmlnaHQsIGJvdHRvbX0gPVxuICAgICAgICBwcm9wcztcbiAgICBjb25zdCBzdHlsZXMgPSBtZXJnZUFsbChbc3R5bGUsIHt0b3AsIGxlZnQsIHJpZ2h0LCBib3R0b219XSk7XG4gICAgcmV0dXJuIChcbiAgICAgICAgPGRpdiBjbGFzc05hbWU9e2NsYXNzX25hbWV9IGlkPXtpZGVudGl0eX0gc3R5bGU9e3N0eWxlc30+XG4gICAgICAgICAgICB7Y2hpbGRyZW59XG4gICAgICAgIDwvZGl2PlxuICAgICk7XG59O1xuXG5leHBvcnQgZGVmYXVsdCBTdGlja3k7XG4iLCJpbXBvcnQgUmVhY3QsIHt1c2VFZmZlY3QsIHVzZU1lbW8sIHVzZVN0YXRlfSBmcm9tICdyZWFjdCc7XG5pbXBvcnQge2pvaW59IGZyb20gJ3JhbWRhJztcbmltcG9ydCB7VG9hc3RQcm9wc30gZnJvbSAnLi4vdHlwZXMnO1xuXG4vKipcbiAqIERpc3BsYXkgYSBtZXNzYWdlIG92ZXIgdGhlIHVpIHRoYXQgd2lsbCBkaXNhcHBlYXJzIGFmdGVyIGEgZGVsYXkuXG4gKlxuICogOkNTUzpcbiAqXG4gKiAgICAgLSBgYGRhenpsZXItZXh0cmEtdG9hc3RgYFxuICogICAgIC0gYGBvcGVuZWRgYFxuICogICAgIC0gYGB0b2FzdC1pbm5lcmBgXG4gKiAgICAgLSBgYHRvcGBgXG4gKiAgICAgLSBgYHRvcC1sZWZ0YGBcbiAqICAgICAtIGBgdG9wLXJpZ2h0YGBcbiAqICAgICAtIGBgYm90dG9tYGBcbiAqICAgICAtIGBgYm90dG9tLWxlZnRgYFxuICogICAgIC0gYGBib3R0b20tcmlnaHRgYFxuICogICAgIC0gYGByaWdodGBgXG4gKi9cbmNvbnN0IFRvYXN0ID0gKHByb3BzOiBUb2FzdFByb3BzKSA9PiB7XG4gICAgY29uc3Qge1xuICAgICAgICBjbGFzc19uYW1lLFxuICAgICAgICBzdHlsZSxcbiAgICAgICAgaWRlbnRpdHksXG4gICAgICAgIG1lc3NhZ2UsXG4gICAgICAgIHBvc2l0aW9uLFxuICAgICAgICBvcGVuZWQsXG4gICAgICAgIGRlbGF5LFxuICAgICAgICB1cGRhdGVBc3BlY3RzLFxuICAgIH0gPSBwcm9wcztcbiAgICBjb25zdCBbZGlzcGxheWVkLCBzZXREaXNwbGF5ZWRdID0gdXNlU3RhdGUoZmFsc2UpO1xuXG4gICAgY29uc3QgY3NzID0gdXNlTWVtbygoKSA9PiB7XG4gICAgICAgIGNvbnN0IGMgPSBbY2xhc3NfbmFtZSwgcG9zaXRpb25dO1xuICAgICAgICBpZiAob3BlbmVkKSB7XG4gICAgICAgICAgICBjLnB1c2goJ29wZW5lZCcpO1xuICAgICAgICB9XG4gICAgICAgIHJldHVybiBqb2luKCcgJywgYyk7XG4gICAgfSwgW2NsYXNzX25hbWUsIG9wZW5lZCwgcG9zaXRpb25dKTtcbiAgICB1c2VFZmZlY3QoKCkgPT4ge1xuICAgICAgICBpZiAob3BlbmVkICYmICFkaXNwbGF5ZWQpIHtcbiAgICAgICAgICAgIHNldFRpbWVvdXQoKCkgPT4ge1xuICAgICAgICAgICAgICAgIHVwZGF0ZUFzcGVjdHMoe29wZW5lZDogZmFsc2V9KTtcbiAgICAgICAgICAgICAgICBzZXREaXNwbGF5ZWQoZmFsc2UpO1xuICAgICAgICAgICAgfSwgZGVsYXkpO1xuICAgICAgICAgICAgc2V0RGlzcGxheWVkKHRydWUpO1xuICAgICAgICB9XG4gICAgfSwgW29wZW5lZCwgZGlzcGxheWVkLCBkZWxheV0pO1xuXG4gICAgcmV0dXJuIChcbiAgICAgICAgPGRpdiBjbGFzc05hbWU9e2Nzc30gc3R5bGU9e3N0eWxlfSBpZD17aWRlbnRpdHl9PlxuICAgICAgICAgICAge21lc3NhZ2V9XG4gICAgICAgIDwvZGl2PlxuICAgICk7XG59O1xuXG5Ub2FzdC5kZWZhdWx0UHJvcHMgPSB7XG4gICAgZGVsYXk6IDMwMDAsXG4gICAgcG9zaXRpb246ICd0b3AnLFxuICAgIG9wZW5lZDogdHJ1ZSxcbn07XG5cbmV4cG9ydCBkZWZhdWx0IFRvYXN0O1xuIiwiaW1wb3J0IFJlYWN0LCB7dXNlTWVtb30gZnJvbSAncmVhY3QnO1xuaW1wb3J0IHtpcywgam9pbiwgaW5jbHVkZXMsIHNwbGl0LCBzbGljZSwgY29uY2F0LCB3aXRob3V0fSBmcm9tICdyYW1kYSc7XG5pbXBvcnQge1RyZWVWaWV3SXRlbVByb3BzLCBUcmVlVmlld1Byb3BzfSBmcm9tICcuLi90eXBlcyc7XG5cbmNvbnN0IFRyZWVWaWV3RWxlbWVudCA9ICh7XG4gICAgbGFiZWwsXG4gICAgb25DbGljayxcbiAgICBpZGVudGlmaWVyLFxuICAgIGl0ZW1zLFxuICAgIGxldmVsLFxuICAgIHNlbGVjdGVkLFxuICAgIGV4cGFuZGVkX2l0ZW1zLFxuICAgIG5lc3RfaWNvbl9leHBhbmRlZCxcbiAgICBuZXN0X2ljb25fY29sbGFwc2VkLFxufTogVHJlZVZpZXdJdGVtUHJvcHMpID0+IHtcbiAgICBjb25zdCBpc1NlbGVjdGVkID0gdXNlTWVtbyhcbiAgICAgICAgKCkgPT4gc2VsZWN0ZWQgJiYgaW5jbHVkZXMoaWRlbnRpZmllciwgc2VsZWN0ZWQpLFxuICAgICAgICBbc2VsZWN0ZWQsIGlkZW50aWZpZXJdXG4gICAgKTtcbiAgICBjb25zdCBpc0V4cGFuZGVkID0gdXNlTWVtbyhcbiAgICAgICAgKCkgPT4gaW5jbHVkZXMoaWRlbnRpZmllciwgZXhwYW5kZWRfaXRlbXMpLFxuICAgICAgICBbZXhwYW5kZWRfaXRlbXMsIGV4cGFuZGVkX2l0ZW1zXVxuICAgICk7XG4gICAgY29uc3QgY3NzID0gWyd0cmVlLWl0ZW0tbGFiZWwnLCBgbGV2ZWwtJHtsZXZlbH1gXTtcbiAgICBpZiAoaXNTZWxlY3RlZCkge1xuICAgICAgICBjc3MucHVzaCgnc2VsZWN0ZWQnKTtcbiAgICB9XG5cbiAgICByZXR1cm4gKFxuICAgICAgICA8ZGl2XG4gICAgICAgICAgICBjbGFzc05hbWU9e2B0cmVlLWl0ZW0gbGV2ZWwtJHtsZXZlbH1gfVxuICAgICAgICAgICAgc3R5bGU9e3ttYXJnaW5MZWZ0OiBgJHtsZXZlbH1yZW1gfX1cbiAgICAgICAgPlxuICAgICAgICAgICAgPGRpdlxuICAgICAgICAgICAgICAgIGNsYXNzTmFtZT17am9pbignICcsIGNzcyl9XG4gICAgICAgICAgICAgICAgb25DbGljaz17KGUpID0+IG9uQ2xpY2soZSwgaWRlbnRpZmllciwgQm9vbGVhbihpdGVtcykpfVxuICAgICAgICAgICAgPlxuICAgICAgICAgICAgICAgIHtpdGVtcyAmJiAoXG4gICAgICAgICAgICAgICAgICAgIDxzcGFuIGNsYXNzTmFtZT1cInRyZWUtY2FyZXRcIj5cbiAgICAgICAgICAgICAgICAgICAgICAgIHtpc0V4cGFuZGVkID8gbmVzdF9pY29uX2V4cGFuZGVkIDogbmVzdF9pY29uX2NvbGxhcHNlZH1cbiAgICAgICAgICAgICAgICAgICAgPC9zcGFuPlxuICAgICAgICAgICAgICAgICl9XG4gICAgICAgICAgICAgICAge2xhYmVsIHx8IGlkZW50aWZpZXJ9XG4gICAgICAgICAgICA8L2Rpdj5cblxuICAgICAgICAgICAge2l0ZW1zICYmIGlzRXhwYW5kZWQgJiYgKFxuICAgICAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwidHJlZS1zdWItaXRlbXNcIj5cbiAgICAgICAgICAgICAgICAgICAge2l0ZW1zLm1hcCgoaXRlbSkgPT5cbiAgICAgICAgICAgICAgICAgICAgICAgIHJlbmRlckl0ZW0oe1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHBhcmVudDogaWRlbnRpZmllcixcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBvbkNsaWNrLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGl0ZW0sXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgbGV2ZWw6IGxldmVsICsgMSxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBzZWxlY3RlZCxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBuZXN0X2ljb25fZXhwYW5kZWQsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgbmVzdF9pY29uX2NvbGxhcHNlZCxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBleHBhbmRlZF9pdGVtcyxcbiAgICAgICAgICAgICAgICAgICAgICAgIH0pXG4gICAgICAgICAgICAgICAgICAgICl9XG4gICAgICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgICApfVxuICAgICAgICA8L2Rpdj5cbiAgICApO1xufTtcblxuY29uc3QgcmVuZGVySXRlbSA9ICh7cGFyZW50LCBpdGVtLCBsZXZlbCwgLi4ucmVzdH06IGFueSkgPT4ge1xuICAgIGlmIChpcyhTdHJpbmcsIGl0ZW0pKSB7XG4gICAgICAgIHJldHVybiAoXG4gICAgICAgICAgICA8VHJlZVZpZXdFbGVtZW50XG4gICAgICAgICAgICAgICAgbGFiZWw9e2l0ZW19XG4gICAgICAgICAgICAgICAgaWRlbnRpZmllcj17cGFyZW50ID8gam9pbignLicsIFtwYXJlbnQsIGl0ZW1dKSA6IGl0ZW19XG4gICAgICAgICAgICAgICAgbGV2ZWw9e2xldmVsIHx8IDB9XG4gICAgICAgICAgICAgICAga2V5PXtpdGVtfVxuICAgICAgICAgICAgICAgIHsuLi5yZXN0fVxuICAgICAgICAgICAgLz5cbiAgICAgICAgKTtcbiAgICB9XG4gICAgcmV0dXJuIChcbiAgICAgICAgPFRyZWVWaWV3RWxlbWVudFxuICAgICAgICAgICAgey4uLml0ZW19XG4gICAgICAgICAgICBsZXZlbD17bGV2ZWwgfHwgMH1cbiAgICAgICAgICAgIGtleT17aXRlbS5pZGVudGlmaWVyfVxuICAgICAgICAgICAgaWRlbnRpZmllcj17XG4gICAgICAgICAgICAgICAgcGFyZW50ID8gam9pbignLicsIFtwYXJlbnQsIGl0ZW0uaWRlbnRpZmllcl0pIDogaXRlbS5pZGVudGlmaWVyXG4gICAgICAgICAgICB9XG4gICAgICAgICAgICB7Li4ucmVzdH1cbiAgICAgICAgLz5cbiAgICApO1xufTtcblxuLyoqXG4gKiBBIHRyZWUgb2YgbmVzdGVkIGl0ZW1zLlxuICpcbiAqIDpDU1M6XG4gKlxuICogICAgIC0gYGBkYXp6bGVyLWV4dHJhLXRyZWUtdmlld2BgXG4gKiAgICAgLSBgYHRyZWUtaXRlbWBgXG4gKiAgICAgLSBgYHRyZWUtaXRlbS1sYWJlbGBgXG4gKiAgICAgLSBgYHRyZWUtc3ViLWl0ZW1zYGBcbiAqICAgICAtIGBgdHJlZS1jYXJldGBgXG4gKiAgICAgLSBgYHNlbGVjdGVkYGBcbiAqICAgICAtIGBgbGV2ZWwte259YGBcbiAqXG4gKiA6ZXhhbXBsZTpcbiAqXG4gKiAuLiBsaXRlcmFsaW5jbHVkZTo6IC4uLy4uL3Rlc3RzL2NvbXBvbmVudHMvcGFnZXMvdHJlZXZpZXcucHlcbiAqL1xuY29uc3QgVHJlZVZpZXcgPSAoe1xuICAgIGNsYXNzX25hbWUsXG4gICAgc3R5bGUsXG4gICAgaWRlbnRpdHksXG4gICAgdXBkYXRlQXNwZWN0cyxcbiAgICBpdGVtcyxcbiAgICBzZWxlY3RlZCxcbiAgICBleHBhbmRlZF9pdGVtcyxcbiAgICBuZXN0X2ljb25fZXhwYW5kZWQsXG4gICAgbmVzdF9pY29uX2NvbGxhcHNlZCxcbn06IFRyZWVWaWV3UHJvcHMpID0+IHtcbiAgICBjb25zdCBvbkNsaWNrID0gKGUsIGlkZW50aWZpZXIsIGV4cGFuZCkgPT4ge1xuICAgICAgICBlLnN0b3BQcm9wYWdhdGlvbigpO1xuICAgICAgICBjb25zdCBwYXlsb2FkOiBhbnkgPSB7fTtcbiAgICAgICAgaWYgKHNlbGVjdGVkICYmIGluY2x1ZGVzKGlkZW50aWZpZXIsIHNlbGVjdGVkKSkge1xuICAgICAgICAgICAgbGV0IGxhc3QgPSBzcGxpdCgnLicsIGlkZW50aWZpZXIpO1xuICAgICAgICAgICAgbGFzdCA9IHNsaWNlKDAsIGxhc3QubGVuZ3RoIC0gMSwgbGFzdCk7XG4gICAgICAgICAgICBpZiAobGFzdC5sZW5ndGggPT09IDApIHtcbiAgICAgICAgICAgICAgICBwYXlsb2FkLnNlbGVjdGVkID0gbnVsbDtcbiAgICAgICAgICAgIH0gZWxzZSBpZiAobGFzdC5sZW5ndGggPT09IDEpIHtcbiAgICAgICAgICAgICAgICBwYXlsb2FkLnNlbGVjdGVkID0gbGFzdFswXTtcbiAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgcGF5bG9hZC5zZWxlY3RlZCA9IGpvaW4oJy4nLCBsYXN0KTtcbiAgICAgICAgICAgIH1cbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIHBheWxvYWQuc2VsZWN0ZWQgPSBpZGVudGlmaWVyO1xuICAgICAgICB9XG5cbiAgICAgICAgaWYgKGV4cGFuZCkge1xuICAgICAgICAgICAgaWYgKGluY2x1ZGVzKGlkZW50aWZpZXIsIGV4cGFuZGVkX2l0ZW1zKSkge1xuICAgICAgICAgICAgICAgIHBheWxvYWQuZXhwYW5kZWRfaXRlbXMgPSB3aXRob3V0KFtpZGVudGlmaWVyXSwgZXhwYW5kZWRfaXRlbXMpO1xuICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICBwYXlsb2FkLmV4cGFuZGVkX2l0ZW1zID0gY29uY2F0KGV4cGFuZGVkX2l0ZW1zLCBbaWRlbnRpZmllcl0pO1xuICAgICAgICAgICAgfVxuICAgICAgICB9XG4gICAgICAgIHVwZGF0ZUFzcGVjdHMocGF5bG9hZCk7XG4gICAgfTtcbiAgICByZXR1cm4gKFxuICAgICAgICA8ZGl2IGNsYXNzTmFtZT17Y2xhc3NfbmFtZX0gc3R5bGU9e3N0eWxlfSBpZD17aWRlbnRpdHl9PlxuICAgICAgICAgICAge2l0ZW1zLm1hcCgoaXRlbSkgPT5cbiAgICAgICAgICAgICAgICByZW5kZXJJdGVtKHtcbiAgICAgICAgICAgICAgICAgICAgaXRlbSxcbiAgICAgICAgICAgICAgICAgICAgb25DbGljayxcbiAgICAgICAgICAgICAgICAgICAgc2VsZWN0ZWQsXG4gICAgICAgICAgICAgICAgICAgIG5lc3RfaWNvbl9leHBhbmRlZCxcbiAgICAgICAgICAgICAgICAgICAgbmVzdF9pY29uX2NvbGxhcHNlZCxcbiAgICAgICAgICAgICAgICAgICAgZXhwYW5kZWRfaXRlbXMsXG4gICAgICAgICAgICAgICAgfSlcbiAgICAgICAgICAgICl9XG4gICAgICAgIDwvZGl2PlxuICAgICk7XG59O1xuXG5UcmVlVmlldy5kZWZhdWx0UHJvcHMgPSB7XG4gICAgbmVzdF9pY29uX2NvbGxhcHNlZDogJ+KPtScsXG4gICAgbmVzdF9pY29uX2V4cGFuZGVkOiAn4o+3JyxcbiAgICBleHBhbmRlZF9pdGVtczogW10sXG59O1xuXG5leHBvcnQgZGVmYXVsdCBUcmVlVmlldztcbiIsImltcG9ydCAnLi4vc2Nzcy9pbmRleC5zY3NzJztcblxuaW1wb3J0IE5vdGljZSBmcm9tICcuL2NvbXBvbmVudHMvTm90aWNlJztcbmltcG9ydCBQYWdlciBmcm9tICcuL2NvbXBvbmVudHMvUGFnZXInO1xuaW1wb3J0IFNwaW5uZXIgZnJvbSAnLi9jb21wb25lbnRzL1NwaW5uZXInO1xuaW1wb3J0IFN0aWNreSBmcm9tICcuL2NvbXBvbmVudHMvU3RpY2t5JztcbmltcG9ydCBEcmF3ZXIgZnJvbSAnLi9jb21wb25lbnRzL0RyYXdlcic7XG5pbXBvcnQgUG9wVXAgZnJvbSAnLi9jb21wb25lbnRzL1BvcFVwJztcbmltcG9ydCBUcmVlVmlldyBmcm9tICcuL2NvbXBvbmVudHMvVHJlZVZpZXcnO1xuaW1wb3J0IFRvYXN0IGZyb20gJy4vY29tcG9uZW50cy9Ub2FzdCc7XG5pbXBvcnQgUGFnZU1hcCBmcm9tICcuL2NvbXBvbmVudHMvUGFnZU1hcCc7XG5pbXBvcnQgQ29sb3JQaWNrZXIgZnJvbSAnLi9jb21wb25lbnRzL0NvbG9yUGlja2VyJztcblxuZXhwb3J0IHtcbiAgICBOb3RpY2UsXG4gICAgUGFnZXIsXG4gICAgU3Bpbm5lcixcbiAgICBTdGlja3ksXG4gICAgRHJhd2VyLFxuICAgIFBvcFVwLFxuICAgIFRyZWVWaWV3LFxuICAgIFRvYXN0LFxuICAgIFBhZ2VNYXAsXG4gICAgQ29sb3JQaWNrZXIsXG59O1xuIiwibW9kdWxlLmV4cG9ydHMgPSBfX1dFQlBBQ0tfRVhURVJOQUxfTU9EVUxFX3JlYWN0X187Il0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9