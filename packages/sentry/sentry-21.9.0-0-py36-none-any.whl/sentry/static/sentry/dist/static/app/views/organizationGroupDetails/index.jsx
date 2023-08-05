Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const analytics_1 = require("app/utils/analytics");
const withGlobalSelection_1 = (0, tslib_1.__importDefault)(require("app/utils/withGlobalSelection"));
const withOrganization_1 = (0, tslib_1.__importStar)(require("app/utils/withOrganization"));
const groupDetails_1 = (0, tslib_1.__importDefault)(require("./groupDetails"));
class OrganizationGroupDetails extends React.Component {
    constructor(props) {
        super(props);
        // Setup in the constructor as render() may be expensive
        this.startMetricCollection();
    }
    componentDidMount() {
        (0, analytics_1.analytics)('issue_page.viewed', {
            group_id: parseInt(this.props.params.groupId, 10),
            org_id: parseInt(this.props.organization.id, 10),
        });
    }
    /**
     * See "page-issue-list-start" for explanation on hot/cold-starts
     */
    startMetricCollection() {
        const startType = (0, withOrganization_1.isLightweightOrganization)(this.props.organization)
            ? 'cold-start'
            : 'warm-start';
        analytics_1.metric.mark({ name: 'page-issue-details-start', data: { start_type: startType } });
    }
    render() {
        const _a = this.props, { selection } = _a, props = (0, tslib_1.__rest)(_a, ["selection"]);
        return (<groupDetails_1.default key={`${this.props.params.groupId}-envs:${selection.environments.join(',')}`} environments={selection.environments} {...props}/>);
    }
}
exports.default = (0, withOrganization_1.default)((0, withGlobalSelection_1.default)(OrganizationGroupDetails));
//# sourceMappingURL=index.jsx.map