Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const enzyme_1 = require("sentry-test/enzyme");
const clipboardTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/clipboardTooltip"));
const tooltip_1 = require("app/components/tooltip");
describe('ClipboardTooltip', function () {
    it('renders', function () {
        const title = 'tooltip content';
        const wrapper = (0, enzyme_1.mountWithTheme)(<clipboardTooltip_1.default title={title}>
        <span>This text displays a tooltip when hovering</span>
      </clipboardTooltip_1.default>);
        jest.useFakeTimers();
        const trigger = wrapper.find('span');
        trigger.simulate('mouseEnter');
        jest.advanceTimersByTime(tooltip_1.OPEN_DELAY);
        wrapper.update();
        const tooltipClipboardWrapper = wrapper.find('TooltipClipboardWrapper');
        expect(tooltipClipboardWrapper.length).toEqual(1);
        const tooltipTextContent = tooltipClipboardWrapper.find('TextOverflow');
        expect(tooltipTextContent.length).toEqual(1);
        const clipboardContent = tooltipClipboardWrapper.find('Clipboard');
        expect(clipboardContent.length).toEqual(1);
        expect(clipboardContent.props().value).toEqual(title);
        const iconCopy = clipboardContent.find('IconCopy');
        expect(iconCopy.length).toEqual(1);
    });
});
//# sourceMappingURL=clipboardTooltip.spec.jsx.map