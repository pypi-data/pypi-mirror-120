Object.defineProperty(exports, "__esModule", { value: true });
exports.SidebarWrapper = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_router_1 = require("react-router");
const react_1 = require("@emotion/react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const queryString = (0, tslib_1.__importStar)(require("query-string"));
const preferences_1 = require("app/actionCreators/preferences");
const sidebarPanelActions_1 = (0, tslib_1.__importDefault)(require("app/actions/sidebarPanelActions"));
const feature_1 = (0, tslib_1.__importDefault)(require("app/components/acl/feature"));
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const hookOrDefault_1 = (0, tslib_1.__importDefault)(require("app/components/hookOrDefault"));
const utils_1 = require("app/components/organizations/globalSelectionHeader/utils");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const hookStore_1 = (0, tslib_1.__importDefault)(require("app/stores/hookStore"));
const preferencesStore_1 = (0, tslib_1.__importDefault)(require("app/stores/preferencesStore"));
const sidebarPanelStore_1 = (0, tslib_1.__importDefault)(require("app/stores/sidebarPanelStore"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const urls_1 = require("app/utils/discover/urls");
const theme_1 = (0, tslib_1.__importDefault)(require("app/utils/theme"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const broadcasts_1 = (0, tslib_1.__importDefault)(require("./broadcasts"));
const help_1 = (0, tslib_1.__importDefault)(require("./help"));
const onboardingStatus_1 = (0, tslib_1.__importDefault)(require("./onboardingStatus"));
const serviceIncidents_1 = (0, tslib_1.__importDefault)(require("./serviceIncidents"));
const sidebarDropdown_1 = (0, tslib_1.__importDefault)(require("./sidebarDropdown"));
const sidebarItem_1 = (0, tslib_1.__importDefault)(require("./sidebarItem"));
const types_1 = require("./types");
const SidebarOverride = (0, hookOrDefault_1.default)({
    hookName: 'sidebar:item-override',
    defaultComponent: ({ children }) => <React.Fragment>{children({})}</React.Fragment>,
});
class Sidebar extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            horizontal: false,
        };
        this.mq = null;
        this.sidebarRef = React.createRef();
        this.toggleSidebar = () => {
            const { collapsed } = this.props;
            if (!collapsed) {
                (0, preferences_1.hideSidebar)();
            }
            else {
                (0, preferences_1.showSidebar)();
            }
        };
        this.checkHash = () => {
            if (window.location.hash === '#welcome') {
                this.togglePanel(types_1.SidebarPanelKey.OnboardingWizard);
            }
        };
        this.handleMediaQueryChange = (changed) => {
            this.setState({
                horizontal: changed.matches,
            });
        };
        this.togglePanel = (panel) => sidebarPanelActions_1.default.togglePanel(panel);
        this.hidePanel = () => sidebarPanelActions_1.default.hidePanel();
        // Keep the global selection querystring values in the path
        this.navigateWithGlobalSelection = (pathname, evt) => {
            var _a;
            const globalSelectionRoutes = [
                'alerts',
                'alerts/rules',
                'dashboards',
                'issues',
                'releases',
                'user-feedback',
                'discover',
                'discover/results',
                'performance',
            ].map(route => `/organizations/${this.props.organization.slug}/${route}/`);
            // Only keep the querystring if the current route matches one of the above
            if (globalSelectionRoutes.includes(pathname)) {
                const query = (0, utils_1.extractSelectionParameters)((_a = this.props.location) === null || _a === void 0 ? void 0 : _a.query);
                // Handle cmd-click (mac) and meta-click (linux)
                if (evt.metaKey) {
                    const q = queryString.stringify(query);
                    evt.currentTarget.href = `${evt.currentTarget.href}?${q}`;
                    return;
                }
                evt.preventDefault();
                react_router_1.browserHistory.push({ pathname, query });
            }
            this.hidePanel();
        };
        if (!window.matchMedia) {
            return;
        }
        // TODO(billy): We should consider moving this into a component
        this.mq = window.matchMedia(`(max-width: ${theme_1.default.breakpoints[1]})`);
        this.mq.addListener(this.handleMediaQueryChange);
        this.state.horizontal = this.mq.matches;
    }
    componentDidMount() {
        document.body.classList.add('body-sidebar');
        this.checkHash();
        this.doCollapse(this.props.collapsed);
    }
    // Sidebar doesn't use children, so don't use it to compare
    // Also ignore location, will re-render when routes change (instead of query params)
    //
    // NOTE(epurkhiser): The comment above is why I added `children?: never` as a
    // type to this component. I'm not sure the implications of removing this so
    // I've just left it for now.
    shouldComponentUpdate(_a, nextState) {
        var { children: _children, location: _location } = _a, nextPropsToCompare = (0, tslib_1.__rest)(_a, ["children", "location"]);
        const _b = this.props, { children: _childrenCurrent, location: _locationCurrent } = _b, currentPropsToCompare = (0, tslib_1.__rest)(_b, ["children", "location"]);
        return (!(0, isEqual_1.default)(currentPropsToCompare, nextPropsToCompare) ||
            !(0, isEqual_1.default)(this.state, nextState));
    }
    componentDidUpdate(prevProps) {
        var _a;
        const { collapsed, location } = this.props;
        // Close active panel if we navigated anywhere
        if ((location === null || location === void 0 ? void 0 : location.pathname) !== ((_a = prevProps.location) === null || _a === void 0 ? void 0 : _a.pathname)) {
            this.hidePanel();
        }
        // Collapse
        if (collapsed !== prevProps.collapsed) {
            this.doCollapse(collapsed);
        }
    }
    componentWillUnmount() {
        document.body.classList.remove('body-sidebar');
        if (this.mq) {
            this.mq.removeListener(this.handleMediaQueryChange);
            this.mq = null;
        }
    }
    doCollapse(collapsed) {
        if (collapsed) {
            document.body.classList.add('collapsed');
        }
        else {
            document.body.classList.remove('collapsed');
        }
    }
    render() {
        const { activePanel, organization, collapsed } = this.props;
        const { horizontal } = this.state;
        const config = configStore_1.default.getConfig();
        const user = configStore_1.default.get('user');
        const hasPanel = !!activePanel;
        const orientation = horizontal ? 'top' : 'left';
        const sidebarItemProps = {
            orientation,
            collapsed,
            hasPanel,
        };
        const hasOrganization = !!organization;
        const projects = hasOrganization && (<sidebarItem_1.default {...sidebarItemProps} index onClick={this.hidePanel} icon={<icons_1.IconProject size="md"/>} label={<guideAnchor_1.default target="projects">{(0, locale_1.t)('Projects')}</guideAnchor_1.default>} to={`/organizations/${organization.slug}/projects/`} id="projects"/>);
        const issues = hasOrganization && (<sidebarItem_1.default {...sidebarItemProps} onClick={(_id, evt) => this.navigateWithGlobalSelection(`/organizations/${organization.slug}/issues/`, evt)} icon={<icons_1.IconIssues size="md"/>} label={<guideAnchor_1.default target="issues">{(0, locale_1.t)('Issues')}</guideAnchor_1.default>} to={`/organizations/${organization.slug}/issues/`} id="issues"/>);
        const discover2 = hasOrganization && (<feature_1.default hookName="feature-disabled:discover2-sidebar-item" features={['discover-basic']} organization={organization}>
        <sidebarItem_1.default {...sidebarItemProps} onClick={(_id, evt) => this.navigateWithGlobalSelection((0, urls_1.getDiscoverLandingUrl)(organization), evt)} icon={<icons_1.IconTelescope size="md"/>} label={<guideAnchor_1.default target="discover">{(0, locale_1.t)('Discover')}</guideAnchor_1.default>} to={(0, urls_1.getDiscoverLandingUrl)(organization)} id="discover-v2"/>
      </feature_1.default>);
        const performance = hasOrganization && (<feature_1.default hookName="feature-disabled:performance-sidebar-item" features={['performance-view']} organization={organization}>
        <SidebarOverride id="performance-override">
          {(overideProps) => (<sidebarItem_1.default {...sidebarItemProps} onClick={(_id, evt) => this.navigateWithGlobalSelection(`/organizations/${organization.slug}/performance/`, evt)} icon={<icons_1.IconLightning size="md"/>} label={<guideAnchor_1.default target="performance">{(0, locale_1.t)('Performance')}</guideAnchor_1.default>} to={`/organizations/${organization.slug}/performance/`} id="performance" {...overideProps}/>)}
        </SidebarOverride>
      </feature_1.default>);
        const releases = hasOrganization && (<sidebarItem_1.default {...sidebarItemProps} onClick={(_id, evt) => this.navigateWithGlobalSelection(`/organizations/${organization.slug}/releases/`, evt)} icon={<icons_1.IconReleases size="md"/>} label={<guideAnchor_1.default target="releases">{(0, locale_1.t)('Releases')}</guideAnchor_1.default>} to={`/organizations/${organization.slug}/releases/`} id="releases"/>);
        const userFeedback = hasOrganization && (<sidebarItem_1.default {...sidebarItemProps} onClick={(_id, evt) => this.navigateWithGlobalSelection(`/organizations/${organization.slug}/user-feedback/`, evt)} icon={<icons_1.IconSupport size="md"/>} label={(0, locale_1.t)('User Feedback')} to={`/organizations/${organization.slug}/user-feedback/`} id="user-feedback"/>);
        const alerts = hasOrganization && (<feature_1.default features={['incidents', 'alert-details-redesign']} requireAll={false}>
        {({ features }) => {
                const hasIncidents = features.includes('incidents');
                const hasAlertList = features.includes('alert-details-redesign');
                const alertsPath = hasIncidents && !hasAlertList
                    ? `/organizations/${organization.slug}/alerts/`
                    : `/organizations/${organization.slug}/alerts/rules/`;
                return (<sidebarItem_1.default {...sidebarItemProps} onClick={(_id, evt) => this.navigateWithGlobalSelection(alertsPath, evt)} icon={<icons_1.IconSiren size="md"/>} label={(0, locale_1.t)('Alerts')} to={alertsPath} id="alerts"/>);
            }}
      </feature_1.default>);
        const monitors = hasOrganization && (<feature_1.default features={['monitors']} organization={organization}>
        <sidebarItem_1.default {...sidebarItemProps} onClick={(_id, evt) => this.navigateWithGlobalSelection(`/organizations/${organization.slug}/monitors/`, evt)} icon={<icons_1.IconLab size="md"/>} label={(0, locale_1.t)('Monitors')} to={`/organizations/${organization.slug}/monitors/`} id="monitors"/>
      </feature_1.default>);
        const dashboards = hasOrganization && (<feature_1.default hookName="feature-disabled:dashboards-sidebar-item" features={['discover', 'discover-query', 'dashboards-basic', 'dashboards-edit']} organization={organization} requireAll={false}>
        <sidebarItem_1.default {...sidebarItemProps} index onClick={(_id, evt) => this.navigateWithGlobalSelection(`/organizations/${organization.slug}/dashboards/`, evt)} icon={<icons_1.IconGraph size="md"/>} label={(0, locale_1.t)('Dashboards')} to={`/organizations/${organization.slug}/dashboards/`} id="customizable-dashboards" isNew/>
      </feature_1.default>);
        const activity = hasOrganization && (<sidebarItem_1.default {...sidebarItemProps} onClick={this.hidePanel} icon={<icons_1.IconActivity size="md"/>} label={(0, locale_1.t)('Activity')} to={`/organizations/${organization.slug}/activity/`} id="activity"/>);
        const stats = hasOrganization && (<sidebarItem_1.default {...sidebarItemProps} onClick={this.hidePanel} icon={<icons_1.IconStats size="md"/>} label={(0, locale_1.t)('Stats')} to={`/organizations/${organization.slug}/stats/`} id="stats"/>);
        const settings = hasOrganization && (<sidebarItem_1.default {...sidebarItemProps} onClick={this.hidePanel} icon={<icons_1.IconSettings size="md"/>} label={(0, locale_1.t)('Settings')} to={`/settings/${organization.slug}/`} id="settings"/>);
        return (<exports.SidebarWrapper ref={this.sidebarRef} collapsed={collapsed}>
        <SidebarSectionGroupPrimary>
          <SidebarSection>
            <sidebarDropdown_1.default orientation={orientation} collapsed={collapsed} org={organization} user={user} config={config}/>
          </SidebarSection>

          <PrimaryItems>
            {hasOrganization && (<React.Fragment>
                <SidebarSection>
                  {projects}
                  {issues}
                  {performance}
                  {releases}
                  {userFeedback}
                  {alerts}
                  {discover2}
                </SidebarSection>

                <SidebarSection>
                  {dashboards}
                  {monitors}
                </SidebarSection>

                <SidebarSection>
                  {activity}
                  {stats}
                </SidebarSection>

                <SidebarSection>{settings}</SidebarSection>
              </React.Fragment>)}
          </PrimaryItems>
        </SidebarSectionGroupPrimary>

        {hasOrganization && (<SidebarSectionGroup>
            <SidebarSection noMargin noPadding>
              <onboardingStatus_1.default org={organization} currentPanel={activePanel} onShowPanel={() => this.togglePanel(types_1.SidebarPanelKey.OnboardingWizard)} hidePanel={this.hidePanel} {...sidebarItemProps}/>
            </SidebarSection>

            <SidebarSection>
              {hookStore_1.default.get('sidebar:bottom-items').length > 0 &&
                    hookStore_1.default.get('sidebar:bottom-items')[0](Object.assign({ organization }, sidebarItemProps))}
              <help_1.default orientation={orientation} collapsed={collapsed} hidePanel={this.hidePanel} organization={organization}/>
              <broadcasts_1.default orientation={orientation} collapsed={collapsed} currentPanel={activePanel} onShowPanel={() => this.togglePanel(types_1.SidebarPanelKey.Broadcasts)} hidePanel={this.hidePanel} organization={organization}/>
              <serviceIncidents_1.default orientation={orientation} collapsed={collapsed} currentPanel={activePanel} onShowPanel={() => this.togglePanel(types_1.SidebarPanelKey.StatusUpdate)} hidePanel={this.hidePanel}/>
            </SidebarSection>

            {!horizontal && (<SidebarSection>
                <SidebarCollapseItem id="collapse" data-test-id="sidebar-collapse" {...sidebarItemProps} icon={<StyledIconChevron collapsed={collapsed}/>} label={collapsed ? (0, locale_1.t)('Expand') : (0, locale_1.t)('Collapse')} onClick={this.toggleSidebar}/>
              </SidebarSection>)}
          </SidebarSectionGroup>)}
      </exports.SidebarWrapper>);
    }
}
class SidebarContainer extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            collapsed: preferencesStore_1.default.getInitialState().collapsed,
            activePanel: '',
        };
        this.preferenceUnsubscribe = preferencesStore_1.default.listen((preferences) => this.onPreferenceChange(preferences), undefined);
        this.sidebarUnsubscribe = sidebarPanelStore_1.default.listen((activePanel) => this.onSidebarPanelChange(activePanel), undefined);
    }
    componentWillUnmount() {
        this.preferenceUnsubscribe();
        this.sidebarUnsubscribe();
    }
    onPreferenceChange(preferences) {
        if (preferences.collapsed === this.state.collapsed) {
            return;
        }
        this.setState({ collapsed: preferences.collapsed });
    }
    onSidebarPanelChange(activePanel) {
        this.setState({ activePanel });
    }
    render() {
        const { activePanel, collapsed } = this.state;
        return <Sidebar {...this.props} {...{ activePanel, collapsed }}/>;
    }
}
exports.default = (0, withOrganization_1.default)(SidebarContainer);
const responsiveFlex = (0, react_1.css) `
  display: flex;
  flex-direction: column;

  @media (max-width: ${theme_1.default.breakpoints[1]}) {
    flex-direction: row;
  }
`;
exports.SidebarWrapper = (0, styled_1.default)('div') `
  background: ${p => p.theme.sidebar.background};
  background: ${p => p.theme.sidebarGradient};
  color: ${p => p.theme.sidebar.color};
  line-height: 1;
  padding: 12px 0 2px; /* Allows for 32px avatars  */
  width: ${p => p.theme.sidebar.expandedWidth};
  position: fixed;
  top: ${p => (configStore_1.default.get('demoMode') ? p.theme.demo.headerSize : 0)};
  left: 0;
  bottom: 0;
  justify-content: space-between;
  z-index: ${p => p.theme.zIndex.sidebar};
  ${responsiveFlex};
  ${p => p.collapsed && `width: ${p.theme.sidebar.collapsedWidth};`};

  @media (max-width: ${p => p.theme.breakpoints[1]}) {
    top: 0;
    left: 0;
    right: 0;
    height: ${p => p.theme.sidebar.mobileHeight};
    bottom: auto;
    width: auto;
    padding: 0 ${(0, space_1.default)(1)};
    align-items: center;
  }
`;
const SidebarSectionGroup = (0, styled_1.default)('div') `
  ${responsiveFlex};
  flex-shrink: 0; /* prevents shrinking on Safari */
`;
const SidebarSectionGroupPrimary = (0, styled_1.default)('div') `
  ${responsiveFlex};
  /* necessary for child flexing on msedge and ff */
  min-height: 0;
  min-width: 0;
  flex: 1;
  /* expand to fill the entire height on mobile */
  @media (max-width: ${p => p.theme.breakpoints[1]}) {
    height: 100%;
    align-items: center;
  }
`;
const PrimaryItems = (0, styled_1.default)('div') `
  overflow: auto;
  flex: 1;
  display: flex;
  flex-direction: column;
  -ms-overflow-style: -ms-autohiding-scrollbar;
  @media (max-height: 675px) and (min-width: ${p => p.theme.breakpoints[1]}) {
    border-bottom: 1px solid ${p => p.theme.gray400};
    padding-bottom: ${(0, space_1.default)(1)};
    box-shadow: rgba(0, 0, 0, 0.15) 0px -10px 10px inset;
    &::-webkit-scrollbar {
      background-color: transparent;
      width: 8px;
    }
    &::-webkit-scrollbar-thumb {
      background: ${p => p.theme.gray400};
      border-radius: 8px;
    }
  }
  @media (max-width: ${p => p.theme.breakpoints[1]}) {
    overflow-y: visible;
    flex-direction: row;
    height: 100%;
    align-items: center;
    border-right: 1px solid ${p => p.theme.gray400};
    padding-right: ${(0, space_1.default)(1)};
    margin-right: ${(0, space_1.default)(0.5)};
    box-shadow: rgba(0, 0, 0, 0.15) -10px 0px 10px inset;
    ::-webkit-scrollbar {
      display: none;
    }
  }
`;
const SidebarSection = (0, styled_1.default)(SidebarSectionGroup) `
  ${p => !p.noMargin && `margin: ${(0, space_1.default)(1)} 0`};
  ${p => !p.noPadding && 'padding: 0 19px'};

  @media (max-width: ${p => p.theme.breakpoints[0]}) {
    margin: 0;
    padding: 0;
  }

  &:empty {
    display: none;
  }
`;
const ExpandedIcon = (0, react_1.css) `
  transition: 0.3s transform ease;
  transform: rotate(270deg);
`;
const CollapsedIcon = (0, react_1.css) `
  transform: rotate(90deg);
`;
const StyledIconChevron = (0, styled_1.default)((_a) => {
    var { collapsed } = _a, props = (0, tslib_1.__rest)(_a, ["collapsed"]);
    return (<icons_1.IconChevron direction="left" size="md" isCircled css={[ExpandedIcon, collapsed && CollapsedIcon]} {...props}/>);
}) ``;
const SidebarCollapseItem = (0, styled_1.default)(sidebarItem_1.default) `
  @media (max-width: ${p => p.theme.breakpoints[1]}) {
    display: none;
  }
`;
//# sourceMappingURL=index.jsx.map