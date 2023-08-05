Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reactTestingLibrary_1 = require("sentry-test/reactTestingLibrary");
const banner_1 = (0, tslib_1.__importDefault)(require("app/components/banner"));
describe('Banner', function () {
    it('can be dismissed', function () {
        const wrapper = (0, reactTestingLibrary_1.mountWithTheme)(<banner_1.default dismissKey="test" title="test"/>);
        expect(wrapper.getByText('test')).toBeInTheDocument();
        reactTestingLibrary_1.fireEvent.click(wrapper.getByLabelText('Close'));
        expect(wrapper.queryByText('test')).toBeNull();
        expect(localStorage.getItem('test-banner-dismissed')).toBe('true');
    });
    it('is not dismissable', function () {
        const wrapper = (0, reactTestingLibrary_1.mountWithTheme)(<banner_1.default isDismissable={false}/>);
        expect(wrapper.queryByLabelText('Close')).toBeNull();
    });
});
//# sourceMappingURL=banner.spec.jsx.map