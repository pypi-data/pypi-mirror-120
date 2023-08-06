"use strict";
(function webpackUniversalModuleDefinition(root, factory) {
	if(typeof exports === 'object' && typeof module === 'object')
		module.exports = factory(require("react"), require("react-dom"));
	else if(typeof define === 'function' && define.amd)
		define(["react", "react-dom"], factory);
	else if(typeof exports === 'object')
		exports["dazzler_renderer"] = factory(require("react"), require("react-dom"));
	else
		root["dazzler_renderer"] = factory(root["React"], root["ReactDOM"]);
})(self, function(__WEBPACK_EXTERNAL_MODULE_react__, __WEBPACK_EXTERNAL_MODULE_react_dom__) {
return (self["webpackChunkdazzler_name_"] = self["webpackChunkdazzler_name_"] || []).push([["renderer"],{

/***/ "./src/renderer/js/aspects.ts":
/*!************************************!*\
  !*** ./src/renderer/js/aspects.ts ***!
  \************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


exports.__esModule = true;
exports.isSameAspect = exports.getAspectKey = exports.coerceAspect = exports.isAspect = void 0;
var ramda_1 = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
var isAspect = function (obj) {
    return ramda_1.is(Object, obj) && ramda_1.has('identity', obj) && ramda_1.has('aspect', obj);
};
exports.isAspect = isAspect;
var coerceAspect = function (obj, getAspect) { return (exports.isAspect(obj) ? getAspect(obj.identity, obj.aspect) : obj); };
exports.coerceAspect = coerceAspect;
var getAspectKey = function (identity, aspect) {
    return aspect + "@" + identity;
};
exports.getAspectKey = getAspectKey;
var isSameAspect = function (a, b) {
    return a.identity === b.identity && a.aspect === b.aspect;
};
exports.isSameAspect = isSameAspect;


/***/ }),

/***/ "./src/renderer/js/components/Renderer.tsx":
/*!*************************************************!*\
  !*** ./src/renderer/js/components/Renderer.tsx ***!
  \*************************************************/
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
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
var react_1 = __importStar(__webpack_require__(/*! react */ "react"));
var Updater_1 = __importDefault(__webpack_require__(/*! ./Updater */ "./src/renderer/js/components/Updater.tsx"));
var Renderer = function (props) {
    var _a = react_1.useState(1), reloadKey = _a[0], setReloadKey = _a[1];
    // FIXME find where this is used and refactor/remove
    // @ts-ignore
    window.dazzler_base_url = props.baseUrl;
    return (react_1["default"].createElement("div", { className: "dazzler-renderer" },
        react_1["default"].createElement(Updater_1["default"], __assign({}, props, { key: "upd-" + reloadKey, hotReload: function () { return setReloadKey(reloadKey + 1); } }))));
};
exports.default = Renderer;


/***/ }),

/***/ "./src/renderer/js/components/Updater.tsx":
/*!************************************************!*\
  !*** ./src/renderer/js/components/Updater.tsx ***!
  \************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


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
var requests_1 = __webpack_require__(/*! ../requests */ "./src/renderer/js/requests.ts");
var hydrator_1 = __webpack_require__(/*! ../hydrator */ "./src/renderer/js/hydrator.tsx");
var requirements_1 = __webpack_require__(/*! ../requirements */ "./src/renderer/js/requirements.ts");
var commons_1 = __webpack_require__(/*! commons */ "./src/commons/js/index.ts");
var ramda_1 = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
var transforms_1 = __webpack_require__(/*! ../transforms */ "./src/renderer/js/transforms.ts");
var aspects_1 = __webpack_require__(/*! ../aspects */ "./src/renderer/js/aspects.ts");
var Updater = /** @class */ (function (_super) {
    __extends(Updater, _super);
    function Updater(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            layout: null,
            ready: false,
            page: null,
            bindings: {},
            packages: [],
            reload: false,
            rebindings: [],
            requirements: [],
            reloading: false,
            needRefresh: false,
            ties: [],
        };
        // The api url for the page is the same but a post.
        // Fetch bindings, packages & requirements
        _this.pageApi = requests_1.apiRequest(window.location.href);
        // All components get connected.
        _this.boundComponents = {};
        _this.ws = null;
        _this.updateAspects = _this.updateAspects.bind(_this);
        _this.connect = _this.connect.bind(_this);
        _this.disconnect = _this.disconnect.bind(_this);
        _this.onMessage = _this.onMessage.bind(_this);
        return _this;
    }
    Updater.prototype.updateAspects = function (identity, aspects) {
        var _this = this;
        return new Promise(function (resolve) {
            var aspectKeys = ramda_1.keys(aspects);
            var bindings = aspectKeys
                .map(function (key) { return (__assign(__assign({}, _this.state.bindings[aspects_1.getAspectKey(identity, key)]), { value: aspects[key] })); })
                .filter(function (e) { return e.trigger; });
            _this.state.rebindings.forEach(function (binding) {
                if (binding.trigger.identity.test(identity)) {
                    // @ts-ignore
                    bindings = ramda_1.concat(bindings, aspectKeys
                        .filter(function (k) {
                        return binding.trigger.aspect.test(k);
                    })
                        .map(function (k) { return (__assign(__assign({}, binding), { value: aspects[k], trigger: __assign(__assign({}, binding.trigger), { identity: identity, aspect: k }) })); }));
                }
            });
            var removableTies = [];
            ramda_1.flatten(aspectKeys.map(function (aspect) {
                var ties = [];
                for (var i = 0; i < _this.state.ties.length; i++) {
                    var tie = _this.state.ties[i];
                    var trigger = tie.trigger;
                    if ((trigger.regex &&
                        // @ts-ignore
                        trigger.identity.test(identity) &&
                        // @ts-ignore
                        trigger.aspect.test(aspect)) ||
                        aspects_1.isSameAspect(trigger, { identity: identity, aspect: aspect })) {
                        ties.push(__assign(__assign({}, tie), { value: aspects[aspect] }));
                    }
                }
                return ties;
            })).forEach(function (tie) {
                var transforms = tie.transforms;
                var value = tie.value;
                if (tie.trigger.once) {
                    removableTies.push(tie);
                }
                if (transforms) {
                    value = transforms.reduce(function (acc, e) {
                        return transforms_1.executeTransform(e.transform, acc, e.args, e.next, _this.getAspect.bind(_this));
                    }, value);
                }
                tie.targets.forEach(function (t) {
                    var _a;
                    var component = _this.boundComponents[t.identity];
                    if (component) {
                        component.updateAspects((_a = {}, _a[t.aspect] = value, _a));
                    }
                });
            });
            if (removableTies.length) {
                _this.setState({
                    ties: _this.state.ties.filter(function (t) {
                        return !removableTies.reduce(function (acc, tie) {
                            return acc ||
                                (aspects_1.isSameAspect(t.trigger, tie.trigger) &&
                                    ramda_1.all(function (_a) {
                                        var t1 = _a[0], t2 = _a[1];
                                        return aspects_1.isSameAspect(t1, t2);
                                    })(ramda_1.zip(t.targets, tie.targets)));
                        }, false);
                    }),
                });
            }
            if (!bindings) {
                resolve(0);
            }
            else {
                var removableBindings_1 = [];
                bindings.forEach(function (binding) {
                    _this.sendBinding(binding, binding.value);
                    if (binding.trigger.once) {
                        removableBindings_1.push(binding);
                    }
                });
                if (removableBindings_1.length) {
                    _this.setState({
                        bindings: removableBindings_1.reduce(function (acc, binding) {
                            return ramda_1.dissoc(aspects_1.getAspectKey(binding.trigger.identity, binding.trigger.aspect), acc);
                        }, _this.state.bindings),
                    });
                }
                // TODO investigate reasons/uses of promise
                resolve(bindings.length);
            }
        });
    };
    Updater.prototype.getAspect = function (identity, aspect) {
        var c = this.boundComponents[identity];
        if (c) {
            return c.getAspect(aspect);
        }
        return undefined;
    };
    Updater.prototype.connect = function (identity, setAspects, getAspect, matchAspects, updateAspects) {
        this.boundComponents[identity] = {
            setAspects: setAspects,
            getAspect: getAspect,
            matchAspects: matchAspects,
            updateAspects: updateAspects,
        };
    };
    Updater.prototype.disconnect = function (identity) {
        delete this.boundComponents[identity];
    };
    Updater.prototype.onMessage = function (response) {
        var _this = this;
        var data = JSON.parse(response.data);
        var identity = data.identity, kind = data.kind, payload = data.payload, storage = data.storage, request_id = data.request_id;
        var store;
        if (storage === 'session') {
            store = window.sessionStorage;
        }
        else {
            store = window.localStorage;
        }
        switch (kind) {
            case 'set-aspect':
                var setAspects = function (component) {
                    return component
                        .setAspects(hydrator_1.hydrateProps(payload, _this.updateAspects, _this.connect, _this.disconnect))
                        .then(function () { return _this.updateAspects(identity, payload); });
                };
                if (data.regex) {
                    var pattern_1 = new RegExp(data.identity);
                    ramda_1.keys(this.boundComponents)
                        .filter(function (k) { return pattern_1.test(k); })
                        .map(function (k) { return _this.boundComponents[k]; })
                        .forEach(setAspects);
                }
                else {
                    setAspects(this.boundComponents[identity]);
                }
                break;
            case 'get-aspect':
                var aspect = data.aspect;
                var wanted = this.boundComponents[identity];
                if (!wanted) {
                    this.ws.send(JSON.stringify({
                        kind: kind,
                        identity: identity,
                        aspect: aspect,
                        request_id: request_id,
                        error: "Aspect not found " + identity + "." + aspect,
                    }));
                    return;
                }
                var value = wanted.getAspect(aspect);
                this.ws.send(JSON.stringify({
                    kind: kind,
                    identity: identity,
                    aspect: aspect,
                    value: hydrator_1.prepareProp(value),
                    request_id: request_id,
                }));
                break;
            case 'set-storage':
                store.setItem(identity, JSON.stringify(payload));
                break;
            case 'get-storage':
                this.ws.send(JSON.stringify({
                    kind: kind,
                    identity: identity,
                    request_id: request_id,
                    value: JSON.parse(store.getItem(identity)),
                }));
                break;
            case 'reload':
                var filenames = data.filenames, hot = data.hot, refresh = data.refresh, deleted = data.deleted;
                if (refresh) {
                    this.ws.close();
                    this.setState({ reloading: true, needRefresh: true });
                    return;
                }
                if (hot) {
                    // The ws connection will close, when it
                    // reconnect it will do a hard reload of the page api.
                    this.setState({ reloading: true });
                    return;
                }
                filenames.forEach(requirements_1.loadRequirement);
                deleted.forEach(function (r) { return commons_1.disableCss(r.url); });
                break;
            case 'ping':
                // Just do nothing.
                break;
        }
    };
    Updater.prototype.sendBinding = function (binding, value) {
        var _this = this;
        // Collect all values and send a binding payload
        var trigger = __assign(__assign({}, binding.trigger), { value: hydrator_1.prepareProp(value) });
        var states = binding.states.reduce(function (acc, state) {
            if (state.regex) {
                var identityPattern_1 = new RegExp(state.identity);
                var aspectPattern_1 = new RegExp(state.aspect);
                return ramda_1.concat(acc, ramda_1.flatten(ramda_1.keys(_this.boundComponents).map(function (k) {
                    var values = [];
                    if (identityPattern_1.test(k)) {
                        values = _this.boundComponents[k]
                            .matchAspects(aspectPattern_1)
                            .map(function (_a) {
                            var name = _a[0], val = _a[1];
                            return (__assign(__assign({}, state), { identity: k, aspect: name, value: hydrator_1.prepareProp(val) }));
                        });
                    }
                    return values;
                })));
            }
            acc.push(__assign(__assign({}, state), { value: _this.boundComponents[state.identity] &&
                    hydrator_1.prepareProp(_this.boundComponents[state.identity].getAspect(state.aspect)) }));
            return acc;
        }, []);
        var payload = {
            trigger: trigger,
            states: states,
            kind: 'binding',
            page: this.state.page,
            key: binding.key,
        };
        this.ws.send(JSON.stringify(payload));
    };
    Updater.prototype._connectWS = function () {
        var _this = this;
        // Setup websocket for updates
        var tries = 0;
        var hardClose = false;
        var connexion = function () {
            var url = "ws" + (window.location.href.startsWith('https') ? 's' : '') + "://" + ((_this.props.baseUrl && _this.props.baseUrl) ||
                window.location.host) + "/" + _this.state.page + "/ws";
            _this.ws = new WebSocket(url);
            _this.ws.addEventListener('message', _this.onMessage);
            _this.ws.onopen = function () {
                if (_this.state.reloading) {
                    hardClose = true;
                    _this.ws.close();
                    if (_this.state.needRefresh) {
                        window.location.reload();
                    }
                    else {
                        _this.props.hotReload();
                    }
                }
                else {
                    _this.setState({ ready: true });
                    tries = 0;
                }
            };
            _this.ws.onclose = function () {
                var reconnect = function () {
                    tries++;
                    connexion();
                };
                if (!hardClose && tries < _this.props.retries) {
                    setTimeout(reconnect, 1000);
                }
            };
        };
        connexion();
    };
    Updater.prototype.componentDidMount = function () {
        var _this = this;
        this.pageApi('', { method: 'POST' }).then(function (response) {
            var toRegex = function (x) { return new RegExp(x); };
            _this.setState({
                page: response.page,
                layout: response.layout,
                bindings: ramda_1.pickBy(function (b) { return !b.regex; }, response.bindings),
                // Regex bindings triggers
                rebindings: ramda_1.map(function (x) {
                    var binding = response.bindings[x];
                    binding.trigger = ramda_1.evolve({
                        identity: toRegex,
                        aspect: toRegex,
                    }, binding.trigger);
                    return binding;
                }, ramda_1.keys(ramda_1.pickBy(function (b) { return b.regex; }, response.bindings))),
                packages: response.packages,
                requirements: response.requirements,
                ties: ramda_1.map(function (tie) {
                    if (tie.trigger.regex) {
                        return ramda_1.evolve({
                            trigger: {
                                identity: toRegex,
                                aspect: toRegex,
                            },
                        }, tie);
                    }
                    return tie;
                }, response.ties),
            }, function () {
                return requirements_1.loadRequirements(response.requirements, response.packages).then(function () {
                    if (ramda_1.keys(response.bindings).length || response.reload) {
                        _this._connectWS();
                    }
                    else {
                        _this.setState({ ready: true });
                    }
                });
            });
        });
    };
    Updater.prototype.render = function () {
        var _a = this.state, layout = _a.layout, ready = _a.ready, reloading = _a.reloading;
        if (!ready) {
            return (react_1["default"].createElement("div", { className: "dazzler-loading-container" },
                react_1["default"].createElement("div", { className: "dazzler-spin" }),
                react_1["default"].createElement("div", { className: "dazzler-loading" }, "Loading...")));
        }
        if (reloading) {
            return (react_1["default"].createElement("div", { className: "dazzler-loading-container" },
                react_1["default"].createElement("div", { className: "dazzler-spin reload" }),
                react_1["default"].createElement("div", { className: "dazzler-loading" }, "Reloading...")));
        }
        if (!hydrator_1.isComponent(layout)) {
            throw new Error("Layout is not a component: " + layout);
        }
        var contexts = [];
        var onContext = function (contextComponent) {
            contexts.push(contextComponent);
        };
        var hydrated = hydrator_1.hydrateComponent(layout.name, layout.package, layout.identity, hydrator_1.hydrateProps(layout.aspects, this.updateAspects, this.connect, this.disconnect, onContext), this.updateAspects, this.connect, this.disconnect, onContext);
        return (react_1["default"].createElement("div", { className: "dazzler-rendered" }, contexts.length
            ? contexts.reduce(function (acc, Context) {
                if (!acc) {
                    return react_1["default"].createElement(Context, null, hydrated);
                }
                return react_1["default"].createElement(Context, null, acc);
            }, null)
            : hydrated));
    };
    return Updater;
}(react_1["default"].Component));
exports.default = Updater;


/***/ }),

/***/ "./src/renderer/js/components/Wrapper.tsx":
/*!************************************************!*\
  !*** ./src/renderer/js/components/Wrapper.tsx ***!
  \************************************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


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
var ramda_1 = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
var commons_1 = __webpack_require__(/*! commons */ "./src/commons/js/index.ts");
/**
 * Wraps components for aspects updating.
 */
var Wrapper = /** @class */ (function (_super) {
    __extends(Wrapper, _super);
    function Wrapper(props) {
        var _this = _super.call(this, props) || this;
        _this.state = {
            aspects: props.aspects || {},
            ready: false,
            initial: false,
        };
        _this.setAspects = _this.setAspects.bind(_this);
        _this.getAspect = _this.getAspect.bind(_this);
        _this.updateAspects = _this.updateAspects.bind(_this);
        _this.matchAspects = _this.matchAspects.bind(_this);
        return _this;
    }
    Wrapper.prototype.updateAspects = function (aspects) {
        var _this = this;
        return this.setAspects(aspects).then(function () {
            return _this.props.updateAspects(_this.props.identity, aspects);
        });
    };
    Wrapper.prototype.setAspects = function (aspects) {
        var _this = this;
        return new Promise(function (resolve) {
            _this.setState({ aspects: __assign(__assign({}, _this.state.aspects), aspects) }, resolve);
        });
    };
    Wrapper.prototype.getAspect = function (aspect) {
        return this.state.aspects[aspect];
    };
    Wrapper.prototype.matchAspects = function (pattern) {
        var _this = this;
        return ramda_1.keys(this.state.aspects)
            .filter(function (k) { return pattern.test(k); })
            .map(function (k) { return [k, _this.state.aspects[k]]; });
    };
    Wrapper.prototype.componentDidMount = function () {
        var _this = this;
        // Only update the component when mounted.
        // Otherwise gets a race condition with willUnmount
        this.props.connect(this.props.identity, this.setAspects, this.getAspect, this.matchAspects, this.updateAspects);
        if (!this.state.initial) {
            this.updateAspects(this.state.aspects).then(function () {
                return _this.setState({ ready: true, initial: true });
            });
        }
    };
    Wrapper.prototype.componentWillUnmount = function () {
        this.props.disconnect(this.props.identity);
    };
    Wrapper.prototype.render = function () {
        var _a = this.props, component = _a.component, component_name = _a.component_name, package_name = _a.package_name;
        var _b = this.state, aspects = _b.aspects, ready = _b.ready;
        if (!ready) {
            return null;
        }
        return react_1["default"].cloneElement(component, __assign(__assign({}, aspects), { updateAspects: this.updateAspects, identity: this.props.identity, class_name: ramda_1.join(' ', ramda_1.concat([
                package_name
                    .replace('_', '-')
                    .toLowerCase() + "-" + commons_1.camelToSpinal(component_name),
            ], aspects.class_name ? aspects.class_name.split(' ') : [])) }));
    };
    return Wrapper;
}(react_1["default"].Component));
exports.default = Wrapper;


/***/ }),

/***/ "./src/renderer/js/hydrator.tsx":
/*!**************************************!*\
  !*** ./src/renderer/js/hydrator.tsx ***!
  \**************************************/
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
exports.prepareProp = exports.hydrateComponent = exports.hydrateProps = exports.isComponent = void 0;
var ramda_1 = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
var react_1 = __importDefault(__webpack_require__(/*! react */ "react"));
var Wrapper_1 = __importDefault(__webpack_require__(/*! ./components/Wrapper */ "./src/renderer/js/components/Wrapper.tsx"));
function isComponent(c) {
    return (ramda_1.type(c) === 'Object' &&
        c.hasOwnProperty('package') &&
        c.hasOwnProperty('aspects') &&
        c.hasOwnProperty('name') &&
        c.hasOwnProperty('identity'));
}
exports.isComponent = isComponent;
function hydrateProps(props, updateAspects, connect, disconnect, onContext) {
    var replace = {};
    Object.entries(props).forEach(function (_a) {
        var k = _a[0], v = _a[1];
        if (ramda_1.type(v) === 'Array') {
            replace[k] = v.map(function (c) {
                if (!isComponent(c)) {
                    // Mixing components and primitives
                    if (ramda_1.type(c) === 'Object') {
                        // Not a component but maybe it contains some ?
                        return hydrateProps(c, updateAspects, connect, disconnect, onContext);
                    }
                    return c;
                }
                var newProps = hydrateProps(c.aspects, updateAspects, connect, disconnect, onContext);
                if (!newProps.key) {
                    newProps.key = c.identity;
                }
                return hydrateComponent(c.name, c.package, c.identity, newProps, updateAspects, connect, disconnect, onContext);
            });
        }
        else if (isComponent(v)) {
            var newProps = hydrateProps(v.aspects, updateAspects, connect, disconnect, onContext);
            replace[k] = hydrateComponent(v.name, v.package, v.identity, newProps, updateAspects, connect, disconnect, onContext);
        }
        else if (ramda_1.type(v) === 'Object') {
            replace[k] = hydrateProps(v, updateAspects, connect, disconnect, onContext);
        }
    });
    return __assign(__assign({}, props), replace);
}
exports.hydrateProps = hydrateProps;
function hydrateComponent(name, package_name, identity, props, updateAspects, connect, disconnect, onContext) {
    var pack = window[package_name];
    if (!pack) {
        throw new Error("Invalid package name: " + package_name);
    }
    var component = pack[name];
    if (!component) {
        throw new Error("Invalid component name: " + package_name + "." + name);
    }
    // @ts-ignore
    var element = react_1["default"].createElement(component, props);
    /* eslint-disable react/prop-types */
    var wrapper = function (_a) {
        var children = _a.children;
        return (react_1["default"].createElement(Wrapper_1["default"], { identity: identity, updateAspects: updateAspects, component: element, connect: connect, package_name: package_name, component_name: name, aspects: __assign({ children: children }, props), disconnect: disconnect, key: "wrapper-" + identity }));
    };
    if (component.isContext) {
        onContext(wrapper);
        return null;
    }
    return wrapper({});
}
exports.hydrateComponent = hydrateComponent;
function prepareProp(prop) {
    if (react_1["default"].isValidElement(prop)) {
        // @ts-ignore
        var props = prop.props;
        return {
            identity: props.identity,
            // @ts-ignore
            aspects: ramda_1.map(prepareProp, ramda_1.omit([
                'identity',
                'updateAspects',
                '_name',
                '_package',
                'aspects',
                'key',
            ], props.aspects)),
            name: props.component_name,
            package: props.package_name,
        };
    }
    if (ramda_1.type(prop) === 'Array') {
        return prop.map(prepareProp);
    }
    if (ramda_1.type(prop) === 'Object') {
        return ramda_1.map(prepareProp, prop);
    }
    return prop;
}
exports.prepareProp = prepareProp;


/***/ }),

/***/ "./src/renderer/js/index.tsx":
/*!***********************************!*\
  !*** ./src/renderer/js/index.tsx ***!
  \***********************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {


var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
exports.__esModule = true;
exports.render = exports.Renderer = void 0;
var react_1 = __importDefault(__webpack_require__(/*! react */ "react"));
var react_dom_1 = __importDefault(__webpack_require__(/*! react-dom */ "react-dom"));
var Renderer_1 = __importDefault(__webpack_require__(/*! ./components/Renderer */ "./src/renderer/js/components/Renderer.tsx"));
exports.Renderer = Renderer_1["default"];
function render(_a, element) {
    var baseUrl = _a.baseUrl, ping = _a.ping, ping_interval = _a.ping_interval, retries = _a.retries;
    react_dom_1["default"].render(react_1["default"].createElement(Renderer_1["default"], { baseUrl: baseUrl, ping: ping, ping_interval: ping_interval, retries: retries }), element);
}
exports.render = render;


/***/ }),

/***/ "./src/renderer/js/requests.ts":
/*!*************************************!*\
  !*** ./src/renderer/js/requests.ts ***!
  \*************************************/
/***/ (function(__unused_webpack_module, exports) {


/* eslint-disable no-magic-numbers */
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
exports.apiRequest = exports.xhrRequest = exports.JSONHEADERS = void 0;
var jsonPattern = /json/i;
var defaultXhrOptions = {
    method: 'GET',
    headers: {},
    payload: '',
    json: true,
};
exports.JSONHEADERS = {
    'Content-Type': 'application/json',
};
function xhrRequest(url, options) {
    if (options === void 0) { options = defaultXhrOptions; }
    return new Promise(function (resolve, reject) {
        var _a = __assign(__assign({}, defaultXhrOptions), options), method = _a.method, headers = _a.headers, payload = _a.payload, json = _a.json;
        var xhr = new XMLHttpRequest();
        xhr.open(method, url);
        var head = json ? __assign(__assign({}, exports.JSONHEADERS), headers) : headers;
        Object.keys(head).forEach(function (k) { return xhr.setRequestHeader(k, head[k]); });
        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    var responseValue = xhr.response;
                    if (jsonPattern.test(xhr.getResponseHeader('Content-Type'))) {
                        responseValue = JSON.parse(xhr.responseText);
                    }
                    resolve(responseValue);
                }
                else {
                    reject({
                        error: 'RequestError',
                        message: "XHR " + url + " FAILED - STATUS: " + xhr.status + " MESSAGE: " + xhr.statusText,
                        status: xhr.status,
                        xhr: xhr,
                    });
                }
            }
        };
        xhr.onerror = function (err) { return reject(err); };
        // @ts-ignore
        xhr.send(json ? JSON.stringify(payload) : payload);
    });
}
exports.xhrRequest = xhrRequest;
function apiRequest(baseUrl) {
    return function () {
        var url = baseUrl + arguments[0];
        var options = arguments[1] || {};
        options.headers = __assign({}, options.headers);
        return new Promise(function (resolve) {
            xhrRequest(url, options).then(resolve);
        });
    };
}
exports.apiRequest = apiRequest;


/***/ }),

/***/ "./src/renderer/js/requirements.ts":
/*!*****************************************!*\
  !*** ./src/renderer/js/requirements.ts ***!
  \*****************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


exports.__esModule = true;
exports.loadRequirements = exports.loadRequirement = void 0;
var commons_1 = __webpack_require__(/*! commons */ "./src/commons/js/index.ts");
var ramda_1 = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
function loadRequirement(requirement) {
    return new Promise(function (resolve, reject) {
        var url = requirement.url, kind = requirement.kind;
        var method;
        if (kind === 'js') {
            method = commons_1.loadScript;
        }
        else if (kind === 'css') {
            method = commons_1.loadCss;
        }
        else if (kind === 'map') {
            return resolve();
        }
        else {
            return reject({ error: "Invalid requirement kind: " + kind });
        }
        return method(url).then(resolve)["catch"](reject);
    });
}
exports.loadRequirement = loadRequirement;
function loadOneByOne(requirements) {
    return new Promise(function (resolve) {
        var handle = function (reqs) {
            if (reqs.length) {
                var requirement = reqs[0];
                loadRequirement(requirement).then(function () { return handle(ramda_1.drop(1, reqs)); });
            }
            else {
                resolve(null);
            }
        };
        handle(requirements);
    });
}
function loadRequirements(requirements, packages) {
    return new Promise(function (resolve, reject) {
        var loadings = [];
        Object.keys(packages).forEach(function (pack_name) {
            var pack = packages[pack_name];
            loadings = loadings.concat(loadOneByOne(pack.requirements.filter(function (r) { return r.kind === 'js'; })));
            loadings = loadings.concat(pack.requirements
                .filter(function (r) { return r.kind === 'css'; })
                .map(loadRequirement));
        });
        // Then load requirements so they can use packages
        // and override css.
        Promise.all(loadings)
            .then(function () {
            var i = 0;
            // Load in order.
            var handler = function () {
                if (i < requirements.length) {
                    loadRequirement(requirements[i]).then(function () {
                        i++;
                        handler();
                    });
                }
                else {
                    resolve();
                }
            };
            handler();
        })["catch"](reject);
    });
}
exports.loadRequirements = loadRequirements;


/***/ }),

/***/ "./src/renderer/js/transforms.ts":
/*!***************************************!*\
  !*** ./src/renderer/js/transforms.ts ***!
  \***************************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {


exports.__esModule = true;
exports.executeTransform = void 0;
/* eslint-disable no-use-before-define */
var ramda_1 = __webpack_require__(/*! ramda */ "./node_modules/ramda/es/index.js");
var aspects_1 = __webpack_require__(/*! ./aspects */ "./src/renderer/js/aspects.ts");
var transforms = {
    /* String transforms */
    ToUpper: function (value) {
        return value.toUpperCase();
    },
    ToLower: function (value) {
        return value.toLowerCase();
    },
    Format: function (value, args) {
        var template = args.template;
        if (ramda_1.is(String, value) || ramda_1.is(Number, value) || ramda_1.is(Boolean, value)) {
            return ramda_1.replace('${value}', value, template);
        }
        else if (ramda_1.is(Object, value)) {
            return ramda_1.reduce(function (acc, _a) {
                var k = _a[0], v = _a[1];
                return ramda_1.replace("${" + k + "}", v, acc);
            }, template, ramda_1.toPairs(value));
        }
        return value;
    },
    Split: function (value, args) {
        var separator = args.separator;
        return ramda_1.split(separator, value);
    },
    Trim: function (value) {
        return ramda_1.trim(value);
    },
    /* Number Transform */
    Add: function (value, args, getAspect) {
        if (ramda_1.is(Number, args.value)) {
            return value + args.value;
        }
        return value + aspects_1.coerceAspect(args.value, getAspect);
    },
    Sub: function (value, args, getAspect) {
        if (ramda_1.is(Number, args.value)) {
            return value - args.value;
        }
        return value - aspects_1.coerceAspect(args.value, getAspect);
    },
    Divide: function (value, args, getAspect) {
        if (ramda_1.is(Number, args.value)) {
            return value / args.value;
        }
        return value / aspects_1.coerceAspect(args.value, getAspect);
    },
    Multiply: function (value, args, getAspect) {
        if (ramda_1.is(Number, args.value)) {
            return value * args.value;
        }
        return value * aspects_1.coerceAspect(args.value, getAspect);
    },
    Modulus: function (value, args, getAspect) {
        if (ramda_1.is(Number, args.value)) {
            return value % args.value;
        }
        return value % aspects_1.coerceAspect(args.value, getAspect);
    },
    ToPrecision: function (value, args) {
        return value.toPrecision(args.precision);
    },
    /* Array transforms  */
    Concat: function (value, args, getAspect) {
        var other = args.other;
        return ramda_1.concat(value, aspects_1.coerceAspect(other, getAspect));
    },
    Slice: function (value, args) {
        return ramda_1.slice(args.start, args.stop, value);
    },
    Map: function (value, args, getAspect) {
        var transform = args.transform;
        return value.map(function (e) {
            return exports.executeTransform(transform.transform, e, transform.args, transform.next, getAspect);
        });
    },
    Filter: function (value, args, getAspect) {
        var comparison = args.comparison;
        return value.filter(function (e) {
            return exports.executeTransform(comparison.transform, e, comparison.args, comparison.next, getAspect);
        });
    },
    Reduce: function (value, args, getAspect) {
        var transform = args.transform, accumulator = args.accumulator;
        var acc = aspects_1.coerceAspect(accumulator, getAspect);
        return value.reduce(function (previous, next) {
            return exports.executeTransform(transform.transform, [previous, next], transform.args, transform.next, getAspect);
        }, acc);
    },
    Pluck: function (value, args) {
        var field = args.field;
        return ramda_1.pluck(field, value);
    },
    Append: function (value, args, getAspect) {
        return ramda_1.concat(value, [aspects_1.coerceAspect(args.value, getAspect)]);
    },
    Prepend: function (value, args, getAspect) {
        return ramda_1.concat([aspects_1.coerceAspect(args.value, getAspect)], value);
    },
    Insert: function (value, args, getAspect) {
        var target = args.target, front = args.front;
        var t = aspects_1.coerceAspect(target, getAspect);
        return front ? ramda_1.concat([value], t) : ramda_1.concat(t, [value]);
    },
    Take: function (value, args, getAspect) {
        var n = args.n;
        return ramda_1.take(aspects_1.coerceAspect(n, getAspect), value);
    },
    Length: function (value) {
        return value.length;
    },
    Range: function (value, args, getAspect) {
        var start = args.start, end = args.end, step = args.step;
        var s = aspects_1.coerceAspect(start, getAspect);
        var e = aspects_1.coerceAspect(end, getAspect);
        var i = s;
        var arr = [];
        while (i < e) {
            arr.push(i);
            i += step;
        }
        return arr;
    },
    Includes: function (value, args, getAspect) {
        return ramda_1.includes(aspects_1.coerceAspect(args.value, getAspect), value);
    },
    Find: function (value, args, getAspect) {
        var comparison = args.comparison;
        return ramda_1.find(function (a) {
            return exports.executeTransform(comparison.transform, a, comparison.args, comparison.next, getAspect);
        })(value);
    },
    Join: function (value, args, getAspect) {
        return ramda_1.join(aspects_1.coerceAspect(args.separator, getAspect), value);
    },
    Sort: function (value, args, getAspect) {
        var transform = args.transform;
        return ramda_1.sort(function (a, b) {
            return exports.executeTransform(transform.transform, [a, b], transform.args, transform.next, getAspect);
        }, value);
    },
    Reverse: function (value) {
        return ramda_1.reverse(value);
    },
    Unique: function (value) {
        return ramda_1.uniq(value);
    },
    Zip: function (value, args, getAspect) {
        return ramda_1.zip(value, aspects_1.coerceAspect(args.value, getAspect));
    },
    /* Object transforms */
    Pick: function (value, args) {
        return ramda_1.pick(args.fields, value);
    },
    Get: function (value, args) {
        return value[args.field];
    },
    Set: function (v, args, getAspect) {
        var key = args.key, value = args.value;
        v[key] = aspects_1.coerceAspect(value, getAspect);
        return v;
    },
    Put: function (value, args, getAspect) {
        var key = args.key, target = args.target;
        var obj = aspects_1.coerceAspect(target, getAspect);
        obj[key] = value;
        return obj;
    },
    Merge: function (value, args, getAspect) {
        var deep = args.deep, direction = args.direction, other = args.other;
        var otherValue = other;
        if (aspects_1.isAspect(other)) {
            otherValue = getAspect(other.identity, other.aspect);
        }
        if (direction === 'right') {
            if (deep) {
                return ramda_1.mergeDeepRight(value, otherValue);
            }
            return ramda_1.mergeRight(value, otherValue);
        }
        if (deep) {
            return ramda_1.mergeDeepLeft(value, otherValue);
        }
        return ramda_1.mergeLeft(value, otherValue);
    },
    ToJson: function (value) {
        return JSON.stringify(value);
    },
    FromJson: function (value) {
        return JSON.parse(value);
    },
    ToPairs: function (value) {
        return ramda_1.toPairs(value);
    },
    FromPairs: function (value) {
        return ramda_1.fromPairs(value);
    },
    /* Conditionals */
    If: function (value, args, getAspect) {
        var comparison = args.comparison, then = args.then, otherwise = args.otherwise;
        var c = transforms[comparison.transform];
        if (c(value, comparison.args, getAspect)) {
            return exports.executeTransform(then.transform, value, then.args, then.next, getAspect);
        }
        if (otherwise) {
            return exports.executeTransform(otherwise.transform, value, otherwise.args, otherwise.next, getAspect);
        }
        return value;
    },
    Equals: function (value, args, getAspect) {
        return ramda_1.equals(value, aspects_1.coerceAspect(args.other, getAspect));
    },
    NotEquals: function (value, args, getAspect) {
        return !ramda_1.equals(value, aspects_1.coerceAspect(args.other, getAspect));
    },
    Match: function (value, args, getAspect) {
        var r = new RegExp(aspects_1.coerceAspect(args.other, getAspect));
        return r.test(value);
    },
    Greater: function (value, args, getAspect) {
        return value > aspects_1.coerceAspect(args.other, getAspect);
    },
    GreaterOrEquals: function (value, args, getAspect) {
        return value >= aspects_1.coerceAspect(args.other, getAspect);
    },
    Lesser: function (value, args, getAspect) {
        return value < aspects_1.coerceAspect(args.other, getAspect);
    },
    LesserOrEquals: function (value, args, getAspect) {
        return value <= aspects_1.coerceAspect(args.other, getAspect);
    },
    And: function (value, args, getAspect) {
        return value && aspects_1.coerceAspect(args.other, getAspect);
    },
    Or: function (value, args, getAspect) {
        return value || aspects_1.coerceAspect(args.other, getAspect);
    },
    Not: function (value) {
        return !value;
    },
    RawValue: function (value, args) {
        return args.value;
    },
    AspectValue: function (value, args, getAspect) {
        var _a = args.target, identity = _a.identity, aspect = _a.aspect;
        return getAspect(identity, aspect);
    },
};
var executeTransform = function (transform, value, args, next, getAspect) {
    var t = transforms[transform];
    var newValue = t(value, args, getAspect);
    if (next.length) {
        var n = next[0];
        return exports.executeTransform(n.transform, newValue, n.args, 
        // Execute the next first, then back to chain.
        ramda_1.concat(n.next, ramda_1.drop(1, next)), getAspect);
    }
    return newValue;
};
exports.executeTransform = executeTransform;
exports.default = transforms;


/***/ }),

/***/ "react":
/*!****************************************************************************************************!*\
  !*** external {"commonjs":"react","commonjs2":"react","amd":"react","umd":"react","root":"React"} ***!
  \****************************************************************************************************/
/***/ ((module) => {

module.exports = __WEBPACK_EXTERNAL_MODULE_react__;

/***/ }),

/***/ "react-dom":
/*!***********************************************************************************************************************!*\
  !*** external {"commonjs":"react-dom","commonjs2":"react-dom","amd":"react-dom","umd":"react-dom","root":"ReactDOM"} ***!
  \***********************************************************************************************************************/
/***/ ((module) => {

module.exports = __WEBPACK_EXTERNAL_MODULE_react_dom__;

/***/ })

},
/******/ __webpack_require__ => { // webpackRuntimeModules
/******/ var __webpack_exec__ = (moduleId) => (__webpack_require__(__webpack_require__.s = moduleId))
/******/ var __webpack_exports__ = (__webpack_exec__("./src/renderer/js/index.tsx"));
/******/ return __webpack_exports__;
/******/ }
]);
});
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJmaWxlIjoiZGF6emxlcl9yZW5kZXJlcl9iZTU5Zjg1ZDM0MjFjZmQ3YjQ2MS5qcyIsIm1hcHBpbmdzIjoiO0FBQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0EsQ0FBQztBQUNELE87Ozs7Ozs7Ozs7O0FDVkEsbUZBQThCO0FBR3ZCLElBQU0sUUFBUSxHQUFHLFVBQUMsR0FBUTtJQUM3QixpQkFBRSxDQUFDLE1BQU0sRUFBRSxHQUFHLENBQUMsSUFBSSxXQUFHLENBQUMsVUFBVSxFQUFFLEdBQUcsQ0FBQyxJQUFJLFdBQUcsQ0FBQyxRQUFRLEVBQUUsR0FBRyxDQUFDO0FBQTdELENBQTZELENBQUM7QUFEckQsZ0JBQVEsWUFDNkM7QUFFM0QsSUFBTSxZQUFZLEdBQUcsVUFDeEIsR0FBUSxFQUNSLFNBQWlDLElBQzNCLFFBQUMsZ0JBQVEsQ0FBQyxHQUFHLENBQUMsQ0FBQyxDQUFDLENBQUMsU0FBUyxDQUFDLEdBQUcsQ0FBQyxRQUFRLEVBQUUsR0FBRyxDQUFDLE1BQU0sQ0FBQyxDQUFDLENBQUMsQ0FBQyxHQUFHLENBQUMsRUFBM0QsQ0FBMkQsQ0FBQztBQUh6RCxvQkFBWSxnQkFHNkM7QUFFL0QsSUFBTSxZQUFZLEdBQUcsVUFBQyxRQUFnQixFQUFFLE1BQWM7SUFDekQsT0FBRyxNQUFNLFNBQUksUUFBVTtBQUF2QixDQUF1QixDQUFDO0FBRGYsb0JBQVksZ0JBQ0c7QUFFckIsSUFBTSxZQUFZLEdBQUcsVUFBQyxDQUFTLEVBQUUsQ0FBUztJQUM3QyxRQUFDLENBQUMsUUFBUSxLQUFLLENBQUMsQ0FBQyxRQUFRLElBQUksQ0FBQyxDQUFDLE1BQU0sS0FBSyxDQUFDLENBQUMsTUFBTTtBQUFsRCxDQUFrRCxDQUFDO0FBRDFDLG9CQUFZLGdCQUM4Qjs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7Ozs7OztBQ2Z2RCxzRUFBc0M7QUFDdEMsa0hBQWdDO0FBSWhDLElBQU0sUUFBUSxHQUFHLFVBQUMsS0FBb0I7SUFD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LElBQU0sQ0FBQyxHQUFHLElBQUksQ0FBQyxDQUFDLENBQUMsQ0FBQztRQUNsQixPQUFPLHdCQUFnQixDQUNuQixDQUFDLENBQUMsU0FBUyxFQUNYLFFBQVEsRUFDUixDQUFDLENBQUMsSUFBSTtRQUNOLDhDQUE4QztRQUM5QyxjQUFNLENBQUMsQ0FBQyxDQUFDLElBQUksRUFBRSxZQUFJLENBQUMsQ0FBQyxFQUFFLElBQUksQ0FBQyxDQUFDLEVBQzdCLFNBQVMsQ0FDWixDQUFDO0tBQ0w7SUFDRCxPQUFPLFFBQVEsQ0FBQztBQUNwQixDQUFDLENBQUM7QUFyQlcsd0JBQWdCLG9CQXFCM0I7QUFFRixrQkFBZSxVQUFVLENBQUM7Ozs7Ozs7Ozs7O0FDOVYxQjs7Ozs7Ozs7OztBQ0FBIiwic291cmNlcyI6WyJ3ZWJwYWNrOi8vLy93ZWJwYWNrL3VuaXZlcnNhbE1vZHVsZURlZmluaXRpb24/Iiwid2VicGFjazovLy8vLi9zcmMvcmVuZGVyZXIvanMvYXNwZWN0cy50cz8iLCJ3ZWJwYWNrOi8vLy8uL3NyYy9yZW5kZXJlci9qcy9jb21wb25lbnRzL1JlbmRlcmVyLnRzeD8iLCJ3ZWJwYWNrOi8vLy8uL3NyYy9yZW5kZXJlci9qcy9jb21wb25lbnRzL1VwZGF0ZXIudHN4PyIsIndlYnBhY2s6Ly8vLy4vc3JjL3JlbmRlcmVyL2pzL2NvbXBvbmVudHMvV3JhcHBlci50c3g/Iiwid2VicGFjazovLy8vLi9zcmMvcmVuZGVyZXIvanMvaHlkcmF0b3IudHN4PyIsIndlYnBhY2s6Ly8vLy4vc3JjL3JlbmRlcmVyL2pzL2luZGV4LnRzeD8iLCJ3ZWJwYWNrOi8vLy8uL3NyYy9yZW5kZXJlci9qcy9yZXF1ZXN0cy50cz8iLCJ3ZWJwYWNrOi8vLy8uL3NyYy9yZW5kZXJlci9qcy9yZXF1aXJlbWVudHMudHM/Iiwid2VicGFjazovLy8vLi9zcmMvcmVuZGVyZXIvanMvdHJhbnNmb3Jtcy50cz8iLCJ3ZWJwYWNrOi8vLy9leHRlcm5hbCB7XCJjb21tb25qc1wiOlwicmVhY3RcIixcImNvbW1vbmpzMlwiOlwicmVhY3RcIixcImFtZFwiOlwicmVhY3RcIixcInVtZFwiOlwicmVhY3RcIixcInJvb3RcIjpcIlJlYWN0XCJ9PyIsIndlYnBhY2s6Ly8vL2V4dGVybmFsIHtcImNvbW1vbmpzXCI6XCJyZWFjdC1kb21cIixcImNvbW1vbmpzMlwiOlwicmVhY3QtZG9tXCIsXCJhbWRcIjpcInJlYWN0LWRvbVwiLFwidW1kXCI6XCJyZWFjdC1kb21cIixcInJvb3RcIjpcIlJlYWN0RE9NXCJ9PyJdLCJzb3VyY2VzQ29udGVudCI6WyIoZnVuY3Rpb24gd2VicGFja1VuaXZlcnNhbE1vZHVsZURlZmluaXRpb24ocm9vdCwgZmFjdG9yeSkge1xuXHRpZih0eXBlb2YgZXhwb3J0cyA9PT0gJ29iamVjdCcgJiYgdHlwZW9mIG1vZHVsZSA9PT0gJ29iamVjdCcpXG5cdFx0bW9kdWxlLmV4cG9ydHMgPSBmYWN0b3J5KHJlcXVpcmUoXCJyZWFjdFwiKSwgcmVxdWlyZShcInJlYWN0LWRvbVwiKSk7XG5cdGVsc2UgaWYodHlwZW9mIGRlZmluZSA9PT0gJ2Z1bmN0aW9uJyAmJiBkZWZpbmUuYW1kKVxuXHRcdGRlZmluZShbXCJyZWFjdFwiLCBcInJlYWN0LWRvbVwiXSwgZmFjdG9yeSk7XG5cdGVsc2UgaWYodHlwZW9mIGV4cG9ydHMgPT09ICdvYmplY3QnKVxuXHRcdGV4cG9ydHNbXCJkYXp6bGVyX3JlbmRlcmVyXCJdID0gZmFjdG9yeShyZXF1aXJlKFwicmVhY3RcIiksIHJlcXVpcmUoXCJyZWFjdC1kb21cIikpO1xuXHRlbHNlXG5cdFx0cm9vdFtcImRhenpsZXJfcmVuZGVyZXJcIl0gPSBmYWN0b3J5KHJvb3RbXCJSZWFjdFwiXSwgcm9vdFtcIlJlYWN0RE9NXCJdKTtcbn0pKHNlbGYsIGZ1bmN0aW9uKF9fV0VCUEFDS19FWFRFUk5BTF9NT0RVTEVfcmVhY3RfXywgX19XRUJQQUNLX0VYVEVSTkFMX01PRFVMRV9yZWFjdF9kb21fXykge1xucmV0dXJuICIsImltcG9ydCB7aGFzLCBpc30gZnJvbSAncmFtZGEnO1xuaW1wb3J0IHtBc3BlY3QsIFRyYW5zZm9ybUdldEFzcGVjdEZ1bmN9IGZyb20gJy4vdHlwZXMnO1xuXG5leHBvcnQgY29uc3QgaXNBc3BlY3QgPSAob2JqOiBhbnkpOiBib29sZWFuID0+XG4gICAgaXMoT2JqZWN0LCBvYmopICYmIGhhcygnaWRlbnRpdHknLCBvYmopICYmIGhhcygnYXNwZWN0Jywgb2JqKTtcblxuZXhwb3J0IGNvbnN0IGNvZXJjZUFzcGVjdCA9IChcbiAgICBvYmo6IGFueSxcbiAgICBnZXRBc3BlY3Q6IFRyYW5zZm9ybUdldEFzcGVjdEZ1bmNcbik6IGFueSA9PiAoaXNBc3BlY3Qob2JqKSA/IGdldEFzcGVjdChvYmouaWRlbnRpdHksIG9iai5hc3BlY3QpIDogb2JqKTtcblxuZXhwb3J0IGNvbnN0IGdldEFzcGVjdEtleSA9IChpZGVudGl0eTogc3RyaW5nLCBhc3BlY3Q6IHN0cmluZyk6IHN0cmluZyA9PlxuICAgIGAke2FzcGVjdH1AJHtpZGVudGl0eX1gO1xuXG5leHBvcnQgY29uc3QgaXNTYW1lQXNwZWN0ID0gKGE6IEFzcGVjdCwgYjogQXNwZWN0KSA9PlxuICAgIGEuaWRlbnRpdHkgPT09IGIuaWRlbnRpdHkgJiYgYS5hc3BlY3QgPT09IGIuYXNwZWN0O1xuIiwiaW1wb3J0IFJlYWN0LCB7dXNlU3RhdGV9IGZyb20gJ3JlYWN0JztcbmltcG9ydCBVcGRhdGVyIGZyb20gJy4vVXBkYXRlcic7XG5cbmltcG9ydCB7UmVuZGVyT3B0aW9uc30gZnJvbSAnLi4vdHlwZXMnO1xuXG5jb25zdCBSZW5kZXJlciA9IChwcm9wczogUmVuZGVyT3B0aW9ucykgPT4ge1xuICAgIGNvbnN0IFtyZWxvYWRLZXksIHNldFJlbG9hZEtleV0gPSB1c2VTdGF0ZSgxKTtcblxuICAgIC8vIEZJWE1FIGZpbmQgd2hlcmUgdGhpcyBpcyB1c2VkIGFuZCByZWZhY3Rvci9yZW1vdmVcbiAgICAvLyBAdHMtaWdub3JlXG4gICAgd2luZG93LmRhenpsZXJfYmFzZV91cmwgPSBwcm9wcy5iYXNlVXJsO1xuICAgIHJldHVybiAoXG4gICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiZGF6emxlci1yZW5kZXJlclwiPlxuICAgICAgICAgICAgPFVwZGF0ZXJcbiAgICAgICAgICAgICAgICB7Li4ucHJvcHN9XG4gICAgICAgICAgICAgICAga2V5PXtgdXBkLSR7cmVsb2FkS2V5fWB9XG4gICAgICAgICAgICAgICAgaG90UmVsb2FkPXsoKSA9PiBzZXRSZWxvYWRLZXkocmVsb2FkS2V5ICsgMSl9XG4gICAgICAgICAgICAvPlxuICAgICAgICA8L2Rpdj5cbiAgICApO1xufTtcblxuZXhwb3J0IGRlZmF1bHQgUmVuZGVyZXI7XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IHthcGlSZXF1ZXN0fSBmcm9tICcuLi9yZXF1ZXN0cyc7XG5pbXBvcnQge1xuICAgIGh5ZHJhdGVDb21wb25lbnQsXG4gICAgaHlkcmF0ZVByb3BzLFxuICAgIGlzQ29tcG9uZW50LFxuICAgIHByZXBhcmVQcm9wLFxufSBmcm9tICcuLi9oeWRyYXRvcic7XG5pbXBvcnQge2xvYWRSZXF1aXJlbWVudCwgbG9hZFJlcXVpcmVtZW50c30gZnJvbSAnLi4vcmVxdWlyZW1lbnRzJztcbmltcG9ydCB7ZGlzYWJsZUNzc30gZnJvbSAnY29tbW9ucyc7XG5pbXBvcnQge1xuICAgIHBpY2tCeSxcbiAgICBrZXlzLFxuICAgIG1hcCxcbiAgICBldm9sdmUsXG4gICAgY29uY2F0LFxuICAgIGZsYXR0ZW4sXG4gICAgZGlzc29jLFxuICAgIHppcCxcbiAgICBhbGwsXG59IGZyb20gJ3JhbWRhJztcbmltcG9ydCB7ZXhlY3V0ZVRyYW5zZm9ybX0gZnJvbSAnLi4vdHJhbnNmb3Jtcyc7XG5pbXBvcnQge1xuICAgIEJpbmRpbmcsXG4gICAgQm91bmRDb21wb25lbnRzLFxuICAgIEV2b2x2ZWRCaW5kaW5nLFxuICAgIFRpZSxcbiAgICBVcGRhdGVyUHJvcHMsXG4gICAgVXBkYXRlclN0YXRlLFxufSBmcm9tICcuLi90eXBlcyc7XG5pbXBvcnQge2dldEFzcGVjdEtleSwgaXNTYW1lQXNwZWN0fSBmcm9tICcuLi9hc3BlY3RzJztcblxuZXhwb3J0IGRlZmF1bHQgY2xhc3MgVXBkYXRlciBleHRlbmRzIFJlYWN0LkNvbXBvbmVudDxcbiAgICBVcGRhdGVyUHJvcHMsXG4gICAgVXBkYXRlclN0YXRlXG4+IHtcbiAgICBwcml2YXRlIHBhZ2VBcGk6IEZ1bmN0aW9uO1xuICAgIHByaXZhdGUgcmVhZG9ubHkgYm91bmRDb21wb25lbnRzOiBCb3VuZENvbXBvbmVudHM7XG4gICAgcHJpdmF0ZSB3czogV2ViU29ja2V0O1xuXG4gICAgY29uc3RydWN0b3IocHJvcHMpIHtcbiAgICAgICAgc3VwZXIocHJvcHMpO1xuICAgICAgICB0aGlzLnN0YXRlID0ge1xuICAgICAgICAgICAgbGF5b3V0OiBudWxsLFxuICAgICAgICAgICAgcmVhZHk6IGZhbHNlLFxuICAgICAgICAgICAgcGFnZTogbnVsbCxcbiAgICAgICAgICAgIGJpbmRpbmdzOiB7fSxcbiAgICAgICAgICAgIHBhY2thZ2VzOiBbXSxcbiAgICAgICAgICAgIHJlbG9hZDogZmFsc2UsXG4gICAgICAgICAgICByZWJpbmRpbmdzOiBbXSxcbiAgICAgICAgICAgIHJlcXVpcmVtZW50czogW10sXG4gICAgICAgICAgICByZWxvYWRpbmc6IGZhbHNlLFxuICAgICAgICAgICAgbmVlZFJlZnJlc2g6IGZhbHNlLFxuICAgICAgICAgICAgdGllczogW10sXG4gICAgICAgIH07XG4gICAgICAgIC8vIFRoZSBhcGkgdXJsIGZvciB0aGUgcGFnZSBpcyB0aGUgc2FtZSBidXQgYSBwb3N0LlxuICAgICAgICAvLyBGZXRjaCBiaW5kaW5ncywgcGFja2FnZXMgJiByZXF1aXJlbWVudHNcbiAgICAgICAgdGhpcy5wYWdlQXBpID0gYXBpUmVxdWVzdCh3aW5kb3cubG9jYXRpb24uaHJlZik7XG4gICAgICAgIC8vIEFsbCBjb21wb25lbnRzIGdldCBjb25uZWN0ZWQuXG4gICAgICAgIHRoaXMuYm91bmRDb21wb25lbnRzID0ge307XG4gICAgICAgIHRoaXMud3MgPSBudWxsO1xuXG4gICAgICAgIHRoaXMudXBkYXRlQXNwZWN0cyA9IHRoaXMudXBkYXRlQXNwZWN0cy5iaW5kKHRoaXMpO1xuICAgICAgICB0aGlzLmNvbm5lY3QgPSB0aGlzLmNvbm5lY3QuYmluZCh0aGlzKTtcbiAgICAgICAgdGhpcy5kaXNjb25uZWN0ID0gdGhpcy5kaXNjb25uZWN0LmJpbmQodGhpcyk7XG4gICAgICAgIHRoaXMub25NZXNzYWdlID0gdGhpcy5vbk1lc3NhZ2UuYmluZCh0aGlzKTtcbiAgICB9XG5cbiAgICB1cGRhdGVBc3BlY3RzKGlkZW50aXR5OiBzdHJpbmcsIGFzcGVjdHMpIHtcbiAgICAgICAgcmV0dXJuIG5ldyBQcm9taXNlKChyZXNvbHZlKSA9PiB7XG4gICAgICAgICAgICBjb25zdCBhc3BlY3RLZXlzOiBzdHJpbmdbXSA9IGtleXM8c3RyaW5nPihhc3BlY3RzKTtcbiAgICAgICAgICAgIGxldCBiaW5kaW5nczogQmluZGluZ1tdIHwgRXZvbHZlZEJpbmRpbmdbXSA9IGFzcGVjdEtleXNcbiAgICAgICAgICAgICAgICAubWFwKChrZXk6IHN0cmluZykgPT4gKHtcbiAgICAgICAgICAgICAgICAgICAgLi4udGhpcy5zdGF0ZS5iaW5kaW5nc1tnZXRBc3BlY3RLZXkoaWRlbnRpdHksIGtleSldLFxuICAgICAgICAgICAgICAgICAgICB2YWx1ZTogYXNwZWN0c1trZXldLFxuICAgICAgICAgICAgICAgIH0pKVxuICAgICAgICAgICAgICAgIC5maWx0ZXIoKGUpID0+IGUudHJpZ2dlcik7XG5cbiAgICAgICAgICAgIHRoaXMuc3RhdGUucmViaW5kaW5ncy5mb3JFYWNoKChiaW5kaW5nKSA9PiB7XG4gICAgICAgICAgICAgICAgaWYgKGJpbmRpbmcudHJpZ2dlci5pZGVudGl0eS50ZXN0KGlkZW50aXR5KSkge1xuICAgICAgICAgICAgICAgICAgICAvLyBAdHMtaWdub3JlXG4gICAgICAgICAgICAgICAgICAgIGJpbmRpbmdzID0gY29uY2F0KFxuICAgICAgICAgICAgICAgICAgICAgICAgYmluZGluZ3MsXG4gICAgICAgICAgICAgICAgICAgICAgICBhc3BlY3RLZXlzXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgLmZpbHRlcigoazogc3RyaW5nKSA9PlxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBiaW5kaW5nLnRyaWdnZXIuYXNwZWN0LnRlc3QoaylcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICApXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgLm1hcCgoaykgPT4gKHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgLi4uYmluZGluZyxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdmFsdWU6IGFzcGVjdHNba10sXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHRyaWdnZXI6IHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC4uLmJpbmRpbmcudHJpZ2dlcixcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGlkZW50aXR5LFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgYXNwZWN0OiBrLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB9LFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIH0pKVxuICAgICAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH0pO1xuXG4gICAgICAgICAgICBjb25zdCByZW1vdmFibGVUaWVzID0gW107XG5cbiAgICAgICAgICAgIGZsYXR0ZW4oXG4gICAgICAgICAgICAgICAgYXNwZWN0S2V5cy5tYXAoKGFzcGVjdCkgPT4ge1xuICAgICAgICAgICAgICAgICAgICBjb25zdCB0aWVzID0gW107XG4gICAgICAgICAgICAgICAgICAgIGZvciAobGV0IGkgPSAwOyBpIDwgdGhpcy5zdGF0ZS50aWVzLmxlbmd0aDsgaSsrKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICBjb25zdCB0aWUgPSB0aGlzLnN0YXRlLnRpZXNbaV07XG4gICAgICAgICAgICAgICAgICAgICAgICBjb25zdCB7dHJpZ2dlcn0gPSB0aWU7XG4gICAgICAgICAgICAgICAgICAgICAgICBpZiAoXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgKHRyaWdnZXIucmVnZXggJiZcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgLy8gQHRzLWlnbm9yZVxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB0cmlnZ2VyLmlkZW50aXR5LnRlc3QoaWRlbnRpdHkpICYmXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC8vIEB0cy1pZ25vcmVcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdHJpZ2dlci5hc3BlY3QudGVzdChhc3BlY3QpKSB8fFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGlzU2FtZUFzcGVjdCh0cmlnZ2VyLCB7aWRlbnRpdHksIGFzcGVjdH0pXG4gICAgICAgICAgICAgICAgICAgICAgICApIHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB0aWVzLnB1c2goe1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAuLi50aWUsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHZhbHVlOiBhc3BlY3RzW2FzcGVjdF0sXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgfSk7XG4gICAgICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgcmV0dXJuIHRpZXM7XG4gICAgICAgICAgICAgICAgfSlcbiAgICAgICAgICAgICkuZm9yRWFjaCgodGllOiBUaWUpID0+IHtcbiAgICAgICAgICAgICAgICBjb25zdCB7dHJhbnNmb3Jtc30gPSB0aWU7XG4gICAgICAgICAgICAgICAgbGV0IHZhbHVlID0gdGllLnZhbHVlO1xuXG4gICAgICAgICAgICAgICAgaWYgKHRpZS50cmlnZ2VyLm9uY2UpIHtcbiAgICAgICAgICAgICAgICAgICAgcmVtb3ZhYmxlVGllcy5wdXNoKHRpZSk7XG4gICAgICAgICAgICAgICAgfVxuXG4gICAgICAgICAgICAgICAgaWYgKHRyYW5zZm9ybXMpIHtcbiAgICAgICAgICAgICAgICAgICAgdmFsdWUgPSB0cmFuc2Zvcm1zLnJlZHVjZSgoYWNjLCBlKSA9PiB7XG4gICAgICAgICAgICAgICAgICAgICAgICByZXR1cm4gZXhlY3V0ZVRyYW5zZm9ybShcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBlLnRyYW5zZm9ybSxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBhY2MsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgZS5hcmdzLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGUubmV4dCxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB0aGlzLmdldEFzcGVjdC5iaW5kKHRoaXMpXG4gICAgICAgICAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgICAgICAgICB9LCB2YWx1ZSk7XG4gICAgICAgICAgICAgICAgfVxuXG4gICAgICAgICAgICAgICAgdGllLnRhcmdldHMuZm9yRWFjaCgodCkgPT4ge1xuICAgICAgICAgICAgICAgICAgICBjb25zdCBjb21wb25lbnQgPSB0aGlzLmJvdW5kQ29tcG9uZW50c1t0LmlkZW50aXR5XTtcbiAgICAgICAgICAgICAgICAgICAgaWYgKGNvbXBvbmVudCkge1xuICAgICAgICAgICAgICAgICAgICAgICAgY29tcG9uZW50LnVwZGF0ZUFzcGVjdHMoe1t0LmFzcGVjdF06IHZhbHVlfSk7XG4gICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICB9KTtcbiAgICAgICAgICAgIH0pO1xuXG4gICAgICAgICAgICBpZiAocmVtb3ZhYmxlVGllcy5sZW5ndGgpIHtcbiAgICAgICAgICAgICAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgICAgICAgICAgICAgICAgdGllczogdGhpcy5zdGF0ZS50aWVzLmZpbHRlcihcbiAgICAgICAgICAgICAgICAgICAgICAgICh0KSA9PlxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICFyZW1vdmFibGVUaWVzLnJlZHVjZShcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgKGFjYywgdGllKSA9PlxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgYWNjIHx8XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAoaXNTYW1lQXNwZWN0KHQudHJpZ2dlciwgdGllLnRyaWdnZXIpICYmXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgYWxsKChbdDEsIHQyXSkgPT4gaXNTYW1lQXNwZWN0KHQxLCB0MikpKFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB6aXAodC50YXJnZXRzLCB0aWUudGFyZ2V0cylcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICApKSxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZmFsc2VcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICApXG4gICAgICAgICAgICAgICAgICAgICksXG4gICAgICAgICAgICAgICAgfSk7XG4gICAgICAgICAgICB9XG5cbiAgICAgICAgICAgIGlmICghYmluZGluZ3MpIHtcbiAgICAgICAgICAgICAgICByZXNvbHZlKDApO1xuICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICBjb25zdCByZW1vdmFibGVCaW5kaW5ncyA9IFtdO1xuICAgICAgICAgICAgICAgIGJpbmRpbmdzLmZvckVhY2goKGJpbmRpbmcpID0+IHtcbiAgICAgICAgICAgICAgICAgICAgdGhpcy5zZW5kQmluZGluZyhiaW5kaW5nLCBiaW5kaW5nLnZhbHVlKTtcbiAgICAgICAgICAgICAgICAgICAgaWYgKGJpbmRpbmcudHJpZ2dlci5vbmNlKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICByZW1vdmFibGVCaW5kaW5ncy5wdXNoKGJpbmRpbmcpO1xuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgfSk7XG4gICAgICAgICAgICAgICAgaWYgKHJlbW92YWJsZUJpbmRpbmdzLmxlbmd0aCkge1xuICAgICAgICAgICAgICAgICAgICB0aGlzLnNldFN0YXRlKHtcbiAgICAgICAgICAgICAgICAgICAgICAgIGJpbmRpbmdzOiByZW1vdmFibGVCaW5kaW5ncy5yZWR1Y2UoXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgKGFjYywgYmluZGluZykgPT5cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZGlzc29jKFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgZ2V0QXNwZWN0S2V5KFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGJpbmRpbmcudHJpZ2dlci5pZGVudGl0eSxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICBiaW5kaW5nLnRyaWdnZXIuYXNwZWN0XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICApLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgYWNjXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICksXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy5zdGF0ZS5iaW5kaW5nc1xuICAgICAgICAgICAgICAgICAgICAgICAgKSxcbiAgICAgICAgICAgICAgICAgICAgfSk7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIC8vIFRPRE8gaW52ZXN0aWdhdGUgcmVhc29ucy91c2VzIG9mIHByb21pc2VcbiAgICAgICAgICAgICAgICByZXNvbHZlKGJpbmRpbmdzLmxlbmd0aCk7XG4gICAgICAgICAgICB9XG4gICAgICAgIH0pO1xuICAgIH1cblxuICAgIGdldEFzcGVjdDxUPihpZGVudGl0eTogc3RyaW5nLCBhc3BlY3Q6IHN0cmluZyk6IFQgfCB1bmRlZmluZWQge1xuICAgICAgICBjb25zdCBjID0gdGhpcy5ib3VuZENvbXBvbmVudHNbaWRlbnRpdHldO1xuICAgICAgICBpZiAoYykge1xuICAgICAgICAgICAgcmV0dXJuIGMuZ2V0QXNwZWN0KGFzcGVjdCk7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIHVuZGVmaW5lZDtcbiAgICB9XG5cbiAgICBjb25uZWN0KGlkZW50aXR5LCBzZXRBc3BlY3RzLCBnZXRBc3BlY3QsIG1hdGNoQXNwZWN0cywgdXBkYXRlQXNwZWN0cykge1xuICAgICAgICB0aGlzLmJvdW5kQ29tcG9uZW50c1tpZGVudGl0eV0gPSB7XG4gICAgICAgICAgICBzZXRBc3BlY3RzLFxuICAgICAgICAgICAgZ2V0QXNwZWN0LFxuICAgICAgICAgICAgbWF0Y2hBc3BlY3RzLFxuICAgICAgICAgICAgdXBkYXRlQXNwZWN0cyxcbiAgICAgICAgfTtcbiAgICB9XG5cbiAgICBkaXNjb25uZWN0KGlkZW50aXR5KSB7XG4gICAgICAgIGRlbGV0ZSB0aGlzLmJvdW5kQ29tcG9uZW50c1tpZGVudGl0eV07XG4gICAgfVxuXG4gICAgb25NZXNzYWdlKHJlc3BvbnNlKSB7XG4gICAgICAgIGNvbnN0IGRhdGEgPSBKU09OLnBhcnNlKHJlc3BvbnNlLmRhdGEpO1xuICAgICAgICBjb25zdCB7aWRlbnRpdHksIGtpbmQsIHBheWxvYWQsIHN0b3JhZ2UsIHJlcXVlc3RfaWR9ID0gZGF0YTtcbiAgICAgICAgbGV0IHN0b3JlO1xuICAgICAgICBpZiAoc3RvcmFnZSA9PT0gJ3Nlc3Npb24nKSB7XG4gICAgICAgICAgICBzdG9yZSA9IHdpbmRvdy5zZXNzaW9uU3RvcmFnZTtcbiAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgIHN0b3JlID0gd2luZG93LmxvY2FsU3RvcmFnZTtcbiAgICAgICAgfVxuICAgICAgICBzd2l0Y2ggKGtpbmQpIHtcbiAgICAgICAgICAgIGNhc2UgJ3NldC1hc3BlY3QnOlxuICAgICAgICAgICAgICAgIGNvbnN0IHNldEFzcGVjdHMgPSAoY29tcG9uZW50KSA9PlxuICAgICAgICAgICAgICAgICAgICBjb21wb25lbnRcbiAgICAgICAgICAgICAgICAgICAgICAgIC5zZXRBc3BlY3RzKFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGh5ZHJhdGVQcm9wcyhcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgcGF5bG9hZCxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdGhpcy51cGRhdGVBc3BlY3RzLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB0aGlzLmNvbm5lY3QsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMuZGlzY29ubmVjdFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIClcbiAgICAgICAgICAgICAgICAgICAgICAgIClcbiAgICAgICAgICAgICAgICAgICAgICAgIC50aGVuKCgpID0+IHRoaXMudXBkYXRlQXNwZWN0cyhpZGVudGl0eSwgcGF5bG9hZCkpO1xuICAgICAgICAgICAgICAgIGlmIChkYXRhLnJlZ2V4KSB7XG4gICAgICAgICAgICAgICAgICAgIGNvbnN0IHBhdHRlcm4gPSBuZXcgUmVnRXhwKGRhdGEuaWRlbnRpdHkpO1xuICAgICAgICAgICAgICAgICAgICBrZXlzKHRoaXMuYm91bmRDb21wb25lbnRzKVxuICAgICAgICAgICAgICAgICAgICAgICAgLmZpbHRlcigoazogc3RyaW5nKSA9PiBwYXR0ZXJuLnRlc3QoaykpXG4gICAgICAgICAgICAgICAgICAgICAgICAubWFwKChrKSA9PiB0aGlzLmJvdW5kQ29tcG9uZW50c1trXSlcbiAgICAgICAgICAgICAgICAgICAgICAgIC5mb3JFYWNoKHNldEFzcGVjdHMpO1xuICAgICAgICAgICAgICAgIH0gZWxzZSB7XG4gICAgICAgICAgICAgICAgICAgIHNldEFzcGVjdHModGhpcy5ib3VuZENvbXBvbmVudHNbaWRlbnRpdHldKTtcbiAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgYnJlYWs7XG4gICAgICAgICAgICBjYXNlICdnZXQtYXNwZWN0JzpcbiAgICAgICAgICAgICAgICBjb25zdCB7YXNwZWN0fSA9IGRhdGE7XG4gICAgICAgICAgICAgICAgY29uc3Qgd2FudGVkID0gdGhpcy5ib3VuZENvbXBvbmVudHNbaWRlbnRpdHldO1xuICAgICAgICAgICAgICAgIGlmICghd2FudGVkKSB7XG4gICAgICAgICAgICAgICAgICAgIHRoaXMud3Muc2VuZChcbiAgICAgICAgICAgICAgICAgICAgICAgIEpTT04uc3RyaW5naWZ5KHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBraW5kLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGlkZW50aXR5LFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGFzcGVjdCxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICByZXF1ZXN0X2lkLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGVycm9yOiBgQXNwZWN0IG5vdCBmb3VuZCAke2lkZW50aXR5fS4ke2FzcGVjdH1gLFxuICAgICAgICAgICAgICAgICAgICAgICAgfSlcbiAgICAgICAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgICAgICAgICAgcmV0dXJuO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICBjb25zdCB2YWx1ZSA9IHdhbnRlZC5nZXRBc3BlY3QoYXNwZWN0KTtcbiAgICAgICAgICAgICAgICB0aGlzLndzLnNlbmQoXG4gICAgICAgICAgICAgICAgICAgIEpTT04uc3RyaW5naWZ5KHtcbiAgICAgICAgICAgICAgICAgICAgICAgIGtpbmQsXG4gICAgICAgICAgICAgICAgICAgICAgICBpZGVudGl0eSxcbiAgICAgICAgICAgICAgICAgICAgICAgIGFzcGVjdCxcbiAgICAgICAgICAgICAgICAgICAgICAgIHZhbHVlOiBwcmVwYXJlUHJvcCh2YWx1ZSksXG4gICAgICAgICAgICAgICAgICAgICAgICByZXF1ZXN0X2lkLFxuICAgICAgICAgICAgICAgICAgICB9KVxuICAgICAgICAgICAgICAgICk7XG4gICAgICAgICAgICAgICAgYnJlYWs7XG4gICAgICAgICAgICBjYXNlICdzZXQtc3RvcmFnZSc6XG4gICAgICAgICAgICAgICAgc3RvcmUuc2V0SXRlbShpZGVudGl0eSwgSlNPTi5zdHJpbmdpZnkocGF5bG9hZCkpO1xuICAgICAgICAgICAgICAgIGJyZWFrO1xuICAgICAgICAgICAgY2FzZSAnZ2V0LXN0b3JhZ2UnOlxuICAgICAgICAgICAgICAgIHRoaXMud3Muc2VuZChcbiAgICAgICAgICAgICAgICAgICAgSlNPTi5zdHJpbmdpZnkoe1xuICAgICAgICAgICAgICAgICAgICAgICAga2luZCxcbiAgICAgICAgICAgICAgICAgICAgICAgIGlkZW50aXR5LFxuICAgICAgICAgICAgICAgICAgICAgICAgcmVxdWVzdF9pZCxcbiAgICAgICAgICAgICAgICAgICAgICAgIHZhbHVlOiBKU09OLnBhcnNlKHN0b3JlLmdldEl0ZW0oaWRlbnRpdHkpKSxcbiAgICAgICAgICAgICAgICAgICAgfSlcbiAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgICAgIGJyZWFrO1xuICAgICAgICAgICAgY2FzZSAncmVsb2FkJzpcbiAgICAgICAgICAgICAgICBjb25zdCB7ZmlsZW5hbWVzLCBob3QsIHJlZnJlc2gsIGRlbGV0ZWR9ID0gZGF0YTtcbiAgICAgICAgICAgICAgICBpZiAocmVmcmVzaCkge1xuICAgICAgICAgICAgICAgICAgICB0aGlzLndzLmNsb3NlKCk7XG4gICAgICAgICAgICAgICAgICAgIHRoaXMuc2V0U3RhdGUoe3JlbG9hZGluZzogdHJ1ZSwgbmVlZFJlZnJlc2g6IHRydWV9KTtcbiAgICAgICAgICAgICAgICAgICAgcmV0dXJuO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICBpZiAoaG90KSB7XG4gICAgICAgICAgICAgICAgICAgIC8vIFRoZSB3cyBjb25uZWN0aW9uIHdpbGwgY2xvc2UsIHdoZW4gaXRcbiAgICAgICAgICAgICAgICAgICAgLy8gcmVjb25uZWN0IGl0IHdpbGwgZG8gYSBoYXJkIHJlbG9hZCBvZiB0aGUgcGFnZSBhcGkuXG4gICAgICAgICAgICAgICAgICAgIHRoaXMuc2V0U3RhdGUoe3JlbG9hZGluZzogdHJ1ZX0pO1xuICAgICAgICAgICAgICAgICAgICByZXR1cm47XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgIGZpbGVuYW1lcy5mb3JFYWNoKGxvYWRSZXF1aXJlbWVudCk7XG4gICAgICAgICAgICAgICAgZGVsZXRlZC5mb3JFYWNoKChyKSA9PiBkaXNhYmxlQ3NzKHIudXJsKSk7XG4gICAgICAgICAgICAgICAgYnJlYWs7XG4gICAgICAgICAgICBjYXNlICdwaW5nJzpcbiAgICAgICAgICAgICAgICAvLyBKdXN0IGRvIG5vdGhpbmcuXG4gICAgICAgICAgICAgICAgYnJlYWs7XG4gICAgICAgIH1cbiAgICB9XG5cbiAgICBzZW5kQmluZGluZyhiaW5kaW5nLCB2YWx1ZSkge1xuICAgICAgICAvLyBDb2xsZWN0IGFsbCB2YWx1ZXMgYW5kIHNlbmQgYSBiaW5kaW5nIHBheWxvYWRcbiAgICAgICAgY29uc3QgdHJpZ2dlciA9IHtcbiAgICAgICAgICAgIC4uLmJpbmRpbmcudHJpZ2dlcixcbiAgICAgICAgICAgIHZhbHVlOiBwcmVwYXJlUHJvcCh2YWx1ZSksXG4gICAgICAgIH07XG4gICAgICAgIGNvbnN0IHN0YXRlcyA9IGJpbmRpbmcuc3RhdGVzLnJlZHVjZSgoYWNjLCBzdGF0ZSkgPT4ge1xuICAgICAgICAgICAgaWYgKHN0YXRlLnJlZ2V4KSB7XG4gICAgICAgICAgICAgICAgY29uc3QgaWRlbnRpdHlQYXR0ZXJuID0gbmV3IFJlZ0V4cChzdGF0ZS5pZGVudGl0eSk7XG4gICAgICAgICAgICAgICAgY29uc3QgYXNwZWN0UGF0dGVybiA9IG5ldyBSZWdFeHAoc3RhdGUuYXNwZWN0KTtcbiAgICAgICAgICAgICAgICByZXR1cm4gY29uY2F0KFxuICAgICAgICAgICAgICAgICAgICBhY2MsXG4gICAgICAgICAgICAgICAgICAgIGZsYXR0ZW4oXG4gICAgICAgICAgICAgICAgICAgICAgICBrZXlzKHRoaXMuYm91bmRDb21wb25lbnRzKS5tYXAoKGs6IHN0cmluZykgPT4ge1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGxldCB2YWx1ZXMgPSBbXTtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBpZiAoaWRlbnRpdHlQYXR0ZXJuLnRlc3QoaykpIHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdmFsdWVzID0gdGhpcy5ib3VuZENvbXBvbmVudHNba11cbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC5tYXRjaEFzcGVjdHMoYXNwZWN0UGF0dGVybilcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC5tYXAoKFtuYW1lLCB2YWxdKSA9PiAoe1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIC4uLnN0YXRlLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGlkZW50aXR5OiBrLFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGFzcGVjdDogbmFtZSxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB2YWx1ZTogcHJlcGFyZVByb3AodmFsKSxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIH0pKTtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgcmV0dXJuIHZhbHVlcztcbiAgICAgICAgICAgICAgICAgICAgICAgIH0pXG4gICAgICAgICAgICAgICAgICAgIClcbiAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgfVxuXG4gICAgICAgICAgICBhY2MucHVzaCh7XG4gICAgICAgICAgICAgICAgLi4uc3RhdGUsXG4gICAgICAgICAgICAgICAgdmFsdWU6XG4gICAgICAgICAgICAgICAgICAgIHRoaXMuYm91bmRDb21wb25lbnRzW3N0YXRlLmlkZW50aXR5XSAmJlxuICAgICAgICAgICAgICAgICAgICBwcmVwYXJlUHJvcChcbiAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMuYm91bmRDb21wb25lbnRzW3N0YXRlLmlkZW50aXR5XS5nZXRBc3BlY3QoXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgc3RhdGUuYXNwZWN0XG4gICAgICAgICAgICAgICAgICAgICAgICApXG4gICAgICAgICAgICAgICAgICAgICksXG4gICAgICAgICAgICB9KTtcbiAgICAgICAgICAgIHJldHVybiBhY2M7XG4gICAgICAgIH0sIFtdKTtcblxuICAgICAgICBjb25zdCBwYXlsb2FkID0ge1xuICAgICAgICAgICAgdHJpZ2dlcixcbiAgICAgICAgICAgIHN0YXRlcyxcbiAgICAgICAgICAgIGtpbmQ6ICdiaW5kaW5nJyxcbiAgICAgICAgICAgIHBhZ2U6IHRoaXMuc3RhdGUucGFnZSxcbiAgICAgICAgICAgIGtleTogYmluZGluZy5rZXksXG4gICAgICAgIH07XG4gICAgICAgIHRoaXMud3Muc2VuZChKU09OLnN0cmluZ2lmeShwYXlsb2FkKSk7XG4gICAgfVxuXG4gICAgX2Nvbm5lY3RXUygpIHtcbiAgICAgICAgLy8gU2V0dXAgd2Vic29ja2V0IGZvciB1cGRhdGVzXG4gICAgICAgIGxldCB0cmllcyA9IDA7XG4gICAgICAgIGxldCBoYXJkQ2xvc2UgPSBmYWxzZTtcbiAgICAgICAgY29uc3QgY29ubmV4aW9uID0gKCkgPT4ge1xuICAgICAgICAgICAgY29uc3QgdXJsID0gYHdzJHtcbiAgICAgICAgICAgICAgICB3aW5kb3cubG9jYXRpb24uaHJlZi5zdGFydHNXaXRoKCdodHRwcycpID8gJ3MnIDogJydcbiAgICAgICAgICAgIH06Ly8ke1xuICAgICAgICAgICAgICAgICh0aGlzLnByb3BzLmJhc2VVcmwgJiYgdGhpcy5wcm9wcy5iYXNlVXJsKSB8fFxuICAgICAgICAgICAgICAgIHdpbmRvdy5sb2NhdGlvbi5ob3N0XG4gICAgICAgICAgICB9LyR7dGhpcy5zdGF0ZS5wYWdlfS93c2A7XG4gICAgICAgICAgICB0aGlzLndzID0gbmV3IFdlYlNvY2tldCh1cmwpO1xuICAgICAgICAgICAgdGhpcy53cy5hZGRFdmVudExpc3RlbmVyKCdtZXNzYWdlJywgdGhpcy5vbk1lc3NhZ2UpO1xuICAgICAgICAgICAgdGhpcy53cy5vbm9wZW4gPSAoKSA9PiB7XG4gICAgICAgICAgICAgICAgaWYgKHRoaXMuc3RhdGUucmVsb2FkaW5nKSB7XG4gICAgICAgICAgICAgICAgICAgIGhhcmRDbG9zZSA9IHRydWU7XG4gICAgICAgICAgICAgICAgICAgIHRoaXMud3MuY2xvc2UoKTtcbiAgICAgICAgICAgICAgICAgICAgaWYgKHRoaXMuc3RhdGUubmVlZFJlZnJlc2gpIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIHdpbmRvdy5sb2NhdGlvbi5yZWxvYWQoKTtcbiAgICAgICAgICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMucHJvcHMuaG90UmVsb2FkKCk7XG4gICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgICAgICB0aGlzLnNldFN0YXRlKHtyZWFkeTogdHJ1ZX0pO1xuICAgICAgICAgICAgICAgICAgICB0cmllcyA9IDA7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfTtcbiAgICAgICAgICAgIHRoaXMud3Mub25jbG9zZSA9ICgpID0+IHtcbiAgICAgICAgICAgICAgICBjb25zdCByZWNvbm5lY3QgPSAoKSA9PiB7XG4gICAgICAgICAgICAgICAgICAgIHRyaWVzKys7XG4gICAgICAgICAgICAgICAgICAgIGNvbm5leGlvbigpO1xuICAgICAgICAgICAgICAgIH07XG4gICAgICAgICAgICAgICAgaWYgKCFoYXJkQ2xvc2UgJiYgdHJpZXMgPCB0aGlzLnByb3BzLnJldHJpZXMpIHtcbiAgICAgICAgICAgICAgICAgICAgc2V0VGltZW91dChyZWNvbm5lY3QsIDEwMDApO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgIH07XG4gICAgICAgIH07XG4gICAgICAgIGNvbm5leGlvbigpO1xuICAgIH1cblxuICAgIGNvbXBvbmVudERpZE1vdW50KCkge1xuICAgICAgICB0aGlzLnBhZ2VBcGkoJycsIHttZXRob2Q6ICdQT1NUJ30pLnRoZW4oKHJlc3BvbnNlKSA9PiB7XG4gICAgICAgICAgICBjb25zdCB0b1JlZ2V4ID0gKHgpID0+IG5ldyBSZWdFeHAoeCk7XG4gICAgICAgICAgICB0aGlzLnNldFN0YXRlKFxuICAgICAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgICAgICAgcGFnZTogcmVzcG9uc2UucGFnZSxcbiAgICAgICAgICAgICAgICAgICAgbGF5b3V0OiByZXNwb25zZS5sYXlvdXQsXG4gICAgICAgICAgICAgICAgICAgIGJpbmRpbmdzOiBwaWNrQnkoKGIpID0+ICFiLnJlZ2V4LCByZXNwb25zZS5iaW5kaW5ncyksXG4gICAgICAgICAgICAgICAgICAgIC8vIFJlZ2V4IGJpbmRpbmdzIHRyaWdnZXJzXG4gICAgICAgICAgICAgICAgICAgIHJlYmluZGluZ3M6IG1hcCgoeCkgPT4ge1xuICAgICAgICAgICAgICAgICAgICAgICAgY29uc3QgYmluZGluZyA9IHJlc3BvbnNlLmJpbmRpbmdzW3hdO1xuICAgICAgICAgICAgICAgICAgICAgICAgYmluZGluZy50cmlnZ2VyID0gZXZvbHZlKFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgaWRlbnRpdHk6IHRvUmVnZXgsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIGFzcGVjdDogdG9SZWdleCxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB9LFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGJpbmRpbmcudHJpZ2dlclxuICAgICAgICAgICAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgICAgICAgICAgICAgIHJldHVybiBiaW5kaW5nO1xuICAgICAgICAgICAgICAgICAgICB9LCBrZXlzKHBpY2tCeSgoYikgPT4gYi5yZWdleCwgcmVzcG9uc2UuYmluZGluZ3MpKSksXG4gICAgICAgICAgICAgICAgICAgIHBhY2thZ2VzOiByZXNwb25zZS5wYWNrYWdlcyxcbiAgICAgICAgICAgICAgICAgICAgcmVxdWlyZW1lbnRzOiByZXNwb25zZS5yZXF1aXJlbWVudHMsXG4gICAgICAgICAgICAgICAgICAgIHRpZXM6IG1hcCgodGllKSA9PiB7XG4gICAgICAgICAgICAgICAgICAgICAgICBpZiAodGllLnRyaWdnZXIucmVnZXgpIHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICByZXR1cm4gZXZvbHZlKFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICB0cmlnZ2VyOiB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgaWRlbnRpdHk6IHRvUmVnZXgsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgYXNwZWN0OiB0b1JlZ2V4LFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgfSxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgfSxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgdGllXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgICAgIHJldHVybiB0aWU7XG4gICAgICAgICAgICAgICAgICAgIH0sIHJlc3BvbnNlLnRpZXMpLFxuICAgICAgICAgICAgICAgIH0sXG4gICAgICAgICAgICAgICAgKCkgPT5cbiAgICAgICAgICAgICAgICAgICAgbG9hZFJlcXVpcmVtZW50cyhcbiAgICAgICAgICAgICAgICAgICAgICAgIHJlc3BvbnNlLnJlcXVpcmVtZW50cyxcbiAgICAgICAgICAgICAgICAgICAgICAgIHJlc3BvbnNlLnBhY2thZ2VzXG4gICAgICAgICAgICAgICAgICAgICkudGhlbigoKSA9PiB7XG4gICAgICAgICAgICAgICAgICAgICAgICBpZiAoa2V5cyhyZXNwb25zZS5iaW5kaW5ncykubGVuZ3RoIHx8IHJlc3BvbnNlLnJlbG9hZCkge1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIHRoaXMuX2Nvbm5lY3RXUygpO1xuICAgICAgICAgICAgICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICB0aGlzLnNldFN0YXRlKHtyZWFkeTogdHJ1ZX0pO1xuICAgICAgICAgICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgICAgICAgICB9KVxuICAgICAgICAgICAgKTtcbiAgICAgICAgfSk7XG4gICAgfVxuXG4gICAgcmVuZGVyKCkge1xuICAgICAgICBjb25zdCB7bGF5b3V0LCByZWFkeSwgcmVsb2FkaW5nfSA9IHRoaXMuc3RhdGU7XG4gICAgICAgIGlmICghcmVhZHkpIHtcbiAgICAgICAgICAgIHJldHVybiAoXG4gICAgICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJkYXp6bGVyLWxvYWRpbmctY29udGFpbmVyXCI+XG4gICAgICAgICAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiZGF6emxlci1zcGluXCIgLz5cbiAgICAgICAgICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJkYXp6bGVyLWxvYWRpbmdcIj5Mb2FkaW5nLi4uPC9kaXY+XG4gICAgICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgICApO1xuICAgICAgICB9XG4gICAgICAgIGlmIChyZWxvYWRpbmcpIHtcbiAgICAgICAgICAgIHJldHVybiAoXG4gICAgICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJkYXp6bGVyLWxvYWRpbmctY29udGFpbmVyXCI+XG4gICAgICAgICAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiZGF6emxlci1zcGluIHJlbG9hZFwiIC8+XG4gICAgICAgICAgICAgICAgICAgIDxkaXYgY2xhc3NOYW1lPVwiZGF6emxlci1sb2FkaW5nXCI+UmVsb2FkaW5nLi4uPC9kaXY+XG4gICAgICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICAgICApO1xuICAgICAgICB9XG4gICAgICAgIGlmICghaXNDb21wb25lbnQobGF5b3V0KSkge1xuICAgICAgICAgICAgdGhyb3cgbmV3IEVycm9yKGBMYXlvdXQgaXMgbm90IGEgY29tcG9uZW50OiAke2xheW91dH1gKTtcbiAgICAgICAgfVxuXG4gICAgICAgIGNvbnN0IGNvbnRleHRzID0gW107XG5cbiAgICAgICAgY29uc3Qgb25Db250ZXh0ID0gKGNvbnRleHRDb21wb25lbnQpID0+IHtcbiAgICAgICAgICAgIGNvbnRleHRzLnB1c2goY29udGV4dENvbXBvbmVudCk7XG4gICAgICAgIH07XG5cbiAgICAgICAgY29uc3QgaHlkcmF0ZWQgPSBoeWRyYXRlQ29tcG9uZW50KFxuICAgICAgICAgICAgbGF5b3V0Lm5hbWUsXG4gICAgICAgICAgICBsYXlvdXQucGFja2FnZSxcbiAgICAgICAgICAgIGxheW91dC5pZGVudGl0eSxcbiAgICAgICAgICAgIGh5ZHJhdGVQcm9wcyhcbiAgICAgICAgICAgICAgICBsYXlvdXQuYXNwZWN0cyxcbiAgICAgICAgICAgICAgICB0aGlzLnVwZGF0ZUFzcGVjdHMsXG4gICAgICAgICAgICAgICAgdGhpcy5jb25uZWN0LFxuICAgICAgICAgICAgICAgIHRoaXMuZGlzY29ubmVjdCxcbiAgICAgICAgICAgICAgICBvbkNvbnRleHRcbiAgICAgICAgICAgICksXG4gICAgICAgICAgICB0aGlzLnVwZGF0ZUFzcGVjdHMsXG4gICAgICAgICAgICB0aGlzLmNvbm5lY3QsXG4gICAgICAgICAgICB0aGlzLmRpc2Nvbm5lY3QsXG4gICAgICAgICAgICBvbkNvbnRleHRcbiAgICAgICAgKTtcblxuICAgICAgICByZXR1cm4gKFxuICAgICAgICAgICAgPGRpdiBjbGFzc05hbWU9XCJkYXp6bGVyLXJlbmRlcmVkXCI+XG4gICAgICAgICAgICAgICAge2NvbnRleHRzLmxlbmd0aFxuICAgICAgICAgICAgICAgICAgICA/IGNvbnRleHRzLnJlZHVjZSgoYWNjLCBDb250ZXh0KSA9PiB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgIGlmICghYWNjKSB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgICByZXR1cm4gPENvbnRleHQ+e2h5ZHJhdGVkfTwvQ29udGV4dD47XG4gICAgICAgICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgICAgICAgcmV0dXJuIDxDb250ZXh0PnthY2N9PC9Db250ZXh0PjtcbiAgICAgICAgICAgICAgICAgICAgICB9LCBudWxsKVxuICAgICAgICAgICAgICAgICAgICA6IGh5ZHJhdGVkfVxuICAgICAgICAgICAgPC9kaXY+XG4gICAgICAgICk7XG4gICAgfVxufVxuIiwiaW1wb3J0IFJlYWN0IGZyb20gJ3JlYWN0JztcbmltcG9ydCB7Y29uY2F0LCBqb2luLCBrZXlzfSBmcm9tICdyYW1kYSc7XG5pbXBvcnQge2NhbWVsVG9TcGluYWx9IGZyb20gJ2NvbW1vbnMnO1xuaW1wb3J0IHtXcmFwcGVyUHJvcHMsIFdyYXBwZXJTdGF0ZX0gZnJvbSAnLi4vdHlwZXMnO1xuXG4vKipcbiAqIFdyYXBzIGNvbXBvbmVudHMgZm9yIGFzcGVjdHMgdXBkYXRpbmcuXG4gKi9cbmV4cG9ydCBkZWZhdWx0IGNsYXNzIFdyYXBwZXIgZXh0ZW5kcyBSZWFjdC5Db21wb25lbnQ8XG4gICAgV3JhcHBlclByb3BzLFxuICAgIFdyYXBwZXJTdGF0ZVxuPiB7XG4gICAgY29uc3RydWN0b3IocHJvcHMpIHtcbiAgICAgICAgc3VwZXIocHJvcHMpO1xuICAgICAgICB0aGlzLnN0YXRlID0ge1xuICAgICAgICAgICAgYXNwZWN0czogcHJvcHMuYXNwZWN0cyB8fCB7fSxcbiAgICAgICAgICAgIHJlYWR5OiBmYWxzZSxcbiAgICAgICAgICAgIGluaXRpYWw6IGZhbHNlLFxuICAgICAgICB9O1xuICAgICAgICB0aGlzLnNldEFzcGVjdHMgPSB0aGlzLnNldEFzcGVjdHMuYmluZCh0aGlzKTtcbiAgICAgICAgdGhpcy5nZXRBc3BlY3QgPSB0aGlzLmdldEFzcGVjdC5iaW5kKHRoaXMpO1xuICAgICAgICB0aGlzLnVwZGF0ZUFzcGVjdHMgPSB0aGlzLnVwZGF0ZUFzcGVjdHMuYmluZCh0aGlzKTtcbiAgICAgICAgdGhpcy5tYXRjaEFzcGVjdHMgPSB0aGlzLm1hdGNoQXNwZWN0cy5iaW5kKHRoaXMpO1xuICAgIH1cblxuICAgIHVwZGF0ZUFzcGVjdHMoYXNwZWN0cykge1xuICAgICAgICByZXR1cm4gdGhpcy5zZXRBc3BlY3RzKGFzcGVjdHMpLnRoZW4oKCkgPT5cbiAgICAgICAgICAgIHRoaXMucHJvcHMudXBkYXRlQXNwZWN0cyh0aGlzLnByb3BzLmlkZW50aXR5LCBhc3BlY3RzKVxuICAgICAgICApO1xuICAgIH1cblxuICAgIHNldEFzcGVjdHMoYXNwZWN0cykge1xuICAgICAgICByZXR1cm4gbmV3IFByb21pc2U8dm9pZD4oKHJlc29sdmUpID0+IHtcbiAgICAgICAgICAgIHRoaXMuc2V0U3RhdGUoXG4gICAgICAgICAgICAgICAge2FzcGVjdHM6IHsuLi50aGlzLnN0YXRlLmFzcGVjdHMsIC4uLmFzcGVjdHN9fSxcbiAgICAgICAgICAgICAgICByZXNvbHZlXG4gICAgICAgICAgICApO1xuICAgICAgICB9KTtcbiAgICB9XG5cbiAgICBnZXRBc3BlY3QoYXNwZWN0KSB7XG4gICAgICAgIHJldHVybiB0aGlzLnN0YXRlLmFzcGVjdHNbYXNwZWN0XTtcbiAgICB9XG5cbiAgICBtYXRjaEFzcGVjdHMocGF0dGVybikge1xuICAgICAgICByZXR1cm4ga2V5cyh0aGlzLnN0YXRlLmFzcGVjdHMpXG4gICAgICAgICAgICAuZmlsdGVyKChrKSA9PiBwYXR0ZXJuLnRlc3QoaykpXG4gICAgICAgICAgICAubWFwKChrKSA9PiBbaywgdGhpcy5zdGF0ZS5hc3BlY3RzW2tdXSk7XG4gICAgfVxuXG4gICAgY29tcG9uZW50RGlkTW91bnQoKSB7XG4gICAgICAgIC8vIE9ubHkgdXBkYXRlIHRoZSBjb21wb25lbnQgd2hlbiBtb3VudGVkLlxuICAgICAgICAvLyBPdGhlcndpc2UgZ2V0cyBhIHJhY2UgY29uZGl0aW9uIHdpdGggd2lsbFVubW91bnRcbiAgICAgICAgdGhpcy5wcm9wcy5jb25uZWN0KFxuICAgICAgICAgICAgdGhpcy5wcm9wcy5pZGVudGl0eSxcbiAgICAgICAgICAgIHRoaXMuc2V0QXNwZWN0cyxcbiAgICAgICAgICAgIHRoaXMuZ2V0QXNwZWN0LFxuICAgICAgICAgICAgdGhpcy5tYXRjaEFzcGVjdHMsXG4gICAgICAgICAgICB0aGlzLnVwZGF0ZUFzcGVjdHNcbiAgICAgICAgKTtcbiAgICAgICAgaWYgKCF0aGlzLnN0YXRlLmluaXRpYWwpIHtcbiAgICAgICAgICAgIHRoaXMudXBkYXRlQXNwZWN0cyh0aGlzLnN0YXRlLmFzcGVjdHMpLnRoZW4oKCkgPT5cbiAgICAgICAgICAgICAgICB0aGlzLnNldFN0YXRlKHtyZWFkeTogdHJ1ZSwgaW5pdGlhbDogdHJ1ZX0pXG4gICAgICAgICAgICApO1xuICAgICAgICB9XG4gICAgfVxuXG4gICAgY29tcG9uZW50V2lsbFVubW91bnQoKSB7XG4gICAgICAgIHRoaXMucHJvcHMuZGlzY29ubmVjdCh0aGlzLnByb3BzLmlkZW50aXR5KTtcbiAgICB9XG5cbiAgICByZW5kZXIoKSB7XG4gICAgICAgIGNvbnN0IHtjb21wb25lbnQsIGNvbXBvbmVudF9uYW1lLCBwYWNrYWdlX25hbWV9ID0gdGhpcy5wcm9wcztcbiAgICAgICAgY29uc3Qge2FzcGVjdHMsIHJlYWR5fSA9IHRoaXMuc3RhdGU7XG4gICAgICAgIGlmICghcmVhZHkpIHtcbiAgICAgICAgICAgIHJldHVybiBudWxsO1xuICAgICAgICB9XG5cbiAgICAgICAgcmV0dXJuIFJlYWN0LmNsb25lRWxlbWVudChjb21wb25lbnQsIHtcbiAgICAgICAgICAgIC4uLmFzcGVjdHMsXG4gICAgICAgICAgICB1cGRhdGVBc3BlY3RzOiB0aGlzLnVwZGF0ZUFzcGVjdHMsXG4gICAgICAgICAgICBpZGVudGl0eTogdGhpcy5wcm9wcy5pZGVudGl0eSxcbiAgICAgICAgICAgIGNsYXNzX25hbWU6IGpvaW4oXG4gICAgICAgICAgICAgICAgJyAnLFxuICAgICAgICAgICAgICAgIGNvbmNhdChcbiAgICAgICAgICAgICAgICAgICAgW1xuICAgICAgICAgICAgICAgICAgICAgICAgYCR7cGFja2FnZV9uYW1lXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgLnJlcGxhY2UoJ18nLCAnLScpXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgLnRvTG93ZXJDYXNlKCl9LSR7Y2FtZWxUb1NwaW5hbChjb21wb25lbnRfbmFtZSl9YCxcbiAgICAgICAgICAgICAgICAgICAgXSxcbiAgICAgICAgICAgICAgICAgICAgYXNwZWN0cy5jbGFzc19uYW1lID8gYXNwZWN0cy5jbGFzc19uYW1lLnNwbGl0KCcgJykgOiBbXVxuICAgICAgICAgICAgICAgIClcbiAgICAgICAgICAgICksXG4gICAgICAgIH0pO1xuICAgIH1cbn1cbiIsImltcG9ydCB7bWFwLCBvbWl0LCB0eXBlfSBmcm9tICdyYW1kYSc7XG5pbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IFdyYXBwZXIgZnJvbSAnLi9jb21wb25lbnRzL1dyYXBwZXInO1xuaW1wb3J0IHtBbnlEaWN0fSBmcm9tICdjb21tb25zL2pzL3R5cGVzJztcbmltcG9ydCB7XG4gICAgQ29ubmVjdEZ1bmMsXG4gICAgRGlzY29ubmVjdEZ1bmMsXG4gICAgV3JhcHBlclByb3BzLFxuICAgIFdyYXBwZXJVcGRhdGVBc3BlY3RGdW5jLFxufSBmcm9tICcuL3R5cGVzJztcblxuZXhwb3J0IGZ1bmN0aW9uIGlzQ29tcG9uZW50KGM6IGFueSk6IGJvb2xlYW4ge1xuICAgIHJldHVybiAoXG4gICAgICAgIHR5cGUoYykgPT09ICdPYmplY3QnICYmXG4gICAgICAgIGMuaGFzT3duUHJvcGVydHkoJ3BhY2thZ2UnKSAmJlxuICAgICAgICBjLmhhc093blByb3BlcnR5KCdhc3BlY3RzJykgJiZcbiAgICAgICAgYy5oYXNPd25Qcm9wZXJ0eSgnbmFtZScpICYmXG4gICAgICAgIGMuaGFzT3duUHJvcGVydHkoJ2lkZW50aXR5JylcbiAgICApO1xufVxuXG5leHBvcnQgZnVuY3Rpb24gaHlkcmF0ZVByb3BzKFxuICAgIHByb3BzOiBBbnlEaWN0LFxuICAgIHVwZGF0ZUFzcGVjdHM6IFdyYXBwZXJVcGRhdGVBc3BlY3RGdW5jLFxuICAgIGNvbm5lY3Q6IENvbm5lY3RGdW5jLFxuICAgIGRpc2Nvbm5lY3Q6IERpc2Nvbm5lY3RGdW5jLFxuICAgIG9uQ29udGV4dD86IEZ1bmN0aW9uXG4pIHtcbiAgICBjb25zdCByZXBsYWNlID0ge307XG4gICAgT2JqZWN0LmVudHJpZXMocHJvcHMpLmZvckVhY2goKFtrLCB2XSkgPT4ge1xuICAgICAgICBpZiAodHlwZSh2KSA9PT0gJ0FycmF5Jykge1xuICAgICAgICAgICAgcmVwbGFjZVtrXSA9IHYubWFwKChjKSA9PiB7XG4gICAgICAgICAgICAgICAgaWYgKCFpc0NvbXBvbmVudChjKSkge1xuICAgICAgICAgICAgICAgICAgICAvLyBNaXhpbmcgY29tcG9uZW50cyBhbmQgcHJpbWl0aXZlc1xuICAgICAgICAgICAgICAgICAgICBpZiAodHlwZShjKSA9PT0gJ09iamVjdCcpIHtcbiAgICAgICAgICAgICAgICAgICAgICAgIC8vIE5vdCBhIGNvbXBvbmVudCBidXQgbWF5YmUgaXQgY29udGFpbnMgc29tZSA/XG4gICAgICAgICAgICAgICAgICAgICAgICByZXR1cm4gaHlkcmF0ZVByb3BzKFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGMsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgdXBkYXRlQXNwZWN0cyxcbiAgICAgICAgICAgICAgICAgICAgICAgICAgICBjb25uZWN0LFxuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGRpc2Nvbm5lY3QsXG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgb25Db250ZXh0XG4gICAgICAgICAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgICAgIHJldHVybiBjO1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICBjb25zdCBuZXdQcm9wczoge1trZXk6IHN0cmluZ106IGFueX0gPSBoeWRyYXRlUHJvcHMoXG4gICAgICAgICAgICAgICAgICAgIGMuYXNwZWN0cyxcbiAgICAgICAgICAgICAgICAgICAgdXBkYXRlQXNwZWN0cyxcbiAgICAgICAgICAgICAgICAgICAgY29ubmVjdCxcbiAgICAgICAgICAgICAgICAgICAgZGlzY29ubmVjdCxcbiAgICAgICAgICAgICAgICAgICAgb25Db250ZXh0XG4gICAgICAgICAgICAgICAgKTtcbiAgICAgICAgICAgICAgICBpZiAoIW5ld1Byb3BzLmtleSkge1xuICAgICAgICAgICAgICAgICAgICBuZXdQcm9wcy5rZXkgPSBjLmlkZW50aXR5O1xuICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICByZXR1cm4gaHlkcmF0ZUNvbXBvbmVudChcbiAgICAgICAgICAgICAgICAgICAgYy5uYW1lLFxuICAgICAgICAgICAgICAgICAgICBjLnBhY2thZ2UsXG4gICAgICAgICAgICAgICAgICAgIGMuaWRlbnRpdHksXG4gICAgICAgICAgICAgICAgICAgIG5ld1Byb3BzLFxuICAgICAgICAgICAgICAgICAgICB1cGRhdGVBc3BlY3RzLFxuICAgICAgICAgICAgICAgICAgICBjb25uZWN0LFxuICAgICAgICAgICAgICAgICAgICBkaXNjb25uZWN0LFxuICAgICAgICAgICAgICAgICAgICBvbkNvbnRleHRcbiAgICAgICAgICAgICAgICApO1xuICAgICAgICAgICAgfSk7XG4gICAgICAgIH0gZWxzZSBpZiAoaXNDb21wb25lbnQodikpIHtcbiAgICAgICAgICAgIGNvbnN0IG5ld1Byb3BzID0gaHlkcmF0ZVByb3BzKFxuICAgICAgICAgICAgICAgIHYuYXNwZWN0cyxcbiAgICAgICAgICAgICAgICB1cGRhdGVBc3BlY3RzLFxuICAgICAgICAgICAgICAgIGNvbm5lY3QsXG4gICAgICAgICAgICAgICAgZGlzY29ubmVjdCxcbiAgICAgICAgICAgICAgICBvbkNvbnRleHRcbiAgICAgICAgICAgICk7XG4gICAgICAgICAgICByZXBsYWNlW2tdID0gaHlkcmF0ZUNvbXBvbmVudChcbiAgICAgICAgICAgICAgICB2Lm5hbWUsXG4gICAgICAgICAgICAgICAgdi5wYWNrYWdlLFxuICAgICAgICAgICAgICAgIHYuaWRlbnRpdHksXG4gICAgICAgICAgICAgICAgbmV3UHJvcHMsXG4gICAgICAgICAgICAgICAgdXBkYXRlQXNwZWN0cyxcbiAgICAgICAgICAgICAgICBjb25uZWN0LFxuICAgICAgICAgICAgICAgIGRpc2Nvbm5lY3QsXG4gICAgICAgICAgICAgICAgb25Db250ZXh0XG4gICAgICAgICAgICApO1xuICAgICAgICB9IGVsc2UgaWYgKHR5cGUodikgPT09ICdPYmplY3QnKSB7XG4gICAgICAgICAgICByZXBsYWNlW2tdID0gaHlkcmF0ZVByb3BzKFxuICAgICAgICAgICAgICAgIHYsXG4gICAgICAgICAgICAgICAgdXBkYXRlQXNwZWN0cyxcbiAgICAgICAgICAgICAgICBjb25uZWN0LFxuICAgICAgICAgICAgICAgIGRpc2Nvbm5lY3QsXG4gICAgICAgICAgICAgICAgb25Db250ZXh0XG4gICAgICAgICAgICApO1xuICAgICAgICB9XG4gICAgfSk7XG4gICAgcmV0dXJuIHsuLi5wcm9wcywgLi4ucmVwbGFjZX07XG59XG5cbmV4cG9ydCBmdW5jdGlvbiBoeWRyYXRlQ29tcG9uZW50KFxuICAgIG5hbWU6IHN0cmluZyxcbiAgICBwYWNrYWdlX25hbWU6IHN0cmluZyxcbiAgICBpZGVudGl0eTogc3RyaW5nLFxuICAgIHByb3BzOiBBbnlEaWN0LFxuICAgIHVwZGF0ZUFzcGVjdHM6IFdyYXBwZXJVcGRhdGVBc3BlY3RGdW5jLFxuICAgIGNvbm5lY3Q6IENvbm5lY3RGdW5jLFxuICAgIGRpc2Nvbm5lY3Q6IERpc2Nvbm5lY3RGdW5jLFxuICAgIG9uQ29udGV4dDogRnVuY3Rpb25cbikge1xuICAgIGNvbnN0IHBhY2sgPSB3aW5kb3dbcGFja2FnZV9uYW1lXTtcbiAgICBpZiAoIXBhY2spIHtcbiAgICAgICAgdGhyb3cgbmV3IEVycm9yKGBJbnZhbGlkIHBhY2thZ2UgbmFtZTogJHtwYWNrYWdlX25hbWV9YCk7XG4gICAgfVxuICAgIGNvbnN0IGNvbXBvbmVudCA9IHBhY2tbbmFtZV07XG4gICAgaWYgKCFjb21wb25lbnQpIHtcbiAgICAgICAgdGhyb3cgbmV3IEVycm9yKGBJbnZhbGlkIGNvbXBvbmVudCBuYW1lOiAke3BhY2thZ2VfbmFtZX0uJHtuYW1lfWApO1xuICAgIH1cbiAgICAvLyBAdHMtaWdub3JlXG4gICAgY29uc3QgZWxlbWVudCA9IFJlYWN0LmNyZWF0ZUVsZW1lbnQoY29tcG9uZW50LCBwcm9wcyk7XG5cbiAgICAvKiBlc2xpbnQtZGlzYWJsZSByZWFjdC9wcm9wLXR5cGVzICovXG4gICAgY29uc3Qgd3JhcHBlciA9ICh7Y2hpbGRyZW59OiB7Y2hpbGRyZW4/OiBhbnl9KSA9PiAoXG4gICAgICAgIDxXcmFwcGVyXG4gICAgICAgICAgICBpZGVudGl0eT17aWRlbnRpdHl9XG4gICAgICAgICAgICB1cGRhdGVBc3BlY3RzPXt1cGRhdGVBc3BlY3RzfVxuICAgICAgICAgICAgY29tcG9uZW50PXtlbGVtZW50fVxuICAgICAgICAgICAgY29ubmVjdD17Y29ubmVjdH1cbiAgICAgICAgICAgIHBhY2thZ2VfbmFtZT17cGFja2FnZV9uYW1lfVxuICAgICAgICAgICAgY29tcG9uZW50X25hbWU9e25hbWV9XG4gICAgICAgICAgICBhc3BlY3RzPXt7Y2hpbGRyZW4sIC4uLnByb3BzfX1cbiAgICAgICAgICAgIGRpc2Nvbm5lY3Q9e2Rpc2Nvbm5lY3R9XG4gICAgICAgICAgICBrZXk9e2B3cmFwcGVyLSR7aWRlbnRpdHl9YH1cbiAgICAgICAgLz5cbiAgICApO1xuXG4gICAgaWYgKGNvbXBvbmVudC5pc0NvbnRleHQpIHtcbiAgICAgICAgb25Db250ZXh0KHdyYXBwZXIpO1xuICAgICAgICByZXR1cm4gbnVsbDtcbiAgICB9XG4gICAgcmV0dXJuIHdyYXBwZXIoe30pO1xufVxuXG5leHBvcnQgZnVuY3Rpb24gcHJlcGFyZVByb3AocHJvcDogYW55KSB7XG4gICAgaWYgKFJlYWN0LmlzVmFsaWRFbGVtZW50KHByb3ApKSB7XG4gICAgICAgIC8vIEB0cy1pZ25vcmVcbiAgICAgICAgY29uc3QgcHJvcHM6IFdyYXBwZXJQcm9wcyA9IHByb3AucHJvcHM7XG4gICAgICAgIHJldHVybiB7XG4gICAgICAgICAgICBpZGVudGl0eTogcHJvcHMuaWRlbnRpdHksXG4gICAgICAgICAgICAvLyBAdHMtaWdub3JlXG4gICAgICAgICAgICBhc3BlY3RzOiBtYXAoXG4gICAgICAgICAgICAgICAgcHJlcGFyZVByb3AsXG4gICAgICAgICAgICAgICAgb21pdChcbiAgICAgICAgICAgICAgICAgICAgW1xuICAgICAgICAgICAgICAgICAgICAgICAgJ2lkZW50aXR5JyxcbiAgICAgICAgICAgICAgICAgICAgICAgICd1cGRhdGVBc3BlY3RzJyxcbiAgICAgICAgICAgICAgICAgICAgICAgICdfbmFtZScsXG4gICAgICAgICAgICAgICAgICAgICAgICAnX3BhY2thZ2UnLFxuICAgICAgICAgICAgICAgICAgICAgICAgJ2FzcGVjdHMnLFxuICAgICAgICAgICAgICAgICAgICAgICAgJ2tleScsXG4gICAgICAgICAgICAgICAgICAgIF0sXG4gICAgICAgICAgICAgICAgICAgIHByb3BzLmFzcGVjdHNcbiAgICAgICAgICAgICAgICApXG4gICAgICAgICAgICApLFxuICAgICAgICAgICAgbmFtZTogcHJvcHMuY29tcG9uZW50X25hbWUsXG4gICAgICAgICAgICBwYWNrYWdlOiBwcm9wcy5wYWNrYWdlX25hbWUsXG4gICAgICAgIH07XG4gICAgfVxuICAgIGlmICh0eXBlKHByb3ApID09PSAnQXJyYXknKSB7XG4gICAgICAgIHJldHVybiBwcm9wLm1hcChwcmVwYXJlUHJvcCk7XG4gICAgfVxuICAgIGlmICh0eXBlKHByb3ApID09PSAnT2JqZWN0Jykge1xuICAgICAgICByZXR1cm4gbWFwKHByZXBhcmVQcm9wLCBwcm9wKTtcbiAgICB9XG4gICAgcmV0dXJuIHByb3A7XG59XG4iLCJpbXBvcnQgUmVhY3QgZnJvbSAncmVhY3QnO1xuaW1wb3J0IFJlYWN0RE9NIGZyb20gJ3JlYWN0LWRvbSc7XG5pbXBvcnQgUmVuZGVyZXIgZnJvbSAnLi9jb21wb25lbnRzL1JlbmRlcmVyJztcbmltcG9ydCB7UmVuZGVyT3B0aW9uc30gZnJvbSAnLi90eXBlcyc7XG5cbmZ1bmN0aW9uIHJlbmRlcihcbiAgICB7YmFzZVVybCwgcGluZywgcGluZ19pbnRlcnZhbCwgcmV0cmllc306IFJlbmRlck9wdGlvbnMsXG4gICAgZWxlbWVudDogc3RyaW5nXG4pIHtcbiAgICBSZWFjdERPTS5yZW5kZXIoXG4gICAgICAgIDxSZW5kZXJlclxuICAgICAgICAgICAgYmFzZVVybD17YmFzZVVybH1cbiAgICAgICAgICAgIHBpbmc9e3Bpbmd9XG4gICAgICAgICAgICBwaW5nX2ludGVydmFsPXtwaW5nX2ludGVydmFsfVxuICAgICAgICAgICAgcmV0cmllcz17cmV0cmllc31cbiAgICAgICAgLz4sXG4gICAgICAgIGVsZW1lbnRcbiAgICApO1xufVxuXG4vLyBAdHMtaWdub3JlXG5leHBvcnQge1JlbmRlcmVyLCByZW5kZXJ9O1xuIiwiLyogZXNsaW50LWRpc2FibGUgbm8tbWFnaWMtbnVtYmVycyAqL1xuXG5pbXBvcnQge1hoclJlcXVlc3RPcHRpb25zfSBmcm9tICcuL3R5cGVzJztcblxuY29uc3QganNvblBhdHRlcm4gPSAvanNvbi9pO1xuXG5jb25zdCBkZWZhdWx0WGhyT3B0aW9uczogWGhyUmVxdWVzdE9wdGlvbnMgPSB7XG4gICAgbWV0aG9kOiAnR0VUJyxcbiAgICBoZWFkZXJzOiB7fSxcbiAgICBwYXlsb2FkOiAnJyxcbiAgICBqc29uOiB0cnVlLFxufTtcblxuZXhwb3J0IGNvbnN0IEpTT05IRUFERVJTID0ge1xuICAgICdDb250ZW50LVR5cGUnOiAnYXBwbGljYXRpb24vanNvbicsXG59O1xuXG5leHBvcnQgZnVuY3Rpb24geGhyUmVxdWVzdChcbiAgICB1cmw6IHN0cmluZyxcbiAgICBvcHRpb25zOiBYaHJSZXF1ZXN0T3B0aW9ucyA9IGRlZmF1bHRYaHJPcHRpb25zXG4pIHtcbiAgICByZXR1cm4gbmV3IFByb21pc2U8YW55PigocmVzb2x2ZSwgcmVqZWN0KSA9PiB7XG4gICAgICAgIGNvbnN0IHttZXRob2QsIGhlYWRlcnMsIHBheWxvYWQsIGpzb259ID0ge1xuICAgICAgICAgICAgLi4uZGVmYXVsdFhock9wdGlvbnMsXG4gICAgICAgICAgICAuLi5vcHRpb25zLFxuICAgICAgICB9O1xuICAgICAgICBjb25zdCB4aHIgPSBuZXcgWE1MSHR0cFJlcXVlc3QoKTtcbiAgICAgICAgeGhyLm9wZW4obWV0aG9kLCB1cmwpO1xuICAgICAgICBjb25zdCBoZWFkID0ganNvbiA/IHsuLi5KU09OSEVBREVSUywgLi4uaGVhZGVyc30gOiBoZWFkZXJzO1xuICAgICAgICBPYmplY3Qua2V5cyhoZWFkKS5mb3JFYWNoKChrKSA9PiB4aHIuc2V0UmVxdWVzdEhlYWRlcihrLCBoZWFkW2tdKSk7XG4gICAgICAgIHhoci5vbnJlYWR5c3RhdGVjaGFuZ2UgPSAoKSA9PiB7XG4gICAgICAgICAgICBpZiAoeGhyLnJlYWR5U3RhdGUgPT09IFhNTEh0dHBSZXF1ZXN0LkRPTkUpIHtcbiAgICAgICAgICAgICAgICBpZiAoeGhyLnN0YXR1cyA9PT0gMjAwKSB7XG4gICAgICAgICAgICAgICAgICAgIGxldCByZXNwb25zZVZhbHVlID0geGhyLnJlc3BvbnNlO1xuICAgICAgICAgICAgICAgICAgICBpZiAoXG4gICAgICAgICAgICAgICAgICAgICAgICBqc29uUGF0dGVybi50ZXN0KHhoci5nZXRSZXNwb25zZUhlYWRlcignQ29udGVudC1UeXBlJykpXG4gICAgICAgICAgICAgICAgICAgICkge1xuICAgICAgICAgICAgICAgICAgICAgICAgcmVzcG9uc2VWYWx1ZSA9IEpTT04ucGFyc2UoeGhyLnJlc3BvbnNlVGV4dCk7XG4gICAgICAgICAgICAgICAgICAgIH1cbiAgICAgICAgICAgICAgICAgICAgcmVzb2x2ZShyZXNwb25zZVZhbHVlKTtcbiAgICAgICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgICAgICByZWplY3Qoe1xuICAgICAgICAgICAgICAgICAgICAgICAgZXJyb3I6ICdSZXF1ZXN0RXJyb3InLFxuICAgICAgICAgICAgICAgICAgICAgICAgbWVzc2FnZTogYFhIUiAke3VybH0gRkFJTEVEIC0gU1RBVFVTOiAke3hoci5zdGF0dXN9IE1FU1NBR0U6ICR7eGhyLnN0YXR1c1RleHR9YCxcbiAgICAgICAgICAgICAgICAgICAgICAgIHN0YXR1czogeGhyLnN0YXR1cyxcbiAgICAgICAgICAgICAgICAgICAgICAgIHhocixcbiAgICAgICAgICAgICAgICAgICAgfSk7XG4gICAgICAgICAgICAgICAgfVxuICAgICAgICAgICAgfVxuICAgICAgICB9O1xuICAgICAgICB4aHIub25lcnJvciA9IChlcnIpID0+IHJlamVjdChlcnIpO1xuICAgICAgICAvLyBAdHMtaWdub3JlXG4gICAgICAgIHhoci5zZW5kKGpzb24gPyBKU09OLnN0cmluZ2lmeShwYXlsb2FkKSA6IHBheWxvYWQpO1xuICAgIH0pO1xufVxuXG5leHBvcnQgZnVuY3Rpb24gYXBpUmVxdWVzdChiYXNlVXJsOiBzdHJpbmcpIHtcbiAgICByZXR1cm4gZnVuY3Rpb24gKCkge1xuICAgICAgICBjb25zdCB1cmwgPSBiYXNlVXJsICsgYXJndW1lbnRzWzBdO1xuICAgICAgICBjb25zdCBvcHRpb25zID0gYXJndW1lbnRzWzFdIHx8IHt9O1xuICAgICAgICBvcHRpb25zLmhlYWRlcnMgPSB7Li4ub3B0aW9ucy5oZWFkZXJzfTtcbiAgICAgICAgcmV0dXJuIG5ldyBQcm9taXNlKChyZXNvbHZlKSA9PiB7XG4gICAgICAgICAgICB4aHJSZXF1ZXN0KHVybCwgb3B0aW9ucykudGhlbihyZXNvbHZlKTtcbiAgICAgICAgfSk7XG4gICAgfTtcbn1cbiIsImltcG9ydCB7bG9hZENzcywgbG9hZFNjcmlwdH0gZnJvbSAnY29tbW9ucyc7XG5pbXBvcnQge1BhY2thZ2UsIFJlcXVpcmVtZW50fSBmcm9tICcuL3R5cGVzJztcbmltcG9ydCB7ZHJvcH0gZnJvbSAncmFtZGEnO1xuXG5leHBvcnQgZnVuY3Rpb24gbG9hZFJlcXVpcmVtZW50KHJlcXVpcmVtZW50OiBSZXF1aXJlbWVudCkge1xuICAgIHJldHVybiBuZXcgUHJvbWlzZTx2b2lkPigocmVzb2x2ZSwgcmVqZWN0KSA9PiB7XG4gICAgICAgIGNvbnN0IHt1cmwsIGtpbmR9ID0gcmVxdWlyZW1lbnQ7XG4gICAgICAgIGxldCBtZXRob2Q7XG4gICAgICAgIGlmIChraW5kID09PSAnanMnKSB7XG4gICAgICAgICAgICBtZXRob2QgPSBsb2FkU2NyaXB0O1xuICAgICAgICB9IGVsc2UgaWYgKGtpbmQgPT09ICdjc3MnKSB7XG4gICAgICAgICAgICBtZXRob2QgPSBsb2FkQ3NzO1xuICAgICAgICB9IGVsc2UgaWYgKGtpbmQgPT09ICdtYXAnKSB7XG4gICAgICAgICAgICByZXR1cm4gcmVzb2x2ZSgpO1xuICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgcmV0dXJuIHJlamVjdCh7ZXJyb3I6IGBJbnZhbGlkIHJlcXVpcmVtZW50IGtpbmQ6ICR7a2luZH1gfSk7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIG1ldGhvZCh1cmwpLnRoZW4ocmVzb2x2ZSkuY2F0Y2gocmVqZWN0KTtcbiAgICB9KTtcbn1cblxuZnVuY3Rpb24gbG9hZE9uZUJ5T25lKHJlcXVpcmVtZW50czogUmVxdWlyZW1lbnRbXSkge1xuICAgIHJldHVybiBuZXcgUHJvbWlzZSgocmVzb2x2ZSkgPT4ge1xuICAgICAgICBjb25zdCBoYW5kbGUgPSAocmVxcykgPT4ge1xuICAgICAgICAgICAgaWYgKHJlcXMubGVuZ3RoKSB7XG4gICAgICAgICAgICAgICAgY29uc3QgcmVxdWlyZW1lbnQgPSByZXFzWzBdO1xuICAgICAgICAgICAgICAgIGxvYWRSZXF1aXJlbWVudChyZXF1aXJlbWVudCkudGhlbigoKSA9PiBoYW5kbGUoZHJvcCgxLCByZXFzKSkpO1xuICAgICAgICAgICAgfSBlbHNlIHtcbiAgICAgICAgICAgICAgICByZXNvbHZlKG51bGwpO1xuICAgICAgICAgICAgfVxuICAgICAgICB9O1xuICAgICAgICBoYW5kbGUocmVxdWlyZW1lbnRzKTtcbiAgICB9KTtcbn1cblxuZXhwb3J0IGZ1bmN0aW9uIGxvYWRSZXF1aXJlbWVudHMoXG4gICAgcmVxdWlyZW1lbnRzOiBSZXF1aXJlbWVudFtdLFxuICAgIHBhY2thZ2VzOiB7W2s6IHN0cmluZ106IFBhY2thZ2V9XG4pIHtcbiAgICByZXR1cm4gbmV3IFByb21pc2U8dm9pZD4oKHJlc29sdmUsIHJlamVjdCkgPT4ge1xuICAgICAgICBsZXQgbG9hZGluZ3MgPSBbXTtcbiAgICAgICAgT2JqZWN0LmtleXMocGFja2FnZXMpLmZvckVhY2goKHBhY2tfbmFtZSkgPT4ge1xuICAgICAgICAgICAgY29uc3QgcGFjayA9IHBhY2thZ2VzW3BhY2tfbmFtZV07XG4gICAgICAgICAgICBsb2FkaW5ncyA9IGxvYWRpbmdzLmNvbmNhdChcbiAgICAgICAgICAgICAgICBsb2FkT25lQnlPbmUocGFjay5yZXF1aXJlbWVudHMuZmlsdGVyKChyKSA9PiByLmtpbmQgPT09ICdqcycpKVxuICAgICAgICAgICAgKTtcbiAgICAgICAgICAgIGxvYWRpbmdzID0gbG9hZGluZ3MuY29uY2F0KFxuICAgICAgICAgICAgICAgIHBhY2sucmVxdWlyZW1lbnRzXG4gICAgICAgICAgICAgICAgICAgIC5maWx0ZXIoKHIpID0+IHIua2luZCA9PT0gJ2NzcycpXG4gICAgICAgICAgICAgICAgICAgIC5tYXAobG9hZFJlcXVpcmVtZW50KVxuICAgICAgICAgICAgKTtcbiAgICAgICAgfSk7XG4gICAgICAgIC8vIFRoZW4gbG9hZCByZXF1aXJlbWVudHMgc28gdGhleSBjYW4gdXNlIHBhY2thZ2VzXG4gICAgICAgIC8vIGFuZCBvdmVycmlkZSBjc3MuXG4gICAgICAgIFByb21pc2UuYWxsKGxvYWRpbmdzKVxuICAgICAgICAgICAgLnRoZW4oKCkgPT4ge1xuICAgICAgICAgICAgICAgIGxldCBpID0gMDtcbiAgICAgICAgICAgICAgICAvLyBMb2FkIGluIG9yZGVyLlxuICAgICAgICAgICAgICAgIGNvbnN0IGhhbmRsZXIgPSAoKSA9PiB7XG4gICAgICAgICAgICAgICAgICAgIGlmIChpIDwgcmVxdWlyZW1lbnRzLmxlbmd0aCkge1xuICAgICAgICAgICAgICAgICAgICAgICAgbG9hZFJlcXVpcmVtZW50KHJlcXVpcmVtZW50c1tpXSkudGhlbigoKSA9PiB7XG4gICAgICAgICAgICAgICAgICAgICAgICAgICAgaSsrO1xuICAgICAgICAgICAgICAgICAgICAgICAgICAgIGhhbmRsZXIoKTtcbiAgICAgICAgICAgICAgICAgICAgICAgIH0pO1xuICAgICAgICAgICAgICAgICAgICB9IGVsc2Uge1xuICAgICAgICAgICAgICAgICAgICAgICAgcmVzb2x2ZSgpO1xuICAgICAgICAgICAgICAgICAgICB9XG4gICAgICAgICAgICAgICAgfTtcbiAgICAgICAgICAgICAgICBoYW5kbGVyKCk7XG4gICAgICAgICAgICB9KVxuICAgICAgICAgICAgLmNhdGNoKHJlamVjdCk7XG4gICAgfSk7XG59XG4iLCIvKiBlc2xpbnQtZGlzYWJsZSBuby11c2UtYmVmb3JlLWRlZmluZSAqL1xuaW1wb3J0IHtcbiAgICBjb25jYXQsXG4gICAgZHJvcCxcbiAgICBlcXVhbHMsXG4gICAgZmluZCxcbiAgICBmcm9tUGFpcnMsXG4gICAgaW5jbHVkZXMsXG4gICAgaXMsXG4gICAgam9pbixcbiAgICBtZXJnZURlZXBMZWZ0LFxuICAgIG1lcmdlRGVlcFJpZ2h0LFxuICAgIG1lcmdlTGVmdCxcbiAgICBtZXJnZVJpZ2h0LFxuICAgIHBpY2ssXG4gICAgcGx1Y2ssXG4gICAgcmVkdWNlLFxuICAgIHJlcGxhY2UsXG4gICAgcmV2ZXJzZSxcbiAgICBzbGljZSxcbiAgICBzb3J0LFxuICAgIHNwbGl0LFxuICAgIHRha2UsXG4gICAgdG9QYWlycyxcbiAgICB0cmltLFxuICAgIHVuaXEsXG4gICAgemlwLFxufSBmcm9tICdyYW1kYSc7XG5pbXBvcnQge1RyYW5zZm9ybSwgVHJhbnNmb3JtRnVuYywgVHJhbnNmb3JtR2V0QXNwZWN0RnVuY30gZnJvbSAnLi90eXBlcyc7XG5pbXBvcnQge2NvZXJjZUFzcGVjdCwgaXNBc3BlY3R9IGZyb20gJy4vYXNwZWN0cyc7XG5cbmNvbnN0IHRyYW5zZm9ybXM6IHtba2V5OiBzdHJpbmddOiBUcmFuc2Zvcm1GdW5jfSA9IHtcbiAgICAvKiBTdHJpbmcgdHJhbnNmb3JtcyAqL1xuICAgIFRvVXBwZXI6ICh2YWx1ZSkgPT4ge1xuICAgICAgICByZXR1cm4gdmFsdWUudG9VcHBlckNhc2UoKTtcbiAgICB9LFxuICAgIFRvTG93ZXI6ICh2YWx1ZSkgPT4ge1xuICAgICAgICByZXR1cm4gdmFsdWUudG9Mb3dlckNhc2UoKTtcbiAgICB9LFxuICAgIEZvcm1hdDogKHZhbHVlLCBhcmdzKSA9PiB7XG4gICAgICAgIGNvbnN0IHt0ZW1wbGF0ZX0gPSBhcmdzO1xuICAgICAgICBpZiAoaXMoU3RyaW5nLCB2YWx1ZSkgfHwgaXMoTnVtYmVyLCB2YWx1ZSkgfHwgaXMoQm9vbGVhbiwgdmFsdWUpKSB7XG4gICAgICAgICAgICByZXR1cm4gcmVwbGFjZSgnJHt2YWx1ZX0nLCB2YWx1ZSwgdGVtcGxhdGUpO1xuICAgICAgICB9IGVsc2UgaWYgKGlzKE9iamVjdCwgdmFsdWUpKSB7XG4gICAgICAgICAgICByZXR1cm4gcmVkdWNlKFxuICAgICAgICAgICAgICAgIChhY2MsIFtrLCB2XSkgPT4gcmVwbGFjZShgJFxceyR7a319YCwgdiwgYWNjKSxcbiAgICAgICAgICAgICAgICB0ZW1wbGF0ZSxcbiAgICAgICAgICAgICAgICB0b1BhaXJzKHZhbHVlKVxuICAgICAgICAgICAgKTtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gdmFsdWU7XG4gICAgfSxcbiAgICBTcGxpdDogKHZhbHVlLCBhcmdzKSA9PiB7XG4gICAgICAgIGNvbnN0IHtzZXBhcmF0b3J9ID0gYXJncztcbiAgICAgICAgcmV0dXJuIHNwbGl0KHNlcGFyYXRvciwgdmFsdWUpO1xuICAgIH0sXG4gICAgVHJpbTogKHZhbHVlKSA9PiB7XG4gICAgICAgIHJldHVybiB0cmltKHZhbHVlKTtcbiAgICB9LFxuICAgIC8qIE51bWJlciBUcmFuc2Zvcm0gKi9cbiAgICBBZGQ6ICh2YWx1ZSwgYXJncywgZ2V0QXNwZWN0KSA9PiB7XG4gICAgICAgIGlmIChpcyhOdW1iZXIsIGFyZ3MudmFsdWUpKSB7XG4gICAgICAgICAgICByZXR1cm4gdmFsdWUgKyBhcmdzLnZhbHVlO1xuICAgICAgICB9XG4gICAgICAgIHJldHVybiB2YWx1ZSArIGNvZXJjZUFzcGVjdChhcmdzLnZhbHVlLCBnZXRBc3BlY3QpO1xuICAgIH0sXG4gICAgU3ViOiAodmFsdWUsIGFyZ3MsIGdldEFzcGVjdCkgPT4ge1xuICAgICAgICBpZiAoaXMoTnVtYmVyLCBhcmdzLnZhbHVlKSkge1xuICAgICAgICAgICAgcmV0dXJuIHZhbHVlIC0gYXJncy52YWx1ZTtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gdmFsdWUgLSBjb2VyY2VBc3BlY3QoYXJncy52YWx1ZSwgZ2V0QXNwZWN0KTtcbiAgICB9LFxuICAgIERpdmlkZTogKHZhbHVlLCBhcmdzLCBnZXRBc3BlY3QpID0+IHtcbiAgICAgICAgaWYgKGlzKE51bWJlciwgYXJncy52YWx1ZSkpIHtcbiAgICAgICAgICAgIHJldHVybiB2YWx1ZSAvIGFyZ3MudmFsdWU7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIHZhbHVlIC8gY29lcmNlQXNwZWN0KGFyZ3MudmFsdWUsIGdldEFzcGVjdCk7XG4gICAgfSxcbiAgICBNdWx0aXBseTogKHZhbHVlLCBhcmdzLCBnZXRBc3BlY3QpID0+IHtcbiAgICAgICAgaWYgKGlzKE51bWJlciwgYXJncy52YWx1ZSkpIHtcbiAgICAgICAgICAgIHJldHVybiB2YWx1ZSAqIGFyZ3MudmFsdWU7XG4gICAgICAgIH1cbiAgICAgICAgcmV0dXJuIHZhbHVlICogY29lcmNlQXNwZWN0KGFyZ3MudmFsdWUsIGdldEFzcGVjdCk7XG4gICAgfSxcbiAgICBNb2R1bHVzOiAodmFsdWUsIGFyZ3MsIGdldEFzcGVjdCkgPT4ge1xuICAgICAgICBpZiAoaXMoTnVtYmVyLCBhcmdzLnZhbHVlKSkge1xuICAgICAgICAgICAgcmV0dXJuIHZhbHVlICUgYXJncy52YWx1ZTtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gdmFsdWUgJSBjb2VyY2VBc3BlY3QoYXJncy52YWx1ZSwgZ2V0QXNwZWN0KTtcbiAgICB9LFxuICAgIFRvUHJlY2lzaW9uOiAodmFsdWUsIGFyZ3MpID0+IHtcbiAgICAgICAgcmV0dXJuIHZhbHVlLnRvUHJlY2lzaW9uKGFyZ3MucHJlY2lzaW9uKTtcbiAgICB9LFxuICAgIC8qIEFycmF5IHRyYW5zZm9ybXMgICovXG4gICAgQ29uY2F0OiAodmFsdWUsIGFyZ3MsIGdldEFzcGVjdCkgPT4ge1xuICAgICAgICBjb25zdCB7b3RoZXJ9ID0gYXJncztcbiAgICAgICAgcmV0dXJuIGNvbmNhdCh2YWx1ZSwgY29lcmNlQXNwZWN0KG90aGVyLCBnZXRBc3BlY3QpKTtcbiAgICB9LFxuICAgIFNsaWNlOiAodmFsdWUsIGFyZ3MpID0+IHtcbiAgICAgICAgcmV0dXJuIHNsaWNlKGFyZ3Muc3RhcnQsIGFyZ3Muc3RvcCwgdmFsdWUpO1xuICAgIH0sXG4gICAgTWFwOiAodmFsdWUsIGFyZ3MsIGdldEFzcGVjdCkgPT4ge1xuICAgICAgICBjb25zdCB7dHJhbnNmb3JtfSA9IGFyZ3M7XG4gICAgICAgIHJldHVybiB2YWx1ZS5tYXAoKGUpID0+XG4gICAgICAgICAgICBleGVjdXRlVHJhbnNmb3JtKFxuICAgICAgICAgICAgICAgIHRyYW5zZm9ybS50cmFuc2Zvcm0sXG4gICAgICAgICAgICAgICAgZSxcbiAgICAgICAgICAgICAgICB0cmFuc2Zvcm0uYXJncyxcbiAgICAgICAgICAgICAgICB0cmFuc2Zvcm0ubmV4dCxcbiAgICAgICAgICAgICAgICBnZXRBc3BlY3RcbiAgICAgICAgICAgIClcbiAgICAgICAgKTtcbiAgICB9LFxuICAgIEZpbHRlcjogKHZhbHVlLCBhcmdzLCBnZXRBc3BlY3QpID0+IHtcbiAgICAgICAgY29uc3Qge2NvbXBhcmlzb259ID0gYXJncztcbiAgICAgICAgcmV0dXJuIHZhbHVlLmZpbHRlcigoZSkgPT5cbiAgICAgICAgICAgIGV4ZWN1dGVUcmFuc2Zvcm0oXG4gICAgICAgICAgICAgICAgY29tcGFyaXNvbi50cmFuc2Zvcm0sXG4gICAgICAgICAgICAgICAgZSxcbiAgICAgICAgICAgICAgICBjb21wYXJpc29uLmFyZ3MsXG4gICAgICAgICAgICAgICAgY29tcGFyaXNvbi5uZXh0LFxuICAgICAgICAgICAgICAgIGdldEFzcGVjdFxuICAgICAgICAgICAgKVxuICAgICAgICApO1xuICAgIH0sXG4gICAgUmVkdWNlOiAodmFsdWUsIGFyZ3MsIGdldEFzcGVjdCkgPT4ge1xuICAgICAgICBjb25zdCB7dHJhbnNmb3JtLCBhY2N1bXVsYXRvcn0gPSBhcmdzO1xuICAgICAgICBjb25zdCBhY2MgPSBjb2VyY2VBc3BlY3QoYWNjdW11bGF0b3IsIGdldEFzcGVjdCk7XG4gICAgICAgIHJldHVybiB2YWx1ZS5yZWR1Y2UoXG4gICAgICAgICAgICAocHJldmlvdXMsIG5leHQpID0+XG4gICAgICAgICAgICAgICAgZXhlY3V0ZVRyYW5zZm9ybShcbiAgICAgICAgICAgICAgICAgICAgdHJhbnNmb3JtLnRyYW5zZm9ybSxcbiAgICAgICAgICAgICAgICAgICAgW3ByZXZpb3VzLCBuZXh0XSxcbiAgICAgICAgICAgICAgICAgICAgdHJhbnNmb3JtLmFyZ3MsXG4gICAgICAgICAgICAgICAgICAgIHRyYW5zZm9ybS5uZXh0LFxuICAgICAgICAgICAgICAgICAgICBnZXRBc3BlY3RcbiAgICAgICAgICAgICAgICApLFxuICAgICAgICAgICAgYWNjXG4gICAgICAgICk7XG4gICAgfSxcbiAgICBQbHVjazogKHZhbHVlLCBhcmdzKSA9PiB7XG4gICAgICAgIGNvbnN0IHtmaWVsZH0gPSBhcmdzO1xuICAgICAgICByZXR1cm4gcGx1Y2soZmllbGQsIHZhbHVlKTtcbiAgICB9LFxuICAgIEFwcGVuZDogKHZhbHVlLCBhcmdzLCBnZXRBc3BlY3QpID0+IHtcbiAgICAgICAgcmV0dXJuIGNvbmNhdCh2YWx1ZSwgW2NvZXJjZUFzcGVjdChhcmdzLnZhbHVlLCBnZXRBc3BlY3QpXSk7XG4gICAgfSxcbiAgICBQcmVwZW5kOiAodmFsdWUsIGFyZ3MsIGdldEFzcGVjdCkgPT4ge1xuICAgICAgICByZXR1cm4gY29uY2F0KFtjb2VyY2VBc3BlY3QoYXJncy52YWx1ZSwgZ2V0QXNwZWN0KV0sIHZhbHVlKTtcbiAgICB9LFxuICAgIEluc2VydDogKHZhbHVlLCBhcmdzLCBnZXRBc3BlY3QpID0+IHtcbiAgICAgICAgY29uc3Qge3RhcmdldCwgZnJvbnR9ID0gYXJncztcbiAgICAgICAgY29uc3QgdCA9IGNvZXJjZUFzcGVjdCh0YXJnZXQsIGdldEFzcGVjdCk7XG4gICAgICAgIHJldHVybiBmcm9udCA/IGNvbmNhdChbdmFsdWVdLCB0KSA6IGNvbmNhdCh0LCBbdmFsdWVdKTtcbiAgICB9LFxuICAgIFRha2U6ICh2YWx1ZSwgYXJncywgZ2V0QXNwZWN0KSA9PiB7XG4gICAgICAgIGNvbnN0IHtufSA9IGFyZ3M7XG4gICAgICAgIHJldHVybiB0YWtlKGNvZXJjZUFzcGVjdChuLCBnZXRBc3BlY3QpLCB2YWx1ZSk7XG4gICAgfSxcbiAgICBMZW5ndGg6ICh2YWx1ZSkgPT4ge1xuICAgICAgICByZXR1cm4gdmFsdWUubGVuZ3RoO1xuICAgIH0sXG4gICAgUmFuZ2U6ICh2YWx1ZSwgYXJncywgZ2V0QXNwZWN0KSA9PiB7XG4gICAgICAgIGNvbnN0IHtzdGFydCwgZW5kLCBzdGVwfSA9IGFyZ3M7XG4gICAgICAgIGNvbnN0IHMgPSBjb2VyY2VBc3BlY3Qoc3RhcnQsIGdldEFzcGVjdCk7XG4gICAgICAgIGNvbnN0IGUgPSBjb2VyY2VBc3BlY3QoZW5kLCBnZXRBc3BlY3QpO1xuICAgICAgICBsZXQgaSA9IHM7XG4gICAgICAgIGNvbnN0IGFyciA9IFtdO1xuICAgICAgICB3aGlsZSAoaSA8IGUpIHtcbiAgICAgICAgICAgIGFyci5wdXNoKGkpO1xuICAgICAgICAgICAgaSArPSBzdGVwO1xuICAgICAgICB9XG4gICAgICAgIHJldHVybiBhcnI7XG4gICAgfSxcbiAgICBJbmNsdWRlczogKHZhbHVlLCBhcmdzLCBnZXRBc3BlY3QpID0+IHtcbiAgICAgICAgcmV0dXJuIGluY2x1ZGVzKGNvZXJjZUFzcGVjdChhcmdzLnZhbHVlLCBnZXRBc3BlY3QpLCB2YWx1ZSk7XG4gICAgfSxcbiAgICBGaW5kOiAodmFsdWUsIGFyZ3MsIGdldEFzcGVjdCkgPT4ge1xuICAgICAgICBjb25zdCB7Y29tcGFyaXNvbn0gPSBhcmdzO1xuICAgICAgICByZXR1cm4gZmluZCgoYSkgPT5cbiAgICAgICAgICAgIGV4ZWN1dGVUcmFuc2Zvcm0oXG4gICAgICAgICAgICAgICAgY29tcGFyaXNvbi50cmFuc2Zvcm0sXG4gICAgICAgICAgICAgICAgYSxcbiAgICAgICAgICAgICAgICBjb21wYXJpc29uLmFyZ3MsXG4gICAgICAgICAgICAgICAgY29tcGFyaXNvbi5uZXh0LFxuICAgICAgICAgICAgICAgIGdldEFzcGVjdFxuICAgICAgICAgICAgKVxuICAgICAgICApKHZhbHVlKTtcbiAgICB9LFxuICAgIEpvaW46ICh2YWx1ZSwgYXJncywgZ2V0QXNwZWN0KSA9PiB7XG4gICAgICAgIHJldHVybiBqb2luKGNvZXJjZUFzcGVjdChhcmdzLnNlcGFyYXRvciwgZ2V0QXNwZWN0KSwgdmFsdWUpO1xuICAgIH0sXG4gICAgU29ydDogKHZhbHVlLCBhcmdzLCBnZXRBc3BlY3QpID0+IHtcbiAgICAgICAgY29uc3Qge3RyYW5zZm9ybX0gPSBhcmdzO1xuICAgICAgICByZXR1cm4gc29ydChcbiAgICAgICAgICAgIChhLCBiKSA9PlxuICAgICAgICAgICAgICAgIGV4ZWN1dGVUcmFuc2Zvcm0oXG4gICAgICAgICAgICAgICAgICAgIHRyYW5zZm9ybS50cmFuc2Zvcm0sXG4gICAgICAgICAgICAgICAgICAgIFthLCBiXSxcbiAgICAgICAgICAgICAgICAgICAgdHJhbnNmb3JtLmFyZ3MsXG4gICAgICAgICAgICAgICAgICAgIHRyYW5zZm9ybS5uZXh0LFxuICAgICAgICAgICAgICAgICAgICBnZXRBc3BlY3RcbiAgICAgICAgICAgICAgICApLFxuICAgICAgICAgICAgdmFsdWVcbiAgICAgICAgKTtcbiAgICB9LFxuICAgIFJldmVyc2U6ICh2YWx1ZSkgPT4ge1xuICAgICAgICByZXR1cm4gcmV2ZXJzZSh2YWx1ZSk7XG4gICAgfSxcbiAgICBVbmlxdWU6ICh2YWx1ZSkgPT4ge1xuICAgICAgICByZXR1cm4gdW5pcSh2YWx1ZSk7XG4gICAgfSxcbiAgICBaaXA6ICh2YWx1ZSwgYXJncywgZ2V0QXNwZWN0KSA9PiB7XG4gICAgICAgIHJldHVybiB6aXAodmFsdWUsIGNvZXJjZUFzcGVjdChhcmdzLnZhbHVlLCBnZXRBc3BlY3QpKTtcbiAgICB9LFxuICAgIC8qIE9iamVjdCB0cmFuc2Zvcm1zICovXG4gICAgUGljazogKHZhbHVlLCBhcmdzKSA9PiB7XG4gICAgICAgIHJldHVybiBwaWNrKGFyZ3MuZmllbGRzLCB2YWx1ZSk7XG4gICAgfSxcbiAgICBHZXQ6ICh2YWx1ZSwgYXJncykgPT4ge1xuICAgICAgICByZXR1cm4gdmFsdWVbYXJncy5maWVsZF07XG4gICAgfSxcbiAgICBTZXQ6ICh2LCBhcmdzLCBnZXRBc3BlY3QpID0+IHtcbiAgICAgICAgY29uc3Qge2tleSwgdmFsdWV9ID0gYXJncztcbiAgICAgICAgdltrZXldID0gY29lcmNlQXNwZWN0KHZhbHVlLCBnZXRBc3BlY3QpO1xuICAgICAgICByZXR1cm4gdjtcbiAgICB9LFxuICAgIFB1dDogKHZhbHVlLCBhcmdzLCBnZXRBc3BlY3QpID0+IHtcbiAgICAgICAgY29uc3Qge2tleSwgdGFyZ2V0fSA9IGFyZ3M7XG4gICAgICAgIGNvbnN0IG9iaiA9IGNvZXJjZUFzcGVjdCh0YXJnZXQsIGdldEFzcGVjdCk7XG4gICAgICAgIG9ialtrZXldID0gdmFsdWU7XG4gICAgICAgIHJldHVybiBvYmo7XG4gICAgfSxcbiAgICBNZXJnZTogKHZhbHVlLCBhcmdzLCBnZXRBc3BlY3QpID0+IHtcbiAgICAgICAgY29uc3Qge2RlZXAsIGRpcmVjdGlvbiwgb3RoZXJ9ID0gYXJncztcbiAgICAgICAgbGV0IG90aGVyVmFsdWUgPSBvdGhlcjtcbiAgICAgICAgaWYgKGlzQXNwZWN0KG90aGVyKSkge1xuICAgICAgICAgICAgb3RoZXJWYWx1ZSA9IGdldEFzcGVjdChvdGhlci5pZGVudGl0eSwgb3RoZXIuYXNwZWN0KTtcbiAgICAgICAgfVxuICAgICAgICBpZiAoZGlyZWN0aW9uID09PSAncmlnaHQnKSB7XG4gICAgICAgICAgICBpZiAoZGVlcCkge1xuICAgICAgICAgICAgICAgIHJldHVybiBtZXJnZURlZXBSaWdodCh2YWx1ZSwgb3RoZXJWYWx1ZSk7XG4gICAgICAgICAgICB9XG4gICAgICAgICAgICByZXR1cm4gbWVyZ2VSaWdodCh2YWx1ZSwgb3RoZXJWYWx1ZSk7XG4gICAgICAgIH1cbiAgICAgICAgaWYgKGRlZXApIHtcbiAgICAgICAgICAgIHJldHVybiBtZXJnZURlZXBMZWZ0KHZhbHVlLCBvdGhlclZhbHVlKTtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gbWVyZ2VMZWZ0KHZhbHVlLCBvdGhlclZhbHVlKTtcbiAgICB9LFxuICAgIFRvSnNvbjogKHZhbHVlKSA9PiB7XG4gICAgICAgIHJldHVybiBKU09OLnN0cmluZ2lmeSh2YWx1ZSk7XG4gICAgfSxcbiAgICBGcm9tSnNvbjogKHZhbHVlKSA9PiB7XG4gICAgICAgIHJldHVybiBKU09OLnBhcnNlKHZhbHVlKTtcbiAgICB9LFxuICAgIFRvUGFpcnM6ICh2YWx1ZSkgPT4ge1xuICAgICAgICByZXR1cm4gdG9QYWlycyh2YWx1ZSk7XG4gICAgfSxcbiAgICBGcm9tUGFpcnM6ICh2YWx1ZSkgPT4ge1xuICAgICAgICByZXR1cm4gZnJvbVBhaXJzKHZhbHVlKTtcbiAgICB9LFxuICAgIC8qIENvbmRpdGlvbmFscyAqL1xuICAgIElmOiAodmFsdWUsIGFyZ3MsIGdldEFzcGVjdCkgPT4ge1xuICAgICAgICBjb25zdCB7Y29tcGFyaXNvbiwgdGhlbiwgb3RoZXJ3aXNlfSA9IGFyZ3M7XG4gICAgICAgIGNvbnN0IGMgPSB0cmFuc2Zvcm1zW2NvbXBhcmlzb24udHJhbnNmb3JtXTtcblxuICAgICAgICBpZiAoYyh2YWx1ZSwgY29tcGFyaXNvbi5hcmdzLCBnZXRBc3BlY3QpKSB7XG4gICAgICAgICAgICByZXR1cm4gZXhlY3V0ZVRyYW5zZm9ybShcbiAgICAgICAgICAgICAgICB0aGVuLnRyYW5zZm9ybSxcbiAgICAgICAgICAgICAgICB2YWx1ZSxcbiAgICAgICAgICAgICAgICB0aGVuLmFyZ3MsXG4gICAgICAgICAgICAgICAgdGhlbi5uZXh0LFxuICAgICAgICAgICAgICAgIGdldEFzcGVjdFxuICAgICAgICAgICAgKTtcbiAgICAgICAgfVxuICAgICAgICBpZiAob3RoZXJ3aXNlKSB7XG4gICAgICAgICAgICByZXR1cm4gZXhlY3V0ZVRyYW5zZm9ybShcbiAgICAgICAgICAgICAgICBvdGhlcndpc2UudHJhbnNmb3JtLFxuICAgICAgICAgICAgICAgIHZhbHVlLFxuICAgICAgICAgICAgICAgIG90aGVyd2lzZS5hcmdzLFxuICAgICAgICAgICAgICAgIG90aGVyd2lzZS5uZXh0LFxuICAgICAgICAgICAgICAgIGdldEFzcGVjdFxuICAgICAgICAgICAgKTtcbiAgICAgICAgfVxuICAgICAgICByZXR1cm4gdmFsdWU7XG4gICAgfSxcbiAgICBFcXVhbHM6ICh2YWx1ZSwgYXJncywgZ2V0QXNwZWN0KSA9PiB7XG4gICAgICAgIHJldHVybiBlcXVhbHModmFsdWUsIGNvZXJjZUFzcGVjdChhcmdzLm90aGVyLCBnZXRBc3BlY3QpKTtcbiAgICB9LFxuICAgIE5vdEVxdWFsczogKHZhbHVlLCBhcmdzLCBnZXRBc3BlY3QpID0+IHtcbiAgICAgICAgcmV0dXJuICFlcXVhbHModmFsdWUsIGNvZXJjZUFzcGVjdChhcmdzLm90aGVyLCBnZXRBc3BlY3QpKTtcbiAgICB9LFxuICAgIE1hdGNoOiAodmFsdWUsIGFyZ3MsIGdldEFzcGVjdCkgPT4ge1xuICAgICAgICBjb25zdCByID0gbmV3IFJlZ0V4cChjb2VyY2VBc3BlY3QoYXJncy5vdGhlciwgZ2V0QXNwZWN0KSk7XG4gICAgICAgIHJldHVybiByLnRlc3QodmFsdWUpO1xuICAgIH0sXG4gICAgR3JlYXRlcjogKHZhbHVlLCBhcmdzLCBnZXRBc3BlY3QpID0+IHtcbiAgICAgICAgcmV0dXJuIHZhbHVlID4gY29lcmNlQXNwZWN0KGFyZ3Mub3RoZXIsIGdldEFzcGVjdCk7XG4gICAgfSxcbiAgICBHcmVhdGVyT3JFcXVhbHM6ICh2YWx1ZSwgYXJncywgZ2V0QXNwZWN0KSA9PiB7XG4gICAgICAgIHJldHVybiB2YWx1ZSA+PSBjb2VyY2VBc3BlY3QoYXJncy5vdGhlciwgZ2V0QXNwZWN0KTtcbiAgICB9LFxuICAgIExlc3NlcjogKHZhbHVlLCBhcmdzLCBnZXRBc3BlY3QpID0+IHtcbiAgICAgICAgcmV0dXJuIHZhbHVlIDwgY29lcmNlQXNwZWN0KGFyZ3Mub3RoZXIsIGdldEFzcGVjdCk7XG4gICAgfSxcbiAgICBMZXNzZXJPckVxdWFsczogKHZhbHVlLCBhcmdzLCBnZXRBc3BlY3QpID0+IHtcbiAgICAgICAgcmV0dXJuIHZhbHVlIDw9IGNvZXJjZUFzcGVjdChhcmdzLm90aGVyLCBnZXRBc3BlY3QpO1xuICAgIH0sXG4gICAgQW5kOiAodmFsdWUsIGFyZ3MsIGdldEFzcGVjdCkgPT4ge1xuICAgICAgICByZXR1cm4gdmFsdWUgJiYgY29lcmNlQXNwZWN0KGFyZ3Mub3RoZXIsIGdldEFzcGVjdCk7XG4gICAgfSxcbiAgICBPcjogKHZhbHVlLCBhcmdzLCBnZXRBc3BlY3QpID0+IHtcbiAgICAgICAgcmV0dXJuIHZhbHVlIHx8IGNvZXJjZUFzcGVjdChhcmdzLm90aGVyLCBnZXRBc3BlY3QpO1xuICAgIH0sXG4gICAgTm90OiAodmFsdWUpID0+IHtcbiAgICAgICAgcmV0dXJuICF2YWx1ZTtcbiAgICB9LFxuICAgIFJhd1ZhbHVlOiAodmFsdWUsIGFyZ3MpID0+IHtcbiAgICAgICAgcmV0dXJuIGFyZ3MudmFsdWU7XG4gICAgfSxcbiAgICBBc3BlY3RWYWx1ZTogKHZhbHVlLCBhcmdzLCBnZXRBc3BlY3QpID0+IHtcbiAgICAgICAgY29uc3Qge2lkZW50aXR5LCBhc3BlY3R9ID0gYXJncy50YXJnZXQ7XG4gICAgICAgIHJldHVybiBnZXRBc3BlY3QoaWRlbnRpdHksIGFzcGVjdCk7XG4gICAgfSxcbn07XG5cbmV4cG9ydCBjb25zdCBleGVjdXRlVHJhbnNmb3JtID0gKFxuICAgIHRyYW5zZm9ybTogc3RyaW5nLFxuICAgIHZhbHVlOiBhbnksXG4gICAgYXJnczogYW55LFxuICAgIG5leHQ6IEFycmF5PFRyYW5zZm9ybT4sXG4gICAgZ2V0QXNwZWN0OiBUcmFuc2Zvcm1HZXRBc3BlY3RGdW5jXG4pID0+IHtcbiAgICBjb25zdCB0ID0gdHJhbnNmb3Jtc1t0cmFuc2Zvcm1dO1xuICAgIGNvbnN0IG5ld1ZhbHVlID0gdCh2YWx1ZSwgYXJncywgZ2V0QXNwZWN0KTtcbiAgICBpZiAobmV4dC5sZW5ndGgpIHtcbiAgICAgICAgY29uc3QgbiA9IG5leHRbMF07XG4gICAgICAgIHJldHVybiBleGVjdXRlVHJhbnNmb3JtKFxuICAgICAgICAgICAgbi50cmFuc2Zvcm0sXG4gICAgICAgICAgICBuZXdWYWx1ZSxcbiAgICAgICAgICAgIG4uYXJncyxcbiAgICAgICAgICAgIC8vIEV4ZWN1dGUgdGhlIG5leHQgZmlyc3QsIHRoZW4gYmFjayB0byBjaGFpbi5cbiAgICAgICAgICAgIGNvbmNhdChuLm5leHQsIGRyb3AoMSwgbmV4dCkpLFxuICAgICAgICAgICAgZ2V0QXNwZWN0XG4gICAgICAgICk7XG4gICAgfVxuICAgIHJldHVybiBuZXdWYWx1ZTtcbn07XG5cbmV4cG9ydCBkZWZhdWx0IHRyYW5zZm9ybXM7XG4iLCJtb2R1bGUuZXhwb3J0cyA9IF9fV0VCUEFDS19FWFRFUk5BTF9NT0RVTEVfcmVhY3RfXzsiLCJtb2R1bGUuZXhwb3J0cyA9IF9fV0VCUEFDS19FWFRFUk5BTF9NT0RVTEVfcmVhY3RfZG9tX187Il0sIm5hbWVzIjpbXSwic291cmNlUm9vdCI6IiJ9