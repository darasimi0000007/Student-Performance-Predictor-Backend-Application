# SHAP: Quick Reference Guide for Student Performance Prediction

## What is SHAP?

**SHAP (SHapley Additive exPlanations)** uses game theory to explain individual predictions from machine learning models. It answers: *"How much did each feature contribute to this specific prediction?"*

### Core Concept: SHAP Value
$$\text{Prediction} = \text{Base Value} + \sum (\text{SHAP Value}_i)$$

- **Base Value**: Average prediction across all training data
- **SHAP Value**: Each feature's contribution to the deviation from base value
- **Sum of SHAP Values**: Total deviation = Final Prediction - Base Value

---

## Why SHAP for Student Performance?

| Challenge | SHAP Solution |
|-----------|---------------|
| Model is a "black box" | SHAP explains individual predictions |
| Why did a student fail? | SHAP shows which factors pushed toward fail |
| Feature importance unclear | SHAP provides individual & global importance |
| Building stakeholder trust | SHAP offers interpretable explanations |
| Fairness concerns | SHAP reveals if biased features drive predictions |

---

## SHAP in Your Project

### Installation
```bash
pip install shap
```

### Basic Workflow
```python
import shap
from sklearn.ensemble import RandomForestClassifier

# Train your model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Create SHAP explainer (fast for tree models)
explainer = shap.TreeExplainer(model)

# Calculate SHAP values
shap_values = explainer.shap_values(X_test)

# Visualize
shap.summary_plot(shap_values[1], X_test, feature_names=feature_names)
```

---

## Visualization Guide

### 1. **Summary Plot (Bar Chart)**
**Shows**: Which features matter most overall  
**Best For**: Quick feature importance ranking  
**Interpretation**: 
- Taller bar = more important feature
- Measures mean absolute SHAP values

```python
shap.summary_plot(shap_values[1], X_test, plot_type="bar", 
                 feature_names=feature_names)
```

### 2. **Summary Plot (Beeswarm)**
**Shows**: Individual feature impacts and their range  
**Best For**: Understanding feature distribution effects  
**Interpretation**:
- Left = pushes toward FAIL
- Right = pushes toward PASS
- Red dots = high feature value
- Blue dots = low feature value
- Spread = variability in impact

```python
shap.summary_plot(shap_values[1], X_test, feature_names=feature_names)
```

### 3. **Force Plot**
**Shows**: How one student's prediction was made  
**Best For**: Explaining individual predictions  
**Interpretation**:
- Red (left) = factors pushing toward FAIL
- Blue (right) = factors pushing toward PASS
- Width = magnitude of effect
- Final value = model's prediction

```python
shap.force_plot(explainer.expected_value[1], shap_values[1][0], 
               X_test[0], feature_names=feature_names)
```

### 4. **Dependence Plot**
**Shows**: Relationship between feature value and SHAP impact  
**Best For**: Finding feature interactions  
**Interpretation**:
- X-axis: Feature value
- Y-axis: SHAP value (impact on prediction)
- Pattern reveals non-linear relationships
- Color shows interacting feature

```python
shap.dependence_plot(feature_index, shap_values[1], X_test, 
                    feature_names=feature_names)
```

### 5. **Waterfall Plot**
**Shows**: Step-by-step breakdown of one prediction  
**Best For**: Detailed explanation of model reasoning  
**Interpretation**:
- Base value (starting point)
- Each bar = one feature's contribution
- Red = pushes toward FAIL
- Blue = pushes toward PASS
- Final value = actual prediction

```python
explainer = shap.Explainer(model, X_train)
shap_vals = explainer(X_test)
shap.plots.waterfall(shap_vals[0])
```

---

## Feature Importance Ranking

**Global Importance** (all students):
```python
# Mean absolute SHAP values
feature_importance = np.abs(shap_values[1]).mean(axis=0)
importance_df = pd.DataFrame({
    'Feature': feature_names,
    'Importance': feature_importance
}).sort_values('Importance', ascending=False)
```

**Local Importance** (specific student):
```python
# SHAP values for one prediction
sample_importance = np.abs(shap_values[1][student_index])
local_importance_df = pd.DataFrame({
    'Feature': feature_names,
    'SHAP_Value': shap_values[1][student_index],
    'Abs_SHAP_Value': sample_importance
}).sort_values('Abs_SHAP_Value', ascending=False)
```

---

## Key SHAP Properties

| Property | Explanation |
|----------|-------------|
| **Consistency** | If model output increases, feature's SHAP value never decreases |
| **Accuracy** | SHAP values sum to (prediction - base value) |
| **Local Accuracy** | SHAP values explain the exact prediction made |
| **Global Accuracy** | SHAP values average to feature importance |

---

## Common SHAP Explainers

### TreeExplainer (Recommended for Your Model)
- **Use When**: Tree-based models (RandomForest, XGBoost, LightGBM)
- **Speed**: ⚡ FAST
- **Accuracy**: 100% accurate
- **Cost**: Efficient computation

```python
explainer = shap.TreeExplainer(model)
```

### KernelExplainer (Model-Agnostic)
- **Use When**: Any model type
- **Speed**: 🐌 SLOW
- **Accuracy**: Approximation
- **Best For**: Complex models, when TreeExplainer unavailable

```python
explainer = shap.KernelExplainer(model.predict, X_background)
```

### LinearExplainer (Linear Models)
- **Use When**: Linear models only
- **Speed**: ⚡ FAST
- **Use For**: Logistic Regression, Linear Regression

```python
explainer = shap.LinearExplainer(model, X_train)
```

---

## Interpreting SHAP for Pass/Fail Predictions

### Positive SHAP Values (→ PASS)
These features push the prediction toward passing:
- Good attendance
- High study time
- Good family support
- Health/motivation factors

### Negative SHAP Values (→ FAIL)
These features push the prediction toward failing:
- Frequent absences
- Low study time
- Previous failures
- Travel time issues

---

## Real Example Interpretation

**Student #5 - Predicted to PASS**
- Base value: 0.45 (50% average chance of passing)
- High study time: +0.15 (helps pass)
- Good attendance: +0.12 (helps pass)
- Family support: +0.08 (helps pass)
- Travel time: -0.05 (hurts pass chance)
- **Final Prediction: 0.75** (75% confidence in passing)

---

## Best Practices

✅ **DO:**
- Use SHAP alongside traditional feature importance
- Compare explanations across multiple students
- Validate explanations with domain knowledge
- Document your findings
- Update model and explanations regularly

❌ **DON'T:**
- Treat SHAP values as causation
- Ignore feature interactions
- Over-interpret small SHAP differences
- Assume all features are equally modifiable
- Base all decisions only on SHAP values

---

## Troubleshooting

### Issue: SHAP values not summing to prediction
**Cause**: Using class 0 vs class 1 explanations  
**Solution**: Use correct class index (0=FAIL, 1=PASS)

### Issue: Force plot too crowded
**Cause**: Too many features with similar importance  
**Solution**: Plot only top 10-15 features

### Issue: Slow computation
**Cause**: Large dataset with KernelExplainer  
**Solution**: Use TreeExplainer or reduce sample size

---

## Integration with Your Code

```python
# In your main.py or FastAPI app
from shap_analysis import SHAPAnalyzer

# Initialize
analyzer = SHAPAnalyzer("ml_model/stud_performance_classifier.joblib")

# Load data
X_test, X_train, features = analyzer.load_and_prepare_data("data/student-mat.csv")

# Create explainer
analyzer.create_explainer(X_train)

# Get explanations for API predictions
top_features = analyzer.get_top_features_for_prediction(sample_index=0, top_n=5)
```

---

## Further Learning

- **SHAP GitHub Issues**: Real-world examples and solutions
- **Interpretable ML Book**: christophm.github.io/interpretable-ml-book
- **SHAP Paper**: "A Unified Approach to Interpreting Model Predictions"
- **Kaggle Notebooks**: Search "SHAP" for diverse applications

