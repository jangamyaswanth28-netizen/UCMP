
CREATE INDEX idx_current_user ON consent_current(user_id);
CREATE INDEX idx_current_status ON consent_current(status);
CREATE INDEX idx_event_user_type_seq ON consent_events(user_id, consent_type_id, sequence_number);
CREATE INDEX idx_event_timestamp ON consent_events(event_timestamp);
CREATE INDEX idx_consent_code ON consent_types(consent_code);
