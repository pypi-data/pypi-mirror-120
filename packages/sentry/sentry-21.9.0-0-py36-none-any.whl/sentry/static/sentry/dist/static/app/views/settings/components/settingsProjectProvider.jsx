Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const withProject_1 = (0, tslib_1.__importDefault)(require("app/utils/withProject"));
/**
 * Simple Component that takes project from context and passes it as props to children
 *
 * Don't do anything additional (e.g. loader) because not all children require project
 *
 * This is made because some components (e.g. ProjectPluginDetail) takes project as prop
 */
class SettingsProjectProvider extends react_1.Component {
    render() {
        const { children, project } = this.props;
        if ((0, react_1.isValidElement)(children)) {
            return (0, react_1.cloneElement)(children, Object.assign(Object.assign(Object.assign({}, this.props), children.props), { project }));
        }
        return null;
    }
}
exports.default = (0, withProject_1.default)(SettingsProjectProvider);
//# sourceMappingURL=settingsProjectProvider.jsx.map