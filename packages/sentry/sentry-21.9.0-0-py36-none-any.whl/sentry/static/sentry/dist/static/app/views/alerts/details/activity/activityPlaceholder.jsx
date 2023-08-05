Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const item_1 = (0, tslib_1.__importDefault)(require("app/components/activity/item"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
exports.default = (0, react_1.withTheme)(function ActivityPlaceholder(props) {
    return (<item_1.default bubbleProps={{
            backgroundColor: props.theme.backgroundSecondary,
            borderColor: props.theme.backgroundSecondary,
        }}>
      {() => <Placeholder />}
    </item_1.default>);
});
const Placeholder = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(4)};
`;
//# sourceMappingURL=activityPlaceholder.jsx.map