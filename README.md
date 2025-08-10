# Cloud Service Anomaly Detector

A full-stack, cloud-native application designed to monitor the health of an AWS EC2 instance, analyze its performance metrics for anomalies using a machine learning model, and expose the results via a RESTful API. This project demonstrates a complete development lifecycle, from automated infrastructure provisioning to a CI/CD pipeline for the application code.

---

## Tech Stack

* **Infrastructure as Code (IaC):** Terraform
* **Cloud Provider:** Amazon Web Services (AWS)
* **Backend:** Python, Flask
* **Data Science & ML:** Pandas, Scikit-learn
* **Containerization:** Docker
* **CI/CD:** GitHub Actions

---

## Core Features

* **Automated Infrastructure:** All necessary cloud infrastructure, including the EC2 instance, security groups, and IAM roles, is defined and managed declaratively with Terraform.
* **Time-Series Analysis:** A Python service fetches CPU utilization metrics from AWS CloudWatch.
* **Machine Learning:** An `IsolationForest` model from Scikit-learn is used to perform unsupervised anomaly detection on the collected metric data.
* **RESTful API:** A Flask web server exposes a single endpoint (`/analyze`) that returns the latest analysis results in a clean JSON format.
* **Containerized Application:** The entire Python application is packaged into a portable, isolated Docker container.
* **Continuous Integration:** A GitHub Actions workflow automatically triggers on every push to the `main` branch to build the Docker container, ensuring the application is always in a buildable state.

---

## Project Structure

```
.
├─┬─ .github/workflows/ # GitHub Actions CI/CD pipeline
│ └── docker-build.yml
├── .gitignore
├── .dockerignore
├── Dockerfile # Recipe for building the application container
├── README.md # You are here!
├── app.py # Flask API server
├── core_logic.py # Core data fetching and analysis functions
├── main.tf # Terraform configuration for AWS infrastructure
└── requirements.txt # Python dependencies
```

---

## How to Run This Project Locally

### Prerequisites

* An [AWS Account](https://aws.amazon.com/free/)
* [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli) installed and configured on your local machine.
* [AWS CLI](https://aws.amazon.com/cli/) installed, with credentials configured via `aws configure`.
* [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

### Step 1: Deploy the Cloud Infrastructure

1. Clone the repository:
```bash
git clone [Your GitHub Repo URL]
cd cloud-anomaly-detector
```
2. Initialize Terraform to download the necessary providers:
```bash
terraform init
```
3. Apply the Terraform plan to build the AWS resources. Confirm with `yes`.
```bash
terraform apply
```4. Note the `instance_id` from the Terraform output. You will need to paste this ID into the `INSTANCE_ID` variable at the top of the `core_logic.py` file.

### Step 2: Run the Application (Two Options)

#### Option A: Run Directly with Python

1. Create and activate a Python virtual environment:
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```2. Install the required dependencies:
```bash
pip install -r requirements.txt
```
3. Run the Flask application:
```bash
python app.py
```

#### Option B: Run with Docker (Recommended)

1. Build the Docker image from the `Dockerfile`:
```bash
docker build -t cloud-anomaly-detector .
```
2. Run the application inside a container:
```bash
docker run --rm -p 5000:5000 cloud-anomaly-detector
```

### Step 3: Access the API

Once the application is running (using either option), you can access the API endpoint in your browser or with a tool like Postman:

`http://127.0.0.1:5000/analyze`

### Step 4: Clean Up Resources

To avoid incurring AWS costs, destroy the cloud infrastructure when you are finished.

```bash
terraform destroy
```