# GROOMIE
#### Video Demo:  https://youtu.be/pWuCqrAB5Mk
#### Description:
# Groomie – Dog Grooming Appointment Booking System

## Overview
Drawing from inspiration of apps like ROVER and ZOCDOC I found a need for a pet grooming app that would simplify the experience for pet owners.

**Groomie** is a Flask-based web application that enables dog owners to find, book, and manage grooming appointments at salons in multiple Texas cities. The application combines a secure user authentication system, an appointment scheduler with double-booking prevention, and an intuitive user interface. Groomie is designed as a functional prototype but with a structure that can be extended into a full production service.

The application is backed by an **SQLite** database, chosen for its simplicity and portability, and uses **Werkzeug’s password hashing** to ensure credentials are stored securely. It also includes session-based authentication to restrict booking, viewing, and modifying appointments to logged-in users only.

---

## Features
- **User Registration & Login** – Create a new account, log in securely, and maintain a session.
- **Browse Groomers by City** – View preloaded salon details (name, address, phone, rating, description, and photo) for multiple cities.
- **Book Appointments** – Select a date and available time slot for your chosen groomer.
- **View Bookings** – See all your confirmed appointments in one place.
- **Reschedule Appointments** – Change the date or time of an existing booking.
- **Cancel Appointments** – Remove an appointment you no longer need.
- **Double-Booking Prevention** – Ensures the same groomer, date, and time slot cannot be booked by multiple users.

---

## File Structure

### `app.py`
This is the main application file containing:
- **Flask Initialization**: Creates the app instance and sets a secret key for session management.
- **Database Initialization (`init_db`)**:
  - Creates `users` and `bookings` tables if they don’t exist.
  - `users` stores unique usernames, emails, and hashed passwords.
  - `bookings` stores appointment details linked to a `user_id`.
- **Preloaded Groomers Dictionary**: Contains salon data for **Houston**, **Dallas**, **Austin**, and **San Antonio**. Each entry has a name, address, phone number, rating, description, and image.
- **Helper Functions**:
  - `get_time_slots()` – Generates half-hour slots from 8:00 AM to 5:00 PM.
  - `get_db_connection()` – Opens an SQLite connection with row access.
- **Routes**:
  - `/` – Redirects to login.
  - `/register` – Handles new user creation, with validation and password hashing.
  - `/login` – Authenticates and starts a user session.
  - `/logout` – Logs out the current user.
  - `/choose_city` – Lets users pick a city to see available groomers.
  - `/groomers/<city>` – Lists groomers for the selected city.
  - `/book/<city>/<groomer>` – Displays booking form and saves valid bookings.
  - `/confirmation` – Shows all current bookings for the logged-in user.
  - `/appointments` – Displays all appointments in date/time order.
  - `/cancel/<appointment_id>` – Deletes an appointment.
  - `/reschedule/<appointment_id>` – Updates appointment date/time.

---

### Templates (HTML)
The app has these template files in a `/templates` folder:
- **`register.html`** – Registration form.
- **`login.html`** – Login form.
- **`choose_city.html`** – City selection dropdown.
- **`groomers.html`** – Displays groomers in the selected city.
- **`book.html`** – Booking form for chosen groomer/date/time.
- **`confirmation.html`** – Lists bookings for confirmation.
- **`appointments.html`** – Displays and manages upcoming appointments.
- **`reschedule.html`** – Form for updating appointment time.

Each template extends a base layout (`base.html`) with a navigation bar, flash messages, and consistent styling.

---

## Database Schema

Below is two databases, but in future designs could potentially hold more data of groomers being added to the system who choose to be a part of groomie increasing its potential for new clients and new cities.

### `users` Table
| Column   | Type    | Details |
|----------|---------|---------|
| id       | INTEGER | Primary key |
| username | TEXT    | Unique, required |
| email    | TEXT    | Unique, required |
| password | TEXT    | Hashed password |

### `bookings` Table
| Column       | Type    | Details |
|--------------|---------|---------|
| id           | INTEGER | Primary key |
| user_id      | INTEGER | Foreign key to `users` |
| city         | TEXT    | Booking city |
| groomer_name | TEXT    | Groomer’s name |
| time_slot    | TEXT    | Appointment time |

---

## Design Choices

### 1. Flask Framework
Flask was chosen for its lightweight nature, making it ideal for quick development without unnecessary complexity. It’s flexible enough for small-scale prototypes and easy to expand later.

### 2. SQLite Database
SQLite’s architecture makes it easy to set up and run locally without additional software. It’s perfect for testing and small deployments.

### 3. Preloaded Groomer Data
For this prototype, groomer details are stored in a Python dictionary instead of a database table. A future enhancement would involve storing and managing groomers in a database.

### 4. Password Security
Passwords are hashed with `generate_password_hash()` from `werkzeug.security`. Storing plain-text passwords is avoided to ensure security.

### 5. Session-Based Authentication
User login state is stored in Flask’s `session` object to protect booking-related routes.

### 6. Double-Booking Prevention
The booking process checks the database for existing records with the same city, groomer, date, and time before confirming.

---

## Enhancements for Further Development

### 1. Admin Panel – Manage groomer entries and view all bookings.

### 2. Email/SMS Reminders – Notify users of upcoming appointments.

### 3. User Profile Management – Allow updating usernames, emails, and passwords.

### 4. Search and Filters – Find groomers by rating, services, or proximity.

### 5. Mobile App Integration – Create API endpoints for iOS/Android apps.

### Conclusion

Groomie showcases a complete booking flow—from registration and browsing services to scheduling, managing, and cancelling appointments. While the current version uses hardcoded groomer data and a lightweight SQLite backend, the modular design makes it easy to expand with more robust features. It’s a strong base for a real-world grooming appointment system. I thoroughly enjoyed working on this project and conducting research to identify the most effective methods for implementing the application, as well as determining the features and requirements necessary for it to become fully operational.

## Running the Application

### Requirements
- Python 3.x
- Flask
- Werkzeug

### Installation
```bash
git clone <repository_url>
cd groomie
pip install flask werkzeug
