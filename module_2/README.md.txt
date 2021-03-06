
Краткое описание

Основные цели и задачи проекта: отследить влияние условий жизни учащихся в возрасте от 15 до 22 лет на их успеваемость по математике, 
чтобы на ранней стадии выявлять студентов, находящихся в группе риска.

Краткая информация о данных: в базе данных содержится ряд числовых и номенативных параметров разной степени полноты, призванных (возможно) объяснить 
зезультат получения учеником указанного балла на госэкзамене по математике.

Этапы работы над проектом:
1. Проведение первичной обработки данных.
2. Анализ и очистка числовых переменных.
3. Преобразование и оценка номинативных переменных.
4. Выводы относительно качества данных и степени влияния переменных.

Основные выводы.

B результате EDA для анализа влияния условий жизни учащихся в возрасте от 15 до 22 лет на их успеваемость по 
математике были получены следующие выводы:

1. В данных достаточно много пустых значений и выбрасов, а также много (а именно 37) сторок с нулевым значением 
основного показателя score - данные весьма разнородны.
2. Из числовых параметров наибольшее положительное влияние оказывают образование матери и время на учёбу помимо 
школы, отрицательное - возраст ученика и проведение времени с друзьями.
3. Из номенативных показателей более или менее важны все кроме аббревиатуры школы и гендерного признака.
4. Статистически значимые различия найдены только в показателе желания получить высшее образование.

Комментарий.

Вызывает вопрос момент с "обрезанием выбрасов". Находя выбрасы в какм-то параметре мы, как я поняла, выкидываем 
из данных эти строки. Однако в этих же строках дрогого параметра могут (и скорее всего) не содержатся выбросы, а 
мы эти строки уже исключили из анализа... Как тогда очищать данные? Для каждого столбца создавать копию, в ней 
обрезать выбросы и анализировать каждый парамент отдельно? Но тогда о применении функций не может идти и речи, 
а трудозатраты возрастают многократно...

Ответы на вопросы саморефлексии:

1. Какова была ваша роль в команде?

К сожалению, не участвовала в камандном решении задач - сложно организоваться во времени, а просто пользователем
быть не хочется.

2. Какой частью своей работы вы остались особенно довольны?

Самостоятельностью.

3. Что не получилось сделать так, как хотелось? Над чем ещё стоит поработать?

Не получилось доконца разобраться с работой функций. С синтаксисом работаю по методу тыка.

4. Что интересного и полезного вы узнали в этом модуле?

Все было интересно и полезно, поскольку ново. Особенно интересны были полученные на основе анализа выводы.

5. Что является вашим главным результатом при прохождении этого проекта?

Открытие ряда инструментов анализа данных.

6. Планируете ли вы менять стратегию изучения последующих модулей?

Да. Постараюсь найти время для более полного изучения синтаксиса.