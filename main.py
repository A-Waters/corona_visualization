import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def read_file(fileName):
    """
    purpose: load and fix data into a data frame frome a file \n
    pre: filename/location \n
    return: pandas dataframe : [country][day since 1-21-20 till 49+][data element]
    """
    data = pd.read_csv(fileName) 
    pd.set_option('display.max_rows', None)

    data = data.fillna('0-0-0-0')

    # total infections, ? ,recoveries, deaths
    # [country][day since 1-21-20 till 49+][data element]
    extracted_data = {}

    for label in data.columns[1:]:
        label_data = []
        for i in range(len(data[label])):
            
            day_data = data[label][i].split('-')
            if len(day_data) == 1:
                day_data = [day_data[0], 0, 0, 0]
            elif len(day_data) == 2:
                day_data = [day_data[0], 0, day_data[1], 0]
            elif len(day_data) == 3:
                day_data = [day_data[0], 0, day_data[1], day_data[2]]
            elif len(day_data) != 4:
                print("E: " + str(day_data))

            day_data = list(map(int, day_data))

            label_data.append(day_data)

        extracted_data[label] = label_data


    new_data = pd.DataFrame.from_dict(extracted_data)
    # [country][day since 1-21-20 till 49+][data element]
    return new_data

def generate_plot_data(incoming_data):
    """
    purpose: generates data to be plotted based on given dataframe \n
    pre: pandas dataframe : [country][day since 1-21-20 till 49+][data element] \n
    return: dict : {coutry][data element][day]}
    """

    # incoming_data =  pandas dataframe: [country][day since 1-21-20 till 49+][data element]


    # [country][data Elemement][day]
    # data element = [found], [unknown], [recoveries], [deaths]
    plot_data = {}
    for location in incoming_data.columns:
        location_reacp = [[], [], [], []]
        for day_data in incoming_data[location]:
            for data_type in range(len(day_data)):
                location_reacp[data_type].append(day_data[data_type])

        plot_data[location] = location_reacp

    # [coutry][data element][day]

    return plot_data


def generate_deltas(plot_data):
    """
    purpose: generates change over day baed on given data \n
    pre: dict : {coutry : [data element][days]} \n
    return: dict : {coutry : [data element delta][days]}
    """

    deltas = {}
    for location in plot_data.keys():
        location_deltas = [[],[],[],[]]
        for data_element_index in range(len(plot_data[location])):
            for day_value_index in range(1,len(plot_data[location][data_element_index])):
                location_deltas[data_element_index].append(
                    plot_data[location][data_element_index][day_value_index]
                    -plot_data[location][data_element_index][day_value_index-1]
                    )

        deltas[location] = location_deltas
    
    return deltas



    def show_data(incoming_data, inintal_offset = False):
        """
        purpose: show data \n
        pre: incoming_data : data to show \n
            inintal_offset : start days at first infection \n
        return:  none
        """
        # under constuction
        pass

            
            



if __name__ == "__main__":

    file_name = 'virus.csv'

    # returns pandas data frame
    # [country][day since 1-21-20 till 49+][data element]
    data = read_file(file_name)

    # returns dict array
    # coutry : [data element][days since day since 1-21-20]
    plot_data = generate_plot_data(data)

    # returns dict array
    # coutry : [data element][days since day since 1-21-20]
    delta_data = generate_deltas(plot_data)


    # data elements = total infections, unknown, recoveries, deaths        
    
    print(plot_data.keys())
    
    data1, = plt.plot(plot_data['india'][0])
    data2, = plt.plot(plot_data['beijing'][0])

    data1.set_label("india")
    data2.set_label('beijing')



    plt.title("Corona")
    plt.xlabel("days")
    plt.ylabel("infections")

    plt.legend()
    plt.show()