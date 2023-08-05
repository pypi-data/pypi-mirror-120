Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const types_1 = require("./types");
const Status = ({ className, incident, disableIconColor }) => {
    const { status } = incident;
    const isResolved = status === types_1.IncidentStatus.CLOSED;
    const isWarning = status === types_1.IncidentStatus.WARNING;
    const icon = isResolved ? (<icons_1.IconCheckmark color={disableIconColor ? undefined : 'green300'}/>) : isWarning ? (<icons_1.IconWarning color={disableIconColor ? undefined : 'orange400'}/>) : (<icons_1.IconFire color={disableIconColor ? undefined : 'red300'}/>);
    const text = isResolved ? (0, locale_1.t)('Resolved') : isWarning ? (0, locale_1.t)('Warning') : (0, locale_1.t)('Critical');
    return (<Wrapper className={className}>
      <Icon>{icon}</Icon>
      {text}
    </Wrapper>);
};
exports.default = Status;
const Wrapper = (0, styled_1.default)('div') `
  display: grid;
  grid-auto-flow: column;
  align-items: center;
  grid-template-columns: auto 1fr;
  grid-gap: ${(0, space_1.default)(0.75)};
`;
const Icon = (0, styled_1.default)('span') `
  margin-bottom: -3px;
`;
//# sourceMappingURL=status.jsx.map