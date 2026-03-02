
-- Sample Consent Type
INSERT INTO consent_types (consent_type_id, consent_code, description, is_mandatory)
VALUES (gen_random_uuid(), 'EMAIL_MARKETING', 'Email Marketing Consent', false);
