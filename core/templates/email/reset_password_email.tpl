{% extends "mail_templated/base.tpl" %}

{% block subject %}
Reset Password Api
{% endblock %}

{% block preheader %}
{% endblock %}

{% block html %}
http://localhost:8000/accounts/api/v1/password/reset/confirm/{{ token }}
{% endblock %}