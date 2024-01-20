**Project**: fablabOS
**Author**: James Rutter
**Start Date**: Jan. 9, 2024

This is an ambitious project to build out a integrated set of systems and services to better improve the user experience at the Haystack Fab Lab. This design could be applied to other contexts, such as community makerspaces, university labs, fab labs, and communal studios. The goal is to utilize a series of open hardware devices, such as the RaspberryPi and Arduino to accomplish as much of the system as possible. This project will be open-source and shared and used as a learning opportunity for students of the Fab Lab.


# Project Structure 
- `/assets` static files utilized for GUI/front-end. Currently has `/images`, `/scripts`, and `/styles` to organize these areas. Images and other media files could be stored on a remote S3 service for better performance (e.g., Supabase). 
- `/api` is a Flask instance and the primary server engine handling API functions. 
- `/data` is where the database schema and sqlite db reside. Note: In the current implementation, the Flask instance (API) is generating its own db located in `/instance`, which is not being tracked and being used for development purposes. 
- 

# API Overview 
### Setup Database
Before starting a project, you need to initialize the database. Run the following command: 
- `flask --app api init-db`

This executes the schema file (schema.db) and builds the tables in sqlite. It does not populate it with any data. 

### Seed Database (optional)
To populate the database with test data, run the following command: 
- `flask --app api seed-db`

### Start the server 
To start running the API server, use one of the following commands from the project directory:
- `flask run --debug`
- `flask --app api run` 



# Feature List

## A resource management system for makerspaces and Fab Labs. 

## Access Control System

An RFID or NFC reader system to control access to certain areas or machines. Members could use RFID tags or cards to gain access. While machine access controls is not all that interested, it could be useful in other contexts within a lab and makes for an interesting technical challenge. RFID/NFC-based systems could be utilized within community spaces in other ways.

- **Priority Level: 4/10**

## Scheduling System: Equipment Booking & Reservations

Develop a web-interface (UI) to run on an installed kiosk computer or tablet to allow lab users to reserve and book time on equipment in the space.

## Equipment Stats and Logs

Record equipment and resource usage and provide a dashboard to review analytics.

## Inventory Management System

Implement an inventory management system for tools and supplies. A barcode scanner could be used and then connected to Haystack's Lightspeed API to add and track chargers to student accounts. This same system could be used to log and report bugs and issues with equipment, log maintenance tasks, and notes for future users.

## Environment Monitoring

- Cameras to inspect machines for safety, general security or live-stream camera for project timelapses.
- Use sensors with Raspberry Pi to monitor environmental conditions like temperature, humidity, or air quality, ensuring a comfortable and safe workspace.

## Environment Feedback & Notifications

- Control lights, speakers, and other output devices based on environmental conditions or other external factors.

## Networked Notification System:

Set up a system where Raspberry Pis can display notifications or messages on screens around the space, useful for announcing events, closures, or equipment status.

## Backup System

- Backup all critical data and system information to remote server.

## Interactive Learning Stations

Set up stations with Raspberry Pis where participants can engage in self-guided learning, like programming tutorials, electronics basics, or 3D modeling.

## Digital Signage and Information Kiosks

- Use Raspberry Pis to power digital signs or kiosks providing information about the makerspace, upcoming workshops, or project ideas.
- priortiy: 9/10

## Custom Project Showcase

Set up screens where members can showcase their projects or documentations, possibly with interactive elements powered by Raspberry Pis.

# Software Tooling

## fabMods

fab mods are a community developed set of tools to generate machine code for machines. Currently the UI is lacking and there is not a lot of documentation. This could be incorporated as part of this project, or forked and a new version developed altogether.

# Goals

- Collaborative open-source development. A goal of this project is to attract and collaborate with other Fab Lab network makers who are interested in working and developing such a project.

# Technology Stack 
- Backend: Python (Flask)
- Database: SQLite
- Frontend: 

# API Design 
## User Endpoints
- GET /api/users: Retrieve a list of users.
- POST /api/users: Create a new user.
- GET /api/users/{userid}: Retrieve a detailed view of a specific user.
- PUT /api/users/{userid}: Update a specific user's details.
- DELETE /api/users/{userid}: Remove a user.
## Equipment Endpoints 
- GET /api/equipment: List all equipment.
- POST /api/equipment: Add new equipment.
- GET /api/equipment/{equipmentid}: Get details for a piece of equipment.
- PUT /api/equipment/{equipmentid}: Update equipment details.
- DELETE /api/equipment/{equipmentid}: Remove equipment from the database.
## Reservation Endpoints 
- GET /api/reservations: List all reservations.
- POST /api/reservations: Create a new reservation.
- GET /api/reservations/{reservationid}: View details of a reservation.
- PUT /api/reservations/{reservationid}: Modify a reservation.
- DELETE /api/reservations/{reservationid}: Cancel a reservation.

# UI Design 
## Views 
- Login/Registration Page
- Dashboard
- Equipment Catalog
- Equipment Detail Page
- Reservation System 
- User Profiles 
- Admin Panel 

## UI Requirements
- resonsive design (mobile friendly)
- high quality user experience 
- accessibility 
- high quality user interface and design 

# Features 


