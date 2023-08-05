Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const enzyme_1 = require("sentry-test/enzyme");
const initializeOrg_1 = require("sentry-test/initializeOrg");
const eventView_1 = (0, tslib_1.__importDefault)(require("app/utils/discover/eventView"));
const landing_1 = require("app/views/performance/landing");
const utils_1 = require("app/views/performance/landing/utils");
function initializeData(settings) {
    // @ts-expect-error
    const _defaultProject = TestStubs.Project();
    const _settings = Object.assign({ query: {}, features: [], projects: [_defaultProject], project: _defaultProject }, settings);
    const { query, features } = _settings;
    // @ts-expect-error
    const projects = [TestStubs.Project()];
    const [project] = projects;
    // @ts-expect-error
    const organization = TestStubs.Organization({
        features,
        projects,
    });
    const router = {
        location: {
            query: Object.assign({}, query),
        },
    };
    const initialData = (0, initializeOrg_1.initializeOrg)({ organization, projects, project, router });
    return initialData;
}
const WrappedComponent = ({ data }) => {
    const eventView = eventView_1.default.fromLocation(data.router.location);
    return (<landing_1.PerformanceLanding organization={data.organization} location={data.router.location} eventView={eventView} projects={data.projects} shouldShowOnboarding={false} handleSearch={() => { }} handleTrendsClick={() => { }} setError={() => { }}/>);
};
describe('Performance > Landing > Index', function () {
    beforeEach(function () {
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/organizations/org-slug/sdk-updates/',
            body: [],
        });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            url: '/prompts-activity/',
            body: {},
        });
        // @ts-expect-error
        MockApiClient.addMockResponse({
            method: 'GET',
            url: `/organizations/org-slug/key-transactions-list/`,
            body: [],
        });
    });
    afterEach(function () {
        // @ts-expect-error
        MockApiClient.clearMockResponses();
    });
    it('renders basic UI elements', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const data = initializeData();
            const wrapper = (0, enzyme_1.mountWithTheme)(<WrappedComponent data={data}/>, data.routerContext);
            // @ts-expect-error
            yield tick();
            wrapper.update();
            expect(wrapper.find('div[data-test-id="performance-landing-v3"]').exists()).toBe(true);
        });
    });
    it('renders frontend pageload view', function () {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const data = initializeData({
                query: { landingDisplay: utils_1.LandingDisplayField.FRONTEND_PAGELOAD },
            });
            const wrapper = (0, enzyme_1.mountWithTheme)(<WrappedComponent data={data}/>, data.routerContext);
            // @ts-expect-error
            yield tick();
            wrapper.update();
            expect(wrapper.find('div[data-test-id="frontend-pageload-view"]').exists()).toBe(true);
        });
    });
});
//# sourceMappingURL=index.spec.jsx.map