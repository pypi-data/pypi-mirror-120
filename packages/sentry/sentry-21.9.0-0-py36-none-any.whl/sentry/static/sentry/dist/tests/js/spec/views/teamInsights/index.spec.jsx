Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
const teamInsights_1 = (0, tslib_1.__importDefault)(require("app/views/teamInsights"));
describe('TeamInsightsContainer', () => {
    it('blocks access if org is missing flag', () => {
        // @ts-expect-error
        const organization = TestStubs.Organization();
        // @ts-expect-error
        const context = TestStubs.routerContext([{ organization }]);
        const wrapper = (0, reactTestingLibrary_1.mountWithTheme)(<teamInsights_1.default organization={organization}>
        <div>test</div>
      </teamInsights_1.default>, { context });
        expect(wrapper.queryByText('test')).toBeNull();
    });
    it('allows access for orgs with flag', () => {
        // @ts-expect-error
        const organization = TestStubs.Organization({ features: ['team-insights'] });
        // @ts-expect-error
        const context = TestStubs.routerContext([{ organization }]);
        const wrapper = (0, reactTestingLibrary_1.mountWithTheme)(<teamInsights_1.default organization={organization}>
        <div>test</div>
      </teamInsights_1.default>, { context });
        expect(wrapper.getByText('test')).toBeTruthy();
    });
});
//# sourceMappingURL=index.spec.jsx.map