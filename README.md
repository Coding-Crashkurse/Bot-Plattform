# BotPlattform

## Overview

BotPlattform is a comprehensive system that combines a backend built with FastAPI for user registration, role management, bot management, and group assignments, with a simple frontend chat UI built using React. The platform allows users to interact with different bots through a visually appealing card-based interface.

## Backend (FastAPI)

The backend is powered by FastAPI and is responsible for managing users, roles, bots, and groups. The API provides endpoints for:

- **User Registration**: Allows new users to register and manage their profiles.
- **Role Management**: Assigns roles to users to control access to certain features.
- **Bot Management**: Creates and manages bots that users can interact with.
- **Group Management**: Organizes bots and users into groups for easier management.

### Setup Script (`setup.py`)

The `setup.py` script is used to create bots, users, and assign them to groups. This script automates the initial setup process by populating the database with predefined bots and associating them with the appropriate users and groups.

## Frontend (React)

The frontend is a simple chat UI built with React. It provides:

- **Bot Cards**: A card for each bot, allowing users to easily select which bot they want to interact with.
- **Routing to Bots**: When a user selects a bot card, they are routed to the corresponding chat interface where they can interact with the selected bot.

## Applications

- **testapp1.py**: A simple LLM app demonstrating basic functionality. Start this app using `python testapp1.py`.
- **testapp2.py**: A second LLM app providing additional features. Start this app using `python testapp2.py`.

## Getting Started

To get started with BotPlattform:

1. **Install Dependencies**:

   - Run `poetry install` to install the required backend dependencies.
   - Navigate to the `llm-frontend` directory and run `npm install` to install the required frontend dependencies.

2. **Run the Backend**:

   - Start the FastAPI server to handle backend operations using `uvicorn app.main:app --reload` or the appropriate command for your project.

3. **Run the Frontend**:

   - Navigate to the `llm-frontend` directory and run `npm run dev` to start the React frontend.

4. **Setup Bots**:

   - Run `python setup.py` to initialize bots, users, and assign them to groups.

5. **Start Applications**:
   - Use `python testapp1.py` to start `testapp1`.
   - Use `python testapp2.py` to start `testapp2`.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
