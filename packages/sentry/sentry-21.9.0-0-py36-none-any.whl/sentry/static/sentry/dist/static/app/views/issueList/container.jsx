Object.defineProperty(exports, "__esModule", { value: true });
exports.IssueListContainer = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_document_title_1 = (0, tslib_1.__importDefault)(require("react-document-title"));
const lightWeightNoProjectMessage_1 = (0, tslib_1.__importDefault)(require("app/components/lightWeightNoProjectMessage"));
const globalSelectionHeader_1 = (0, tslib_1.__importDefault)(require("app/components/organizations/globalSelectionHeader"));
const analytics_1 = require("app/utils/analytics");
const withOrganization_1 = (0, tslib_1.__importStar)(require("app/utils/withOrganization"));
class IssueListContainer extends react_1.Component {
    componentDidMount() {
        // Setup here as render() may be expensive
        this.startMetricCollection();
    }
    /**
     * The user can (1) land on IssueList as the first page as they enter Sentry,
     * or (2) navigate into IssueList with the stores preloaded with data.
     *
     * Case (1) will be slower and we can easily identify it as it uses the
     * lightweight organization
     */
    startMetricCollection() {
        const isLightWeight = (0, withOrganization_1.isLightweightOrganization)(this.props.organization);
        const startType = isLightWeight ? 'cold-start' : 'warm-start';
        analytics_1.metric.mark({ name: 'page-issue-list-start', data: { start_type: startType } });
    }
    getTitle() {
        return `Issues - ${this.props.organization.slug} - Sentry`;
    }
    render() {
        const { organization, children } = this.props;
        return (<react_document_title_1.default title={this.getTitle()}>
        <globalSelectionHeader_1.default>
          <lightWeightNoProjectMessage_1.default organization={organization}>
            {children}
          </lightWeightNoProjectMessage_1.default>
        </globalSelectionHeader_1.default>
      </react_document_title_1.default>);
    }
}
exports.IssueListContainer = IssueListContainer;
exports.default = (0, withOrganization_1.default)(IssueListContainer);
//# sourceMappingURL=container.jsx.map