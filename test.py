test = '1-hnl'
import pycountry
test=test.split('-')

country=test[-1:]
print(country[0])
country = country[0]
#country='fr'
#print(country)
league_country=pycountry.countries.get(alpha_2=f'{country}')
print(league_country.name)