Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const chartZoom_1 = (0, tslib_1.__importDefault)(require("app/components/charts/chartZoom"));
const errorPanel_1 = (0, tslib_1.__importDefault)(require("app/components/charts/errorPanel"));
const transitionChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/transitionChart"));
const transparentLoadingMask_1 = (0, tslib_1.__importDefault)(require("app/components/charts/transparentLoadingMask"));
const icons_1 = require("app/icons");
const sessionTerm_1 = require("app/views/releases/utils/sessionTerm");
const healthChart_1 = (0, tslib_1.__importDefault)(require("./healthChart"));
const utils_1 = require("./utils");
class ReleaseChartContainer extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            shouldRecalculateVisibleSeries: true,
        };
        this.handleVisibleSeriesRecalculated = () => {
            this.setState({ shouldRecalculateVisibleSeries: false });
        };
    }
    render() {
        const { loading, errored, reloading, chartData, selection, yAxis, router, platform, title, help, } = this.props;
        const { shouldRecalculateVisibleSeries } = this.state;
        const { datetime } = selection;
        const { utc, period, start, end } = datetime;
        const timeseriesData = chartData.filter(({ seriesName }) => {
            // There is no concept of Abnormal sessions in javascript
            if ((seriesName === sessionTerm_1.sessionTerm.abnormal ||
                seriesName === sessionTerm_1.sessionTerm.otherAbnormal) &&
                ['javascript', 'node'].includes(platform)) {
                return false;
            }
            return true;
        });
        return (<chartZoom_1.default router={router} period={period} utc={utc} start={start} end={end}>
        {zoomRenderProps => {
                if (errored) {
                    return (<errorPanel_1.default>
                <icons_1.IconWarning color="gray300" size="lg"/>
              </errorPanel_1.default>);
                }
                return (<transitionChart_1.default loading={loading} reloading={reloading}>
              <transparentLoadingMask_1.default visible={reloading}/>
              <healthChart_1.default timeseriesData={timeseriesData.sort(utils_1.sortSessionSeries)} zoomRenderProps={zoomRenderProps} reloading={reloading} yAxis={yAxis} location={router.location} shouldRecalculateVisibleSeries={shouldRecalculateVisibleSeries} onVisibleSeriesRecalculated={this.handleVisibleSeriesRecalculated} platform={platform} title={title} help={help}/>
            </transitionChart_1.default>);
            }}
      </chartZoom_1.default>);
    }
}
exports.default = ReleaseChartContainer;
//# sourceMappingURL=healthChartContainer.jsx.map