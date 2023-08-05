Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const partition_1 = (0, tslib_1.__importDefault)(require("lodash/partition"));
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withProjectsSpecified_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjectsSpecified"));
const globalSelectionHeader_1 = (0, tslib_1.__importDefault)(require("./globalSelectionHeader"));
const initializeGlobalSelectionHeader_1 = (0, tslib_1.__importDefault)(require("./initializeGlobalSelectionHeader"));
class GlobalSelectionHeaderContainer extends React.Component {
    constructor() {
        super(...arguments);
        this.getProjects = () => {
            const { organization, projects } = this.props;
            const { isSuperuser } = configStore_1.default.get('user');
            const isOrgAdmin = organization.access.includes('org:admin');
            const [memberProjects, nonMemberProjects] = (0, partition_1.default)(projects, project => project.isMember);
            if (isSuperuser || isOrgAdmin) {
                return [memberProjects, nonMemberProjects];
            }
            return [memberProjects, []];
        };
    }
    render() {
        const _a = this.props, { loadingProjects, location, organization, router, routes, defaultSelection, forceProject, shouldForceProject, skipLoadLastUsed, showAbsolute } = _a, props = (0, tslib_1.__rest)(_a, ["loadingProjects", "location", "organization", "router", "routes", "defaultSelection", "forceProject", "shouldForceProject", "skipLoadLastUsed", "showAbsolute"]);
        const enforceSingleProject = !organization.features.includes('global-views');
        const [memberProjects, nonMemberProjects] = this.getProjects();
        // We can initialize before ProjectsStore is fully loaded if we don't need to enforce single project.
        return (<React.Fragment>
        {(!loadingProjects || (!shouldForceProject && !enforceSingleProject)) && (<initializeGlobalSelectionHeader_1.default location={location} skipLoadLastUsed={!!skipLoadLastUsed} router={router} organization={organization} defaultSelection={defaultSelection} forceProject={forceProject} shouldForceProject={!!shouldForceProject} shouldEnforceSingleProject={enforceSingleProject} memberProjects={memberProjects} showAbsolute={showAbsolute}/>)}
        <globalSelectionHeader_1.default {...props} loadingProjects={loadingProjects} location={location} organization={organization} router={router} routes={routes} shouldForceProject={!!shouldForceProject} defaultSelection={defaultSelection} forceProject={forceProject} memberProjects={memberProjects} nonMemberProjects={nonMemberProjects} showAbsolute={showAbsolute}/>
      </React.Fragment>);
    }
}
exports.default = (0, withOrganization_1.default)((0, withProjectsSpecified_1.default)((0, react_router_1.withRouter)(GlobalSelectionHeaderContainer)));
//# sourceMappingURL=index.jsx.map