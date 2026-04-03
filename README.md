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

Columns to drop for feature set: school, medu, fedu, Dalc, Walc. This application does not require to know your school unlike the dataset that kept records on whether you attended Gabriel Pereira or Mousinho de Silveira school. For user convenience, I am working to filtering out the least important feature sets so we don't bore users with details to fill.

each categorical column in both datasets and their respective encoder meaning using LabelEncoder
sex F-0, M-1
address U-1, R-0 (rural or urban)
famsize GT3-0, LE3-1 (greater than three or less than three)
pstatus T-1, A-0 (T for living together and A for Apart)
mjob at-home-0, health-1, other-2, services-3, teacher-4
fjob at-home-0, health-1, other-2, services-3, teacher-4
reason course-0, home-1, other-2, reputation-3
guardian father-0, mother-1
schoolsup no-0, yes-1
famsup no-0, yes-1
paid no-0, yes-1
activities no-0, yes-1
nursery no-0, yes-1
higher no-0, yes-1
internet no-0, yes-1
romantic no-0, yes-1
