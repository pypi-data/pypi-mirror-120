Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styles_1 = require("./styles");
const Icon = React.memo(({ icon, color, size }) => {
    const Svg = icon;
    return (<styles_1.IconWrapper color={color}>
      <Svg size={size}/>
    </styles_1.IconWrapper>);
});
exports.default = Icon;
//# sourceMappingURL=icon.jsx.map