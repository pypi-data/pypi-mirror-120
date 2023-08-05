Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const styles_1 = require("app/components/charts/styles");
const count_1 = (0, tslib_1.__importDefault)(require("app/components/count"));
const deployBadge_1 = (0, tslib_1.__importDefault)(require("app/components/deployBadge"));
const globalSelectionLink_1 = (0, tslib_1.__importDefault)(require("app/components/globalSelectionLink"));
const notAvailable_1 = (0, tslib_1.__importDefault)(require("app/components/notAvailable"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const notAvailableMessages_1 = (0, tslib_1.__importDefault)(require("app/constants/notAvailableMessages"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const discoverQuery_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/discoverQuery"));
const fields_1 = require("app/utils/discover/fields");
const data_1 = require("app/views/performance/data");
const sessionTerm_1 = require("app/views/releases/utils/sessionTerm");
const crashFree_1 = (0, tslib_1.__importDefault)(require("../../list/crashFree"));
const releaseAdoption_1 = (0, tslib_1.__importDefault)(require("../../list/releaseAdoption"));
const utils_2 = require("../../list/utils");
const utils_3 = require("../../utils");
const utils_4 = require("../utils");
function ReleaseStats({ organization, release, project, location, selection, isHealthLoading, hasHealthData, getHealthData, }) {
    var _a;
    const { lastDeploy, dateCreated, version } = release;
    const crashCount = getHealthData.getCrashCount(version, project.id, utils_2.DisplayOption.SESSIONS);
    const crashFreeSessions = getHealthData.getCrashFreeRate(version, project.id, utils_2.DisplayOption.SESSIONS);
    const crashFreeUsers = getHealthData.getCrashFreeRate(version, project.id, utils_2.DisplayOption.USERS);
    const get24hSessionCountByRelease = getHealthData.get24hCountByRelease(version, project.id, utils_2.DisplayOption.SESSIONS);
    const get24hSessionCountByProject = getHealthData.get24hCountByProject(project.id, utils_2.DisplayOption.SESSIONS);
    const get24hUserCountByRelease = getHealthData.get24hCountByRelease(version, project.id, utils_2.DisplayOption.USERS);
    const get24hUserCountByProject = getHealthData.get24hCountByProject(project.id, utils_2.DisplayOption.USERS);
    const sessionAdoption = getHealthData.getAdoption(version, project.id, utils_2.DisplayOption.SESSIONS);
    const userAdoption = getHealthData.getAdoption(version, project.id, utils_2.DisplayOption.USERS);
    return (<Container>
      <div>
        <styles_1.SectionHeading>
          {(lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) ? (0, locale_1.t)('Date Deployed') : (0, locale_1.t)('Date Created')}
        </styles_1.SectionHeading>
        <SectionContent>
          <timeSince_1.default date={(_a = lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) !== null && _a !== void 0 ? _a : dateCreated}/>
        </SectionContent>
      </div>

      <div>
        <styles_1.SectionHeading>{(0, locale_1.t)('Last Deploy')}</styles_1.SectionHeading>
        <SectionContent>
          {(lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) ? (<deployBadge_1.default deploy={lastDeploy} orgSlug={organization.slug} version={version} projectId={project.id}/>) : (<notAvailable_1.default />)}
        </SectionContent>
      </div>

      {!organization.features.includes('release-comparison') && (<react_1.Fragment>
          <CrashFreeSection>
            <styles_1.SectionHeading>
              {(0, locale_1.t)('Crash Free Rate')}
              <questionTooltip_1.default position="top" title={(0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE, project.platform)} size="sm"/>
            </styles_1.SectionHeading>
            {isHealthLoading ? (<placeholder_1.default height="58px"/>) : (<SectionContent>
                {(0, utils_1.defined)(crashFreeSessions) || (0, utils_1.defined)(crashFreeUsers) ? (<CrashFreeWrapper>
                    {(0, utils_1.defined)(crashFreeSessions) && (<div>
                        <crashFree_1.default percent={crashFreeSessions} iconSize="md" displayOption={utils_2.DisplayOption.SESSIONS}/>
                      </div>)}

                    {(0, utils_1.defined)(crashFreeUsers) && (<div>
                        <crashFree_1.default percent={crashFreeUsers} iconSize="md" displayOption={utils_2.DisplayOption.USERS}/>
                      </div>)}
                  </CrashFreeWrapper>) : (<notAvailable_1.default tooltip={notAvailableMessages_1.default.releaseHealth}/>)}
              </SectionContent>)}
          </CrashFreeSection>

          <AdoptionSection>
            <styles_1.SectionHeading>
              {(0, locale_1.t)('Adoption')}
              <questionTooltip_1.default position="top" title={(0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ADOPTION, project.platform)} size="sm"/>
            </styles_1.SectionHeading>
            {isHealthLoading ? (<placeholder_1.default height="88px"/>) : (<SectionContent>
                {get24hSessionCountByProject || get24hUserCountByProject ? (<AdoptionWrapper>
                    {(0, utils_1.defined)(get24hSessionCountByProject) &&
                        get24hSessionCountByProject > 0 && (<releaseAdoption_1.default releaseCount={get24hSessionCountByRelease !== null && get24hSessionCountByRelease !== void 0 ? get24hSessionCountByRelease : 0} projectCount={get24hSessionCountByProject !== null && get24hSessionCountByProject !== void 0 ? get24hSessionCountByProject : 0} adoption={sessionAdoption !== null && sessionAdoption !== void 0 ? sessionAdoption : 0} displayOption={utils_2.DisplayOption.SESSIONS} withLabels/>)}

                    {(0, utils_1.defined)(get24hUserCountByProject) &&
                        get24hUserCountByProject > 0 && (<releaseAdoption_1.default releaseCount={get24hUserCountByRelease !== null && get24hUserCountByRelease !== void 0 ? get24hUserCountByRelease : 0} projectCount={get24hUserCountByProject !== null && get24hUserCountByProject !== void 0 ? get24hUserCountByProject : 0} adoption={userAdoption !== null && userAdoption !== void 0 ? userAdoption : 0} displayOption={utils_2.DisplayOption.USERS} withLabels/>)}
                  </AdoptionWrapper>) : (<notAvailable_1.default tooltip={notAvailableMessages_1.default.releaseHealth}/>)}
              </SectionContent>)}
          </AdoptionSection>

          <LinkedStatsSection>
            <div>
              <styles_1.SectionHeading>{(0, locale_1.t)('New Issues')}</styles_1.SectionHeading>
              <SectionContent>
                <tooltip_1.default title={(0, locale_1.t)('Open in Issues')}>
                  <globalSelectionLink_1.default to={(0, utils_3.getReleaseNewIssuesUrl)(organization.slug, project.id, version)}>
                    <count_1.default value={project.newGroups}/>
                  </globalSelectionLink_1.default>
                </tooltip_1.default>
              </SectionContent>
            </div>

            <div>
              <styles_1.SectionHeading>
                {sessionTerm_1.sessionTerm.crashes}
                <questionTooltip_1.default position="top" title={(0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHES, project.platform)} size="sm"/>
              </styles_1.SectionHeading>
              {isHealthLoading ? (<placeholder_1.default height="24px"/>) : (<SectionContent>
                  {hasHealthData ? (<tooltip_1.default title={(0, locale_1.t)('Open in Issues')}>
                      <globalSelectionLink_1.default to={(0, utils_3.getReleaseUnhandledIssuesUrl)(organization.slug, project.id, version)}>
                        <count_1.default value={crashCount !== null && crashCount !== void 0 ? crashCount : 0}/>
                      </globalSelectionLink_1.default>
                    </tooltip_1.default>) : (<notAvailable_1.default tooltip={notAvailableMessages_1.default.releaseHealth}/>)}
                </SectionContent>)}
            </div>

            <div>
              <styles_1.SectionHeading>
                {(0, locale_1.t)('Apdex')}
                <questionTooltip_1.default position="top" title={(0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.APDEX_NEW)} size="sm"/>
              </styles_1.SectionHeading>
              <SectionContent>
                <feature_1.default features={['performance-view']}>
                  {hasFeature => hasFeature ? (<discoverQuery_1.default eventView={(0, utils_4.getReleaseEventView)(selection, release === null || release === void 0 ? void 0 : release.version, organization)} location={location} orgSlug={organization.slug}>
                        {({ isLoading, error, tableData }) => {
                    if (isLoading) {
                        return <placeholder_1.default height="24px"/>;
                    }
                    if (error || !tableData || tableData.data.length === 0) {
                        return <notAvailable_1.default />;
                    }
                    return (<globalSelectionLink_1.default to={{
                            pathname: `/organizations/${organization.slug}/performance/`,
                            query: {
                                query: `release:${release === null || release === void 0 ? void 0 : release.version}`,
                            },
                        }}>
                              <tooltip_1.default title={(0, locale_1.t)('Open in Performance')}>
                                <count_1.default value={tableData.data[0][(0, fields_1.getAggregateAlias)('apdex()')]}/>
                              </tooltip_1.default>
                            </globalSelectionLink_1.default>);
                }}
                      </discoverQuery_1.default>) : (<notAvailable_1.default tooltip={notAvailableMessages_1.default.performance}/>)}
                </feature_1.default>
              </SectionContent>
            </div>
          </LinkedStatsSection>
        </react_1.Fragment>)}
    </Container>);
}
const Container = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 50% 50%;
  grid-row-gap: ${(0, space_1.default)(2)};
  margin-bottom: ${(0, space_1.default)(3)};
`;
const SectionContent = (0, styled_1.default)('div') ``;
const CrashFreeSection = (0, styled_1.default)('div') `
  grid-column: 1/3;
`;
const CrashFreeWrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(1)};
`;
const AdoptionSection = (0, styled_1.default)('div') `
  grid-column: 1/3;
  margin-bottom: ${(0, space_1.default)(1)};
`;
const AdoptionWrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-gap: ${(0, space_1.default)(1.5)};
`;
const LinkedStatsSection = (0, styled_1.default)('div') `
  grid-column: 1/3;
  display: flex;
  justify-content: space-between;
`;
exports.default = ReleaseStats;
//# sourceMappingURL=releaseStats.jsx.map