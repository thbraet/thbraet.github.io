{% extends 'markdown.tpl' %}

{% block output %}
{{ cell.outputs | join('') | e }}
{% endblock %}
