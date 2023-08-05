Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const analytics_1 = require("app/utils/analytics");
const withTeams_1 = (0, tslib_1.__importDefault)(require("app/utils/withTeams"));
const constants_1 = require("app/views/alerts/incidentRules/constants");
const ruleForm_1 = (0, tslib_1.__importDefault)(require("./ruleForm"));
/**
 * Show metric rules form with an empty rule. Redirects to alerts list after creation.
 */
class IncidentRulesCreate extends react_1.Component {
    constructor() {
        super(...arguments);
        this.handleSubmitSuccess = () => {
            const { router } = this.props;
            const { orgId } = this.props.params;
            analytics_1.metric.endTransaction({ name: 'saveAlertRule' });
            router.push(`/organizations/${orgId}/alerts/rules/`);
        };
    }
    render() {
        var _a;
        const _b = this.props, { project, eventView, wizardTemplate, sessionId, teams } = _b, props = (0, tslib_1.__rest)(_b, ["project", "eventView", "wizardTemplate", "sessionId", "teams"]);
        const defaultRule = eventView
            ? (0, constants_1.createRuleFromEventView)(eventView)
            : wizardTemplate
                ? (0, constants_1.createRuleFromWizardTemplate)(wizardTemplate)
                : (0, constants_1.createDefaultRule)();
        const userTeamIds = teams.filter(({ isMember }) => isMember).map(({ id }) => id);
        const projectTeamIds = new Set(project.teams.map(({ id }) => id));
        const defaultOwnerId = (_a = userTeamIds.find(id => projectTeamIds.has(id))) !== null && _a !== void 0 ? _a : null;
        defaultRule.owner = defaultOwnerId && `team:${defaultOwnerId}`;
        return (<ruleForm_1.default onSubmitSuccess={this.handleSubmitSuccess} rule={Object.assign(Object.assign({}, defaultRule), { projects: [project.slug] })} sessionId={sessionId} project={project} userTeamIds={userTeamIds} {...props}/>);
    }
}
exports.default = (0, withTeams_1.default)(IncidentRulesCreate);
//# sourceMappingURL=create.jsx.map