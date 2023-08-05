Object.defineProperty(exports, "__esModule", { value: true });
const tslib_1 = require("tslib");
const prop_types_1 = (0, tslib_1.__importDefault)(require("prop-types"));
const Metadata = prop_types_1.default.shape({
    value: prop_types_1.default.string,
    message: prop_types_1.default.string,
    directive: prop_types_1.default.string,
    type: prop_types_1.default.string,
    title: prop_types_1.default.string,
    uri: prop_types_1.default.string,
});
const Avatar = prop_types_1.default.shape({
    avatarType: prop_types_1.default.oneOf(['letter_avatar', 'upload', 'gravatar']),
    avatarUuid: prop_types_1.default.string,
});
/**
 * A User is someone that has registered on Sentry
 */
const User = prop_types_1.default.shape({
    avatar: Avatar,
    avatarUrl: prop_types_1.default.string,
    dateJoined: prop_types_1.default.string,
    email: prop_types_1.default.string,
    emails: prop_types_1.default.arrayOf(prop_types_1.default.shape({
        is_verified: prop_types_1.default.bool,
        id: prop_types_1.default.string,
        email: prop_types_1.default.string,
    })),
    has2fa: prop_types_1.default.bool,
    hasPasswordAuth: prop_types_1.default.bool,
    id: prop_types_1.default.string,
    identities: prop_types_1.default.array,
    isActive: prop_types_1.default.bool,
    isManaged: prop_types_1.default.bool,
    lastActive: prop_types_1.default.string,
    lastLogin: prop_types_1.default.string,
    username: prop_types_1.default.string,
});
const EventOrGroupType = prop_types_1.default.oneOf([
    'error',
    'csp',
    'hpkp',
    'expectct',
    'expectstaple',
    'default',
    'transaction',
]);
const Group = prop_types_1.default.shape({
    id: prop_types_1.default.string.isRequired,
    annotations: prop_types_1.default.array,
    assignedTo: User,
    count: prop_types_1.default.string,
    culprit: prop_types_1.default.string,
    firstSeen: prop_types_1.default.string,
    hasSeen: prop_types_1.default.bool,
    isBookmarked: prop_types_1.default.bool,
    isPublic: prop_types_1.default.bool,
    isSubscribed: prop_types_1.default.bool,
    lastSeen: prop_types_1.default.string,
    level: prop_types_1.default.string,
    logger: prop_types_1.default.string,
    metadata: Metadata,
    numComments: prop_types_1.default.number,
    permalink: prop_types_1.default.string,
    project: prop_types_1.default.shape({
        name: prop_types_1.default.string,
        slug: prop_types_1.default.string,
    }),
    shareId: prop_types_1.default.string,
    shortId: prop_types_1.default.string,
    status: prop_types_1.default.string,
    statusDetails: prop_types_1.default.object,
    title: prop_types_1.default.string,
    type: EventOrGroupType,
    userCount: prop_types_1.default.number,
});
const Team = prop_types_1.default.shape({
    id: prop_types_1.default.string.isRequired,
    slug: prop_types_1.default.string.isRequired,
});
const Project = prop_types_1.default.shape({
    // snuba returns id as number
    id: prop_types_1.default.oneOfType([prop_types_1.default.string, prop_types_1.default.number]).isRequired,
    slug: prop_types_1.default.string.isRequired,
    // snuba results may not contain a `name` or `isBookmarked
    teams: prop_types_1.default.arrayOf(Team),
    name: prop_types_1.default.string,
    isBookmarked: prop_types_1.default.bool,
    status: prop_types_1.default.string,
});
const Organization = prop_types_1.default.shape({
    id: prop_types_1.default.string.isRequired,
});
exports.default = {
    Group,
    Organization,
    Project,
    User,
};
//# sourceMappingURL=sentryTypes.jsx.map