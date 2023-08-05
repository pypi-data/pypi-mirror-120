Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const highlight_1 = (0, tslib_1.__importDefault)(require("app/components/highlight"));
const tag_1 = (0, tslib_1.__importDefault)(require("app/components/tag"));
const locale_1 = require("app/locale");
const breadcrumbs_1 = require("app/types/breadcrumbs");
const Level = (0, react_1.memo)(({ level, searchTerm = '' }) => {
    switch (level) {
        case breadcrumbs_1.BreadcrumbLevelType.FATAL:
            return (<tag_1.default type="error">
          <highlight_1.default text={searchTerm}>{(0, locale_1.t)('fatal')}</highlight_1.default>
        </tag_1.default>);
        case breadcrumbs_1.BreadcrumbLevelType.ERROR:
            return (<tag_1.default type="error">
          <highlight_1.default text={searchTerm}>{(0, locale_1.t)('error')}</highlight_1.default>
        </tag_1.default>);
        case breadcrumbs_1.BreadcrumbLevelType.INFO:
            return (<tag_1.default type="info">
          <highlight_1.default text={searchTerm}>{(0, locale_1.t)('info')}</highlight_1.default>
        </tag_1.default>);
        case breadcrumbs_1.BreadcrumbLevelType.WARNING:
            return (<tag_1.default type="warning">
          <highlight_1.default text={searchTerm}>{(0, locale_1.t)('warning')}</highlight_1.default>
        </tag_1.default>);
        default:
            return (<tag_1.default>
          <highlight_1.default text={searchTerm}>{level || (0, locale_1.t)('undefined')}</highlight_1.default>
        </tag_1.default>);
    }
});
exports.default = Level;
//# sourceMappingURL=level.jsx.map