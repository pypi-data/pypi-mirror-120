Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const react_1 = require("react");
const styled_1 = (0, tslib_1.__importDefault)(require("@emotion/styled"));
const item_1 = (0, tslib_1.__importDefault)(require("app/components/activity/item"));
const space_1 = (0, tslib_1.__importDefault)(require("app/styles/space"));
const body_1 = (0, tslib_1.__importDefault)(require("./body"));
const editorTools_1 = (0, tslib_1.__importDefault)(require("./editorTools"));
const header_1 = (0, tslib_1.__importDefault)(require("./header"));
const input_1 = (0, tslib_1.__importDefault)(require("./input"));
class Note extends react_1.Component {
    constructor() {
        super(...arguments);
        this.state = {
            editing: false,
        };
        this.handleEdit = () => {
            this.setState({ editing: true });
        };
        this.handleEditFinish = () => {
            this.setState({ editing: false });
        };
        this.handleDelete = () => {
            const { onDelete } = this.props;
            onDelete(this.props);
        };
        this.handleCreate = (note) => {
            const { onCreate } = this.props;
            if (onCreate) {
                onCreate(note);
            }
        };
        this.handleUpdate = (note) => {
            const { onUpdate } = this.props;
            onUpdate(note, this.props);
            this.setState({ editing: false });
        };
    }
    render() {
        const { modelId, user, dateCreated, text, authorName, hideDate, minHeight, showTime, projectSlugs, } = this.props;
        const activityItemProps = {
            hideDate,
            showTime,
            id: `activity-item-${modelId}`,
            author: {
                type: 'user',
                user,
            },
            date: dateCreated,
        };
        if (!this.state.editing) {
            return (<ActivityItemWithEditing {...activityItemProps} header={<header_1.default authorName={authorName} user={user} onEdit={this.handleEdit} onDelete={this.handleDelete}/>}>
          <body_1.default text={text}/>
        </ActivityItemWithEditing>);
        }
        // When editing, `NoteInput` has its own header, pass render func
        // to control rendering of bubble body
        return (<StyledActivityItem {...activityItemProps}>
        {() => (<input_1.default modelId={modelId} minHeight={minHeight} text={text} onEditFinish={this.handleEditFinish} onUpdate={this.handleUpdate} onCreate={this.handleCreate} projectSlugs={projectSlugs}/>)}
      </StyledActivityItem>);
    }
}
const StyledActivityItem = (0, styled_1.default)(item_1.default) `
  /* this was nested under ".activity-note.activity-bubble" */
  ul {
    list-style: disc;
  }

  h1,
  h2,
  h3,
  h4,
  p,
  ul:not(.nav),
  ol,
  pre,
  hr,
  blockquote {
    margin-bottom: ${(0, space_1.default)(2)};
  }

  ul:not(.nav),
  ol {
    padding-left: 20px;
  }

  p {
    a {
      word-wrap: break-word;
    }
  }

  blockquote {
    font-size: 15px;
    background: ${p => p.theme.gray200};

    p:last-child {
      margin-bottom: 0;
    }
  }
`;
const ActivityItemWithEditing = (0, styled_1.default)(StyledActivityItem) `
  &:hover {
    ${editorTools_1.default} {
      display: inline-block;
    }
  }
`;
exports.default = Note;
//# sourceMappingURL=index.jsx.map