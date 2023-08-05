Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const indicators_1 = (0, tslib_1.__importDefault)(require("app/components/indicators"));
const themeAndStyleProvider_1 = (0, tslib_1.__importDefault)(require("app/themeAndStyleProvider"));
const awsLambdaCloudformation_1 = (0, tslib_1.__importDefault)(require("./awsLambdaCloudformation"));
const awsLambdaFailureDetails_1 = (0, tslib_1.__importDefault)(require("./awsLambdaFailureDetails"));
const awsLambdaFunctionSelect_1 = (0, tslib_1.__importDefault)(require("./awsLambdaFunctionSelect"));
const awsLambdaProjectSelect_1 = (0, tslib_1.__importDefault)(require("./awsLambdaProjectSelect"));
/**
 * This component is a wrapper for specific pipeline views for integrations
 */
const pipelineMapper = {
    awsLambdaProjectSelect: [awsLambdaProjectSelect_1.default, 'AWS Lambda Select Project'],
    awsLambdaFunctionSelect: [awsLambdaFunctionSelect_1.default, 'AWS Lambda Select Lambdas'],
    awsLambdaCloudformation: [awsLambdaCloudformation_1.default, 'AWS Lambda Create Cloudformation'],
    awsLambdaFailureDetails: [awsLambdaFailureDetails_1.default, 'AWS Lambda View Failures'],
};
class PipelineView extends React.Component {
    componentDidMount() {
        // update the title based on our mappings
        const title = this.mapping[1];
        document.title = title;
    }
    get mapping() {
        const { pipelineName } = this.props;
        const mapping = pipelineMapper[pipelineName];
        if (!mapping) {
            throw new Error(`Invalid pipeline name ${pipelineName}`);
        }
        return mapping;
    }
    render() {
        const Component = this.mapping[0];
        return (<themeAndStyleProvider_1.default>
        <indicators_1.default className="indicators-container"/>
        <Component {...this.props}/>
      </themeAndStyleProvider_1.default>);
    }
}
exports.default = PipelineView;
//# sourceMappingURL=pipelineView.jsx.map