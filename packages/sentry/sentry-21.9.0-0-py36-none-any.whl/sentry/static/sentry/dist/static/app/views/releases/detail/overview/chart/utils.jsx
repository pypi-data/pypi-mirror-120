Object.defineProperty(exports, "__esModule", { value: true });
exports.fillCrashFreeChartDataFromSessionsReponse = exports.fillChartDataFromSessionsResponse = exports.getTotalsFromSessionsResponse = exports.sortSessionSeries = exports.isOtherSeries = exports.initOtherSessionDurationChartData = exports.initSessionDurationChartData = exports.initOtherCrashFreeChartData = exports.initCrashFreeChartData = exports.initOtherSessionsBreakdownChartData = exports.initSessionsBreakdownChartData = exports.getReleaseEventView = exports.getInterval = void 0;
const tslib_1 = require("tslib");
const color_1 = (0, tslib_1.__importDefault)(require("color"));
const utils_1 = require("app/components/charts/utils");
const chartPalette_1 = (0, tslib_1.__importDefault)(require("app/constants/chartPalette"));
const locale_1 = require("app/locale");
const utils_2 = require("app/utils");
const dates_1 = require("app/utils/dates");
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const fields_1 = require("app/utils/discover/fields");
const formatters_1 = require("app/utils/formatters");
const constants_1 = require("app/utils/performance/vitals/constants");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const utils_3 = require("app/views/releases/utils");
const sessionTerm_1 = require("app/views/releases/utils/sessionTerm");
const releaseChartControls_1 = require("./releaseChartControls");
function getInterval(datetimeObj, { highFidelity } = {}) {
    const diffInMinutes = (0, utils_1.getDiffInMinutes)(datetimeObj);
    if (highFidelity &&
        diffInMinutes < 360 // limit on backend is set to six hour
    ) {
        return '5m';
    }
    if (diffInMinutes > utils_1.TWO_WEEKS) {
        return '6h';
    }
    else {
        return '1h';
    }
}
exports.getInterval = getInterval;
function getReleaseEventView(selection, version, yAxis, eventType = releaseChartControls_1.EventType.ALL, vitalType = fields_1.WebVital.LCP, organization, 
/**
 * Indicates that we're only interested in the current release.
 * This is useful for the event meta end point where we don't want
 * to include the other releases.
 */
currentOnly) {
    const { projects, environments, datetime } = selection;
    const { start, end, period } = datetime;
    const releaseFilter = currentOnly ? `release:${version}` : '';
    const toOther = `to_other(release,"${(0, utils_2.escapeDoubleQuotes)(version)}",others,current)`;
    // this orderby ensures that the order is [others, current]
    const toOtherAlias = (0, fields_1.getAggregateAlias)(toOther);
    const baseQuery = {
        id: undefined,
        version: 2,
        name: `${(0, locale_1.t)('Release')} ${(0, formatters_1.formatVersion)(version)}`,
        fields: [`count()`, toOther],
        orderby: toOtherAlias,
        range: period,
        environment: environments,
        projects,
        start: start ? (0, dates_1.getUtcDateString)(start) : undefined,
        end: end ? (0, dates_1.getUtcDateString)(end) : undefined,
    };
    switch (yAxis) {
        case releaseChartControls_1.YAxis.FAILED_TRANSACTIONS:
            const statusFilters = ['ok', 'cancelled', 'unknown'].map(s => `!transaction.status:${s}`);
            return eventView_1.default.fromSavedQuery(Object.assign(Object.assign({}, baseQuery), { query: new tokenizeSearch_1.MutableSearch(['event.type:transaction', releaseFilter, ...statusFilters].filter(Boolean)).formatString() }));
        case releaseChartControls_1.YAxis.COUNT_VITAL:
        case releaseChartControls_1.YAxis.COUNT_DURATION:
            const column = yAxis === releaseChartControls_1.YAxis.COUNT_DURATION ? 'transaction.duration' : vitalType;
            const threshold = yAxis === releaseChartControls_1.YAxis.COUNT_DURATION
                ? organization === null || organization === void 0 ? void 0 : organization.apdexThreshold
                : constants_1.WEB_VITAL_DETAILS[vitalType].poorThreshold;
            return eventView_1.default.fromSavedQuery(Object.assign(Object.assign({}, baseQuery), { query: new tokenizeSearch_1.MutableSearch([
                    'event.type:transaction',
                    releaseFilter,
                    threshold ? `${column}:>${threshold}` : '',
                ].filter(Boolean)).formatString() }));
        case releaseChartControls_1.YAxis.EVENTS:
            const eventTypeFilter = eventType === releaseChartControls_1.EventType.ALL ? '' : `event.type:${eventType}`;
            return eventView_1.default.fromSavedQuery(Object.assign(Object.assign({}, baseQuery), { query: new tokenizeSearch_1.MutableSearch([releaseFilter, eventTypeFilter].filter(Boolean)).formatString() }));
        default:
            return eventView_1.default.fromSavedQuery(Object.assign(Object.assign({}, baseQuery), { fields: ['issue', 'title', 'count()', 'count_unique(user)', 'project'], query: new tokenizeSearch_1.MutableSearch([
                    `release:${version}`,
                    '!event.type:transaction',
                ]).formatString(), orderby: '-count' }));
    }
}
exports.getReleaseEventView = getReleaseEventView;
function initSessionsBreakdownChartData(theme) {
    const colors = theme.charts.getColorPalette(14);
    return {
        healthy: {
            seriesName: sessionTerm_1.sessionTerm.healthy,
            data: [],
            color: theme.green300,
            areaStyle: {
                color: theme.green300,
                opacity: 1,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        },
        errored: {
            seriesName: sessionTerm_1.sessionTerm.errored,
            data: [],
            color: colors[12],
            areaStyle: {
                color: colors[12],
                opacity: 1,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        },
        abnormal: {
            seriesName: sessionTerm_1.sessionTerm.abnormal,
            data: [],
            color: colors[15],
            areaStyle: {
                color: colors[15],
                opacity: 1,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        },
        crashed: {
            seriesName: sessionTerm_1.sessionTerm.crashed,
            data: [],
            color: theme.red300,
            areaStyle: {
                color: theme.red300,
                opacity: 1,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        },
    };
}
exports.initSessionsBreakdownChartData = initSessionsBreakdownChartData;
function initOtherSessionsBreakdownChartData(theme) {
    const colors = theme.charts.getColorPalette(14);
    return Object.assign({ healthy: {
            seriesName: sessionTerm_1.sessionTerm.otherHealthy,
            data: [],
            color: theme.green300,
            areaStyle: {
                color: theme.green300,
                opacity: 0.3,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        }, errored: {
            seriesName: sessionTerm_1.sessionTerm.otherErrored,
            data: [],
            color: colors[12],
            areaStyle: {
                color: colors[12],
                opacity: 0.3,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        }, abnormal: {
            seriesName: sessionTerm_1.sessionTerm.otherAbnormal,
            data: [],
            color: colors[15],
            areaStyle: {
                color: colors[15],
                opacity: 0.3,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        }, crashed: {
            seriesName: sessionTerm_1.sessionTerm.otherCrashed,
            data: [],
            color: theme.red300,
            areaStyle: {
                color: theme.red300,
                opacity: 0.3,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        } }, initOtherReleasesChartData());
}
exports.initOtherSessionsBreakdownChartData = initOtherSessionsBreakdownChartData;
function initCrashFreeChartData() {
    return {
        users: {
            seriesName: sessionTerm_1.sessionTerm['crash-free-users'],
            data: [],
            color: chartPalette_1.default[1][0],
            lineStyle: {
                color: chartPalette_1.default[1][0],
            },
        },
        sessions: {
            seriesName: sessionTerm_1.sessionTerm['crash-free-sessions'],
            data: [],
            color: chartPalette_1.default[1][1],
            lineStyle: {
                color: chartPalette_1.default[1][1],
            },
        },
    };
}
exports.initCrashFreeChartData = initCrashFreeChartData;
function initOtherCrashFreeChartData() {
    return Object.assign(Object.assign({}, initOtherReleasesChartData()), { users: {
            seriesName: sessionTerm_1.sessionTerm.otherCrashFreeUsers,
            data: [],
            z: 0,
            color: (0, color_1.default)(chartPalette_1.default[1][0]).lighten(0.9).alpha(0.9).string(),
            lineStyle: {
                color: chartPalette_1.default[1][0],
                opacity: 0.1,
            },
        }, sessions: {
            seriesName: sessionTerm_1.sessionTerm.otherCrashFreeSessions,
            data: [],
            z: 0,
            color: (0, color_1.default)(chartPalette_1.default[1][1]).lighten(0.5).alpha(0.9).string(),
            lineStyle: {
                color: chartPalette_1.default[1][1],
                opacity: 0.3,
            },
        } });
}
exports.initOtherCrashFreeChartData = initOtherCrashFreeChartData;
function initSessionDurationChartData() {
    return {
        0: {
            seriesName: sessionTerm_1.sessionTerm.duration,
            data: [],
            color: chartPalette_1.default[0][0],
            areaStyle: {
                color: chartPalette_1.default[0][0],
                opacity: 1,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        },
    };
}
exports.initSessionDurationChartData = initSessionDurationChartData;
function initOtherSessionDurationChartData() {
    return {
        0: {
            seriesName: sessionTerm_1.sessionTerm.otherReleases,
            data: [],
            z: 0,
            color: (0, color_1.default)(chartPalette_1.default[0][0]).alpha(0.4).string(),
            areaStyle: {
                color: chartPalette_1.default[0][0],
                opacity: 0.3,
            },
            lineStyle: {
                opacity: 0,
                width: 0.4,
            },
        },
    };
}
exports.initOtherSessionDurationChartData = initOtherSessionDurationChartData;
// this series will never be filled with data - we use it to act as an alias in legend (we don't display other healthy, other crashes, etc. there)
// if you click on it, we toggle all "other" series (other healthy, other crashed, ...)
function initOtherReleasesChartData() {
    return {
        otherReleases: {
            seriesName: sessionTerm_1.sessionTerm.otherReleases,
            data: [],
            color: (0, color_1.default)(chartPalette_1.default[0][0]).alpha(0.4).string(),
        },
    };
}
function isOtherSeries(series) {
    return [
        sessionTerm_1.sessionTerm.otherCrashed,
        sessionTerm_1.sessionTerm.otherAbnormal,
        sessionTerm_1.sessionTerm.otherErrored,
        sessionTerm_1.sessionTerm.otherHealthy,
        sessionTerm_1.sessionTerm.otherCrashFreeUsers,
        sessionTerm_1.sessionTerm.otherCrashFreeSessions,
    ].includes(series.seriesName);
}
exports.isOtherSeries = isOtherSeries;
const seriesOrder = [
    sessionTerm_1.sessionTerm.healthy,
    sessionTerm_1.sessionTerm.errored,
    sessionTerm_1.sessionTerm.crashed,
    sessionTerm_1.sessionTerm.abnormal,
    sessionTerm_1.sessionTerm.otherHealthy,
    sessionTerm_1.sessionTerm.otherErrored,
    sessionTerm_1.sessionTerm.otherCrashed,
    sessionTerm_1.sessionTerm.otherAbnormal,
    sessionTerm_1.sessionTerm.duration,
    sessionTerm_1.sessionTerm['crash-free-sessions'],
    sessionTerm_1.sessionTerm['crash-free-users'],
    sessionTerm_1.sessionTerm.otherCrashFreeSessions,
    sessionTerm_1.sessionTerm.otherCrashFreeUsers,
    sessionTerm_1.sessionTerm.otherReleases,
];
function sortSessionSeries(a, b) {
    return seriesOrder.indexOf(a.seriesName) - seriesOrder.indexOf(b.seriesName);
}
exports.sortSessionSeries = sortSessionSeries;
function getTotalsFromSessionsResponse({ response, field, }) {
    return response.groups.reduce((acc, group) => {
        return acc + group.totals[field];
    }, 0);
}
exports.getTotalsFromSessionsResponse = getTotalsFromSessionsResponse;
function fillChartDataFromSessionsResponse({ response, field, groupBy, chartData, valueFormatter, }) {
    response.intervals.forEach((interval, index) => {
        response.groups.forEach(group => {
            const value = group.series[field][index];
            chartData[groupBy === null ? 0 : group.by[groupBy]].data.push({
                name: interval,
                value: typeof valueFormatter === 'function' ? valueFormatter(value) : value,
            });
        });
    });
    return chartData;
}
exports.fillChartDataFromSessionsResponse = fillChartDataFromSessionsResponse;
function fillCrashFreeChartDataFromSessionsReponse({ response, field, entity, chartData, }) {
    response.intervals.forEach((interval, index) => {
        var _a, _b;
        const intervalTotalSessions = response.groups.reduce((acc, group) => acc + group.series[field][index], 0);
        const intervalCrashedSessions = (_b = (_a = response.groups.find(group => group.by['session.status'] === 'crashed')) === null || _a === void 0 ? void 0 : _a.series[field][index]) !== null && _b !== void 0 ? _b : 0;
        const crashedSessionsPercent = (0, utils_2.percent)(intervalCrashedSessions, intervalTotalSessions);
        chartData[entity].data.push({
            name: interval,
            value: intervalTotalSessions === 0
                ? null
                : (0, utils_3.getCrashFreePercent)(100 - crashedSessionsPercent),
        });
    });
    return chartData;
}
exports.fillCrashFreeChartDataFromSessionsReponse = fillCrashFreeChartDataFromSessionsReponse;
//# sourceMappingURL=utils.jsx.map