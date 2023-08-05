Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const chunk_1 = (0, tslib_1.__importDefault)(require("lodash/chunk"));
const maxBy_1 = (0, tslib_1.__importDefault)(require("lodash/maxBy"));
const events_1 = require("app/actionCreators/events");
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const eventsRequest_1 = (0, tslib_1.__importDefault)(require("app/components/charts/eventsRequest"));
const optionSelector_1 = (0, tslib_1.__importDefault)(require("app/components/charts/optionSelector"));
const styles_1 = require("app/components/charts/styles");
const loadingMask_1 = (0, tslib_1.__importDefault)(require("app/components/loadingMask"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const types_1 = require("../../types");
const thresholdsChart_1 = (0, tslib_1.__importDefault)(require("./thresholdsChart"));
const TIME_PERIOD_MAP = {
    [types_1.TimePeriod.SIX_HOURS]: (0, locale_1.t)('Last 6 hours'),
    [types_1.TimePeriod.ONE_DAY]: (0, locale_1.t)('Last 24 hours'),
    [types_1.TimePeriod.THREE_DAYS]: (0, locale_1.t)('Last 3 days'),
    [types_1.TimePeriod.SEVEN_DAYS]: (0, locale_1.t)('Last 7 days'),
    [types_1.TimePeriod.FOURTEEN_DAYS]: (0, locale_1.t)('Last 14 days'),
    [types_1.TimePeriod.THIRTY_DAYS]: (0, locale_1.t)('Last 30 days'),
};
/**
 * If TimeWindow is small we want to limit the stats period
 * If the time window is one day we want to use a larger stats period
 */
const AVAILABLE_TIME_PERIODS = {
    [types_1.TimeWindow.ONE_MINUTE]: [
        types_1.TimePeriod.SIX_HOURS,
        types_1.TimePeriod.ONE_DAY,
        types_1.TimePeriod.THREE_DAYS,
        types_1.TimePeriod.SEVEN_DAYS,
    ],
    [types_1.TimeWindow.FIVE_MINUTES]: [
        types_1.TimePeriod.ONE_DAY,
        types_1.TimePeriod.THREE_DAYS,
        types_1.TimePeriod.SEVEN_DAYS,
        types_1.TimePeriod.FOURTEEN_DAYS,
        types_1.TimePeriod.THIRTY_DAYS,
    ],
    [types_1.TimeWindow.TEN_MINUTES]: [
        types_1.TimePeriod.ONE_DAY,
        types_1.TimePeriod.THREE_DAYS,
        types_1.TimePeriod.SEVEN_DAYS,
        types_1.TimePeriod.FOURTEEN_DAYS,
        types_1.TimePeriod.THIRTY_DAYS,
    ],
    [types_1.TimeWindow.FIFTEEN_MINUTES]: [
        types_1.TimePeriod.THREE_DAYS,
        types_1.TimePeriod.SEVEN_DAYS,
        types_1.TimePeriod.FOURTEEN_DAYS,
        types_1.TimePeriod.THIRTY_DAYS,
    ],
    [types_1.TimeWindow.THIRTY_MINUTES]: [
        types_1.TimePeriod.SEVEN_DAYS,
        types_1.TimePeriod.FOURTEEN_DAYS,
        types_1.TimePeriod.THIRTY_DAYS,
    ],
    [types_1.TimeWindow.ONE_HOUR]: [types_1.TimePeriod.FOURTEEN_DAYS, types_1.TimePeriod.THIRTY_DAYS],
    [types_1.TimeWindow.TWO_HOURS]: [types_1.TimePeriod.THIRTY_DAYS],
    [types_1.TimeWindow.FOUR_HOURS]: [types_1.TimePeriod.THIRTY_DAYS],
    [types_1.TimeWindow.ONE_DAY]: [types_1.TimePeriod.THIRTY_DAYS],
};
const AGGREGATE_FUNCTIONS = {
    avg: (seriesChunk) => AGGREGATE_FUNCTIONS.sum(seriesChunk) / seriesChunk.length,
    sum: (seriesChunk) => seriesChunk.reduce((acc, series) => acc + series.value, 0),
    max: (seriesChunk) => Math.max(...seriesChunk.map(series => series.value)),
    min: (seriesChunk) => Math.min(...seriesChunk.map(series => series.value)),
};
/**
 * Determines the number of datapoints to roll up
 */
const getBucketSize = (timeWindow, dataPoints) => {
    const MAX_DPS = 720;
    for (const bucketSize of [5, 10, 15, 30, 60, 120, 240]) {
        const chunkSize = bucketSize / timeWindow;
        if (dataPoints / chunkSize <= MAX_DPS) {
            return bucketSize / timeWindow;
        }
    }
    return 2;
};
/**
 * This is a chart to be used in Metric Alert rules that fetches events based on
 * query, timewindow, and aggregations.
 */
class TriggersChart extends React.PureComponent {
    constructor() {
        super(...arguments);
        this.state = {
            statsPeriod: types_1.TimePeriod.ONE_DAY,
            totalEvents: null,
        };
        this.handleStatsPeriodChange = (timePeriod) => {
            this.setState({ statsPeriod: timePeriod });
        };
        this.getStatsPeriod = () => {
            const { statsPeriod } = this.state;
            const { timeWindow } = this.props;
            const statsPeriodOptions = AVAILABLE_TIME_PERIODS[timeWindow];
            const period = statsPeriodOptions.includes(statsPeriod)
                ? statsPeriod
                : statsPeriodOptions[0];
            return period;
        };
    }
    componentDidMount() {
        this.fetchTotalCount();
    }
    componentDidUpdate(prevProps, prevState) {
        const { query, environment, timeWindow } = this.props;
        const { statsPeriod } = this.state;
        if (prevProps.environment !== environment ||
            prevProps.query !== query ||
            prevProps.timeWindow !== timeWindow ||
            prevState.statsPeriod !== statsPeriod) {
            this.fetchTotalCount();
        }
    }
    fetchTotalCount() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, organization, environment, projects, query } = this.props;
            const statsPeriod = this.getStatsPeriod();
            try {
                const totalEvents = yield (0, events_1.fetchTotalCount)(api, organization.slug, {
                    field: [],
                    project: projects.map(({ id }) => id),
                    query,
                    statsPeriod,
                    environment: environment ? [environment] : [],
                });
                this.setState({ totalEvents });
            }
            catch (e) {
                this.setState({ totalEvents: null });
            }
        });
    }
    render() {
        const { api, organization, projects, timeWindow, query, aggregate, triggers, resolveThreshold, thresholdType, environment, header, } = this.props;
        const { statsPeriod, totalEvents } = this.state;
        const statsPeriodOptions = AVAILABLE_TIME_PERIODS[timeWindow];
        const period = this.getStatsPeriod();
        return (<feature_1.default features={['metric-alert-builder-aggregate']} organization={organization}>
        {({ hasFeature }) => {
                return (<eventsRequest_1.default api={api} organization={organization} query={query} environment={environment ? [environment] : undefined} project={projects.map(({ id }) => Number(id))} interval={`${timeWindow}m`} period={period} yAxis={aggregate} includePrevious={false} currentSeriesName={aggregate} partial={false}>
              {({ loading, reloading, timeseriesData }) => {
                        var _a;
                        let maxValue;
                        let timeseriesLength;
                        if (((_a = timeseriesData === null || timeseriesData === void 0 ? void 0 : timeseriesData[0]) === null || _a === void 0 ? void 0 : _a.data) !== undefined) {
                            maxValue = (0, maxBy_1.default)(timeseriesData[0].data, ({ value }) => value);
                            timeseriesLength = timeseriesData[0].data.length;
                            if (hasFeature && timeseriesLength > 600) {
                                const avgData = [];
                                const minData = [];
                                const maxData = [];
                                const chunkSize = getBucketSize(timeWindow, timeseriesData[0].data.length);
                                (0, chunk_1.default)(timeseriesData[0].data, chunkSize).forEach(seriesChunk => {
                                    avgData.push({
                                        name: seriesChunk[0].name,
                                        value: AGGREGATE_FUNCTIONS.avg(seriesChunk),
                                    });
                                    minData.push({
                                        name: seriesChunk[0].name,
                                        value: AGGREGATE_FUNCTIONS.min(seriesChunk),
                                    });
                                    maxData.push({
                                        name: seriesChunk[0].name,
                                        value: AGGREGATE_FUNCTIONS.max(seriesChunk),
                                    });
                                });
                                timeseriesData = [
                                    timeseriesData[0],
                                    { seriesName: (0, locale_1.t)('Minimum'), data: minData },
                                    { seriesName: (0, locale_1.t)('Average'), data: avgData },
                                    { seriesName: (0, locale_1.t)('Maximum'), data: maxData },
                                ];
                            }
                        }
                        const chart = (<React.Fragment>
                    {header}
                    <TransparentLoadingMask visible={reloading}/>
                    {loading || reloading ? (<ChartPlaceholder />) : (<thresholdsChart_1.default period={statsPeriod} maxValue={maxValue ? maxValue.value : maxValue} data={timeseriesData} triggers={triggers} resolveThreshold={resolveThreshold} thresholdType={thresholdType}/>)}
                    <styles_1.ChartControls>
                      <styles_1.InlineContainer>
                        <React.Fragment>
                          <styles_1.SectionHeading>{(0, locale_1.t)('Total Events')}</styles_1.SectionHeading>
                          {totalEvents !== null ? (<styles_1.SectionValue>{totalEvents.toLocaleString()}</styles_1.SectionValue>) : (<styles_1.SectionValue>&mdash;</styles_1.SectionValue>)}
                        </React.Fragment>
                      </styles_1.InlineContainer>
                      <styles_1.InlineContainer>
                        <optionSelector_1.default options={statsPeriodOptions.map(timePeriod => ({
                                label: TIME_PERIOD_MAP[timePeriod],
                                value: timePeriod,
                                disabled: loading || reloading,
                            }))} selected={period} onChange={this.handleStatsPeriodChange} title={(0, locale_1.t)('Display')}/>
                      </styles_1.InlineContainer>
                    </styles_1.ChartControls>
                  </React.Fragment>);
                        return chart;
                    }}
            </eventsRequest_1.default>);
            }}
      </feature_1.default>);
    }
}
exports.default = (0, withApi_1.default)(TriggersChart);
const TransparentLoadingMask = (0, styled_1.default)(loadingMask_1.default) `
  ${p => !p.visible && 'display: none;'};
  opacity: 0.4;
  z-index: 1;
`;
const ChartPlaceholder = (0, styled_1.default)(placeholder_1.default) `
  /* Height and margin should add up to graph size (200px) */
  margin: 0 0 ${(0, space_1.default)(2)};
  height: 184px;
`;
//# sourceMappingURL=index.jsx.map