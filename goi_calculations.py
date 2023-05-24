""" COMMERCIAL REAL ESTATE - GOI CALCULATIONS ______________________________________________________________________ """

# Begining stages of creating formulas for Financial Model GUI
# This script will be used to pass in data regarding a multifamily property or another type of investment property real estate assets being built, acquired, or refinanced
# The GOI (Gross Operating Income) class will output Gross Potential Income, Total Economic Vacancy, and Gross Operating Income. 
# This is a simple calculation that will become more complex in the future and will be able to handle more forecasting data
# Staight calculations can be used to input data from any period, daily, weekly, monthly, yearly, five or 10-year summaries... etc.
# These formulas are used when calculating the top section of a Real Estate Investment Property Proforma


class GOI:
    def __init__(self):
        self.revenue_streams = {}
        self.vacancy_streams = {}
        self.total_units = 0  # Keep track of total units added

    # Total property potential
    def add_real_estate(self, property_type, num_units=None, avg_rent=None, rents=None):
        if avg_rent is None and rents is None:
            raise ValueError("You must provide either average rent or a list of rents.")
        if avg_rent is not None and rents is not None:
            raise ValueError("You cannot provide both average rent and a list of rents.")
        if rents is not None:
            avg_rent = sum(rents) / len(rents)
            num_units = len(rents)  # override num_units with the number of rents provided
        if num_units is None:
            raise ValueError("You must provide either num_units or a list of rents.")

        self.revenue_streams[property_type] = {
            'avg_revenue': avg_rent,
            'units': num_units,
        }

        # Update the total number of units
        self.total_units += num_units

    # Total vacancy (or vacancy prediction if using class if forward-looking financial statements)
    def subtract_real_estate(self, property_type, num_units=None, avg_rent=None, rents=None, total_vacancy=None):
        if total_vacancy is not None:
            if len(self.vacancy_streams) > 0:
                raise ValueError("You cannot provide total vacancy along with other types of real estate.")
            self.vacancy_streams['total'] = {'vacancy_percentage': total_vacancy}
            return
        else:
            if avg_rent is None and rents is None:
                raise ValueError("You must provide either average rent or a list of rents.")
            if avg_rent is not None and rents is not None:
                raise ValueError("You cannot provide both average rent and a list of rents.")
            if rents is not None:
                avg_rent = sum(rents) / len(rents)
                num_units = len(rents)
            if num_units is None:
                raise ValueError("You must provide either num_units or a list of rents.")

            # Check if the total units to subtract exceeds the total units added
            total_vacancy_units = sum(stream['units'] for stream in self.vacancy_streams.values())
            if total_vacancy_units + num_units > self.total_units:
                raise ValueError("The total number of units to subtract exceeds the total number of units added.")

            self.vacancy_streams[property_type] = {
                'avg_loss': avg_rent,
                'units': num_units,
            }

    def gross_potential_income(self):
        total_revenue = 0
        for revenue_stream, data in self.revenue_streams.items():
            total_revenue += data['avg_revenue'] * data['units']
        return total_revenue

    def less_total_economic_vacancy(self):
        total_loss = 0
        for vacancy_stream, data in self.vacancy_streams.items():
            if 'vacancy_percentage' in data:
                total_loss += self.gross_potential_income() * data['vacancy_percentage']
            else:
                total_loss += data['avg_loss'] * data['units']
        return total_loss

    def gross_operating_income(self):
        return self.gross_potential_income() - self.less_total_economic_vacancy()
 
my_business = GOI()


### Usage (unhash or copy and paste the lines below to add additional or different types of revenue to the calculation)


## TODO: add an input called category so that I can categorize difrent income sources based on unit type and group them to return subcategories that make up , which can be used to control the income category which will be added. This would be useful for mixed use, senior housing and hotel assets. 
## TODO: add additional error handling. In add_real_estate method, we are assuming that num_units is None only when rents are provided. But in the function parameters, we have num_units=None as a default. This might cause confusion if someone accidentally calls the function without giving num_units or rents.
## TODO: add current/ potential credit loss into GOI calculation

# Add various types of real estate and their rents
# Used to calculate current property potential if all units are rented out
# Can use this in multiple ways in final GUI regardless if someone wants to itemize units or input average rents based on unit type in Final GUI
my_business.add_real_estate('studio', num_units=5, avg_rent=500)
my_business.add_real_estate('one_bedroom', rents=[600, 620, 610])
my_business.add_real_estate('two_bedroom', rents=[600, 620, 610, 790])
my_business.add_real_estate('three_bedroom', rents=[1600, 1620, 1610])
### my_business.add_real_estate('one_bedroom', rents=[2600, 2620, 2610, 3120, 3432])
### my_business.add_real_estate('commercial_space', rents=[3000])

# TODO: Change the input structure of other fees to be a percentage of total units that are currently occupied; since not everyone will have a pet, and in certain business models like senior housing might have optional room service fees or food service, everyone will probably pay trash fee's though, so these are dynamic variables
my_business.add_real_estate('pet_fees', rents=[100])
my_business.add_real_estate('other_fee_1', rents=[3000]) 
my_business.add_real_estate('other_fee_2', rents=[3000])
my_business.add_real_estate('other_fee_3', rents=[3000])
my_business.add_real_estate('other_fee_4', rents=[3000])

# Subtract unrented units for certain types of real estate, used to calculate vacancy and subtract from total property potential 
# Note: You cannot use the total_vacancy factor when itemizing vacant units; this will be a feature that is toggled on and off when building out projections
my_business.subtract_real_estate('studio', num_units=5, avg_rent=500)
my_business.subtract_real_estate('one_bedroom', rents=[600, 620, 1200, 1500])
### my_business.subtract_real_estate('total', total_vacancy=0.05)


# Print the Gross Potential Income, Total Economic Vacancy, and Gross Operating Income
print(f'Monthly Gross Potential Income: ${my_business.gross_potential_income()}')
print(f'Monthly Total Economic Vacancy: ${my_business.less_total_economic_vacancy()}')
print(f'Monthly Gross Operating Income (GOI): ${my_business.gross_operating_income()}')


