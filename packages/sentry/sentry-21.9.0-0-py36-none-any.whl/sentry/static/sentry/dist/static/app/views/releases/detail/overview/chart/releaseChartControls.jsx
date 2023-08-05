Object.defineProperty(exports, "__esModule", { value: true });
exports.PERFORMANCE_AXIS = exports.EventType = exports.YAxis = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const optionSelector_1 = (0, tslib_1.__importDefault)(require("app/components/charts/optionSelector"));
const styles_1 = require("app/components/charts/styles");
const questionTooltip_1 = (0, tslib_1.__importDefault)(require("app/components/questionTooltip"));
const notAvailableMessages_1 = (0, tslib_1.__importDefault)(require("app/constants/notAvailableMessages"));
const locale_1 = require("app/locale");
const fields_1 = require("app/utils/discover/fields");
const constants_1 = require("app/utils/performance/vitals/constants");
var YAxis;
(function (YAxis) {
    YAxis["SESSIONS"] = "sessions";
    YAxis["USERS"] = "users";
    YAxis["CRASH_FREE"] = "crashFree";
    YAxis["SESSION_DURATION"] = "sessionDuration";
    YAxis["EVENTS"] = "events";
    YAxis["FAILED_TRANSACTIONS"] = "failedTransactions";
    YAxis["COUNT_DURATION"] = "countDuration";
    YAxis["COUNT_VITAL"] = "countVital";
})(YAxis = exports.YAxis || (exports.YAxis = {}));
var EventType;
(function (EventType) {
    EventType["ALL"] = "all";
    EventType["CSP"] = "csp";
    EventType["DEFAULT"] = "default";
    EventType["ERROR"] = "error";
    EventType["TRANSACTION"] = "transaction";
})(EventType = exports.EventType || (exports.EventType = {}));
exports.PERFORMANCE_AXIS = [
    YAxis.FAILED_TRANSACTIONS,
    YAxis.COUNT_DURATION,
    YAxis.COUNT_VITAL,
];
const ReleaseChartControls = ({ summary, yAxis, onYAxisChange, organization, hasHealthData, hasDiscover, hasPerformance, eventType = EventType.ALL, onEventTypeChange, vitalType = fields_1.WebVital.LCP, onVitalTypeChange, }) => {
    const noHealthDataTooltip = !hasHealthData
        ? notAvailableMessages_1.default.releaseHealth
        : undefined;
    const noDiscoverTooltip = !hasDiscover ? notAvailableMessages_1.default.discover : undefined;
    const noPerformanceTooltip = !hasPerformance
        ? notAvailableMessages_1.default.performance
        : undefined;
    const yAxisOptions = [
        {
            value: YAxis.SESSIONS,
            label: (0, locale_1.t)('Session Count'),
            disabled: !hasHealthData,
            tooltip: noHealthDataTooltip,
        },
        {
            value: YAxis.SESSION_DURATION,
            label: (0, locale_1.t)('Session Duration'),
            disabled: !hasHealthData,
            tooltip: noHealthDataTooltip,
        },
        {
            value: YAxis.USERS,
            label: (0, locale_1.t)('User Count'),
            disabled: !hasHealthData,
            tooltip: noHealthDataTooltip,
        },
        {
            value: YAxis.CRASH_FREE,
            label: (0, locale_1.t)('Crash Free Rate'),
            disabled: !hasHealthData,
            tooltip: noHealthDataTooltip,
        },
        {
            value: YAxis.FAILED_TRANSACTIONS,
            label: (0, locale_1.t)('Failure Count'),
            disabled: !hasPerformance,
            tooltip: noPerformanceTooltip,
        },
        {
            value: YAxis.COUNT_DURATION,
            label: (0, locale_1.t)('Slow Duration Count'),
            disabled: !hasPerformance,
            tooltip: noPerformanceTooltip,
        },
        {
            value: YAxis.COUNT_VITAL,
            label: (0, locale_1.t)('Slow Vital Count'),
            disabled: !hasPerformance,
            tooltip: noPerformanceTooltip,
        },
        {
            value: YAxis.EVENTS,
            label: (0, locale_1.t)('Event Count'),
            disabled: !hasDiscover && !hasPerformance,
            tooltip: noDiscoverTooltip,
        },
    ];
    const getSummaryHeading = () => {
        switch (yAxis) {
            case YAxis.USERS:
                return (0, locale_1.t)('Total Active Users');
            case YAxis.CRASH_FREE:
                return (0, locale_1.t)('Average Rate');
            case YAxis.SESSION_DURATION:
                return (0, locale_1.t)('Median Duration');
            case YAxis.EVENTS:
                return (0, locale_1.t)('Total Events');
            case YAxis.FAILED_TRANSACTIONS:
                return (0, locale_1.t)('Failed Transactions');
            case YAxis.COUNT_DURATION:
                return (0, locale_1.t)('Count over %sms', organization.apdexThreshold);
            case YAxis.COUNT_VITAL:
                return vitalType !== fields_1.WebVital.CLS
                    ? (0, locale_1.t)('Count over %sms', constants_1.WEB_VITAL_DETAILS[vitalType].poorThreshold)
                    : (0, locale_1.t)('Count over %s', constants_1.WEB_VITAL_DETAILS[vitalType].poorThreshold);
            case YAxis.SESSIONS:
            default:
                return (0, locale_1.t)('Total Sessions');
        }
    };
    return (<styles_1.ChartControls>
      <styles_1.InlineContainer>
        <styles_1.SectionHeading key="total-label">
          {getSummaryHeading()}
          <questionTooltip_1.default position="top" size="sm" title={(0, locale_1.t)('This value includes only the current release.')}/>
        </styles_1.SectionHeading>
        <styles_1.SectionValue key="total-value">{summary}</styles_1.SectionValue>
      </styles_1.InlineContainer>
      <styles_1.InlineContainer>
        <SecondarySelector yAxis={yAxis} eventType={eventType} onEventTypeChange={onEventTypeChange} vitalType={vitalType} onVitalTypeChange={onVitalTypeChange}/>
        <optionSelector_1.default title={(0, locale_1.t)('Display')} selected={yAxis} options={yAxisOptions} onChange={onYAxisChange}/>
      </styles_1.InlineContainer>
    </styles_1.ChartControls>);
};
const eventTypeOptions = [
    { value: EventType.ALL, label: (0, locale_1.t)('All') },
    { value: EventType.CSP, label: (0, locale_1.t)('CSP') },
    { value: EventType.DEFAULT, label: (0, locale_1.t)('Default') },
    { value: EventType.ERROR, label: 'Error' },
    { value: EventType.TRANSACTION, label: (0, locale_1.t)('Transaction') },
];
const vitalTypeOptions = [
    fields_1.WebVital.FP,
    fields_1.WebVital.FCP,
    fields_1.WebVital.LCP,
    fields_1.WebVital.FID,
    fields_1.WebVital.CLS,
].map(vital => ({ value: vital, label: constants_1.WEB_VITAL_DETAILS[vital].name }));
function SecondarySelector({ yAxis, eventType, onEventTypeChange, vitalType, onVitalTypeChange, }) {
    switch (yAxis) {
        case YAxis.EVENTS:
            return (<optionSelector_1.default title={(0, locale_1.t)('Event Type')} selected={eventType} options={eventTypeOptions} onChange={onEventTypeChange}/>);
        case YAxis.COUNT_VITAL:
            return (<optionSelector_1.default title={(0, locale_1.t)('Vital')} selected={vitalType} options={vitalTypeOptions} onChange={onVitalTypeChange}/>);
        default:
            return null;
    }
}
exports.default = ReleaseChartControls;
//# sourceMappingURL=releaseChartControls.jsx.map