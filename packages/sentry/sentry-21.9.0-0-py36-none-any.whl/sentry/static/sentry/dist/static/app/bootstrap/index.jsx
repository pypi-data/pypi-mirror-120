Object.defineProperty(exports, "__esModule", { value: true });
exports.bootstrap = void 0;
const tslib_1 = require("tslib");
const BOOTSTRAP_URL = '/api/client-config/';
const bootApplication = (data) => {
    window.csrfCookieName = data.csrfCookieName;
    return data;
};
function bootWithHydration() {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const response = yield fetch(BOOTSTRAP_URL);
        const data = yield response.json();
        window.__initialData = data;
        return bootApplication(data);
    });
}
function bootstrap() {
    return (0, tslib_1.__awaiter)(this, void 0, void 0, function* () {
        const bootstrapData = window.__initialData;
        // If __initialData is not already set on the window, we are likely running in
        // pure SPA mode, meaning django is not serving our frontend application and we
        // need to make an API request to hydrate the bootstrap data to boot the app.
        if (bootstrapData === undefined) {
            return yield bootWithHydration();
        }
        return bootApplication(bootstrapData);
    });
}
exports.bootstrap = bootstrap;
//# sourceMappingURL=index.jsx.map