#!/usr/bin/env python
# coding: utf-8

# In[429]:


import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import itertools as it
from collections import Counter


# In[430]:


data = pd.read_csv('movie_bd_v5.xls')
data.sample(5)


# In[431]:


data.describe()


# # Предобработка

# In[432]:


# создадим словарь для ответов
answers = {}

# тут другие ваши предобработки колонок например:

#the time given in the dataset is in string format.
#So we need to change this in datetime format
data.release_date = data.release_date.apply(lambda d: pd.to_datetime(d))
# и заменяем данные в колонке с даты на месяц, так как только он нам понадобится
data.release_date = data.release_date.dt.month

# рассчитаем и добавим в датасет колонку profit
data['profit'] = data['revenue'] - data['budget']


# # 1. У какого фильма из списка самый большой бюджет?

# Использовать варианты ответов в коде решения запрещено.    
# Вы думаете и в жизни у вас будут варианты ответов?)

# In[433]:


# в словарь вставляем номер вопроса и ваш ответ на него
# Пример: 
answers['1'] = '2. Spider-Man 3 (tt0413300)'
# запишите свой вариант ответа
answers['1'] = '5. Pirates of the Caribbean: On Stranger Tides (tt1298650)'
# если ответили верно, можете добавить комментарий со значком "+"


# In[434]:


# тут пишем ваш код для решения данного вопроса:
data_max_budget = data[data['budget'] == data['budget'].max()]
data_max_budget['original_title']


# ВАРИАНТ 2

# In[435]:


# можно добавлять разные варианты решения
data.loc[data['budget'] == data['budget'].max()].imdb_id


# # 2. Какой из фильмов самый длительный (в минутах)?

# In[438]:


# думаю логику работы с этим словарем вы уже поняли, 
# по этому не буду больше его дублировать
answers['2'] = '2. Gods and Generals (tt0279111)'
answers['3'] = '3. Winnie the Pooh (tt1449283)'
answers['4'] = '2. 110'
answers['5'] = '1. 107'
answers['6'] = '5. Avatar (tt0499549)'
answers['7'] = '5. The Lone Ranger (tt1210819)'
answers['8'] = '1. 1478'
answers['9'] = '4. The Dark Knight (tt0468569)'
answers['10'] = '5. The Lone Ranger (tt1210819)'


# In[439]:


data.loc[data['runtime'] == data['runtime'].max()].original_title


# # 3. Какой из фильмов самый короткий (в минутах)?
# 
# 
# 
# 

# In[441]:


data.loc[data['runtime'] == data['runtime'].min()].original_title


# # 4. Какова средняя длительность фильмов?
# 

# In[443]:


int(round(data.runtime.mean(),0))


# # 5. Каково медианное значение длительности фильмов? 

# In[445]:


int(round(data.runtime.median(),0))


# # 6. Какой самый прибыльный фильм?
# #### Внимание! Здесь и далее под «прибылью» или «убытками» понимается разность между сборами и бюджетом фильма. (прибыль = сборы - бюджет) в нашем датасете это будет (profit = revenue - budget) 

# In[446]:


# лучше код получения столбца profit вынести в Предобработку что в начале
data.loc[data['profit'] == data['profit'].max()].original_title


# # 7. Какой фильм самый убыточный? 

# In[447]:


data.loc[data['profit'] == data['profit'].min()].original_title


# # 8. У скольких фильмов из датасета объем сборов оказался выше бюджета?

# In[449]:


data.query('profit>0').profit.count()


# # 9. Какой фильм оказался самым кассовым в 2008 году?

# In[451]:


data_2008 = data.query('release_year==2008')
data_2008.loc[data_2008['revenue'] == data_2008['revenue'].max()].original_title


# # 10. Самый убыточный фильм за период с 2012 по 2014 г. (включительно)?
# 

# In[452]:


data_1214 = data.query('2012<=release_year<=2014')
data_1214.loc[data_1214['profit'] == data_1214['profit'].min()].original_title


# # 11. Какого жанра фильмов больше всего?

# In[454]:


# эту задачу тоже можно решать разными подходами, попробуй реализовать разные варианты
# если будешь добавлять функцию - выноси ее в предобработку что в начале
data['genres'].str.split('|').explode().value_counts().head(1)


# ## ВАРИАНТ 2

# In[455]:


answers['11'] = '3. Drama'
answers['12'] = '1. Drama'
answers['13'] = '5. Peter Jackson'
answers['14'] = '3. Robert Rodriguez'
answers['15'] = '3. Chris Hemsworth'
answers['16'] = '3. Matt Damon'
answers['17'] = '2. Action'


# # 12. Фильмы какого жанра чаще всего становятся прибыльными? 

# In[458]:


data_profit = data.query('profit>0')
data_profit['genres'].str.split('|').explode().value_counts().head(1)


# # 13. У какого режиссера самые большие суммарные кассовые сбооры?

# In[460]:


data_dir_rev = data.groupby(['director']).sum()
data_dir_rev.loc[data_dir_rev['revenue'] == data_dir_rev['revenue'].max()].index[0]


# # 14. Какой режисер снял больше всего фильмов в стиле Action?

# In[462]:


data_dir_ac = data[data.genres.str.contains('Action', na=False)]
data_dir_ac['director'].str.split('|').explode().value_counts().head(1)


# # 15. Фильмы с каким актером принесли самые высокие кассовые сборы в 2012 году? 

# In[465]:


data_12 = data.query('release_year==2012')[['cast', 'revenue']]
data_12.cast = data_12.cast.apply(lambda c: c.split('|'))
data_12_cast = data_12.explode('cast')
data_12_cast.groupby(by = 'cast').revenue.sum().sort_values(ascending = False).head(1)


# # 16. Какой актер снялся в большем количестве высокобюджетных фильмов?

# In[467]:


data_v_bud = data.loc[data['budget'] > data['budget'].mean()]
data_v_bud['cast'].str.split('|').explode().value_counts().head(1)


# # 17. В фильмах какого жанра больше всего снимался Nicolas Cage? 

# In[468]:


data_NC = data[data.cast.str.contains('Nicolas Cage', na=False)]
data_NC['genres'].str.split('|').explode().value_counts().head(1)


# # 18. Самый убыточный фильм от Paramount Pictures

# In[470]:


data_PP = data[data.production_companies.str.contains('Paramount Pictures', na=False)]
data_PP.loc[data_PP['profit'] == data_PP['profit'].min()].original_title


# In[471]:


answers['18'] = '1. K-19: The Widowmaker (tt0267626)'
answers['19'] = '5. 2015'
answers['20'] = '1. 2014'
answers['21'] = '4. Сентябрь'
answers['22'] = '2. 450'


# # 19. Какой год стал самым успешным по суммарным кассовым сборам?

# In[473]:


data_year = data.groupby(['release_year']).sum()
data_year.loc[data_year['revenue'] == data_year['revenue'].max()].index[0]


# # 20. Какой самый прибыльный год для студии Warner Bros?

# In[475]:


data_WB = data[data.production_companies.str.contains('Warner Bros', na=False)].groupby(['release_year']).sum()
data_WB.loc[data_WB['profit'] == data_WB['profit'].max()].index[0]


# # 21. В каком месяце за все годы суммарно вышло больше всего фильмов?

# In[477]:


data.release_date.value_counts().head(1)


# # 22. Сколько суммарно вышло фильмов летом? (за июнь, июль, август)

# In[479]:


data.loc[data['release_date'].isin(['6', '7', '8'])].count().head(1)


# # 23. Для какого режиссера зима – самое продуктивное время года? 

# In[481]:


data_w = data.loc[data['release_date'].isin(['12', '1', '2'])].groupby(['director']).count()
data_w.loc[data_w['imdb_id'] == data_w['imdb_id'].max()].index[0]


# In[484]:


answers['23'] = '5. Peter Jackson'
answers['24'] = '5. Four By Two Productions'
answers['25'] = '3. Midnight Picture Show'
answers['26'] = '1. Inside Out, The Dark Knight, 12 Years a Slave'
answers['27'] = '5. Daniel Radcliffe & Rupert Grint'


# # 24. Какая студия дает самые длинные названия своим фильмам по количеству символов?

# In[485]:


data_ot = data.copy()
data_ot.original_title = data_ot.original_title.apply(lambda ot: len(ot))
data_ot_m = data_ot.loc[data_ot['original_title'] == data_ot['original_title'].max()]
data_ot_m['production_companies'].str.split('|').explode()


# # 25. Описание фильмов какой студии в среднем самые длинные по количеству слов?

# In[486]:


data_overview = data.copy()
data_overview.overview = data_overview.overview.apply(lambda owl: len(owl.split()))
data_pc_ow = data_overview.groupby(['production_companies']).mean()
data_pc_ow.loc[data_pc_ow['overview'] == data_pc_ow['overview'].max()]


# # 26. Какие фильмы входят в 1 процент лучших по рейтингу? 
# по vote_average

# In[487]:


data_1 = data.groupby(['vote_average', 'original_title'])['imdb_id'].count()
data_1.tail(int(round(data.original_title.count()/100, 0)))


# # 27. Какие актеры чаще всего снимаются в одном фильме вместе?
# 

# In[489]:


cast_values = [x.split('|') for x in data['cast']]
pairs = [it.combinations(x, 2) for x in cast_values]
pairs_set = pd.Series([set(y) for x in pairs for y in x]).apply(tuple)
pairs_set.value_counts().head()


# ВАРИАНТ 2

# # Submission

# In[490]:


# в конце можно посмотреть свои ответы к каждому вопросу
answers


# In[491]:


# и убедиться что ни чего не пропустил)
len(answers)


# In[ ]:





# In[ ]:




