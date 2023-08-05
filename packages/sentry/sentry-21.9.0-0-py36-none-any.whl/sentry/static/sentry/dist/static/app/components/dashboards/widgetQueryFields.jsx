Object.defineProperty(exports, "__esModule", { value: true });
exports.QueryFieldWrapper = void 0;
const tslib_1 = require("tslib");
const React = (0, tslib_1.__importStar)(require("react"));
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const button_1 = (0, tslib_1.__importDefault)(require("app/components/button"));
const icons_1 = require("app/icons");
const locale_1 = require("app/locale");
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const fields_1 = require("app/utils/discover/fields");
const columnEditCollection_1 = (0, tslib_1.__importDefault)(require("app/views/eventsV2/table/columnEditCollection"));
const queryField_1 = require("app/views/eventsV2/table/queryField");
const types_1 = require("app/views/eventsV2/table/types");
const field_1 = (0, tslib_1.__importDefault)(require("app/views/settings/components/forms/field"));
function WidgetQueryFields({ displayType, errors, fields, fieldOptions, organization, onChange, style, }) {
    // Handle new fields being added.
    function handleAdd(event) {
        event.preventDefault();
        const newFields = [...fields, ''];
        onChange(newFields);
    }
    function handleRemove(event, fieldIndex) {
        event.preventDefault();
        const newFields = [...fields];
        newFields.splice(fieldIndex, 1);
        onChange(newFields);
    }
    function handleChangeField(value, fieldIndex) {
        const newFields = [...fields];
        newFields[fieldIndex] = (0, fields_1.generateFieldAsString)(value);
        onChange(newFields);
    }
    function handleColumnChange(columns) {
        const newFields = columns.map(fields_1.generateFieldAsString);
        onChange(newFields);
    }
    if (displayType === 'table') {
        return (<field_1.default data-test-id="columns" label={(0, locale_1.t)('Columns')} inline={false} style={Object.assign({ padding: `${(0, space_1.default)(1)} 0` }, (style !== null && style !== void 0 ? style : {}))} error={errors === null || errors === void 0 ? void 0 : errors.fields} flexibleControlStateSize stacked required>
        <StyledColumnEditCollection columns={fields.map(field => (0, fields_1.explodeField)({ field }))} onChange={handleColumnChange} fieldOptions={fieldOptions} organization={organization}/>
      </field_1.default>);
    }
    const hideAddYAxisButton = (['world_map', 'big_number'].includes(displayType) && fields.length === 1) ||
        (['line', 'area', 'stacked_area', 'bar'].includes(displayType) &&
            fields.length === 3);
    // Any function/field choice for Big Number widgets is legal since the
    // data source is from an endpoint that is not timeseries-based.
    // The function/field choice for World Map widget will need to be numeric-like.
    // Column builder for Table widget is already handled above.
    const doNotValidateYAxis = displayType === 'big_number';
    return (<field_1.default data-test-id="y-axis" label={(0, locale_1.t)('Y-Axis')} inline={false} style={Object.assign({ padding: `${(0, space_1.default)(2)} 0 24px 0` }, (style !== null && style !== void 0 ? style : {}))} flexibleControlStateSize error={errors === null || errors === void 0 ? void 0 : errors.fields} required stacked>
      {fields.map((field, i) => {
            const fieldValue = (0, fields_1.explodeField)({ field });
            return (<exports.QueryFieldWrapper key={`${field}:${i}`}>
            <queryField_1.QueryField fieldValue={fieldValue} fieldOptions={fieldOptions} onChange={value => handleChangeField(value, i)} filterPrimaryOptions={option => {
                    // Only validate function names for timeseries widgets and
                    // world map widgets.
                    if (!doNotValidateYAxis &&
                        option.value.kind === types_1.FieldValueKind.FUNCTION) {
                        const primaryOutput = (0, fields_1.aggregateFunctionOutputType)(option.value.meta.name, undefined);
                        if (primaryOutput) {
                            // If a function returns a specific type, then validate it.
                            return (0, fields_1.isLegalYAxisType)(primaryOutput);
                        }
                    }
                    return option.value.kind === types_1.FieldValueKind.FUNCTION;
                }} filterAggregateParameters={option => {
                    // Only validate function parameters for timeseries widgets and
                    // world map widgets.
                    if (doNotValidateYAxis) {
                        return true;
                    }
                    if (fieldValue.kind !== 'function') {
                        return true;
                    }
                    const functionName = fieldValue.function[0];
                    const primaryOutput = (0, fields_1.aggregateFunctionOutputType)(functionName, option.value.meta.name);
                    if (primaryOutput) {
                        return (0, fields_1.isLegalYAxisType)(primaryOutput);
                    }
                    if (option.value.kind === types_1.FieldValueKind.FUNCTION) {
                        // Functions are not legal options as an aggregate/function parameter.
                        return false;
                    }
                    return (0, fields_1.isLegalYAxisType)(option.value.meta.dataType);
                }}/>
            {fields.length > 1 && (<button_1.default size="zero" borderless onClick={event => handleRemove(event, i)} icon={<icons_1.IconDelete />} title={(0, locale_1.t)('Remove this Y-Axis')} label={(0, locale_1.t)('Remove this Y-Axis')}/>)}
          </exports.QueryFieldWrapper>);
        })}
      {!hideAddYAxisButton && (<div>
          <button_1.default size="small" icon={<icons_1.IconAdd isCircled/>} onClick={handleAdd}>
            {(0, locale_1.t)('Add Overlay')}
          </button_1.default>
        </div>)}
    </field_1.default>);
}
const StyledColumnEditCollection = (0, styled_1.default)(columnEditCollection_1.default) `
  margin-top: ${(0, space_1.default)(1)};
`;
exports.QueryFieldWrapper = (0, styled_1.default)('div') `
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: ${(0, space_1.default)(1)};

  > * + * {
    margin-left: ${(0, space_1.default)(1)};
  }
`;
exports.default = WidgetQueryFields;
//# sourceMappingURL=widgetQueryFields.jsx.map