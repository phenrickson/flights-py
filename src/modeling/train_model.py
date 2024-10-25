from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_curve, roc_auc_score, log_loss, accuracy_score
import numpy as np
import pandas as pd
import pickle

# create a preprocessor for the model
def create_preprocessor(numeric_features, categorical_features):
    
    # Define the numeric transformer with imputer
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='mean')),  # You can use different strategies
        ('scaler', StandardScaler())
    ])

    # Define the categorical transformer
    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),  # Handle NaNs for categorical features
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    # Create the preprocessor using ColumnTransformer
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, numeric_features), 
            ('cat', categorical_transformer, categorical_features)
        ]
    )

    return preprocessor

# create a pipeline using model
def create_pipeline(preprocessor, model):
    
    pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', model)
    ])

    return pipeline

# create a function to train model
def train_model(df, numeric_features, categorical_features, model = LogisticRegression(), outcome = 'arr_delay'):

    # Split the data into features and target
    X = df[numeric_features + categorical_features]
    y = df[outcome] 

    # Create the preprocessor
    preprocessor = create_preprocessor(numeric_features, categorical_features)

    # Create the pipeline
    pipeline = create_pipeline(preprocessor, model)

    # Fit the pipeline on the training data
    pipeline.fit(X, y)

    return pipeline

# create a function to predict new data
def score_data(pipeline, new_data):

    # probs
    probs = pipeline.predict_proba(new_data)

    # bind to outcome
    return probs

# assess model
def assess_predictions(pipeline, new_data, threshold = 0.5, outcome = 'arr_delay'):

    y_test = new_data[outcome]

    # Predict probabilities for the positive class
    y_pred_proba = pipeline.predict_proba(new_data)[:, 1]

    # Make predictions based on a threshold (0.5)
    y_pred = (y_pred_proba >= threshold).astype(int)

    # Calculate metrics
    metrics = {
        'ROC AUC': roc_auc_score(y_test, y_pred_proba),
        'Log Loss': log_loss(y_test, y_pred_proba)
    }

    # Convert metrics to a DataFrame and round to four decimal places
    metrics_df = pd.DataFrame.from_dict(metrics, orient='index', columns=['Score']).reset_index()
    metrics_df.columns = ['Metric', 'Score']  # Rename columns
    metrics_df['Score'] = metrics_df['Score'].round(4)  # Round scores to four decimal places

    return metrics_df

# function to extract coefficients
def extract_coefficients(pipeline):

    model = pipeline.named_steps['model']
    intercept = model.intercept_[0]
    coefficients = model.coef_[0]
    feature_names = pipeline.named_steps['preprocessor'].get_feature_names_out()

    intercept_df = pd.DataFrame({'Feature': ['Intercept'], 'Coefficient': [intercept]})

    coef_df = pd.DataFrame({'Feature': feature_names, 'Coefficient': coefficients})

    out_df = pd.concat([intercept_df, coef_df], ignore_index=True)

    return out_df