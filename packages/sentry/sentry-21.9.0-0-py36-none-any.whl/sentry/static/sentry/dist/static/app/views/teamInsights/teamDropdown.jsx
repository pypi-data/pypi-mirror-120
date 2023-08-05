Object.defineProperty(exports, "__esModule", { value: true });
exports.getTeamParams = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const input_1 = (0, tslib_1.__importDefault)(require("app/components/forms/input"));
const locale_1 = require("app/locale");
const filter_1 = (0, tslib_1.__importDefault)(require("./filter"));
const ALERT_LIST_QUERY_DEFAULT_TEAMS = ['myteams', 'unassigned'];
function getTeamParams(team) {
    if (team === undefined) {
        return ALERT_LIST_QUERY_DEFAULT_TEAMS;
    }
    if (team === '') {
        return [];
    }
    if (Array.isArray(team)) {
        return team;
    }
    return [team];
}
exports.getTeamParams = getTeamParams;
function TeamDropdown({ teams, selectedTeam, handleChangeTeam }) {
    const [teamFilterSearch, setTeamFilterSearch] = (0, react_1.useState)();
    const teamItems = teams.map(({ id, name }) => ({
        label: name,
        value: id,
        filtered: teamFilterSearch
            ? !name.toLowerCase().includes(teamFilterSearch.toLowerCase())
            : false,
        checked: selectedTeam === id,
    }));
    return (<filter_1.default header={<StyledInput autoFocus placeholder={(0, locale_1.t)('Filter by team name')} onClick={event => {
                event.stopPropagation();
            }} onChange={(event) => {
                setTeamFilterSearch(event.target.value);
            }} value={teamFilterSearch || ''}/>} onFilterChange={handleChangeTeam} dropdownSection={{
            id: 'teams',
            label: (0, locale_1.t)('Teams'),
            items: teamItems,
        }}/>);
}
exports.default = TeamDropdown;
const StyledInput = (0, styled_1.default)(input_1.default) `
  border: none;
  border-bottom: 1px solid ${p => p.theme.gray200};
  border-radius: 0;
`;
//# sourceMappingURL=teamDropdown.jsx.map