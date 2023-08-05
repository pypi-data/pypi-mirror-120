Object.defineProperty(exports, "__esModule", { value: true });
exports.TeamInsightsOverview = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const Layout = (0, tslib_1.__importStar)(require("app/components/layouts/thirds"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const pageTimeRangeSelector_1 = (0, tslib_1.__importDefault)(require("app/components/pageTimeRangeSelector"));
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const withTeamsForUser_1 = (0, tslib_1.__importDefault)(require("app/utils/withTeamsForUser"));
const headerTabs_1 = (0, tslib_1.__importDefault)(require("./headerTabs"));
const keyTransactions_1 = (0, tslib_1.__importDefault)(require("./keyTransactions"));
const teamDropdown_1 = (0, tslib_1.__importDefault)(require("./teamDropdown"));
const PAGE_QUERY_PARAMS = [
    'pageStatsPeriod',
    'pageStart',
    'pageEnd',
    'pageUtc',
    'dataCategory',
    'transform',
    'sort',
    'query',
    'cursor',
    'team',
];
function TeamInsightsOverview({ organization, teams, loadingTeams, location, router, }) {
    var _a, _b, _c, _d;
    const query = (_a = location === null || location === void 0 ? void 0 : location.query) !== null && _a !== void 0 ? _a : {};
    const currentTeamId = (_b = query.team) !== null && _b !== void 0 ? _b : (_c = teams[0]) === null || _c === void 0 ? void 0 : _c.id;
    const currentTeam = teams.find(team => team.id === currentTeamId);
    const projects = (_d = currentTeam === null || currentTeam === void 0 ? void 0 : currentTeam.projects) !== null && _d !== void 0 ? _d : [];
    function handleChangeTeam(teamId) {
        setStateOnUrl({ team: teamId });
    }
    function handleUpdateDatetime(datetime) {
        const { start, end, relative, utc } = datetime;
        if (start && end) {
            const parser = utc ? moment_1.default.utc : moment_1.default;
            return setStateOnUrl({
                pageStatsPeriod: undefined,
                pageStart: parser(start).format(),
                pageEnd: parser(end).format(),
                pageUtc: utc !== null && utc !== void 0 ? utc : undefined,
            });
        }
        return setStateOnUrl({
            pageStatsPeriod: relative || undefined,
            pageStart: undefined,
            pageEnd: undefined,
            pageUtc: undefined,
        });
    }
    function setStateOnUrl(nextState) {
        const nextQueryParams = (0, pick_1.default)(nextState, PAGE_QUERY_PARAMS);
        const nextLocation = Object.assign(Object.assign({}, location), { query: Object.assign(Object.assign({}, query), nextQueryParams) });
        router.push(nextLocation);
        return nextLocation;
    }
    function dataDatetime() {
        const { start, end, statsPeriod, utc: utcString, } = (0, getParams_1.getParams)(query, {
            allowEmptyPeriod: true,
            allowAbsoluteDatetime: true,
            allowAbsolutePageDatetime: true,
        });
        if (!statsPeriod && !start && !end) {
            return { period: constants_1.DEFAULT_STATS_PERIOD };
        }
        // Following getParams, statsPeriod will take priority over start/end
        if (statsPeriod) {
            return { period: statsPeriod };
        }
        const utc = utcString === 'true';
        if (start && end) {
            return utc
                ? {
                    start: moment_1.default.utc(start).format(),
                    end: moment_1.default.utc(end).format(),
                    utc,
                }
                : {
                    start: (0, moment_1.default)(start).utc().format(),
                    end: (0, moment_1.default)(end).utc().format(),
                    utc,
                };
        }
        return { period: constants_1.DEFAULT_STATS_PERIOD };
    }
    const { period, start, end, utc } = dataDatetime();
    return (<react_1.Fragment>
      <BorderlessHeader>
        <StyledHeaderContent>
          <StyledLayoutTitle>{(0, locale_1.t)('Team Insights')}</StyledLayoutTitle>
        </StyledHeaderContent>
      </BorderlessHeader>
      <Layout.Header>
        <headerTabs_1.default organization={organization} activeTab="teamInsights"/>
      </Layout.Header>

      <Layout.Body>
        {loadingTeams && <loadingIndicator_1.default />}
        {!loadingTeams && (<Layout.Main fullWidth>
            <ControlsWrapper>
              <teamDropdown_1.default teams={teams} selectedTeam={currentTeamId} handleChangeTeam={handleChangeTeam}/>
              <pageTimeRangeSelector_1.default organization={organization} relative={period !== null && period !== void 0 ? period : ''} start={start !== null && start !== void 0 ? start : null} end={end !== null && end !== void 0 ? end : null} utc={utc !== null && utc !== void 0 ? utc : null} onUpdate={handleUpdateDatetime} relativeOptions={(0, omit_1.default)(constants_1.DEFAULT_RELATIVE_PERIODS, ['1h'])}/>
            </ControlsWrapper>

            <SectionTitle>{(0, locale_1.t)('Performance')}</SectionTitle>
            <keyTransactions_1.default organization={organization} projects={projects} period={period} start={start === null || start === void 0 ? void 0 : start.toString()} end={end === null || end === void 0 ? void 0 : end.toString()} location={location}/>
          </Layout.Main>)}
      </Layout.Body>
    </react_1.Fragment>);
}
exports.TeamInsightsOverview = TeamInsightsOverview;
exports.default = (0, withApi_1.default)((0, withOrganization_1.default)((0, withTeamsForUser_1.default)(TeamInsightsOverview)));
const BorderlessHeader = (0, styled_1.default)(Layout.Header) `
  border-bottom: 0;
`;
const StyledHeaderContent = (0, styled_1.default)(Layout.HeaderContent) `
  margin-bottom: 0;
`;
const StyledLayoutTitle = (0, styled_1.default)(Layout.Title) `
  margin-top: ${(0, space_1.default)(0.5)};
`;
const ControlsWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  gap: ${(0, space_1.default)(1)};
  margin-bottom: ${(0, space_1.default)(2)};
`;
const SectionTitle = (0, styled_1.default)(Layout.Title) `
  margin-bottom: ${(0, space_1.default)(1)} !important;
`;
//# sourceMappingURL=overview.jsx.map