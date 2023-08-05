Object.defineProperty(exports, "__esModule", { value: true });
exports.Indicators = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_2 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const framer_motion_1 = require("framer-motion");
const indicator_1 = require("app/actionCreators/indicator");
const toastIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/alerts/toastIndicator"));
const indicatorStore_1 = (0, tslib_1.__importDefault)(require("app/stores/indicatorStore"));
const theme_1 = require("app/utils/theme");
const Toasts = (0, styled_1.default)('div') `
  position: fixed;
  right: 30px;
  bottom: 30px;
  z-index: ${p => p.theme.zIndex.toast};
`;
class Indicators extends react_1.Component {
    constructor() {
        super(...arguments);
        this.handleDismiss = (indicator) => {
            (0, indicator_1.removeIndicator)(indicator);
        };
    }
    render() {
        const _a = this.props, { items } = _a, props = (0, tslib_1.__rest)(_a, ["items"]);
        return (<Toasts {...props}>
        <framer_motion_1.AnimatePresence>
          {items.map((indicator, i) => (
            // We purposefully use `i` as key here because of transitions
            // Toasts can now queue up, so when we change from [firstToast] -> [secondToast],
            // we don't want to  animate `firstToast` out and `secondToast` in, rather we want
            // to replace `firstToast` with `secondToast`
            <toastIndicator_1.default onDismiss={this.handleDismiss} indicator={indicator} key={i}/>))}
        </framer_motion_1.AnimatePresence>
      </Toasts>);
    }
}
exports.Indicators = Indicators;
Indicators.defaultProps = {
    items: [],
};
class IndicatorsContainer extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = { items: indicatorStore_1.default.get() };
        this.unlistener = indicatorStore_1.default.listen((items) => {
            this.setState({ items });
        }, undefined);
    }
    componentWillUnmount() {
        var _a;
        (_a = this.unlistener) === null || _a === void 0 ? void 0 : _a.call(this);
    }
    render() {
        // #NEW-SETTINGS - remove ThemeProvider here once new settings is merged
        // `alerts.html` django view includes this container and doesn't have a theme provider
        // not even sure it is used in django views but this is just an easier temp solution
        return (<react_2.ThemeProvider theme={theme_1.lightTheme}>
        <Indicators {...this.props} items={this.state.items}/>
      </react_2.ThemeProvider>);
    }
}
exports.default = IndicatorsContainer;
//# sourceMappingURL=indicators.jsx.map