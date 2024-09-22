# Churn Management Application For Azubian

![Churn App](App/images/churn05.png)

## Description
This Streamlit application is designed to help businesses understand and predict customer churn using machine learning models. It is containerized using Docker for easy deployment and scaling.

## Features
- **Interactive Dashboards:** Visualize customer data through interactive charts and graphs.
- **Predictive Analytics:** Use pre-trained models to predict customer churn based on historical data.
- **User Authentication:** Secure login system to access the application.
- **Data Upload:** Users can upload their customer data in CSV format for analysis.
- **Customizable Theme:** Supports dark and light themes, adjustable via the Streamlit interface.
- **Docker Integration:** Easily deployable using Docker and Docker Compose.

## Installation

### Prerequisites
- Docker
- Docker Compose

### Clone the Repository
Clone the project repository to your local machine using the following command:
```bash
git clone https://github.com/kbay9/Customer-Churn-Prediction-Challenge-For-Azubian.git
cd Customer-Churn-Prediction-Challenge-For-Azubian
```
### Using Docker Compose
Build and run the application using Docker Compose:
```bash
docker-compose build
docker-compose up
```

## Configuration
Configuration settings can be adjusted in the `Dockerfile` or the `.streamlit/config.toml` file for application-specific settings like themes. For Docker-specific settings, modify the `docker-compose.yml` and `.env` files.

## Usage
Navigate to [http://localhost:8501](http://localhost:8501) in your web browser to access the application. Use the application as described in the Usage section.

## Docker Compose Details
- **Dockerfile**: Defines the Docker container specifics, such as base image, necessary environment setup, and commands.
- **docker-compose.yml**: Configures the services involved in the application, which might include databases, backend services, and the Streamlit app itself.

## License
This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

