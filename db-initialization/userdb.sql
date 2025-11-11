\c userdb



CREATE TABLE public."user" (
	id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	username varchar NULL,
	tax_code varchar(16) NOT NULL,
	name varchar NULL,
	surname varchar NULL,
	birth_date DATE NOT NULL,
	mail varchar NULL,
	phone varchar NULL,
	gender bpchar(1) NULL,	
	residence_address_1 varchar NULL,
	residence_address_2 varchar NULL,
	postal_code varchar NULL,
	city varchar NULL,
	country varchar NULL,
	province varchar NULL,
	CONSTRAINT user_unique UNIQUE (username)
);

CREATE TABLE public.user_credentials (
	username varchar NOT NULL,
	"password" varchar NOT NULL,
	created_at varchar DEFAULT CURRENT_TIMESTAMP NOT NULL,
	CONSTRAINT credentials_unique PRIMARY KEY (username)
);


CREATE TABLE public.access_log (
	id serial4 NOT NULL,
	username varchar NULL,
	access_timestamp timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	ip_address varchar NULL,
	successful bool NULL,
	CONSTRAINT access_log_unique UNIQUE (id)
);





-- TEST DATA INSERTION
INSERT INTO public."user" (username,tax_code,"name",surname,birth_date, mail,phone,gender, residence_address_1, residence_address_2, postal_code, city, country, province) VALUES
	 ('zqaz1234@gmail.com','TSTBVN99S04F839N','Bonaventura Salvatore','Testa','1999-11-04 00:00:00','zqaz1234@gmail.com','3755222244','M', 'VIA CAPPELLA III TRAV', NULL, '80070', 'MONTE DI PROCIDA', 'ITALY', 'NA');

INSERT INTO public.user_credentials
(username, "password", created_at)
VALUES('zqaz1234@gmail.com', '$2b$12$AcN/2E5NptjPH1GobVLGFueFMxnakpcBQsINsLWoeUFWm1he.qGmC', '2025-10-05 14:41:45.145642+00');


