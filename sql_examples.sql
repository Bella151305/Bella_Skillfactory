-- create db

DROP TABLE IF EXISTS classrooms CASCADE;
CREATE TABLE classrooms (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    teacher VARCHAR(100)
);


DROP TABLE IF EXISTS students CASCADE;
CREATE TABLE students (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(100),
    classroom_id INT,
    CONSTRAINT fk_classrooms
        FOREIGN KEY(classroom_id)
        REFERENCES classrooms(id)
);


INSERT INTO classrooms
    (teacher)
VALUES
    ('Mary'),
    ('Jonah');


INSERT INTO students
    (name, classroom_id)
 VALUES
    ('Adam', 1),
    ('Betty', 1),
    ('Caroline', 2);


-- Explicitly specify NULL
INSERT INTO students
    (name, classroom_id)
VALUES
    ('Dina', NULL);

-- Implicitly specify NULL
INSERT INTO students
    (name)
VALUES
    ('Evan');


DROP TABLE IF EXISTS assignments CASCADE;
CREATE TABLE assignments (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    category VARCHAR(20),
    name VARCHAR(200),
    due_date DATE,
    weight FLOAT
);


DROP TABLE IF EXISTS grades CASCADE;
CREATE TABLE grades (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    assignment_id INT,
    score INT,
    student_id INT,
    CONSTRAINT fk_assignments
        FOREIGN KEY(assignment_id)
        REFERENCES assignments(id),
    CONSTRAINT fk_students
        FOREIGN KEY(student_id)
        REFERENCES students(id)
);


/* Replace the FROM line with the path to your CSV */
COPY assignments(category, name, due_date, weight)
FROM 'C:/Users/mgsosna/Desktop/db_data/assignments.csv'
DELIMITER ','
CSV HEADER;

/* Replace the FROM line with the path to your CSV */
COPY grades(assignment_id, score, student_id)
FROM 'C:/Users/mgsosna/Desktop/db_data/grades.csv'
DELIMITER ','
CSV HEADER;


ALTER TABLE students
ADD best_friend_id INT;

UPDATE students
SET best_friend_id = 5
WHERE id = 1;

UPDATE students
SET best_friend_id = 4
WHERE id = 2;

UPDATE students
SET best_friend_id = 2
WHERE id = 3;

UPDATE students
SET best_friend_id = 2
WHERE id = 4;

UPDATE students
SET best_friend_id = 1
WHERE id = 5;


-- filtering and queries, operations on sets

SELECT
    student_id,
    ROUND(AVG(score),1) AS avg_score
FROM
    grades
WHERE
    score BETWEEN 50 AND 75
GROUP BY
    student_id
ORDER BY
    student_id;
    
  
SELECT
    student_id,
    ROUND(AVG(score),1) AS avg_score
FROM
    grades
GROUP BY
    student_id
HAVING
    ROUND(AVG(score),1) BETWEEN 50 AND 75
ORDER BY
    student_id;
    
    
SELECT
    student_id,
    ROUND(AVG(score),1) AS avg_score
FROM
    grades AS g
INNER JOIN
    assignments AS a
    ON a.id = g.assignment_id
WHERE
    a.category = 'homework'
GROUP BY
    student_id
HAVING
    ROUND(AVG(score),1) BETWEEN 50 AND 75;
    
    
SELECT
    score,
    CASE
        WHEN score < 60 THEN 'F'
        WHEN score < 70 THEN 'D'
        WHEN score < 80 THEN 'C'
        WHEN score < 90 THEN 'B'
        ELSE 'A'
    END AS letter
FROM
    grades;


SELECT
    name,
    teacher,
    CASE
        WHEN teacher IS NOT NULL THEN teacher
        ELSE name
    END AS instructor
FROM
    students AS s
LEFT JOIN
    classrooms AS c
    ON c.id = s.classroom_id;
    
    
SELECT
    name,
    teacher,
    COALESCE(teacher, name) AS instructor
FROM
    students AS s
LEFT JOIN
    classrooms AS c
    ON c.id = s.classroom_id;
    
    
SELECT
    COALESCE(NULL, NULL, NULL, 4);
/*
 coalesce
 --------
        4
 */

 SELECT
    COALESCE(NULL, NULL, NULL);
/*
 coalesce
 --------
 [null]
 */
 
 
 SELECT
    s.name,
    g.score,
    a.category
FROM
    students AS s
INNER JOIN
    grades AS g
    ON s.id = g.student_id
INNER JOIN
    assignments AS a
    ON a.id = g.assignment_id
WHERE
    s.name = 'Adam';
    
    
SELECT
    *
FROM (
    SELECT
        name,
        'Name starts with A/B' as reason
    FROM
        students
    WHERE
        LEFT(name,1) IN ('A', 'B')
) AS x

UNION ALL -- UNION ALL возвращает все строки, в то время как UNION убирает дубли

SELECT
    *
FROM (
    SELECT
        name,
        'Name is 5 letters long' AS reason
    FROM
        students
    WHERE
        LENGTH(name) = 5
) AS y;


SELECT
    *
FROM
    students
WHERE
    id IN (1,2,3)

INTERSECT

SELECT
    *
FROM
    students
WHERE
    id IN (2,3,4);

/*
 id | name     | classroom_id
 -- | -------- | ------------
  2 | Betty    |            1
  3 | Caroline |            2
*/


SELECT
    *
FROM
    students
WHERE
    id IN (1,2,3)

EXCEPT

SELECT
    *
FROM
    students
WHERE
    id IN (2,3,4);

/*
 id | name     | classroom_id
 -- | -------- | ------------
  1 | Adam     |            1
*/


SELECT
    name,
    ARRAY_AGG(score) AS scores
FROM
    students AS s
INNER JOIN
    grades AS g
    ON s.id = g.student_id
GROUP BY
    name
ORDER BY
    name;
    
/*
 name     | scores
 -------- | ------
 Adam     | {82,82,80,75,85}
 Betty    | {74,75,70,64,69}
 Caroline | {96,92,90,100,95}
 Dina     | {81,80,84,64,89}
 Evan     | {67,91,85,93,81}
*/


/*
CARDINALITY – выводит количество элементов в массиве.
ARRAY_REPLACE - заменяет указанные элементы.
ARRAY_REMOVE - удаляет указанные элемент.
UNNEST – противоположна функции ARRAY_AGG - позволяет разделить массив на отдельные строки.
*/


SELECT
    name,
    ARRAY_AGG(score) AS scores,
    CARDINALITY(ARRAY_AGG(score)) AS length,
    ARRAY_REPLACE(ARRAY_AGG(score), 82, NULL) AS replaced
FROM
    students AS s
INNER JOIN
    grades AS g
    ON s.id = g.student_id
GROUP BY
    name
ORDER BY
    name;
    
    
-- Самостоятельное объединение (self join)

ALTER TABLE students
ADD best_friend_id INT;

UPDATE students
SET best_friend_id = 5
WHERE id = 1;

UPDATE students
SET best_friend_id = 4
WHERE id = 2;

UPDATE students
SET best_friend_id = 2
WHERE id = 3;



SELECT
    x.name,
    y.name AS best_friend
FROM
    students AS x
INNER JOIN
    students AS y
    ON y.id = x.best_friend_id;

/*
 name     | best_friend
 -------- | -----------
 Adam     | Evan
 Betty    | Dina
 Caroline | Betty
 Dina     | Betty
 Evan     | Adam
*/


-- Оконные функции (Window functions)

SELECT
    s.name,
    g.score,
    AVG(g.score) OVER (
        PARTITION BY s.name
    )
FROM
    students AS s
INNER JOIN
    grades AS g
    ON s.id = g.student_id;

/*
 name  | score | avg
 ------| ----- | ----------
 Adam  |    82 | 80.8000...
 Adam  |    82 | 80.8000...
 Adam  |    80 | 80.8000...
 Adam  |    75 | 80.8000...
 Adam  |    85 | 80.8000...
 Betty |    74 | 70.4000...
 Betty |    75 | 70.4000...
 ...   |   ... |        ...
*/


SELECT
    s.name,
    g.score,
    RANK() OVER (
        ORDER BY g.score
    )
FROM
    grades AS g
INNER JOIN
    students AS s
    ON s.id = g.student_id;

/*
 name  | score | rank
 ----- | ----- | ----
 Betty |    64 |    1
 Dina  |    64 |    1
 Evan  |    67 |    3
 ...   |   ... |  ...
*/


SELECT
    s.name,
    g.score,
    RANK() OVER (
        PARTITION BY s.name  -- ranks by student
        ORDER BY g.score
    )
FROM
    grades AS g
INNER JOIN
    students AS s
    ON s.id = g.student_id;

/*
 name     | score | rank
 -------- | ----- | ----
 Adam     |    75 |    1
 Adam     |    80 |    2
 Adam     |    82 |    3
 Adam     |    82 |    3
 Adam     |    85 |    5
 Betty    |    64 |    1
 Betty    |    69 |    2
 Betty    |    70 |    3
 Betty    |    74 |    4
 Betty    |    75 |    5
 Caroline |    90 |    1
 Caroline |    92 |    2
 ...      |   ... |  ...
*/


-- Оператор WITH

SELECT
    s.name,
    ROUND(AVG(g.score),1) AS avg
FROM
    students AS s
INNER JOIN
    grades AS g
    ON s.id = g.student_id
GROUP BY
    s.name;

/*
 name     | avg
 -------- | ----
 Dina     | 79.6
 Evan     | 83.4
 Betty    | 70.4
 Caroline | 94.6
 Adam     | 80.8
*/


SELECT
    s.name,
    ROUND(AVG(g.score),1) AS avg,
    g.score > avg
    ...
    -- ERROR: column "avg" does not exist

SELECT
    s.name,
    ROUND(AVG(g.score),1) AS avg,
    g.score > ROUND(AVG(g.score),1)
    ...
    -- ERROR: column "g.score" must appear in the GROUP BY
    -- clause or be used in an aggregate function
    

WITH averages AS (
    SELECT
        s.id,
        ROUND(AVG(g.score),1) AS avg_score
    FROM
        students AS s
    INNER JOIN
        grades AS g
        ON s.id = g.student_id
    GROUP BY
        s.id
)
SELECT
    s.name,
    g.score,
    a.avg_score,
    g.score > a.avg_score AS above_avg
FROM
    students AS s
INNER JOIN
    grades AS g
    ON s.id = g.student_id
INNER JOIN
    averages AS a
    ON a.id = s.id;

/*
 name  | score | avg_score | above_avg
 ----- | ----- | --------- | ---------
 Adam  |    82 |      80.8 | true
 Adam  |    82 |      80.8 | true
 Adam  |    80 |      80.8 | false
 Adam  |    75 |      80.8 | false
 Adam  |    85 |      80.8 | true
 Betty |    74 |      70.4 | true
 Betty |    75 |      70.4 | true
*/


SELECT
    s.name
FROM
    students AS s
INNER JOIN
    grades AS g
    ON s.id = g.student_id
INNER JOIN
    assignments AS a
    ON a.id = g.assignment_id
GROUP BY
    s.name
HAVING
    SUM(g.score * a.weight) > 85;

/*
 name
 --------
 Caroline
*/


SELECT
    s.name
FROM
    students AS s
INNER JOIN
    grades AS g
    ON s.id = g.student_id
INNER JOIN
    assignments AS a
    ON a.id = g.assignment_id
WHERE
    a.name = 'biography'
    AND g.score > 70

/*
 name
 --------
 Adam
 Caroline
 Evan
*/


SELECT DISTINCT
    name
FROM
    students
WHERE
    name IN <people_who_passed_final>
    OR name IN <people_who_passed_project>;
    
    
WITH weighted_pass AS (
    SELECT
        s.name
    FROM
        students AS s
    INNER JOIN
        grades AS g
        ON s.id = g.student_id
    INNER JOIN
        assignments AS a
        ON a.id = g.assignment_id
    GROUP BY
        s.name
    HAVING
        SUM(g.score * a.weight) > 85
),
project_pass AS (
    SELECT
        s.name
    FROM
        students AS s
    INNER JOIN
        grades AS g
        ON s.id = g.student_id
    INNER JOIN
        assignments AS a
        ON a.id = g.assignment_id
    WHERE
        a.name = 'biography'
        AND g.score > 70
)
SELECT DISTINCT
    name
FROM
    students
WHERE
    name IN (SELECT name FROM weighted_pass)
    OR name IN (SELECT name FROM project_pass);

/*
 name
 --------
 Evan
 Caroline
 Adam
*/


-- EXPLAIN

EXPLAIN
SELECT
    s.id AS student_id,
    g.score
FROM
    students AS s
LEFT JOIN
    grades AS g
    ON s.id = g.student_id
WHERE
    g.score > 90
ORDER BY
    g.score DESC;
    
/*
 QUERY PLAN
 ----------
 Sort (cost=80.34..81.88 rows=617 width=8)
 [...] Sort Key: g.score DESC
 [...] -> Hash Join (cost=16.98..51.74 rows=617 width=8)
 [...] Hash Cond: (g.student_id = s.id)
 [...] -> Seq Scan on grades g (cost=0.00..33.13 rows=617 width=8)
 [...] Filter: (score > 90)
 [...] -> Hash (cost=13.10..13.10 rows=310 width=4)
 [...] -> Seq Scan on students s (cost=0.00..13.20 rows=320 width=4)
*/


EXPLAIN ANALYZE
SELECT
    s.id AS student_id,
    g.score
FROM
    students AS s
LEFT JOIN
    grades AS g
    ON s.id = g.student_id
WHERE
    g.score > 90
ORDER BY
    g.score DESC;
  
  
  
-- CASCADE

SELECT
    s.name,
    s.classroom_id,
    c.teacher
FROM
    students AS s
LEFT JOIN
    classrooms AS c
    ON c.id = s.classroom_id;

/*
 name     | classroom_id | teacher
 -------- | ------------ | -------
 Adam     |            1 | Mary
 Betty    |            1 | Mary
 Caroline |            2 | Jonah
 Dina     |       [null] | [null]
 Evan     |       [null] | [null]
*/

DROP TABLE classrooms CASCADE;

/*
DROP TABLE
Query returned successfully in 71 msec.
*/

SELECT * FROM students;

/*
 id | name     | classroom_id | best_friend_id
 -- | -------- | ------------ | --------------
  1 | Adam     |            1 |              5
  2 | Betty    |            1 |              4
  3 | Caroline |            2 |              2
  4 | Dina     |       [null] |              2
  5 | Evan     |       [null] |              1
*/


CREATE TABLE classrooms (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    teacher VARCHAR(100)
);

/*
CREATE TABLE
Query returned successfully in 139 msec.
*/

INSERT INTO classrooms
    (teacher)
VALUES
    ('Dr. Random'),
    ('Alien Banana');

/*
INSERT 0 2
Query returned successfully in 99 msec.
*/

SELECT
    s.name,
    s.classroom_id,
    c.teacher
FROM
    students AS s
LEFT JOIN
    classrooms AS c
    ON c.id = s.classroom_id;

/*
 name     | classroom_id | teacher
 -------- | ------------ | -----------
 Adam     |            1 | Dr. Random
 Betty    |            1 | Dr. Random
 Caroline |            2 | Alien Banana
 Dina     |       [null] | [null]
 Evan     |       [null] | [null]
*/


UPDATE students
SET classroom_id = 10
WHERE id = 1;

/*
UPDATE 1
Query returned successfully in 37 msec.
*/

UPDATE grades
SET student_id = 10
WHERE id = 1;
/*
ERROR:  insert or update on table "grades" violates foreign key
    constraint "fk_students"
DETAIL:  Key (student_id)=(10) is not present in table
    "students".
SQL state: 23503
*/


DROP TABLE IF EXISTS students CASCADE;

CREATE TABLE students (
    id INT PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    name VARCHAR(100),
    classroom_id INT,
    CONSTRAINT fk_classrooms
        FOREIGN KEY(classroom_id)
        REFERENCES classrooms(id) ON DELETE CASCADE
);

INSERT INTO students
    (name, classroom_id)
 VALUES
    ('Adam', 1),
    ('Betty', 1),
    ('Caroline', 2);

SELECT * FROM students;
/*
 id | name     | classroom_id
 -- | -------- | ------------
  1 | Adam     |            1
  2 | Betty    |            1
  3 | Caroline |            2
*/

DELETE FROM classrooms
WHERE id = 1;

SELECT * FROM students;
/*
 id | name     | classroom_id
 -- | -------- | ------------
  3 | Caroline |            2
*/


-- Оператор If

DO $$

BEGIN
    IF
        (SELECT COUNT(*) FROM grades) >
        (SELECT COUNT(*) FROM students)
    THEN
        RAISE NOTICE 'More grades than students.';
    ELSE
        RAISE NOTICE 'Equal or more students than grades.';
    END IF;

END $$;

/*
NOTICE: More grades than students.
*/


-- Индексы

CREATE INDEX
    score_index
ON
    grades(score);
