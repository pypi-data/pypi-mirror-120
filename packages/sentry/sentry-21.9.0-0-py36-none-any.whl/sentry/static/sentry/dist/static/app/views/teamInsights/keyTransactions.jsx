Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const table_1 = (0, tslib_1.__importDefault)(require("app/views/performance/table"));
function TeamKeyTransactions({ organization, projects, location, period, start, end, }) {
    const eventView = eventView_1.default.fromSavedQuery({
        id: undefined,
        name: 'Performance',
        query: 'transaction.duration:<15m team_key_transaction:true',
        projects: projects.map(project => Number(project.id)),
        version: 2,
        orderby: '-tpm',
        range: period,
        start,
        end,
        fields: [
            'team_key_transaction',
            'transaction',
            'project',
            'tpm()',
            'p50()',
            'p95()',
            'failure_rate()',
            'apdex()',
            'count_unique(user)',
            'count_miserable(user)',
            'user_misery()',
        ],
    });
    return (<table_1.default eventView={eventView} projects={projects} organization={organization} location={location} setError={() => { }} summaryConditions={eventView.getQueryWithAdditionalConditions()}/>);
}
exports.default = TeamKeyTransactions;
//# sourceMappingURL=keyTransactions.jsx.map