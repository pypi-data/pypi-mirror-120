Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const react_dom_1 = (0, tslib_1.__importDefault)(require("react-dom"));
const css_1 = require("@emotion/css"); // eslint-disable-line emotion/no-vanilla
const react_2 = require("@emotion/react"); // This is needed to set "speedy" = false (for percy)
const preferences_1 = require("app/actionCreators/preferences");
const configStore_1 = (0, tslib_1.__importDefault)(require("app/stores/configStore"));
const global_1 = (0, tslib_1.__importDefault)(require("app/styles/global"));
const theme_1 = require("app/utils/theme");
const withConfig_1 = (0, tslib_1.__importDefault)(require("app/utils/withConfig"));
class Main extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            theme: this.themeName === 'dark' ? theme_1.darkTheme : theme_1.lightTheme,
        };
    }
    componentDidMount() {
        (0, preferences_1.loadPreferencesState)();
    }
    componentDidUpdate(prevProps) {
        const { config } = this.props;
        if (config.theme !== prevProps.config.theme) {
            // eslint-disable-next-line
            this.setState({
                theme: config.theme === 'dark' ? theme_1.darkTheme : theme_1.lightTheme,
            });
        }
    }
    get themeName() {
        return configStore_1.default.get('theme');
    }
    render() {
        return (<react_2.ThemeProvider theme={this.state.theme}>
        <global_1.default isDark={this.props.config.theme === 'dark'} theme={this.state.theme}/>
        <react_2.CacheProvider value={css_1.cache}>{this.props.children}</react_2.CacheProvider>
        {react_dom_1.default.createPortal(<meta name="color-scheme" content={this.themeName}/>, document.head)}
      </react_2.ThemeProvider>);
    }
}
exports.default = (0, withConfig_1.default)(Main);
//# sourceMappingURL=themeAndStyleProvider.jsx.map