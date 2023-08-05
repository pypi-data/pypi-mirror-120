Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const omit_1 = (0, tslib_1.__importDefault)(require("lodash/omit"));
const pick_1 = (0, tslib_1.__importDefault)(require("lodash/pick"));
const guideAnchor_1 = (0, tslib_1.__importDefault)(require("app/components/assistant/guideAnchor"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const errorBoundary_1 = (0, tslib_1.__importDefault)(require("app/components/errorBoundary"));
const eventDataSection_1 = (0, tslib_1.__importDefault)(require("app/components/events/eventDataSection"));
const iconWarning_1 = require("app/icons/iconWarning");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const breadcrumbs_1 = require("app/types/breadcrumbs");
const event_1 = require("app/types/event");
const utils_1 = require("app/utils");
const emptyMessage_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/emptyMessage"));
const searchBarAction_1 = (0, tslib_1.__importDefault)(require("../searchBarAction"));
const searchBarActionFilter_1 = (0, tslib_1.__importDefault)(require("../searchBarAction/searchBarActionFilter"));
const icon_1 = (0, tslib_1.__importDefault)(require("./icon"));
const level_1 = (0, tslib_1.__importDefault)(require("./level"));
const list_1 = (0, tslib_1.__importDefault)(require("./list"));
const styles_1 = require("./styles");
const utils_2 = require("./utils");
class Breadcrumbs extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            searchTerm: '',
            breadcrumbs: [],
            filteredByFilter: [],
            filteredBySearch: [],
            filterOptions: {},
            displayRelativeTime: false,
        };
        this.handleSearch = (value) => {
            this.setState(prevState => ({
                searchTerm: value,
                filteredBySearch: this.filterBySearch(value, prevState.filteredByFilter),
            }));
        };
        this.handleFilter = (filterOptions) => {
            const filteredByFilter = this.getFilteredCrumbsByFilter(filterOptions);
            this.setState(prevState => ({
                filterOptions,
                filteredByFilter,
                filteredBySearch: this.filterBySearch(prevState.searchTerm, filteredByFilter),
            }));
        };
        this.handleSwitchTimeFormat = () => {
            this.setState(prevState => ({
                displayRelativeTime: !prevState.displayRelativeTime,
            }));
        };
        this.handleCleanSearch = () => {
            this.setState({ searchTerm: '' });
        };
        this.handleResetFilter = () => {
            this.setState(({ breadcrumbs, filterOptions, searchTerm }) => ({
                filteredByFilter: breadcrumbs,
                filterOptions: Object.keys(filterOptions).reduce((accumulator, currentValue) => {
                    accumulator[currentValue] = filterOptions[currentValue].map(filterOption => (Object.assign(Object.assign({}, filterOption), { isChecked: false })));
                    return accumulator;
                }, {}),
                filteredBySearch: this.filterBySearch(searchTerm, breadcrumbs),
            }));
        };
        this.handleResetSearchBar = () => {
            this.setState(prevState => ({
                searchTerm: '',
                filteredBySearch: prevState.breadcrumbs,
            }));
        };
    }
    componentDidMount() {
        this.loadBreadcrumbs();
    }
    loadBreadcrumbs() {
        var _a;
        const { data } = this.props;
        let breadcrumbs = data.values;
        // Add the (virtual) breadcrumb based on the error or message event if possible.
        const virtualCrumb = this.getVirtualCrumb();
        if (virtualCrumb) {
            breadcrumbs = [...breadcrumbs, virtualCrumb];
        }
        const transformedCrumbs = (0, utils_2.transformCrumbs)(breadcrumbs);
        const filterOptions = this.getFilterOptions(transformedCrumbs);
        this.setState({
            relativeTime: (_a = transformedCrumbs[transformedCrumbs.length - 1]) === null || _a === void 0 ? void 0 : _a.timestamp,
            breadcrumbs: transformedCrumbs,
            filteredByFilter: transformedCrumbs,
            filteredBySearch: transformedCrumbs,
            filterOptions,
        });
    }
    getFilterOptions(breadcrumbs) {
        const types = this.getFilterTypes(breadcrumbs);
        const levels = this.getFilterLevels(types);
        const options = {};
        if (!!types.length) {
            options[(0, locale_1.t)('Types')] = types.map(type => (0, omit_1.default)(type, 'levels'));
        }
        if (!!levels.length) {
            options[(0, locale_1.t)('Levels')] = levels;
        }
        return options;
    }
    getFilterTypes(breadcrumbs) {
        const filterTypes = [];
        for (const index in breadcrumbs) {
            const breadcrumb = breadcrumbs[index];
            const foundFilterType = filterTypes.findIndex(f => f.id === breadcrumb.type);
            if (foundFilterType === -1) {
                filterTypes.push({
                    id: breadcrumb.type,
                    symbol: <icon_1.default {...(0, omit_1.default)(breadcrumb, 'description')} size="xs"/>,
                    isChecked: false,
                    description: breadcrumb.description,
                    levels: (breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.level) ? [breadcrumb.level] : [],
                });
                continue;
            }
            if ((breadcrumb === null || breadcrumb === void 0 ? void 0 : breadcrumb.level) &&
                !filterTypes[foundFilterType].levels.includes(breadcrumb.level)) {
                filterTypes[foundFilterType].levels.push(breadcrumb.level);
            }
        }
        return filterTypes;
    }
    getFilterLevels(types) {
        const filterLevels = [];
        for (const indexType in types) {
            for (const indexLevel in types[indexType].levels) {
                const level = types[indexType].levels[indexLevel];
                if (filterLevels.some(f => f.id === level)) {
                    continue;
                }
                filterLevels.push({
                    id: level,
                    symbol: <level_1.default level={level}/>,
                    isChecked: false,
                });
            }
        }
        return filterLevels;
    }
    moduleToCategory(module) {
        if (!module) {
            return undefined;
        }
        const match = module.match(/^.*\/(.*?)(:\d+)/);
        if (!match) {
            return module.split(/./)[0];
        }
        return match[1];
    }
    getVirtualCrumb() {
        const { event } = this.props;
        const exception = event.entries.find(entry => entry.type === event_1.EntryType.EXCEPTION);
        if (!exception && !event.message) {
            return undefined;
        }
        const timestamp = event.dateCreated;
        if (exception) {
            const { type, value, module: mdl } = exception.data.values[0];
            return {
                type: breadcrumbs_1.BreadcrumbType.ERROR,
                level: breadcrumbs_1.BreadcrumbLevelType.ERROR,
                category: this.moduleToCategory(mdl) || 'exception',
                data: {
                    type,
                    value,
                },
                timestamp,
            };
        }
        const levelTag = (event.tags || []).find(tag => tag.key === 'level');
        return {
            type: breadcrumbs_1.BreadcrumbType.INFO,
            level: (levelTag === null || levelTag === void 0 ? void 0 : levelTag.value) || breadcrumbs_1.BreadcrumbLevelType.UNDEFINED,
            category: 'message',
            message: event.message,
            timestamp,
        };
    }
    filterBySearch(searchTerm, breadcrumbs) {
        if (!searchTerm.trim()) {
            return breadcrumbs;
        }
        // Slightly hacky, but it works
        // the string is being `stringfy`d here in order to match exactly the same `stringfy`d string of the loop
        const searchFor = JSON.stringify(searchTerm)
            // it replaces double backslash generate by JSON.stringfy with single backslash
            .replace(/((^")|("$))/g, '')
            .toLocaleLowerCase();
        return breadcrumbs.filter(obj => Object.keys((0, pick_1.default)(obj, ['type', 'category', 'message', 'level', 'timestamp', 'data'])).some(key => {
            const info = obj[key];
            if (!(0, utils_1.defined)(info) || !String(info).trim()) {
                return false;
            }
            return JSON.stringify(info)
                .replace(/((^")|("$))/g, '')
                .toLocaleLowerCase()
                .trim()
                .includes(searchFor);
        }));
    }
    getFilteredCrumbsByFilter(filterOptions) {
        const checkedTypeOptions = new Set(Object.values(filterOptions)[0]
            .filter(filterOption => filterOption.isChecked)
            .map(option => option.id));
        const checkedLevelOptions = new Set(Object.values(filterOptions)[1]
            .filter(filterOption => filterOption.isChecked)
            .map(option => option.id));
        const { breadcrumbs } = this.state;
        if (!![...checkedTypeOptions].length && !![...checkedLevelOptions].length) {
            return breadcrumbs.filter(filteredCrumb => checkedTypeOptions.has(filteredCrumb.type) &&
                checkedLevelOptions.has(filteredCrumb.level));
        }
        if (!![...checkedTypeOptions].length) {
            return breadcrumbs.filter(filteredCrumb => checkedTypeOptions.has(filteredCrumb.type));
        }
        if (!![...checkedLevelOptions].length) {
            return breadcrumbs.filter(filteredCrumb => checkedLevelOptions.has(filteredCrumb.level));
        }
        return breadcrumbs;
    }
    getEmptyMessage() {
        const { searchTerm, filteredBySearch, filterOptions } = this.state;
        if (searchTerm && !filteredBySearch.length) {
            const hasActiveFilter = Object.values(filterOptions)
                .flatMap(filterOption => filterOption)
                .find(filterOption => filterOption.isChecked);
            return (<StyledEmptyMessage icon={<iconWarning_1.IconWarning size="xl"/>} action={hasActiveFilter ? (<button_1.default onClick={this.handleResetFilter} priority="primary">
                {(0, locale_1.t)('Reset filter')}
              </button_1.default>) : (<button_1.default onClick={this.handleResetSearchBar} priority="primary">
                {(0, locale_1.t)('Clear search bar')}
              </button_1.default>)}>
          {(0, locale_1.t)('Sorry, no breadcrumbs match your search query')}
        </StyledEmptyMessage>);
        }
        return (<StyledEmptyMessage icon={<iconWarning_1.IconWarning size="xl"/>}>
        {(0, locale_1.t)('There are no breadcrumbs to be displayed')}
      </StyledEmptyMessage>);
    }
    render() {
        const { type, event, organization } = this.props;
        const { filterOptions, searchTerm, filteredBySearch, displayRelativeTime, relativeTime, } = this.state;
        return (<StyledEventDataSection type={type} title={<guideAnchor_1.default target="breadcrumbs" position="right">
            <h3>{(0, locale_1.t)('Breadcrumbs')}</h3>
          </guideAnchor_1.default>} actions={<StyledSearchBarAction placeholder={(0, locale_1.t)('Search breadcrumbs')} onChange={this.handleSearch} query={searchTerm} filter={<searchBarActionFilter_1.default onChange={this.handleFilter} options={filterOptions}/>}/>} wrapTitle={false} isCentered>
        {!!filteredBySearch.length ? (<errorBoundary_1.default>
            <list_1.default breadcrumbs={filteredBySearch} event={event} orgId={organization.slug} onSwitchTimeFormat={this.handleSwitchTimeFormat} displayRelativeTime={displayRelativeTime} searchTerm={searchTerm} relativeTime={relativeTime} // relativeTime has to be always available, as the last item timestamp is the event created time
            />
          </errorBoundary_1.default>) : (this.getEmptyMessage())}
      </StyledEventDataSection>);
    }
}
exports.default = Breadcrumbs;
const StyledEventDataSection = (0, styled_1.default)(eventDataSection_1.default) `
  margin-bottom: ${(0, space_1.default)(3)};
`;
const StyledEmptyMessage = (0, styled_1.default)(emptyMessage_1.default) `
  ${styles_1.aroundContentStyle};
`;
const StyledSearchBarAction = (0, styled_1.default)(searchBarAction_1.default) `
  z-index: 2;
`;
//# sourceMappingURL=index.jsx.map