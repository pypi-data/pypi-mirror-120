Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
const teamStore_1 = (0, tslib_1.__importDefault)(require("app/stores/teamStore"));
const useLegacyStore_1 = require("app/stores/useLegacyStore");
describe('useLegacyStore', () => {
    // @ts-expect-error
    const team = TestStubs.Team();
    function TestComponent() {
        const teamStore = (0, useLegacyStore_1.useLegacyStore)(teamStore_1.default);
        return <div>Teams: {teamStore.teams.length}</div>;
    }
    afterEach(() => {
        teamStore_1.default.reset();
    });
    it('should update on change to store', () => {
        const wrapper = (0, reactTestingLibrary_1.mountWithTheme)(<TestComponent />);
        expect(wrapper.getByText('Teams: 0')).toBeTruthy();
        (0, reactTestingLibrary_1.act)(() => teamStore_1.default.loadInitialData([team]));
        expect(wrapper.getByText('Teams: 1')).toBeTruthy();
    });
});
//# sourceMappingURL=useLegacyStore.spec.jsx.map