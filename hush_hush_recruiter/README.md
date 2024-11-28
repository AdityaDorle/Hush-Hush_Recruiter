hushHush Recruiter

Project Overview

hushHush Recruiter is an automated talent acquisition system developed for Doodle, a global software company renowned for its diverse IT product portfolio including e-commerce applications, cloud platform tools, DevOps tools, IT security solutions, and AI-related tooling. The primary goal of this project is to automate the candidate selection process, making it secretive and efficient, thus minimizing manual efforts and ensuring data privacy.

Features

Automated Candidate Selection: Utilizes data from various sources such as GitHub and Stack Overflow to identify potential candidates.
Secretive Notification System: Automatically notifies candidates if they are selected for a potential role.
Coding Challenge Interface: Provides candidates with an interface to solve coding challenges within a specified timeframe.
Automated Evaluation: Enables Doodle hiring managers to evaluate candidate submissions and notify them of the results.
Data Points
To select the best talent, the system analyzes the following data points:

GitHub Contributions
Stack Overflow Solutions
Additional data points can be extended as needed
Technical Approach
Data Collection
GitHub API:
Extract user contributions, repositories, stars, forks, etc.
Stack Overflow API:
Extract user reputation, answers, questions, badges, etc.
Data Analysis
Unsupervised Learning:

K-Means Clustering:

Used to label the dataset into 'good' and 'bad' candidates based on the extracted features.
Feature Extraction:
Key features such as the number of contributions, the quality of solutions, and activity levels are considered.
Supervised Learning:

Random Forest Classifier:

Trained using the labeled dataset from the clustering step.
Utilizes cross-validation and hyperparameter tuning to optimize the model.
Model Evaluation:
Metrics such as accuracy, precision, recall, and F1-score are used to evaluate the performance.
Implementation
Programming Language: Python

Libraries & Tools:

pandas, numpy for data manipulation
scikit-learn for machine learning algorithms
requests for API calls
flask for the web interface
sqlalchemy for database management

Data Privacy Considerations

All data collected and processed adheres to strict data privacy guidelines.
Personal identifiable information (PII) is anonymized wherever possible.
Only publicly available data is used for analysis.
