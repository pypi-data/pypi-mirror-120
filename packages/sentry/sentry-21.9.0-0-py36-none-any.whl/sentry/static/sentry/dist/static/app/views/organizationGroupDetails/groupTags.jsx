Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const alert_1 = (0, tslib_1.__importDefault)(require("app/components/alert"));
const count_1 = (0, tslib_1.__importDefault)(require("app/components/count"));
const deviceName_1 = (0, tslib_1.__importDefault)(require("app/components/deviceName"));
const globalSelectionLink_1 = (0, tslib_1.__importDefault)(require("app/components/globalSelectionLink"));
const loadingError_1 = (0, tslib_1.__importDefault)(require("app/components/loadingError"));
const loadingIndicator_1 = (0, tslib_1.__importDefault)(require("app/components/loadingIndicator"));
const panels_1 = require("app/components/panels");
const version_1 = (0, tslib_1.__importDefault)(require("app/components/version"));
const locale_1 = require("app/locale");
const overflowEllipsis_1 = (0, tslib_1.__importDefault)(require("app/styles/overflowEllipsis"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const utils_1 = require("app/utils");
const withApi_1 = (0, tslib_1.__importDefault)(require("app/utils/withApi"));
class GroupTags extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            tagList: null,
            loading: true,
            error: false,
        };
        this.fetchData = () => {
            const { api, group, environments } = this.props;
            this.setState({
                loading: true,
                error: false,
            });
            api.request(`/issues/${group.id}/tags/`, {
                query: { environment: environments },
                success: data => {
                    this.setState({
                        tagList: data,
                        error: false,
                        loading: false,
                    });
                },
                error: () => {
                    this.setState({
                        error: true,
                        loading: false,
                    });
                },
            });
        };
    }
    componentDidMount() {
        this.fetchData();
    }
    componentDidUpdate(prevProps) {
        if (!(0, isEqual_1.default)(prevProps.environments, this.props.environments)) {
            this.fetchData();
        }
    }
    getTagsDocsUrl() {
        return 'https://docs.sentry.io/platform-redirect/?next=/enriching-events/tags';
    }
    render() {
        const { baseUrl } = this.props;
        let children = [];
        if (this.state.loading) {
            return <loadingIndicator_1.default />;
        }
        else if (this.state.error) {
            return <loadingError_1.default onRetry={this.fetchData}/>;
        }
        if (this.state.tagList) {
            children = this.state.tagList.map((tag, tagIdx) => {
                const valueChildren = tag.topValues.map((tagValue, tagValueIdx) => {
                    let label = null;
                    const pct = (0, utils_1.percent)(tagValue.count, tag.totalValues);
                    const query = tagValue.query || `${tag.key}:"${tagValue.value}"`;
                    switch (tag.key) {
                        case 'release':
                            label = <version_1.default version={tagValue.name} anchor={false}/>;
                            break;
                        default:
                            label = <deviceName_1.default value={tagValue.name}/>;
                    }
                    return (<li key={tagValueIdx} data-test-id={tag.key}>
              <TagBarGlobalSelectionLink to={{
                            pathname: `${baseUrl}events/`,
                            query: { query },
                        }}>
                <TagBarBackground style={{ width: pct + '%' }}/>
                <TagBarLabel>{label}</TagBarLabel>
                <TagBarCount>
                  <count_1.default value={tagValue.count}/>
                </TagBarCount>
              </TagBarGlobalSelectionLink>
            </li>);
                });
                return (<TagItem key={tagIdx}>
            <panels_1.Panel>
              <panels_1.PanelHeader hasButtons style={{ textTransform: 'none' }}>
                <div style={{ fontSize: 16 }}>{tag.key}</div>
                <DetailsLinkWrapper>
                  <globalSelectionLink_1.default className="btn btn-default btn-sm" to={`${baseUrl}tags/${tag.key}/`}>
                    {(0, locale_1.t)('More Details')}
                  </globalSelectionLink_1.default>
                </DetailsLinkWrapper>
              </panels_1.PanelHeader>
              <panels_1.PanelBody withPadding>
                <ul style={{ listStyleType: 'none', padding: 0, margin: 0 }}>
                  {valueChildren}
                </ul>
              </panels_1.PanelBody>
            </panels_1.Panel>
          </TagItem>);
            });
        }
        return (<div>
        <Container>{children}</Container>
        <alert_1.default type="info">
          {(0, locale_1.tct)('Tags are automatically indexed for searching and breakdown charts. Learn how to [link: add custom tags to issues]', {
                link: <a href={this.getTagsDocsUrl()}/>,
            })}
        </alert_1.default>
      </div>);
    }
}
const DetailsLinkWrapper = (0, styled_1.default)('div') `
  display: flex;
`;
const Container = (0, styled_1.default)('div') `
  display: flex;
  flex-wrap: wrap;
`;
const TagItem = (0, styled_1.default)('div') `
  padding: 0 ${(0, space_1.default)(1)};
  width: 50%;
`;
const TagBarBackground = (0, styled_1.default)('div') `
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  background: ${p => p.theme.tagBar};
  border-radius: ${p => p.theme.borderRadius};
`;
const TagBarGlobalSelectionLink = (0, styled_1.default)(globalSelectionLink_1.default) `
  position: relative;
  display: flex;
  line-height: 2.2;
  color: ${p => p.theme.textColor};
  margin-bottom: ${(0, space_1.default)(0.5)};
  padding: 0 ${(0, space_1.default)(1)};
  background: ${p => p.theme.backgroundSecondary};
  border-radius: ${p => p.theme.borderRadius};
  overflow: hidden;

  &:hover {
    color: ${p => p.theme.textColor};
    text-decoration: underline;
    ${TagBarBackground} {
      background: ${p => p.theme.tagBarHover};
    }
  }
`;
const TagBarLabel = (0, styled_1.default)('div') `
  position: relative;
  flex-grow: 1;
  ${overflowEllipsis_1.default}
`;
const TagBarCount = (0, styled_1.default)('div') `
  position: relative;
  padding-left: ${(0, space_1.default)(2)};
`;
exports.default = (0, withApi_1.default)(GroupTags);
//# sourceMappingURL=groupTags.jsx.map