CREATE SCHEMA IF NOT EXISTS `analytics`;

CREATE TABLE IF NOT EXISTS `analytics.dim_borrower` (
  borrower_id INT64,
  borrower_name STRING,
  borrower_type STRING,
  industry STRING,
  tax_id STRING,
  country STRING,
  state STRING,
  city STRING,
  postal_code STRING,
  inception_date DATE,
  annual_revenue NUMERIC,
  employees INT64
);

CREATE TABLE IF NOT EXISTS `analytics.dim_facility` (
  facility_id INT64,
  borrower_id INT64,
  facility_type STRING,
  limit_amount NUMERIC,
  currency STRING,
  origination_date DATE,
  maturity_date DATE,
  interest_rate_floor_bps INT64,
  covenants_count INT64
);


CREATE TABLE IF NOT EXISTS `analytics.dim_loan` (
  loan_id INT64,
  borrower_id INT64,
  facility_id INT64,
  index_id INT64,
  loan_number STRING,
  status STRING,
  origination_date DATE,
  maturity_date DATE,
  principal_amount NUMERIC,
  currency STRING,
  purpose STRING,
  loan_type STRING,
  margin_bps INT64,
  amortization_type STRING,
  payment_frequency STRING,
  compounding STRING,
  index_name STRING,
  tenor_months INT64,
  index_currency STRING
);

CREATE TABLE IF NOT EXISTS `analytics.dim_collateral` (
  collateral_id INT64,
  loan_id INT64,
  collateral_type STRING,
  value_amount NUMERIC,
  currency STRING,
  valuation_date DATE,
  lien_position STRING,
  location_country STRING,
  location_state STRING
);

CREATE TABLE IF NOT EXISTS `analytics.dim_date` (
  date_key INT64,
  date DATE,
  year INT64,
  quarter STRING,
  month INT64,
  day INT64
);

CREATE TABLE IF NOT EXISTS `analytics.dim_guarantor` (
  guarantor_id INT64,
  borrower_id INT64,
  guarantor_name STRING,
  guarantor_type STRING,
  guarantee_type STRING,
  max_liability_amount NUMERIC,
  currency STRING,
  credit_score INT64,
  ownership_pct NUMERIC
);

CREATE TABLE IF NOT EXISTS `analytics.dim_rate_index` (
  index_id INT64,
  index_name STRING,
  tenor_months INT64,
  index_currency STRING,
  rate_type STRING,
  day_count_convention STRING,
  published_by STRING
);

CREATE TABLE IF NOT EXISTS `analytics.dim_risk_rating` (
  rating_id INT64,
  loan_id INT64,
  borrower_id INT64,
  rating_agency STRING,
  rating_grade STRING,
  score NUMERIC,
  effective_date DATE,
  expiry_date DATE
);

CREATE TABLE IF NOT EXISTS `analytics.fact_loan_snapshot` (
  loan_id INT64,
  borrower_id INT64,
  facility_id INT64,
  snapshot_date_key INT64,
  snapshot_date DATE,
  outstanding_principal NUMERIC,
  current_rate_pct NUMERIC,
  margin_bps INT64,
  rating_grade STRING,
  score NUMERIC
);

CREATE TABLE IF NOT EXISTS `analytics.dim_syndicate_member` (
  member_id INT64,
  bank_name STRING,
  role STRING,
  bank_rating STRING,
  country STRING
);

CREATE TABLE IF NOT EXISTS `analytics.fact_payments` (
  payment_id INT64,
  date_key INT64,
  payment_date DATE,
  loan_id INT64,
  borrower_id INT64,
  facility_id INT64,
  index_id INT64,
  index_name STRING,
  tenor_months INT64,
  payment_amount NUMERIC,
  principal_component NUMERIC,
  interest_component NUMERIC,
  fee_component NUMERIC,
  days_past_due INT64,
  currency STRING,
  payment_method STRING,
  margin_bps INT64
);
