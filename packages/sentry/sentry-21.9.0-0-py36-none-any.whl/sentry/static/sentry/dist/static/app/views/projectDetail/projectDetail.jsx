Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const globalSelection_1 = require("app/actionCreators/globalSelection");
const tags_1 = require("app/actionCreators/tags");
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const breadcrumbs_1 = (0, tslib_1.__importDefault)(require("app/components/breadcrumbs"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const createAlertButton_1 = (0, tslib_1.__importDefault)(require("app/components/createAlertButton"));
const globalAppStoreConnectUpdateAlert_1 = (0, tslib_1.__importDefault)(require("app/components/globalAppStoreConnectUpdateAlert"));
const globalSdkUpdateAlert_1 = (0, tslib_1.__importDefault)(require("app/components/globalSdkUpdateAlert"));
const idBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge"));
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const lightWeightNoProjectMessage_1 = (0, tslib_1.__importDefault)(require("app/components/lightWeightNoProjectMessage"));
const globalSelectionHeader_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/globalSelectionHeader"));
const missingProjectMembership_1 = (0, tslib_1.__importDefault)(require("app/components/projects/missingProjectMembership"));
const textOverflow_1 = (0, tslib_1.__importDefault)(require("app/components/textOverflow"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const organization_1 = require("app/styles/organization");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const routeTitle_1 = (0, tslib_1.__importDefault)(require("app/utils/routeTitle"));
const withGlobalSelection_1 = (0, tslib_1.__importDefault)(require("app/utils/withGlobalSelection"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const asyncView_1 = (0, tslib_1.__importDefault)(require("app/views/asyncView"));
const projectScoreCards_1 = (0, tslib_1.__importDefault)(require("./projectScoreCards/projectScoreCards"));
const projectCharts_1 = (0, tslib_1.__importDefault)(require("./projectCharts"));
const projectFilters_1 = (0, tslib_1.__importDefault)(require("./projectFilters"));
const projectIssues_1 = (0, tslib_1.__importDefault)(require("./projectIssues"));
const projectLatestAlerts_1 = (0, tslib_1.__importDefault)(require("./projectLatestAlerts"));
const projectLatestReleases_1 = (0, tslib_1.__importDefault)(require("./projectLatestReleases"));
const projectQuickLinks_1 = (0, tslib_1.__importDefault)(require("./projectQuickLinks"));
const projectTeamAccess_1 = (0, tslib_1.__importDefault)(require("./projectTeamAccess"));
class ProjectDetail extends asyncView_1.default {
    constructor() {
        super(...arguments);
        this.handleProjectChange = (selectedProjects) => {
            const { projects, router, location, organization } = this.props;
            const newlySelectedProject = projects.find(p => p.id === String(selectedProjects[0]));
            // if we change project in global header, we need to sync the project slug in the URL
            if (newlySelectedProject === null || newlySelectedProject === void 0 ? void 0 : newlySelectedProject.id) {
                router.replace({
                    pathname: `/organizations/${organization.slug}/projects/${newlySelectedProject.slug}/`,
                    query: Object.assign(Object.assign({}, location.query), { project: newlySelectedProject.id, environment: undefined }),
                });
            }
        };
        this.handleSearch = (query) => {
            const { router, location } = this.props;
            router.replace({
                pathname: location.pathname,
                query: Object.assign(Object.assign({}, location.query), { query }),
            });
        };
        this.tagValueLoader = (key, search) => {
            const { location, organization } = this.props;
            const { project: projectId } = location.query;
            return (0, tags_1.fetchTagValues)(this.api, organization.slug, key, search, projectId ? [projectId] : null, location.query);
        };
    }
    getTitle() {
        const { params } = this.props;
        return (0, routeTitle_1.default)((0, locale_1.t)('Project %s', params.projectId), params.orgId, false);
    }
    componentDidMount() {
        this.syncProjectWithSlug();
        if (this.props.location.query.project) {
            this.fetchSessionsExistence();
        }
    }
    componentDidUpdate(prevProps) {
        this.syncProjectWithSlug();
        if (prevProps.location.query.project !== this.props.location.query.project) {
            this.fetchSessionsExistence();
        }
    }
    get project() {
        const { projects, params } = this.props;
        return projects.find(p => p.slug === params.projectId);
    }
    fetchSessionsExistence() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { organization, location } = this.props;
            const { project: projectId, query } = location.query;
            if (!projectId) {
                return;
            }
            this.setState({
                hasSessions: null,
            });
            try {
                const response = yield this.api.requestPromise(`/organizations/${organization.slug}/sessions/`, {
                    query: {
                        project: projectId,
                        field: 'sum(session)',
                        statsPeriod: '90d',
                        interval: '1d',
                        query,
                    },
                });
                this.setState({
                    hasSessions: response.groups[0].totals['sum(session)'] > 0,
                });
            }
            catch (_a) {
                // do nothing
            }
        });
    }
    syncProjectWithSlug() {
        var _a;
        const { router, location } = this.props;
        const projectId = (_a = this.project) === null || _a === void 0 ? void 0 : _a.id;
        if (projectId && projectId !== location.query.project) {
            // if someone visits /organizations/sentry/projects/javascript/ (without ?project=XXX) we need to update URL and globalSelection with the right project ID
            (0, globalSelection_1.updateProjects)([Number(projectId)], router);
        }
    }
    isProjectStabilized() {
        var _a;
        const { selection, location } = this.props;
        const projectId = (_a = this.project) === null || _a === void 0 ? void 0 : _a.id;
        return ((0, utils_1.defined)(projectId) &&
            projectId === location.query.project &&
            projectId === String(selection.projects[0]));
    }
    renderLoading() {
        return this.renderBody();
    }
    renderNoAccess(project) {
        const { organization } = this.props;
        return (<organization_1.PageContent>
        <missingProjectMembership_1.default organization={organization} projectSlug={project.slug}/>
      </organization_1.PageContent>);
    }
    renderProjectNotFound() {
        return (<organization_1.PageContent>
        <alert_1.default type="error" icon={<icons_1.IconWarning />}>
          {(0, locale_1.t)('This project could not be found.')}
        </alert_1.default>
      </organization_1.PageContent>);
    }
    renderBody() {
        const { organization, params, location, router, loadingProjects, selection } = this.props;
        const project = this.project;
        const { hasSessions } = this.state;
        const { query } = location.query;
        const hasPerformance = organization.features.includes('performance-view');
        const hasTransactions = hasPerformance && (project === null || project === void 0 ? void 0 : project.firstTransactionEvent);
        const isProjectStabilized = this.isProjectStabilized();
        const visibleCharts = ['chart1'];
        if (hasTransactions || hasSessions) {
            visibleCharts.push('chart2');
        }
        if (!loadingProjects && !project) {
            return this.renderProjectNotFound();
        }
        if (!loadingProjects && project && !project.hasAccess) {
            return this.renderNoAccess(project);
        }
        return (<globalSelectionHeader_1.default disableMultipleProjectSelection skipLoadLastUsed onUpdateProjects={this.handleProjectChange}>
        <lightWeightNoProjectMessage_1.default organization={organization}>
          <StyledPageContent>
            <Layout.Header>
              <Layout.HeaderContent>
                <breadcrumbs_1.default crumbs={[
                {
                    to: `/organizations/${params.orgId}/projects/`,
                    label: (0, locale_1.t)('Projects'),
                },
                { label: (0, locale_1.t)('Project Details') },
            ]}/>
                <Layout.Title>
                  <textOverflow_1.default>
                    {project && (<idBadge_1.default project={project} avatarSize={28} displayName={params.projectId} disableLink/>)}
                  </textOverflow_1.default>
                </Layout.Title>
              </Layout.HeaderContent>

              <Layout.HeaderActions>
                <buttonBar_1.default gap={1}>
                  <button_1.default to={
            // if we are still fetching project, we can use project slug to build issue stream url and let the redirect handle it
            (project === null || project === void 0 ? void 0 : project.id)
                ? `/organizations/${params.orgId}/issues/?project=${project.id}`
                : `/${params.orgId}/${params.projectId}`}>
                    {(0, locale_1.t)('View All Issues')}
                  </button_1.default>
                  <createAlertButton_1.default organization={organization} projectSlug={params.projectId}/>
                  <button_1.default icon={<icons_1.IconSettings />} label={(0, locale_1.t)('Settings')} to={`/settings/${params.orgId}/projects/${params.projectId}/`}/>
                </buttonBar_1.default>
              </Layout.HeaderActions>
            </Layout.Header>

            <Layout.Body>
              <StyledSdkUpdatesAlert />
              <StyledGlobalAppStoreConnectUpdateAlert project={project} organization={organization}/>
              <Layout.Main>
                <feature_1.default features={['semver']} organization={organization}>
                  <ProjectFiltersWrapper>
                    <projectFilters_1.default query={query} onSearch={this.handleSearch} tagValueLoader={this.tagValueLoader}/>
                  </ProjectFiltersWrapper>
                </feature_1.default>

                <projectScoreCards_1.default organization={organization} isProjectStabilized={isProjectStabilized} selection={selection} hasSessions={hasSessions} hasTransactions={hasTransactions} query={query}/>
                {isProjectStabilized && (<react_1.Fragment>
                    {visibleCharts.map((id, index) => (<projectCharts_1.default location={location} organization={organization} router={router} key={`project-charts-${id}`} chartId={id} chartIndex={index} projectId={project === null || project === void 0 ? void 0 : project.id} hasSessions={hasSessions} hasTransactions={!!hasTransactions} visibleCharts={visibleCharts} query={query}/>))}
                    <projectIssues_1.default organization={organization} location={location} projectId={selection.projects[0]} query={query} api={this.api}/>
                  </react_1.Fragment>)}
              </Layout.Main>
              <Layout.Side>
                <projectTeamAccess_1.default organization={organization} project={project}/>
                <feature_1.default features={['incidents']} organization={organization}>
                  <projectLatestAlerts_1.default organization={organization} projectSlug={params.projectId} location={location} isProjectStabilized={isProjectStabilized}/>
                </feature_1.default>
                <projectLatestReleases_1.default organization={organization} projectSlug={params.projectId} projectId={project === null || project === void 0 ? void 0 : project.id} location={location} isProjectStabilized={isProjectStabilized}/>
                <projectQuickLinks_1.default organization={organization} project={project} location={location}/>
              </Layout.Side>
            </Layout.Body>
          </StyledPageContent>
        </lightWeightNoProjectMessage_1.default>
      </globalSelectionHeader_1.default>);
    }
}
const StyledPageContent = (0, styled_1.default)(organization_1.PageContent) `
  padding: 0;
`;
const ProjectFiltersWrapper = (0, styled_1.default)('div') `
  margin-bottom: ${(0, space_1.default)(2)};
  display: grid;
`;
const StyledSdkUpdatesAlert = (0, styled_1.default)(globalSdkUpdateAlert_1.default) `
  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    margin-bottom: 0;
  }
`;
StyledSdkUpdatesAlert.defaultProps = {
    Wrapper: p => <Layout.Main fullWidth {...p}/>,
};
const StyledGlobalAppStoreConnectUpdateAlert = (0, styled_1.default)(globalAppStoreConnectUpdateAlert_1.default) `
  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    margin-bottom: 0;
  }
`;
StyledGlobalAppStoreConnectUpdateAlert.defaultProps = {
    Wrapper: p => <Layout.Main fullWidth {...p}/>,
};
exports.default = (0, withProjects_1.default)((0, withGlobalSelection_1.default)(ProjectDetail));
//# sourceMappingURL=projectDetail.jsx.map