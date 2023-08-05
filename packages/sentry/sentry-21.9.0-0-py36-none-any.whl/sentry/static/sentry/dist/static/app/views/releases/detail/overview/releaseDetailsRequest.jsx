Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const indicator_1 = require("app/actionCreators/indicator");
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const sessions_1 = require("app/utils/sessions");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const utils_1 = require("../../utils");
class ReleaseDetailsRequest extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            reloading: false,
            errored: false,
            thisRelease: null,
            allReleases: null,
        };
        this.fetchData = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            var _a, _b;
            const { api, disable } = this.props;
            if (disable) {
                return;
            }
            api.clear();
            this.setState(state => ({
                reloading: state.thisRelease !== null && state.allReleases !== null,
                errored: false,
            }));
            const promises = [this.fetchThisRelease(), this.fetchAllReleases()];
            try {
                const [thisRelease, allReleases] = yield Promise.all(promises);
                this.setState({
                    reloading: false,
                    thisRelease: (0, sessions_1.filterSessionsInTimeWindow)(thisRelease, this.baseQueryParams.start, this.baseQueryParams.end),
                    allReleases: (0, sessions_1.filterSessionsInTimeWindow)(allReleases, this.baseQueryParams.start, this.baseQueryParams.end),
                });
            }
            catch (error) {
                (0, indicator_1.addErrorMessage)((_b = (_a = error.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) !== null && _b !== void 0 ? _b : (0, locale_1.t)('Error loading health data'));
                this.setState({
                    reloading: false,
                    errored: true,
                });
            }
        });
    }
    componentDidMount() {
        this.fetchData();
    }
    componentDidUpdate(prevProps) {
        if (prevProps.version !== this.props.version ||
            !(0, isEqual_1.default)(prevProps.location, this.props.location)) {
            this.fetchData();
        }
    }
    get path() {
        const { organization } = this.props;
        return `/organizations/${organization.slug}/sessions/`;
    }
    get baseQueryParams() {
        var _a;
        const { location, releaseBounds, organization } = this.props;
        const releaseParams = (0, utils_1.getReleaseParams)({
            location,
            releaseBounds,
            defaultStatsPeriod: constants_1.DEFAULT_STATS_PERIOD,
            allowEmptyPeriod: true,
        });
        return Object.assign({ field: ['count_unique(user)', 'sum(session)', 'p50(session.duration)'], groupBy: ['session.status'], interval: (0, sessions_1.getSessionsInterval)({
                start: releaseParams.start,
                end: releaseParams.end,
                period: (_a = releaseParams.statsPeriod) !== null && _a !== void 0 ? _a : undefined,
            }, { highFidelity: organization.features.includes('minute-resolution-sessions') }) }, releaseParams);
    }
    fetchThisRelease() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, version } = this.props;
            const response = yield api.requestPromise(this.path, {
                query: Object.assign(Object.assign({}, this.baseQueryParams), { query: `release:"${version}"` }),
            });
            return response;
        });
    }
    fetchAllReleases() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api } = this.props;
            const response = yield api.requestPromise(this.path, {
                query: this.baseQueryParams,
            });
            return response;
        });
    }
    render() {
        const { reloading, errored, thisRelease, allReleases } = this.state;
        const { children } = this.props;
        const loading = thisRelease === null && allReleases === null;
        return children({
            loading,
            reloading,
            errored,
            thisRelease,
            allReleases,
        });
    }
}
exports.default = (0, withApi_1.default)(ReleaseDetailsRequest);
//# sourceMappingURL=releaseDetailsRequest.jsx.map