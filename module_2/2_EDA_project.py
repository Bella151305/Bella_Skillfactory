#!/usr/bin/env python
# coding: utf-8

# In[308]:


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations
from scipy.stats import ttest_ind
import re

pd.set_option('display.max_rows', 50) # показывать больше строк
pd.set_option('display.max_columns', 50) # показывать больше колонок

stud_math = pd.read_csv('stud_math.xls')


# Суть проекта — отследить влияние условий жизни учащихся в возрасте от 15 до 22 лет на их успеваемость по математике, чтобы на ранней стадии выявлять студентов, находящихся в группе риска.
# 
# Стадии выполнения проекта:
# 1. Проведение первичной обработки данных.
# 2. Анализ и очистка числовых переменных.
# 3. Преобразование и оценка номинативных переменных.
# 4. Выводы относительно качества данных и степени влияния переменных.

# In[309]:


display(stud_math.head(10))
stud_math.info()


# 1. Тип данных: 13 числовых столбцов и 17 номенативных.
# 2. Полнота данных: имеются столбцы, в том числе числовые, с отсутствующими данными.

# In[310]:


stud_math.columns


# In[311]:


# изменяем названия столбцов: все с маленькой буквы
stud_math.columns = [column.lower() for column in stud_math.columns]
stud_math.columns


# In[312]:


# Создаем функцию для определения выбросов в числовых столбцах
def column_IQR(column):
    
    median = column.median()
    perc25 = column.quantile(0.25)
    perc75 = column.quantile(0.75)
    IQR = perc75 - perc25
    ma = column.max()
    mi = column.min()
    
    if mi < perc25 - 1.5*IQR or ma > perc75 + 1.5*IQR:
        x = 'Есть выбросы'
    else:
        x = 'Нет выбросов'
    
    return print('25-й перцентиль: {},'.format(perc25), '75-й перцентиль: {},'.format(perc75),
                 'IQR: {}, '.format(IQR),'Границы выбросов: [{f}, {l}].'.format(f=perc25 - 1.5*IQR, l=perc75 + 1.5*IQR),
                '{}.'.format(x))


# In[313]:


# Создаем функцию описания числовых столбцов
def column_describe(column):
    return column.describe()


# In[314]:


# Создаем функцию графиков числовых столбцов
def column_hist(df, column):
    df[column].hist()
    plt.title(column)
    plt.show()
    return plt.show()


# In[315]:


# Анализируем числовые столбцы на наличие выбросов и пустых строк, считаем их количество
# Избавляемся от выбросов пока только в копии базы и считаем их количество
for column in stud_math[['age', 'medu', 'fedu', 'traveltime', 'studytime',
                      'failures', 'studytime, granular', 'famrel', 'freetime',
                      'goout', 'health', 'absences', 'score']]:
    
    stud_math_2 = stud_math.copy()
    stud_math_2 = stud_math_2.loc[stud_math_2[column].between(stud_math_2[column].quantile(0.25)
                                                              - 1.5*(stud_math_2[column].quantile(0.75)-stud_math_2[column].quantile(0.25))
                                                              , stud_math_2[column].quantile(0.75)
                                                              + 1.5*(stud_math_2[column].quantile(0.75)-stud_math_2[column].quantile(0.25))
                                                             )]

    print('{},'.format(column), 'Количество строк без данных: {},'.format(stud_math['age'].count() - stud_math[column].count())
          , '% строк без данных: {},'.format(round((stud_math['age'].count() - stud_math[column].count())/stud_math['age'].count()*100, 2))
          , 'Количество выбросов: {},'.format(stud_math[column].count() - stud_math_2[column].count())
          , '% выбросов: {},'.format(round((stud_math[column].count() - stud_math_2[column].count())/stud_math[column].count()*100, 2)))


# In[316]:


# В базе много строк с остутствием данных (>10). Посмотрим их корреляцию с score
stud_math_3 = stud_math.copy()
for column in stud_math_3[['fedu', 'traveltime', 'failures', 'famrel', 'freetime', 'health', 'absences']]:

    stud_math_3 = stud_math_3.loc[stud_math_3[column].between(stud_math_3[column].quantile(0.25)
                                                              - 1.5*(stud_math_3[column].quantile(0.75)-stud_math_3[column].quantile(0.25))
                                                              , stud_math_3[column].quantile(0.75)
                                                              + 1.5*(stud_math_3[column].quantile(0.75)-stud_math_3[column].quantile(0.25))
                                                             )]


# In[286]:


sns.pairplot(stud_math_3[['fedu', 'traveltime', 'failures', 'famrel', 'freetime', 'health', 'absences', 'score']], kind = 'reg')


# In[317]:


stud_math_3[['fedu', 'traveltime', 'failures', 'famrel', 'freetime', 'health', 'absences', 'score']].corr()


# Корреляция с score всех этих параметров невелика.
# 
# Не будем их принимать во внимание.

# In[318]:


for column in stud_math[['fedu', 'traveltime', 'failures', 'famrel', 'freetime', 'health', 'absences']]:
    stud_math.drop(column, inplace = True, axis = 1)


# In[319]:


# Посмотрим корреляцию остальных показателей с score
for column in stud_math[['age', 'medu', 'studytime', 'studytime, granular', 'goout']]:

    stud_math = stud_math.loc[stud_math[column].between(stud_math[column].quantile(0.25)
                                                        - 1.5*(stud_math[column].quantile(0.75)-stud_math[column].quantile(0.25))
                                                        , stud_math[column].quantile(0.75)
                                                        + 1.5*(stud_math[column].quantile(0.75)-stud_math[column].quantile(0.25))
                                                       )]


# In[304]:


sns.pairplot(stud_math[['age', 'medu', 'studytime', 'studytime, granular', 'goout', 'score']], kind = 'reg')


# In[320]:


stud_math[['age', 'medu', 'studytime', 'studytime, granular', 'goout', 'score']].corr()


# Параметр "studytime, granular" (нет в описании) имеет обратную корреляцию со временем на учёбу помимо школы.
# 
# Не будем его принимать во внимание.

# In[321]:


stud_math.drop(['studytime, granular'], inplace = True, axis = 1)


# Выводы по числовым столбцам.
# 
# Основное влияние на результат по математике имеют:
# 
# 1. Наибольшее влияние на результат оказывает образование матери (чем оно выше, тем лучше результат) - теперь мы знаем, кто помогает детям с математикой:)
# 2. Также большое влияние на результат оказывает возраст ученика (чем старше ученик, тем хуже результат) - этот показатель напрямую связан с проведением времени с друзьями, что вполне объяснимо (чем старше ученик, тем  больше времени он тратит на друзей, а не на учебу).
# 3. На третьем месте по влиянию на результат экзамена - время на учёбу помимо школы (чем оно больше, тем лучше результат).

# In[328]:


# Функции создания дата фрейма,...
def column_valcount(df, column):
    return display(pd.DataFrame(df[column].value_counts()))

# ... подстчетов значений,...
def column_10uni(df, column):
    return print("Значений, встретившихся в столбце более 10 раз:", (df[column].value_counts()>10).sum()
                 , ", ", "Уникальных значений:", df[column].nunique())

# ... выведения общей информации о номенативных столбцах
def column_info(df, column):
    return df.loc[:, [column]].info()


# In[323]:


# Заменяем пропуски на None и анализируем номенативные столбцы
for column in stud_math[['school', 'sex', 'address', 'famsize', 'pstatus', 'mjob', 'fjob',
                         'reason', 'guardian', 'schoolsup', 'famsup', 'paid', 
                         'activities', 'nursery', 'higher', 'internet', 'romantic']]:
    
    stud_math[column] = stud_math[column].astype(str).apply(lambda x: None if x.strip() == '' else x)
    
    column_valcount(stud_math, column)
    column_info(stud_math, column)


# In[329]:


def get_boxplot(column):
    fig, ax = plt.subplots(figsize = (14, 4))
    sns.boxplot(x=column, y='score', 
                data=stud_math.loc[stud_math.loc[:, column].isin(stud_math.loc[:, column].value_counts().index[:10])],
               ax=ax)
    plt.xticks(rotation=45) # поворот текста по оси
    ax.set_title('Boxplot for ' + column)
    plt.show()


# In[330]:


for col in ['school', 'sex', 'address', 'famsize', 'pstatus', 'mjob', 'fjob',
            'reason', 'guardian', 'schoolsup', 'famsup', 'paid', 
            'activities', 'nursery', 'higher', 'internet', 'romantic']:
    get_boxplot(col)


# 1. Школа: в основном сдают экзамен одинаково, MS чуть хуже, но гораздо меньше ус с плохими оценками чем в GP, однако есть.
# 2. Пол: мальчики в среднем сдают экзамен лучше девочек.
# 3. Тип адреса: ученики, проживающие в городе, в среднем сдают экзамен лучьше учеников, проживающих за городом; среднее значение у них чуть выше, однако плотность результатов выше среднего значительно больше.
# 4. Размер семьи: разброс значений в основном объеме в семьях больше 3 человек больше, а среднее значение такое же как в других семьях.
# 5. Как ни странно, раздельное проживание родтелей положительно сказывается на результате.
# 6. Работа матери: не удивительно, что ученики, мамы которых работают учителями, лучше сдают (не факт, что знают) математику, а тех, чьи работают в сфере услуг - знают математику; также видно, что мамы, сидящие дома, участвуют (как могут) в образовании ребенка; вспомним также, что именно образование мам лучше всего сказывается на результатах экзамена.
# 7. Работа отца: та же история - ученики, отцы которых работают учителями, лучше (но не в массе) знают математику; плотность результатов выше среднего значительно больше "у пап", работающих в сфере медицины; а сидящие вот дома отцы не сильно вникают в проблемы детей.
# 8. Школьная образовательная программа не особо помогает ученикам; близость к дому - важнее, но в общем, не сильно влияет на результат, а вот репутация - наше все.
# 9. Разброс значений в основном объеме при материнском опекунстве больше, чем при опекунстве отца, а среднее значение у них на одном уровне; если опекун - не родитель, результаты чуть хуже, однако нет результатов ниже 1 квартилии.
# 10. Дополнительная образовательная поддержка льшь мешает ученикам сосредоточиться на математике.
# 11. Семейная образовательная поддержка тоже не помогает большинству учеников.
# 12. Дополнительные платные занятия по математике дают меньше низких оценок, больше плотность оценок выше среднего.
# 13. Дополнительные внеучебные занятия полезны - расширяют сознание :)
# 14. Посещение детского сада немного помагает - дает много друзей, у котоых можно списать :)
# 15. Без математики в высшем учебном заведении делать нечего.
# 16. Если мама что-то не знает - OK, Google!, но внашем случае скорее - Go LOL! - отрицательный эффект
# 17. А вот романтические отношения сокрее больше помогут в написании сочинения.

# In[336]:


# Проверим, есть ли статистическая разница в распределении оценок по номинативным признакам, с помощью теста Стьюдента.
def get_stat_dif(column):
    cols = stud_math.loc[:, column].value_counts().index[:10]
    combinations_all = list(combinations(cols, 2))
    for comb in combinations_all:
        if ttest_ind(stud_math.loc[stud_math.loc[:, column] == comb[0], 'score'], 
                        stud_math.loc[stud_math.loc[:, column] == comb[1], 'score']).pvalue \
            <= 0.05/len(combinations_all):
            print('Найдены статистически значимые различия для колонки', column)
            break


# In[337]:


for col in ['school', 'sex', 'address', 'famsize', 'pstatus', 'mjob', 'fjob',
            'reason', 'guardian', 'schoolsup', 'famsup', 'paid', 
            'activities', 'nursery', 'higher', 'internet', 'romantic']:
    get_stat_dif(col)


# На основании полученных данных я бы исключила:
# 1. Аббревиатуру школы - репутация дает больше информации о школе;
# 2. Гендерный признак - сдвиг основного объема незначителен - качество определения группы риска от этого не пострадает.

# In[338]:


for column in stud_math[['school', 'sex']]:
    stud_math.drop(column, inplace = True, axis = 1)


# In[340]:


stud_math_for_model = stud_math
stud_math_for_model.info()


# B результате EDA для анализа влияния условий жизни учащихся в возрасте от 15 до 22 лет на их успеваемость по математике были получены следующие выводы:
# 
# 1. В данных достаточно много пустых значений и выбрасов, а также много (а именно 37) сторок с нулевым значением основного показателя score - данные весьма разнородны.
# 2. Из числовых параметров наибольшее положительное влияние оказывают образование матери и время на учёбу помимо школы, отрицательное - возраст ученика и проведение времени с друзьями.
# 3. Из номенативных показателей более или менее важны все кроме аббревиатуры школы и гендерного признака.
# 4. Статистически значимые различия найдены только в показателе желания получить высшее образование.

# Комментарий
# 
# Вызывает вопрос момент с "обрезанием выбрасов". Находя выбрасы в какм-то параметре мы, как я поняла, выкидываем из данных эти строки. Однако в этих же строках дрогого параметра могут (и скорее всего) не содержатся выбросы, а мы эти строки уже исключили из анализа... Как тогда очищать данные? Для каждого столбца создавать копию, в ней обрезать выбросы и анализировать каждый парамент отдельно? Но тогда о применении функций не может идти и речи, а трудозатраты возрастают многократно...

# In[ ]:




