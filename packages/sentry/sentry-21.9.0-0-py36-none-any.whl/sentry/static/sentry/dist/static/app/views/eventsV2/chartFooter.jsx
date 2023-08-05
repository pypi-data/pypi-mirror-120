Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const optionSelector_1 = (0, tslib_1.__importDefault)(require("app/components/charts/optionSelector"));
const styles_1 = require("app/components/charts/styles");
const locale_1 = require("app/locale");
function ChartFooter({ total, yAxisValue, yAxisOptions, onAxisChange, displayMode, displayOptions, onDisplayChange, }) {
    const elements = [];
    elements.push(<styles_1.SectionHeading key="total-label">{(0, locale_1.t)('Total Events')}</styles_1.SectionHeading>);
    elements.push(total === null ? (<styles_1.SectionValue data-test-id="loading-placeholder" key="total-value">
        &mdash;
      </styles_1.SectionValue>) : (<styles_1.SectionValue key="total-value">{total.toLocaleString()}</styles_1.SectionValue>));
    return (<styles_1.ChartControls>
      <styles_1.InlineContainer>{elements}</styles_1.InlineContainer>
      <styles_1.InlineContainer>
        <optionSelector_1.default title={(0, locale_1.t)('Display')} selected={displayMode} options={displayOptions} onChange={onDisplayChange} menuWidth="170px"/>
        <optionSelector_1.default title={(0, locale_1.t)('Y-Axis')} selected={yAxisValue} options={yAxisOptions} onChange={onAxisChange}/>
      </styles_1.InlineContainer>
    </styles_1.ChartControls>);
}
exports.default = ChartFooter;
//# sourceMappingURL=chartFooter.jsx.map