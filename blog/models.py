from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

#   Это поведение следует применять при удалении объекта, на который указывает ссылка . 
#   Это не относится к Django; это стандарт SQL. Хотя у Django есть собственная реализация поверх SQL.
#   Существует семь возможных действий, которые необходимо предпринять при возникновении такого события:
#     CASCADE: когда объект, на который указывает ссылка, удаляется, также удаляйте объекты, 
#     которые имеют ссылки на него (например, когда вы удаляете сообщение в блоге, вы также 
#     можете удалить комментарии). Эквивалент SQL: CASCADE.

    PostTitle = models.CharField(max_length=200, blank=True)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

#   blankопределяет, будет ли поле обязательным в формах. 
#   Это включает в себя администратора и ваши пользовательские формы. 
#   Если blank=Trueто поле не будет обязательным, тогда как если это Falseполе не может быть пустым.
#   Комбинация этих двух вариантов встречается так часто, потому что, 
#   как правило, если вы собираетесь разрешить пустое поле в своей форме, 
#   вам также понадобится ваша база данных, чтобы разрешить NULLзначения для этого поля. 
#   Исключение составляют файлы CharFields и TextFields, 
#   которые в Django никогда не сохраняются как файлы NULL. 
#   Пустые значения сохраняются в БД как пустая строка ('').



    def publish(self):
        if self.published_date is None:
            self.published_date = timezone.now()

        if self.PostTitle == '':
            self.PostTitle = check(self.text)

        self.save()

    def __str__(self):
        if self.PostTitle == '':
            return check(self.text)
        return self.PostTitle

def check(text):
    letters = 'А́а́Е́е́И́и́О́о́У́у́Ы́ы́Э́э́Ю́ю́Я́я́ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЁйцукенгшщзхъфывапролджэячсмитьбюёQWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
    symbols = text.split(' ')[:2]

    fixedText = [i for i in symbols[0] if i in letters]

    if len(symbols) > 1:
        fixedText = fixedText + [' '] + [i for i in symbols[1] if i in letters]

    fixedText = ''.join(fixedText)

    if len(fixedText) > 200:
        print('bigger')
        fixedText = fixedText[:193] + '...'
        print(fixedText)

    return fixedText
