# Cosas utiles que aprendi en este proyecto

## Internacionalizacion

https://phrase.com/blog/posts/translate-python-gnu-gettext/
https://stackoverflow.com/questions/53816180/how-to-update-the-po-and-pot-files-in-gettext-module-using-python
https://simpleit.rocks/python/how-to-translate-a-python-project-with-gettext-the-easy-way/#updating-existing-translations
https://mlocati.github.io/articles/gettext-iconv-windows.html (para hacer update de los archivos PO que no viene por default con python)

python C:\Anaconda3\envs\general\Tools\i18n\pygettext.py -d base -o locales/base.pot app.py


Asumiendo que el po ya esta creado en "es"

msgmerge --update .\locales\es\LC_MESSAGES\base.po .\locales\base.pot (requiere que este instalado el msgmerge)

 python C:\Anaconda3\envs\general\Tools\i18n\msgfmt.py -o .\locales\es\LC_MESSAGES\base.mo .\locales\es\LC_MESSAGES\base  (para crear el mo)