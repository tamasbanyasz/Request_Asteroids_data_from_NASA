from lyricsgenius import Genius
from pandas import DataFrame
from re import sub, escape
from string import punctuation
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tag import pos_tag
from itertools import groupby
from random import choice


class SelectTrackLyrics:
    def __init__(self, artist_name):
        self.artist_name = artist_name
        self.token = 'n6pObQoAE-FlcBm6eYdwjCscQ0wHMEhJbQ0szM8OfoNZqempOWhVKRLO3mPzqFh-'
        self.genius = Genius(self.token, remove_section_headers=True, skip_non_songs=True, verbose=False, timeout=10)

        self.artists = self.genius.search_artists(search_term=self.artist_name, per_page=50, page=1)
        self.artists = self.artists['sections'][0]['hits']

    def search_artist(self):
        artists_df = DataFrame(columns=['Artist'])

        for index in range(len(self.artists)):
            artists_df.loc[len(artists_df['Artist'].index)] = self.artists[index]['result']['name']

        artists_df.index += 1

        print(artists_df)
        return artists_df

    def select_artist(self):
        artists_df = self.search_artist()
        artist_id = 0

        while artist_id == 0:
            selected_index_number = int(input("Choose artist by index number: "))
            if selected_index_number not in artists_df.index:
                print("Wrong ID number.")

            for index, artist in enumerate(self.artists, 1):
                if selected_index_number == index:
                    artist_id = artist['result']['id']

        return artist_id

    def search_albums(self):
        artist_albums = None

        while not artist_albums:
            artist_id = self.select_artist()
            artist = self.genius.artist_albums(artist_id)
            artist_albums = artist['albums']
            if not artist_albums:
                print(f"\n'{artist_albums}'... Empty albums list. :( \n")

        albums_df = DataFrame(columns=['Album_name'])
        album_id_numbers_df = DataFrame(columns=['Album_id'])

        for album in artist_albums:
            albums_df.loc[len(albums_df.index)] = album['name']
            album_id_numbers_df.loc[len(album_id_numbers_df.index)] = album['id']
            album_id_numbers_df['Album_id'] = album_id_numbers_df['Album_id'].astype('int32')

        albums_df.index += 1
        album_id_numbers_df.index += 1

        print(albums_df)
        return albums_df, album_id_numbers_df

    def select_album(self):
        albums_name, albums_ids = self.search_albums()
        album_id = 0

        while album_id == 0:
            album_title = int(input("Choose album by index number: "))
            if album_title not in albums_name.index:
                print("Wrong ID number.")
            else:
                album_id = albums_ids['Album_id'][album_title]

        return album_id

    def search_track(self):
        album_id = self.select_album()

        album_tracks = self.genius.album_tracks(album_id)
        tracks = album_tracks['tracks']

        track_title_df = DataFrame(columns=['Track_name'])
        song_url_df = DataFrame(columns=['Song_url'])

        for index in range(len(tracks)):
            if not tracks[index]['song']['instrumental']:
                track_title_df.loc[len(track_title_df.index)] = tracks[index]['song']['title']
                song_url_df.loc[len(song_url_df.index)] = tracks[index]['song']['url']

        track_title_df.index += 1
        song_url_df.index += 1

        print(track_title_df)
        return track_title_df, song_url_df

    def selected_track(self):
        tracks_title, song_url = self.search_track()

        track_url = None

        while not track_url:
            track_title = int(input("Choose track by index number: "))
            if track_title not in tracks_title.index:
                print("No lyrics found.")
            else:
                track_url = song_url['Song_url'][track_title]

        print(f'\n{track_url}')
        return track_url

    def selected_song_lyrics(self):

        track_url = self.selected_track()

        song_lyrics = self.genius.lyrics(song_url=track_url)
        song_lyrics = song_lyrics.split("\n")[1:]
        song_lyrics = "\n".join(song_lyrics)

        chars = escape(punctuation)
        clear_lyrics = sub(r'[' + chars + ']', '', song_lyrics)

        print(f'{clear_lyrics}\n')
        return clear_lyrics


class LyricsAnalysis:
    def __init__(self):
        self.artist_1 = SelectTrackLyrics("Eminem")
        self.artist_2 = SelectTrackLyrics("Led Zeppelin")
        self.sia = SentimentIntensityAnalyzer()

        self.song_lyrics_from_artist_1 = self.artist_1.selected_song_lyrics()
        self.song_lyrics_from_artist_2 = self.artist_2.selected_song_lyrics()

        self.lyrics_words_from_song_1 = self.song_lyrics_from_artist_1.split()
        self.lyrics_words_from_song_2 = self.song_lyrics_from_artist_2.split()

        self.lyrics_words_from_song_1 = [words.lower() for words in self.lyrics_words_from_song_1]
        self.lyrics_words_from_song_2 = [words.lower() for words in self.lyrics_words_from_song_2]

        self.same_words_per_time_in_dict = {}
        self.get_same_word()

    def get_same_word(self):
        for word in self.lyrics_words_from_song_1:
            self.same_words_per_time_in_dict[word] = list(self.lyrics_words_from_song_2).count(word)

    def print_same_word(self):
        for key, value in self.same_words_per_time_in_dict.items():
            if value:
                print(f"The word '{key.capitalize()}' from the Song 1 appeared '{value}' times in the Song 2 lyrics"
                      )

    def sentiments_of_lyrics(self):
        result_1 = self.sia.polarity_scores(self.song_lyrics_from_artist_1)
        result_2 = self.sia.polarity_scores(self.song_lyrics_from_artist_2)

        print(f'\nFirst lyrics : {result_1}')
        print(f'Second lyrics : {result_2}\n')

    def create_random_sentence_from_the_dict_of_same_words(self):
        tags = pos_tag([key for key, value in self.same_words_per_time_in_dict.items() if value])

        result = {k: [*map(lambda v: v[0], values)]
                  for k, values in groupby(sorted(tags, key=lambda x: x[1]), lambda x: x[1])}
        print(result)

        pos_tags = ['DT', 'NN', 'VBZ', 'IN', 'NN', 'CC', 'JJ', 'PRP', 'NN']

        selected_tags = []

        for tag in pos_tags:
            if tag in result.keys():
                selected_tags.append(result[tag][choice(range(len(result[tag])))])

        res = ' '.join(selected_tags).capitalize()
        print(f'\n{res}\n')


lyrics_analyzis = LyricsAnalysis()
lyrics_analyzis.print_same_word()
lyrics_analyzis.sentiments_of_lyrics()
lyrics_analyzis.create_random_sentence_from_the_dict_of_same_words()
