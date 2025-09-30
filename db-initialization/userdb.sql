\c userdb

CREATE TABLE public."user" (
	id varchar NOT NULL,
	tax_code varchar(16) NULL,
	CONSTRAINT user_pk PRIMARY KEY (id)
);