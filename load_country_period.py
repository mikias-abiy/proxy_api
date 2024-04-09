#!/usr/bin/python3

from api.ps_api import ps_api
from models.db_models.country import Country
from models.db_models.period import Period

from models import storage


country_ipv4 = ps_api.referenceList('ipv4')['items']['country']

country_mix = ps_api.referenceList('mix')['items']['country']

periods = ps_api.referenceList('mix')['items']['period']


for country in country_ipv4:
    name = country['name']
    country_id = country['id']
    type = 'ipv4'
    cnt = Country(country_id=country_id, name=name, type=type)
    cnt.save()



for country in country_mix:
    name = country['name']
    country_id = country['id']
    type = 'ipv4'
    cnt = Country(country_id=country_id, name=name, type=type)
    cnt.save()

for period in periods:
    response = ps_api.orderCalcIpv4(countryId=country_ipv4[0]['id'], periodId=period['id'], quantity=1, authorization=None, coupon=None, customTargetName="test_pack")
    name = period['name']
    period_id = period['id']
    price = response['price']
    prd = Period(period_id=period_id, name=name, price=price)
    prd.save()