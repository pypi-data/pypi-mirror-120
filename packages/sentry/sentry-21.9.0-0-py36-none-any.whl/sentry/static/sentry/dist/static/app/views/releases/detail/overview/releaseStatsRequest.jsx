Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_1 = require("@emotion/react");
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const meanBy_1 = (0, tslib_1.__importDefault)(require("lodash/meanBy"));
const omitBy_1 = (0, tslib_1.__importDefault)(require("lodash/omitBy"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const events_1 = require("app/actionCreators/events");
const indicator_1 = require("app/actionCreators/indicator");
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
const locale_1 = require("app/locale");
const utils_1 = require("app/utils");
const formatters_1 = require("app/utils/formatters");
const tokenizeSearch_1 = require("app/utils/tokenizeSearch");
const utils_2 = require("../../utils");
const releaseChartControls_1 = require("./chart/releaseChartControls");
const utils_3 = require("./chart/utils");
const omitIgnoredProps = (props) => (0, omitBy_1.default)(props, (_, key) => ['api', 'orgId', 'projectSlug', 'location', 'children'].includes(key));
class ReleaseStatsRequest extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            reloading: false,
            errored: false,
            data: null,
        };
        this.unmounting = false;
        this.fetchData = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            var _a, _b;
            let data = null;
            const { yAxis, hasHealthData, hasDiscover, hasPerformance } = this.props;
            if (!hasHealthData && !hasDiscover && !hasPerformance) {
                return;
            }
            this.setState(state => ({
                reloading: state.data !== null,
                errored: false,
            }));
            try {
                if (yAxis === releaseChartControls_1.YAxis.SESSIONS) {
                    data = yield this.fetchSessions();
                }
                if (yAxis === releaseChartControls_1.YAxis.USERS) {
                    data = yield this.fetchUsers();
                }
                if (yAxis === releaseChartControls_1.YAxis.CRASH_FREE) {
                    data = yield this.fetchCrashFree();
                }
                if (yAxis === releaseChartControls_1.YAxis.SESSION_DURATION) {
                    data = yield this.fetchSessionDuration();
                }
                if (yAxis === releaseChartControls_1.YAxis.EVENTS ||
                    yAxis === releaseChartControls_1.YAxis.FAILED_TRANSACTIONS ||
                    yAxis === releaseChartControls_1.YAxis.COUNT_DURATION ||
                    yAxis === releaseChartControls_1.YAxis.COUNT_VITAL) {
                    // this is used to get total counts for chart footer summary
                    data = yield this.fetchEventData();
                }
            }
            catch (error) {
                (0, indicator_1.addErrorMessage)((_b = (_a = error.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : (0, locale_1.t)('Error loading chart data'));
                this.setState({
                    errored: true,
                    data: null,
                });
            }
            if (!(0, utils_1.defined)(data) && !this.state.errored) {
                // this should not happen
                this.setState({
                    errored: true,
                    data: null,
                });
            }
            if (this.unmounting) {
                return;
            }
            this.setState({
                reloading: false,
                data,
            });
        });
    }
    componentDidMount() {
        this.fetchData();
    }
    componentDidUpdate(prevProps) {
        if ((0, isEqual_1.default)(omitIgnoredProps(prevProps), omitIgnoredProps(this.props))) {
            return;
        }
        this.fetchData();
    }
    componentWillUnmount() {
        this.unmounting = true;
    }
    get path() {
        const { organization } = this.props;
        return `/organizations/${organization.slug}/sessions/`;
    }
    get baseQueryParams() {
        const { version, organization, location, selection, defaultStatsPeriod } = this.props;
        return Object.assign({ query: new tokenizeSearch_1.MutableSearch([`release:"${version}"`]).formatString(), interval: (0, utils_3.getInterval)(selection.datetime, {
                highFidelity: organization.features.includes('minute-resolution-sessions'),
            }) }, (0, getParams_1.getParams)((0, pick_1.default)(location.query, Object.values(globalSelectionHeader_1.URL_PARAM)), {
            defaultStatsPeriod,
        }));
    }
    fetchSessions() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, version, theme } = this.props;
            const [releaseResponse, otherReleasesResponse] = yield Promise.all([
                api.requestPromise(this.path, {
                    query: Object.assign(Object.assign({}, this.baseQueryParams), { field: 'sum(session)', groupBy: 'session.status' }),
                }),
                api.requestPromise(this.path, {
                    query: Object.assign(Object.assign({}, this.baseQueryParams), { field: 'sum(session)', groupBy: 'session.status', query: new tokenizeSearch_1.MutableSearch([`!release:"${version}"`]).formatString() }),
                }),
            ]);
            const totalSessions = (0, utils_3.getTotalsFromSessionsResponse)({
                response: releaseResponse,
                field: 'sum(session)',
            });
            const chartData = (0, utils_3.fillChartDataFromSessionsResponse)({
                response: releaseResponse,
                field: 'sum(session)',
                groupBy: 'session.status',
                chartData: (0, utils_3.initSessionsBreakdownChartData)(theme),
            });
            const otherChartData = (0, utils_3.fillChartDataFromSessionsResponse)({
                response: otherReleasesResponse,
                field: 'sum(session)',
                groupBy: 'session.status',
                chartData: (0, utils_3.initOtherSessionsBreakdownChartData)(theme),
            });
            return {
                chartData: [...Object.values(chartData), ...Object.values(otherChartData)],
                chartSummary: totalSessions.toLocaleString(),
            };
        });
    }
    fetchUsers() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, version, theme } = this.props;
            const [releaseResponse, otherReleasesResponse] = yield Promise.all([
                api.requestPromise(this.path, {
                    query: Object.assign(Object.assign({}, this.baseQueryParams), { field: 'count_unique(user)', groupBy: 'session.status' }),
                }),
                api.requestPromise(this.path, {
                    query: Object.assign(Object.assign({}, this.baseQueryParams), { field: 'count_unique(user)', groupBy: 'session.status', query: new tokenizeSearch_1.MutableSearch([`!release:"${version}"`]).formatString() }),
                }),
            ]);
            const totalUsers = (0, utils_3.getTotalsFromSessionsResponse)({
                response: releaseResponse,
                field: 'count_unique(user)',
            });
            const chartData = (0, utils_3.fillChartDataFromSessionsResponse)({
                response: releaseResponse,
                field: 'count_unique(user)',
                groupBy: 'session.status',
                chartData: (0, utils_3.initSessionsBreakdownChartData)(theme),
            });
            const otherChartData = (0, utils_3.fillChartDataFromSessionsResponse)({
                response: otherReleasesResponse,
                field: 'count_unique(user)',
                groupBy: 'session.status',
                chartData: (0, utils_3.initOtherSessionsBreakdownChartData)(theme),
            });
            return {
                chartData: [...Object.values(chartData), ...Object.values(otherChartData)],
                chartSummary: totalUsers.toLocaleString(),
            };
        });
    }
    fetchCrashFree() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, version } = this.props;
            const [releaseResponse, otherReleasesResponse] = yield Promise.all([
                api.requestPromise(this.path, {
                    query: Object.assign(Object.assign({}, this.baseQueryParams), { field: ['sum(session)', 'count_unique(user)'], groupBy: 'session.status' }),
                }),
                api.requestPromise(this.path, {
                    query: Object.assign(Object.assign({}, this.baseQueryParams), { field: ['sum(session)', 'count_unique(user)'], groupBy: 'session.status', query: new tokenizeSearch_1.MutableSearch([`!release:"${version}"`]).formatString() }),
                }),
            ]);
            let chartData = (0, utils_3.fillCrashFreeChartDataFromSessionsReponse)({
                response: releaseResponse,
                field: 'sum(session)',
                entity: 'sessions',
                chartData: (0, utils_3.initCrashFreeChartData)(),
            });
            chartData = (0, utils_3.fillCrashFreeChartDataFromSessionsReponse)({
                response: releaseResponse,
                field: 'count_unique(user)',
                entity: 'users',
                chartData,
            });
            let otherChartData = (0, utils_3.fillCrashFreeChartDataFromSessionsReponse)({
                response: otherReleasesResponse,
                field: 'sum(session)',
                entity: 'sessions',
                chartData: (0, utils_3.initOtherCrashFreeChartData)(),
            });
            otherChartData = (0, utils_3.fillCrashFreeChartDataFromSessionsReponse)({
                response: otherReleasesResponse,
                field: 'count_unique(user)',
                entity: 'users',
                chartData: otherChartData,
            });
            // summary is averaging previously rounded values - this might lead to a slightly skewed percentage
            const summary = (0, locale_1.tct)('[usersPercent] users, [sessionsPercent] sessions', {
                usersPercent: (0, utils_2.displayCrashFreePercent)((0, meanBy_1.default)(chartData.users.data.filter(item => (0, utils_1.defined)(item.value)), 'value')),
                sessionsPercent: (0, utils_2.displayCrashFreePercent)((0, meanBy_1.default)(chartData.sessions.data.filter(item => (0, utils_1.defined)(item.value)), 'value')),
            });
            return {
                chartData: [...Object.values(chartData), ...Object.values(otherChartData)],
                chartSummary: summary,
            };
        });
    }
    fetchSessionDuration() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, version } = this.props;
            const [releaseResponse, otherReleasesResponse] = yield Promise.all([
                api.requestPromise(this.path, {
                    query: Object.assign(Object.assign({}, this.baseQueryParams), { field: 'p50(session.duration)' }),
                }),
                api.requestPromise(this.path, {
                    query: Object.assign(Object.assign({}, this.baseQueryParams), { field: 'p50(session.duration)', query: new tokenizeSearch_1.MutableSearch([`!release:"${version}"`]).formatString() }),
                }),
            ]);
            const totalMedianDuration = (0, utils_3.getTotalsFromSessionsResponse)({
                response: releaseResponse,
                field: 'p50(session.duration)',
            });
            const chartData = (0, utils_3.fillChartDataFromSessionsResponse)({
                response: releaseResponse,
                field: 'p50(session.duration)',
                groupBy: null,
                chartData: (0, utils_3.initSessionDurationChartData)(),
                valueFormatter: duration => (0, utils_2.roundDuration)(duration ? duration / 1000 : 0),
            });
            const otherChartData = (0, utils_3.fillChartDataFromSessionsResponse)({
                response: otherReleasesResponse,
                field: 'p50(session.duration)',
                groupBy: null,
                chartData: (0, utils_3.initOtherSessionDurationChartData)(),
                valueFormatter: duration => (0, utils_2.roundDuration)(duration ? duration / 1000 : 0),
            });
            return {
                chartData: [...Object.values(chartData), ...Object.values(otherChartData)],
                chartSummary: (0, formatters_1.getExactDuration)((0, utils_2.roundDuration)(totalMedianDuration ? totalMedianDuration / 1000 : 0)),
            };
        });
    }
    fetchEventData() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, organization, location, yAxis, eventType, vitalType, selection, version } = this.props;
            const eventView = (0, utils_3.getReleaseEventView)(selection, version, yAxis, eventType, vitalType, organization, true);
            const payload = eventView.getEventsAPIPayload(location);
            const eventsCountResponse = yield (0, events_1.fetchTotalCount)(api, organization.slug, payload);
            const chartSummary = eventsCountResponse.toLocaleString();
            return { chartData: [], chartSummary };
        });
    }
    render() {
        var _a, _b;
        const { children } = this.props;
        const { data, reloading, errored } = this.state;
        const loading = data === null;
        return children({
            loading,
            reloading,
            errored,
            chartData: (_a = data === null || data === void 0 ? void 0 : data.chartData) !== null && _a !== void 0 ? _a : [],
            chartSummary: (_b = data === null || data === void 0 ? void 0 : data.chartSummary) !== null && _b !== void 0 ? _b : '',
        });
    }
}
exports.default = (0, react_1.withTheme)(ReleaseStatsRequest);
//# sourceMappingURL=releaseStatsRequest.jsx.map