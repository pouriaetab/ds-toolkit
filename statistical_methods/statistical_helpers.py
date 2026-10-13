import pandas as pd
from scipy.stats import shapiro
from scipy.stats import levene
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.tools.tools import add_constant

def shapiro_test_to_df(dataframe, sort_by='p-value', threshold=0.05):
    """
    Performs the Shapiro-Wilk test on each column of a pandas DataFrame, returns the results in a new DataFrame,
    sorts the results by the specified column, and adds a column indicating if normality is met.

    Parameters:
    - dataframe: pandas DataFrame containing numerical data for which the Shapiro-Wilk test will be performed.
    - sort_by: String, column name to sort the results DataFrame by. Default is 'p-value'.
    - threshold: Float, the threshold for the p-value to decide if normality is met. Default is 0.05.

    Returns:
    - A pandas DataFrame with each row representing a feature from the input DataFrame, columns for Shapiro-Wilk 
      test statistics and p-values, and a column indicating if normality is met.
    """
    features, statistics, p_values, normality = [], [], [], []

    # Iterate over each column in the DataFrame and perform Shapiro-Wilk test
    for feature in dataframe.columns:
        stat, p = shapiro(dataframe[feature])
        features.append(feature)
        statistics.append(stat)
        p_values.append(p)
        # Determine if normality is met
        normality.append("Pass" if p > threshold else "Fail")

    # Create and return the results DataFrame
    results_df = pd.DataFrame({
        'Feature': features,
        'Statistics': statistics,
        'p-value': p_values,
        'Normality': normality
    }).set_index('Feature')

    # Sort the DataFrame
    results_df = results_df.sort_values(by=sort_by)

    return results_df

def check_homogeneity(dataframe, group_column):
    """
    Performs Levene's test for homogeneity of variances across different groups in a dataframe.

    Parameters:
    - dataframe: pandas DataFrame containing the data.
    - group_column: The name of the column in `dataframe` that contains the grouping variable.

    Returns:
    - DataFrame with features, their Levene's test statistic, p-value, and homogeneity assessment.
    """
    # Initialize list to store results
    results_list = []

    # Make sure group_column is considered during feature extraction
    # Here, no need to drop group_column as we're not performing numeric operations on it
    features = dataframe.columns.drop([group_column]) if group_column in dataframe.columns else dataframe.columns
    
    for feature in features:
        if feature != group_column:  # Make sure to skip the group column for Levene's test
            # Gathering data for each group for the current feature
            group_data = [group[feature].values for name, group in dataframe.groupby(group_column, observed=True)]
            stat, p = levene(*group_data)
            
            # Determining homogeneity
            homogeneity = 'Homogeneous' if p > 0.05 else 'Not Homogeneous'
            
            # Accumulating results
            results_list.append({'Feature': feature, 'Statistic': stat, 'p-value': p, 'Homogeneity': homogeneity})
    
    # Creating DataFrame from the accumulated list of results
    results_df = pd.DataFrame(results_list)
    results_df.set_index('Feature', inplace=True)
    
    return results_df

def check_multicollinearity(dataframe):
    """
    Calculates the Variance Inflation Factor (VIF) for each feature in a DataFrame
    to assess multicollinearity and classifies the level of multicollinearity.

    Parameters:
    - dataframe: pandas DataFrame containing only the features (numeric) to be analyzed.

    Returns:
    - A pandas DataFrame with features as rows, including VIF values and multicollinearity classification.
    """
    # Add a constant for VIF calculation
    X = add_constant(dataframe)
    
    # Initialize lists to store data
    features = X.columns
    vif_values = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]
    
    # Classify multicollinearity levels based on VIF values
    multicollinearity = []
    for vif in vif_values:
        if vif == 1:
            multicollinearity.append("No Multicollinearity (Pass)")
        elif 1 < vif < 5:
            multicollinearity.append("Moderate")
        elif 5 <= vif < 10:
            multicollinearity.append("High")
        else:  # vif >= 10
            multicollinearity.append("Significant")
    
    # Create DataFrame from the results
    results_df = pd.DataFrame({
        'Feature': features,
        'VIF': vif_values,
        'Multicollinearity': multicollinearity
    }).set_index('Feature')
    
    return results_df
