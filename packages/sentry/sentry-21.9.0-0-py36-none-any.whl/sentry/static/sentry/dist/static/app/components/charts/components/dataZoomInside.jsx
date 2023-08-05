Object.defineProperty(exports, "__esModule", { value: true });
require("echarts/lib/component/dataZoomInside");
const DEFAULT = {
    type: 'inside',
    zoomOnMouseWheel: 'shift',
    throttle: 50,
};
function DataZoomInside(props) {
    // `props` can be boolean, if so return default
    if (!props || !Array.isArray(props)) {
        const dataZoom = Object.assign(Object.assign({}, DEFAULT), props);
        return [dataZoom];
    }
    return props;
}
exports.default = DataZoomInside;
//# sourceMappingURL=dataZoomInside.jsx.map