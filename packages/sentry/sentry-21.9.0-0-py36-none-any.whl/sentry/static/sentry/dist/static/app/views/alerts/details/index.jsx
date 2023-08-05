Object.defineProperty(exports, "__esModule", { value: true });
exports.alertDetailsLink = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const incident_1 = require("app/actionCreators/incident");
const indicator_1 = require("app/actionCreators/indicator");
const members_1 = require("app/actionCreators/members");
const sentryDocumentTitle_1 = (0, tslib_1.__importDefault)(require("app/components/sentryDocumentTitle"));
const locale_1 = require("app/locale");
const analytics_1 = require("app/utils/analytics");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const types_1 = require("../types");
const utils_1 = require("../utils");
const body_1 = (0, tslib_1.__importDefault)(require("./body"));
const header_1 = (0, tslib_1.__importDefault)(require("./header"));
const alertDetailsLink = (organization, incident) => `/organizations/${organization.slug}/alerts/rules/details/${(incident === null || incident === void 0 ? void 0 : incident.alertRule.status) === types_1.AlertRuleStatus.SNAPSHOT &&
    (incident === null || incident === void 0 ? void 0 : incident.alertRule.originalAlertRuleId)
    ? incident === null || incident === void 0 ? void 0 : incident.alertRule.originalAlertRuleId
    : incident === null || incident === void 0 ? void 0 : incident.alertRule.id}/`;
exports.alertDetailsLink = alertDetailsLink;
class IncidentDetails extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = { isLoading: false, hasError: false };
        this.fetchData = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            this.setState({ isLoading: true, hasError: false });
            const { api, location, organization, params: { orgId, alertId }, } = this.props;
            try {
                const incidentPromise = (0, utils_1.fetchIncident)(api, orgId, alertId).then(incident => {
                    const hasRedesign = incident.alertRule &&
                        this.props.organization.features.includes('alert-details-redesign');
                    // only stop redirect if param is explicitly set to false
                    const stopRedirect = location && location.query && location.query.redirect === 'false';
                    if (hasRedesign && !stopRedirect) {
                        react_router_1.browserHistory.replace({
                            pathname: (0, exports.alertDetailsLink)(organization, incident),
                            query: { alert: incident.identifier },
                        });
                    }
                    this.setState({ incident });
                    (0, incident_1.markIncidentAsSeen)(api, orgId, incident);
                });
                const statsPromise = (0, utils_1.fetchIncidentStats)(api, orgId, alertId).then(stats => this.setState({ stats }));
                // State not set after promise.all because stats *usually* takes
                // more time than the incident api
                yield Promise.all([incidentPromise, statsPromise]);
                this.setState({ isLoading: false, hasError: false });
            }
            catch (_err) {
                this.setState({ isLoading: false, hasError: true });
            }
        });
        this.handleSubscriptionChange = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, params: { orgId, alertId }, } = this.props;
            if (!this.state.incident) {
                return;
            }
            const isSubscribed = this.state.incident.isSubscribed;
            const newIsSubscribed = !isSubscribed;
            this.setState(state => ({
                incident: Object.assign(Object.assign({}, state.incident), { isSubscribed: newIsSubscribed }),
            }));
            try {
                (0, utils_1.updateSubscription)(api, orgId, alertId, newIsSubscribed);
            }
            catch (_err) {
                this.setState(state => ({
                    incident: Object.assign(Object.assign({}, state.incident), { isSubscribed }),
                }));
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('An error occurred, your subscription status was not changed.'));
            }
        });
        this.handleStatusChange = () => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, params: { orgId, alertId }, } = this.props;
            if (!this.state.incident) {
                return;
            }
            const { status } = this.state.incident;
            const newStatus = (0, utils_1.isOpen)(this.state.incident) ? types_1.IncidentStatus.CLOSED : status;
            this.setState(state => ({
                incident: Object.assign(Object.assign({}, state.incident), { status: newStatus }),
            }));
            try {
                const incident = yield (0, utils_1.updateStatus)(api, orgId, alertId, newStatus);
                // Update entire incident object because updating status can cause other parts
                // of the model to change (e.g close date)
                this.setState({ incident });
            }
            catch (_err) {
                this.setState(state => ({
                    incident: Object.assign(Object.assign({}, state.incident), { status }),
                }));
                (0, indicator_1.addErrorMessage)((0, locale_1.t)('An error occurred, your incident status was not changed.'));
            }
        });
    }
    componentDidMount() {
        const { api, organization, params } = this.props;
        (0, analytics_1.trackAnalyticsEvent)({
            eventKey: 'alert_details.viewed',
            eventName: 'Alert Details: Viewed',
            organization_id: parseInt(organization.id, 10),
            alert_id: parseInt(params.alertId, 10),
        });
        (0, members_1.fetchOrgMembers)(api, params.orgId);
        this.fetchData();
    }
    render() {
        var _a;
        const { incident, stats, hasError } = this.state;
        const { params, organization } = this.props;
        const { alertId } = params;
        const project = (_a = incident === null || incident === void 0 ? void 0 : incident.projects) === null || _a === void 0 ? void 0 : _a[0];
        return (<react_1.Fragment>
        <sentryDocumentTitle_1.default title={(0, locale_1.t)('Alert %s', alertId)} orgSlug={organization.slug} projectSlug={project}/>
        <header_1.default hasIncidentDetailsError={hasError} params={params} incident={incident} stats={stats} onSubscriptionChange={this.handleSubscriptionChange} onStatusChange={this.handleStatusChange}/>
        <body_1.default {...this.props} incident={incident} stats={stats}/>
      </react_1.Fragment>);
    }
}
exports.default = (0, withApi_1.default)(IncidentDetails);
//# sourceMappingURL=index.jsx.map