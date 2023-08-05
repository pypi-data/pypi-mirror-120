Object.defineProperty(exports, "__esModule", { value: true });
exports.findByTextContent = void 0;
/**
 * Search for a text broken up by multiple html elements
 * e.g.: <div>Hello <span>world</span></div>
 */
function findByTextContent(screen, textMatch) {
    return screen.findByText((_, contentNode) => {
        const hasText = (node) => node.textContent === textMatch;
        const nodeHasText = hasText(contentNode);
        const childrenDontHaveText = Array.from((contentNode === null || contentNode === void 0 ? void 0 : contentNode.children) || []).every(child => !hasText(child));
        return nodeHasText && childrenDontHaveText;
    });
}
exports.findByTextContent = findByTextContent;
//# sourceMappingURL=utils.jsx.map