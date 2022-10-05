# COVID-19 U.S. Case Surveillance Data Warehouse

Final project for INFSCI 2711 Advanced Topics in Database Management, University of Pittsburgh, Spring 2022.

This repo contains the code for the interactive dashboard web application built to visualize data from data warehouses.

Data ETL, data warehouse design and implementation related code are not included here.


## Introduction

### Data Source

- [COVID-19 Case Surveillance Dataset from U.S. CDC](https://data.cdc.gov/Case-Surveillance/COVID-19-Case-Surveillance-Public-Use-Data-with-Ge/n8mc-b4w4)

- [County level population data from U.S. Census Bureau](https://www2.census.gov/programs-surveys/popest/datasets/2010-2020/counties/totals/)


### Goals
- Provide data-driven public health guidelines, and more efficient allocation of medical resources. 
- Key questions to answer:
  - How does disease spread / severity change with time at different locations?
    - Is there an ongoing outbreak at a particular location and time?
    - Is the outbreak less severe or more severe?
  - How does patient demographics affect disease severity?
    - Are specific demographic group more susceptible to severe outcomes?

## Interactive Dashboard

- The dashboard is built using Python and [Plotly Dash](https://plotly.com/dash/).

- The dash app contains two views, each has many interactive elements to allow a user to specify the the condition and the disease metrics to visualize.


### View 1: Visualizes disease metrics from the time and location perspective

- User can select disease metrics to be visualized on a time-series plot.
- User can choose disease metrics to be displayed on the U.S. map with state-level aggregation data, or on a state map showing county-level aggregation data.

  <img width="500" alt="view 1" src="https://user-images.githubusercontent.com/8323143/193964177-e7a6802e-c33c-4b9d-b0a2-cd878bd173dd.png">


### View 2: Visualizes disease metrics based on patient demographic features

- User can choose any 1, 2, or select all 3 demographic features.
- User can plot 2 different metrics to compare them side-by-side.

  <img width="500" alt="view 2" src="https://user-images.githubusercontent.com/8323143/193964181-e06fcb8e-353c-428b-86b1-0a26795db216.png">
