Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const constants_1 = require("app/constants");
const replaceRouterParams_1 = (0, tslib_1.__importDefault)(require("app/utils/replaceRouterParams"));
const withConfig_1 = (0, tslib_1.__importDefault)(require("app/utils/withConfig"));
/**
 * This view is used when a user lands on the route `/` which historically
 * is a server-rendered route which redirects the user to their last selected organization
 *
 * However, this does not work when in the experimental SPA mode (e.g. developing against a remote API,
 * or a deploy preview), so we must replicate the functionality and redirect
 * the user to the proper organization.
 *
 * TODO: There might be an edge case where user does not have `lastOrganization` set,
 * in which case we should load their list of organizations and make a decision
 */
class AppRoot extends react_1.Component {
    componentDidMount() {
        const { config } = this.props;
        if (config.lastOrganization) {
            react_router_1.browserHistory.replace((0, replaceRouterParams_1.default)(constants_1.DEFAULT_APP_ROUTE, { orgSlug: config.lastOrganization }));
        }
    }
    render() {
        return null;
    }
}
exports.default = (0, withConfig_1.default)(AppRoot);
//# sourceMappingURL=root.jsx.map