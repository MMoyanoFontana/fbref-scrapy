# FBref Scraper API

A FastAPI-based web scraper and API for football statistics from FBref.com. This project provides structured access to team statistics across major European leagues.

## 📋 Features

- **Multi-league support**: Premier League, Serie A, La Liga, Ligue 1, Bundesliga, and Liga Profesional Argentina
- **Comprehensive stats**: Defense, goalkeeping, passing, shooting, possession, and more
- **RESTful API**: Clean endpoints for accessing team statistics
- **Database storage**: SQLModel-based data persistence
- **Modern stack**: FastAPI with async support

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- uv (recommended) or pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fbref-scrappy
```

2. Install dependencies with uv:
```bash
uv sync
```

### Development

Start the development server:
```bash
uv run dev app/main.py
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

### Available Endpoints

#### Teams
- `GET /teams` - List all teams (with pagination)

#### Team Statistics (by team_id and season)
- `GET /teams/{team_id}/defense` - Defensive statistics
- `GET /teams/{team_id}/gca` - Goal and shot creation actions
- `GET /teams/{team_id}/keeper` - Goalkeeper statistics
- `GET /teams/{team_id}/keeper-advanced` - Advanced goalkeeper stats
- `GET /teams/{team_id}/misc` - Miscellaneous statistics
- `GET /teams/{team_id}/passing` - Passing statistics
- `GET /teams/{team_id}/passing-types` - Passing types breakdown
- `GET /teams/{team_id}/playing-time` - Playing time statistics
- `GET /teams/{team_id}/possession` - Possession statistics
- `GET /teams/{team_id}/shooting` - Shooting statistics
- `GET /teams/{team_id}/standard` - Standard statistics

### Example Usage

```bash
# Get all teams
curl http://localhost:8000/teams

# Get Manchester City's defense stats for 2023-24 season
curl "http://localhost:8000/teams/b8fd03ef/defense?season=2023-2024"

# Get Barcelona's passing stats for current season
curl "http://localhost:8000/teams/206d90db/passing?season=2024-2025"
```

## 🏗️ Project Structure

```
fbref-scrappy/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application and routes
│   ├── models.py        # SQLModel database models
│   ├── database.py      # Database configuration
│   └── scraper.py       # Web scraping logic
├── pyproject.toml       # Project configuration
├── uv.lock             # Dependency lock file
└── README.md           # This file
```

## 🔧 Technologies Used

- **FastAPI**: Modern web framework for building APIs
- **SQLModel**: SQL databases with Python type hints
- **BeautifulSoup4**: Web scraping and HTML parsing
- **Pandas**: Data manipulation and analysis
- **Requests**: HTTP library for web scraping
- **SQLAlchemy**: SQL toolkit and ORM
- **uvicorn**: ASGI web server

## 📊 Supported Leagues

- **Premier League** (England)
- **Serie A** (Italy)
- **La Liga** (Spain)
- **Ligue 1** (France)
- **Bundesliga** (Germany)
- **Liga Profesional Argentina** (Argentina)

## 🛠️ Development

### Code Quality

This project uses several tools for code quality:

- **Ruff**: Fast Python linter and formatter
- **MyPy**: Static type checking
- **Pre-commit**: Git hooks for code quality

### Running Tests

```bash
# Install development dependencies
uv sync --group dev

# Run linting
uv run ruff check

# Run type checking
uv run mypy app/
```

## ⚠️ Legal Notice

This project is for educational and research purposes. Please respect FBref.com's robots.txt and terms of service. Consider implementing rate limiting and caching to minimize server load.

## 📄 License

This project is open source. Please check the license file for details.

## 🆘 Support

If you encounter any issues or have questions, please open an issue on the repository.
