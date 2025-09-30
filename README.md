# Local Neighborhood Platform

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Django](https://img.shields.io/badge/Django-4.2-green?logo=django)](https://www.djangoproject.com/)
[![Vue.js](https://img.shields.io/badge/Vue.js-3-green?logo=vue.js)](https://vuejs.org/)
[![Quasar](https://img.shields.io/badge/Quasar-2-blue?logo=quasar)](https://quasar.dev/)

An intelligent, local-first social platform designed to connect neighbors, promote local businesses, and uncover community needs through data analysis and an AI-powered conversational assistant.

---

<!-- 🖼️ SCREENSHOT/GIF OF THE MAIN FEED PAGE GOES HERE -->
<!-- Add a high-quality screenshot or a short GIF showcasing the main feed, sidebars, and overall UI. -->
<!-- Example: <p align="center"><img src="path/to/your/screenshot.png" width="800"></p> -->

---

## 🌟 Key Features

This platform is a full-stack application built with a Django backend and a Quasar (Vue.js) frontend. It includes several advanced features:

*   **Social Feed System**: A dynamic feed where users can create posts with text, multiple images, and hashtags. Includes interactive features like liking and commenting.
*   **Smart Feed Filtering**: The feed intelligently displays posts based on user location, showing public posts and posts exclusive to the user's neighborhood.
*   **Dual Profile System**: Users can register as regular residents or business owners, with dedicated profiles for personal and commercial use.
*   **Automated Neighborhood System**: Automatically assigns users and businesses to their local neighborhood based on geographical coordinates.
*   **Business Directory & Rating**: A filterable directory of local businesses where users can rate and review services.
*   **AI Conversational Assistant (Chatbot)**: An intelligent chatbot, orchestrated with **n8n** and powered by **Google Gemini**, that understands natural language queries to help users find local businesses.
*   **Business Opportunity Recommender**: A machine learning system using **Item-based Collaborative Filtering** to analyze neighborhood data and suggest new business opportunities.
*   **Social Login**: Easy and secure authentication using Google accounts.

---

## 🏛️ System Architecture

The project is structured as a monorepo containing a separate backend and frontend, communicating via a REST API. It also integrates with external AI and automation services.

<!-- 🖼️ ARCHITECTURE DIAGRAM GOES HERE -->
<!-- This is where you put the architecture diagram you created earlier. -->
<!-- Example: <p align="center"><img src="path/to/your/architecture-diagram.png" width="700"></p> -->

### Technology Stack

**Backend (`backend/`)**
*   **Framework**: Django, Django REST Framework
*   **Database**: MySQL
*   **Authentication**: `dj-rest-auth`, `django-allauth` (for JWT and Google Social Login)
*   **Geography**: `geopy` for distance calculations
*   **Tagging**: `django-taggit` for hashtag functionality
*   **Filtering**: `django-filter` for advanced API filtering
*   **ML Model Loading**: `pickle` for loading the recommender system model

**Frontend (`frontend/`)**
*   **Framework**: Vue.js 3 (with Composition API)
*   **UI Framework**: Quasar 2
*   **State Management**: Pinia
*   **API Communication**: Axios
*   **Google Auth**: `vue3-google-login` for Google Identity Services (GIS) integration

**AI & Automation**
*   **LLM**: Google Gemini API (for NLP and response generation)
*   **Workflow Automation**: n8n (self-hosted or cloud) for orchestrating the chatbot logic.

---

## 🚀 Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

*   Python 3.10+
*   Node.js 18+ and npm
*   Docker (for n8n, if running locally)
*   A running MySQL server
*   An `ngrok` account (for exposing the local backend to the n8n cloud instance)

### 1. Backend Setup

1.  **Navigate to the backend directory:**
    ```bash
    cd backend
    ```

2.  **Create a virtual environment and install dependencies:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3.  **Configure environment variables:**
    *   Rename `.env.example` to `.env` (you should create this file).
    *   Fill in your database credentials, Django `SECRET_KEY`, and other required variables.

4.  **Run database migrations:**
    ```bash
    python manage.py migrate
    ```
    *You can also run the data seeding migrations to populate the database with test data.*

5.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```
    The backend API will be available at `http://localhost:8000`.

### 2. Frontend Setup

1.  **Navigate to the frontend directory:**
    ```bash
    cd frontend
    ```

2.  **Install dependencies:**
    ```bash
    npm install
    ```

3.  **Configure environment variables:**
    *   Create a `.env` file in the `frontend` directory.
    *   Add your Google Client ID and other necessary keys:
        ```
        GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
        ```
    *   You also need to configure the backend API URL in `src/boot/axios.js` and the n8n webhook URL in `src/components/ChatbotWidget.vue`.

4.  **Run the development server:**
    ```bash
    quasar dev
    ```
    The frontend will be available at `http://localhost:9000`.

---

## ✨ Showcase

Here are some highlights of the platform's key features.

<!-- 🖼️ A FEW MORE SCREENSHOTS GO HERE -->
<!-- Add 2-3 more high-quality screenshots showcasing different parts of your application. Good choices would be: -->
<!-- 1. The Business Details page. -->
<!-- 2. The User Profile page with the post management section. -->
<!-- 3. The Chatbot in action. -->
<!-- 4. The Recommender System results in the modal. -->

<!-- Example: -->
<!-- ### Intelligent Chat Assistant -->
<!-- <p align="center"><img src="path/to/chatbot-screenshot.png" width="400"></p> -->
<!-- ### Business Recommendation Engine -->
<!-- <p align="center"><img src="path/to/recommender-screenshot.png" width="600"></p> -->

---

## 🎓 Research Component

This project includes two primary research-oriented components:

1.  **Business Opportunity Recommender**: An item-based collaborative filtering model was developed in a Google Colab notebook to find similarities between business categories based on their co-occurrence in different neighborhoods. The resulting similarity matrix is used to recommend new business types for a given neighborhood, addressing potential market gaps.

2.  **Conversational AI**: The chatbot leverages a modern, orchestrated architecture using n8n and Google's Gemini LLM. The research aspect focused on **Prompt Engineering** to enable the LLM to accurately extract structured entities (intent, category, neighborhood) from natural language queries in Persian, which then drives the backend API calls.

---

## 🛠️ Future Work

This platform serves as a strong foundation, and there are many exciting possibilities for future development:

*   **Notification System**: Real-time notifications for likes, comments, and other interactions.
*   **Private Messaging**: A direct messaging feature for users.
*   **Advanced Recommender**: Evolving the recommender to use more advanced techniques like Matrix Factorization and incorporate user ratings.
*   **Conversational Memory**: Enhancing the chatbot to remember the context of the conversation for multi-turn interactions.
*   **Mobile App**: Building a mobile application using Quasar's cross-platform capabilities.

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
