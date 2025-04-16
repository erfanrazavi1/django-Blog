{% extends "mail_templated/base.tpl" %}

{% block subject %}
Accounts API
{% endblock %}

{% block html %}
http://localhost:8000/accounts/api/v1/activation/confirm/{{token}}
{% endblock %}