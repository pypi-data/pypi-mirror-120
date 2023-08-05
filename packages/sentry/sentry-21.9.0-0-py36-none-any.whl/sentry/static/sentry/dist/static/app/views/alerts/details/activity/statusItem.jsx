Object.defineProperty(exports, "__esModule", { value: true });
exports.getTriggerName = void 0;
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const item_1 = (0, tslib_1.__importDefault)(require("app/components/activity/item"));
const locale_1 = require("app/locale");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
const types_1 = require("../../types");
/**
 * StatusItem renders status changes for Alerts
 *
 * For example: incident detected, or closed
 *
 * Note `activity.dateCreated` refers to when the activity was created vs.
 * `incident.dateStarted` which is when an incident was first detected or created
 */
class StatusItem extends react_1.Component {
    render() {
        const { activity, authorName, incident, showTime } = this.props;
        const isDetected = activity.type === types_1.IncidentActivityType.DETECTED;
        const isStarted = activity.type === types_1.IncidentActivityType.STARTED;
        const isClosed = activity.type === types_1.IncidentActivityType.STATUS_CHANGE &&
            activity.value === `${types_1.IncidentStatus.CLOSED}`;
        const isTriggerChange = activity.type === types_1.IncidentActivityType.STATUS_CHANGE && !isClosed;
        // Unknown activity, don't render anything
        if (!isStarted && !isDetected && !isClosed && !isTriggerChange) {
            return null;
        }
        const currentTrigger = getTriggerName(activity.value);
        const previousTrigger = getTriggerName(activity.previousValue);
        return (<item_1.default showTime={showTime} author={{
                type: activity.user ? 'user' : 'system',
                user: activity.user || undefined,
            }} header={<div>
            {isTriggerChange &&
                    previousTrigger &&
                    (0, locale_1.tct)('Alert status changed from [previousTrigger] to [currentTrigger]', {
                        previousTrigger,
                        currentTrigger: <StatusValue>{currentTrigger}</StatusValue>,
                    })}
            {isTriggerChange &&
                    !previousTrigger &&
                    (0, locale_1.tct)('Alert status changed to [currentTrigger]', {
                        currentTrigger: <StatusValue>{currentTrigger}</StatusValue>,
                    })}
            {isClosed &&
                    (incident === null || incident === void 0 ? void 0 : incident.statusMethod) === types_1.IncidentStatusMethod.RULE_UPDATED &&
                    (0, locale_1.t)('This alert has been auto-resolved because the rule that triggered it has been modified or deleted.')}
            {isClosed &&
                    (incident === null || incident === void 0 ? void 0 : incident.statusMethod) !== types_1.IncidentStatusMethod.RULE_UPDATED &&
                    (0, locale_1.tct)('[user] resolved the alert', {
                        user: <StatusValue>{authorName}</StatusValue>,
                    })}
            {isDetected &&
                    ((incident === null || incident === void 0 ? void 0 : incident.alertRule)
                        ? (0, locale_1.t)('Alert was created')
                        : (0, locale_1.tct)('[user] created an alert', {
                            user: <StatusValue>{authorName}</StatusValue>,
                        }))}
            {isStarted && (0, locale_1.t)('Trigger conditions were met for the interval')}
          </div>} date={(0, getDynamicText_1.default)({ value: activity.dateCreated, fixed: new Date(0) })} interval={isStarted ? incident === null || incident === void 0 ? void 0 : incident.alertRule.timeWindow : undefined}/>);
    }
}
exports.default = StatusItem;
const StatusValue = (0, styled_1.default)('span') `
  font-weight: bold;
`;
function getTriggerName(value) {
    if (value === `${types_1.IncidentStatus.WARNING}`) {
        return (0, locale_1.t)('Warning');
    }
    if (value === `${types_1.IncidentStatus.CRITICAL}`) {
        return (0, locale_1.t)('Critical');
    }
    // Otherwise, activity type is not status change
    return '';
}
exports.getTriggerName = getTriggerName;
//# sourceMappingURL=statusItem.jsx.map