"""
###########################################################
This is an automatically generated file! Do no edit!

If price changes exists, modify catalogue in SalesForce instead 
and regenerate file
###########################################################
""" 

TAX = {{ tax }}

CATALOGUE = {}

{% for p in products %}
CATALOGUE['{{ p.code }}'] = {'price': {{ p.price }}, 'description': "{{ p.description }}"}
{% endfor %}


