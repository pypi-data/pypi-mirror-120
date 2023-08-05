Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const noProjectMessage_1 = (0, tslib_1.__importDefault)(require("app/components/noProjectMessage"));
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
class LightWeightNoProjectMessage extends react_1.Component {
    render() {
        const { organization, projects, loadingProjects } = this.props;
        return (<noProjectMessage_1.default {...this.props} projects={projects} loadingProjects={!('projects' in organization) && loadingProjects}/>);
    }
}
exports.default = (0, withProjects_1.default)(LightWeightNoProjectMessage);
//# sourceMappingURL=lightWeightNoProjectMessage.jsx.map