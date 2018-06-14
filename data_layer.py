import django
import apps.generated_world.models as m
from django.db.models import Count, Sum

import datetime
django.setup()

'''
TO RUN THIS FILE:
1) Start the Django Shell:
    
--> python manage.py shell

2) Load and run a file:

EXAMPLE 1
>>> exec(open('data_layer.py').read())

EXAMPLE 2
>>> exec(open('apps/generated_world/data_layer.py').read())

'''

# for club in m.Club.objects.all():
#     print('{} --> \t{}'.format(club.league.name, club.name))

# for league in m.League.objects.filter(sport__contains='ball'):
#     print('{} - {}'.format(league.sport, league.name))
#     for club in league.clubs.all():
#         print('\t{}'.format(club.name))

# for city in m.City.objects.filter(population__lt=15000).order_by('-population'):
#     print('{}\t{}'.format(city.population, city.name))

# for club in m.Club.objects.filter(memberships__person__last='Smith'):
#     print(club.name)
#     for membership in club.memberships.filter(person__last='Smith'):
#         print('\t{} {}'.format(membership.person.first, membership.person.last))

# 1. Returns all the state capitals
def state_capitals():
    for city in m.City.objects.filter(is_capital=1):
        print(city.state.name)

# 2. Returns all cities in reverse order by population
def city_ordered_by_population():
    for city in m.City.objects.all().order_by('-population'):
        print(city.name)

# 3. Takes in a string (sport) and returns the leagues for that sport
def find_leagues_sport(sport):
    for league in m.League.objects.filter(sport=sport):
        print(league.name)
# find_leagues_sport('Cricket')

# 4. Takes in a string (name_fragment) and returns the clubs that contain that string in their name
def find_club_fragment_name(name_fragment):
    for club in m.Club.objects.filter(name__contains = name_fragment):
        print(club.name)
# find_club_fragment_name('City')

# 5. Takes in a string (name_fragment) and returns the companies that do not contain that string in their name
def find_companies_name_not(name_fragment):
    for company in m.Company.objects.exclude(name__contains = name_fragment):
        print(company.name)
# find_companies_name_not('Film')

# 6. Takes in a float and returns the companies that have a net income below that float
def find_company_net_income_below(income):
    for company in m.Company.objects.filter(net_income__lt = income):
        print(company.name)
# find_company_net_income_below(10.5)

# 7. Takes in an integer and returns the streets that match that integer
def find_address_street_number(street_number):
    for address in m.Address.objects.filter(street__contains = street_number):
        print(address.street)
# find_address_street_number(123)

# 8. Takes in two integers and finds the cities with a population between those two integers
def find_cities_population_range(minimum, maximum):
    for city in m.City.objects.filter(population__gt = minimum, population__lt = maximum):
        print(city.name)
# find_cities_population_range(1000, 2000)

# 9. Takes in a cardinal direction and returns the cities that contain that are named accordingly
def find_city_cardinal_direction(cardinal_direction):
    for city in m.City.objects.filter(name__startswith = cardinal_direction):
        print(city.name)
# find_city_cardinal_direction('West')

# 10. Takes in a company association and returns the companies that contain that company association
def find_company_association(association):
    for company in m.Company.objects.filter(name__endswith = association):
        print(company.name)
# find_company_association('Ltd.')





# QUERIES 2
# 1. Takes in a string (department) and returns the companies that have that department
def find_companies_department(department):
    for company in m.Company.objects.filter(departments__name=department):
        print(company.name)
# find_companies_department('Engineering')

# 2. Finds all the people who are currently employed
def find_employed_people():
    for person in m.Person.objects.filter(jobs__is_employed=1):
        print(person.id, person.first)
# find_employed_people()

# 3. Finds all the people who currently play for a given club
def find_player_in_club(club_name):
    for person in m.Person.objects.filter(memberships__club__name=club_name, memberships__is_active=1):
        print(person.first)
# find_player_in_club('Los Little Blitz')

# 4. Finds all past addresses for a given person
def find_all_past_address(person_id):
    for address in m.Address.objects.filter(person__id=person_id, is_current=0):
        print(address.street)
# find_all_past_address(1)

# 5. Finds all the companies for a given industry
def find_companies_by_industry(industry_name):
    for company in m.Company.objects.filter(listings__industry=industry_name):
        print(company.id, company.name)
# find_companies_by_industry('Transportation')

# # 6. Finds all the clubs for a given league
def find_club_from_league(league_name):
    for club in m.Club.objects.filter(league__name=league_name):
        print(club.name)
# find_club_from_league('Global Football League')

# 7. Finds the state with the most number of cities
def find_state_with_most_number_cities():
    state = m.State.objects.annotate(num_cities=Count('cities')).order_by('-num_cities').first()
    print(state.name, state.num_cities)
# find_state_with_most_number_cities()

# 8. Finds the most populous state
def find_populus_state():
    state = m.State.objects.annotate(num_population=Sum('cities__population')).order_by('-num_population').first()
    print(state.name, state.num_population)
# find_populus_state()

# 9. Finds the total assets for a given industry
def find_total_industry_assets(industry_name):
    industry = m.Company.objects.filter(listings__industry = industry_name).aggregate(total_asset=Sum(
        'total_assets'))
    print(industry['total_asset'])
# find_total_industry_assets('Transportation')

# 10. Find the companies for a given industry after a certain date
def find_companies_industry_certain_date(industry_name, certain_date):
    for company in m.Company.objects.filter(listings__industry = industry_name, founded_on__gte=certain_date):
        print(company.name)
# find_companies_industry_certain_date('Transportation', datetime.date(1950, 5, 21))


# QUERIES 3
# 1. Returns the states in descending order by the number of cities they have
def state_descending_by_cities_they_have():
    for state in m.State.objects.annotate(num_cities=Count('cities')).order_by('-num_cities'):
        print(state.name, state.num_cities)
# state_descending_by_cities_they_have()

# 2. Returns the clubs that have the most past memberships
def club_with_most_memberships():
    for club in m.Club.objects.filter(memberships__is_active=0).annotate(past_membership=Count('memberships__person')).order_by('-past_membership'):
        print(club.name, club.past_membership)
# club_with_most_memberships()
# ???????????????????????????????????????????????????????????????????

# 3. Returns the exchanges in descending order by the number of listings they have
def get_exchange_order_by_listing():
    for exchange in m.Exchange.objects.annotate(num_listing=Count('listings')).order_by('-num_listing'):
        print(exchange.name, exchange.num_listing)
# get_exchange_order_by_listing()

# 4. Returns the companies with the most number of departments
def find_companies_most_department():
    for company in m.Company.objects.annotate(num_department=Count('departments')).order_by('-num_department')[:10]:
        print(company.name, company.num_department)
# find_companies_most_department()

# 5. Returns the cities with the most employed people
def get_cities_with_most_employed():
    for city in m.City.objects.annotate(total_employee=Count('addresses__person')).filter(addresses__person__jobs__is_employed=1).order_by('-total_employee'):
        print(city.name, city.total_employee)
# get_cities_with_most_employed()

# 6. Returns the most profitable industries


# 7. Returns the leagues in order of past membership
# 8. Returns the industries with the highest rate of unemployment
# 9. Returns the cities with the most vacant addresses
# 10. Returns the states in descending order by revenue
