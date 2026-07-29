
BEFORE

| id  | name  | address        |
| --- | ---   | ---            |
| 1   | Harry | 4 Privet Drive |
| 2   | Ron   | The Burrow     |



AFTER

| id  | name  | address            |
| --- | ---   | ---                |
| 1   | Harry | 12 Grimmauld Place |
| 2   | Ron   | The Burrow         |




















Slowly Changing Dimension Type 2


| id  | start_date | end_date   | name  | address            |
| --- | ---        | ---        | ---   | ---                |
| 1   | 1981-10-31 | 1996-07-01 | Harry | 4 Privet Drive     |
| 1   | 1996-07-01 | 9999-12-31 | Harry | 12 Grimmauld Place |
| 2   | 1990-01-01 | 9999-12-31 | Ron   | The Burrow         |
