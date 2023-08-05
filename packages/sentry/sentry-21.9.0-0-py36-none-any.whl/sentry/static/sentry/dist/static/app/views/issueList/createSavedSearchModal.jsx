Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const indicator_1 = require("app/actionCreators/indicator");
const savedSearches_1 = require("app/actionCreators/savedSearches");
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const forms_1 = require("app/components/forms");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
const utils_1 = require("./utils");
const DEFAULT_SORT_OPTIONS = [
    utils_1.IssueSortOptions.DATE,
    utils_1.IssueSortOptions.NEW,
    utils_1.IssueSortOptions.FREQ,
    utils_1.IssueSortOptions.PRIORITY,
    utils_1.IssueSortOptions.USER,
];
class CreateSavedSearchModal extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            isSaving: false,
            name: '',
            error: null,
            query: null,
            sort: null,
        };
        this.onSubmit = (e) => {
            const { api, organization } = this.props;
            const query = this.state.query || this.props.query;
            const sort = this.validateSortOption(this.state.sort || this.props.sort);
            e.preventDefault();
            this.setState({ isSaving: true });
            (0, indicator_1.addLoadingMessage)((0, locale_1.t)('Saving Changes'));
            (0, savedSearches_1.createSavedSearch)(api, organization.slug, this.state.name, query, sort)
                .then(_data => {
                this.props.closeModal();
                this.setState({
                    error: null,
                    isSaving: false,
                });
                (0, indicator_1.clearIndicators)();
            })
                .catch(err => {
                let error = (0, locale_1.t)('Unable to save your changes.');
                if (err.responseJSON && err.responseJSON.detail) {
                    error = err.responseJSON.detail;
                }
                this.setState({
                    error,
                    isSaving: false,
                });
                (0, indicator_1.clearIndicators)();
            });
        };
        this.handleChangeName = (val) => {
            this.setState({ name: String(val) });
        };
        this.handleChangeQuery = (val) => {
            this.setState({ query: String(val) });
        };
        this.handleChangeSort = (val) => {
            this.setState({ sort: val });
        };
    }
    /** Handle "date added" sort not being available for saved searches */
    validateSortOption(sort) {
        if (this.sortOptions().find(option => option === sort)) {
            return sort;
        }
        return utils_1.IssueSortOptions.DATE;
    }
    sortOptions() {
        var _a;
        const { organization } = this.props;
        const options = [...DEFAULT_SORT_OPTIONS];
        if ((_a = organization === null || organization === void 0 ? void 0 : organization.features) === null || _a === void 0 ? void 0 : _a.includes('issue-list-trend-sort')) {
            options.push(utils_1.IssueSortOptions.TREND);
        }
        return options;
    }
    render() {
        const { isSaving, error } = this.state;
        const { Header, Footer, Body, closeModal, query, sort } = this.props;
        const sortOptions = this.sortOptions().map(sortOption => ({
            value: sortOption,
            label: (0, utils_1.getSortLabel)(sortOption),
        }));
        return (<form onSubmit={this.onSubmit}>
        <Header>
          <h4>{(0, locale_1.t)('Save Current Search')}</h4>
        </Header>

        <Body>
          {this.state.error && (<div className="alert alert-error alert-block">{error}</div>)}

          <p>{(0, locale_1.t)('All team members will now have access to this search.')}</p>
          <forms_1.TextField key="name" name="name" label={(0, locale_1.t)('Name')} placeholder="e.g. My Search Results" required onChange={this.handleChangeName}/>
          <forms_1.TextField key="query" name="query" label={(0, locale_1.t)('Query')} value={query} required onChange={this.handleChangeQuery}/>
          <forms_1.SelectField key="sort" name="sort" label={(0, locale_1.t)('Sort By')} required clearable={false} defaultValue={this.validateSortOption(sort)} options={sortOptions} onChange={this.handleChangeSort}/>
        </Body>
        <Footer>
          <button_1.default priority="default" size="small" disabled={isSaving} onClick={closeModal} style={{ marginRight: (0, space_1.default)(1) }}>
            {(0, locale_1.t)('Cancel')}
          </button_1.default>
          <button_1.default priority="primary" size="small" disabled={isSaving}>
            {(0, locale_1.t)('Save')}
          </button_1.default>
        </Footer>
      </form>);
    }
}
exports.default = (0, withApi_1.default)(CreateSavedSearchModal);
//# sourceMappingURL=createSavedSearchModal.jsx.map