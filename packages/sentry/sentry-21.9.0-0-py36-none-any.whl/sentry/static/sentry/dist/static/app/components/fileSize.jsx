Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const utils_1 = require("app/utils");
const getDynamicText_1 = (0, tslib_1.__importDefault)(require("app/utils/getDynamicText"));
function FileSize(props) {
    const { className, bytes } = props;
    return (<span className={className}>
      {(0, getDynamicText_1.default)({ value: (0, utils_1.formatBytesBase2)(bytes), fixed: 'xx KB' })}
    </span>);
}
exports.default = FileSize;
//# sourceMappingURL=fileSize.jsx.map