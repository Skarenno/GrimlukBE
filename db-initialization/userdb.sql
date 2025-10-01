\c userdb

CREATE TABLE public.residence_address (
	id varchar NOT NULL,
	residence_address_1 varchar NOT NULL,
	residence_address_2 varchar NULL,
	postal_code varchar NOT NULL,
	city varchar NOT NULL,
	country varchar NOT NULL,
	province varchar NOT NULL,
	residence_type varchar NOT NULL,
	CONSTRAINT residence_address_pk PRIMARY KEY (id)
);


CREATE TABLE public."user" (
	id varchar NOT NULL,
	tax_code varchar(16) NULL,
	"name" varchar NULL,
	surname varchar NULL,
	mail varchar NULL,
	username varchar NULL,
	residence_id varchar NULL,
	phone varchar NULL,
	gender bpchar(1) NULL,
	CONSTRAINT user_pk PRIMARY KEY (id),
	CONSTRAINT user_residence_address_fk FOREIGN KEY (residence_id) REFERENCES public.residence_address(id)
);


CREATE TABLE public.access_log (
	user_id varchar NULL,
	access_timestamp varchar NULL,
	ip_address varchar NULL,
	CONSTRAINT access_log_credentials_fk FOREIGN KEY (user_id) REFERENCES public.user(id)
);


CREATE TABLE public.user_credentials (
	username varchar NOT NULL,
	"password" varchar NOT NULL,
	created_at varchar DEFAULT CURRENT_TIMESTAMP NOT NULL,
	CONSTRAINT credentials_unique PRIMARY KEY (username)
);




-- TEST DATA INSERTION
INSERT INTO public.residence_address
(id, residence_address_1, residence_address_2, postal_code, city, country, province, residence_type)
VALUES('1', 'CAPPELLA III TRAV', NULL, '80070', 'MONTE DI PROCIDA', 'ITALY', 'NA', 'VIA');

INSERT INTO public."user" (id,tax_code,"name",surname,mail,username,residence_id,phone,gender) VALUES
	 ('1','TSTBVN99S04F839N','Bonaventura Salvatore','Testa','zqaz1234@gmail.com','zqaz1234@gmail.com','1','3755222244','M');

