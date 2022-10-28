import pandas as pd
import streamlit as st
import altair as alt
alt.themes.enable("streamlit")


st.set_page_config(page_title="Movie Recommender System App",
                   page_icon="🎬",
                   layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items={
                       'Get Help': 'https://www.extremelycoolapp.com/help',
                       'Report a bug': "https://www.extremelycoolapp.com/bug",
                       'About': "# This is a header. This is an *extremely* cool app!"
                   },
                   )
st.markdown('''<h1 style='text-align: left; color: #000000;'> 🎬 IMDB Movie Recommender System</h1>''',
                unsafe_allow_html=True)


moviesDf = pd.read_csv("datasets/movies.csv")
ratingsDf = pd.read_csv("datasets/ratings.csv")
df = pd.merge(ratingsDf, moviesDf,how="left", on = "movieId")

st.sidebar.header("Please Filter Here:")
option = st.sidebar.selectbox(
    'Enter a movie name: ',
    (df.title.unique()))
sortBy = st.sidebar.selectbox(
    'Sort by: ',
    ('Correlation','Number of Ratings')
)

def createGenresList(df):
    genresList = []
    for genre in df.genres:
        genre = genre.split("|")
        for gen in genre:
            if gen not in genresList:
                genresList.append(gen)
    return genresList

def oheGenresDataframe(df):
    oheGenres = []
    genresList = createGenresList(df)
    for i in df.index:
        movie_data = [1 if genre in df.loc[i]["genres"].split("|") else 0 for genre in genresList]
        oheGenres.append(movie_data)
    return oheGenres
def createRatingDataFrame(df):
    meanRatingToTitle = df.groupby("title")["rating"].mean()
    countRatingToTitle = df.groupby("title")["rating"].count()
    ratingDf = pd.DataFrame({"meanRating": meanRatingToTitle, "countRating": countRatingToTitle})
    return ratingDf

def createToTitlePivotTable(df):
    usersPivotTable = pd.pivot_table(df, columns="title", index="userId", values="rating")
    return usersPivotTable

def correlationToMovie(df,movie):
    corrList = []
    usersPivotTable = createToTitlePivotTable(df)
    moviePivotTable = usersPivotTable[movie]
    for i in range(len(usersPivotTable.columns)):
        corrList.append(moviePivotTable.corr(usersPivotTable.iloc[:, i]))
    corrList = pd.Series(corrList)
    return corrList

def resultDataFrame(df, movie):
    usersPivotTable = createToTitlePivotTable(df)
    corrList = correlationToMovie(df,movie)
    ratingDf = createRatingDataFrame(df)
    totalDf = pd.DataFrame({"title": usersPivotTable.columns,
                            "Correlation": corrList,
                            "Number of Ratings": ratingDf.countRating.values})
    totalDf.dropna(inplace=True)
    if sortBy == "Correlation":
        resultDf = totalDf.loc[totalDf["Number of Ratings"] >= 50].sort_values(["Correlation"]).head(10)
    else:
        resultDf = totalDf.loc[totalDf["Number of Ratings"] >= 50].sort_values(["Number of Ratings"]).head(10)
    return resultDf

resultDf = resultDataFrame(df,option)
#st.write(resultDf)

totalRating = resultDf["Number of Ratings"].sum()/len(resultDf)
meanRating = round(resultDf["Number of Ratings"].mean()/len(resultDf),1)
starRating = ":star:"*int(round(meanRating,0))
left_column, right_column = st.columns(2)


with left_column:
    st.subheader("Total Rating")
    st.subheader(f"{totalRating}")
with right_column:
    st.subheader("Mean Rating")
    st.subheader(f"{meanRating} {starRating}")

def get_chart(resultDf):
    st.subheader(f"Recommend movies According to '{option}' film")
    annotation_layer = (
        alt.Chart(resultDf)
        .mark_bar(size=50, align="center", color="#000000", fontSize=20, fontStyle="bold", height=500)
        .encode(
            x="title",
            y="Correlation",
            color = sortBy,
            tooltip=[
                alt.Tooltip("title",title="title"),
                alt.Tooltip("Correlation",title="Correlation"),
                alt.Tooltip("Number of Ratings",title="Number of Ratings")
            ],
        )
    )
    st.altair_chart(annotation_layer,use_container_width=True)
get_chart(resultDf)

