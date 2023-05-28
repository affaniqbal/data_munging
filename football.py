import pandas as pd
import matplotlib.pyplot as plt

class FootballData:
    def __init__(self, file_path):
        try:
            # Read the .dat file line by line
            lines = []
            with open(file_path, 'r') as file:
                lines = file.readlines()

            # Remove the header from the lines
            data_lines = lines[1:]

            # Remove row 18 from the data
            data_lines.pop(17)

            # Parse the lines using the determined delimiter
            data = []
            for line in data_lines:
                elements = line.split(maxsplit=10)
                elements.pop(0)
                elements.pop(6)
                data.append(elements)

            # Define column headers
            headers = ['Team', 'Players', 'Wins', 'Losses', 'Draws', 'For', 'Against', 'Points']

            # Create a DataFrame from the parsed data with column headers
            self.df = pd.DataFrame(data, columns=headers)

            # Specify the column names to convert and apply pd.numeric() function to selected columns
            columns_to_convert = ['Players', 'Wins', 'Losses', 'Draws', 'For', 'Against', 'Points']
            self.df[columns_to_convert] = self.df[columns_to_convert].apply(pd.to_numeric, errors='coerce')

        except FileNotFoundError:
            print("The file you're trying to open does not exist.")
            raise
        except Exception as e:
            print(f"An error has occurred: {str(e)}")
            raise

    def calculate_for_against_delta(self):
        self.df['ForAgainstDelta'] = abs(self.df['For'] - self.df['Against'])

    def find_lowest_delta_team(self):
        self.calculate_for_against_delta()
        LowestDeltaTeam = self.df.loc[self.df['ForAgainstDelta'].idxmin(), 'Team']
        LowestDeltaFor = self.df.loc[self.df['ForAgainstDelta'].idxmin(), 'For']
        LowestDeltaAgainst = self.df.loc[self.df['ForAgainstDelta'].idxmin(), 'Against']
        print('The team with the smallest difference in For and Against goals is ' + LowestDeltaTeam + ' with ' 
            + str(LowestDeltaFor) + ' goals For and ' + str(LowestDeltaAgainst) + ' goals Against.' )

    def plot_goals(self):
        plt.figure(figsize=(10, 6))
        plt.plot(self.df['Team'], self.df['For'], marker='o', label = 'Goals For')
        plt.plot(self.df['Team'], self.df['Against'], marker='o', label = 'Goals Against')
        plt.plot(self.df['Team'], self.df['ForAgainstDelta'], marker='o', label = 'ForAgainstDelta')

        plt.title('Goals For, Goals Against and Delta between the Two')
        plt.xlabel('Team')
        plt.ylabel('Number of Goals')

        plt.xticks(rotation=90)
        plt.legend()
        plt.show()

# Create an instance of FootballData and call the required methods:

data = FootballData('data/football.dat')
data.find_lowest_delta_team()
data.plot_goals()
