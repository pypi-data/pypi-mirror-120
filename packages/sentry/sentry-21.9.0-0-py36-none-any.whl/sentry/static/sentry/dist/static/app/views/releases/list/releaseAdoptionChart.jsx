Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const compact_1 = (0, tslib_1.__importDefault)(require("lodash/compact"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const asyncComponent_1 = (0, tslib_1.__importDefault)(require("app/components/asyncComponent"));
const chartZoom_1 = (0, tslib_1.__importDefault)(require("app/components/charts/chartZoom"));
const lineChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/lineChart"));
const styles_1 = require("app/components/charts/styles");
const transitionChart_1 = (0, tslib_1.__importDefault)(require("app/components/charts/transitionChart"));
const transparentLoadingMask_1 = (0, tslib_1.__importDefault)(require("app/components/charts/transparentLoadingMask"));
const utils_1 = require("app/components/charts/utils");
const count_1 = (0, tslib_1.__importDefault)(require("app/components/count"));
const getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
const panels_1 = require("app/components/panels");
const placeholder_1 = (0, tslib_1.__importDefault)(require("app/components/placeholder"));
const globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_2 = require("app/utils");
const formatters_1 = require("app/utils/formatters");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const utils_3 = require("app/views/releases/list/utils");
const releaseHealthRequest_1 = require("app/views/releases/utils/releaseHealthRequest");
class ReleaseAdoptionChart extends asyncComponent_1.default {
    constructor() {
        super(...arguments);
        this.shouldReload = true;
        this.handleClick = (params) => {
            const { organization, router, selection, location } = this.props;
            const project = selection.projects[0];
            router.push({
                pathname: `/organizations/${organization === null || organization === void 0 ? void 0 : organization.slug}/releases/${encodeURIComponent(params.seriesId)}/`,
                query: { project, environment: location.query.environment },
            });
        };
    }
    // TODO(release-adoption-chart): refactor duplication
    getInterval() {
        const { organization, location } = this.props;
        const datetimeObj = {
            start: location.query.start,
            end: location.query.end,
            period: location.query.statsPeriod,
            utc: location.query.utc,
        };
        const diffInMinutes = (0, utils_1.getDiffInMinutes)(datetimeObj);
        // use high fidelity intervals when available
        // limit on backend is set to six hour
        if (organization.features.includes('minute-resolution-sessions') &&
            diffInMinutes < 360) {
            return '10m';
        }
        if (diffInMinutes >= utils_1.ONE_WEEK) {
            return '1d';
        }
        else {
            return '1h';
        }
    }
    getEndpoints() {
        const { organization, location, activeDisplay } = this.props;
        const hasSemverFeature = organization.features.includes('semver');
        return [
            [
                'sessions',
                `/organizations/${organization.slug}/sessions/`,
                {
                    query: Object.assign(Object.assign({ interval: this.getInterval() }, (0, getParams_1.getParams)((0, pick_1.default)(location.query, Object.values(globalSelectionHeader_1.URL_PARAM)))), { groupBy: ['release'], field: [(0, releaseHealthRequest_1.sessionDisplayToField)(activeDisplay)], query: location.query.query
                            ? hasSemverFeature
                                ? location.query.query
                                : `release:${location.query.query}`
                            : undefined }),
                },
            ],
        ];
    }
    getReleasesSeries() {
        var _a;
        const { activeDisplay } = this.props;
        const { sessions } = this.state;
        const releases = sessions === null || sessions === void 0 ? void 0 : sessions.groups.map(group => group.by.release);
        if (!releases) {
            return null;
        }
        const totalData = (_a = sessions === null || sessions === void 0 ? void 0 : sessions.groups) === null || _a === void 0 ? void 0 : _a.reduce((acc, group) => (0, releaseHealthRequest_1.reduceTimeSeriesGroups)(acc, group, (0, releaseHealthRequest_1.sessionDisplayToField)(activeDisplay)), []);
        return releases.map(release => {
            var _a, _b;
            const releaseData = (_a = sessions === null || sessions === void 0 ? void 0 : sessions.groups.find(({ by }) => by.release === release)) === null || _a === void 0 ? void 0 : _a.series[(0, releaseHealthRequest_1.sessionDisplayToField)(activeDisplay)];
            return {
                id: release,
                seriesName: (0, formatters_1.formatVersion)(release),
                data: (_b = sessions === null || sessions === void 0 ? void 0 : sessions.intervals.map((interval, index) => {
                    var _a, _b;
                    return ({
                        name: (0, moment_1.default)(interval).valueOf(),
                        value: (0, utils_2.percent)((_a = releaseData === null || releaseData === void 0 ? void 0 : releaseData[index]) !== null && _a !== void 0 ? _a : 0, (_b = totalData === null || totalData === void 0 ? void 0 : totalData[index]) !== null && _b !== void 0 ? _b : 0),
                    });
                })) !== null && _b !== void 0 ? _b : [],
            };
        });
    }
    getTotal() {
        const { activeDisplay } = this.props;
        const { sessions } = this.state;
        return ((sessions === null || sessions === void 0 ? void 0 : sessions.groups.reduce((acc, group) => acc + group.totals[(0, releaseHealthRequest_1.sessionDisplayToField)(activeDisplay)], 0)) || 0);
    }
    renderEmpty() {
        return (<panels_1.Panel>
        <panels_1.PanelBody withPadding>
          <ChartHeader>
            <placeholder_1.default height="24px"/>
          </ChartHeader>
          <placeholder_1.default height="200px"/>
        </panels_1.PanelBody>
        <ChartFooter>
          <placeholder_1.default height="34px"/>
        </ChartFooter>
      </panels_1.Panel>);
    }
    render() {
        const { activeDisplay, router, selection } = this.props;
        const { start, end, period, utc } = selection.datetime;
        const { loading, reloading, sessions } = this.state;
        const releasesSeries = this.getReleasesSeries();
        const totalCount = this.getTotal();
        if ((loading && !reloading) || (reloading && totalCount === 0) || !sessions) {
            return this.renderEmpty();
        }
        if (!(releasesSeries === null || releasesSeries === void 0 ? void 0 : releasesSeries.length)) {
            return null;
        }
        const interval = this.getInterval();
        const numDataPoints = releasesSeries[0].data.length;
        const xAxisData = releasesSeries[0].data.map(point => point.name);
        const hideLastPoint = releasesSeries.findIndex(series => series.data[numDataPoints - 1].value > 0) === -1;
        return (<panels_1.Panel>
        <panels_1.PanelBody withPadding>
          <ChartHeader>
            <ChartTitle>{(0, locale_1.t)('Release Adoption')}</ChartTitle>
          </ChartHeader>
          <transitionChart_1.default loading={loading} reloading={reloading}>
            <transparentLoadingMask_1.default visible={reloading}/>
            <chartZoom_1.default router={router} period={period} utc={utc} start={start} end={end}>
              {zoomRenderProps => (<lineChart_1.default {...zoomRenderProps} grid={{ left: '10px', right: '10px', top: '40px', bottom: '0px' }} series={releasesSeries.map(series => (Object.assign(Object.assign({}, series), { data: hideLastPoint ? series.data.slice(0, -1) : series.data })))} yAxis={{
                    min: 0,
                    max: 100,
                    type: 'value',
                    interval: 10,
                    splitNumber: 10,
                    data: [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
                    axisLabel: {
                        formatter: '{value}%',
                    },
                }} xAxis={{
                    show: true,
                    min: xAxisData[0],
                    max: xAxisData[numDataPoints - 1],
                    type: 'time',
                    data: xAxisData,
                }} tooltip={{
                    formatter: seriesParams => {
                        const series = Array.isArray(seriesParams)
                            ? seriesParams
                            : [seriesParams];
                        const timestamp = series[0].data[0];
                        const [first, second, third, ...rest] = series
                            .filter(s => s.data[1] > 0)
                            .sort((a, b) => b.data[1] - a.data[1]);
                        const restSum = rest.reduce((acc, s) => acc + s.data[1], 0);
                        const seriesToRender = (0, compact_1.default)([first, second, third]);
                        if (rest.length) {
                            seriesToRender.push({
                                seriesName: (0, locale_1.tn)('%s Other', '%s Others', rest.length),
                                data: [timestamp, restSum],
                                marker: '<span style="display:inline-block;margin-right:5px;border-radius:10px;width:10px;height:10px;"></span>',
                            });
                        }
                        if (!seriesToRender.length) {
                            return '<div/>';
                        }
                        const periodObj = (0, getParams_1.parseStatsPeriod)(interval) || {
                            periodLength: 'd',
                            period: '1',
                        };
                        const intervalStart = (0, moment_1.default)(timestamp).format('MMM D LT');
                        const intervalEnd = (series[0].dataIndex === numDataPoints - 1
                            ? (0, moment_1.default)(sessions.end)
                            : (0, moment_1.default)(timestamp).add(parseInt(periodObj.period, 10), periodObj.periodLength)).format('MMM D LT');
                        return [
                            '<div class="tooltip-series">',
                            seriesToRender
                                .map(s => `<div><span class="tooltip-label">${s.marker}<strong>${s.seriesName && (0, utils_1.truncationFormatter)(s.seriesName, 12)}</strong></span>${s.data[1].toFixed(2)}%</div>`)
                                .join(''),
                            '</div>',
                            `<div class="tooltip-date">${intervalStart} &mdash; ${intervalEnd}</div>`,
                            `<div class="tooltip-arrow"></div>`,
                        ].join('');
                    },
                }} onClick={this.handleClick}/>)}
            </chartZoom_1.default>
          </transitionChart_1.default>
        </panels_1.PanelBody>
        <ChartFooter>
          <styles_1.InlineContainer>
            <styles_1.SectionHeading>
              {(0, locale_1.tct)('Total [display]', {
                display: activeDisplay === utils_3.DisplayOption.USERS ? 'Users' : 'Sessions',
            })}
            </styles_1.SectionHeading>
            <styles_1.SectionValue>
              <count_1.default value={totalCount || 0}/>
            </styles_1.SectionValue>
          </styles_1.InlineContainer>
        </ChartFooter>
      </panels_1.Panel>);
    }
}
exports.default = (0, withApi_1.default)(ReleaseAdoptionChart);
const ChartHeader = (0, styled_1.default)(styles_1.HeaderTitleLegend) `
  margin-bottom: ${(0, space_1.default)(1)};
`;
const ChartTitle = (0, styled_1.default)('header') `
  display: flex;
  flex-direction: row;
`;
const ChartFooter = (0, styled_1.default)(panels_1.PanelFooter) `
  display: flex;
  align-items: center;
  padding: ${(0, space_1.default)(1)} 20px;
`;
//# sourceMappingURL=releaseAdoptionChart.jsx.map