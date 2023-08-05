Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const eventsChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/eventsChart"));
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const panels_1 = require("app/components/panels");
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const dates_1 = require("app/utils/dates");
const types_1 = require("app/utils/discover/types");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const queryString_1 = require("app/utils/queryString");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const chartFooter_1 = (0, tslib_1.__importDefault)(require("./chartFooter"));
class ResultsChart extends react_1.Component {
    shouldComponentUpdate(nextProps) {
        const _a = this.props, { eventView } = _a, restProps = (0, tslib_1.__rest)(_a, ["eventView"]);
        const { eventView: nextEventView } = nextProps, restNextProps = (0, tslib_1.__rest)(nextProps, ["eventView"]);
        if (!eventView.isEqualTo(nextEventView)) {
            return true;
        }
        return !(0, isEqual_1.default)(restProps, restNextProps);
    }
    render() {
        const { api, eventView, location, organization, router, confirmedQuery } = this.props;
        const hasPerformanceChartInterpolation = organization.features.includes('performance-chart-interpolation');
        const yAxisValue = eventView.getYAxis();
        const globalSelection = eventView.getGlobalSelection();
        const start = globalSelection.datetime.start
            ? (0, dates_1.getUtcToLocalDateObject)(globalSelection.datetime.start)
            : null;
        const end = globalSelection.datetime.end
            ? (0, dates_1.getUtcToLocalDateObject)(globalSelection.datetime.end)
            : null;
        const { utc } = (0, getParams_1.getParams)(location.query);
        const apiPayload = eventView.getEventsAPIPayload(location);
        const display = eventView.getDisplayMode();
        const isTopEvents = display === types_1.DisplayModes.TOP5 || display === types_1.DisplayModes.DAILYTOP5;
        const isPeriod = display === types_1.DisplayModes.DEFAULT || display === types_1.DisplayModes.TOP5;
        const isDaily = display === types_1.DisplayModes.DAILYTOP5 || display === types_1.DisplayModes.DAILY;
        const isPrevious = display === types_1.DisplayModes.PREVIOUS;
        return (<react_1.Fragment>
        {(0, getDynamicText_1.default)({
                value: (<eventsChart_1.default api={api} router={router} query={apiPayload.query} organization={organization} showLegend yAxis={yAxisValue} projects={globalSelection.projects} environments={globalSelection.environments} start={start} end={end} period={globalSelection.datetime.period} disablePrevious={!isPrevious} disableReleases={!isPeriod} field={isTopEvents ? apiPayload.field : undefined} interval={eventView.interval} showDaily={isDaily} topEvents={isTopEvents ? types_1.TOP_N : undefined} orderby={isTopEvents ? (0, queryString_1.decodeScalar)(apiPayload.sort) : undefined} utc={utc === 'true'} confirmedQuery={confirmedQuery} withoutZerofill={hasPerformanceChartInterpolation}/>),
                fixed: <placeholder_1.default height="200px" testId="skeleton-ui"/>,
            })}
      </react_1.Fragment>);
    }
}
class ResultsChartContainer extends react_1.Component {
    shouldComponentUpdate(nextProps) {
        const _a = this.props, { eventView } = _a, restProps = (0, tslib_1.__rest)(_a, ["eventView"]);
        const { eventView: nextEventView } = nextProps, restNextProps = (0, tslib_1.__rest)(nextProps, ["eventView"]);
        if (!eventView.isEqualTo(nextEventView) ||
            this.props.confirmedQuery !== nextProps.confirmedQuery) {
            return true;
        }
        return !(0, isEqual_1.default)(restProps, restNextProps);
    }
    render() {
        const { api, eventView, location, router, total, onAxisChange, onDisplayChange, organization, confirmedQuery, } = this.props;
        const yAxisValue = eventView.getYAxis();
        const hasQueryFeature = organization.features.includes('discover-query');
        const displayOptions = eventView.getDisplayOptions().filter(opt => {
            // top5 modes are only available with larger packages in saas.
            // We remove instead of disable here as showing tooltips in dropdown
            // menus is clunky.
            if ([types_1.DisplayModes.TOP5, types_1.DisplayModes.DAILYTOP5].includes(opt.value) &&
                !hasQueryFeature) {
                return false;
            }
            return true;
        });
        return (<StyledPanel>
        <ResultsChart api={api} eventView={eventView} location={location} organization={organization} router={router} confirmedQuery={confirmedQuery}/>
        <chartFooter_1.default total={total} yAxisValue={yAxisValue} yAxisOptions={eventView.getYAxisOptions()} onAxisChange={onAxisChange} displayOptions={displayOptions} displayMode={eventView.getDisplayMode()} onDisplayChange={onDisplayChange}/>
      </StyledPanel>);
    }
}
exports.default = (0, withApi_1.default)(ResultsChartContainer);
const StyledPanel = (0, styled_1.default)(panels_1.Panel) `
  @media (min-width: ${p => p.theme.breakpoints[1]}) {
    margin: 0;
  }
`;
//# sourceMappingURL=resultsChart.jsx.map