Object.defineProperty(exports, "__esModule", { value: true });
exports.isLightweightOrganization = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const sentryTypes_1 = (0, tslib_1.__importDefault)(require("app/sentryTypes"));
const withOrganizationMock = WrappedComponent => { var _a; return _a = class WithOrganizationMockWrapper extends react_1.Component {
        render() {
            return (<WrappedComponent organization={this.context.organization || TestStubs.Organization()} {...this.props}/>);
        }
    },
    _a.contextTypes = {
        organization: sentryTypes_1.default.Organization,
    },
    _a; };
const isLightweightOrganization = () => { };
exports.isLightweightOrganization = isLightweightOrganization;
exports.default = withOrganizationMock;
//# sourceMappingURL=withOrganization.jsx.map