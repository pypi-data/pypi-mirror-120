Object.defineProperty(exports, "__esModule", { value: true });
exports.LightWeightOrganizationDetails = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_router_1 = require("react-router");
const organizations_1 = require("app/actionCreators/organizations");
const alertActions_1 = (0, tslib_1.__importDefault)(require("app/actions/alertActions"));
const api_1 = require("app/api");
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const footer_1 = (0, tslib_1.__importDefault)(require("app/components/footer"));
const thirds_1 = require("app/components/layouts/thirds");
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const getRouteStringFromRoutes_1 = (0, tslib_1.__importDefault)(require("app/utils/getRouteStringFromRoutes"));
const withOrganization_1 = (0, tslib_1.__importDefault)(require("app/utils/withOrganization"));
const organizationContext_1 = (0, tslib_1.__importDefault)(require("app/views/organizationContext"));
function DeletionInProgress({ organization }) {
    return (<thirds_1.Body>
      <thirds_1.Main>
        <alert_1.default type="warning" icon={<icons_1.IconWarning />}>
          {(0, locale_1.tct)('The [organization] organization is currently in the process of being deleted from Sentry.', {
            organization: <strong>{organization.slug}</strong>,
        })}
        </alert_1.default>
      </thirds_1.Main>
    </thirds_1.Body>);
}
class DeletionPending extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = { submitInProgress: false };
        this.api = new api_1.Client();
        this.onRestore = () => {
            if (this.state.submitInProgress) {
                return;
            }
            this.setState({ submitInProgress: true });
            this.api.request(`/organizations/${this.props.organization.slug}/`, {
                method: 'PUT',
                data: { cancelDeletion: true },
                success: () => {
                    window.location.reload();
                },
                error: () => {
                    alertActions_1.default.addAlert({
                        message: 'We were unable to restore this organization. Please try again or contact support.',
                        type: 'error',
                    });
                    this.setState({ submitInProgress: false });
                },
            });
        };
    }
    componentWillUnmount() {
        this.api.clear();
    }
    render() {
        const { organization } = this.props;
        const access = new Set(organization.access);
        return (<thirds_1.Body>
        <thirds_1.Main>
          <h3>{(0, locale_1.t)('Deletion Scheduled')}</h3>
          <p>
            {(0, locale_1.tct)('The [organization] organization is currently scheduled for deletion.', {
                organization: <strong>{organization.slug}</strong>,
            })}
          </p>

          {access.has('org:admin') ? (<div>
              <p>
                {(0, locale_1.t)('Would you like to cancel this process and restore the organization back to the original state?')}
              </p>
              <p>
                <button_1.default priority="primary" onClick={this.onRestore} disabled={this.state.submitInProgress}>
                  {(0, locale_1.t)('Restore Organization')}
                </button_1.default>
              </p>
            </div>) : (<p>
              {(0, locale_1.t)('If this is a mistake, contact an organization owner and ask them to restore this organization.')}
            </p>)}
          <p>
            <small>
              {(0, locale_1.t)("Note: Restoration is available until the process begins. Once it does, there's no recovering the data that has been removed.")}
            </small>
          </p>
        </thirds_1.Main>
      </thirds_1.Body>);
    }
}
const OrganizationDetailsBody = (0, withOrganization_1.default)(function OrganizationDetailsBody({ children, organization, }) {
    var _a;
    const status = (_a = organization === null || organization === void 0 ? void 0 : organization.status) === null || _a === void 0 ? void 0 : _a.id;
    if (organization && status === 'pending_deletion') {
        return <DeletionPending organization={organization}/>;
    }
    if (organization && status === 'deletion_in_progress') {
        return <DeletionInProgress organization={organization}/>;
    }
    return (<react_1.Fragment>
      <errorBoundary_1.default>{children}</errorBoundary_1.default>
      <footer_1.default />
    </react_1.Fragment>);
});
class OrganizationDetails extends react_1.Component {
    componentDidMount() {
        const { routes } = this.props;
        const isOldRoute = (0, getRouteStringFromRoutes_1.default)(routes) === '/:orgId/';
        if (isOldRoute) {
            react_router_1.browserHistory.replace(`/organizations/${this.props.params.orgId}/`);
        }
    }
    componentDidUpdate(prevProps) {
        if (prevProps.params &&
            this.props.params &&
            prevProps.params.orgId !== this.props.params.orgId) {
            (0, organizations_1.switchOrganization)();
        }
    }
    render() {
        return (<organizationContext_1.default includeSidebar useLastOrganization {...this.props}>
        <OrganizationDetailsBody {...this.props}>
          {this.props.children}
        </OrganizationDetailsBody>
      </organizationContext_1.default>);
    }
}
exports.default = OrganizationDetails;
function LightWeightOrganizationDetails(props) {
    return <OrganizationDetails detailed={false} {...props}/>;
}
exports.LightWeightOrganizationDetails = LightWeightOrganizationDetails;
//# sourceMappingURL=index.jsx.map