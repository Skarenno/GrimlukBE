\c accountdb

CREATE TABLE public.account (
	account_id varchar NOT NULL,
	CONSTRAINT account_pk PRIMARY KEY (account_id)
);