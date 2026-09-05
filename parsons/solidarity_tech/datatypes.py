"""Types, Enums, and TypedDicts for known Solidarity Tech values."""

from __future__ import annotations

import numbers
from enum import Enum
from typing import Any, Literal, TypedDict

# Type Aliases

CompareValueType = str | numbers.Rational | bool


# Enums


class AttendanceStatus(Enum):
    """Attendance statuses for an event RSVP."""

    YES = "yes"
    NO = "no"
    MAYBE = "maybe"
    WAITLISTED = "waitlisted"


class EventType(Enum):
    """Event types for a Solidarity Tech event."""

    VIRTUAL = "virtual"
    IN_PERSON = "in_person"
    HYBRID = "hybrid"


class FieldType(Enum):
    """Field types for Solidarity Tech user properties."""

    INPUT = "input"
    TEXT_AREA = "textarea"
    NUMBER = "number"
    DATE = "date"
    CHECKBOX = "checkbox"
    SELECT = "select"
    RADIOS = "radios"
    CHECKBOXES = "checkboxes"


class InviteType(Enum):
    """Methods used to invite Solidarity Tech team members."""

    SMS = "sms"
    EMAIL = "email"


class ScopeType(Enum):
    """Scopes for Solidarity Tech records."""

    ORGANIZATION = "Organization"
    CHAPTER = "Chapter"


class InteractionType(Enum):
    """Types of interactions recorded in Solidarity Tech user notes."""

    IN_PERSON = "in_person"
    CALL = "call"
    TEXT = "text"
    EMAIL = "email"


# TypedDicts (Component / Sub-types First)


class UserPropertyDataValue(TypedDict):
    label: dict[str, Any]
    value: str


class ActionData(TypedDict):
    id: int
    user_id: int
    agent_user_id: int | None
    field_type: str | None
    old_value: str | None
    new_value: str | None
    data_import_id: int | None
    created_at: str
    updated_at: str


class TranscriptData(TypedDict):
    summary: str | None
    rating: int | None
    sentiment: str | None
    engagement_analysis: str | None
    engagement_analysis_justification: str | None


class DonationChargeDataChapter(TypedDict):
    id: int
    name: str


class DonationChargeDataUser(TypedDict):
    id: int
    email: str
    first_name: str
    last_name: str
    phone_number: str
    created_at: str
    address1: str | None
    address2: str | None
    city: str | None
    state: str | None
    zip_code: str | None
    country_name: str | None


class DonationChargeDataActionPage(TypedDict):
    id: int
    title: str
    url_slug: str


class AddressData(TypedDict):
    address1: str | None
    address2: str | None
    city: str | None
    state: str | None
    zip_code: str | None
    country: str | None


# --- TypedDicts (Main Entities) ---


class UserPropertyData(TypedDict):
    id: int
    name: str
    key: str
    field_type: FieldType
    options: list[UserPropertyDataValue] | None
    scope_id: int | None
    scope_type: ScopeType | None


class ActivityData(TypedDict):
    id: int
    user_id: int
    name: str
    actionable_id: int
    actionable_type: str
    action: ActionData
    created_at: str
    updated_at: str


class ActivityMetadata(TypedDict):
    total_count: int | None
    limit: int
    offset: int
    cursor: int | None
    next_cursor: int | None


class AgentAssignmentData(TypedDict):
    id: int
    agent_user_id: int
    user_id: int
    created_at: str
    is_active: bool


class CallData(TypedDict):
    id: int
    user_id: int
    chapter_id: int | None
    direction: str
    from_number: str | None
    to_number: str | None
    phonebank_id: int | None
    agent_user_id: int | None
    notes: str | None
    duration: int
    picked_up: bool
    left_voicemail: bool
    twilio_call_sid: str
    created_at: str
    ended_at: str | None
    transcription: TranscriptData | None


class ChapterData(TypedDict):
    id: int
    name: str
    logo_url: str
    organization_id: int
    chapter_phone_number: str
    calendar_feed_url: str


class DonationChargeData(TypedDict):
    id: int
    amount: int
    created_at: str
    updated_at: str
    success: bool
    refunded: bool
    receipt_number: str
    hash_id: str
    processing_fee_cents: int | None
    external_donation_id: str | None
    external_donation_date: str | None
    is_external: bool
    amount_in_dollars: str
    currency: str
    currency_symbol: str
    receipt_url: str
    brand: str
    last4: str
    json: dict[str, Any]
    user: DonationChargeDataUser
    action_page: DonationChargeDataActionPage
    chapter: DonationChargeDataChapter


# The format of this has to be different because "from" is a reserved keyword in Python
EmailSenderData = TypedDict(
    "EmailSenderData",
    {
        "id": int,
        "name": str,
        "email": str,
        "from": str,
        "default_for_scope": bool,
        "scope_type": str,
        "scope_id": int,
        "created_at": str,
    },
)


class FieldSurveyURL(TypedDict):
    url: str
    expires_at: str


class QueryRule(TypedDict):
    id: str
    type: str
    operator: str
    value: CompareValueType | list[CompareValueType]


class QueryParams(TypedDict):
    condition: Literal["AND", "OR"]
    valid: bool
    rules: list[QueryRule]


class UserRelationshipData(TypedDict):
    id: str
    text: str


class UserData(TypedDict):
    id: int
    hash_id: str
    phone_number: str | None
    email: str | None
    first_name: str | None
    last_name: str | None
    alternate_name: str | None
    preferred_language: str
    second_language: str | None
    chapter_id: int
    chapter_ids: list[int]
    branch_id: int | None
    created_at: str
    custom_user_properties: dict[str, str | list[str]]
    address: AddressData
    sms_permission: bool
    call_permission: bool
    email_permission: bool
    other_emails: list[str]
    other_phone_numbers: list[str]


class UserMergeMetadata(TypedDict):
    message: str
    primary_user_id: int
    merged_user_ids: list[int]
    merged_count: int
    not_found_user_ids: list[int] | None


class UserDeleteMetadata(TypedDict):
    message: str
    id: int | None
