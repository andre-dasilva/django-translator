===========
Translator
===========

Translator is an app for collecting translations for specified keys in django admin.

Quick start
-----------
#. Install django-translator: ``pip install django-translator``

#. Add ``django.middleware.locale.LocaleMiddleware`` to MIDDLEWARES settings.

#. Setup your languages in your settings::

	LANGUAGE_CODE = "de"

	LANGUAGES = [
		('de', _('German')),
		('en', _('English')),
		('fr', _('French')),
	]

#. Add "translator, taggit, modeltranslation" to your INSTALLED_APPS setting. Please note that ``modeltranslation`` needs to be before ``django.contrib.admin``::

	INSTALLED_APPS = (
	'modeltranslation',
	'django.contrib.admin',
	...
	'taggit',
	'translator',
	)

#. You have to set the migrations folder for the translator, because we have to add migrations for the set languages.  Add the following to your settings file::

	MIGRATION_MODULES = {
	    'translator': 'my_project.translator_migrations',
	}

#. Create a ``translator_migrations`` python package in your project folder (where your settings.py usually is).

#. Run ``python manage.py makemigrations translator`` to create the translator models based on the languages you specified in your settings file.

#. Run ``python manage.py migrate`` to migrate the translator models to your database.

#. If you intend to use it in the templates, add 'translator.context_processors.translator' to TEMPLATE_CONTEXT_PROCESSORS ::

	 TEMPLATE_CONTEXT_PROCESSORS = (
	 	...
	    'translator.context_processors.translator',
	 )

#. Create translation keys in your templates and models::

	Template::
	{{ translator.a_key }}

	models.py::
	from translator.util import translator_lazy as _

	class Product(models.Model):
		name = models.TextField(verbose_name=_(u"a_key"))

#. Visit the templates. The keys get collected lazy.

#. Translate the keys in the admin.

#. You can disable the translator by setting DJANGO_TRANSLATOR_ENABLED to False.

#. Use a double underscore in your translation keys to make use of the filter in the admin (e.g. "header__title" creates a filter called "header"). If you need another separator, set it as DJANGO_TRANSLATOR_CATEGORY_SEPARATOR in your setting file.

#. Define your urls like this::

	from django.conf.urls.i18n import i18n_patterns
	from django.contrib import admin
	from django.urls import include, path

	urlpatterns = i18n_patterns(
		path('admin/', admin.site.urls),
		path('i18n/', include('django.conf.urls.i18n')),
		prefix_default_language=False,
	)

#. Example language switcher for your templates::

	{% load i18n %} 
	
	<form action="{% url "set_language" %}" method="post"> 
		{% csrf_token %} 
		<input name="next" type="hidden" value="{{ redirect_to }}"> 
		<select name="language" onchange="this.form.submit()"> 
			{% get_current_language as LANGUAGE_CODE %} 
			{% get_available_languages as LANGUAGES %} 
			{% get_language_info_list for LANGUAGES as languages %} 
			{% for language in languages %} 
				<option value="{{ language.code }}"{% if language.code == LANGUAGE_CODE %} selected{% endif %}> 
					{{ language.name_translated }} 
				</option> 
			{% endfor %} 
		</select> 
	</form> 

Project Home
------------
https://github.com/dreipol/django-translator

PyPi
------------
https://pypi.python.org/pypi/django-translator
