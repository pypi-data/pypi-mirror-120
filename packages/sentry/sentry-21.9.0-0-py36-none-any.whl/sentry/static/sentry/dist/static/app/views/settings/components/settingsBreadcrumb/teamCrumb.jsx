Object.defineProperty(exports, "__esModule", { value: true });
exports.TeamCrumb = void 0;
const tslib_1 = require("tslib");
const react_router_1 = require("react-router");
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const recreateRoute_1 = (0, tslib_1.__importDefault)(require("app/utils/recreateRoute"));
const withTeams_1 = (0, tslib_1.__importDefault)(require("app/utils/withTeams"));
const breadcrumbDropdown_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsBreadcrumb/breadcrumbDropdown"));
const menuItem_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsBreadcrumb/menuItem"));
const _1 = require(".");
const TeamCrumb = (_a) => {
    var { teams, params, routes, route } = _a, props = (0, tslib_1.__rest)(_a, ["teams", "params", "routes", "route"]);
    const team = teams.find(({ slug }) => slug === params.teamId);
    const hasMenu = teams.length > 1;
    if (!team) {
        return null;
    }
    return (<breadcrumbDropdown_1.default name={<_1.CrumbLink to={(0, recreateRoute_1.default)(route, {
                routes,
                params: Object.assign(Object.assign({}, params), { teamId: team.slug }),
            })}>
          <idBadge_1.default avatarSize={18} team={team}/>
        </_1.CrumbLink>} onSelect={item => {
            react_router_1.browserHistory.push((0, recreateRoute_1.default)('', {
                routes,
                params: Object.assign(Object.assign({}, params), { teamId: item.value }),
            }));
        }} hasMenu={hasMenu} route={route} items={teams.map((teamItem, index) => ({
            index,
            value: teamItem.slug,
            label: (<menuItem_1.default>
            <idBadge_1.default team={teamItem}/>
          </menuItem_1.default>),
        }))} {...props}/>);
};
exports.TeamCrumb = TeamCrumb;
exports.default = (0, withTeams_1.default)(TeamCrumb);
//# sourceMappingURL=teamCrumb.jsx.map