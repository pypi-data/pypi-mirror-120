Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const forms_1 = require("app/components/forms");
const externalLink_1 = (0, tslib_1.__importDefault)(require("app/components/links/externalLink"));
const narrowLayout_1 = (0, tslib_1.__importDefault)(require("app/components/narrowLayout"));
const locale_1 = require("app/locale");
class NewsletterConsent extends react_1.Component {
    componentDidMount() {
        document.body.classList.add('auth');
    }
    componentWillUnmount() {
        document.body.classList.remove('auth');
    }
    // NOTE: the text here is duplicated within ``RegisterForm`` on the backend
    render() {
        return (<narrowLayout_1.default>
        <p>
          {(0, locale_1.t)('Pardon the interruption, we just need to get a quick answer from you.')}
        </p>

        <forms_1.ApiForm apiMethod="POST" apiEndpoint="/users/me/subscriptions/" onSubmitSuccess={() => { var _a, _b; return (_b = (_a = this.props).onSubmitSuccess) === null || _b === void 0 ? void 0 : _b.call(_a); }} submitLabel={(0, locale_1.t)('Continue')}>
          <forms_1.RadioBooleanField key="subscribed" name="subscribed" label={(0, locale_1.t)('Email Updates')} help={<span>
                {(0, locale_1.tct)(`We'd love to keep you updated via email with product and feature
                   announcements, promotions, educational materials, and events. Our updates
                   focus on relevant information, and we'll never sell your data to third
                   parties. See our [link:Privacy Policy] for more details.
                   `, { link: <externalLink_1.default href="https://sentry.io/privacy/"/> })}
              </span>} yesLabel={(0, locale_1.t)('Yes, I would like to receive updates via email')} noLabel={(0, locale_1.t)("No, I'd prefer not to receive these updates")} required/>
        </forms_1.ApiForm>
      </narrowLayout_1.default>);
    }
}
exports.default = NewsletterConsent;
//# sourceMappingURL=newsletterConsent.jsx.map