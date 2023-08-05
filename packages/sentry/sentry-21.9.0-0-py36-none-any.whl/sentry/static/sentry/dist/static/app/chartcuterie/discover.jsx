Object.defineProperty(exports, "__esModule", { value: true });
exports.discoverCharts = void 0;
const tslib_1 = require("tslib");
const isArray_1 = (0, tslib_1.__importDefault)(require("lodash/isArray"));
const xAxis_1 = (0, tslib_1.__importDefault)(require("app/components/charts/components/xAxis"));
const areaSeries_1 = (0, tslib_1.__importDefault)(require("app/components/charts/series/areaSeries"));
const barSeries_1 = (0, tslib_1.__importDefault)(require("app/components/charts/series/barSeries"));
const theme_1 = require("app/utils/theme");
const slack_1 = require("./slack");
const types_1 = require("./types");
const discoverxAxis = (0, xAxis_1.default)({
    theme: theme_1.lightTheme,
    boundaryGap: true,
    splitNumber: 3,
    isGroupedByDate: true,
    axisLabel: { fontSize: 11 },
});
exports.discoverCharts = [];
exports.discoverCharts.push(Object.assign({ key: types_1.ChartType.SLACK_DISCOVER_TOTAL_PERIOD, getOption: (data) => {
        const color = theme_1.lightTheme.charts.getColorPalette(data.stats.data.length - 2);
        const areaSeries = (0, areaSeries_1.default)({
            name: data.seriesName,
            data: data.stats.data.map(([timestamp, countsForTimestamp]) => [
                timestamp * 1000,
                countsForTimestamp.reduce((acc, { count }) => acc + count, 0),
            ]),
            lineStyle: { color: color === null || color === void 0 ? void 0 : color[0], opacity: 1, width: 0.4 },
            areaStyle: { color: color === null || color === void 0 ? void 0 : color[0], opacity: 1 },
        });
        return Object.assign(Object.assign({}, slack_1.slackChartDefaults), { useUTC: true, color, series: [areaSeries] });
    } }, slack_1.slackChartSize));
exports.discoverCharts.push(Object.assign({ key: types_1.ChartType.SLACK_DISCOVER_TOTAL_DAILY, getOption: (data) => {
        const color = theme_1.lightTheme.charts.getColorPalette(data.stats.data.length - 2);
        const barSeries = (0, barSeries_1.default)({
            name: data.seriesName,
            data: data.stats.data.map(([timestamp, countsForTimestamp]) => ({
                value: [
                    timestamp * 1000,
                    countsForTimestamp.reduce((acc, { count }) => acc + count, 0),
                ],
            })),
            itemStyle: { color: color === null || color === void 0 ? void 0 : color[0], opacity: 1 },
        });
        return Object.assign(Object.assign({}, slack_1.slackChartDefaults), { xAxis: discoverxAxis, useUTC: true, color, series: [barSeries] });
    } }, slack_1.slackChartSize));
exports.discoverCharts.push(Object.assign({ key: types_1.ChartType.SLACK_DISCOVER_TOP5_PERIOD, getOption: (data) => {
        if ((0, isArray_1.default)(data.stats.data)) {
            const color = theme_1.lightTheme.charts.getColorPalette(data.stats.data.length - 2);
            const areaSeries = (0, areaSeries_1.default)({
                data: data.stats.data.map(([timestamp, countsForTimestamp]) => [
                    timestamp * 1000,
                    countsForTimestamp.reduce((acc, { count }) => acc + count, 0),
                ]),
                lineStyle: { color: color === null || color === void 0 ? void 0 : color[0], opacity: 1, width: 0.4 },
                areaStyle: { color: color === null || color === void 0 ? void 0 : color[0], opacity: 1 },
            });
            return Object.assign(Object.assign({}, slack_1.slackChartDefaults), { useUTC: true, color, series: [areaSeries] });
        }
        const stats = Object.values(data.stats);
        const color = theme_1.lightTheme.charts.getColorPalette(stats.length - 2);
        const series = stats
            .sort((a, b) => { var _a, _b; return ((_a = a.order) !== null && _a !== void 0 ? _a : 0) - ((_b = b.order) !== null && _b !== void 0 ? _b : 0); })
            .map((topSeries, i) => (0, areaSeries_1.default)({
            stack: 'area',
            data: topSeries.data.map(([timestamp, countsForTimestamp]) => [
                timestamp * 1000,
                countsForTimestamp.reduce((acc, { count }) => acc + count, 0),
            ]),
            lineStyle: { color: color === null || color === void 0 ? void 0 : color[i], opacity: 1, width: 0.4 },
            areaStyle: { color: color === null || color === void 0 ? void 0 : color[i], opacity: 1 },
        }));
        return Object.assign(Object.assign({}, slack_1.slackChartDefaults), { xAxis: discoverxAxis, useUTC: true, color,
            series });
    } }, slack_1.slackChartSize));
exports.discoverCharts.push(Object.assign({ key: types_1.ChartType.SLACK_DISCOVER_TOP5_DAILY, getOption: (data) => {
        if ((0, isArray_1.default)(data.stats.data)) {
            const color = theme_1.lightTheme.charts.getColorPalette(data.stats.data.length - 2);
            const areaSeries = (0, areaSeries_1.default)({
                data: data.stats.data.map(([timestamp, countsForTimestamp]) => [
                    timestamp * 1000,
                    countsForTimestamp.reduce((acc, { count }) => acc + count, 0),
                ]),
                lineStyle: { color: color === null || color === void 0 ? void 0 : color[0], opacity: 1, width: 0.4 },
                areaStyle: { color: color === null || color === void 0 ? void 0 : color[0], opacity: 1 },
            });
            return Object.assign(Object.assign({}, slack_1.slackChartDefaults), { useUTC: true, color, series: [areaSeries] });
        }
        const stats = Object.values(data.stats);
        const color = theme_1.lightTheme.charts.getColorPalette(stats.length - 2);
        const series = stats
            .sort((a, b) => { var _a, _b; return ((_a = a.order) !== null && _a !== void 0 ? _a : 0) - ((_b = b.order) !== null && _b !== void 0 ? _b : 0); })
            .map((topSeries, i) => (0, barSeries_1.default)({
            stack: 'area',
            data: topSeries.data.map(([timestamp, countsForTimestamp]) => [
                timestamp * 1000,
                countsForTimestamp.reduce((acc, { count }) => acc + count, 0),
            ]),
            itemStyle: { color: color === null || color === void 0 ? void 0 : color[i], opacity: 1 },
        }));
        return Object.assign(Object.assign({}, slack_1.slackChartDefaults), { xAxis: discoverxAxis, useUTC: true, color,
            series });
    } }, slack_1.slackChartSize));
//# sourceMappingURL=discover.jsx.map