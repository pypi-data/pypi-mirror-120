Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const is_prop_valid_1 = (0, tslib_1.__importDefault)(require("@emotion/is-prop-valid"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const autoSelectText_1 = (0, tslib_1.__importDefault)(require("app/components/autoSelectText"));
const ShortId = (_a) => {
    var { shortId, avatar } = _a, props = (0, tslib_1.__rest)(_a, ["shortId", "avatar"]);
    if (!shortId) {
        return null;
    }
    return (<StyledShortId {...props}>
      {avatar}
      <StyledAutoSelectText avatar={!!avatar}>{shortId}</StyledAutoSelectText>
    </StyledShortId>);
};
const StyledShortId = (0, styled_1.default)('div') `
  font-family: ${p => p.theme.text.familyMono};
  display: flex;
  align-items: center;
  justify-content: flex-end;
`;
const StyledAutoSelectText = (0, styled_1.default)(autoSelectText_1.default, { shouldForwardProp: is_prop_valid_1.default }) `
  margin-left: ${p => p.avatar && '0.5em'};
  min-width: 0;
`;
exports.default = ShortId;
//# sourceMappingURL=shortId.jsx.map