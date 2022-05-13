#!/usr/bin/env python
# coding: utf-8

# In[18]:


import numpy as np

def game_core_v3p(number):
    '''Начинаем угадывать с середины отрезка. Далее ограничиваем отрезок поиска медианой списка чисел
    между максимальным и минимальным значением. Для начала поиска минимум = 1, максимум = 100, медиана 50'''
    count = 1
    predict = 50
    minimum = 1
    maximum = 100
    while number != predict:
        count+=1
        if number > predict:
            minimum = predict
            predict = (maximum + minimum + 1) // 2
        else:
            maximum = predict
            predict = (maximum + minimum) // 2
    return count

        
def score_game(game_core):
    '''Запускаем игру 1000 раз, чтобы узнать, как быстро игра угадывает число'''
    count_ls = []
    np.random.seed(1)  # фиксируем RANDOM SEED, чтобы ваш эксперимент был воспроизводим!
    random_array = np.random.randint(1,101, size=(1000))
    for number in random_array:
        count_ls.append(game_core(number))
    score = int(np.mean(count_ls))
    print(f"Ваш алгоритм угадывает число в среднем за {score} попыток")
    return(score)


# In[19]:


# запускаем
score_game(game_core_v3)


# In[ ]:




