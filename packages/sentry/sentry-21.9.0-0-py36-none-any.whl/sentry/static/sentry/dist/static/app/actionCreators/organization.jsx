Object.defineProperty(exports, "__esModule", { value: true });
exports.fetchOrganizationDetails = void 0;
const tslib_1 = require("tslib");
const Sentry = (0, tslib_1.__importStar)(require("@sentry/react"));
const indicator_1 = require("app/actionCreators/indicator");
const organizations_1 = require("app/actionCreators/organizations");
const globalSelectionActions_1 = (0, tslib_1.__importDefault)(require("app/actions/globalSelectionActions"));
const organizationActions_1 = (0, tslib_1.__importDefault)(require("app/actions/organizationActions"));
const projectActions_1 = (0, tslib_1.__importDefault)(require("app/actions/projectActions"));
const teamActions_1 = (0, tslib_1.__importDefault)(require("app/actions/teamActions"));
const api_1 = require("app/api");
const projectsStore_1 = (0, tslib_1.__importDefault)(require("app/stores/projectsStore"));
const teamStore_1 = (0, tslib_1.__importDefault)(require("app/stores/teamStore"));
const getPreloadedData_1 = require("app/utils/getPreloadedData");
function fetchOrg(api, slug, detailed, isInitialFetch) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const detailedQueryParam = detailed ? 1 : 0;
        const org = yield (0, getPreloadedData_1.getPreloadedDataPromise)(`organization?detailed=${detailedQueryParam}`, slug, () => 
        // This data should get preloaded in static/sentry/index.ejs
        // If this url changes make sure to update the preload
        api.requestPromise(`/organizations/${slug}/`, {
            query: { detailed: detailedQueryParam },
        }), isInitialFetch);
        if (!org) {
            throw new Error('retrieved organization is falsey');
        }
        organizationActions_1.default.update(org, { replace: true });
        (0, organizations_1.setActiveOrganization)(org);
        return org;
    });
}
function fetchProjectsAndTeams(slug, isInitialFetch) {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        // Create a new client so the request is not cancelled
        const uncancelableApi = new api_1.Client();
        try {
            const [projects, teams] = yield Promise.all([
                (0, getPreloadedData_1.getPreloadedDataPromise)('projects', slug, () => 
                // This data should get preloaded in static/sentry/index.ejs
                // If this url changes make sure to update the preload
                uncancelableApi.requestPromise(`/organizations/${slug}/projects/`, {
                    query: {
                        all_projects: 1,
                        collapse: 'latestDeploys',
                    },
                }), isInitialFetch),
                (0, getPreloadedData_1.getPreloadedDataPromise)('teams', slug, 
                // This data should get preloaded in static/sentry/index.ejs
                // If this url changes make sure to update the preload
                () => uncancelableApi.requestPromise(`/organizations/${slug}/teams/`), isInitialFetch),
            ]);
            return [projects, teams];
        }
        catch (err) {
            // It's possible these requests fail with a 403 if the user has a role with insufficient access
            // to projects and teams, but *can* access org details (e.g. billing).
            // An example of this is in org settings.
            //
            // Ignore 403s and bubble up other API errors
            if (err.status !== 403) {
                throw err;
            }
        }
        return [[], []];
    });
}
/**
 * Fetches an organization's details with an option for the detailed representation
 * with teams and projects
 *
 * @param api A reference to the api client
 * @param slug The organization slug
 * @param detailed Whether or not the detailed org details should be retrieved
 * @param silent Should we silently update the organization (do not clear the
 *               current organization in the store)
 */
function fetchOrganizationDetails(api, slug, detailed, silent, isInitialFetch) {
    var _a, _b, _c, _d, _e;
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        if (!silent) {
            organizationActions_1.default.fetchOrg();
            projectActions_1.default.reset();
            globalSelectionActions_1.default.reset();
        }
        try {
            const promises = [fetchOrg(api, slug, detailed, isInitialFetch)];
            if (!detailed) {
                promises.push(fetchProjectsAndTeams(slug, isInitialFetch));
            }
            const [org, projectsAndTeams] = yield Promise.all(promises);
            if (!detailed) {
                const [projects, teams] = projectsAndTeams;
                projectActions_1.default.loadProjects(projects);
                teamActions_1.default.loadTeams(teams);
            }
            if (org && detailed) {
                // TODO(davidenwang): Change these to actions after organization.projects
                // and organization.teams no longer exists. Currently if they were changed
                // to actions it would cause OrganizationContext to rerender many times
                teamStore_1.default.loadInitialData(org.teams);
                projectsStore_1.default.loadInitialData(org.projects);
            }
        }
        catch (err) {
            if (!err) {
                return;
            }
            organizationActions_1.default.fetchOrgError(err);
            if (err.status === 403 || err.status === 401) {
                const errMessage = typeof ((_a = err.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) === 'string'
                    ? (_b = err.responseJSON) === null || _b === void 0 ? void 0 : _b.detail
                    : typeof ((_d = (_c = err.responseJSON) === null || _c === void 0 ? void 0 : _c.detail) === null || _d === void 0 ? void 0 : _d.message) === 'string'
                        ? (_e = err.responseJSON) === null || _e === void 0 ? void 0 : _e.detail.message
                        : null;
                if (errMessage) {
                    (0, indicator_1.addErrorMessage)(errMessage);
                }
                return;
            }
            Sentry.captureException(err);
        }
    });
}
exports.fetchOrganizationDetails = fetchOrganizationDetails;
//# sourceMappingURL=organization.jsx.map