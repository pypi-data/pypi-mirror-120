Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const markLine_1 = (0, tslib_1.__importDefault)(require("app/components/charts/components/markLine"));
const markPoint_1 = (0, tslib_1.__importDefault)(require("app/components/charts/components/markPoint"));
const lineChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/lineChart"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const closedSymbol_1 = (0, tslib_1.__importDefault)(require("./closedSymbol"));
const startedSymbol_1 = (0, tslib_1.__importDefault)(require("./startedSymbol"));
function truthy(value) {
    return !!value;
}
/**
 * So we'll have to see how this looks with real data, but echarts requires
 * an explicit (x,y) value to draw a symbol (incident started/closed bubble).
 *
 * This uses the closest date *without* going over.
 *
 * AFAICT we can't give it an x-axis value and have it draw on the line,
 * so we probably need to calculate the y-axis value ourselves if we want it placed
 * at the exact time.
 *
 * @param data Data array
 * @param needle the target timestamp
 */
function getNearbyIndex(data, needle) {
    // `data` is sorted, return the first index whose value (timestamp) is > `needle`
    const index = data.findIndex(([ts]) => ts > needle);
    // this shouldn't happen, as we try to buffer dates before start/end dates
    if (index === 0) {
        return 0;
    }
    return index !== -1 ? index - 1 : data.length - 1;
}
const Chart = (props) => {
    const { aggregate, data, started, closed, triggers, resolveThreshold } = props;
    const startedTs = started && moment_1.default.utc(started).unix();
    const closedTs = closed && moment_1.default.utc(closed).unix();
    const chartData = data.map(([ts, val]) => [
        ts * 1000,
        val.length ? val.reduce((acc, { count } = { count: 0 }) => acc + count, 0) : 0,
    ]);
    const startedCoordinate = startedTs
        ? chartData[getNearbyIndex(data, startedTs)]
        : undefined;
    const showClosedMarker = data && closedTs && data[data.length - 1] && data[data.length - 1][0] >= closedTs
        ? true
        : false;
    const closedCoordinate = closedTs && showClosedMarker ? chartData[getNearbyIndex(data, closedTs)] : undefined;
    const seriesName = aggregate;
    const warningTrigger = triggers === null || triggers === void 0 ? void 0 : triggers.find(trig => trig.label === 'warning');
    const criticalTrigger = triggers === null || triggers === void 0 ? void 0 : triggers.find(trig => trig.label === 'critical');
    const warningTriggerAlertThreshold = typeof (warningTrigger === null || warningTrigger === void 0 ? void 0 : warningTrigger.alertThreshold) === 'number'
        ? warningTrigger === null || warningTrigger === void 0 ? void 0 : warningTrigger.alertThreshold
        : undefined;
    const criticalTriggerAlertThreshold = typeof (criticalTrigger === null || criticalTrigger === void 0 ? void 0 : criticalTrigger.alertThreshold) === 'number'
        ? criticalTrigger === null || criticalTrigger === void 0 ? void 0 : criticalTrigger.alertThreshold
        : undefined;
    const alertResolveThreshold = typeof resolveThreshold === 'number' ? resolveThreshold : undefined;
    const marklinePrecision = Math.max(...[
        warningTriggerAlertThreshold,
        criticalTriggerAlertThreshold,
        alertResolveThreshold,
    ].map(decimal => {
        if (!decimal || !isFinite(decimal))
            return 0;
        let e = 1;
        let p = 0;
        while (Math.round(decimal * e) / e !== decimal) {
            e *= 10;
            p += 1;
        }
        return p;
    }));
    const lineSeries = [
        {
            // e.g. Events or Users
            seriesName,
            dataArray: chartData,
            data: [],
            markPoint: (0, markPoint_1.default)({
                data: [
                    {
                        labelForValue: seriesName,
                        seriesName,
                        symbol: `image://${startedSymbol_1.default}`,
                        name: (0, locale_1.t)('Alert Triggered'),
                        coord: startedCoordinate,
                    },
                    ...(closedTs
                        ? [
                            {
                                labelForValue: seriesName,
                                seriesName,
                                symbol: `image://${closedSymbol_1.default}`,
                                symbolSize: 24,
                                name: (0, locale_1.t)('Alert Resolved'),
                                coord: closedCoordinate,
                            },
                        ]
                        : []),
                ], // TODO(ts): data on this type is likely incomplete (needs @types/echarts@4.6.2)
            }),
        },
        warningTrigger &&
            warningTriggerAlertThreshold && {
            seriesName: 'Warning Alert',
            type: 'line',
            markLine: (0, markLine_1.default)({
                silent: true,
                lineStyle: { color: theme_1.default.yellow300 },
                data: [
                    {
                        yAxis: warningTriggerAlertThreshold,
                    },
                ],
                precision: marklinePrecision,
                label: {
                    show: true,
                    position: 'insideEndTop',
                    formatter: 'WARNING',
                    color: theme_1.default.yellow300,
                    fontSize: 10,
                }, // TODO(ts): Color is not an exposed option for label,
            }),
            data: [],
        },
        criticalTrigger &&
            criticalTriggerAlertThreshold && {
            seriesName: 'Critical Alert',
            type: 'line',
            markLine: (0, markLine_1.default)({
                silent: true,
                lineStyle: { color: theme_1.default.red200 },
                data: [
                    {
                        yAxis: criticalTriggerAlertThreshold,
                    },
                ],
                precision: marklinePrecision,
                label: {
                    show: true,
                    position: 'insideEndTop',
                    formatter: 'CRITICAL',
                    color: theme_1.default.red300,
                    fontSize: 10,
                }, // TODO(ts): Color is not an exposed option for label,
            }),
            data: [],
        },
        criticalTrigger &&
            alertResolveThreshold && {
            seriesName: 'Critical Resolve',
            type: 'line',
            markLine: (0, markLine_1.default)({
                silent: true,
                lineStyle: { color: theme_1.default.gray200 },
                data: [
                    {
                        yAxis: alertResolveThreshold,
                    },
                ],
                precision: marklinePrecision,
                label: {
                    show: true,
                    position: 'insideEndBottom',
                    formatter: 'CRITICAL RESOLUTION',
                    color: theme_1.default.gray200,
                    fontSize: 10,
                }, // TODO(ts): Color is not an option for label,
            }),
            data: [],
        },
    ].filter(truthy);
    return (<lineChart_1.default isGroupedByDate showTimeInTooltip grid={{
            left: 0,
            right: 0,
            top: (0, space_1.default)(2),
            bottom: 0,
        }} series={lineSeries}/>);
};
exports.default = Chart;
//# sourceMappingURL=chart.jsx.map