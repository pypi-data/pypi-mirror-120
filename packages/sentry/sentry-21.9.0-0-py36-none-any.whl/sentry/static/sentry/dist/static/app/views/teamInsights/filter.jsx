Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const dropdownButton_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownButton"));
const dropdownControl_1 = (0, tslib_1.__importStar)(require("app/components/dropdownControl"));
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
function FilterSection({ label, items, toggleFilter }) {
    return (<react_1.Fragment>
      <Header>
        <span>{label}</span>
      </Header>
      {items
            .filter(item => !item.filtered)
            .map(item => (<ListItem key={item.value} isChecked={item.checked} onClick={() => {
                toggleFilter(item.value);
            }}>
            <TeamName>{item.label}</TeamName>
          </ListItem>))}
    </react_1.Fragment>);
}
class Filter extends react_1.Component {
    constructor() {
        super(...arguments);
        this.toggleFilter = (value) => {
            const { onFilterChange } = this.props;
            onFilterChange(value);
        };
    }
    render() {
        const { dropdownSection, header } = this.props;
        const selected = this.props.dropdownSection.items.find(item => item.checked);
        const dropDownButtonProps = {
            priority: 'default',
            hasDarkBorderBottomColor: false,
        };
        return (<dropdownControl_1.default menuWidth="240px" blendWithActor alwaysRenderMenu={false} button={({ isOpen, getActorProps }) => (<StyledDropdownButton {...getActorProps()} isOpen={isOpen} hasDarkBorderBottomColor={dropDownButtonProps.hasDarkBorderBottomColor} priority={dropDownButtonProps.priority} data-test-id="filter-button">
            {(0, locale_1.t)('Team: ')}
            {selected === null || selected === void 0 ? void 0 : selected.label}
          </StyledDropdownButton>)}>
        {({ isOpen, getMenuProps }) => (<MenuContent {...getMenuProps()} isOpen={isOpen} blendCorner alignMenu="left" width="240px">
            <List>
              {header}
              <FilterSection {...dropdownSection} toggleFilter={this.toggleFilter}/>
            </List>
          </MenuContent>)}
      </dropdownControl_1.default>);
    }
}
const MenuContent = (0, styled_1.default)(dropdownControl_1.Content) `
  max-height: 290px;
  overflow-y: auto;
`;
const Header = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: auto min-content;
  grid-column-gap: ${(0, space_1.default)(1)};
  align-items: center;

  margin: 0;
  background-color: ${p => p.theme.backgroundSecondary};
  color: ${p => p.theme.gray300};
  font-weight: normal;
  font-size: ${p => p.theme.fontSizeMedium};
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  border-bottom: 1px solid ${p => p.theme.border};
`;
const StyledDropdownButton = (0, styled_1.default)(dropdownButton_1.default) `
  white-space: nowrap;
  max-width: 200px;
  height: 42px;

  z-index: ${p => p.theme.zIndex.dropdown};
`;
const List = (0, styled_1.default)('ul') `
  list-style: none;
  margin: 0;
  padding: 0;
`;
const ListItem = (0, styled_1.default)('li') `
  display: grid;
  grid-template-columns: 1fr max-content;
  grid-column-gap: ${(0, space_1.default)(1)};
  align-items: center;
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  border-bottom: 1px solid ${p => p.theme.border};
  cursor: pointer;
  :hover {
    background-color: ${p => p.theme.backgroundSecondary};
  }

  &:hover span {
    color: ${p => p.theme.blue300};
    text-decoration: underline;
  }
`;
const TeamName = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeMedium};
  ${overflowEllipsis_1.default};
`;
exports.default = Filter;
//# sourceMappingURL=filter.jsx.map