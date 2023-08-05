Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const incident_1 = require("app/actionCreators/incident");
const constants_1 = require("app/constants");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const guid_1 = require("app/utils/guid");
const replaceAtArrayIndex_1 = require("app/utils/replaceAtArrayIndex");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const types_1 = require("../../types");
const activity_1 = (0, tslib_1.__importDefault)(require("./activity"));
/**
 * Activity component on Incident Details view
 * Allows user to leave a comment on an alertId as well as
 * fetch and render existing activity items.
 */
class ActivityContainer extends react_1.PureComponent {
    constructor() {
        super(...arguments);
        this.state = {
            loading: true,
            error: false,
            noteInputId: (0, guid_1.uniqueId)(),
            noteInputText: '',
            createBusy: false,
            createError: false,
            createErrorJSON: null,
            activities: null,
        };
        this.handleCreateNote = (note) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, params } = this.props;
            const { alertId, orgId } = params;
            const newActivity = {
                comment: note.text,
                type: types_1.IncidentActivityType.COMMENT,
                dateCreated: new Date().toISOString(),
                user: configStore_1.default.get('user'),
                id: (0, guid_1.uniqueId)(),
                incidentIdentifier: alertId,
            };
            this.setState(state => ({
                createBusy: true,
                // This is passed as a key to NoteInput that re-mounts
                // (basically so we can reset text input to empty string)
                noteInputId: (0, guid_1.uniqueId)(),
                activities: [newActivity, ...(state.activities || [])],
                noteInputText: '',
            }));
            try {
                const newNote = yield (0, incident_1.createIncidentNote)(api, orgId, alertId, note);
                this.setState(state => {
                    // Update activities to replace our fake new activity with activity object from server
                    const activities = [
                        newNote,
                        ...state.activities.filter(activity => activity !== newActivity),
                    ];
                    return {
                        createBusy: false,
                        activities,
                    };
                });
            }
            catch (error) {
                this.setState(state => {
                    const activities = state.activities.filter(activity => activity !== newActivity);
                    return {
                        // We clear the textarea immediately when submitting, restore
                        // value when there has been an error
                        noteInputText: note.text,
                        activities,
                        createBusy: false,
                        createError: true,
                        createErrorJSON: error.responseJSON || constants_1.DEFAULT_ERROR_JSON,
                    };
                });
            }
        });
        this.getIndexAndActivityFromState = (activity) => {
            // `index` should probably be found, if not let error hit Sentry
            const index = this.state.activities !== null
                ? this.state.activities.findIndex(({ id }) => id === activity.id)
                : '';
            return [index, this.state.activities[index]];
        };
        this.handleDeleteNote = (activity) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, params } = this.props;
            const { alertId, orgId } = params;
            const [index, oldActivity] = this.getIndexAndActivityFromState(activity);
            this.setState(state => ({
                activities: removeFromArrayIndex(state.activities, index),
            }));
            try {
                yield (0, incident_1.deleteIncidentNote)(api, orgId, alertId, activity.id);
            }
            catch (error) {
                this.setState(state => ({
                    activities: (0, replaceAtArrayIndex_1.replaceAtArrayIndex)(state.activities, index, oldActivity),
                }));
            }
        });
        this.handleUpdateNote = (note, activity) => (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, params } = this.props;
            const { alertId, orgId } = params;
            const [index, oldActivity] = this.getIndexAndActivityFromState(activity);
            this.setState(state => ({
                activities: (0, replaceAtArrayIndex_1.replaceAtArrayIndex)(state.activities, index, Object.assign(Object.assign({}, oldActivity), { comment: note.text })),
            }));
            try {
                yield (0, incident_1.updateIncidentNote)(api, orgId, alertId, activity.id, note);
            }
            catch (error) {
                this.setState(state => ({
                    activities: (0, replaceAtArrayIndex_1.replaceAtArrayIndex)(state.activities, index, oldActivity),
                }));
            }
        });
    }
    componentDidMount() {
        this.fetchData();
    }
    componentDidUpdate(prevProps) {
        // Only refetch if incidentStatus changes.
        //
        // This component can mount before incident details is fully loaded.
        // In which case, `incidentStatus` is null and we will be fetching via `cDM`
        // There's no need to fetch this gets updated due to incident details being loaded
        if (prevProps.incidentStatus !== null &&
            prevProps.incidentStatus !== this.props.incidentStatus) {
            this.fetchData();
        }
    }
    fetchData() {
        return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
            const { api, params } = this.props;
            const { alertId, orgId } = params;
            try {
                const activities = yield (0, incident_1.fetchIncidentActivities)(api, orgId, alertId);
                this.setState({ activities, loading: false });
            }
            catch (err) {
                this.setState({ loading: false, error: !!err });
            }
        });
    }
    render() {
        const _a = this.props, { api, params, incident } = _a, props = (0, tslib_1.__rest)(_a, ["api", "params", "incident"]);
        const { alertId } = params;
        const me = configStore_1.default.get('user');
        return (<activity_1.default alertId={alertId} me={me} api={api} {...this.state} loading={this.state.loading || !incident} incident={incident} onCreateNote={this.handleCreateNote} onUpdateNote={this.handleUpdateNote} onDeleteNote={this.handleDeleteNote} {...props}/>);
    }
}
exports.default = (0, withApi_1.default)(ActivityContainer);
function removeFromArrayIndex(array, index) {
    const newArray = [...array];
    newArray.splice(index, 1);
    return newArray;
}
//# sourceMappingURL=index.jsx.map