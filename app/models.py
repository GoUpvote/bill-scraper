from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, ForeignKey, Table, BigInteger
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship
from app.database.base import Base
from datetime import datetime

class ActiveStorageAttachment(Base):
    __tablename__ = 'active_storage_attachments'

    id = Column(BigInteger, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    record_type = Column(String, nullable=False)
    record_id = Column(BigInteger, nullable=False)
    blob_id = Column(BigInteger, nullable=False)
    created_at = Column(DateTime, nullable=False)


class ActiveStorageBlob(Base):
    __tablename__ = 'active_storage_blobs'

    id = Column(BigInteger, primary_key=True, nullable=False)
    key = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    content_type = Column(String)
    meta_data = Column(Text)
    service_name = Column(String, nullable=False)
    byte_size = Column(BigInteger, nullable=False)
    checksum = Column(String)
    created_at = Column(DateTime, nullable=False)


class ActiveStorageVariantRecord(Base):
    __tablename__ = 'active_storage_variant_records'

    id = Column(BigInteger, primary_key=True, nullable=False)
    blob_id = Column(BigInteger, nullable=False)
    variation_digest = Column(String, nullable=False)


class AdminUpload(Base):
    __tablename__ = 'admin_uploads'

    id = Column(BigInteger, primary_key=True, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class ArInternalMetadatum(Base):
    __tablename__ = 'ar_internal_metadata'

    key = Column(String, primary_key=True, nullable=False)
    value = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class BatchImport(Base):
    __tablename__ = 'batch_imports'

    id = Column(BigInteger, primary_key=True, nullable=False)
    state_code = Column(String)
    url = Column(String)
    status = Column(String, default='new')
    counts = Column(Text)
    dir_prefix = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class BillInstance(Base):
    __tablename__ = 'bill_instances'

    id = Column(BigInteger, primary_key=True, nullable=False)
    legiscan_bill_id = Column(BigInteger)
    client_legiscan_bill_id = Column(BigInteger)
    legiscan_bill_text_id = Column(BigInteger)
    user_id = Column(BigInteger)
    edited_text = Column(Text)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    owner_id = Column(Integer)


class BillTextCodeSection(Base):
    __tablename__ = 'bill_text_code_sections'

    id = Column(BigInteger, primary_key=True, nullable=False)
    legiscan_bill_text_id = Column(BigInteger)
    legiscan_bill_id = Column(BigInteger)
    state_code = Column(String)
    chapter = Column(String)
    section = Column(String)
    impact = Column(String)
    description = Column(Text)
    readable = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class BillUpdate(Base):
    __tablename__ = 'bill_updates'

    id = Column(BigInteger, primary_key=True, nullable=False)
    legiscan_bill_id = Column(BigInteger)
    update_type = Column(String)
    notifications_sent = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    meta_data = Column(Text)


class ClientLegiscanBill(Base):
    __tablename__ = 'client_legiscan_bills'

    id = Column(BigInteger, primary_key=True, nullable=False)
    client_id = Column(BigInteger)
    legiscan_bill_id = Column(BigInteger)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    sentiment = Column(String, default='watch')


class ClientLegislativeTag(Base):
    __tablename__ = 'client_legislative_tags'

    id = Column(BigInteger, primary_key=True, nullable=False)
    client_id = Column(BigInteger)
    legislative_tag_id = Column(BigInteger)
    tier = Column(Integer)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class ClientState(Base):
    __tablename__ = 'client_states'

    id = Column(BigInteger, primary_key=True, nullable=False)
    client_id = Column(BigInteger)
    state_id = Column(BigInteger)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class Client(Base):
    __tablename__ = 'clients'

    id = Column(BigInteger, primary_key=True, nullable=False)
    organization_id = Column(BigInteger)
    name = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    self_org = Column(Boolean, default=False)
    recommendations_generated = Column(Boolean, default=False)


class CodeSection(Base):
    __tablename__ = 'code_sections'

    id = Column(BigInteger, primary_key=True, nullable=False)
    legiscan_bill_id = Column(BigInteger)
    state_code = Column(String)
    chapter = Column(String)
    section = Column(String)
    impact = Column(String)
    description = Column(Text)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    readable = Column(String)


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(BigInteger, primary_key=True, nullable=False)
    bill_instance_id = Column(BigInteger)
    user_id = Column(BigInteger)
    comment = Column(Text)
    commented_on_text = Column(Text)
    comment_type = Column(String)
    start_idx = Column(Integer)
    end_idx = Column(Integer)
    key_point_idx = Column(Integer)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    orphaned = Column(Boolean, default=False)
    original_created_at = Column(DateTime)
    comment_hash = Column(String)


class CommitteeTracking(Base):
    __tablename__ = 'committee_trackings'

    id = Column(BigInteger, primary_key=True, nullable=False)
    user_id = Column(BigInteger)
    legiscan_committee_id = Column(BigInteger)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    needs_notification = Column(Boolean, default=False)


class CommitteeUpdate(Base):
    __tablename__ = 'committee_updates'

    id = Column(BigInteger, primary_key=True, nullable=False)
    legiscan_committee_id = Column(BigInteger)
    update_type = Column(String)
    notifications_sent = Column(Boolean, default=False)
    meta_data = Column(Text)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    legiscan_bill_id = Column(Integer)


class ConstituentLegislativeTag(Base):
    __tablename__ = 'constituent_legislative_tags'

    id = Column(BigInteger, primary_key=True, nullable=False)
    constituent_id = Column(BigInteger)
    legislative_tag_id = Column(BigInteger)
    tier = Column(Integer, default=1)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class Constituent(Base):
    __tablename__ = 'constituents'

    id = Column(BigInteger, primary_key=True, nullable=False)
    name = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class Conversation(Base):
    __tablename__ = 'conversations'

    id = Column(BigInteger, primary_key=True, nullable=False)
    user_id = Column(BigInteger)
    legiscan_bill_id = Column(BigInteger)
    is_visible = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class EventLog(Base):
    __tablename__ = 'event_logs'

    id = Column(BigInteger, primary_key=True, nullable=False)
    event_key = Column(String)
    meta_data = Column(Text)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class Global(Base):
    __tablename__ = 'globals'

    id = Column(BigInteger, primary_key=True, nullable=False)
    key = Column(String)
    value = Column(Text)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class Invite(Base):
    __tablename__ = 'invites'

    id = Column(BigInteger, primary_key=True, nullable=False)
    organization_id = Column(BigInteger)
    code = Column(String)
    email = Column(String)
    org_role = Column(String)
    status = Column(String, default='sent')
    accepted_at = Column(DateTime)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class KeywordPhraseBill(Base):
    __tablename__ = 'keyword_phrase_bills'

    id = Column(BigInteger, primary_key=True, nullable=False)
    keyword_phrase_id = Column(BigInteger)
    legiscan_bill_id = Column(BigInteger)
    is_initial = Column(Boolean, nullable=False)
    notified_at = Column(DateTime)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class KeywordPhraseState(Base):
    __tablename__ = 'keyword_phrase_states'

    id = Column(BigInteger, primary_key=True, nullable=False)
    keyword_phrase_id = Column(BigInteger)
    state_id = Column(BigInteger)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class KeywordPhrase(Base):
    __tablename__ = 'keyword_phrases'

    id = Column(BigInteger, primary_key=True, nullable=False)
    user_id = Column(BigInteger)
    phrase = Column(String)
    every_state = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class LegiscanActionBill(Base):
    __tablename__ = 'legiscan_action_bills'

    id = Column(BigInteger, primary_key=True, nullable=False)
    legiscan_action_id = Column(BigInteger)
    legiscan_bill_id = Column(BigInteger)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class LegiscanAction(Base):
    __tablename__ = 'legiscan_actions'

    id = Column(BigInteger, primary_key=True, nullable=False)
    legiscan_bill_id = Column(BigInteger)
    creation_date = Column(String)
    action_date = Column(String)
    action_type = Column(String)
    location = Column(String)
    action_time = Column(String)
    bill_committee = Column(String)
    chamber = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    is_cancelled = Column(Boolean, default=False)
    event_hash = Column(String)
    description = Column(String)
    state_code = Column(String)
    name = Column(String)
    is_scraped = Column(Boolean, default=False)
    other_bills = Column(String)


class LegiscanAmendment(Base):
    __tablename__ = 'legiscan_amendments'

    id = Column(BigInteger, primary_key=True, nullable=False)
    legiscan_bill_id = Column(BigInteger)
    amendment_id = Column(Integer)
    adopted = Column(Integer)
    chamber = Column(String)
    chamber_id = Column(Integer)
    amendment_date = Column(String)
    title = Column(String)
    description = Column(Text)
    mime = Column(String)
    mime_id = Column(Integer)
    url = Column(String)
    state_link = Column(String)
    amendment_size = Column(Integer)
    amendment_hash = Column(String)
    doc = Column(Text)
    amendment_text = Column(Text)
    alt_amendment = Column(Integer)
    alt_mime = Column(String)
    alt_mime_id = Column(Integer)
    alt_state_link = Column(String)
    alt_amendment_size = Column(Integer)
    alt_amendment_hash = Column(String)
    alt_doc = Column(Text)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    amendment_type = Column(String, default='regular')
    parsed_status = Column(String)


class LegiscanBillAssociation(Base):
    __tablename__ = 'legiscan_bill_associations'

    id = Column(BigInteger, primary_key=True, nullable=False)
    from_bill_id = Column(Integer)
    to_bill_id = Column(Integer)
    association_type = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class LegiscanBillLegislativeTag(Base):
    __tablename__ = 'legiscan_bill_legislative_tags'

    id = Column(BigInteger, primary_key=True, nullable=False)
    legiscan_bill_id = Column(BigInteger)
    legislative_tag_id = Column(BigInteger)
    tier = Column(Integer, default=1)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class LegiscanBillPerson(Base):
    __tablename__ = 'legiscan_bill_persons'

    id = Column(BigInteger, primary_key=True, nullable=False)
    legiscan_bill_id = Column(BigInteger)
    legiscan_person_id = Column(BigInteger)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class LegiscanBillSearchObject(Base):
    __tablename__ = 'legiscan_bill_search_objects'

    id = Column(BigInteger, primary_key=True, nullable=False)
    legiscan_bill_id = Column(BigInteger)
    title = Column(Text)
    gpt_title = Column(Text)
    gpt_summary = Column(Text)
    bill_number = Column(String)
    bill_text = Column(Text)
    key_points = Column(Text)
    tags = Column(Text)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    gpt_description = Column(Text)
    state_code = Column(String)


class LegiscanBillTag(Base):
    __tablename__ = 'legiscan_bill_tags'

    id = Column(BigInteger, primary_key=True, nullable=False)
    legiscan_bill_id = Column(BigInteger)
    legiscan_tag_id = Column(BigInteger)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class LegiscanBillText(Base):
    __tablename__ = 'legiscan_bill_texts'

    id = Column(BigInteger, primary_key=True, nullable=False)
    doc_id = Column(Integer)
    bill_id = Column(Integer)
    bill_date = Column(String)
    bill_type = Column(String)
    type_id = Column(String)
    mime = Column(String)
    mime_id = Column(Integer)
    url = Column(String)
    state_link = Column(String)
    text_size = Column(Integer)
    text_hash = Column(String)
    doc = Column(Text)
    bill_text = Column(Text)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    gpt_title = Column(String)
    gpt_summary = Column(Text)
    gpt_key_points = Column(Text)
    gpt_pros = Column(Text)
    gpt_cons = Column(Text)
    gpt_processed = Column(Boolean, default=False)
    gpt_tags_processed = Column(Boolean, default=False)
    legiscan_bill_id = Column(Integer)
    tags_set_in_pinecone = Column(Boolean, default=False)
    gpt_description = Column(Text)
    pinecone_loaded = Column(Boolean, default=False)
    pinecone_chunk_length = Column(Integer)
    langchain_generated = Column(Boolean, default=False)
    llm_model_name = Column(String)
    bill_text_code_sections_generated = Column(Boolean, default=False)
    entry_source = Column(String, default='ingest')
    is_merged = Column(Boolean, default=True)


class LegiscanBillVersionBillText(Base):
    __tablename__ = 'legiscan_bill_version_bill_texts'

    id = Column(BigInteger, primary_key=True, nullable=False)
    legiscan_bill_version_id = Column(BigInteger)
    legiscan_bill_text_id = Column(BigInteger)


class LegiscanBillVersion(Base):
    __tablename__ = 'legiscan_bill_versions'

    id = Column(BigInteger, primary_key=True, nullable=False)
    legiscan_bill_id = Column(BigInteger)
    bill_id = Column(Integer)
    url = Column(String)
    state_link = Column(String)
    completed = Column(Integer)
    number = Column(String)
    change_hash = Column(String)
    status_date = Column(String)
    status = Column(String)
    last_action_date = Column(String)
    last_action = Column(String)
    title = Column(String)
    description = Column(String)
    progress = Column(Text)
    state = Column(String)
    state_id = Column(Integer)
    bill_number = Column(String)
    bill_type = Column(String)
    bill_type_id = Column(String)
    body = Column(String)
    body_id = Column(Integer)
    current_body = Column(String)
    current_body_id = Column(Integer)
    pending_committee_id = Column(Integer)
    committee = Column(Text)
    referrals = Column(Text)
    history = Column(Text)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    sasts = Column(Text)
    amendments = Column(Text)
    actions_parsed = Column(Boolean, default=False)
    calendar = Column(Text)
    entry_source = Column(String, default='ingest')
    is_merged = Column(Boolean, default=True)


class LegiscanBill(Base):
    __tablename__ = 'legiscan_bills'

    id = Column(BigInteger, primary_key=True, nullable=False)
    legiscan_session_id = Column(BigInteger)
    bill_id = Column(Integer)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    introduced_date = Column(String)
    legiscan_committee_id = Column(Integer)
    chamber = Column(String)
    bill_type = Column(String)
    subcommittee = Column(String)
    last_action_date = Column(String)
    signed_by_governor = Column(Boolean, default=False)
    parent_id = Column(Integer)
    current_stage = Column(String)
    has_roll_call = Column(Boolean, default=False)
    readable_bill_number = Column(String)
    state_code = Column(String)
    pinecone_loaded = Column(Boolean, default=False)
    langchain_generated = Column(Boolean, default=False)
    langchain_processed = Column(Boolean, default=False)
    code_sections_generated = Column(Boolean, default=False)
    pinecone_chunk_length = Column(Integer)
    llm_model_name = Column(String)
    current_bill_number = Column(String)
    current_title = Column(String)
    current_state_link = Column(String)
    current_gpt_title = Column(String)
    current_gpt_description = Column(Text)
    current_gpt_summary = Column(Text)
    has_bill_text = Column(Boolean, default=False)
    entry_source = Column(String, default='ingest')
    is_merged = Column(Boolean, default=True)


class LegiscanCommittee(Base):
    __tablename__ = 'legiscan_committees'

    id = Column(BigInteger, primary_key=True, nullable=False)
    legiscan_person_id = Column(BigInteger)
    state_code = Column(String)
    name = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    chamber = Column(String)
    legiscan_committee_id = Column(Integer)
    chamber_id = Column(Integer)


class LegiscanEvent(Base):
    __tablename__ = 'legiscan_events'

    id = Column(BigInteger, primary_key=True, nullable=False)
    legiscan_bill_id = Column(BigInteger)
    event_date = Column(String)
    action = Column(String)
    chamber = Column(String)
    chamber_id = Column(Integer)
    importance = Column(Integer)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    hidden = Column(Boolean, default=False)
    entry_source = Column(String, default='ingest')


class LegiscanImportJson(Base):
    __tablename__ = 'legiscan_import_jsons'

    id = Column(BigInteger, primary_key=True, nullable=False)
    batch_import_id = Column(BigInteger)
    object_type = Column(String)
    json_text = Column(Text)
    status = Column(String, default='new')
    error_message = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class LegiscanPersonVersion(Base):
    __tablename__ = 'legiscan_person_versions'

    id = Column(BigInteger, primary_key=True, nullable=False)
    legiscan_person_id = Column(BigInteger)
    person_hash = Column(String)
    state_id = Column(Integer)
    party_id = Column(String)
    party = Column(String)
    role_id = Column(Integer)
    role = Column(String)
    name = Column(String)
    first_name = Column(String)
    middle_name = Column(String)
    last_name = Column(String)
    suffix = Column(String)
    nickname = Column(String)
    district = Column(String)
    ftm_eid = Column(Integer)
    votesmart_id = Column(Integer)
    opensecrets_id = Column(String)
    knowwho_pid = Column(Integer)
    ballotpedia = Column(String)
    bioguide_id = Column(String)
    committee_sponsor = Column(Integer)
    committee_id = Column(Integer)
    state_federal = Column(Integer)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class LegiscanPerson(Base):
    __tablename__ = 'legiscan_persons'

    id = Column(BigInteger, primary_key=True, nullable=False)
    people_id = Column(Integer)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    is_committee = Column(Boolean, default=False)
    first_name = Column(String)
    last_name = Column(String)


class LegiscanRawJsonStateObjectStat(Base):
    __tablename__ = 'legiscan_raw_json_state_object_stats'

    id = Column(BigInteger, primary_key=True, nullable=False)
    state_code = Column(String)
    time_frame = Column(String)
    object_type = Column(String)
    object_count = Column(Integer, default=0)
    median_response_time_ms = Column(Integer)
    median_processing_time_ms = Column(Integer)
    median_go_live_time_ms = Column(Integer)
    median_creation_to_live_time_ms = Column(Integer)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class LegiscanRollCallVote(Base):
    __tablename__ = 'legiscan_roll_call_votes'

    id = Column(BigInteger, primary_key=True, nullable=False)
    legiscan_roll_call_id = Column(BigInteger)
    legiscan_person_id = Column(BigInteger)
    vote_id = Column(Integer)
    vote_text = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class LegiscanRollCall(Base):
    __tablename__ = 'legiscan_roll_calls'

    id = Column(BigInteger, primary_key=True, nullable=False)
    legiscan_bill_id = Column(BigInteger)
    roll_call_id = Column(Integer)
    roll_call_date = Column(String)
    desc = Column(String)
    yea = Column(Integer)
    nay = Column(Integer)
    nv = Column(Integer)
    absent = Column(Integer)
    total = Column(Integer)
    passed = Column(Integer)
    chamber = Column(String)
    chamber_id = Column(Integer)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    is_floor_vote = Column(Boolean, default=False)


class LegiscanSearchResult(Base):
    __tablename__ = 'legiscan_search_results'

    id = Column(BigInteger, primary_key=True, nullable=False)
    legiscan_bill_id = Column(BigInteger)
    params_hash = Column(Text)
    score = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class LegiscanSession(Base):
    __tablename__ = 'legiscan_sessions'

    id = Column(BigInteger, primary_key=True, nullable=False)
    session_id = Column(Integer)
    state_code = Column(String)
    state_id = Column(Integer)
    year_start = Column(Integer)
    year_end = Column(Integer)
    prefile = Column(Integer)
    sine_die = Column(Integer)
    prior = Column(Integer)
    special = Column(Integer)
    session_tag = Column(String)
    session_title = Column(String)
    session_name = Column(String)
    dataset_hash = Column(String)
    session_hash = Column(String)
    name = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class LegiscanSupplement(Base):
    __tablename__ = 'legiscan_supplements'

    id = Column(BigInteger, primary_key=True, nullable=False)
    legiscan_bill_id = Column(BigInteger)
    supplement_id = Column(Integer)
    supplement_date = Column(String)
    type_id = Column(Integer)
    supplement_type = Column(String)
    title = Column(String)
    description = Column(Text)
    mime = Column(String)
    mime_id = Column(Integer)
    url = Column(String)
    state_link = Column(String)
    supplement_size = Column(Integer)
    supplement_hash = Column(String)
    doc = Column(Text)
    alt_supplement = Column(Integer)
    alt_mime = Column(String)
    alt_mime_id = Column(Integer)
    alt_state_link = Column(String)
    alt_supplement_size = Column(Integer)
    alt_supplement_hash = Column(String)
    alt_doc = Column(Text)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class LegiscanTag(Base):
    __tablename__ = 'legiscan_tags'

    id = Column(BigInteger, primary_key=True, nullable=False)
    name = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class LegislativeTag(Base):
    __tablename__ = 'legislative_tags'

    id = Column(BigInteger, primary_key=True, nullable=False)
    name = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class LobbyistConstituent(Base):
    __tablename__ = 'lobbyist_constituents'

    id = Column(BigInteger, primary_key=True, nullable=False)
    lobbyist_id = Column(BigInteger)
    constituent_id = Column(BigInteger)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class Lobbyist(Base):
    __tablename__ = 'lobbyists'

    id = Column(BigInteger, primary_key=True, nullable=False)
    email = Column(String)
    state = Column(String)
    name = Column(String)
    address_one_line = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class Message(Base):
    __tablename__ = 'messages'

    id = Column(BigInteger, primary_key=True, nullable=False)
    conversation_id = Column(BigInteger)
    message_type = Column(String)
    body = Column(Text)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class Notification(Base):
    __tablename__ = 'notifications'

    id = Column(BigInteger, primary_key=True, nullable=False)
    user_id = Column(BigInteger)
    legiscan_bill_id = Column(BigInteger)
    notification_type = Column(String)
    seen = Column(Boolean, default=False)
    meta_data = Column(Text)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    portal_id = Column(Integer)


class OffloadedBillText(Base):
    __tablename__ = 'offloaded_bill_texts'

    id = Column(BigInteger, primary_key=True, nullable=False)
    legiscan_bill_text_id = Column(BigInteger)
    doc = Column(Text)
    bill_text = Column(Text)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class OrganizationState(Base):
    __tablename__ = 'organization_states'

    id = Column(BigInteger, primary_key=True, nullable=False)
    organization_id = Column(BigInteger)
    state_id = Column(BigInteger)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class Organization(Base):
    __tablename__ = 'organizations'

    id = Column(BigInteger, primary_key=True, nullable=False)
    name = Column(String)
    paid_full_access_license_count = Column(Integer, default=0)
    paid = Column(Boolean, default=False)
    total_payment_amount = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    paid_readonly_license_count = Column(Integer, default=0)
    multi_state = Column(Boolean, default=False)
    portal_license_count = Column(Integer, default=0)


class Payment(Base):
    __tablename__ = 'payments'

    id = Column(BigInteger, primary_key=True, nullable=False)
    user_id = Column(BigInteger)
    payment_date = Column(String)
    end_date = Column(String)
    amount = Column(String)
    notes = Column(Text)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    organization_id = Column(Integer)


class PortalUser(Base):
    __tablename__ = 'portal_users'

    id = Column(BigInteger, primary_key=True, nullable=False)
    portal_id = Column(BigInteger)
    user_id = Column(BigInteger)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    invite_code = Column(String)
    invite_claimed = Column(Boolean, default=False)
    invited_by_user_id = Column(Integer)
    status = Column(String, default='invite_sent')


class Portal(Base):
    __tablename__ = 'portals'

    id = Column(BigInteger, primary_key=True, nullable=False)
    title = Column(String)
    description = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    organization_id = Column(BigInteger)
    client_id = Column(BigInteger)
    is_archived = Column(Boolean, default=False)


class PythonJob(Base):
    __tablename__ = 'python_jobs'

    id = Column(BigInteger, primary_key=True, nullable=False)
    status = Column(String, default='new')
    job_type = Column(String)
    object_id = Column(Integer)
    content = Column(Text)
    meta_data = Column(postgresql.JSONB)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    scheduled_at = Column(DateTime)


class RawLegiscanJson(Base):
    __tablename__ = 'raw_legiscan_jsons'

    id = Column(BigInteger, primary_key=True, nullable=False)
    status = Column(String, default='new')
    raw_json = Column(Text)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    object_type = Column(String)
    responded_at = Column(DateTime)
    processed_at = Column(DateTime)
    live_at = Column(DateTime)
    legiscan_bill_id = Column(Integer)
    internal_object_id = Column(Integer)
    state_code = Column(String)


class Recommendation(Base):
    __tablename__ = 'recommendations'

    id = Column(BigInteger, primary_key=True, nullable=False)
    client_id = Column(BigInteger)
    legiscan_bill_id = Column(BigInteger)
    score = Column(String)
    score_explain = Column(Text)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class Referral(Base):
    __tablename__ = 'referrals'

    id = Column(BigInteger, primary_key=True, nullable=False)
    user_id = Column(BigInteger)
    referred_user_id = Column(Integer)
    bonus_claimed = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class Response(Base):
    __tablename__ = 'responses'

    id = Column(BigInteger, primary_key=True, nullable=False)
    user_id = Column(BigInteger)
    question = Column(String)
    answer = Column(Integer)
    identifier = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    version = Column(String, default='1')


class SchemaMigration(Base):
    __tablename__ = 'schema_migrations'

    version = Column(String, primary_key=True, nullable=False)


class ShareRecipient(Base):
    __tablename__ = 'share_recipients'

    id = Column(BigInteger, primary_key=True, nullable=False)
    share_id = Column(BigInteger)
    email = Column(String)
    sent = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class Share(Base):
    __tablename__ = 'shares'

    id = Column(BigInteger, primary_key=True, nullable=False)
    user_id = Column(BigInteger)
    legiscan_bill_id = Column(BigInteger)
    share_code = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class StateUniqueEventAction(Base):
    __tablename__ = 'state_unique_event_actions'

    id = Column(BigInteger, primary_key=True, nullable=False)
    state_id = Column(BigInteger)
    action = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class StateUniqueRollCallDesc(Base):
    __tablename__ = 'state_unique_roll_call_descs'

    id = Column(BigInteger, primary_key=True, nullable=False)
    state_id = Column(BigInteger)
    roll_call_desc = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class State(Base):
    __tablename__ = 'states'

    id = Column(BigInteger, primary_key=True, nullable=False)
    name = Column(String)
    state_code = Column(String)
    is_live = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    legiscan_state_id = Column(Integer)
    bill_count = Column(Integer, default=0)
    bill_text_count = Column(Integer, default=0)
    bill_text_pinecone_loaded_count = Column(Integer, default=0)
    bill_text_langchain_generated_count = Column(Integer, default=0)
    bill_text_code_sections_generated_count = Column(Integer, default=0)
    caches_last_refreshed_at = Column(DateTime)


class SurveyCandidateScore(Base):
    __tablename__ = 'survey_candidate_scores'

    id = Column(BigInteger, primary_key=True, nullable=False)
    user_id = Column(BigInteger)
    survey_candidate_id = Column(BigInteger)
    score = Column(Integer)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class SurveyCandidate(Base):
    __tablename__ = 'survey_candidates'

    id = Column(BigInteger, primary_key=True, nullable=False)
    json_id = Column(Integer)
    name = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class SurveyParty(Base):
    __tablename__ = 'survey_parties'

    id = Column(BigInteger, primary_key=True, nullable=False)
    json_id = Column(Integer)
    name = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class SurveyPersona(Base):
    __tablename__ = 'survey_personas'

    id = Column(BigInteger, primary_key=True, nullable=False)
    json_id = Column(Integer)
    name = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class Tagging(Base):
    __tablename__ = 'taggings'

    id = Column(BigInteger, primary_key=True, nullable=False)
    tag_id = Column(BigInteger)
    legiscan_bill_id = Column(BigInteger)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(BigInteger, primary_key=True, nullable=False)
    user_id = Column(BigInteger)
    name = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    portal_id = Column(Integer)


class Term(Base):
    __tablename__ = 'terms'

    id = Column(BigInteger, primary_key=True, nullable=False)
    terms_of_service = Column(Text)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class Tracking(Base):
    __tablename__ = 'trackings'

    id = Column(BigInteger, primary_key=True, nullable=False)
    user_id = Column(BigInteger)
    legiscan_bill_id = Column(BigInteger)
    needs_notification = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    sentiment = Column(String, default='watch')
    portal_id = Column(Integer)


class UserClient(Base):
    __tablename__ = 'user_clients'

    id = Column(BigInteger, primary_key=True, nullable=False)
    user_id = Column(BigInteger)
    client_id = Column(BigInteger)
    owner = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class UserConstituentLegislativeTag(Base):
    __tablename__ = 'user_constituent_legislative_tags'

    id = Column(BigInteger, primary_key=True, nullable=False)
    user_id = Column(BigInteger)
    constituent_id = Column(BigInteger)
    legislative_tag_id = Column(BigInteger)
    tier = Column(Integer, default=1)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)


class User(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, nullable=False)
    provider = Column(String, nullable=False, default='email')
    uid = Column(String, nullable=False, default='')
    email = Column(String, nullable=False, default='')
    encrypted_password = Column(String, nullable=False, default='')
    reset_password_token = Column(String)
    reset_password_sent_at = Column(DateTime)
    allow_password_change = Column(Boolean, default=True)
    remember_created_at = Column(DateTime)
    sign_in_count = Column(Integer, nullable=False, default=0)
    current_sign_in_at = Column(DateTime)
    last_sign_in_at = Column(DateTime)
    current_sign_in_ip = Column(String)
    last_sign_in_ip = Column(String)
    tokens = Column(String)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    first_name = Column(String)
    last_name = Column(String)
    street = Column(String)
    street_line2 = Column(String)
    city = Column(String)
    state = Column(String)
    zip = Column(String)
    is_admin = Column(Boolean, default=False)
    last_tos_agreed_to = Column(Integer, default=0)
    referral_code = Column(String)
    bonus_months = Column(Integer, default=0)
    referred_by_code = Column(String)
    feed_last_fetched_at = Column(DateTime)
    auth_key = Column(String)
    newsletter_opted_in = Column(Boolean, default=False)
    source = Column(String, default='app')
    engagement_score = Column(Integer, default=0)
    survey_paid = Column(Boolean, default=False)
    influencer_code = Column(String)
    influencer_id = Column(BigInteger)
    survey_candidate_id = Column(Integer)
    survey_persona_id = Column(Integer)
    survey_party_id = Column(Integer)
    paid = Column(Boolean, default=False)
    api_token = Column(String)
    has_access = Column(Boolean, default=True)
    organization_id = Column(Integer)
    org_role = Column(String)
    can_auto_import_clients = Column(Boolean, default=False)
    has_auto_imported_clients = Column(Boolean, default=False)


class ViaPythonJob(Base):
    __tablename__ = 'via_python_jobs'

    id = Column(BigInteger, primary_key=True, nullable=False)
    status = Column(String, default='new')
    job_type = Column(String)
    object_id = Column(Integer)
    content = Column(Text)
    meta_data = Column(postgresql.JSONB)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
