Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const getDisplayName_1 = (0, tslib_1.__importDefault)(require("app/utils/getDisplayName"));
/**
 * Higher order component that passes the config object to the wrapped component
 */
function withConfig(WrappedComponent) {
    class WithConfig extends React.Component {
        constructor() {
            super(...arguments);
            this.state = { config: configStore_1.default.getConfig() };
            this.unsubscribe = configStore_1.default.listen(() => this.setState({ config: configStore_1.default.getConfig() }), undefined);
        }
        componentWillUnmount() {
            this.unsubscribe();
        }
        render() {
            const _a = this.props, { config } = _a, props = (0, tslib_1.__rest)(_a, ["config"]);
            return (<WrappedComponent {...Object.assign({ config: config !== null && config !== void 0 ? config : this.state.config }, props)}/>);
        }
    }
    WithConfig.displayName = `withConfig(${(0, getDisplayName_1.default)(WrappedComponent)})`;
    return WithConfig;
}
exports.default = withConfig;
//# sourceMappingURL=withConfig.jsx.map