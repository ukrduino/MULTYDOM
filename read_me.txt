при ошибке No module named 'django.forms.util'
Для починки CKeditor
исправить и файле где ошибка util на utilS
-from django.forms.util import flatatt		 +from django.forms.utils import flatatt