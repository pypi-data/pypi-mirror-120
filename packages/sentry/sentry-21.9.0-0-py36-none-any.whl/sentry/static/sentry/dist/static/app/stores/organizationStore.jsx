Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const reflux_1 = (0, tslib_1.__importDefault)(require("reflux"));
const organizationActions_1 = (0, tslib_1.__importDefault)(require("app/actions/organizationActions"));
const projectActions_1 = (0, tslib_1.__importDefault)(require("app/actions/projectActions"));
const teamActions_1 = (0, tslib_1.__importDefault)(require("app/actions/teamActions"));
const constants_1 = require("app/constants");
const storeConfig = {
    init() {
        this.reset();
        this.listenTo(organizationActions_1.default.update, this.onUpdate);
        this.listenTo(organizationActions_1.default.fetchOrg, this.reset);
        this.listenTo(organizationActions_1.default.fetchOrgError, this.onFetchOrgError);
        // fill in teams and projects if they are loaded
        this.listenTo(projectActions_1.default.loadProjects, this.onLoadProjects);
        this.listenTo(teamActions_1.default.loadTeams, this.onLoadTeams);
        // mark the store as dirty if projects or teams change
        this.listenTo(projectActions_1.default.createSuccess, this.onProjectOrTeamChange);
        this.listenTo(projectActions_1.default.updateSuccess, this.onProjectOrTeamChange);
        this.listenTo(projectActions_1.default.changeSlug, this.onProjectOrTeamChange);
        this.listenTo(projectActions_1.default.addTeamSuccess, this.onProjectOrTeamChange);
        this.listenTo(projectActions_1.default.removeTeamSuccess, this.onProjectOrTeamChange);
        this.listenTo(teamActions_1.default.updateSuccess, this.onProjectOrTeamChange);
        this.listenTo(teamActions_1.default.removeTeamSuccess, this.onProjectOrTeamChange);
        this.listenTo(teamActions_1.default.createTeamSuccess, this.onProjectOrTeamChange);
    },
    reset() {
        this.loading = true;
        this.error = null;
        this.errorType = null;
        this.organization = null;
        this.dirty = false;
        this.trigger(this.get());
    },
    onUpdate(updatedOrg, { replace = false } = {}) {
        this.loading = false;
        this.error = null;
        this.errorType = null;
        this.organization = replace ? updatedOrg : Object.assign(Object.assign({}, this.organization), updatedOrg);
        this.dirty = false;
        this.trigger(this.get());
    },
    onFetchOrgError(err) {
        this.organization = null;
        this.errorType = null;
        switch (err === null || err === void 0 ? void 0 : err.status) {
            case 401:
                this.errorType = constants_1.ORGANIZATION_FETCH_ERROR_TYPES.ORG_NO_ACCESS;
                break;
            case 404:
                this.errorType = constants_1.ORGANIZATION_FETCH_ERROR_TYPES.ORG_NOT_FOUND;
                break;
            default:
        }
        this.loading = false;
        this.error = err;
        this.dirty = false;
        this.trigger(this.get());
    },
    onProjectOrTeamChange() {
        // mark the store as dirty so the next fetch will trigger an org details refetch
        this.dirty = true;
    },
    onLoadProjects(projects) {
        if (this.organization) {
            // sort projects to mimic how they are received from backend
            projects.sort((a, b) => a.slug.localeCompare(b.slug));
            this.organization = Object.assign(Object.assign({}, this.organization), { projects });
            this.trigger(this.get());
        }
    },
    onLoadTeams(teams) {
        if (this.organization) {
            // sort teams to mimic how they are received from backend
            teams.sort((a, b) => a.slug.localeCompare(b.slug));
            this.organization = Object.assign(Object.assign({}, this.organization), { teams });
            this.trigger(this.get());
        }
    },
    get() {
        return {
            organization: this.organization,
            error: this.error,
            loading: this.loading,
            errorType: this.errorType,
            dirty: this.dirty,
        };
    },
};
const OrganizationStore = reflux_1.default.createStore(storeConfig);
exports.default = OrganizationStore;
//# sourceMappingURL=organizationStore.jsx.map