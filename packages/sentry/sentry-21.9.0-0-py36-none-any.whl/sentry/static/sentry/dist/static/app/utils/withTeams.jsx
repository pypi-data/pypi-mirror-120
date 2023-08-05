Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const teamStore_1 = (0, tslib_1.__importDefault)(require("app/stores/teamStore"));
const getDisplayName_1 = (0, tslib_1.__importDefault)(require("app/utils/getDisplayName"));
/**
 * Higher order component that uses TeamStore and provides a list of teams
 */
function withTeams(WrappedComponent) {
    class WithTeams extends React.Component {
        constructor() {
            super(...arguments);
            this.state = {
                teams: teamStore_1.default.getAll(),
            };
            this.unsubscribe = teamStore_1.default.listen(() => this.setState({ teams: teamStore_1.default.getAll() }), undefined);
        }
        componentWillUnmount() {
            this.unsubscribe();
        }
        render() {
            return (<WrappedComponent teams={this.state.teams} {...this.props}/>);
        }
    }
    WithTeams.displayName = `withTeams(${(0, getDisplayName_1.default)(WrappedComponent)})`;
    return WithTeams;
}
exports.default = withTeams;
//# sourceMappingURL=withTeams.jsx.map