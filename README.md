# NetworkSecurity — ML Pipeline with CI/CD

An end-to-end machine learning project for network security and phishing-data classification, built with Python, FastAPI, scikit-learn, MongoDB, MLflow, AWS S3, Docker, and GitHub Actions.

## Overview

NetworkSecurity implements a machine learning pipeline that ingests data, validates datasets, transforms features, trains classification models, and stores artifacts for subsequent use.

The application exposes API endpoints through FastAPI and supports containerization and automated Docker image publishing to Amazon Elastic Container Registry (ECR).

## Features

- **Data Ingestion:** Retrieves and prepares data using MongoDB.
- **Data Validation:** Validates datasets and generates data-drift reports.
- **Data Transformation:** Preprocesses features for machine learning.
- **Model Training:** Trains classification models and saves trained artifacts.
- **Experiment Tracking:** Uses MLflow to record model training runs.
- **Artifact Storage:** Uploads datasets, preprocessing objects, reports, and trained models to AWS S3.
- **REST API:** Provides application endpoints through FastAPI.
- **Docker:** Packages the application and its Python dependencies into a container.
- **CI/CD:** Uses GitHub Actions to build the Docker image and push it to Amazon ECR.

## Technology Stack

- **Language:** Python
- **API Framework:** FastAPI, Uvicorn
- **Machine Learning:** scikit-learn, NumPy, pandas
- **Database:** MongoDB
- **Experiment Tracking:** MLflow
- **Cloud Storage:** AWS S3
- **Containerization:** Docker
- **Container Registry:** Amazon ECR
- **CI/CD:** GitHub Actions

## Project Structure

```text
NETWORKSECURITY/
├── Artifacts/
├── final_model/
├── networksecurity/
│   ├── components/
│   ├── entity/
│   ├── exception/
│   ├── logging/
│   ├── pipeline/
│   └── utils/
├── .github/
│   └── workflows/
│       └── workflow.yml
├── app.py
├── Dockerfile
├── requirements.txt
└── README.md
```

*The directory structure above is representative. Your actual repository may contain additional files and folders.*

## Prerequisites

Install or configure the following:

- Python 3.10
- Git
- Docker Desktop
- MongoDB or MongoDB Atlas
- AWS account with appropriate S3 and ECR permissions
- AWS CLI
- An AWS S3 bucket and an ECR repository

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

Replace the repository URL with your actual GitHub repository URL.

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

Ensure `python-multipart` is included in `requirements.txt` because the application accepts uploaded files.

### 4. Configure environment variables

Create a local `.env` file if your application uses one. Configure the MongoDB connection string and other required application settings according to your code.

Never commit credentials, database passwords, AWS secret keys, or `.env` files to GitHub.

## Run the Application

Start the FastAPI application from the project root:

```bash
uvicorn app:app --host 127.0.0.1 --port 8000 --reload
```

Open the interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

The available endpoints depend on the routes defined in `app.py`.

## MLflow

Start the MLflow tracking server in a separate terminal:

```bash
mlflow server --host 127.0.0.1 --port 5000
```

Open the tracking interface:

```text
http://127.0.0.1:5000
```

Keep the MLflow server running while executing training operations that depend on it. For containerized or cloud deployments, configure a tracking URI reachable from the application container rather than relying on its own `127.0.0.1`.

## AWS S3 Configuration

Configure the AWS CLI locally:

```bash
aws configure
```

Provide your AWS access key, secret access key, region, and output format when prompted.

Verify your configuration:

```bash
aws sts get-caller-identity
```

List objects in the project bucket:

```bash
aws s3 ls s3://YOUR_BUCKET_NAME/ --recursive
```

Replace `YOUR_BUCKET_NAME` with your actual bucket name.

Use IAM roles or securely managed credentials in deployed environments. Do not embed AWS credentials in source code or Docker images.

## Docker

### Build the image

```bash
docker build -t networksecurity .
```

### Run the container

```bash
docker run --rm -p 8000:8000 networksecurity
```

Open:

```text
http://127.0.0.1:8000/docs
```

The Dockerfile uses a Python 3.10 Debian Bookworm image, installs AWS CLI and Python dependencies, and starts FastAPI using Uvicorn.

Ensure the container receives the required database connection settings, AWS permissions, and MLflow tracking configuration. The application must be able to reach those services from inside the container.

## CI/CD with GitHub Actions

The GitHub Actions workflow automates the following steps when changes are pushed to the `main` branch:

1. Checks out the repository.
2. Performs the configured integration-stage commands.
3. Configures AWS credentials.
4. Authenticates with Amazon ECR.
5. Builds the Docker image.
6. Pushes the image to ECR with the `latest` tag.

### Required GitHub Secrets

Configure these repository secrets under **Settings → Secrets and variables → Actions**:

| Secret | Description |
|---|---|
| `AWS_ACCESS_KEY_ID` | AWS access key ID |
| `AWS_SECRET_ACCESS_KEY` | AWS secret access key |
| `AWS_REGION` | AWS region, such as `us-east-1` |
| `ECR_REPOSITORY_NAME` | Name of the existing ECR repository |

The associated AWS identity must have the required permissions to authenticate with ECR and upload images.

The current workflow's lint and unit-test steps are placeholders. Add actual linting and test commands before treating them as quality checks.

## Troubleshooting

### Docker cannot connect to the engine

Start Docker Desktop and verify:

```bash
docker version
```

The output should contain both Client and Server sections.

### Debian repository errors during the build

Use a supported Debian-based Python image, such as:

```dockerfile
FROM python:3.10-slim-bookworm
```

### FastAPI reports that python-multipart is missing

Add this dependency to `requirements.txt`:

```text
python-multipart
```

Rebuild the image afterward.

### MLflow connection refused

Ensure the MLflow tracking server is running and that the configured tracking URI is accessible from the application.

### AWS S3 or ECR permission errors

Check the AWS region, bucket or repository name, credentials, and IAM permissions. Avoid putting credentials directly in your Dockerfile.

## Security Notes

- Keep `.env`, credentials, and private keys out of Git.
- Add `.env`, `venv/`, `.venv/`, and `__pycache__/` to `.gitignore`.
- Use least-privilege IAM permissions.
- Avoid loading pickle files from untrusted sources.
- Configure authentication and network restrictions before exposing APIs publicly.
- Use a persistent and appropriately secured MLflow tracking backend for production deployments.

## Future Improvements

- Add automated unit and integration tests.
- Add a proper linting stage.
- Introduce automated model evaluation and validation.
- Configure deployment to a cloud hosting service.
- Add structured monitoring, logging, and health checks.

## License

Add a license appropriate for your project before distributing or reusing the source code.
