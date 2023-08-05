Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const alertStore_1 = (0, tslib_1.__importDefault)(require("app/stores/alertStore"));
const theme_1 = require("app/utils/theme");
const alertMessage_1 = (0, tslib_1.__importDefault)(require("./alertMessage"));
class SystemAlerts extends React.Component {
    constructor() {
        super(...arguments);
        this.state = this.getInitialState();
        this.unlistener = alertStore_1.default.listen((alerts) => this.setState({ alerts }), undefined);
    }
    getInitialState() {
        return {
            alerts: alertStore_1.default.getInitialState(),
        };
    }
    componentWillUnmount() {
        var _a;
        (_a = this.unlistener) === null || _a === void 0 ? void 0 : _a.call(this);
    }
    render() {
        const { className } = this.props;
        const { alerts } = this.state;
        return (<react_1.ThemeProvider theme={theme_1.lightTheme}>
        <div className={className}>
          {alerts.map((alert, index) => (<alertMessage_1.default alert={alert} key={`${alert.id}-${index}`} system/>))}
        </div>
      </react_1.ThemeProvider>);
    }
}
exports.default = SystemAlerts;
//# sourceMappingURL=systemAlerts.jsx.map