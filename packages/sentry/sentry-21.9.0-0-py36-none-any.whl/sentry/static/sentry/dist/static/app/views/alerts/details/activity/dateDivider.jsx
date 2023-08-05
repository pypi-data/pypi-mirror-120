Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const DateDivider = (0, styled_1.default)('div') `
  font-size: ${p => p.theme.fontSizeMedium};
  display: flex;
  align-items: center;
  justify-content: center;
  color: ${p => p.theme.subText};
  margin: ${(0, space_1.default)(1.5)} 0;

  &:before,
  &:after {
    content: '';
    display: block;
    flex-grow: 1;
    height: 1px;
    background-color: ${p => p.theme.gray200};
  }

  &:before {
    margin-right: ${(0, space_1.default)(2)};
  }

  &:after {
    margin-left: ${(0, space_1.default)(2)};
  }
`;
exports.default = DateDivider;
//# sourceMappingURL=dateDivider.jsx.map