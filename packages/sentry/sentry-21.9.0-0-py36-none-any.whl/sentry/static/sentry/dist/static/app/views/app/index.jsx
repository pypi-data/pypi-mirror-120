Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_keydown_1 = (0, tslib_1.__importDefault)(require("react-keydown"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const prop_types_1 = (0, tslib_1.__importDefault)(require("prop-types"));
const deployPreview_1 = require("app/actionCreators/deployPreview");
const guides_1 = require("app/actionCreators/guides");
const modal_1 = require("app/actionCreators/modal");
const alertActions_1 = (0, tslib_1.__importDefault)(require("app/actions/alertActions"));
const api_1 = require("app/api");
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const globalModal_1 = (0, tslib_1.__importDefault)(require("app/components/globalModal"));
const hookOrDefault_1 = (0, tslib_1.__importDefault)(require("app/components/hookOrDefault"));
const indicators_1 = (0, tslib_1.__importDefault)(require("app/components/indicators"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const constants_1 = require("app/constants");
const locale_1 = require("app/locale");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const hookStore_1 = (0, tslib_1.__importDefault)(require("app/stores/hookStore"));
const organizationsStore_1 = (0, tslib_1.__importDefault)(require("app/stores/organizationsStore"));
const organizationStore_1 = (0, tslib_1.__importDefault)(require("app/stores/organizationStore"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const withConfig_1 = (0, tslib_1.__importDefault)(require("app/utils/withConfig"));
const newsletterConsent_1 = (0, tslib_1.__importDefault)(require("app/views/newsletterConsent"));
const systemAlerts_1 = (0, tslib_1.__importDefault)(require("./systemAlerts"));
const GlobalNotifications = (0, hookOrDefault_1.default)({
    hookName: 'component:global-notifications',
    defaultComponent: () => null,
});
function getAlertTypeForProblem(problem) {
    switch (problem.severity) {
        case 'critical':
            return 'error';
        default:
            return 'warning';
    }
}
class App extends react_1.Component {
    constructor() {
        var _a, _b, _c;
        super(...arguments);
        this.state = {
            loading: false,
            error: false,
            needsUpgrade: ((_a = configStore_1.default.get('user')) === null || _a === void 0 ? void 0 : _a.isSuperuser) && configStore_1.default.get('needsUpgrade'),
            newsletterConsentPrompt: (_c = (_b = configStore_1.default.get('user')) === null || _b === void 0 ? void 0 : _b.flags) === null || _c === void 0 ? void 0 : _c.newsletter_consent_prompt,
        };
        this.mainContainerRef = (0, react_1.createRef)();
        this.unlistener = organizationStore_1.default.listen(state => this.setState({ organization: state.organization }), undefined);
        this.onConfigured = () => this.setState({ needsUpgrade: false });
        // this is somewhat hackish
        this.handleNewsletterConsent = () => this.setState({
            newsletterConsentPrompt: false,
        });
        this.handleGlobalModalClose = () => {
            var _a;
            if (typeof ((_a = this.mainContainerRef.current) === null || _a === void 0 ? void 0 : _a.focus) === 'function') {
                // Focus the main container to get hotkeys to keep working after modal closes
                this.mainContainerRef.current.focus();
            }
        };
    }
    getChildContext() {
        return {
            location: this.props.location,
        };
    }
    componentDidMount() {
        this.props.api.request('/organizations/', {
            query: {
                member: '1',
            },
            success: data => {
                organizationsStore_1.default.load(data);
                this.setState({
                    loading: false,
                });
            },
            error: () => {
                this.setState({
                    loading: false,
                    error: true,
                });
            },
        });
        this.props.api.request('/internal/health/', {
            success: data => {
                if (data && data.problems) {
                    data.problems.forEach(problem => {
                        alertActions_1.default.addAlert({
                            id: problem.id,
                            message: problem.message,
                            type: getAlertTypeForProblem(problem),
                            url: problem.url,
                        });
                    });
                }
            },
            error: () => { }, // TODO: do something?
        });
        configStore_1.default.get('messages').forEach(msg => {
            alertActions_1.default.addAlert({
                message: msg.message,
                type: msg.level,
                neverExpire: true,
            });
        });
        if (constants_1.DEPLOY_PREVIEW_CONFIG) {
            (0, deployPreview_1.displayDeployPreviewAlert)();
        }
        else if (constants_1.EXPERIMENTAL_SPA) {
            (0, deployPreview_1.displayExperimentalSpaAlert)();
        }
        (0, api_1.initApiClientErrorHandling)();
        const user = configStore_1.default.get('user');
        if (user) {
            hookStore_1.default.get('analytics:init-user').map(cb => cb(user));
        }
        (0, guides_1.fetchGuides)();
    }
    componentDidUpdate(prevProps) {
        const { config } = this.props;
        if (!(0, isEqual_1.default)(config, prevProps.config)) {
            this.handleConfigStoreChange(config);
        }
    }
    componentWillUnmount() {
        var _a;
        organizationsStore_1.default.load([]);
        (_a = this.unlistener) === null || _a === void 0 ? void 0 : _a.call(this);
    }
    handleConfigStoreChange(config) {
        const newState = {};
        if (config.needsUpgrade !== undefined) {
            newState.needsUpgrade = config.needsUpgrade;
        }
        if (config.user !== undefined) {
            newState.user = config.user;
        }
        if (Object.keys(newState).length > 0) {
            this.setState(newState);
        }
    }
    openCommandPalette(e) {
        (0, modal_1.openCommandPalette)();
        e.preventDefault();
        e.stopPropagation();
    }
    toggleDarkMode() {
        configStore_1.default.set('theme', configStore_1.default.get('theme') === 'light' ? 'dark' : 'light');
    }
    renderBody() {
        const { needsUpgrade, newsletterConsentPrompt } = this.state;
        if (needsUpgrade) {
            const InstallWizard = (0, react_1.lazy)(() => Promise.resolve().then(() => (0, tslib_1.__importStar)(require('app/views/admin/installWizard'))));
            return (<react_1.Suspense fallback={null}>
          <InstallWizard onConfigured={this.onConfigured}/>;
        </react_1.Suspense>);
        }
        if (newsletterConsentPrompt) {
            return <newsletterConsent_1.default onSubmitSuccess={this.handleNewsletterConsent}/>;
        }
        return this.props.children;
    }
    render() {
        if (this.state.loading) {
            return (<loadingIndicator_1.default triangle>
          {(0, locale_1.t)('Getting a list of all of your organizations.')}
        </loadingIndicator_1.default>);
        }
        return (<MainContainer tabIndex={-1} ref={this.mainContainerRef}>
        <globalModal_1.default onClose={this.handleGlobalModalClose}/>
        <systemAlerts_1.default className="messages-container"/>
        <GlobalNotifications className="notifications-container messages-container" organization={this.state.organization}/>
        <indicators_1.default className="indicators-container"/>
        <errorBoundary_1.default>{this.renderBody()}</errorBoundary_1.default>
      </MainContainer>);
    }
}
App.childContextTypes = {
    location: prop_types_1.default.object,
};
(0, tslib_1.__decorate)([
    (0, react_keydown_1.default)('meta+shift+p', 'meta+k', 'ctrl+shift+p', 'ctrl+k')
], App.prototype, "openCommandPalette", null);
(0, tslib_1.__decorate)([
    (0, react_keydown_1.default)('meta+shift+l', 'ctrl+shift+l')
], App.prototype, "toggleDarkMode", null);
exports.default = (0, withApi_1.default)((0, withConfig_1.default)(App));
const MainContainer = (0, styled_1.default)('div') `
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  outline: none;
  padding-top: ${p => (configStore_1.default.get('demoMode') ? p.theme.demo.headerSize : 0)};
`;
//# sourceMappingURL=index.jsx.map