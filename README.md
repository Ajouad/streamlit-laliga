 # Visualizing the La Liga dataset

## Table of Contents
- [Overview of the project](#overview-of-the-project)
- [Dataset Download](#dataset-download)
- [Data Analysis](#data-analysis)
- [Installing Requirements](#installing-requirements)
- [Launching the web app](#launching-the-web-app)


## Overview of the project
This project aims to analyze and visualize football data from the Spanish La Liga and display the results in a web app. The goal is to understand patterns and trends in the league to provide insights into the game's dynamics. The data visualization is done using Streamlit, presenting historical data from various perspectives.

## Dataset Download
To get started, you will need to clone this repository and then download the dataset from [here](https://datahub.io/sports-data/spanish-la-liga#resource-spanish-la-liga_zip). After downloading, place the data files in the same repository.

## Data Analysis
A comprehensive exploratory data analysis is conducted to extract meaningful insights from the La Liga data. This is the preliminary step to recognize the primary patterns and to discern the possible transformations or preparations for predictive models.

## Installing Requirements
To install the necessary dependencies, use the following command:

pip install -U -r requirements.txt


## Launching the web app
Detailed instructions on launching the Streamlit web app are provided in the repository. Ensure you've set up everything as mentioned above.



## Launching the Web App using Docker
To run the Streamlit web app using Docker, follow these steps:

### 1. Build the Docker Image:
Navigate to the directory containing the Dockerfile.

cd path/to/your/project

Now, build the Docker image. Tag it with a descriptive name for easier reference:

docker build -t your-image-name .

Note: Make sure you include the dot . at the end, which signifies the current directory.

### 2. Run the Docker Container:
After building the image, run the container:

docker run -p 8501:8501 your-image-name

This command maps port 8501 inside the container to port 8501 on your machine.

### 3. Access the Streamlit App:
With the container running, open a web browser and navigate to:

http://localhost:8501

Your Streamlit app should be live and accessible!

To stop the container, press CTRL+C in the terminal.

Note: Replace your-image-name with a suitable name for your project (e.g., laliga-app). If you make updates to your project and wish to reflect those in the Docker container, rebuild the image and run the container again.



