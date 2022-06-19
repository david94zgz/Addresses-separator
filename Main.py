import pandas as pd
import json


# This program takes an address as an input from the user through the terminal. 
# Then, it splits and returns the address as street and house number. 
# Lastly, it save all the information in a CSV file named 'Addresses.csv'


"""
    This are some examples of inputs and outputs from the program

    "Winterallee 3"    -> {"street": "Winterallee", "housenumber": "3"}
    "Musterstrasse 45" -> {"street": "Musterstrasse", "housenumber": "45"}
    "Blaufeldweg 123B" -> {"street": "Blaufeldweg", "housenumber": "123B"}
    "Am Bächle 23" -> {"street": "Am Bächle", "housenumber": "23"}
    "Auf der Vogelwiese 23 b" -> {"street": "Auf der Vogelwiese", "housenumber": "23 b"}
    "4, rue de la revolution" -> {"street": "rue de la revolution", "housenumber": "4"}
    "200 Broadway Av" -> {"street": "Broadway Av", "housenumber": "200"}
    "Calle Aduana, 29" -> {"street": "Calle Aduana", "housenumber": "29"}
    "Calle 39 No 1540" -> {"street": "Calle 39", "housenumber": "No 1540"}
"""


# Initialize a dictionaty to generate or append later to the CSV file
dicctionaryToDB = {
    "address": list(),
    "street": list(),
    "housenumber": list()
}


def save_address(address, street, housenumber):
    """
    Take address data and append it to the initialized dictionary
    """
    dicctionaryToDB["address"].append(address)
    dicctionaryToDB["street"].append(street)
    dicctionaryToDB["housenumber"].append(housenumber)



def address_house_separator(address):
    """
    Takes as an input an address and make all the pertinent transformations to divide the 
    input into street and house number. Then, it retrieves this information in the form of a JSON.

    It also save all that information into the python dictionary 'dicctionaryToDB'
    """
    fil = [x.isnumeric() for x in address.split()]

    if ',' in address:
        lis = [x.strip() for x in address.split(',')]
        housenumber = min(lis, key=len)
        street = max(lis, key=len)

    elif len([i for (i, v) in zip(address.split(), fil) if v]) > 1:
        for x in range(1, len(address)):
            if address[x-1].isnumeric() == True and address[x].isnumeric() == False:
                lis = [address[:x].strip(), address[x:].strip()]
                street = max(lis, key=len)
                housenumber = min(lis, key=len)
                break

    else:
        if address[0].isdigit():
            housenumber = address.split()[0].strip()
            street = ' '.join(address.split()[1:]).strip()

        else:
            for x in range(len(address)):
                if address[x].isnumeric():
                    street = address[:x].strip()
                    housenumber = address[x:].strip()
                    break
    
    save_address(address, street, housenumber)
    return print(json.dumps({"street":street, "housenumber":housenumber}))


# Allowes the user to enter an address that will be use to extract its street and house number
# and to save it.
input_address = input('>> Enter your address: ')
address_house_separator(input_address)


# Try to open "Addresses.csv" and appendes to it the information from the inserted address.
# If it cannot open it, it will create it and append the information from the inserted address.
try:
    df = pd.read_csv("Addresses.csv", index_col="Unnamed: 0", sep=';')
    updatedDf = pd.concat([df, pd.DataFrame(dicctionaryToDB)], ignore_index=True, join="outer")
    updatedDf.to_csv('Addresses.csv', sep=';')

except:
    df = pd.DataFrame(dicctionaryToDB)
    df.to_csv('Addresses.csv', sep=';')
