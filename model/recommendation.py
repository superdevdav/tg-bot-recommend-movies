from imports import *


credits = pd.read_csv(r'D:\Рабочий стол\kursovaya\model\data\TMDBdataset\credits.csv')
movies = pd.read_csv(r'D:\Рабочий стол\kursovaya\model\data\TMDBdataset\movies.csv')

credits.columns = ['id', 'title', 'cast', 'crew']
movies_data = movies.merge(credits, on='id')
#print(movies.head(2))

# средняя оценка (голос) по всей таблице
C = movies_data['vote_average'].mean()
#print(C)

# минимальное количество голосов для попадания 
m = movies_data['vote_count'].quantile(0.9)
#print(m)

#qualified movies
q_movies = movies_data.copy().loc[movies_data['vote_count'] >= m]

def weighted_rating(df, m=m, C=C):
  v = df['vote_count']
  R = df['vote_average']
  return (v/(v+m) * R) + (m/(v+m) * C)

q_movies['score'] = q_movies.apply(weighted_rating, axis=1)
q_movies = q_movies.sort_values('score', ascending=False)
#q_movies.head()
q_movies = q_movies.loc[:, ['original_title', 'vote_count', 'vote_average', 'score']]

# Объект векторизатор TF-IDF. Удаление всех английских стоп-слов, таких как 'the', 'a'.
tfidf = TfidfVectorizer(stop_words="english")
# Замена NaN пустой строкой
movies_data['overview'] = movies_data['overview'].fillna('')
# Создание матрицы TF-IDF путем подгонки и преобразования данных
tfidf_matrix = tfidf.fit_transform(movies_data['overview'])

# Вычисление величины, обозначающей сходство между двумя фильмами
# cosine similarity matrix
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

# series индексов и названий фильмов
indices = pd.Series(movies_data.index, index=movies_data['original_title']).drop_duplicates()

def get_recommendations(original_title, cosine_sim=cosine_sim):
  try:
      idx = indices[original_title]
      # Получение оценок попарного сходства всех фильмов с этим фильмом
      sim_scores = list(enumerate(cosine_sim[idx]))

      # Сортировка фильмов по оценке попарного сходства
      sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

      # оценки топ 10 фильмов
      sim_scores = sim_scores[1:11]

      # получение индексов фильмов
      movie_indices = [i[0] for i in sim_scores]

      return list(movies_data['original_title'].iloc[movie_indices])
  except:
      return ["Нет такого фильма"]

#print(get_recommendations('Batman Forever'))

features = ['cast', 'crew', 'keywords', 'genres']
for feat in features:
  movies_data[feat] = movies_data[feat].apply(literal_eval)

# Получение имени директора из crew
def get_director(x):
  for i in x:
      if i['job'] == 'Director':
          return i['name']
  return np.nan

# Возвращаем 3 первых элемента списка или весь список целиком
def get_list(x):
  if isinstance(x, list):
      names = [i['name'] for i in x]
      if len(names) > 3:
          names = names[:3]
      return names
  return []

movies_data['director'] = movies_data['crew'].apply(get_director)

features = ['cast', 'keywords', 'genres']
for feat in features:
  movies_data[feat] = movies_data[feat].apply(get_list)

# удаление пробелов и привидение к нижнему регистру
def edit_data(x):
  if isinstance(x, list):
      return [str.lower(i.replace(' ', '')) for i in x]
  else:
      if isinstance(x, str):
          return str.lower(x.replace(' ', ''))
      return ''

features = ['cast', 'director', 'genres', 'keywords']

for feat in features:
  movies_data[feat] = movies_data[feat].apply(edit_data)

def create_metadata_soup(x):
  return ' '.join(x['keywords']) + ' ' + ' '.join(x['cast']) + ' ' + x['director'] + ' ' + ' '.join(x['genres'])
movies_data['soup'] = movies_data.apply(create_metadata_soup, axis=1)

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(movies_data['soup'])

cosine_sim2 = cosine_similarity(count_matrix, count_matrix)

movies_data = movies_data.reset_index()
indices = pd.Series(movies_data.index, index=movies_data['original_title'])

#recommMoviesList = get_recommendations('Minions', cosine_sim2)
#print(recommMoviesList)