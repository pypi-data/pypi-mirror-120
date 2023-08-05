Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const react_1 = require("@emotion/react");
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const areaChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/areaChart"));
const lineChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/lineChart"));
const stackedAreaChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/stackedAreaChart"));
const styles_1 = require("app/components/charts/styles");
const utils_1 = require("app/components/charts/utils");
const utils_2 = require("app/components/organizations/timeRangeSelector/utils");
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const utils_3 = require("app/utils");
const dates_1 = require("app/utils/dates");
const charts_1 = require("app/utils/discover/charts");
const formatters_1 = require("app/utils/formatters");
const queryString_1 = require("app/utils/queryString");
const utils_4 = require("app/views/releases/utils");
const sessionTerm_1 = require("../../../utils/sessionTerm");
const releaseChartControls_1 = require("./releaseChartControls");
const utils_5 = require("./utils");
class HealthChart extends React.Component {
    constructor() {
        super(...arguments);
        this.handleLegendSelectChanged = legendChange => {
            const { location } = this.props;
            const { selected } = legendChange;
            const to = Object.assign(Object.assign({}, location), { query: Object.assign(Object.assign({}, location.query), { unselectedSeries: Object.keys(selected).filter(key => !selected[key]) }) });
            react_router_1.browserHistory.replace(to);
        };
        this.formatTooltipValue = (value) => {
            const { yAxis } = this.props;
            switch (yAxis) {
                case releaseChartControls_1.YAxis.SESSION_DURATION:
                    return typeof value === 'number' ? (0, formatters_1.getExactDuration)(value, true) : '\u2015';
                case releaseChartControls_1.YAxis.CRASH_FREE:
                    return (0, utils_3.defined)(value) ? `${value}%` : '\u2015';
                case releaseChartControls_1.YAxis.SESSIONS:
                case releaseChartControls_1.YAxis.USERS:
                default:
                    return typeof value === 'number' ? value.toLocaleString() : value !== null && value !== void 0 ? value : '';
            }
        };
    }
    componentDidMount() {
        if (this.shouldUnselectHealthySeries()) {
            this.props.onVisibleSeriesRecalculated();
            this.handleLegendSelectChanged({ selected: { Healthy: false } });
        }
    }
    shouldComponentUpdate(nextProps) {
        if (this.props.title !== nextProps.title) {
            return true;
        }
        if (nextProps.reloading || !nextProps.timeseriesData) {
            return false;
        }
        if (this.props.location.query.unselectedSeries !==
            nextProps.location.query.unselectedSeries) {
            return true;
        }
        if ((0, isEqual_1.default)(this.props.timeseriesData, nextProps.timeseriesData)) {
            return false;
        }
        return true;
    }
    shouldUnselectHealthySeries() {
        const { timeseriesData, location, shouldRecalculateVisibleSeries } = this.props;
        const otherAreasThanHealthyArePositive = timeseriesData
            .filter(s => ![
            sessionTerm_1.sessionTerm.healthy,
            sessionTerm_1.sessionTerm.otherHealthy,
            sessionTerm_1.sessionTerm.otherErrored,
            sessionTerm_1.sessionTerm.otherCrashed,
            sessionTerm_1.sessionTerm.otherAbnormal,
        ].includes(s.seriesName))
            .some(s => s.data.some(d => d.value > 0));
        const alreadySomethingUnselected = !!(0, queryString_1.decodeScalar)(location.query.unselectedSeries);
        return (shouldRecalculateVisibleSeries &&
            otherAreasThanHealthyArePositive &&
            !alreadySomethingUnselected);
    }
    configureYAxis() {
        const { theme, yAxis } = this.props;
        switch (yAxis) {
            case releaseChartControls_1.YAxis.CRASH_FREE:
                return {
                    max: 100,
                    scale: true,
                    axisLabel: {
                        formatter: (value) => (0, utils_4.displayCrashFreePercent)(value),
                        color: theme.chartLabel,
                    },
                };
            case releaseChartControls_1.YAxis.SESSION_DURATION:
                return {
                    scale: true,
                    axisLabel: {
                        formatter: value => (0, charts_1.axisDuration)(value * 1000),
                        color: theme.chartLabel,
                    },
                };
            case releaseChartControls_1.YAxis.SESSIONS:
            case releaseChartControls_1.YAxis.USERS:
            default:
                return undefined;
        }
    }
    configureXAxis() {
        const { timeseriesData, zoomRenderProps } = this.props;
        if (timeseriesData.every(s => s.data.length === 1)) {
            if (zoomRenderProps.period) {
                const { start, end } = (0, utils_2.parseStatsPeriod)(zoomRenderProps.period, null);
                return { min: start, max: end };
            }
            return {
                min: (0, dates_1.getUtcDateString)(zoomRenderProps.start),
                max: (0, dates_1.getUtcDateString)(zoomRenderProps.end),
            };
        }
        return undefined;
    }
    getChart() {
        const { yAxis } = this.props;
        switch (yAxis) {
            case releaseChartControls_1.YAxis.SESSION_DURATION:
                return areaChart_1.default;
            case releaseChartControls_1.YAxis.SESSIONS:
            case releaseChartControls_1.YAxis.USERS:
                return stackedAreaChart_1.default;
            case releaseChartControls_1.YAxis.CRASH_FREE:
            default:
                return lineChart_1.default;
        }
    }
    getLegendTooltipDescription(serieName) {
        const { platform } = this.props;
        switch (serieName) {
            case sessionTerm_1.sessionTerm.crashed:
                return (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASHED, platform);
            case sessionTerm_1.sessionTerm.abnormal:
                return (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ABNORMAL, platform);
            case sessionTerm_1.sessionTerm.errored:
                return (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.ERRORED, platform);
            case sessionTerm_1.sessionTerm.healthy:
                return (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.HEALTHY, platform);
            case sessionTerm_1.sessionTerm['crash-free-users']:
                return (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_USERS, platform);
            case sessionTerm_1.sessionTerm['crash-free-sessions']:
                return (0, sessionTerm_1.getSessionTermDescription)(sessionTerm_1.SessionTerm.CRASH_FREE_SESSIONS, platform);
            default:
                return '';
        }
    }
    getLegendSeries() {
        const { timeseriesData } = this.props;
        return (timeseriesData
            .filter(d => !(0, utils_5.isOtherSeries)(d))
            // we don't want Other Healthy, Other Crashed, etc. to show up in the legend
            .sort(utils_5.sortSessionSeries)
            .map(d => d.seriesName));
    }
    getLegendSelectedSeries() {
        var _a;
        const { location, yAxis } = this.props;
        const selection = (_a = (0, utils_1.getSeriesSelection)(location)) !== null && _a !== void 0 ? _a : {};
        // otherReleases toggles all "other" series (other healthy, other crashed, etc.) at once
        const otherReleasesVisible = !(selection[sessionTerm_1.sessionTerm.otherReleases] === false);
        if (yAxis === releaseChartControls_1.YAxis.SESSIONS || yAxis === releaseChartControls_1.YAxis.USERS) {
            selection[sessionTerm_1.sessionTerm.otherErrored] =
                !(selection === null || selection === void 0 ? void 0 : selection.hasOwnProperty(sessionTerm_1.sessionTerm.errored)) && otherReleasesVisible;
            selection[sessionTerm_1.sessionTerm.otherCrashed] =
                !(selection === null || selection === void 0 ? void 0 : selection.hasOwnProperty(sessionTerm_1.sessionTerm.crashed)) && otherReleasesVisible;
            selection[sessionTerm_1.sessionTerm.otherAbnormal] =
                !(selection === null || selection === void 0 ? void 0 : selection.hasOwnProperty(sessionTerm_1.sessionTerm.abnormal)) && otherReleasesVisible;
            selection[sessionTerm_1.sessionTerm.otherHealthy] =
                !(selection === null || selection === void 0 ? void 0 : selection.hasOwnProperty(sessionTerm_1.sessionTerm.healthy)) && otherReleasesVisible;
        }
        if (yAxis === releaseChartControls_1.YAxis.CRASH_FREE) {
            selection[sessionTerm_1.sessionTerm.otherCrashFreeSessions] =
                !(selection === null || selection === void 0 ? void 0 : selection.hasOwnProperty(sessionTerm_1.sessionTerm['crash-free-sessions'])) &&
                    otherReleasesVisible;
            selection[sessionTerm_1.sessionTerm.otherCrashFreeUsers] =
                !(selection === null || selection === void 0 ? void 0 : selection.hasOwnProperty(sessionTerm_1.sessionTerm['crash-free-users'])) &&
                    otherReleasesVisible;
        }
        return selection;
    }
    render() {
        const { timeseriesData, zoomRenderProps, title, help } = this.props;
        const Chart = this.getChart();
        const legend = {
            right: 10,
            top: 0,
            data: this.getLegendSeries(),
            selected: this.getLegendSelectedSeries(),
            tooltip: {
                show: true,
                // TODO(ts) tooltip.formatter has incorrect types in echarts 4
                formatter: (params) => {
                    var _a;
                    const seriesNameDesc = this.getLegendTooltipDescription((_a = params.name) !== null && _a !== void 0 ? _a : '');
                    if (!seriesNameDesc) {
                        return '';
                    }
                    return ['<div class="tooltip-description">', seriesNameDesc, '</div>'].join('');
                },
            },
        };
        return (<React.Fragment>
        <styles_1.HeaderTitleLegend>
          {title}
          {help && <questionTooltip_1.default size="sm" position="top" title={help}/>}
        </styles_1.HeaderTitleLegend>

        <Chart legend={legend} {...zoomRenderProps} series={timeseriesData} isGroupedByDate seriesOptions={{
                showSymbol: false,
            }} grid={{
                left: '10px',
                right: '10px',
                top: '40px',
                bottom: '0px',
            }} yAxis={this.configureYAxis()} xAxis={this.configureXAxis()} tooltip={{ valueFormatter: this.formatTooltipValue }} onLegendSelectChanged={this.handleLegendSelectChanged} transformSinglePointToBar/>
      </React.Fragment>);
    }
}
exports.default = (0, react_1.withTheme)(HealthChart);
//# sourceMappingURL=healthChart.jsx.map