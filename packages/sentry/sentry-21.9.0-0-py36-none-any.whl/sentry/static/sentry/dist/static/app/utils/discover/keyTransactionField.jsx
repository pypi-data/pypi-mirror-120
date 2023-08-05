Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const performance_1 = require("app/actionCreators/performance");
const icons_1 = require("app/icons");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
class KeyTransactionField extends react_1.Component {
    constructor(props) {
        super(props);
        this.toggleKeyTransactionHandler = () => {
            const { api, organization, transactionName } = this.props;
            const { isKeyTransaction } = this.state;
            const projectId = this.getProjectId();
            // All the props are guaranteed to be not undefined at this point
            // as they have all been validated in the render method.
            (0, performance_1.toggleKeyTransaction)(api, isKeyTransaction, organization.slug, [projectId], transactionName).then(() => {
                this.setState({
                    isKeyTransaction: !isKeyTransaction,
                });
            });
        };
        this.state = {
            isKeyTransaction: !!props.isKeyTransaction,
        };
    }
    getProjectId() {
        const { projects, projectSlug } = this.props;
        const project = projects.find(proj => proj.slug === projectSlug);
        if (!project) {
            return null;
        }
        return project.id;
    }
    render() {
        const { organization, projectSlug, transactionName } = this.props;
        const { isKeyTransaction } = this.state;
        const star = (<StyledKey color={isKeyTransaction ? 'yellow300' : 'gray200'} isSolid={isKeyTransaction} data-test-id="key-transaction-column"/>);
        // All these fields need to be defined in order to toggle a key transaction
        // Since they're not defined, we just render a plain star icon with no action
        // associated with it
        if (organization === undefined ||
            projectSlug === undefined ||
            transactionName === undefined ||
            this.getProjectId() === null) {
            return star;
        }
        return <KeyColumn onClick={this.toggleKeyTransactionHandler}>{star}</KeyColumn>;
    }
}
const KeyColumn = (0, styled_1.default)('div') ``;
const StyledKey = (0, styled_1.default)(icons_1.IconStar) `
  cursor: pointer;
  vertical-align: middle;
`;
exports.default = (0, withApi_1.default)((0, withProjects_1.default)(KeyTransactionField));
//# sourceMappingURL=keyTransactionField.jsx.map