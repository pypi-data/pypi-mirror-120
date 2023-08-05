Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const styles_1 = require("./styles");
const getTimeTooltipTitle = (displayRelativeTime) => {
    if (displayRelativeTime) {
        return (0, locale_1.t)('Switch to absolute');
    }
    return (0, locale_1.t)('Switch to relative');
};
const ListHeader = (0, react_1.memo)(({ onSwitchTimeFormat, displayRelativeTime }) => (<react_1.Fragment>
    <StyledGridCell>{(0, locale_1.t)('Type')}</StyledGridCell>
    <Category>{(0, locale_1.t)('Category')}</Category>
    <StyledGridCell>{(0, locale_1.t)('Description')}</StyledGridCell>
    <StyledGridCell>{(0, locale_1.t)('Level')}</StyledGridCell>
    <Time onClick={onSwitchTimeFormat}>
      <tooltip_1.default title={getTimeTooltipTitle(displayRelativeTime)}>
        <StyledIconSwitch size="xs"/>
      </tooltip_1.default>
      <span> {(0, locale_1.t)('Time')}</span>
    </Time>
  </react_1.Fragment>));
exports.default = ListHeader;
const StyledGridCell = (0, styled_1.default)(styles_1.GridCell) `
  position: sticky;
  z-index: ${p => p.theme.zIndex.breadcrumbs.header};
  top: 0;
  border-bottom: 1px solid ${p => p.theme.border};
  background: ${p => p.theme.backgroundSecondary};
  color: ${p => p.theme.subText};
  font-weight: 600;
  text-transform: uppercase;
  line-height: 1;
  font-size: ${p => p.theme.fontSizeExtraSmall};

  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    padding: ${(0, space_1.default)(2)} ${(0, space_1.default)(2)};
    font-size: ${p => p.theme.fontSizeSmall};
  }
`;
const Category = (0, styled_1.default)(StyledGridCell) `
  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    padding-left: ${(0, space_1.default)(1)};
  }
`;
const Time = (0, styled_1.default)(StyledGridCell) `
  display: grid;
  grid-template-columns: max-content 1fr;
  grid-gap: ${(0, space_1.default)(1)};
  cursor: pointer;
`;
const StyledIconSwitch = (0, styled_1.default)(icons_1.IconSwitch) `
  transition: 0.15s color;
  &:hover {
    color: ${p => p.theme.gray300};
  }
`;
//# sourceMappingURL=listHeader.jsx.map