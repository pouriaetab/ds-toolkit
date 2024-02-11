#!/bin/bash

# Define the root directory where you want to create the folders.
root_dir="statistical_methods"

# Main topics as an array
main_topics=(
    "descriptive_statistics"
    "inferential_statistics"
    "t_test"
    "anova_analysis_of_variance"
    "manova_multivariate_analysis_of_variance"
    "ancova_analysis_of_covariance"
    "chi_squared_test"
    "fishers_exact_test"
    "non_parametric_tests"
    "correlation_coefficients"
    "regression_analysis"
    "factor_analysis"
    "principal_component_analysis_pca"
    "cluster_analysis"
    "discriminant_analysis"
    "time_series_analysis"
    "survival_analysis"
    "mixed_models"
    "bayesian_statistics"
    "structural_equation_modeling"
    "meta_analysis"
    "power_and_sample_size_calculation"
    "post_hoc_tests"
    "reliability_testing"
    "path_analysis"
)

# Create root directory and navigate into it
mkdir -p "$root_dir"
cd "$root_dir"

# Create main topic folders and add a .ipynb file in each
for topic in "${main_topics[@]}"; do
    mkdir -p "$topic"
    # Create the .ipynb file with a basic structure inside each topic folder
    echo '{
 "cells": [],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.x"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}' > "$topic/$topic.ipynb"
done

echo "Main topic folders and .ipynb files have been created."
