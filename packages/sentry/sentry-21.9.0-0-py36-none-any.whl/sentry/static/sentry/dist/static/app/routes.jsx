Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const lazyLoad_1 = (0, tslib_1.__importDefault)(require("app/components/lazyLoad"));
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const hookStore_1 = (0, tslib_1.__importDefault)(require("app/stores/hookStore"));
const errorHandler_1 = (0, tslib_1.__importDefault)(require("app/utils/errorHandler"));
const app_1 = (0, tslib_1.__importDefault)(require("app/views/app"));
const layout_1 = (0, tslib_1.__importDefault)(require("app/views/auth/layout"));
const container_1 = (0, tslib_1.__importDefault)(require("app/views/issueList/container"));
const overview_1 = (0, tslib_1.__importDefault)(require("app/views/issueList/overview"));
const organizationContext_1 = (0, tslib_1.__importDefault)(require("app/views/organizationContext"));
const organizationDetails_1 = (0, tslib_1.__importStar)(require("app/views/organizationDetails"));
const types_1 = require("app/views/organizationGroupDetails/types");
const organizationRoot_1 = (0, tslib_1.__importDefault)(require("app/views/organizationRoot"));
const projectEventRedirect_1 = (0, tslib_1.__importDefault)(require("app/views/projectEventRedirect"));
const redirectDeprecatedProjectRoute_1 = (0, tslib_1.__importDefault)(require("app/views/projects/redirectDeprecatedProjectRoute"));
const routeNotFound_1 = (0, tslib_1.__importDefault)(require("app/views/routeNotFound"));
const settingsProjectProvider_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsProjectProvider"));
const settingsWrapper_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/settingsWrapper"));
/**
 * We add some additional props to our routes
 */
const Route = react_router_1.Route;
const IndexRoute = react_router_1.IndexRoute;
/**
 * Use react-router to lazy load a route. Use this for codesplitting containers
 * (e.g. SettingsLayout)
 *
 * The typical method for lazy loading a route leaf node is using the
 * <LazyLoad> component + `componentPromise`
 *
 * For wrapper / layout views react-router handles the route tree better by
 * using getComponent with this lazyLoad helper. If we just use <LazyLoad> it
 * will end up having to re-render more components than necessary.
 */
const lazyLoad = (load) => (_loc, cb) => load().then(module => cb(null, module.default));
const hook = (name) => hookStore_1.default.get(name).map(cb => cb());
const SafeLazyLoad = (0, errorHandler_1.default)(lazyLoad_1.default);
function routes() {
    const accountSettingsRoutes = (<React.Fragment>
      <react_router_1.IndexRedirect to="details/"/>

      <Route path="details/" name="Details" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/accountDetails')))} component={SafeLazyLoad}/>

      <Route path="notifications/" name="Notifications">
        <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/notifications/notificationSettings')))} component={SafeLazyLoad}/>
        <Route path=":fineTuneType/" name="Fine Tune Alerts" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/accountNotificationFineTuning')))} component={SafeLazyLoad}/>
      </Route>
      <Route path="emails/" name="Emails" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/accountEmails')))} component={SafeLazyLoad}/>

      <Route path="authorizations/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/accountAuthorizations')))} component={SafeLazyLoad}/>

      <Route name="Security" path="security/">
        <Route componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/accountSecurity/accountSecurityWrapper')))} component={SafeLazyLoad}>
          <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/accountSecurity')))} component={SafeLazyLoad}/>
          <Route path="session-history/" name="Session History" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/accountSecurity/sessionHistory')))} component={SafeLazyLoad}/>
          <Route path="mfa/:authId/" name="Details" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/accountSecurity/accountSecurityDetails')))} component={SafeLazyLoad}/>
        </Route>

        <Route path="mfa/:authId/enroll/" name="Enroll" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/accountSecurity/accountSecurityEnroll')))} component={SafeLazyLoad}/>
      </Route>

      <Route path="subscriptions/" name="Subscriptions" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/accountSubscriptions')))} component={SafeLazyLoad}/>

      <Route path="identities/" name="Identities" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/accountIdentities')))} component={SafeLazyLoad}/>

      <Route path="api/" name="API">
        <react_router_1.IndexRedirect to="auth-tokens/"/>

        <Route path="auth-tokens/" name="Auth Tokens">
          <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/apiTokens')))} component={SafeLazyLoad}/>
          <Route path="new-token/" name="Create New Token" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/apiNewToken')))} component={SafeLazyLoad}/>
        </Route>

        <Route path="applications/" name="Applications">
          <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/apiApplications')))} component={SafeLazyLoad}/>
          <Route path=":appId/" name="Details" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/apiApplications/details')))} component={SafeLazyLoad}/>
        </Route>

        {hook('routes:api')}
      </Route>

      <Route path="close-account/" name="Close Account" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/accountClose')))} component={SafeLazyLoad}/>
    </React.Fragment>);
    const projectSettingsRoutes = (<React.Fragment>
      <IndexRoute name="General" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectGeneralSettings')))} component={SafeLazyLoad}/>
      <Route path="teams/" name="Teams" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/project/projectTeams')))} component={SafeLazyLoad}/>

      <Route name="Alerts" path="alerts/" component={SafeLazyLoad} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectAlerts')))}>
        <IndexRoute component={SafeLazyLoad} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectAlerts/settings')))}/>
        <react_router_1.Redirect from="new/" to="/organizations/:orgId/alerts/:projectId/new/"/>
        <react_router_1.Redirect from="rules/" to="/organizations/:orgId/alerts/rules/"/>
        <react_router_1.Redirect from="rules/new/" to="/organizations/:orgId/alerts/:projectId/new/"/>
        <react_router_1.Redirect from="metric-rules/new/" to="/organizations/:orgId/alerts/:projectId/new/"/>
        <react_router_1.Redirect from="rules/:ruleId/" to="/organizations/:orgId/alerts/rules/:projectId/:ruleId/"/>
        <react_router_1.Redirect from="metric-rules/:ruleId/" to="/organizations/:orgId/alerts/metric-rules/:projectId/:ruleId/"/>
      </Route>

      <Route name="Environments" path="environments/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/project/projectEnvironments')))} component={SafeLazyLoad}>
        <IndexRoute />
        <Route path="hidden/"/>
      </Route>
      <Route name="Tags" path="tags/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectTags')))} component={SafeLazyLoad}/>
      <react_router_1.Redirect from="issue-tracking/" to="/settings/:orgId/:projectId/plugins/"/>
      <Route path="release-tracking/" name="Release Tracking" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/project/projectReleaseTracking')))} component={SafeLazyLoad}/>
      <Route path="ownership/" name="Issue Owners" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/project/projectOwnership')))} component={SafeLazyLoad}/>
      <Route path="data-forwarding/" name="Data Forwarding" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectDataForwarding')))} component={SafeLazyLoad}/>
      <Route name={(0, locale_1.t)('Security & Privacy')} path="security-and-privacy/" component={SafeLazyLoad} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectSecurityAndPrivacy')))}/>
      <Route path="debug-symbols/" name="Debug Information Files" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectDebugFiles')))} component={SafeLazyLoad}/>
      <Route path="proguard/" name={(0, locale_1.t)('ProGuard Mappings')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectProguard')))} component={SafeLazyLoad}/>
      <Route path="performance/" name={(0, locale_1.t)('Performance')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectPerformance')))} component={SafeLazyLoad}/>
      <Route path="source-maps/" name={(0, locale_1.t)('Source Maps')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectSourceMaps')))} component={SafeLazyLoad}>
        <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectSourceMaps/list')))} component={SafeLazyLoad}/>
        <Route path=":name/" name={(0, locale_1.t)('Archive')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectSourceMaps/detail')))} component={SafeLazyLoad}/>
      </Route>
      <Route path="processing-issues/" name="Processing Issues" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/project/projectProcessingIssues')))} component={SafeLazyLoad}/>
      <Route path="filters/" name="Inbound Filters" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/project/projectFilters')))} component={SafeLazyLoad}>
        <react_router_1.IndexRedirect to="data-filters/"/>
        <Route path=":filterType/"/>
      </Route>
      <Route name={(0, locale_1.t)('Filters & Sampling')} path="filters-and-sampling/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/project/filtersAndSampling')))} component={SafeLazyLoad}/>
      <Route path="issue-grouping/" name={(0, locale_1.t)('Issue Grouping')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectIssueGrouping')))} component={SafeLazyLoad}/>
      <Route path="hooks/" name="Service Hooks" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/project/projectServiceHooks')))} component={SafeLazyLoad}/>
      <Route path="hooks/new/" name="Create Service Hook" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/project/projectCreateServiceHook')))} component={SafeLazyLoad}/>
      <Route path="hooks/:hookId/" name="Service Hook Details" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/project/projectServiceHookDetails')))} component={SafeLazyLoad}/>
      <Route path="keys/" name="Client Keys">
        <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/project/projectKeys/list')))} component={SafeLazyLoad}/>

        <Route path=":keyId/" name="Details" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/project/projectKeys/details')))} component={SafeLazyLoad}/>
      </Route>
      <Route path="user-feedback/" name="User Feedback" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/project/projectUserFeedback')))} component={SafeLazyLoad}/>
      <react_router_1.Redirect from="csp/" to="security-headers/"/>
      <Route path="security-headers/" name="Security Headers">
        <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectSecurityHeaders')))} component={SafeLazyLoad}/>
        <Route path="csp/" name="Content Security Policy" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectSecurityHeaders/csp')))} component={SafeLazyLoad}/>
        <Route path="expect-ct/" name="Certificate Transparency" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectSecurityHeaders/expectCt')))} component={SafeLazyLoad}/>
        <Route path="hpkp/" name="HPKP" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectSecurityHeaders/hpkp')))} component={SafeLazyLoad}/>
      </Route>
      <Route path="plugins/" name="Legacy Integrations">
        <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectPlugins')))} component={SafeLazyLoad}/>
        <Route path=":pluginId/" name="Integration Details" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/projectPlugins/details')))} component={SafeLazyLoad}/>
      </Route>
      <Route path="install/" name="Configuration">
        <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/projectInstall/overview')))} component={SafeLazyLoad}/>
        <Route path=":platform/" name="Docs" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/projectInstall/platformOrIntegration')))} component={SafeLazyLoad}/>
      </Route>
    </React.Fragment>);
    // This is declared in the routes() function because some routes need the
    // hook store which is not available at import time.
    const orgSettingsRoutes = (<React.Fragment>
      <IndexRoute name="General" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationGeneralSettings')))} component={SafeLazyLoad}/>

      <Route path="projects/" name="Projects" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationProjects')))} component={SafeLazyLoad}/>

      <Route path="api-keys/" name="API Key">
        <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationApiKeys')))} component={SafeLazyLoad}/>

        <Route path=":apiKey/" name="Details" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationApiKeys/organizationApiKeyDetails')))} component={SafeLazyLoad}/>
      </Route>

      <Route path="audit-log/" name="Audit Log" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationAuditLog')))} component={SafeLazyLoad}/>

      <Route path="auth/" name="Auth Providers" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationAuth')))} component={SafeLazyLoad}/>

      <react_router_1.Redirect from="members/requests" to="members/"/>
      <Route path="members/" name="Members">
        <Route componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationMembers/organizationMembersWrapper')))} component={SafeLazyLoad}>
          <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationMembers/organizationMembersList')))} component={SafeLazyLoad}/>
        </Route>

        <Route path=":memberId/" name="Details" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationMembers/organizationMemberDetail')))} component={SafeLazyLoad}/>
      </Route>

      <Route path="rate-limits/" name="Rate Limits" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationRateLimits')))} component={SafeLazyLoad}/>

      <Route name={(0, locale_1.t)('Relay')} path="relay/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationRelay')))} component={SafeLazyLoad}/>

      <Route path="repos/" name="Repositories" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationRepositories')))} component={SafeLazyLoad}/>

      <Route path="performance/" name={(0, locale_1.t)('Performance')} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationPerformance')))} component={SafeLazyLoad}/>

      <Route path="settings/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationGeneralSettings')))} component={SafeLazyLoad}/>

      <Route name={(0, locale_1.t)('Security & Privacy')} path="security-and-privacy/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationSecurityAndPrivacy')))} component={SafeLazyLoad}/>

      <Route name="Teams" path="teams/">
        <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationTeams')))} component={SafeLazyLoad}/>

        <Route name="Team" path=":teamId/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationTeams/teamDetails')))} component={SafeLazyLoad}>
          <react_router_1.IndexRedirect to="members/"/>
          <Route path="members/" name="Members" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationTeams/teamMembers')))} component={SafeLazyLoad}/>
          <Route path="notifications/" name="Notifications" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationTeams/teamNotifications')))} component={SafeLazyLoad}/>
          <Route path="projects/" name="Projects" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationTeams/teamProjects')))} component={SafeLazyLoad}/>
          <Route path="settings/" name="Settings" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationTeams/teamSettings')))} component={SafeLazyLoad}/>
        </Route>
      </Route>

      <react_router_1.Redirect from="plugins/" to="integrations/"/>
      <Route name="Integrations" path="plugins/">
        <Route name="Integration Details" path=":integrationSlug/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationIntegrations/pluginDetailedView')))} component={SafeLazyLoad}/>
      </Route>

      <react_router_1.Redirect from="sentry-apps/" to="integrations/"/>
      <Route name="Integrations" path="sentry-apps/">
        <Route name="Details" path=":integrationSlug" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationIntegrations/sentryAppDetailedView')))} component={SafeLazyLoad}/>
      </Route>

      <react_router_1.Redirect from="document-integrations/" to="integrations/"/>
      <Route name="Integrations" path="document-integrations/">
        <Route name="Details" path=":integrationSlug" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationIntegrations/docIntegrationDetailedView')))} component={SafeLazyLoad}/>
      </Route>
      <Route name="Integrations" path="integrations/">
        <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationIntegrations/integrationListDirectory')))} component={SafeLazyLoad}/>
        <Route name="Integration Details" path=":integrationSlug" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationIntegrations/integrationDetailedView')))} component={SafeLazyLoad}/>
        <Route name="Configure Integration" path=":providerKey/:integrationId/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationIntegrations/configureIntegration')))} component={SafeLazyLoad}/>
      </Route>

      <Route name="Developer Settings" path="developer-settings/">
        <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationDeveloperSettings')))} component={SafeLazyLoad}/>
        <Route name="New Public Integration" path="new-public/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationDeveloperSettings/sentryApplicationDetails')))} component={SafeLazyLoad}/>
        <Route name="New Internal Integration" path="new-internal/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationDeveloperSettings/sentryApplicationDetails')))} component={SafeLazyLoad}/>
        <Route name="Edit Integration" path=":appSlug/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationDeveloperSettings/sentryApplicationDetails')))} component={SafeLazyLoad}/>
        <Route name="Integration Dashboard" path=":appSlug/dashboard/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organizationDeveloperSettings/sentryApplicationDashboard')))} component={SafeLazyLoad}/>
      </Route>
    </React.Fragment>);
    return (<Route>
      {constants_1.EXPERIMENTAL_SPA && (<Route path="/auth/login/" component={(0, errorHandler_1.default)(layout_1.default)}>
          <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/auth/login')))} component={SafeLazyLoad}/>
        </Route>)}

      <Route path="/" component={(0, errorHandler_1.default)(app_1.default)}>
        <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/app/root')))} component={SafeLazyLoad}/>

        <Route path="/accept/:memberId/:token/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/acceptOrganizationInvite')))} component={SafeLazyLoad}/>
        <Route path="/accept-transfer/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/acceptProjectTransfer')))} component={SafeLazyLoad}/>
        <Route path="/extensions/external-install/:integrationSlug/:installationId" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/integrationOrganizationLink')))} component={SafeLazyLoad}/>

        <Route path="/extensions/:integrationSlug/link/" getComponent={lazyLoad(() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/integrationOrganizationLink'))))}/>

        <Route path="/sentry-apps/:sentryAppSlug/external-install/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/sentryAppExternalInstallation')))} component={SafeLazyLoad}/>
        <react_router_1.Redirect from="/account/" to="/settings/account/details/"/>

        <react_router_1.Redirect from="/share/group/:shareId/" to="/share/issue/:shareId/"/>
        <Route path="/share/issue/:shareId/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/sharedGroupDetails')))} component={SafeLazyLoad}/>

        <Route path="/organizations/new/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationCreate')))} component={SafeLazyLoad}/>

        <Route path="/organizations/:orgId/data-export/:dataExportId" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/dataExport/dataDownload')))} component={SafeLazyLoad}/>

        <Route path="/organizations/:orgId/disabled-member/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/disabledMember')))} component={SafeLazyLoad}/>

        <Route path="/join-request/:orgId/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationJoinRequest')))} component={SafeLazyLoad}/>

        <Route path="/onboarding/:orgId/" component={(0, errorHandler_1.default)(organizationContext_1.default)}>
          <react_router_1.IndexRedirect to="welcome/"/>
          <Route path=":step/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/onboarding/onboarding')))} component={SafeLazyLoad}/>
        </Route>

        {/* Settings routes */}
        <Route component={(0, errorHandler_1.default)(organizationDetails_1.default)}>
          <Route path="/settings/" name="Settings" component={settingsWrapper_1.default}>
            <IndexRoute getComponent={lazyLoad(() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/settingsIndex'))))}/>

            <Route path="account/" name="Account" getComponent={lazyLoad(() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/account/accountSettingsLayout'))))}>
              {accountSettingsRoutes}
            </Route>

            <Route name="Organization" path=":orgId/">
              <Route getComponent={lazyLoad(() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/organization/organizationSettingsLayout'))))}>
                {hook('routes:organization')}
                {orgSettingsRoutes}
              </Route>

              <Route name="Project" path="projects/:projectId/" getComponent={lazyLoad(() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/settings/project/projectSettingsLayout'))))}>
                <Route component={(0, errorHandler_1.default)(settingsProjectProvider_1.default)}>
                  {projectSettingsRoutes}
                </Route>
              </Route>

              <react_router_1.Redirect from=":projectId/" to="projects/:projectId/"/>
              <react_router_1.Redirect from=":projectId/alerts/" to="projects/:projectId/alerts/"/>
              <react_router_1.Redirect from=":projectId/alerts/rules/" to="projects/:projectId/alerts/rules/"/>
              <react_router_1.Redirect from=":projectId/alerts/rules/:ruleId/" to="projects/:projectId/alerts/rules/:ruleId/"/>
            </Route>
          </Route>
        </Route>

        {/* A route tree for lightweight organizational detail views. We place
      this above the heavyweight organization detail views because there
      exist some redirects from deprecated routes which should not take
      precedence over these lightweight routes */}
        <Route component={(0, errorHandler_1.default)(organizationDetails_1.LightWeightOrganizationDetails)}>
          <Route path="/organizations/:orgId/projects/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/projectsDashboard')))} component={SafeLazyLoad}/>
          <Route path="/organizations/:orgId/teamInsights/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/teamInsights')))} component={SafeLazyLoad}>
            <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/teamInsights/overview')))} component={SafeLazyLoad}/>
          </Route>
          <Route path="/organizations/:orgId/dashboards/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/dashboardsV2')))} component={SafeLazyLoad}>
            <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/dashboardsV2/manage')))} component={SafeLazyLoad}/>
          </Route>

          <Route path="/organizations/:orgId/user-feedback/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/userFeedback')))} component={SafeLazyLoad}/>

          <Route path="/organizations/:orgId/issues/" component={(0, errorHandler_1.default)(container_1.default)}>
            <react_router_1.Redirect from="/organizations/:orgId/" to="/organizations/:orgId/issues/"/>
            <IndexRoute component={(0, errorHandler_1.default)(overview_1.default)}/>
            <Route path="searches/:searchId/" component={(0, errorHandler_1.default)(overview_1.default)}/>
            <Route path="sessionPercent" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/issueList/testSessionPercent')))} component={SafeLazyLoad}/>
          </Route>

          {/* Once org issues is complete, these routes can be nested under
        /organizations/:orgId/issues */}
          <Route path="/organizations/:orgId/issues/:groupId/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails')))} component={SafeLazyLoad}>
            <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupEventDetails')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.DETAILS,
            isEventRoute: false,
        }}/>
            <Route path="/organizations/:orgId/issues/:groupId/activity/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupActivity')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.ACTIVITY,
            isEventRoute: false,
        }}/>
            <Route path="/organizations/:orgId/issues/:groupId/events/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupEvents')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.EVENTS,
            isEventRoute: false,
        }}/>
            <Route path="/organizations/:orgId/issues/:groupId/tags/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupTags')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.TAGS,
            isEventRoute: false,
        }}/>
            <Route path="/organizations/:orgId/issues/:groupId/tags/:tagKey/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupTagValues')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.TAGS,
            isEventRoute: false,
        }}/>
            <Route path="/organizations/:orgId/issues/:groupId/feedback/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupUserFeedback')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.USER_FEEDBACK,
            isEventRoute: false,
        }}/>
            <Route path="/organizations/:orgId/issues/:groupId/attachments/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupEventAttachments')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.ATTACHMENTS,
            isEventRoute: false,
        }}/>
            <Route path="/organizations/:orgId/issues/:groupId/similar/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupSimilarIssues')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.SIMILAR_ISSUES,
            isEventRoute: false,
        }}/>
            <Route path="/organizations/:orgId/issues/:groupId/merged/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupMerged')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.MERGED,
            isEventRoute: false,
        }}/>
            <Route path="/organizations/:orgId/issues/:groupId/grouping/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/grouping')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.GROUPING,
            isEventRoute: false,
        }}/>
            <Route path="/organizations/:orgId/issues/:groupId/events/:eventId/">
              <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupEventDetails')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.DETAILS,
            isEventRoute: true,
        }}/>
              <Route path="activity/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupActivity')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.ACTIVITY,
            isEventRoute: true,
        }}/>
              <Route path="events/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupEvents')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.EVENTS,
            isEventRoute: true,
        }}/>
              <Route path="similar/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupSimilarIssues')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.SIMILAR_ISSUES,
            isEventRoute: true,
        }}/>
              <Route path="tags/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupTags')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.TAGS,
            isEventRoute: true,
        }}/>
              <Route path="tags/:tagKey/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupTagValues')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.TAGS,
            isEventRoute: true,
        }}/>
              <Route path="feedback/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupUserFeedback')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.USER_FEEDBACK,
            isEventRoute: true,
        }}/>
              <Route path="attachments/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupEventAttachments')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.ATTACHMENTS,
            isEventRoute: true,
        }}/>
              <Route path="merged/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/groupMerged')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.MERGED,
            isEventRoute: true,
        }}/>
              <Route path="grouping/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationGroupDetails/grouping')))} component={SafeLazyLoad} props={{
            currentTab: types_1.Tab.GROUPING,
            isEventRoute: true,
        }}/>
            </Route>
          </Route>

          <Route path="/organizations/:orgId/alerts/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/alerts')))} component={SafeLazyLoad}>
            <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/alerts/list')))} component={SafeLazyLoad}/>

            <Route path="rules/details/:ruleId/" name="Alert Rule Details" component={SafeLazyLoad} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/alerts/rules/details')))}/>

            <Route path="rules/">
              <IndexRoute component={SafeLazyLoad} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/alerts/rules')))}/>
              <Route path=":projectId/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/alerts/builder/projectProvider')))} component={SafeLazyLoad}>
                <react_router_1.IndexRedirect to="/organizations/:orgId/alerts/rules/"/>
                <Route path=":ruleId/" name="Edit Alert Rule" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/alerts/edit')))} component={SafeLazyLoad}/>
              </Route>
            </Route>

            <Route path="metric-rules/">
              <react_router_1.IndexRedirect to="/organizations/:orgId/alerts/rules/"/>
              <Route path=":projectId/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/alerts/builder/projectProvider')))} component={SafeLazyLoad}>
                <react_router_1.IndexRedirect to="/organizations/:orgId/alerts/rules/"/>
                <Route path=":ruleId/" name="Edit Alert Rule" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/alerts/edit')))} component={SafeLazyLoad}/>
              </Route>
            </Route>

            <Route path="rules/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/alerts/rules')))} component={SafeLazyLoad}/>

            <Route path=":alertId/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/alerts/details')))} component={SafeLazyLoad}/>

            <Route path=":projectId/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/alerts/builder/projectProvider')))} component={SafeLazyLoad}>
              <Route path="new/" name="New Alert Rule" component={SafeLazyLoad} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/alerts/create')))}/>
              <Route path="wizard/" name="Alert Creation Wizard" component={SafeLazyLoad} componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/alerts/wizard')))}/>
            </Route>
          </Route>

          <Route path="/organizations/:orgId/monitors/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/monitors')))} component={SafeLazyLoad}>
            <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/monitors/monitors')))} component={SafeLazyLoad}/>
            <Route path="/organizations/:orgId/monitors/create/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/monitors/create')))} component={SafeLazyLoad}/>
            <Route path="/organizations/:orgId/monitors/:monitorId/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/monitors/details')))} component={SafeLazyLoad}/>
            <Route path="/organizations/:orgId/monitors/:monitorId/edit/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/monitors/edit')))} component={SafeLazyLoad}/>
          </Route>

          <Route path="/organizations/:orgId/releases/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/releases')))} component={SafeLazyLoad}>
            <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/releases/list')))} component={SafeLazyLoad}/>
            <Route path=":release/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/releases/detail')))} component={SafeLazyLoad}>
              <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/releases/detail/overview')))} component={SafeLazyLoad}/>
              <Route path="commits/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/releases/detail/commits')))} component={SafeLazyLoad}/>
              <Route path="files-changed/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/releases/detail/filesChanged')))} component={SafeLazyLoad}/>
              <react_router_1.Redirect from="new-events/" to="/organizations/:orgId/releases/:release/"/>
              <react_router_1.Redirect from="all-events/" to="/organizations/:orgId/releases/:release/"/>
            </Route>
          </Route>

          <Route path="/organizations/:orgId/activity/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationActivity')))} component={SafeLazyLoad}/>

          <Route path="/organizations/:orgId/stats/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/organizationStats')))} component={SafeLazyLoad}/>

          <Route path="/organizations/:orgId/projects/:projectId/events/:eventId/" component={(0, errorHandler_1.default)(projectEventRedirect_1.default)}/>

          {/*
      TODO(mark) Long term this /queries route should go away and /discover should be the
      canonical route for discover2. We have a redirect right now as /discover was for
      discover 1 and most of the application is linking to /discover/queries and not /discover
      */}
          <react_router_1.Redirect from="/organizations/:orgId/discover/" to="/organizations/:orgId/discover/queries/"/>
          <Route path="/organizations/:orgId/discover/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/eventsV2')))} component={SafeLazyLoad}>
            <Route path="queries/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/eventsV2/landing')))} component={SafeLazyLoad}/>
            <Route path="results/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/eventsV2/results')))} component={SafeLazyLoad}/>
            <Route path=":eventSlug/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/eventsV2/eventDetails')))} component={SafeLazyLoad}/>
          </Route>
          <Route path="/organizations/:orgId/performance/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/performance')))} component={SafeLazyLoad}>
            <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/performance/content')))} component={SafeLazyLoad}/>
          </Route>
          <Route path="/organizations/:orgId/performance/trends/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/performance')))} component={SafeLazyLoad}>
            <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/performance/trends')))} component={SafeLazyLoad}/>
          </Route>
          <Route path="/organizations/:orgId/performance/summary/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/performance')))} component={SafeLazyLoad}>
            <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/performance/transactionSummary/transactionOverview')))} component={SafeLazyLoad}/>
            <Route path="/organizations/:orgId/performance/summary/vitals/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/performance/transactionSummary/transactionVitals')))} component={SafeLazyLoad}/>
            <Route path="/organizations/:orgId/performance/summary/tags/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/performance/transactionSummary/transactionTags')))} component={SafeLazyLoad}/>
            <Route path="/organizations/:orgId/performance/summary/events/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/performance/transactionSummary/transactionEvents')))} component={SafeLazyLoad}/>
          </Route>
          <Route path="/organizations/:orgId/performance/vitaldetail/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/performance')))} component={SafeLazyLoad}>
            <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/performance/vitalDetail')))} component={SafeLazyLoad}/>
          </Route>
          <Route path="/organizations/:orgId/performance/trace/:traceSlug/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/performance')))} component={SafeLazyLoad}>
            <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/performance/traceDetails')))} component={SafeLazyLoad}/>
          </Route>
          <Route path="/organizations/:orgId/performance/:eventSlug/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/performance')))} component={SafeLazyLoad}>
            <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/performance/transactionDetails')))} component={SafeLazyLoad}/>
          </Route>
          <Route path="/organizations/:orgId/performance/compare/:baselineEventSlug/:regressionEventSlug/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/performance')))} component={SafeLazyLoad}>
            <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/performance/compare')))} component={SafeLazyLoad}/>
          </Route>
          <Route path="/organizations/:orgId/dashboards/new/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/dashboardsV2/create')))} component={SafeLazyLoad}>
            <Route path="widget/:widgetId/edit/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/dashboardsV2/widget')))} component={SafeLazyLoad}/>
            <Route path="widget/new/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/dashboardsV2/widget')))} component={SafeLazyLoad}/>
          </Route>
          <react_router_1.Redirect from="/organizations/:orgId/dashboards/:dashboardId/" to="/organizations/:orgId/dashboard/:dashboardId/"/>
          <Route path="/organizations/:orgId/dashboard/:dashboardId/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/dashboardsV2/view')))} component={SafeLazyLoad}>
            <Route path="widget/:widgetId/edit/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/dashboardsV2/widget')))} component={SafeLazyLoad}/>
            <Route path="widget/new/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/dashboardsV2/widget')))} component={SafeLazyLoad}/>
          </Route>

          {/* Admin/manage routes */}
          <Route name="Admin" path="/manage/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/admin/adminLayout')))} component={SafeLazyLoad}>
            <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/admin/adminOverview')))} component={SafeLazyLoad}/>
            <Route name="Buffer" path="buffer/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/admin/adminBuffer')))} component={SafeLazyLoad}/>
            <Route name="Relays" path="relays/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/admin/adminRelays')))} component={SafeLazyLoad}/>
            <Route name="Organizations" path="organizations/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/admin/adminOrganizations')))} component={SafeLazyLoad}/>
            <Route name="Projects" path="projects/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/admin/adminProjects')))} component={SafeLazyLoad}/>
            <Route name="Queue" path="queue/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/admin/adminQueue')))} component={SafeLazyLoad}/>
            <Route name="Quotas" path="quotas/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/admin/adminQuotas')))} component={SafeLazyLoad}/>
            <Route name="Settings" path="settings/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/admin/adminSettings')))} component={SafeLazyLoad}/>
            <Route name="Users" path="users/">
              <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/admin/adminUsers')))} component={SafeLazyLoad}/>
              <Route path=":id" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/admin/adminUserEdit')))} component={SafeLazyLoad}/>
            </Route>
            <Route name="Mail" path="status/mail/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/admin/adminMail')))} component={SafeLazyLoad}/>
            <Route name="Environment" path="status/environment/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/admin/adminEnvironment')))} component={SafeLazyLoad}/>
            <Route name="Packages" path="status/packages/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/admin/adminPackages')))} component={SafeLazyLoad}/>
            <Route name="Warnings" path="status/warnings/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/admin/adminWarnings')))} component={SafeLazyLoad}/>
            {hook('routes:admin')}
          </Route>
        </Route>

        {/* The heavyweight organization detail views */}
        <Route path="/:orgId/" component={(0, errorHandler_1.default)(organizationDetails_1.default)}>
          <Route component={(0, errorHandler_1.default)(organizationRoot_1.default)}>
            {hook('routes:organization-root')}

            <Route path="/organizations/:orgId/projects/:projectId/getting-started/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/projectInstall/gettingStarted')))} component={SafeLazyLoad}>
              <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/projectInstall/overview')))} component={SafeLazyLoad}/>
              <Route path=":platform/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/projectInstall/platformOrIntegration')))} component={SafeLazyLoad}/>
            </Route>

            <Route path="/organizations/:orgId/teams/new/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/teamCreate')))} component={SafeLazyLoad}/>

            <Route path="/organizations/:orgId/">
              {hook('routes:organization')}
              <react_router_1.Redirect from="/organizations/:orgId/teams/" to="/settings/:orgId/teams/"/>
              <react_router_1.Redirect from="/organizations/:orgId/teams/your-teams/" to="/settings/:orgId/teams/"/>
              <react_router_1.Redirect from="/organizations/:orgId/teams/all-teams/" to="/settings/:orgId/teams/"/>
              <react_router_1.Redirect from="/organizations/:orgId/teams/:teamId/" to="/settings/:orgId/teams/:teamId/"/>
              <react_router_1.Redirect from="/organizations/:orgId/teams/:teamId/members/" to="/settings/:orgId/teams/:teamId/members/"/>
              <react_router_1.Redirect from="/organizations/:orgId/teams/:teamId/projects/" to="/settings/:orgId/teams/:teamId/projects/"/>
              <react_router_1.Redirect from="/organizations/:orgId/teams/:teamId/settings/" to="/settings/:orgId/teams/:teamId/settings/"/>
              <react_router_1.Redirect from="/organizations/:orgId/settings/" to="/settings/:orgId/"/>
              <react_router_1.Redirect from="/organizations/:orgId/api-keys/" to="/settings/:orgId/api-keys/"/>
              <react_router_1.Redirect from="/organizations/:orgId/api-keys/:apiKey/" to="/settings/:orgId/api-keys/:apiKey/"/>
              <react_router_1.Redirect from="/organizations/:orgId/members/" to="/settings/:orgId/members/"/>
              <react_router_1.Redirect from="/organizations/:orgId/members/:memberId/" to="/settings/:orgId/members/:memberId/"/>
              <react_router_1.Redirect from="/organizations/:orgId/rate-limits/" to="/settings/:orgId/rate-limits/"/>
              <react_router_1.Redirect from="/organizations/:orgId/repos/" to="/settings/:orgId/repos/"/>
            </Route>
            <Route path="/organizations/:orgId/projects/new/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/projectInstall/newProject')))} component={SafeLazyLoad}/>
          </Route>
          <Route path=":projectId/getting-started/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/projectInstall/gettingStarted')))} component={SafeLazyLoad}>
            <IndexRoute componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/projectInstall/overview')))} component={SafeLazyLoad}/>
            <Route path=":platform/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/projectInstall/platformOrIntegration')))} component={SafeLazyLoad}/>
          </Route>
        </Route>

        {/* A route tree for lightweight organizational detail views.
          This is strictly for deprecated URLs that we need to maintain */}
        <Route component={(0, errorHandler_1.default)(organizationDetails_1.LightWeightOrganizationDetails)}>
          {/* This is in the bottom lightweight group because "/organizations/:orgId/projects/new/" in heavyweight needs to be matched first */}
          <Route path="/organizations/:orgId/projects/:projectId/" componentPromise={() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/projectDetail')))} component={SafeLazyLoad}/>

          <Route name="Organization" path="/:orgId/">
            <Route path=":projectId/">
              {/* Support for deprecated URLs (pre-Sentry 10). We just redirect users to new canonical URLs. */}
              <IndexRoute component={(0, errorHandler_1.default)((0, redirectDeprecatedProjectRoute_1.default)(({ orgId, projectId }) => `/organizations/${orgId}/issues/?project=${projectId}`))}/>
              <Route path="issues/" component={(0, errorHandler_1.default)((0, redirectDeprecatedProjectRoute_1.default)(({ orgId, projectId }) => `/organizations/${orgId}/issues/?project=${projectId}`))}/>
              <Route path="dashboard/" component={(0, errorHandler_1.default)((0, redirectDeprecatedProjectRoute_1.default)(({ orgId, projectId }) => `/organizations/${orgId}/dashboards/?project=${projectId}`))}/>
              <Route path="user-feedback/" component={(0, errorHandler_1.default)((0, redirectDeprecatedProjectRoute_1.default)(({ orgId, projectId }) => `/organizations/${orgId}/user-feedback/?project=${projectId}`))}/>
              <Route path="releases/" component={(0, errorHandler_1.default)((0, redirectDeprecatedProjectRoute_1.default)(({ orgId, projectId }) => `/organizations/${orgId}/releases/?project=${projectId}`))}/>
              <Route path="releases/:version/" component={(0, errorHandler_1.default)((0, redirectDeprecatedProjectRoute_1.default)(({ orgId, projectId, router }) => `/organizations/${orgId}/releases/${router.params.version}/?project=${projectId}`))}/>
              <Route path="releases/:version/new-events/" component={(0, errorHandler_1.default)((0, redirectDeprecatedProjectRoute_1.default)(({ orgId, projectId, router }) => `/organizations/${orgId}/releases/${router.params.version}/new-events/?project=${projectId}`))}/>
              <Route path="releases/:version/all-events/" component={(0, errorHandler_1.default)((0, redirectDeprecatedProjectRoute_1.default)(({ orgId, projectId, router }) => `/organizations/${orgId}/releases/${router.params.version}/all-events/?project=${projectId}`))}/>
              <Route path="releases/:version/commits/" component={(0, errorHandler_1.default)((0, redirectDeprecatedProjectRoute_1.default)(({ orgId, projectId, router }) => `/organizations/${orgId}/releases/${router.params.version}/commits/?project=${projectId}`))}/>
            </Route>
          </Route>
        </Route>

        <Route path="/:orgId/">
          <Route path=":projectId/settings/">
            <react_router_1.Redirect from="teams/" to="/settings/:orgId/projects/:projectId/teams/"/>
            <react_router_1.Redirect from="alerts/" to="/settings/:orgId/projects/:projectId/alerts/"/>
            <react_router_1.Redirect from="alerts/rules/" to="/settings/:orgId/projects/:projectId/alerts/rules/"/>
            <react_router_1.Redirect from="alerts/rules/new/" to="/settings/:orgId/projects/:projectId/alerts/rules/new/"/>
            <react_router_1.Redirect from="alerts/rules/:ruleId/" to="/settings/:orgId/projects/:projectId/alerts/rules/:ruleId/"/>
            <react_router_1.Redirect from="environments/" to="/settings/:orgId/projects/:projectId/environments/"/>
            <react_router_1.Redirect from="environments/hidden/" to="/settings/:orgId/projects/:projectId/environments/hidden/"/>
            <react_router_1.Redirect from="tags/" to="/settings/projects/:orgId/projects/:projectId/tags/"/>
            <react_router_1.Redirect from="issue-tracking/" to="/settings/:orgId/projects/:projectId/issue-tracking/"/>
            <react_router_1.Redirect from="release-tracking/" to="/settings/:orgId/projects/:projectId/release-tracking/"/>
            <react_router_1.Redirect from="ownership/" to="/settings/:orgId/projects/:projectId/ownership/"/>
            <react_router_1.Redirect from="data-forwarding/" to="/settings/:orgId/projects/:projectId/data-forwarding/"/>
            <react_router_1.Redirect from="debug-symbols/" to="/settings/:orgId/projects/:projectId/debug-symbols/"/>
            <react_router_1.Redirect from="processing-issues/" to="/settings/:orgId/projects/:projectId/processing-issues/"/>
            <react_router_1.Redirect from="filters/" to="/settings/:orgId/projects/:projectId/filters/"/>
            <react_router_1.Redirect from="hooks/" to="/settings/:orgId/projects/:projectId/hooks/"/>
            <react_router_1.Redirect from="keys/" to="/settings/:orgId/projects/:projectId/keys/"/>
            <react_router_1.Redirect from="keys/:keyId/" to="/settings/:orgId/projects/:projectId/keys/:keyId/"/>
            <react_router_1.Redirect from="user-feedback/" to="/settings/:orgId/projects/:projectId/user-feedback/"/>
            <react_router_1.Redirect from="security-headers/" to="/settings/:orgId/projects/:projectId/security-headers/"/>
            <react_router_1.Redirect from="security-headers/csp/" to="/settings/:orgId/projects/:projectId/security-headers/csp/"/>
            <react_router_1.Redirect from="security-headers/expect-ct/" to="/settings/:orgId/projects/:projectId/security-headers/expect-ct/"/>
            <react_router_1.Redirect from="security-headers/hpkp/" to="/settings/:orgId/projects/:projectId/security-headers/hpkp/"/>
            <react_router_1.Redirect from="plugins/" to="/settings/:orgId/projects/:projectId/plugins/"/>
            <react_router_1.Redirect from="plugins/:pluginId/" to="/settings/:orgId/projects/:projectId/plugins/:pluginId/"/>
            <react_router_1.Redirect from="integrations/:providerKey/" to="/settings/:orgId/projects/:projectId/integrations/:providerKey/"/>
            <react_router_1.Redirect from="install/" to="/settings/:orgId/projects/:projectId/install/"/>
            <react_router_1.Redirect from="install/:platform'" to="/settings/:orgId/projects/:projectId/install/:platform/"/>
          </Route>
          <react_router_1.Redirect from=":projectId/group/:groupId/" to="issues/:groupId/"/>
          <react_router_1.Redirect from=":projectId/issues/:groupId/" to="/organizations/:orgId/issues/:groupId/"/>
          <react_router_1.Redirect from=":projectId/issues/:groupId/events/" to="/organizations/:orgId/issues/:groupId/events/"/>
          <react_router_1.Redirect from=":projectId/issues/:groupId/events/:eventId/" to="/organizations/:orgId/issues/:groupId/events/:eventId/"/>
          <react_router_1.Redirect from=":projectId/issues/:groupId/tags/" to="/organizations/:orgId/issues/:groupId/tags/"/>
          <react_router_1.Redirect from=":projectId/issues/:groupId/tags/:tagKey/" to="/organizations/:orgId/issues/:groupId/tags/:tagKey/"/>
          <react_router_1.Redirect from=":projectId/issues/:groupId/feedback/" to="/organizations/:orgId/issues/:groupId/feedback/"/>
          <react_router_1.Redirect from=":projectId/issues/:groupId/similar/" to="/organizations/:orgId/issues/:groupId/similar/"/>
          <react_router_1.Redirect from=":projectId/issues/:groupId/merged/" to="/organizations/:orgId/issues/:groupId/merged/"/>
          <Route path=":projectId/events/:eventId/" component={(0, errorHandler_1.default)(projectEventRedirect_1.default)}/>
        </Route>

        {hook('routes')}

        <Route path="*" component={(0, errorHandler_1.default)(routeNotFound_1.default)}/>
      </Route>
    </Route>);
}
exports.default = routes;
//# sourceMappingURL=routes.jsx.map