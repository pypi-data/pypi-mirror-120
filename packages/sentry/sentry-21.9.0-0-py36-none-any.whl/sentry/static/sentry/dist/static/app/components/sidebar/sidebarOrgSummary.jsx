Object.defineProperty(exports, "__esModule", { value: true });
exports.OrgSummary = void 0;
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const organizationAvatar_1 = (0, tslib_1.__importDefault)(require("app/components/avatar/organizationAvatar"));
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const SidebarOrgSummary = ({ organization }) => {
    const fullOrg = organization;
    const projects = fullOrg.projects && fullOrg.projects.length;
    const extra = [];
    if (projects) {
        extra.push((0, locale_1.tn)('%s project', '%s projects', projects));
    }
    return (<OrgSummary>
      <organizationAvatar_1.default organization={organization} size={36}/>

      <Details>
        <SummaryOrgName>{organization.name}</SummaryOrgName>
        {!!extra.length && <SummaryOrgDetails>{extra.join(', ')}</SummaryOrgDetails>}
      </Details>
    </OrgSummary>);
};
const OrgSummary = (0, styled_1.default)('div') `
  display: flex;
  padding: 10px 15px;
  overflow: hidden;
`;
exports.OrgSummary = OrgSummary;
const SummaryOrgName = (0, styled_1.default)('div') `
  color: ${p => p.theme.textColor};
  font-size: 16px;
  line-height: 1.1;
  font-weight: bold;
  margin-bottom: 4px;
  ${overflowEllipsis_1.default};
`;
const SummaryOrgDetails = (0, styled_1.default)('div') `
  color: ${p => p.theme.subText};
  font-size: 14px;
  line-height: 1;
  ${overflowEllipsis_1.default};
`;
const Details = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
  justify-content: center;

  padding-left: 10px;
  overflow: hidden;
`;
exports.default = SidebarOrgSummary;
//# sourceMappingURL=sidebarOrgSummary.jsx.map