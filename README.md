# Mansoura Research Hub

## Overview
This project aims to assist researchers in discovering, reviewing, and comparing recent academic papers based on their topic of interest. The application scrapes data from Google Scholar and Papers With Code to provide paper details, summaries, code availability, and comparative reviews.

---

## File Structure

### Backend (Python)
```
backend/
|
|-- app/
|   |-- __init__.py             # Package initialization
|   |-- main.py                 # FastAPI app and endpoints
|   |-- services/
|   |   |-- scraper.py          # Web scraping logic for Google Scholar and Papers With Code
|   |   |-- summarizer.py       # Summarization logic using Hugging Face Transformers
|   |   |-- comparator.py       # Logic for generating comparative reviews
|-- requirements.txt            # Python dependencies
|-- README.md                   # Backend-specific documentation
```

### Frontend (Flutter)
```
frontend/
|
|-- lib/
|   |-- main.dart               # Entry point for the Flutter app
|   |-- screens/
|   |   |-- home_screen.dart    # Home screen for topic input
|   |   |-- result_screen.dart  # Screen displaying fetched results
|   |-- models/
|   |   |-- paper_model.dart    # Data model for research papers
|   |-- services/
|   |   |-- api_service.dart    # API integration logic
|-- pubspec.yaml                # Flutter dependencies
|-- README.md                   # Frontend-specific documentation
```

### Root Structure
```
MansouraResearchHub/
|
|-- backend/                    # Python backend
|-- frontend/                   # Flutter frontend
|-- README.md                   # Project overview
|-- .gitignore                  # Git ignored files
|-- LICENSE                     # License file
```

---

## Backend: Python Implementation
### Features
- **Paper Search:** Fetches paper metadata (title, authors, summary, link, etc.) from Google Scholar.
- **Code Availability:** Checks if implementations are available on Papers With Code.
- **Summarization:** Generates concise summaries for fetched papers.
- **Comparative Review:** Compares papers based on metadata and code availability.

### Setup Instructions
1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/MansouraResearchHub.git
   cd MansouraResearchHub/backend
   ```
2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the server**
   ```bash
   uvicorn app.main:app --reload
   ```
4. **Access API documentation**
   Open [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to test endpoints interactively.

---

## Frontend: Flutter Implementation
### Features
- **User Input:** Accepts topic of interest from users.
- **Results Display:** Shows a list of papers with metadata, summaries, and code availability.
- **Comparative Review:** Provides an aggregated comparison view.

### Setup Instructions
1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/MansouraResearchHub.git
   cd MansouraResearchHub/frontend
   ```
2. **Install dependencies**
   ```bash
   flutter pub get
   ```
3. **Run the app**
   ```bash
   flutter run
   ```

---

## Integration
The backend and frontend communicate via REST APIs. Ensure the backend server is running and replace the `BASE_URL` in the Flutter app with the backend server's address.

---

## Contributing
1. Fork the repository.
2. Create a new branch (`feature/your-feature`).
3. Commit your changes.
4. Push to the branch.
5. Open a pull request.

---

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

---

## Acknowledgments
- [Google Scholar](https://scholar.google.com) for paper metadata.
- [Papers With Code](https://paperswithcode.com) for code availability.
- [Hugging Face](https://huggingface.co) for the summarization model.
