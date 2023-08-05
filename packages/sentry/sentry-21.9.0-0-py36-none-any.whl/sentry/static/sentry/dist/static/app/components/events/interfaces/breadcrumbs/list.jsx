Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const react_virtualized_1 = require("react-virtualized");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const isEqual_1 = (0, tslib_1.__importDefault)(require("lodash/isEqual"));
const listBody_1 = (0, tslib_1.__importDefault)(require("./listBody"));
const listHeader_1 = (0, tslib_1.__importDefault)(require("./listHeader"));
const styles_1 = require("./styles");
const LIST_MAX_HEIGHT = 400;
const cache = new react_virtualized_1.CellMeasurerCache({
    fixedWidth: true,
    minHeight: 42,
});
class ListContainer extends React.Component {
    constructor() {
        super(...arguments);
        this.state = {
            scrollToIndex: this.props.breadcrumbs.length - 1,
        };
        this.listRef = null;
        this.updateGrid = () => {
            if (this.listRef) {
                cache.clearAll();
                this.listRef.forceUpdateGrid();
            }
        };
        this.setScrollbarSize = ({ size }) => {
            this.setState({ scrollbarSize: size });
        };
        this.renderRow = ({ index, key, parent, style }) => {
            const { breadcrumbs } = this.props;
            const breadcrumb = breadcrumbs[index];
            const isLastItem = breadcrumbs[breadcrumbs.length - 1].id === breadcrumb.id;
            const { height } = style;
            return (<react_virtualized_1.CellMeasurer cache={cache} columnIndex={0} key={key} parent={parent} rowIndex={index}>
        {({ measure }) => isLastItem ? (<Row style={style} onLoad={measure} data-test-id="last-crumb">
              {this.renderBody(breadcrumb, height, isLastItem)}
            </Row>) : (<Row style={style} onLoad={measure}>
              {this.renderBody(breadcrumb, height)}
            </Row>)}
      </react_virtualized_1.CellMeasurer>);
        };
    }
    componentDidMount() {
        this.updateGrid();
    }
    componentDidUpdate(prevProps) {
        this.updateGrid();
        if (!(0, isEqual_1.default)(prevProps.breadcrumbs, this.props.breadcrumbs) &&
            !this.state.scrollToIndex) {
            this.setScrollToIndex(undefined);
        }
    }
    setScrollToIndex(scrollToIndex) {
        this.setState({ scrollToIndex });
    }
    renderBody(breadcrumb, height, isLastItem = false) {
        const { event, orgId, searchTerm, relativeTime, displayRelativeTime } = this.props;
        return (<listBody_1.default orgId={orgId} searchTerm={searchTerm} breadcrumb={breadcrumb} event={event} relativeTime={relativeTime} displayRelativeTime={displayRelativeTime} isLastItem={isLastItem} height={height ? String(height) : undefined}/>);
    }
    render() {
        const { breadcrumbs, displayRelativeTime, onSwitchTimeFormat } = this.props;
        const { scrollToIndex, scrollbarSize } = this.state;
        // onResize is required in case the user rotates the device.
        return (<Wrapper>
        <react_virtualized_1.AutoSizer disableHeight onResize={this.updateGrid}>
          {({ width }) => (<React.Fragment>
              <RowSticky width={width} scrollbarSize={scrollbarSize}>
                <listHeader_1.default displayRelativeTime={!!displayRelativeTime} onSwitchTimeFormat={onSwitchTimeFormat}/>
              </RowSticky>
              <StyledList ref={(el) => {
                    this.listRef = el;
                }} deferredMeasurementCache={cache} height={LIST_MAX_HEIGHT} overscanRowCount={5} rowCount={breadcrumbs.length} rowHeight={cache.rowHeight} rowRenderer={this.renderRow} width={width} onScrollbarPresenceChange={this.setScrollbarSize} 
            // when the component mounts, it scrolls to the last item
            scrollToIndex={scrollToIndex} scrollToAlignment={scrollToIndex ? 'end' : undefined}/>
            </React.Fragment>)}
        </react_virtualized_1.AutoSizer>
      </Wrapper>);
    }
}
exports.default = ListContainer;
const Wrapper = (0, styled_1.default)('div') `
  overflow: hidden;
  ${styles_1.aroundContentStyle}
`;
// XXX(ts): Emotion11 has some trouble with List's defaultProps
//
// It gives the list have a dynamic height; otherwise, in the case of filtered
// options, a list will be displayed with an empty space
const StyledList = (0, styled_1.default)(react_virtualized_1.List) `
  height: auto !important;
  max-height: ${p => p.height}px;
  overflow-y: auto !important;
  outline: none;
`;
const Row = (0, styled_1.default)('div') `
  display: grid;
  grid-template-columns: 45px minmax(55px, 1fr) 6fr 86px 67px;
  @media (min-width: ${p => p.theme.breakpoints[0]}) {
    grid-template-columns: 63px minmax(132px, 1fr) 6fr 75px 85px;
  }
  ${p => p.width && `width: ${p.width}px;`}
`;
const RowSticky = (0, styled_1.default)(Row) `
  ${p => p.scrollbarSize &&
    `padding-right: ${p.scrollbarSize};
     grid-template-columns: 45px minmax(55px, 1fr) 6fr 86px calc(67px + ${p.scrollbarSize}px);
     @media (min-width: ${p.theme.breakpoints[0]}) {
      grid-template-columns: 63px minmax(132px, 1fr) 6fr 75px calc(85px + ${p.scrollbarSize}px);
    }
  `}
`;
//# sourceMappingURL=list.jsx.map