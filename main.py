import streamlit as st
import pandas as pd
from sklearn import datasets
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,classification_report, accuracy_score

st.set_page_config(page_title="Ex-stream-ly Cool App",
                    page_icon="⭐",
                    layout="wide",
                    initial_sidebar_state="expanded",
                   menu_items={
                       'Get Help': 'https://www.extremelycoolapp.com/help',
                       'Report a bug': "https://www.extremelycoolapp.com/bug",
                       'About': "# This is a header. This is an *extremely* cool app!"
                   }
                   )
st.markdown('''<h4 style='text-align: left; color: #d73b5c;'>* Data is based "IMDB 5000 Movie Dataset"</h4>''',
                unsafe_allow_html=True)
st.title("Streamlit Example")
st.write("""
# Explore Different Classifier
Which one is the best?
""")
dataset_name = st.sidebar.selectbox("Select Dataset",("Iris","Breast Cancer","Wine dataset"))
classifier_name = st.sidebar.selectbox("Select Classifier",("KNN","SVM","Random Forest"))
def get_dataset(dataset_name):
    if dataset_name == "Iris":
        data = datasets.load_iris()
    elif dataset_name == "Breast Cancer":
        data = datasets.load_breast_cancer()
    else:
        data = datasets.load_wine()
    X = data.data
    y = data.target
    return X,y
X,y = get_dataset(dataset_name)

st.write("shape of datasets",X.shape)
st.write("number of classes",len(np.unique(y)))

def add_parameter(classifier_name):
    params = dict()
    if classifier_name == "KNN":
        K = st.sidebar.slider("K",1,15)
        params["K"] = K
    elif classifier_name == "SVM":
        C = st.sidebar.slider("C",0.01,10.0) # kayan nokta(float) value
        params["C"] = C
    else:
        max_depth = st.sidebar.slider("max_depth",2,15)
        n_estimators = st.sidebar.slider("n_estimators",1,100)
        params["max_depth"] = max_depth
        params["n_estimators"] = n_estimators
    return params
params = add_parameter(classifier_name)
st.write(f"Parameters: {params}")

def get_classifier(classifier_name,params):
    if classifier_name == "KNN":
        clf = KNeighborsClassifier(n_neighbors = params["K"])
    elif classifier_name == "SVM":
        clf = SVC(C = params["C"])
    else:
        clf = RandomForestClassifier(max_depth=params["max_depth"],n_estimators=params["n_estimators"])
    return clf
clf = get_classifier(classifier_name,params)

X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=42)

clf.fit(X_train,y_train)
y_pred = clf.predict(X_test)
acc = accuracy_score(y_test,y_pred)
#classReport = classification_report(y_test,y_pred)
st.write(f"Classifier Name: {classifier_name}")
st.write(f"Accuracy Score: {acc}")

#x = st.slider('Select a value')
#st.write(x, 'squared is', x * x)





