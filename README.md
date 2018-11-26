# Mini-Readability Parser


Большинство веб-страниц сейчас перегружено всевозможной рекламой... Наша задача «вытащить»
из веб-страницы только полезную информацию, отбросив весь «мусор» (навигацию, рекламу и тд).
Полученный текст нужно отформатировать для максимально комфортного чтения в любом
текстовом редакторе. 

Правила форматирования: 

- ширина строки не больше 80 символов (если
больше, переносим по словам);
- абзацы и заголовки отбиваются пустой строкой
- если в тексте
встречаются ссылки, то URL вставить в текст в квадратных скобках. 

Остальные правила на ваше усмотрение.

Программа оформляется в виде **утилиты командной строки**, которой **в качестве параметра
указывается произвольный URL**. Она извлекает по этому URL страницу, обрабатывает ее и
формирует текстовый файл с текстом статьи, представленной на данной странице.
В качестве примера можно взять любую статью на lenta.ru, gazeta.ru и тд
Алгоритм должен быть максимально универсальным, то есть работать на большинстве сайтов.

**Усложнение задачи 1**: Имя выходного файла должно формироваться автоматически по URL.
Примерно так:
http://lenta.ru/news/2013/03/dtp/index.html => [CUR_DIR]/lenta.ru/news/2013/03/dtp/index.txt

**Усложнение задачи 2**: Программа должна поддаваться настройке – в отдельном файле/файлах
задаются шаблоны обработки страниц.

## Требования к выполнению задачи

- Задача выполняется на С++|Python с использованием классов. Не должно использоваться
сторонних библиотек, впрямую решающих задачу.
- Предпочтительная среда выполнения – MS Windows.
- Решение должно состоять из документа, описывающего алгоритм, исходных кодов
программы, исполняемого модуля.
- Приложите список URL, на которых вы проверяли свое решение. И результаты проверки.
- Желательно указать направление дальнейшего улучшения/развития программы.

---

## Алгоритм

Предположим, что полезный контент на html-странице обычно представляет собой текст в виде предложений, отформатированных с использованием html-тегов для текстовой разметки: p, h1-h6, b, i и др.; ссылок, специальных блоков (например, code). 
Сам полезный контент обычно содержится внутри блоков div, article или section.

1. Преобразуем html-документ в дерево html-тегов.   
1. Рекурсивно обходим дерево и в каждом узле:
   - отбрасываем узел, если он должен быть проигнорирован (настраивается в `config.py`)
   - сохраняем узел в качестве кандидата на контейнер с полезным контентом
   - удаляем узел из дерева
1.  Для всех полученных контейнеров считаем стоимость, исходя из:
    - количества предложений в тексте
    - длины предложения
    - частоты встречаемости знаков препинания в предложении
1. Выбираем узел с наибольшей стоимостью
1. Рекурсивно обходим потомков узла и форматируем их содержимое согласно правилам в `config.py` 


## Возможные улучшения

1. Добавить эвристики в функцию стоимости, например:
   - количество вложенных "нетекстовых" и "текстовых" тегов
   - средняя длина слова
   - повторяющиеся css-классы/id для отсечения блоков с комментариями, где тоже может быть много текста
   - игнорировать множество классов, обычно используещееся не для оформления текста (например, .nav)
   - возможно, игнорировать элементы с атрибутами `hidden` и т.п.
1. Использовать методы data science для:
   - поиска наиболее важных параметров функции стоимости
   - настройки весов функции стоимости
   - определения назначения блоков, исходя из их положения на странице
1. Более полно покрыть код тестами для безопасного внесения изменений
1. Извлекать из статьи картинки
1. Формировать на выход документ в markdown

## Примеры работы

Программа тестировалась на URL:

- https://www.gazeta.ru/sport/news/2018/11/23/n_12322837.shtml -> [результат](examples/1.txt) 
- https://lenta.ru/news/2018/11/23/elephants/
- https://meduza.io/news/2018/11/23/fsb-soobschila-o-pytkah-v-reabilitatsionnyh-tsentrah-v-saratove-tam-uderzhivayut-lyudey-s-alkogolnoy-i-narkozavisimostyu
- http://www.nashgorod.ru/news/economy/23-11-2018/rossiyane-uhodyat-v-on-layn-prodazhi-cherez-doski-ob-yavleniy-i-sotsseti-dostigli-600-mlrd
- https://rg.ru/2018/11/23/v-kremle-obiavili-datu-bolshoj-press-konferencii-putina.html
- https://medium.com/s/nerd-processor/the-ultimate-guide-to-fantastic-beasts-2-460814f88d79
- https://habr.com/company/mailru/blog/429186/