import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, auc
from sklearn.preprocessing import LabelEncoder
import joblib
import numpy as np

# Load the data
data = pd.read_csv('cve.csv')

# Drop unnecessary columns
data.drop(columns=['Unnamed: 0'], inplace=True)

# Handle missing values by directly updating the DataFrame
for column in ['access_authentication', 'access_complexity', 'access_vector', 
               'impact_availability', 'impact_confidentiality', 'impact_integrity']:
    mode_value = data[column].mode()[0]
    data[column] = data[column].fillna(mode_value)

# Convert date columns to datetime and extract year, month, day
data['mod_date'] = pd.to_datetime(data['mod_date'])
data['pub_date'] = pd.to_datetime(data['pub_date'])
data['mod_year'] = data['mod_date'].dt.year
data['mod_month'] = data['mod_date'].dt.month
data['mod_day'] = data['mod_date'].dt.day
data['pub_year'] = data['pub_date'].dt.year
data['pub_month'] = data['pub_date'].dt.month
data['pub_day'] = data['pub_date'].dt.day

# Remove original date columns
data.drop(columns=['mod_date', 'pub_date'], inplace=True)

# Encode categorical variables
le = LabelEncoder()
for col in data.columns[data.dtypes == 'object']:
    data[col] = le.fit_transform(data[col])

# Define features and target
X = data.drop(columns=['cvss', 'summary'])  # Exclude 'summary' for simplicity
y = data['cvss'] > 5  # Binary classification: High severity (True) if CVSS score > 5

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=None)

# Initialize and train a Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=None)
model.fit(X_train, y_train)

# Save the model using joblib
model_filename = 'security_vuln.joblib'  
joblib.dump(model, model_filename)

# Make predictions and evaluate the model
y_pred = model.predict(X_test)
accuracy = model.score(X_test, y_test)
report = classification_report(y_test, y_pred)

# Print the results
print(f'Accuracy: {accuracy}')
print('Classification Report:')
print(report)

# Plotting the confusion matrix
cm = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(8, 6))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=['Non-Vulnerable', 'Vulnerable'], yticklabels=['Non-Vulnerable', 'Vulnerable'])
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix')
plt.show()

# Plotting feature importance
feature_importances = model.feature_importances_
indices = np.argsort(feature_importances)
plt.figure(figsize=(10, 8))
plt.title('Feature Importances')
plt.barh(range(len(indices)), feature_importances[indices], color='b', align='center')
plt.yticks(range(len(indices)), [X.columns[i] for i in indices])
plt.xlabel('Relative Importance')
plt.show()

# Plotting ROC Curve
fpr, tpr, _ = roc_curve(y_test, model.predict_proba(X_test)[:, 1])
roc_auc = auc(fpr, tpr)
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.legend(loc="lower right")
plt.show()
