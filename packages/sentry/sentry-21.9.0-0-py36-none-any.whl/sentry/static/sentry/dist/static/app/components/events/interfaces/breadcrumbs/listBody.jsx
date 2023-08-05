Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const tooltip_1 = (0, tslib_1.__importDefault)(require("app/components/tooltip"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const breadcrumbs_1 = require("app/types/breadcrumbs");
const category_1 = (0, tslib_1.__importDefault)(require("./category"));
const data_1 = (0, tslib_1.__importDefault)(require("./data"));
const icon_1 = (0, tslib_1.__importDefault)(require("./icon"));
const level_1 = (0, tslib_1.__importDefault)(require("./level"));
const styles_1 = require("./styles");
const time_1 = (0, tslib_1.__importDefault)(require("./time"));
const ListBody = (0, react_1.memo)(({ orgId, event, breadcrumb, relativeTime, displayRelativeTime, searchTerm, isLastItem, height, }) => {
    const hasError = breadcrumb.type === breadcrumbs_1.BreadcrumbType.ERROR;
    return (<react_1.Fragment>
        <styles_1.GridCellLeft hasError={hasError} isLastItem={isLastItem}>
          <tooltip_1.default title={breadcrumb.description}>
            <icon_1.default icon={breadcrumb.icon} color={breadcrumb.color}/>
          </tooltip_1.default>
        </styles_1.GridCellLeft>
        <GridCellCategory hasError={hasError} isLastItem={isLastItem}>
          <category_1.default category={breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.category} searchTerm={searchTerm}/>
        </GridCellCategory>
        <styles_1.GridCell hasError={hasError} isLastItem={isLastItem} height={height}>
          <data_1.default event={event} orgId={orgId} breadcrumb={breadcrumb} searchTerm={searchTerm}/>
        </styles_1.GridCell>
        <styles_1.GridCell hasError={hasError} isLastItem={isLastItem}>
          <level_1.default level={breadcrumb.level} searchTerm={searchTerm}/>
        </styles_1.GridCell>
        <styles_1.GridCell hasError={hasError} isLastItem={isLastItem}>
          <time_1.default timestamp={breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.timestamp} relativeTime={relativeTime} displayRelativeTime={displayRelativeTime} searchTerm={searchTerm}/>
        </styles_1.GridCell>
      </react_1.Fragment>);
});
exports.default = ListBody;
const GridCellCategory = (0, styled_1.default)(styles_1.GridCell) `
  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    padding-left: ${(0, space_1.default)(1)};
  }
`;
//# sourceMappingURL=listBody.jsx.map