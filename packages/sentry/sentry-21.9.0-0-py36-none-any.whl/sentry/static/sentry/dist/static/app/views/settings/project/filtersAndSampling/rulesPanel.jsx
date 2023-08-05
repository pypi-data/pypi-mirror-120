Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const buttonBar_1 = (0, tslib_1.__importDefault)(require("app/components/buttonBar"));
const panels_1 = require("app/components/panels");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const rules_1 = (0, tslib_1.__importDefault)(require("./rules"));
const utils_1 = require("./utils");
function RulesPanel({ rules, onAddRule, onEditRule, onDeleteRule, disabled, onUpdateRules, isErrorPanel, }) {
    const panelType = isErrorPanel ? (0, locale_1.t)('error') : (0, locale_1.t)('transaction');
    return (<panels_1.Panel>
      <rules_1.default rules={rules} onEditRule={onEditRule} onDeleteRule={onDeleteRule} disabled={disabled} onUpdateRules={onUpdateRules} emptyMessage={(0, locale_1.t)('There are no %s rules to display', panelType)}/>
      <StyledPanelFooter>
        <buttonBar_1.default gap={1}>
          <button_1.default href={utils_1.DYNAMIC_SAMPLING_DOC_LINK} external>
            {(0, locale_1.t)('Read the docs')}
          </button_1.default>
          <button_1.default priority="primary" onClick={onAddRule} disabled={disabled} title={disabled
            ? (0, locale_1.t)('You do not have permission to add dynamic sampling rules.')
            : undefined}>
            {(0, locale_1.t)('Add %s rule', panelType)}
          </button_1.default>
        </buttonBar_1.default>
      </StyledPanelFooter>
    </panels_1.Panel>);
}
exports.default = RulesPanel;
const StyledPanelFooter = (0, styled_1.default)(panels_1.PanelFooter) `
  padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(2)};
  display: flex;
  align-items: center;
  justify-content: flex-end;
`;
//# sourceMappingURL=rulesPanel.jsx.map