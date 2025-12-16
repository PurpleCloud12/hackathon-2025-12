
# AI SQL Data Validator

This project is a React web application that uses the Gemini API to translate natural language into SQL queries for data validation.

## How to Run Locally

To run this project in your local development environment, you will need [Node.js](https://nodejs.org/) (version 18 or higher) installed. We will use **Vite** as the development server.

### Step 1: Set Up Project Files

1.  Create a new folder for your project on your computer.
2.  Place all the project files (including `package.json`, `vite.config.ts`, etc.) into this new folder.

### Step 2: Install Dependencies

Open your terminal, navigate into your project folder, and run the following command to install the necessary packages:

```bash
npm install
```

### Step 3: Create Environment File

The application needs your Gemini API key and the backend URL to function.

1.  In the root of your project folder, create a new file named `.env`.
2.  Add the following lines to the `.env` file, replacing the placeholder values with your actual key and backend address:

```
# Your Gemini API Key
VITE_API_KEY=YOUR_GEMINI_API_KEY

# The full URL for your backend API
VITE_BACKEND_URL=http://10.88.0.4:8080/api/compare-tables
```

**Important:** Vite only exposes environment variables prefixed with `VITE_` to the frontend code for security reasons.

### Step 4: Run the Backend Server

This frontend application is designed to communicate with a backend service. **You must have your backend server running** and accessible at the URL you specified in your `.env` file.

### Step 5: Start the Frontend Development Server

Now you are ready to start the frontend application. Run the following command in your terminal:

```bash
npm run dev
```

Vite will start the development server, and your default web browser will automatically open to `http://localhost:3000`.

Any changes you make to the source code will now automatically reload in the browser.
