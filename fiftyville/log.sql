-- Keep a log of any SQL queries you execute as you solve the mystery.

-- Query to find out more about the crime
SELECT description FROM crime_scene_reports WHERE month = 7 AND day = 28 AND street = 'Humphrey Street';
    -- Theft of the CS50 duck took place at 10:15am at the Humphrey Street bakery.
    -- Interviews were conducted today with three witnesses who were present at the time – each of their interview transcripts mentions the bakery.
    -- Littering took place at 16:36. No known witnesses.

-- Interviews
SELECT name FROM interviews WHERE month = 7 AND day = 28;
    -- Jose :
    SELECT transcript FROM interviews WHERE name = 'Jose';
        -- Transcript of Jose :  “Ah,” said he, “I forgot that I had not seen you for some weeks.
        -- It is a little souvenir from the King of Bohemia in return for my assistance in the case of the Irene Adler papers.”

    -- Eugene 1:
    SELECT transcript FROM interviews WHERE name = 'Eugene';
        -- Transcript of Eugene 1 : “I suppose,” said Holmes, “that when Mr. Windibank came back from France he was very annoyed at your having gone to the ball.”

    -- Barbara :
    SELECT transcript FROM interviews WHERE name = 'Barbara';
        -- Transcript of Barbara : “You had my note?” he asked with a deep harsh voice and a strongly marked German accent.
        -- “I told you that I would call.” He looked from one to the other of us, as if uncertain which to address.

    -- Ruth :
    SELECT transcript FROM interviews WHERE name = 'Ruth';
        -- Transcript of Ruth : “I will get her to show me.” Sometime within ten minutes of the theft, I saw the thief get into a car in the bakery parking lot and drive away.
        -- If you have security footage from the bakery parking lot, you might want to look for cars that left the parking lot in that time frame.

    -- Eugene 2:
    SELECT transcript FROM interviews WHERE name = 'Eugene';
        -- Transcript of Eugene 2 : I don't know the thief's name, but it was someone I recognized.
        -- Earlier this morning, before I arrived at Emma's bakery, I was walking by the ATM on Leggett Street and saw the thief there withdrawing some money.

    -- Raymond :
    SELECT transcript FROM interviews WHERE name = 'Raymond';
        -- Transcript of Raymond :  “Good-night, Mister Sherlock Holmes.” As the thief was leaving the bakery, they called someone who talked to them for less than a minute.
        -- In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow.
        -- The thief then asked the person on the other end of the phone to purchase the flight ticket.

    -- Lily :
    SELECT transcript FROM interviews WHERE name = 'Lily';
        -- Transcript of Lily :  Our neighboring courthouse has a very annoying rooster that crows loudly at 6am every day.
        -- My sons Robert and Patrick took the rooster to a city far, far away, so it may never bother us again. My sons have successfully arrived in Paris.

-- Three witnesses
    -- Ruth
    -- Eugene 2
    -- Raymond

-- Based on Ruth: Baker logs & security cams between 10:15 am and 10:25 am
-- Determine what year of the theft
    SELECT year FROM bakery_security_logs
    -- Year 2024

    -- Security log license_plate
    SELECT * FROM bakery_security_logs WHERE year = 2024 AND month = 7 AND day = 28 AND hour = 10 AND minute BETWEEN 15 AND 25;
        -- 5P2BI95, 94KL12X, 6P58WS2, 4328GD8, G412CB7, L93JTIZ, 322W7JE, 0NTHK55
        -- Get names for license plates
        SELECT p.name, b.activity, b.license_plate, b.year, b.month, b.day, b.hour, b.minute
        FROM bakery_security_logs b
        JOIN people p ON p.license_plate = b.license_plate
        WHERE b.year = 2024 AND b.month = 7 AND b.day = 28 AND b.hour = 10 AND b.minute BETWEEN 15 AND 25;
        -- Vanessa, Bruce, Barry, Luca, Sofia, Iman, Diana, Kelsey (In order above)

-- Based on Eugene: ATM transcations
-- Determine who used ATM before robbery
    SELECT * FROM atm_transactions WHERE atm_location = 'Leggett Street' AND year = 2024 AND month = 7 AND day = 28;
    -- 9 transactions with 8 withdraws
        SELECT a.*, p.name FROM atm_transactions a
        JOIN bank_accounts b ON a.account_number = b.account_number
        JOIN people p ON b.person_id = p.id
        WHERE a.atm_location = 'Leggett Street' AND a.year = 2024 AND a.month = 7 AND a.day = 28 AND a.transaction_type = 'withdraw';
        -- Bruce, Diana, Brooke, Kenny, Iman, Luca, Taylor, Benista

        -- Current suspects: Bruce, Diana, Iman, Luca

-- Based on Raymond : Calls that day under 60 seconds
    SELECT * FROM phone_calls WHERE year = 2024 AND month = 7 AND day = 28 AND duration < 60;
    -- 9 phone calls under 60 seconds
        ---------------+----------------+------+-------+-----+----------+
        SELECT p.name, p.caller, p.receiver, p.year, p.month, p.day, p.duration
        FROM phone_calls p
        JOIN people p ON p.caller = p.phone_number
        WHERE p.year = 2024 AND p.month = 7 AND p.day = 28 AND p.duration < 60;
        -- Callers: Sofia, Kelsey, Bruce, Kelsey, Taylor, Diana, Carina, Kenny, Benista

        -- Current suspects: Bruce, Diana

-- Flights
    -- Find airport id of Fiftyville
        SELECT * FROM airports;
        -- CSF = id 8
        -- Find the flights ordered by earliest
            SELECT f.*, origin.full_name AS origin_airport, destination.full_name AS destination_airport
            FROM flights f JOIN airports origin ON f.origin_airport_id = origin.id
            JOIN airports destination ON f.destination_airport_id = destination.id
            WHERE origin.id = 8 AND f.year = 2024 AND f.month = 7 AND f.day = 29 ORDER BY f.hour, f.minute;
            -- LaGuardia Aiport at 8:20 am with is in New York (36)
            -- Look at passenger list for Bruce or Diana
                SELECT p.name
                FROM people p
                JOIN passengers ps ON p.passport_number = ps.passport_number
                WHERE ps.flight_id = 36 AND p.name IN ('Bruce' , 'Diana');
                -- Name is Bruce
                -- Who is Bruce's accomplice
                    SELECT p2.name AS receiver
                    FROM phone_calls p JOIN people p1 ON p.caller = p1.phone_number
                    JOIN people p2 ON p.receiver = p2.phone_number
                    WHERE p1.name = 'Bruce' AND p.year = 2024 AND p.month = 7 AND p.day = 28 AND p.duration < 60;
                    -- Bruce called Robin

