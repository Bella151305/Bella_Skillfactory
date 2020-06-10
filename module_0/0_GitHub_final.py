#!/usr/bin/env python
# coding: utf-8

# In[18]:


import numpy as np

def game_core_v3(number):
    '''Сначала загаданное число на эквивалентность 50. Затем уменьшаем или увеличиваем его
       в зависимости от того, больше оно или меньше нужного на 10. На последнем этапе перебираем по 1.
       Функция принимает загаданное число и возвращает число попыток'''
    count = 0
    predict = 50  # проверяем на эквивалентность 50
    if number > predict:
        for digit in [x for x in range(10,101,10)][5:]:  # формируем список выше 50
            predict = digit
            count += 1
            if number == predict:
                break
            elif number < predict:
                in_list = [in_digit for in_digit in range(digit-1,digit)]  # список для перебора по 1
                for in_digit in in_list:
                    predict = in_digit
                    count += 1
                if number == predict:
                    break
    elif number < predict:
        for digit in [x for x in range(10,101,10)][:5]:  # формируем список ниже 50
            predict = digit
            count += 1
            if number == predict:
                break
            elif number > predict:
                in_list = [in_digit for in_digit in range(digit-1,digit)] # список для перебора по 1
                for in_digit in in_list:
                    predict = in_digit
                    count += 1
                if number == predict:
                    break
    return(count) # выход из цикла, если угадали
        
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




