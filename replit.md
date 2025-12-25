# ChurnChaser - Customer Retention Predictor

## Overview

ChurnChaser is a Streamlit-based web application designed for eCommerce businesses to predict customer churn risk. The application allows users to upload customer data in CSV format and receive churn predictions using a machine learning model. It provides an intuitive interface for analyzing customer retention patterns and identifying at-risk customers.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit web framework
- **Styling**: Custom CSS with Google Fonts (Bauhaus 93) for branding
- **Layout**: Wide layout with expandable sidebar for better user experience
- **UI Components**: File uploader, data preview tables, interactive charts, and download buttons

### Backend Architecture
- **Core Logic**: Python-based data processing and machine learning inference
- **Data Processing**: Pandas for CSV handling and data manipulation
- **Machine Learning**: Scikit-learn for model loading and predictions
- **Visualization**: Plotly for interactive charts and graphs

## Key Components

### Data Upload and Validation
- CSV file upload functionality with validation
- Required columns: CustomerID, Recency, Frequency, Monetary, SupportTickets, Tenure
- Data preview showing first 5 rows of uploaded data
- Basic data validation to ensure required columns are present

### Machine Learning Model
- Pre-trained Random Forest classifier stored as pickle file
- Fallback dummy prediction function if model file doesn't exist
- Churn probability calculation (0.00 to 1.00 scale)
- Risk categorization (Low, Medium, High) based on probability thresholds

### Visualization Dashboard
- Pie chart showing distribution of churn risk categories
- Optional bar chart for top 10 customers most likely to churn
- Interactive Plotly charts for better user engagement

### Export Functionality
- CSV download option for prediction results
- Includes CustomerID, Churn Probability, and Risk Category

## Data Flow

1. **Input**: User uploads CSV file with customer data
2. **Validation**: System validates required columns and data format
3. **Processing**: Data is processed and fed to the ML model
4. **Prediction**: Model generates churn probabilities for each customer
5. **Categorization**: Probabilities are converted to risk categories
6. **Visualization**: Results are displayed in charts and tables
7. **Export**: User can download results as CSV file

## External Dependencies

### Python Libraries
- **streamlit**: Web application framework
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **plotly**: Interactive visualization
- **scikit-learn**: Machine learning model handling
- **pickle**: Model serialization/deserialization

### External Resources
- **Google Fonts**: Bauhaus 93 font for branding
- **CSS**: Custom styling for modern UI appearance

## Deployment Strategy

### Local Development
- Single Python file (app.py) structure for simplicity
- Streamlit's built-in development server
- Hot reload for development iterations

### Production Considerations
- Streamlit Cloud deployment ready
- Model file (churn_model.pkl) should be included in repository
- Environment requirements specified for dependency management
- Responsive design for various screen sizes

### File Structure
- `app.py`: Main application file containing all functionality
- `churn_model.pkl`: Pre-trained machine learning model (if available)
- Custom CSS embedded within the application for styling

The architecture prioritizes simplicity and user experience, with a single-file application structure that's easy to deploy and maintain while providing comprehensive churn prediction capabilities for eCommerce businesses.

## Recent Changes: Latest modifications with dates

### 2025-07-31: Production-Ready GitHub Release Preparation
- Created comprehensive professional README.md with deployment instructions
- Resolved sidebar visibility issues by migrating to expandable FAQ sections in main content
- Updated text references to match new layout ("samples below" instead of "sidebar")
- Cleaned up project structure and removed Replit-specific files from GitHub version
- Added production deployment files:
  - Dockerfile and docker-compose.yml for containerization
  - Procfile and setup.sh for Heroku deployment
  - requirements-github.txt for dependency management
  - .gitignore with comprehensive exclusions
  - LICENSE (MIT) and CONTRIBUTING.md for open source compliance
  - CHANGELOG.md documenting development history
- Reorganized assets from attached_assets/ to assets/ folder
- Updated all asset paths in application code
- Documented technical challenges and solutions in README
- Project now ready for direct GitHub deployment with multiple platform support