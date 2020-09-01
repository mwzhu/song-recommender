import pandas
import numpy as np
from sklearn.model_selection import train_test_split
import Recommender as Recommender
import ssl
ssl._create_default_https_context = ssl._create_unverified_context

song_df_1 = pandas.read_table('https://static.turi.com/datasets/millionsong/10000.txt',header=None)
song_df_1.columns = ['user_id', 'song_id', 'listen_count']

#Read song  metadata
song_df_2 =  pandas.read_csv('https://static.turi.com/datasets/millionsong/song_data.csv')

#Merge the two dataframes above to create input dataframe for recommender systems
song_df = pandas.merge(song_df_1, song_df_2.drop_duplicates(['song_id']), on="song_id", how="left")
song_df['song'] = song_df['title'].map(str) + " - " + song_df['artist_name']
song_df = song_df.head(10000)

#Code to get most popular songs, but implementation is too slow#
# song_grouped = song_df.groupby(['song']).agg({'listen_count': 'count'}).reset_index()
# popular_songs = song_grouped.sort_values(['listen_count', 'song'], ascending = [0,1])
# popular_songs = popular_songs.head(1000)
# song_df = song_df.loc[song_df['song'].isin(popular_songs['song'])]

#Personalized song Recommender
train_data, test_data = train_test_split(song_df, test_size = 0.20, random_state=0)

is_model = Recommender.item_similarity_recommender_py()
is_model.create(train_data, 'user_id', 'song')

def recommend(songs):
    return is_model.get_similar_items(songs)

def unique_songs():
    unique_songs = np.sort(song_df['song'].unique())
    df = pandas.DataFrame(columns = ['Song'])
    for i in range(len(unique_songs)):
        df.loc[len(df)] = [unique_songs[i]]
    df.index = np.arange(1, len(df)+1)
    return df

def print_songs():
    list = []
    unique_songs = np.sort(song_df['song'].unique())
    for i in range(len(unique_songs)):
        list.append(unique_songs[i])
    return list
