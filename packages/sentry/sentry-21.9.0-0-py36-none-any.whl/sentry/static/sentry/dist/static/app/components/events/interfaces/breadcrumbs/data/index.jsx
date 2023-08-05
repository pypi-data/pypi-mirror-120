Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const breadcrumbs_1 = require("app/types/breadcrumbs");
const default_1 = (0, tslib_1.__importDefault)(require("./default"));
const exception_1 = (0, tslib_1.__importDefault)(require("./exception"));
const http_1 = (0, tslib_1.__importDefault)(require("./http"));
const Data = ({ breadcrumb, event, orgId, searchTerm }) => {
    if (breadcrumb.type === breadcrumbs_1.BreadcrumbType.HTTP) {
        return <http_1.default breadcrumb={breadcrumb} searchTerm={searchTerm}/>;
    }
    if (breadcrumb.type === breadcrumbs_1.BreadcrumbType.WARNING ||
        breadcrumb.type === breadcrumbs_1.BreadcrumbType.ERROR) {
        return <exception_1.default breadcrumb={breadcrumb} searchTerm={searchTerm}/>;
    }
    return (<default_1.default event={event} orgId={orgId} breadcrumb={breadcrumb} searchTerm={searchTerm}/>);
};
exports.default = Data;
//# sourceMappingURL=index.jsx.map