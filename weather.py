import pandas as pd
import matplotlib.pyplot as plt

#We create a class for Weatherdata and define the required functions, referred to as methods.
class WeatherData:
    #method to load the data. Only first 30 rows are selected as final row as manual inspection reveals that 
    #final row is average. For larger datasets where manual checking not possible, line-by-line datachecks recommended.
    def __init__(self, file_path):
        try:
            self.df = pd.read_csv(file_path, delim_whitespace=True, header = 0)
            self.df = self.df[['Dy','MxT','MnT','AvT']]
            self.df = self.df.iloc[:30]
            self.df = self.df.rename(columns={
                'Dy': 'DayNumber',
                'MxT': 'MaxTemperature',
                'MnT': 'MinTemperature',
                'AvT': 'AverageTemperature'
            })

            self.df = self.df.applymap(lambda x: int(x.replace('*', '')) if '*' in str(x) else x)
            self.df = self.df.apply(pd.to_numeric, errors='coerce')
            
        except FileNotFoundError:
            print("The file you're trying to open does not exist.")
        except Exception as e:
            print(f"An error has occurred: {str(e)}")

    #method to print daily temperatures. As only first four rows are selected in the load method, entire df is printed. Alternative would be to 
    #relocate methods of renaming column headers and selecting required columns in this method instead.
    def print_daily_temperatures(self):
        print('The minimum, maximum and average temperatures for each day')
        print(self.df)

    #method which scans the AverageTemperature column for the id where value is maximised. Note that id and DayNumber are not coincident as 
    #id starts with 0 and DayNumber with 1
    #Using the id, the corresponding DayNumber is selected in the print command.
    def find_warmest_day(self):
        warmest_day = self.df['AverageTemperature'].idxmax()
        print('The day with the highest average temperature is day number ' +str(self.df.loc[warmest_day, 'DayNumber']) + ' with an average temperature of ' 
              +  str(self.df.loc[warmest_day, 'AverageTemperature']) + 'F')

    #method which scans the AverageTemperature column for the id where value is minimised. Note that id and DayNumber are not coincident as id starts with 0 and DayNumber with 1
    #Using the id, the corresponding DayNumber is selected in the print command.
    def find_coolest_day(self):
        coolest_day = self.df['AverageTemperature'].idxmin()
        print('The day with the lowest average temperature is day number ' +str(self.df.loc[coolest_day, 'DayNumber']) + ' with an average temperature of ' 
              +  str(self.df.loc[coolest_day, 'AverageTemperature']) + 'F')

    #method which creates a new column titled TemperatureRange by calculating the absolute difference between the MaxTemperature and MinTemperature columns.
    #From this new dataframe column, the id or row where the TemperatureRange is minimised is selected.
    #In the print statement, a range of relevant information is outputed by using different columns of the relevant row.
    def find_smallest_range(self):
        self.df['TemperatureRange'] = abs(self.df['MaxTemperature'] - self.df['MinTemperature'])
        min_range_day = self.df.loc[self.df['TemperatureRange'].idxmin()]
        print('The day with the smallest temperature range is day number ' + str(int(min_range_day.DayNumber)) + ' with a max temperature of ' 
              + str(min_range_day.MaxTemperature)  + 'F' + ' and a min temperature of ' + str(min_range_day.MinTemperature)  + 'F')

    #method which plots a figure displaying the average temperature against Day Number
    def plot_average_temperature(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.df['DayNumber'], self.df['AverageTemperature'], marker='o')

        plt.title('Day Number vs Average Temperature')
        plt.xlabel('Day Number')
        plt.ylabel('Average Temperature')

        plt.show()

# We now create an instance of WeatherData and call the required methods:
data = WeatherData('data/weather.dat')
data.print_daily_temperatures()
print()
data.find_warmest_day()
data.find_coolest_day()
data.find_smallest_range()
data.plot_average_temperature()

