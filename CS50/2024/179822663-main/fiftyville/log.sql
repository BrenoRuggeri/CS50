-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT * FROM crime_scene_reports
WHERE street = 'Humphrey Street';

-- Transcripts mentions the bakery.
SELECT * FROM interviews
WHERE transcript LIKE '%bakery%';

-- FOLLOWING THE SUGESTION OFF RUTH AND LOOKING AT bakery_security_logs in the day of theft.
SELECT * FROM bakery_security_logs
WHERE day = 28 AND hour = 10 AND minute BETWEEN 15 and 25;

-- SEARCHING FOR THE NAME OF PERSON WITH THE license_plate.
SELECT name FROM people
JOIN bakery_security_logs ON bakery_security_logs.license_plate = people.license_plate
WHERE year = 2023 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25;

-- FOLLOWING THE SUGESTION OF EUGENE AND LOOKING WHO WITHDRAW MONEY IN THE ATM on Leggett Street.
-- LOOKING THE NAME OF PERSON WHO WITHDRAW MONEY IN ATM AND COMPARING WITH THE NAME OF DRIVERS WHO LEAVES THE BAKERY.

SELECT name FROM people
JOIN bank_accounts ON bank_accounts.person_id = people.id
JOIN atm_transactions ON atm_transactions.account_number = bank_accounts.account_number
WHERE day = 28 AND atm_location = 'Leggett Street';

-- SUSPECTS: BRUCE, DIANA, LUCA, IMAN
-- FOLLOWING THE SUGESTION OFF RAYMOND AND LOOKING WHO MAKE A CALL WITH SHORT DURATION.

SELECT * FROM phone_calls
WHERE day = 28 AND duration <60;

-- LOOKING FOR NAME OF CALLER.

SELECT name FROM people
JOIN phone_calls ON phone_calls.caller = people.phone_number
WHERE day = 28 AND duration <60;

-- SUSPECTS NAMES: BRUCE, DIANA.

-- LOOKING THE ID OF AIRPORT OF FIFTYVILLE.
SELECT * FROM airports
WHERE city LIKE '%fiftyville%';

-- LOOKING AT THE FLIGHTS WHERE origin_airport_id IS FIFTYVILLE AND THE DAY IS 29.
SELECT * FROM flights
WHERE origin_airport_id = 8 AND day = 29;

-- ACORDING TO RAYMOND THE SUSPECT WILL TAKE THE EARLIER FLY IN THE MORNING, IN THIS CASE FLY ID 36.
-- THE destination_airport_id FROM THE FLY 36 is 4.
-- NOW LETS DISCOVERY THE full_name OF THE AIRPORT ID 4.
SELECT full_name FROM airports
WHERE id = 4;

-- NOW LETS TAKE A LOOK IN WHAT CITY THE LaGuardia Airport is.

SELECT city FROM airports
WHERE id =4;


-- LOOKING WICH ONE OF SUSPECT ARE IN THE LIST OF FLY ID 36.

SELECT name FROM people
JOIN passengers ps ON people.passport_number = ps.passport_number
WHERE flight_id = 36;

-- BRUCE IS THE ONLY SUSPECT IS IN THE FLIGHT.
-- NOW TO FIND THE ACCOMPLICE I GONNA CHECK FOR WHO BRUCE CALLS.
-- THE NUMBER OF THE PEOPLE WHO RECEIVER THE BRUCE CALLS IS (375) 555-8161.
-- SO LETS FOUND THE NAME OF THE RECEIVER.

SELECT name FROM people
WHERE phone_number LIKE '%(375) 555-8161%';

-- THE ACCOMPLICE IS ROBIN.
