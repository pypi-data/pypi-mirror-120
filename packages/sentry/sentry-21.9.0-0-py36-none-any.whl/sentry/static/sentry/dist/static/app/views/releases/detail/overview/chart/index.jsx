Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_2 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const eventsChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/eventsChart"));
const styles_1 = require("app/components/charts/styles");
const panels_1 = require("app/components/panels");
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const locale_1 = require("app/locale");
const analytics_1 = require("app/utils/analytics");
const queryString_1 = require("app/utils/queryString");
const data_1 = require("app/views/performance/data");
const releaseStatsRequest_1 = (0, tslib_1.__importDefault)(require("../releaseStatsRequest"));
const healthChartContainer_1 = (0, tslib_1.__importDefault)(require("./healthChartContainer"));
const releaseChartControls_1 = (0, tslib_1.__importStar)(require("./releaseChartControls"));
const utils_1 = require("./utils");
class ReleaseChartContainer extends react_1.Component {
    constructor() {
        super(...arguments);
        /**
         * The top events endpoint used to generate these series is not guaranteed to return a series
         * for both the current release and the other releases. This happens when there is insufficient
         * data. In these cases, the endpoint will return a single zerofilled series for the current
         * release.
         *
         * This is problematic as we want to show both series even if one is empty. To deal with this,
         * we clone the non empty series (to preserve the timestamps) with value 0 (to represent the
         * lack of data).
         */
        this.seriesTransformer = (series) => {
            let current = null;
            let others = null;
            const allSeries = [];
            series.forEach(s => {
                if (s.seriesName === 'current' || s.seriesName === (0, locale_1.t)('This Release')) {
                    current = s;
                }
                else if (s.seriesName === 'others' || s.seriesName === (0, locale_1.t)('Other Releases')) {
                    others = s;
                }
                else {
                    allSeries.push(s);
                }
            });
            if (current !== null && others === null) {
                others = this.cloneSeriesAsZero(current);
            }
            else if (current === null && others !== null) {
                current = this.cloneSeriesAsZero(others);
            }
            if (others !== null) {
                others.seriesName = (0, locale_1.t)('Other Releases');
                allSeries.unshift(others);
            }
            if (current !== null) {
                current.seriesName = (0, locale_1.t)('This Release');
                allSeries.unshift(current);
            }
            return allSeries;
        };
    }
    componentDidMount() {
        const { organization, yAxis, platform } = this.props;
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: `release_detail.display_chart`,
            eventName: `Release Detail: Display Chart`,
            organization_id: parseInt(organization.id, 10),
            display: yAxis,
            platform,
        });
    }
    /**
     * This returns an array with 3 colors, one for each of
     * 1. This Release
     * 2. Other Releases
     * 3. Releases (the markers)
     */
    getTransactionsChartColors() {
        const { yAxis, theme } = this.props;
        switch (yAxis) {
            case releaseChartControls_1.YAxis.FAILED_TRANSACTIONS:
                return [theme.red300, theme.red100, theme.purple300];
            default:
                return [theme.purple300, theme.purple100, theme.purple300];
        }
    }
    getChartTitle() {
        const { yAxis, organization } = this.props;
        switch (yAxis) {
            case releaseChartControls_1.YAxis.SESSIONS:
                return {
                    title: (0, locale_1.t)('Session Count'),
                    help: (0, locale_1.t)('The number of sessions in a given period.'),
                };
            case releaseChartControls_1.YAxis.USERS:
                return {
                    title: (0, locale_1.t)('User Count'),
                    help: (0, locale_1.t)('The number of users in a given period.'),
                };
            case releaseChartControls_1.YAxis.SESSION_DURATION:
                return { title: (0, locale_1.t)('Session Duration') };
            case releaseChartControls_1.YAxis.CRASH_FREE:
                return { title: (0, locale_1.t)('Crash Free Rate') };
            case releaseChartControls_1.YAxis.FAILED_TRANSACTIONS:
                return {
                    title: (0, locale_1.t)('Failure Count'),
                    help: (0, data_1.getTermHelp)(organization, data_1.PERFORMANCE_TERM.FAILURE_RATE),
                };
            case releaseChartControls_1.YAxis.COUNT_DURATION:
                return { title: (0, locale_1.t)('Slow Duration Count') };
            case releaseChartControls_1.YAxis.COUNT_VITAL:
                return { title: (0, locale_1.t)('Slow Vital Count') };
            case releaseChartControls_1.YAxis.EVENTS:
            default:
                return { title: (0, locale_1.t)('Event Count') };
        }
    }
    cloneSeriesAsZero(series) {
        return Object.assign(Object.assign({}, series), { data: series.data.map(point => (Object.assign(Object.assign({}, point), { value: 0 }))) });
    }
    renderStackedChart() {
        const { location, router, organization, api, releaseMeta, yAxis, eventType, vitalType, selection, version, } = this.props;
        const { projects, environments, datetime } = selection;
        const { start, end, period, utc } = datetime;
        const eventView = (0, utils_1.getReleaseEventView)(selection, version, yAxis, eventType, vitalType, organization);
        const apiPayload = eventView.getEventsAPIPayload(location);
        const colors = this.getTransactionsChartColors();
        const { title, help } = this.getChartTitle();
        const releaseQueryExtra = {
            showTransactions: location.query.showTransactions,
            eventType,
            vitalType,
            yAxis,
        };
        return (<eventsChart_1.default router={router} organization={organization} showLegend yAxis={eventView.getYAxis()} query={apiPayload.query} api={api} projects={projects} environments={environments} start={start} end={end} period={period} utc={utc} disablePrevious emphasizeReleases={[releaseMeta.version]} field={eventView.getFields()} topEvents={2} orderby={(0, queryString_1.decodeScalar)(apiPayload.sort)} currentSeriesName={(0, locale_1.t)('This Release')} 
        // This seems a little strange but is intentional as EventsChart
        // uses the previousSeriesName as the secondary series name
        previousSeriesName={(0, locale_1.t)('Other Releases')} seriesTransformer={this.seriesTransformer} disableableSeries={[(0, locale_1.t)('This Release'), (0, locale_1.t)('Other Releases')]} colors={colors} preserveReleaseQueryParams releaseQueryExtra={releaseQueryExtra} chartHeader={<styles_1.HeaderTitleLegend>
            {title}
            {help && <questionTooltip_1.default size="sm" position="top" title={help}/>}
          </styles_1.HeaderTitleLegend>} legendOptions={{ right: 10, top: 0 }} chartOptions={{ grid: { left: '10px', right: '10px', top: '40px', bottom: '0px' } }}/>);
    }
    renderHealthChart(loading, reloading, errored, chartData) {
        const { selection, yAxis, router, platform } = this.props;
        const { title, help } = this.getChartTitle();
        return (<healthChartContainer_1.default platform={platform} loading={loading} errored={errored} reloading={reloading} chartData={chartData} selection={selection} yAxis={yAxis} router={router} title={title} help={help}/>);
    }
    render() {
        const { yAxis, eventType, vitalType, hasDiscover, hasHealthData, hasPerformance, onYAxisChange, onEventTypeChange, onVitalTypeChange, organization, defaultStatsPeriod, api, version, selection, location, projectSlug, } = this.props;
        return (<releaseStatsRequest_1.default api={api} organization={organization} projectSlug={projectSlug} version={version} selection={selection} location={location} yAxis={yAxis} eventType={eventType} vitalType={vitalType} hasHealthData={hasHealthData} hasDiscover={hasDiscover} hasPerformance={hasPerformance} defaultStatsPeriod={defaultStatsPeriod}>
        {({ loading, reloading, errored, chartData, chartSummary }) => (<panels_1.Panel>
            <styles_1.ChartContainer>
              {((hasDiscover || hasPerformance) && yAxis === releaseChartControls_1.YAxis.EVENTS) ||
                    (hasPerformance && releaseChartControls_1.PERFORMANCE_AXIS.includes(yAxis))
                    ? this.renderStackedChart()
                    : this.renderHealthChart(loading, reloading, errored, chartData)}
            </styles_1.ChartContainer>
            <AnchorWrapper>
              <guideAnchor_1.default target="release_chart" position="bottom" offset="-80px">
                <react_1.Fragment />
              </guideAnchor_1.default>
            </AnchorWrapper>
            <releaseChartControls_1.default summary={chartSummary} yAxis={yAxis} onYAxisChange={onYAxisChange} eventType={eventType} onEventTypeChange={onEventTypeChange} vitalType={vitalType} onVitalTypeChange={onVitalTypeChange} organization={organization} hasDiscover={hasDiscover} hasHealthData={hasHealthData} hasPerformance={hasPerformance}/>
          </panels_1.Panel>)}
      </releaseStatsRequest_1.default>);
    }
}
exports.default = (0, react_2.withTheme)(ReleaseChartContainer);
const AnchorWrapper = (0, styled_1.default)('div') `
  height: 0;
  width: 0;
  margin-left: 50%;
`;
//# sourceMappingURL=index.jsx.map