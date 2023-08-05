Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const projectsStore_1 = (0, tslib_1.__importDefault)(require("app/stores/projectsStore"));
const getDisplayName_1 = (0, tslib_1.__importDefault)(require("app/utils/getDisplayName"));
/**
 * Higher order component that takes specificProjectSlugs and provides list of that projects from ProjectsStore
 */
function withProjectsSpecified(WrappedComponent) {
    class WithProjectsSpecified extends React.Component {
        constructor() {
            super(...arguments);
            this.state = projectsStore_1.default.getState(this.props.specificProjectSlugs);
            this.unsubscribe = projectsStore_1.default.listen(() => {
                const storeState = projectsStore_1.default.getState(this.props.specificProjectSlugs);
                if (!(0, isEqual_1.default)(this.state, storeState)) {
                    this.setState(storeState);
                }
            }, undefined);
        }
        static getDerivedStateFromProps(nextProps) {
            return projectsStore_1.default.getState(nextProps.specificProjectSlugs);
        }
        componentWillUnmount() {
            this.unsubscribe();
        }
        render() {
            return (<WrappedComponent {...this.props} projects={this.state.projects} loadingProjects={this.state.loading}/>);
        }
    }
    WithProjectsSpecified.displayName = `withProjectsSpecified(${(0, getDisplayName_1.default)(WrappedComponent)})`;
    return WithProjectsSpecified;
}
exports.default = withProjectsSpecified;
//# sourceMappingURL=withProjectsSpecified.jsx.map