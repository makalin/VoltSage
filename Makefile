# VoltSage Makefile
# Common development tasks

.PHONY: help install setup test run clean

# Default target
help:
	@echo "VoltSage - Electric Vehicle Range Predictor"
	@echo "=========================================="
	@echo ""
	@echo "Available commands:"
	@echo "  install    - Install Python dependencies"
	@echo "  setup      - Set up database and train model"
	@echo "  test       - Run test suite"
	@echo "  run        - Start the Flask application"
	@echo "  clean      - Clean up generated files"
	@echo "  dev        - Start development server with auto-reload"
	@echo "  api-test   - Test API endpoints"
	@echo "  format     - Format code with black"
	@echo "  lint       - Run linting checks"

# Install dependencies
install:
	@echo "Installing Python dependencies..."
	pip install -r requirements.txt

# Set up the project (database + model)
setup:
	@echo "Setting up VoltSage..."
	python setup_db.py
	@echo "Setup complete!"

# Run tests
test:
	@echo "Running test suite..."
	python test_app.py

# Start the application
run:
	@echo "Starting VoltSage..."
	python run.py

# Development server with auto-reload
dev:
	@echo "Starting development server..."
	FLASK_DEBUG=True python app.py

# Test API endpoints
api-test:
	@echo "Testing API endpoints..."
	curl -X POST http://localhost:5000/api/predict \
		-H "Content-Type: application/json" \
		-d '{"temperature": 20, "wind_speed": 10, "driving_style": "moderate", "cargo_weight": 100}'
	@echo ""
	curl -X GET http://localhost:5000/api/history

# Format code
format:
	@echo "Formatting code..."
	black . --line-length=88

# Lint code
lint:
	@echo "Running linting checks..."
	flake8 . --max-line-length=88 --ignore=E203,W503

# Clean up generated files
clean:
	@echo "Cleaning up..."
	rm -rf __pycache__
	rm -rf *.pyc
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	@echo "Cleanup complete!"

# Full setup (install + setup + test)
full-setup: install setup test
	@echo "Full setup complete!"

# Production setup
prod-setup:
	@echo "Setting up for production..."
	pip install -r requirements.txt
	python setup_db.py
	@echo "Production setup complete!"

# Docker commands (if using Docker)
docker-build:
	docker build -t voltsage .

docker-run:
	docker run -p 5000:5000 voltsage

# Database commands
db-reset:
	@echo "Resetting database..."
	rm -f voltsage.db
	python setup_db.py

# Model commands
model-retrain:
	@echo "Retraining model..."
	rm -f models/ev_range_model.joblib
	python -c "from models.range_predictor import RangePredictor; RangePredictor()"

# Backup database
backup:
	@echo "Backing up database..."
	cp voltsage.db voltsage_backup_$(shell date +%Y%m%d_%H%M%S).db

# Show project info
info:
	@echo "VoltSage Project Information"
	@echo "============================"
	@echo "Python version: $(shell python --version)"
	@echo "Flask version: $(shell python -c 'import flask; print(flask.__version__)')"
	@echo "Database exists: $(shell test -f voltsage.db && echo 'Yes' || echo 'No')"
	@echo "Model exists: $(shell test -f models/ev_range_model.joblib && echo 'Yes' || echo 'No')" 