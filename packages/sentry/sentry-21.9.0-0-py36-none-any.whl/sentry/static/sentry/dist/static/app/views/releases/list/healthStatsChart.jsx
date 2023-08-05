Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_lazyload_1 = (0, tslib_1.__importDefault)(require("react-lazyload"));
const react_2 = require("@emotion/react");
const miniBarChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/miniBarChart"));
const locale_1 = require("app/locale");
const utils_1 = require("./utils");
class HealthStatsChart extends react_1.Component {
    constructor() {
        super(...arguments);
        this.formatTooltip = (value) => {
            const { activeDisplay } = this.props;
            const suffix = activeDisplay === utils_1.DisplayOption.USERS
                ? (0, locale_1.tn)('user', 'users', value)
                : (0, locale_1.tn)('session', 'sessions', value);
            return `${value.toLocaleString()} ${suffix}`;
        };
    }
    render() {
        const { height, data, theme } = this.props;
        return (<react_lazyload_1.default debounce={50} height={height}>
        <miniBarChart_1.default series={data} height={height} isGroupedByDate showTimeInTooltip hideDelay={50} tooltipFormatter={this.formatTooltip} colors={[theme.purple300, theme.gray200]}/>
      </react_lazyload_1.default>);
    }
}
HealthStatsChart.defaultProps = {
    height: 24,
};
exports.default = (0, react_2.withTheme)(HealthStatsChart);
//# sourceMappingURL=healthStatsChart.jsx.map