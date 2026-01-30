USE DATABASE DEMO;
USE SCHEMA PUBLIC;

ALTER WAREHOUSE compute_wh RESUME;

CREATE
OR REPLACE TABLE patient_visits (
    visit_id     STRING NOT NULL,
    patient_id   STRING NOT NULL,
    visit_date   DATE NOT NULL,
    department   STRING NOT NULL,
    visit_cost   NUMBER(10, 2) NOT NULL,
    is_emergency BOOLEAN NOT NULL
);

SELECT * FROM demo.public.patient_visits;




-- PUT file:///tmp/demo/patient_visit_2026_01_01.csv @~;
LIST @~;






-- load data
COPY INTO demo.public.patient_visits
FROM @~ 
FILE_FORMAT = (
    TYPE = CSV
    SKIP_HEADER = 1
);

SELECT * FROM demo.public.patient_visits;



-- day 3
COPY INTO demo.public.patient_visits
FROM @~ 
FILE_FORMAT = (
    TYPE = CSV
    SKIP_HEADER = 1
    ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE
);






-- day 3 - show errors
COPY INTO demo.public.patient_visits
FROM @~ 
FILE_FORMAT = (
    TYPE = CSV
    SKIP_HEADER = 1
    ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE
)
VALIDATION_MODE = RETURN_ERRORS;






-- clean up user stage
LIST @~;

REMOVE @~;







-- reload data with PURGE
COPY INTO demo.public.patient_visits
FROM @~ 
FILE_FORMAT = (
    TYPE = CSV
    SKIP_HEADER = 1
    ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE
)
PURGE = TRUE;


SELECT * FROM demo.public.patient_visits;

TRUNCATE TABLE demo.public.patient_visits;

LIST @~;








DROP TABLE demo.public.patient_visits;
