# Student Performance Predictor
Project Overview:
This project is a backend system focused on predicting the performance of a student according to different individual factors


Dataset Summary:
The Student Performance Dataset is a publicly available educational dataset from the UCI Machine Learning Repository. It contains detailed student records from Portuguese secondary schools, designed to support research on academic achievement modeling and predictive analytics.
Here is the link to the dataset: https://archive.ics.uci.edu/dataset/320/student+performance

Check the page for what each column means:
'school', 'sex', 'age', 'address', 'famsize', 'Pstatus', 'Medu', 'Fedu',
       'Mjob', 'Fjob', 'reason', 'guardian', 'traveltime', 'studytime',
       'failures', 'schoolsup', 'famsup', 'paid', 'activities', 'nursery',
       'higher', 'internet', 'romantic', 'famrel', 'freetime', 'goout', 'Dalc',
       'Walc', 'health', 'absences', 'G1', 'G2', 'G3'

Column headers are the same for both datasets

Columns to drop for feature set: school. This application does not require to know your school unlike the dataset that kept records on whether you attended Gabriel Pereira or Mousinho de Silveira school. For user convenience, I am working to filtering out the least important feature sets so we don't bore users with details to fill