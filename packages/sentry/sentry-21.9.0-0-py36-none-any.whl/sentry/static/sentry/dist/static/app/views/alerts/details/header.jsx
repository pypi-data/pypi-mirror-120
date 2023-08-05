Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const is_prop_valid_1 = (0, tslib_1.__importDefault)(require("@emotion/is-prop-valid"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const breadcrumbs_1 = (0, tslib_1.__importDefault)(require("app/components/breadcrumbs"));
const count_1 = (0, tslib_1.__importDefault)(require("app/components/count"));
const dropdownControl_1 = (0, tslib_1.__importDefault)(require("app/components/dropdownControl"));
const duration_1 = (0, tslib_1.__importDefault)(require("app/components/duration"));
const projectBadge_1 = (0, tslib_1.__importDefault)(require("app/components/idBadge/projectBadge"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const menuItem_1 = (0, tslib_1.__importDefault)(require("app/components/menuItem"));
const pageHeading_1 = (0, tslib_1.__importDefault)(require("app/components/pageHeading"));
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const subscribeButton_1 = (0, tslib_1.__importDefault)(require("app/components/subscribeButton"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const organization_1 = require("app/styles/organization");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const dates_1 = require("app/utils/dates");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const projects_1 = (0, tslib_1.__importDefault)(require("app/utils/projects"));
const types_1 = require("app/views/alerts/incidentRules/types");
const status_1 = (0, tslib_1.__importDefault)(require("../status"));
const utils_1 = require("../utils");
class DetailsHeader extends React.Component {
    renderStatus() {
        const { incident, onStatusChange } = this.props;
        const isIncidentOpen = incident && (0, utils_1.isOpen)(incident);
        const statusLabel = incident ? <StyledStatus incident={incident}/> : null;
        return (<dropdownControl_1.default data-test-id="status-dropdown" label={statusLabel} alignRight blendWithActor={false} buttonProps={{
                size: 'small',
                disabled: !incident || !isIncidentOpen,
                hideBottomBorder: false,
            }}>
        <StatusMenuItem isActive>
          {incident && <status_1.default disableIconColor incident={incident}/>}
        </StatusMenuItem>
        <StatusMenuItem onSelect={onStatusChange}>
          <icons_1.IconCheckmark color="green300"/>
          {(0, locale_1.t)('Resolved')}
        </StatusMenuItem>
      </dropdownControl_1.default>);
    }
    render() {
        var _a, _b, _c;
        const { hasIncidentDetailsError, incident, params, stats, onSubscriptionChange } = this.props;
        const isIncidentReady = !!incident && !hasIncidentDetailsError;
        // ex - Wed, May 27, 2020 11:09 AM
        const dateFormat = (0, dates_1.use24Hours)() ? 'ddd, MMM D, YYYY HH:mm' : 'llll';
        const dateStarted = incident && (0, moment_1.default)(new Date(incident.dateStarted)).format(dateFormat);
        const duration = incident &&
            (0, moment_1.default)(incident.dateClosed ? new Date(incident.dateClosed) : new Date()).diff((0, moment_1.default)(new Date(incident.dateStarted)), 'seconds');
        const isErrorDataset = ((_a = incident === null || incident === void 0 ? void 0 : incident.alertRule) === null || _a === void 0 ? void 0 : _a.dataset) === types_1.Dataset.ERRORS;
        const environmentLabel = (_c = (_b = incident === null || incident === void 0 ? void 0 : incident.alertRule) === null || _b === void 0 ? void 0 : _b.environment) !== null && _c !== void 0 ? _c : (0, locale_1.t)('All Environments');
        const project = incident && incident.projects && incident.projects[0];
        return (<Header>
        <BreadCrumbBar>
          <AlertBreadcrumbs crumbs={[
                { label: (0, locale_1.t)('Alerts'), to: `/organizations/${params.orgId}/alerts/` },
                { label: incident && `#${incident.id}` },
            ]}/>
          <Controls>
            <subscribeButton_1.default disabled={!isIncidentReady} isSubscribed={incident === null || incident === void 0 ? void 0 : incident.isSubscribed} onClick={onSubscriptionChange} size="small"/>
            {this.renderStatus()}
          </Controls>
        </BreadCrumbBar>
        <Details columns={isErrorDataset ? 5 : 3}>
          <div>
            <IncidentTitle data-test-id="incident-title" loading={!isIncidentReady}>
              {incident && !hasIncidentDetailsError ? incident.title : 'Loading'}
            </IncidentTitle>
            <IncidentSubTitle loading={!isIncidentReady}>
              {(0, locale_1.t)('Triggered: ')}
              {dateStarted}
            </IncidentSubTitle>
          </div>

          {hasIncidentDetailsError ? (<StyledLoadingError />) : (<GroupedHeaderItems columns={isErrorDataset ? 5 : 3}>
              <ItemTitle>{(0, locale_1.t)('Environment')}</ItemTitle>
              <ItemTitle>{(0, locale_1.t)('Project')}</ItemTitle>
              {isErrorDataset && <ItemTitle>{(0, locale_1.t)('Users affected')}</ItemTitle>}
              {isErrorDataset && <ItemTitle>{(0, locale_1.t)('Total events')}</ItemTitle>}
              <ItemTitle>{(0, locale_1.t)('Active For')}</ItemTitle>
              <ItemValue>{environmentLabel}</ItemValue>
              <ItemValue>
                {project ? (<projects_1.default slugs={[project]} orgId={params.orgId}>
                    {({ projects }) => (projects === null || projects === void 0 ? void 0 : projects.length) && (<projectBadge_1.default avatarSize={18} project={projects[0]}/>)}
                  </projects_1.default>) : (<placeholder_1.default height="25px"/>)}
              </ItemValue>
              {isErrorDataset && (<ItemValue>
                  {stats ? (<count_1.default value={stats.uniqueUsers}/>) : (<placeholder_1.default height="25px"/>)}
                </ItemValue>)}
              {isErrorDataset && (<ItemValue>
                  {stats ? (<count_1.default value={stats.totalEvents}/>) : (<placeholder_1.default height="25px"/>)}
                </ItemValue>)}
              <ItemValue>
                {incident ? (<duration_1.default seconds={(0, getDynamicText_1.default)({ value: duration || 0, fixed: 1200 })}/>) : (<placeholder_1.default height="25px"/>)}
              </ItemValue>
            </GroupedHeaderItems>)}
        </Details>
      </Header>);
    }
}
exports.default = DetailsHeader;
const Header = (0, styled_1.default)('div') `
  background-color: ${p => p.theme.backgroundSecondary};
  border-bottom: 1px solid ${p => p.theme.border};
`;
const BreadCrumbBar = (0, styled_1.default)('div') `
  display: flex;
  margin-bottom: 0;
  padding: ${(0, space_1.default)(2)} ${(0, space_1.default)(4)} ${(0, space_1.default)(1)};
`;
const AlertBreadcrumbs = (0, styled_1.default)(breadcrumbs_1.default) `
  flex-grow: 1;
  font-size: ${p => p.theme.fontSizeExtraLarge};
  padding: 0;
`;
const Controls = (0, styled_1.default)('div') `
  display: grid;
  grid-auto-flow: column;
  grid-gap: ${(0, space_1.default)(1)};
`;
const Details = (0, styled_1.default)(organization_1.PageHeader, {
    shouldForwardProp: p => typeof p === 'string' && (0, is_prop_valid_1.default)(p) && p !== 'columns',
}) `
  margin-bottom: 0;
  padding: ${(0, space_1.default)(1.5)} ${(0, space_1.default)(4)} ${(0, space_1.default)(2)};

  grid-template-columns: max-content auto;
  display: grid;
  grid-gap: ${(0, space_1.default)(3)};
  grid-auto-flow: column;

  @media (max-width: ${p => p.theme.breakpoints[p.columns === 3 ? 1 : 2]}) {
    grid-template-columns: auto;
    grid-auto-flow: row;
  }
`;
const StyledLoadingError = (0, styled_1.default)(loadingError_1.default) `
  flex: 1;

  &.alert.alert-block {
    margin: 0 20px;
  }
`;
const GroupedHeaderItems = (0, styled_1.default)('div', {
    shouldForwardProp: p => typeof p === 'string' && (0, is_prop_valid_1.default)(p) && p !== 'columns',
}) `
  display: grid;
  grid-template-columns: repeat(${p => p.columns}, max-content);
  grid-gap: ${(0, space_1.default)(1)} ${(0, space_1.default)(4)};
  text-align: right;
  margin-top: ${(0, space_1.default)(1)};

  @media (max-width: ${p => p.theme.breakpoints[p.columns === 3 ? 1 : 2]}) {
    text-align: left;
  }
`;
const ItemTitle = (0, styled_1.default)('h6') `
  font-size: ${p => p.theme.fontSizeSmall};
  margin-bottom: 0;
  text-transform: uppercase;
  color: ${p => p.theme.gray300};
  letter-spacing: 0.1px;
`;
const ItemValue = (0, styled_1.default)('div') `
  display: flex;
  justify-content: flex-end;
  align-items: center;
  font-size: ${p => p.theme.fontSizeExtraLarge};
`;
const IncidentTitle = (0, styled_1.default)(pageHeading_1.default, {
    shouldForwardProp: p => typeof p === 'string' && (0, is_prop_valid_1.default)(p) && p !== 'loading',
}) `
  ${p => p.loading && 'opacity: 0'};
  line-height: 1.5;
`;
const IncidentSubTitle = (0, styled_1.default)('div', {
    shouldForwardProp: p => typeof p === 'string' && (0, is_prop_valid_1.default)(p) && p !== 'loading',
}) `
  ${p => p.loading && 'opacity: 0'};
  font-size: ${p => p.theme.fontSizeLarge};
  color: ${p => p.theme.gray300};
`;
const StyledStatus = (0, styled_1.default)(status_1.default) `
  margin-right: ${(0, space_1.default)(2)};
`;
const StatusMenuItem = (0, styled_1.default)(menuItem_1.default) `
  > span {
    padding: ${(0, space_1.default)(1)} ${(0, space_1.default)(1.5)};
    font-size: ${p => p.theme.fontSizeSmall};
    font-weight: 600;
    line-height: 1;
    text-align: left;
    display: grid;
    grid-template-columns: max-content 1fr;
    grid-gap: ${(0, space_1.default)(0.75)};
    align-items: center;
  }
`;
//# sourceMappingURL=header.jsx.map