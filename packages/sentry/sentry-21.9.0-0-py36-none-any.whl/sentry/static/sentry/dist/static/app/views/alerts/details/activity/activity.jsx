Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const groupBy_1 = (0, tslib_1.__importDefault)(require("lodash/groupBy"));
const moment_1 = (0, tslib_1.__importDefault)(require("moment"));
const item_1 = (0, tslib_1.__importDefault)(require("app/components/activity/item"));
const note_1 = (0, tslib_1.__importDefault)(require("app/components/activity/note"));
const inputWithStorage_1 = (0, tslib_1.__importDefault)(require("app/components/activity/note/inputWithStorage"));
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const timeSince_1 = (0, tslib_1.__importDefault)(require("app/components/timeSince"));
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const types_1 = require("../../types");
const activityPlaceholder_1 = (0, tslib_1.__importDefault)(require("./activityPlaceholder"));
const dateDivider_1 = (0, tslib_1.__importDefault)(require("./dateDivider"));
const statusItem_1 = (0, tslib_1.__importDefault)(require("./statusItem"));
/**
 * Activity component on Incident Details view
 * Allows user to leave a comment on an alertId as well as
 * fetch and render existing activity items.
 */
class Activity extends React.Component {
    constructor() {
        super(...arguments);
        this.handleUpdateNote = (note, { activity }) => {
            const { onUpdateNote } = this.props;
            onUpdateNote(note, activity);
        };
        this.handleDeleteNote = ({ activity }) => {
            const { onDeleteNote } = this.props;
            onDeleteNote(activity);
        };
    }
    render() {
        const { loading, error, me, alertId, incident, activities, noteInputId, createBusy, createError, createErrorJSON, onCreateNote, } = this.props;
        const noteProps = Object.assign({ minHeight: 80, projectSlugs: (incident && incident.projects) || [] }, this.props.noteInputProps);
        const activitiesByDate = (0, groupBy_1.default)(activities, ({ dateCreated }) => (0, moment_1.default)(dateCreated).format('ll'));
        const today = (0, moment_1.default)().format('ll');
        return (<div>
        <item_1.default author={{ type: 'user', user: me }}>
          {() => (<inputWithStorage_1.default key={noteInputId} storageKey="incidentIdinput" itemKey={alertId} onCreate={onCreateNote} busy={createBusy} error={createError} errorJSON={createErrorJSON} placeholder={(0, locale_1.t)('Leave a comment, paste a tweet, or link any other relevant information about this alert...')} {...noteProps}/>)}
        </item_1.default>

        {error && <loadingError_1.default message={(0, locale_1.t)('There was a problem loading activities')}/>}

        {loading && (<React.Fragment>
            <activityPlaceholder_1.default />
            <activityPlaceholder_1.default />
            <activityPlaceholder_1.default />
          </React.Fragment>)}

        {!loading &&
                !error &&
                Object.entries(activitiesByDate).map(([date, activitiesForDate]) => {
                    const title = date === today ? ((0, locale_1.t)('Today')) : (<React.Fragment>
                  {date} <StyledTimeSince date={date}/>
                </React.Fragment>);
                    return (<React.Fragment key={date}>
                <dateDivider_1.default>{title}</dateDivider_1.default>
                {activitiesForDate &&
                            activitiesForDate.map(activity => {
                                var _a, _b;
                                const authorName = (_b = (_a = activity.user) === null || _a === void 0 ? void 0 : _a.name) !== null && _b !== void 0 ? _b : 'Sentry';
                                if (activity.type === types_1.IncidentActivityType.COMMENT) {
                                    return (<errorBoundary_1.default mini key={`note-${activity.id}`}>
                          <note_1.default showTime user={activity.user} modelId={activity.id} text={activity.comment || ''} dateCreated={activity.dateCreated} activity={activity} authorName={authorName} onDelete={this.handleDeleteNote} onUpdate={this.handleUpdateNote} {...noteProps}/>
                        </errorBoundary_1.default>);
                                }
                                else {
                                    return (<errorBoundary_1.default mini key={`note-${activity.id}`}>
                          <statusItem_1.default showTime incident={incident} authorName={authorName} activity={activity}/>
                        </errorBoundary_1.default>);
                                }
                            })}
              </React.Fragment>);
                })}
      </div>);
    }
}
exports.default = Activity;
const StyledTimeSince = (0, styled_1.default)(timeSince_1.default) `
  color: ${p => p.theme.gray300};
  font-size: ${p => p.theme.fontSizeSmall};
  margin-left: ${(0, space_1.default)(0.5)};
`;
//# sourceMappingURL=activity.jsx.map