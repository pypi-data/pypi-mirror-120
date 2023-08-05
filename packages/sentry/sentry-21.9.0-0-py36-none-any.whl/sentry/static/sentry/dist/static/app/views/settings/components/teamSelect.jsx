Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const debounce_1 = (0, tslib_1.__importDefault)(require("lodash/debounce"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const confirm_1 = (0, tslib_1.__importDefault)(require("app/components/confirm"));
const dropdownAutoComplete_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownAutoComplete"));
const dropdownButton_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownButton"));
const teamBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge/teamBadge"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const panels_1 = require("app/components/panels");
const constants_1 = require("app/constants");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
class TeamSelect extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            loading: true,
            teamsSearch: null,
        };
        this.fetchTeams = (0, debounce_1.default)((query) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, organization } = this.props;
            const teamsSearch = yield api.requestPromise(`/organizations/${organization.slug}/teams/`, {
                query: { query, per_page: constants_1.TEAMS_PER_PAGE },
            });
            this.setState({ teamsSearch, loading: false });
        }), constants_1.DEFAULT_DEBOUNCE_DURATION);
        this.handleQueryUpdate = (event) => {
            this.setState({ loading: true });
            this.fetchTeams(event.target.value);
        };
        this.handleAddTeam = (option) => {
            var _a;
            const team = (_a = this.state.teamsSearch) === null || _a === void 0 ? void 0 : _a.find(tm => tm.slug === option.value);
            if (team) {
                this.props.onAddTeam(team);
            }
        };
        this.handleRemove = (teamSlug) => {
            this.props.onRemoveTeam(teamSlug);
        };
    }
    componentDidMount() {
        this.fetchTeams();
    }
    renderTeamAddDropDown() {
        const { disabled, selectedTeams, menuHeader } = this.props;
        const { teamsSearch } = this.state;
        const isDisabled = disabled;
        let options = [];
        if (teamsSearch === null || teamsSearch.length === 0) {
            options = [];
        }
        else {
            options = teamsSearch
                .filter(team => !selectedTeams.some(selectedTeam => selectedTeam.slug === team.slug))
                .map((team, index) => ({
                index,
                value: team.slug,
                searchKey: team.slug,
                label: <DropdownTeamBadge avatarSize={18} team={team}/>,
            }));
        }
        return (<dropdownAutoComplete_1.default items={options} busyItemsStillVisible={this.state.loading} onChange={this.handleQueryUpdate} onSelect={this.handleAddTeam} emptyMessage={(0, locale_1.t)('No teams')} menuHeader={menuHeader} disabled={isDisabled} alignMenu="right">
        {({ isOpen }) => (<dropdownButton_1.default aria-label={(0, locale_1.t)('Add Team')} isOpen={isOpen} size="xsmall" disabled={isDisabled}>
            {(0, locale_1.t)('Add Team')}
          </dropdownButton_1.default>)}
      </dropdownAutoComplete_1.default>);
    }
    renderBody() {
        const { organization, selectedTeams, disabled, confirmLastTeamRemoveMessage } = this.props;
        if (selectedTeams.length === 0) {
            return <emptyMessage_1.default>{(0, locale_1.t)('No Teams assigned')}</emptyMessage_1.default>;
        }
        const confirmMessage = selectedTeams.length === 1 && confirmLastTeamRemoveMessage
            ? confirmLastTeamRemoveMessage
            : null;
        return selectedTeams.map(team => (<TeamRow key={team.slug} orgId={organization.slug} team={team} onRemove={this.handleRemove} disabled={disabled} confirmMessage={confirmMessage}/>));
    }
    render() {
        return (<panels_1.Panel>
        <panels_1.PanelHeader hasButtons>
          {(0, locale_1.t)('Team')}
          {this.renderTeamAddDropDown()}
        </panels_1.PanelHeader>

        <panels_1.PanelBody>{this.renderBody()}</panels_1.PanelBody>
      </panels_1.Panel>);
    }
}
const TeamRow = ({ orgId, team, onRemove, disabled, confirmMessage }) => (<TeamPanelItem>
    <StyledLink to={`/settings/${orgId}/teams/${team.slug}/`}>
      <teamBadge_1.default team={team}/>
    </StyledLink>
    <confirm_1.default message={confirmMessage} bypass={!confirmMessage} onConfirm={() => onRemove(team.slug)} disabled={disabled}>
      <button_1.default size="xsmall" icon={<icons_1.IconSubtract isCircled size="xs"/>} disabled={disabled}>
        {(0, locale_1.t)('Remove')}
      </button_1.default>
    </confirm_1.default>
  </TeamPanelItem>);
const DropdownTeamBadge = (0, styled_1.default)(teamBadge_1.default) `
  font-weight: normal;
  font-size: ${p => p.theme.fontSizeMedium};
  text-transform: none;
`;
const TeamPanelItem = (0, styled_1.default)(panels_1.PanelItem) `
  padding: ${(0, space_1.default)(2)};
  align-items: center;
`;
const StyledLink = (0, styled_1.default)(link_1.default) `
  flex: 1;
  margin-right: ${(0, space_1.default)(1)};
`;
exports.default = (0, withApi_1.default)(TeamSelect);
//# sourceMappingURL=teamSelect.jsx.map