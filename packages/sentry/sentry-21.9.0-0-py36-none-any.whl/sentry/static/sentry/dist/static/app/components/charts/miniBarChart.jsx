Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
// Import to ensure echarts components are loaded.
require("./components/markPoint");
const React = (0, tslib_1.__importStar)(require("react"));
const set_1 = (0, tslib_1.__importDefault)(require("lodash/set"));
const dates_1 = require("app/utils/dates");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const barChart_1 = (0, tslib_1.__importDefault)(require("./barChart"));
const utils_1 = require("./utils");
const defaultProps = {
    /**
     * Colors to use on the chart.
     */
    colors: [theme_1.default.gray200, theme_1.default.purple300, theme_1.default.purple300],
    /**
     * Show max/min values on yAxis
     */
    labelYAxisExtents: false,
    /**
     * Whether not the series should be stacked.
     *
     * Some of our stats endpoints return data where the 'total' series includes
     * breakdown data (issues). For these results `stacked` should be false.
     * Other endpoints return decomposed results that need to be stacked (outcomes).
     */
    stacked: false,
};
class MiniBarChart extends React.Component {
    render() {
        const _a = this.props, { markers, emphasisColors, colors, series: _series, labelYAxisExtents, stacked, series, hideDelay, tooltipFormatter } = _a, props = (0, tslib_1.__rest)(_a, ["markers", "emphasisColors", "colors", "series", "labelYAxisExtents", "stacked", "series", "hideDelay", "tooltipFormatter"]);
        const { ref: _ref } = props, barChartProps = (0, tslib_1.__rest)(props, ["ref"]);
        let chartSeries = [];
        // Ensure bars overlap and that empty values display as we're disabling the axis lines.
        if (series && series.length) {
            chartSeries = series.map((original, i) => {
                var _a;
                const updated = Object.assign(Object.assign({}, original), { cursor: 'normal', type: 'bar' });
                if (i === 0) {
                    updated.barMinHeight = 1;
                    if (stacked === false) {
                        updated.barGap = '-100%';
                    }
                }
                if (stacked) {
                    updated.stack = 'stack1';
                }
                (0, set_1.default)(updated, 'itemStyle.color', colors[i]);
                (0, set_1.default)(updated, 'itemStyle.opacity', 0.6);
                (0, set_1.default)(updated, 'itemStyle.emphasis.opacity', 1.0);
                (0, set_1.default)(updated, 'itemStyle.emphasis.color', (_a = emphasisColors === null || emphasisColors === void 0 ? void 0 : emphasisColors[i]) !== null && _a !== void 0 ? _a : colors[i]);
                return updated;
            });
        }
        if (markers) {
            const markerTooltip = {
                show: true,
                trigger: 'item',
                formatter: ({ data }) => {
                    var _a;
                    const time = (0, dates_1.getFormattedDate)(data.coord[0], 'MMM D, YYYY LT', {
                        local: !this.props.utc,
                    });
                    const name = (0, utils_1.truncationFormatter)(data.name, (_a = props === null || props === void 0 ? void 0 : props.xAxis) === null || _a === void 0 ? void 0 : _a.truncate);
                    return [
                        '<div class="tooltip-series">',
                        `<div><span class="tooltip-label"><strong>${name}</strong></span></div>`,
                        '</div>',
                        '<div class="tooltip-date">',
                        time,
                        '</div>',
                        '</div>',
                        '<div class="tooltip-arrow"></div>',
                    ].join('');
                },
            };
            const markPoint = {
                data: markers.map((marker) => {
                    var _a;
                    return ({
                        name: marker.name,
                        coord: [marker.value, 0],
                        tooltip: markerTooltip,
                        symbol: 'circle',
                        symbolSize: (_a = marker.symbolSize) !== null && _a !== void 0 ? _a : 8,
                        itemStyle: {
                            color: marker.color,
                            borderColor: '#ffffff',
                        },
                    });
                }),
            };
            chartSeries[0].markPoint = markPoint;
        }
        const yAxisOptions = labelYAxisExtents
            ? {
                showMinLabel: true,
                showMaxLabel: true,
                interval: Infinity,
            }
            : {
                axisLabel: {
                    show: false,
                },
            };
        const chartOptions = {
            tooltip: {
                trigger: 'axis',
                hideDelay,
                valueFormatter: tooltipFormatter
                    ? (value) => tooltipFormatter(value)
                    : undefined,
            },
            yAxis: Object.assign({ max(value) {
                    // This keeps small datasets from looking 'scary'
                    // by having full bars for < 10 values.
                    return Math.max(10, value.max);
                }, splitLine: {
                    show: false,
                } }, yAxisOptions),
            grid: {
                // Offset to ensure there is room for the marker symbols at the
                // default size.
                top: labelYAxisExtents ? 6 : 0,
                bottom: markers || labelYAxisExtents ? 4 : 0,
                left: markers ? 4 : 0,
                right: markers ? 4 : 0,
            },
            xAxis: {
                axisLine: {
                    show: false,
                },
                axisTick: {
                    show: false,
                    alignWithLabel: true,
                },
                axisLabel: {
                    show: false,
                },
                axisPointer: {
                    type: 'line',
                    label: {
                        show: false,
                    },
                    lineStyle: {
                        width: 0,
                    },
                },
            },
            options: {
                animation: false,
            },
        };
        return <barChart_1.default series={chartSeries} {...chartOptions} {...barChartProps}/>;
    }
}
MiniBarChart.defaultProps = defaultProps;
exports.default = MiniBarChart;
//# sourceMappingURL=miniBarChart.jsx.map