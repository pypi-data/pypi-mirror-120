Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const modal_1 = require("app/actionCreators/modal");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const panels_1 = require("app/components/panels");
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const recreateRoute_1 = (0, tslib_1.__importDefault)(require("app/utils/recreateRoute"));
const settingsPageHeader_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsPageHeader"));
const allTeamsList_1 = (0, tslib_1.__importDefault)(require("./allTeamsList"));
const organizationAccessRequests_1 = (0, tslib_1.__importDefault)(require("./organizationAccessRequests"));
function OrganizationTeams({ allTeams, activeTeams, organization, access, features, routes, params, requestList, onRemoveAccessRequest, }) {
    if (!organization) {
        return null;
    }
    const canCreateTeams = access.has('project:admin');
    const action = (<button_1.default priority="primary" size="small" disabled={!canCreateTeams} title={!canCreateTeams ? (0, locale_1.t)('You do not have permission to create teams') : undefined} onClick={() => (0, modal_1.openCreateTeamModal)({
            organization,
        })} icon={<icons_1.IconAdd size="xs" isCircled/>}>
      {(0, locale_1.t)('Create Team')}
    </button_1.default>);
    const teamRoute = routes.find(({ path }) => path === 'teams/');
    const urlPrefix = teamRoute
        ? (0, recreateRoute_1.default)(teamRoute, { routes, params, stepBack: -2 })
        : '';
    const activeTeamIds = new Set(activeTeams.map(team => team.id));
    const otherTeams = allTeams.filter(team => !activeTeamIds.has(team.id));
    const title = (0, locale_1.t)('Teams');
    return (<div data-test-id="team-list">
      <sentryDocumentTitle_1.default title={title} orgSlug={organization.slug}/>
      <settingsPageHeader_1.default title={title} action={action}/>

      <organizationAccessRequests_1.default orgId={params.orgId} requestList={requestList} onRemoveAccessRequest={onRemoveAccessRequest}/>
      <panels_1.Panel>
        <panels_1.PanelHeader>{(0, locale_1.t)('Your Teams')}</panels_1.PanelHeader>
        <panels_1.PanelBody>
          <allTeamsList_1.default urlPrefix={urlPrefix} organization={organization} teamList={activeTeams} access={access} openMembership={false}/>
        </panels_1.PanelBody>
      </panels_1.Panel>
      <panels_1.Panel>
        <panels_1.PanelHeader>{(0, locale_1.t)('Other Teams')}</panels_1.PanelHeader>
        <panels_1.PanelBody>
          <allTeamsList_1.default urlPrefix={urlPrefix} organization={organization} teamList={otherTeams} access={access} openMembership={!!(features.has('open-membership') || access.has('org:write'))}/>
        </panels_1.PanelBody>
      </panels_1.Panel>
    </div>);
}
exports.default = OrganizationTeams;
//# sourceMappingURL=organizationTeams.jsx.map