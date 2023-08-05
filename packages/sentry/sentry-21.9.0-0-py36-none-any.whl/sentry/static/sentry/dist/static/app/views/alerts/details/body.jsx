Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const styles_1 = require("app/components/charts/styles");
const duration_1 = (0, tslib_1.__importDefault)(require("app/components/duration"));
const keyValueTable_1 = require("app/components/keyValueTable");
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const navTabs_1 = (0, tslib_1.__importDefault)(require("app/components/navTabs"));
const panels_1 = require("app/components/panels");
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const seenByList_1 = (0, tslib_1.__importDefault)(require("app/components/seenByList"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const organization_1 = require("app/styles/organization");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const projects_1 = (0, tslib_1.__importDefault)(require("app/utils/projects"));
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const index_1 = require("app/views/alerts/details/index");
const constants_1 = require("app/views/alerts/incidentRules/constants");
const presets_1 = require("app/views/alerts/incidentRules/presets");
const types_1 = require("app/views/alerts/incidentRules/types");
const types_2 = require("../types");
const utils_2 = require("../utils");
const activity_1 = (0, tslib_1.__importDefault)(require("./activity"));
const chart_1 = (0, tslib_1.__importDefault)(require("./chart"));
class DetailsBody extends react_1.Component {
    get metricPreset() {
        const { incident } = this.props;
        return incident ? (0, utils_2.getIncidentMetricPreset)(incident) : undefined;
    }
    /**
     * Return a string describing the threshold based on the threshold and the type
     */
    getThresholdText(value, thresholdType, isAlert = false) {
        if (!(0, utils_1.defined)(value)) {
            return '';
        }
        const isAbove = thresholdType === types_1.AlertRuleThresholdType.ABOVE;
        const direction = isAbove === isAlert ? '>' : '<';
        return `${direction} ${value}`;
    }
    renderRuleDetails() {
        var _a, _b, _c, _d, _e, _f, _g, _h, _j, _k;
        const { incident } = this.props;
        if (incident === undefined) {
            return <placeholder_1.default height="200px"/>;
        }
        const criticalTrigger = incident === null || incident === void 0 ? void 0 : incident.alertRule.triggers.find(({ label }) => label === 'critical');
        const warningTrigger = incident === null || incident === void 0 ? void 0 : incident.alertRule.triggers.find(({ label }) => label === 'warning');
        return (<keyValueTable_1.KeyValueTable>
        <keyValueTable_1.KeyValueTableRow keyName={(0, locale_1.t)('Data Source')} value={utils_2.DATA_SOURCE_LABELS[(_a = incident.alertRule) === null || _a === void 0 ? void 0 : _a.dataset]}/>
        <keyValueTable_1.KeyValueTableRow keyName={(0, locale_1.t)('Metric')} value={(_b = incident.alertRule) === null || _b === void 0 ? void 0 : _b.aggregate}/>
        <keyValueTable_1.KeyValueTableRow keyName={(0, locale_1.t)('Time Window')} value={incident && <duration_1.default seconds={incident.alertRule.timeWindow * 60}/>}/>
        {((_c = incident.alertRule) === null || _c === void 0 ? void 0 : _c.query) && (<keyValueTable_1.KeyValueTableRow keyName={(0, locale_1.t)('Filter')} value={<span title={(_d = incident.alertRule) === null || _d === void 0 ? void 0 : _d.query}>{(_e = incident.alertRule) === null || _e === void 0 ? void 0 : _e.query}</span>}/>)}
        <keyValueTable_1.KeyValueTableRow keyName={(0, locale_1.t)('Critical Trigger')} value={this.getThresholdText(criticalTrigger === null || criticalTrigger === void 0 ? void 0 : criticalTrigger.alertThreshold, (_f = incident.alertRule) === null || _f === void 0 ? void 0 : _f.thresholdType, true)}/>
        {(0, utils_1.defined)(warningTrigger) && (<keyValueTable_1.KeyValueTableRow keyName={(0, locale_1.t)('Warning Trigger')} value={this.getThresholdText(warningTrigger === null || warningTrigger === void 0 ? void 0 : warningTrigger.alertThreshold, (_g = incident.alertRule) === null || _g === void 0 ? void 0 : _g.thresholdType, true)}/>)}

        {(0, utils_1.defined)((_h = incident.alertRule) === null || _h === void 0 ? void 0 : _h.resolveThreshold) && (<keyValueTable_1.KeyValueTableRow keyName={(0, locale_1.t)('Resolution')} value={this.getThresholdText((_j = incident.alertRule) === null || _j === void 0 ? void 0 : _j.resolveThreshold, (_k = incident.alertRule) === null || _k === void 0 ? void 0 : _k.thresholdType)}/>)}
      </keyValueTable_1.KeyValueTable>);
    }
    renderChartHeader() {
        var _a, _b, _c, _d, _e;
        const { incident } = this.props;
        const alertRule = incident === null || incident === void 0 ? void 0 : incident.alertRule;
        return (<ChartHeader>
        <div>
          {(_b = (_a = this.metricPreset) === null || _a === void 0 ? void 0 : _a.name) !== null && _b !== void 0 ? _b : (0, locale_1.t)('Custom metric')}
          <ChartParameters>
            {(0, locale_1.tct)('Metric: [metric] over [window]', {
                metric: <code>{(_c = alertRule === null || alertRule === void 0 ? void 0 : alertRule.aggregate) !== null && _c !== void 0 ? _c : '\u2026'}</code>,
                window: (<code>
                  {incident ? (<duration_1.default seconds={incident.alertRule.timeWindow * 60}/>) : ('\u2026')}
                </code>),
            })}
            {((alertRule === null || alertRule === void 0 ? void 0 : alertRule.query) || ((_d = incident === null || incident === void 0 ? void 0 : incident.alertRule) === null || _d === void 0 ? void 0 : _d.dataset)) &&
                (0, locale_1.tct)('Filter: [datasetType] [filter]', {
                    datasetType: ((_e = incident === null || incident === void 0 ? void 0 : incident.alertRule) === null || _e === void 0 ? void 0 : _e.dataset) && (<code>{constants_1.DATASET_EVENT_TYPE_FILTERS[incident.alertRule.dataset]}</code>),
                    filter: (alertRule === null || alertRule === void 0 ? void 0 : alertRule.query) && <code>{alertRule.query}</code>,
                })}
          </ChartParameters>
        </div>
      </ChartHeader>);
    }
    renderChartActions() {
        const { incident, params, stats } = this.props;
        return (
        // Currently only one button in pannel, hide panel if not available
        <feature_1.default features={['discover-basic']}>
        <ChartActions>
          <projects_1.default slugs={incident === null || incident === void 0 ? void 0 : incident.projects} orgId={params.orgId}>
            {({ initiallyLoaded, fetching, projects }) => {
                const preset = this.metricPreset;
                const ctaOpts = {
                    orgSlug: params.orgId,
                    projects: (initiallyLoaded ? projects : []),
                    incident,
                    stats,
                };
                const _a = preset
                    ? preset.makeCtaParams(ctaOpts)
                    : (0, presets_1.makeDefaultCta)(ctaOpts), { buttonText } = _a, props = (0, tslib_1.__rest)(_a, ["buttonText"]);
                return (<button_1.default size="small" priority="primary" disabled={!incident || fetching || !initiallyLoaded} {...props}>
                  {buttonText}
                </button_1.default>);
            }}
          </projects_1.default>
        </ChartActions>
      </feature_1.default>);
    }
    render() {
        var _a, _b;
        const { params, incident, organization, stats } = this.props;
        const hasRedesign = (incident === null || incident === void 0 ? void 0 : incident.alertRule) &&
            !(0, utils_2.isIssueAlert)(incident === null || incident === void 0 ? void 0 : incident.alertRule) &&
            organization.features.includes('alert-details-redesign');
        const alertRuleLink = hasRedesign && incident
            ? (0, index_1.alertDetailsLink)(organization, incident)
            : `/organizations/${params.orgId}/alerts/metric-rules/${incident === null || incident === void 0 ? void 0 : incident.projects[0]}/${(_a = incident === null || incident === void 0 ? void 0 : incident.alertRule) === null || _a === void 0 ? void 0 : _a.id}/`;
        return (<StyledPageContent>
        <Main>
          {incident &&
                incident.status === types_2.IncidentStatus.CLOSED &&
                incident.statusMethod === types_2.IncidentStatusMethod.RULE_UPDATED && (<AlertWrapper>
                <alert_1.default type="warning" icon={<icons_1.IconWarning size="sm"/>}>
                  {(0, locale_1.t)('This alert has been auto-resolved because the rule that triggered it has been modified or deleted')}
                </alert_1.default>
              </AlertWrapper>)}
          <organization_1.PageContent>
            <ChartPanel>
              <panels_1.PanelBody withPadding>
                {this.renderChartHeader()}
                {incident && stats ? (<chart_1.default triggers={incident.alertRule.triggers} resolveThreshold={incident.alertRule.resolveThreshold} aggregate={incident.alertRule.aggregate} data={stats.eventStats.data} started={incident.dateStarted} closed={incident.dateClosed || undefined}/>) : (<placeholder_1.default height="200px"/>)}
              </panels_1.PanelBody>
              {this.renderChartActions()}
            </ChartPanel>
          </organization_1.PageContent>
          <DetailWrapper>
            <ActivityPageContent>
              <StyledNavTabs underlined>
                <li className="active">
                  <link_1.default to="">{(0, locale_1.t)('Activity')}</link_1.default>
                </li>

                <SeenByTab>
                  {incident && (<StyledSeenByList iconPosition="right" seenBy={incident.seenBy} iconTooltip={(0, locale_1.t)('People who have viewed this alert')}/>)}
                </SeenByTab>
              </StyledNavTabs>
              <activity_1.default incident={incident} params={params} incidentStatus={!!incident ? incident.status : null}/>
            </ActivityPageContent>
            <Sidebar>
              <SidebarHeading>
                <span>{(0, locale_1.t)('Alert Rule')}</span>
                {(((_b = incident === null || incident === void 0 ? void 0 : incident.alertRule) === null || _b === void 0 ? void 0 : _b.status) !== types_2.AlertRuleStatus.SNAPSHOT ||
                hasRedesign) && (<SideHeaderLink disabled={!!(incident === null || incident === void 0 ? void 0 : incident.id)} to={(incident === null || incident === void 0 ? void 0 : incident.id)
                    ? {
                        pathname: alertRuleLink,
                    }
                    : ''}>
                    {(0, locale_1.t)('View Alert Rule')}
                  </SideHeaderLink>)}
              </SidebarHeading>
              {this.renderRuleDetails()}
            </Sidebar>
          </DetailWrapper>
        </Main>
      </StyledPageContent>);
    }
}
exports.default = DetailsBody;
const Main = (0, styled_1.default)('div') `
  background-color: ${p => p.theme.background};
  padding-top: ${(0, space_1.default)(3)};
  flex-grow: 1;
`;
const DetailWrapper = (0, styled_1.default)('div') `
  display: flex;
  flex: 1;

  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    flex-direction: column-reverse;
  }
`;
const ActivityPageContent = (0, styled_1.default)(organization_1.PageContent) `
  @media (max-width: ${theme_1.default.breakpoints[0]}) {
    width: 100%;
    margin-bottom: 0;
  }
`;
const Sidebar = (0, styled_1.default)(organization_1.PageContent) `
  width: 400px;
  flex: none;
  padding-top: ${(0, space_1.default)(3)};

  @media (max-width: ${theme_1.default.breakpoints[0]}) {
    width: 100%;
    padding-top: ${(0, space_1.default)(3)};
    margin-bottom: 0;
    border-bottom: 1px solid ${p => p.theme.border};
  }
`;
const SidebarHeading = (0, styled_1.default)(styles_1.SectionHeading) `
  display: flex;
  justify-content: space-between;
`;
const SideHeaderLink = (0, styled_1.default)(link_1.default) `
  font-weight: normal;
`;
const StyledPageContent = (0, styled_1.default)(organization_1.PageContent) `
  padding: 0;
  flex-direction: column;
`;
const ChartPanel = (0, styled_1.default)(panels_1.Panel) ``;
const ChartHeader = (0, styled_1.default)('header') `
  margin-bottom: ${(0, space_1.default)(1)};
`;
const ChartActions = (0, styled_1.default)(panels_1.PanelFooter) `
  display: flex;
  justify-content: flex-end;
  padding: ${(0, space_1.default)(2)};
`;
const ChartParameters = (0, styled_1.default)('div') `
  color: ${p => p.theme.subText};
  font-size: ${p => p.theme.fontSizeMedium};
  display: grid;
  grid-auto-flow: column;
  grid-auto-columns: max-content;
  grid-gap: ${(0, space_1.default)(4)};
  align-items: center;
  overflow-x: auto;

  > * {
    position: relative;
  }

  > *:not(:last-of-type):after {
    content: '';
    display: block;
    height: 70%;
    width: 1px;
    background: ${p => p.theme.gray200};
    position: absolute;
    right: -${(0, space_1.default)(2)};
    top: 15%;
  }
`;
const AlertWrapper = (0, styled_1.default)('div') `
  padding: ${(0, space_1.default)(2)} ${(0, space_1.default)(4)} 0;
`;
const StyledNavTabs = (0, styled_1.default)(navTabs_1.default) `
  display: flex;
`;
const SeenByTab = (0, styled_1.default)('li') `
  flex: 1;
  margin-left: ${(0, space_1.default)(2)};
  margin-right: 0;

  .nav-tabs > & {
    margin-right: 0;
  }
`;
const StyledSeenByList = (0, styled_1.default)(seenByList_1.default) `
  margin-top: 0;
`;
//# sourceMappingURL=body.jsx.map