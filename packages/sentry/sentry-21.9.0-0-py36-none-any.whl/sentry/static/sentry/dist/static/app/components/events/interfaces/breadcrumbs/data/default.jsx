Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const annotatedText_1 = (0, tslib_1.__importDefault)(require("app/components/events/meta/annotatedText"));
const metaProxy_1 = require("app/components/events/meta/metaProxy");
const highlight_1 = (0, tslib_1.__importDefault)(require("app/components/highlight"));
const link_1 = (0, tslib_1.__importDefault)(require("app/components/links/link"));
const urls_1 = require("app/utils/discover/urls");
const withProjects_1 = (0, tslib_1.__importDefault)(require("app/utils/withProjects"));
const summary_1 = (0, tslib_1.__importDefault)(require("./summary"));
const Default = ({ breadcrumb, event, orgId, searchTerm }) => (<summary_1.default kvData={breadcrumb.data}>
    {(breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.message) && (<annotatedText_1.default value={<FormatMessage searchTerm={searchTerm} event={event} orgId={orgId} breadcrumb={breadcrumb} message={breadcrumb.message}/>} meta={(0, metaProxy_1.getMeta)(breadcrumb, 'message')}/>)}
  </summary_1.default>);
function isEventId(maybeEventId) {
    // maybeEventId is an event id if it's a hex string of 32 characters long
    return /^[a-fA-F0-9]{32}$/.test(maybeEventId);
}
const FormatMessage = (0, withProjects_1.default)(function FormatMessageInner({ searchTerm, event, message, breadcrumb, projects, loadingProjects, orgId, }) {
    const content = <highlight_1.default text={searchTerm}>{message}</highlight_1.default>;
    if (!loadingProjects &&
        typeof orgId === 'string' &&
        breadcrumb.category === 'sentry.transaction' &&
        isEventId(message)) {
        const maybeProject = projects.find(project => {
            return project.id === event.projectID;
        });
        if (!maybeProject) {
            return content;
        }
        const projectSlug = maybeProject.slug;
        const eventSlug = (0, urls_1.generateEventSlug)({ project: projectSlug, id: message });
        return <link_1.default to={(0, urls_1.eventDetailsRoute)({ orgSlug: orgId, eventSlug })}>{content}</link_1.default>;
    }
    return content;
});
exports.default = Default;
//# sourceMappingURL=default.jsx.map