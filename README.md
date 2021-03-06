# AGRANT – Интегратор абитуриента 
## Введение

Приложение «AGRANT – Интегратор абитуриента» направленно  на создание интегрирующей взаимосвязанной информационной системы, включающей данные результатов итоговой аттестации выпускников школ, перечня различных программ подготовки бакалавриата и специалитета, количества бюджетных мест с использованием алгоритмов наилучшего распределения (в частности, алгоритма Гейла-Шепли) и системы автоматизированного отбора возможных вариантов.


## Дорожная карта проект

- [X] Анализ существующих информационных систем
- [X] Выявление и обоснование теоретической необходимости включения алгоритмов наилучшего распределения
- [X] Разработка приложения, реализующего модель информационной системы
    - Разработка базы данных пользователя и методов взаимодействия с ней
    - Создание баз данных вузов и программ обучения
    - Заполнение базы пользователей данными поступающих прошлых лет
    - Заполнение баз данных о вузах
    - Создание удобного и вариативного интерфейса (юзабилити)
    - Реализация алгоритма наилучшего распределения поступающих
- [X] Экспериментальная проверка возможности формирования оптимальной стратегии поступления

## Описание предлагаемого решения 

Предлагаемая нами модель является информационной системой, так как соответствует устоявшимся определениям.  

Функциональной особенностью обработки данных является использование алгоритма Гейла-Шепли, благодаря чему система производит расчет наилучшего распределения всех зарегистрированных в системе абитуриентов по бюджетным местам в соответствующих вузах.  

Прогнозируемо использование такого подхода к формированию стратегии поступления позволит с одной стороны минимизировать недоборы или, наоборот, высокий конкурс в вузы. С другой стороны самому поступающему не нужно будет тратить время на изучение и анализ конкурсных списков, чтобы минимизировать собственные риски. Таким образом, мы можем говорить, что предлагаемая модель приближает возможность формирования наиболее оптимальной стратегии поступления с минимальными рисками для обеих сторон.


## Экспериментальная проверка предлагаемого решения

>![](https://i.ibb.co/ZhdWSvB/2022-01-26-073852.png)  
Шаг 1. Открываем приложение, нажимаем кнопку «Регистрация», вводим необходимые данные

>![](https://i.ibb.co/fqNh7b3/Screenshot-2022-01-26-07-39-23.png)  
Шаг 2. Далее нажимаем на кнопку «Вход» и вводим данные для входа, после чего отобразится созданный профиль пользователя 

>![](https://i.ibb.co/7yXKCTp/2022-01-26-074005.png)  
Шаг 3. Вводим данные о результатах, полученных в ходе государственной итоговой аттестации.

>![](https://i.ibb.co/tsFMJzz/2022-01-26-074143.png)
![](https://i.ibb.co/v3hRLzS/2022-01-26-074127.png)  
Шаг 4. Заполняем данные о личных предпочтениях по направлениям подготовки и вузам.

>![](https://i.ibb.co/JngFLCT/Screenshot-2022-01-26-07-37-50.png)
![](https://i.ibb.co/9bMzM4X/Screenshot-2022-01-26-07-42-08.png)  
Шаг 5. Сохраняем введенные данные и обновляем данные. Система автоматически определит наилучшее возможное распределение, учитывая личные данные пользователя, а также данные других участников приемной кампании – как абитуриентов, так и вузов и приемных комиссий.


>![](https://i.ibb.co/QHycXGc/2022-01-26-074243.png)  
Шаг 6. Далее можно проверить свое место в списке, выбрав вуз и нужное нам направление с учетом выше упомянутых параметров.

Сравнивая наш результат с итогами поступления прошлого года можем заметить, что помимо более равномерной разницы баллов у абитуриентов еще вырос минимальный проходной балл, связанно это с тем, что выпускники, у которых было меньше баллов и которым все равно поступать на платку или бюджет могли рискнуть и попасть на бюджет, в тоже время люди с более высокими баллами оказались в пролете из-за боязни не поступить.


## Оценка результатов и перспективы

Созданная модель информационной системы полноценно отвечает запланированным результатам как ее использования (юзабилити), так и результатов ее работы на экспериментальной выборке.  

Оценивая перспективы внедрения данной модели, можно говорить об упрощении формирования стратегии поступления в вузы, благодаря использованию статистических и интеллектуально-ориентированных методов распределения, автоматизации процесса сбора данных как по выпускникам, так и по университетам. Как следствие, предлагаемое решение способно помочь минимизировать риски и упростить анализ возможных вариантов для поступления.

# Установка и запуск

Скачать проект
```bash
$ git clone https://github.com/OverHome/Agrant.git
$ cd Agrant
```

Установить нужные библиотеки
```bash 
$ pip install -r requirements.txt
```
Запустить приложение
```bash 
$ python main.py
```

