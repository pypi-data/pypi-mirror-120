function app() {
    return __awaiter(this, void 0, void 0, function* () {
        const [{ bootstrap }, { initializeMain }] = yield Promise.all([
            Promise.resolve().then(() => __importStar(require('app/bootstrap'))),
            Promise.resolve().then(() => __importStar(require('app/bootstrap/initializeMain'))),
        ]);
        const data = yield bootstrap();
        initializeMain(data);
    });
}
app();
//# sourceMappingURL=index.jsx.map