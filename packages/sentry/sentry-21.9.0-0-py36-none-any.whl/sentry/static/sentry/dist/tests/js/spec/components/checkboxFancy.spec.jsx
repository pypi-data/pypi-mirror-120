Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const enzyme_1 = require("sentry-test/enzyme");
const checkboxFancy_1 = (0, tslib_1.__importDefault)(require("app/components/checkboxFancy/checkboxFancy"));
describe('CheckboxFancy', function () {
    it('renders', function () {
        const wrapper = (0, enzyme_1.mountWithTheme)(<checkboxFancy_1.default />);
        expect(wrapper).toSnapshot();
    });
    it('isChecked', function () {
        const wrapper = (0, enzyme_1.mountWithTheme)(<checkboxFancy_1.default isChecked/>);
        expect(wrapper.props().isChecked).toEqual(true);
        expect(wrapper.find('[data-test-id="icon-check-mark"]').exists()).toEqual(true);
        expect(wrapper.find('[data-test-id="icon-subtract"]').exists()).toEqual(false);
    });
    it('isIndeterminate', function () {
        const wrapper = (0, enzyme_1.mountWithTheme)(<checkboxFancy_1.default isIndeterminate/>);
        expect(wrapper.props().isIndeterminate).toEqual(true);
        expect(wrapper.find('[data-test-id="icon-check-mark"]').exists()).toEqual(false);
        expect(wrapper.find('[data-test-id="icon-subtract"]').exists()).toEqual(true);
    });
    it('isDisabled', function () {
        const wrapper = (0, enzyme_1.mountWithTheme)(<checkboxFancy_1.default isDisabled/>);
        expect(wrapper.props().isDisabled).toEqual(true);
        expect(wrapper.find('[data-test-id="icon-check-mark"]').exists()).toEqual(false);
        expect(wrapper.find('[data-test-id="icon-subtract"]').exists()).toEqual(false);
    });
});
//# sourceMappingURL=checkboxFancy.spec.jsx.map