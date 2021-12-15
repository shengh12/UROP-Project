from tkinter import *
import os
import pandas as pd
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg)
from numpy import log as ln
from PIL import ImageTk, Image
from matplotlib import pyplot as plt
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import tkinter.filedialog
from matplotlib.backends.backend_tkagg import (NavigationToolbar2Tk)
from tkinter import font as tkFont
import math
from tkinter import ttk
from ttkthemes import themed_tk as tk

#Plot takes the compound names and the temperature to make an accurate plot of the delta E graph.
#hello World
def plot(additional_element = False, cathod_name = '', x_cat=0.0, fixed_element = None, analyze = 'None'):
    for widget in frame_2.winfo_children():
        widget.destroy()
    def get_rid_of_white_spaces(string):
        return string.replace(' ', '')

    #try:
    label_status.config(text="plotting...")
    frame_1.update_idletasks()

    #takes the compound names from the user input

    #get rid of any white spaces the user might have inputted into the entry.

    #put everything into lowercase to make it easier, will eventually make the user input just like the
    #file name

    #Rounded the temperature that the user inputted. Because the temperature data of the compunds, anions, and
    #the metals are all with nice integers, just in case if the user decided to put down the temperature
    #as 1000.3, the code rounds this to 1000.

    compound1_name = str(get_rid_of_white_spaces(compound_1_entry.get()).lower())
    compound2_name = str(get_rid_of_white_spaces(compound_2_entry.get()).lower())
    temperature_in_k = int(round(float(get_rid_of_white_spaces(temperature_entry.get()))))

    #Hard coded the anions in with their charges. Their charges are "positive" because we are trying
    #to find the charges of metals so instead of getting a negative charge first, we will just
    #get the postive charge that the metal ions are suppose to have.

    anion_list = ['s', 'f', 'o', 'cl']
    anion_charge = [2, 1, 2, 1]

    #This function just makes the data that the code outputs look nice and easier to find in the folder.
    def rewrite_compound_name_for_file(string):
        new_name = ''
        for i in range(len(string)):
            if i == 0:
                new_name += string[0].upper()
            else:
                new_name += string[i].lower()
        return new_name

    #This function takes the user input and returns the following in this order:
    #[compound file name, charge of metal, generic column name, anion file name, metal file name,
    # the anion name, the coefficient of compound for comparison, and the coefficient of anion for
    # comparison]

    def find_file_name_and_charge(test_string):
        '''
        This function takes the user input and returns the following in this order:
        [compound file name, charge of metal, generic column name, anion file name, metal file name,
        the anion name, the coefficient of compound for comparison, and the coefficient of anion for
        comparison, the metal name]

        '''


        def find_amount_of_metal_and_anions(string):
            '''

            This takes a string, in this case will be the compound name, and returns a list in this
            order [anion name, the amount of metal ions, the amount of anion ions]. So for example
            if the string is 'ag2s', this function will return ['s', 2, 1]
            '''
            return_list = []
            index_of_anion = 0
            index_of_anion_copy = 0
            metals = ''
            anions = ''
            new_string = string.lower()

            #looping backwards through the string

            for i in range(len(new_string) - 1, -1, -1):

                char = new_string[i]

                #right here the code is making an extra check for cl. Because Cl has a length of 2
                #unlike the other anions like S, O which only has a length of 1, the code basically says
                #if you find the letter c, get 2 letters instead of just the 1.

                #We don't have to worry if the metal ion also start with a C because we are looping
                #the string from back to front so the first instance of a 'c' will always be a anion


                if char == 'c':
                    index_of_anion = i
                    index_of_anion_copy = i
                    return_list.append(char + new_string[i + 1])
                    break

                #this comes after the cl loop because if the character in the string is not a c,
                #then it means that it's another anion in the list and the code just finds what
                #anion it is.
                if char in anion_list:
                    index_of_anion = i
                    index_of_anion_copy = i
                    return_list.append(char)
                    break

            #now that the anion and the anion index has been found, we can find the string of the metal
            #just slicing the original comoound string. So if a compound is 'ag2s', the metal string would
            #be 'ag2'.

            metal_string = test_string[0:index_of_anion]

            #looping backwards from the metal string to find how many metal ions there are in the compound

            for i in range(len(metal_string) - 1, -1, -1):
                char = metal_string[i]

                #This if statement just check to see if the first character that we loop
                #from backwards from the string is a letter. If it is, then we know that
                #the metal count is just 1. Otherwise, we just keep adding the number
                #that we find from the back of the metal string to metals and get the amount of
                #metal ions.

                if i == len(metal_string) - 1 and char.isalpha():
                    metals += '1'
                    break
                elif char.isdigit():
                    metals += char
                else:
                    pass

            #The first if statement checks the anion string and just checks to see
            #if the anion count is 1.

            if index_of_anion == len(new_string) - 1:
                anions = '1'
            elif new_string[index_of_anion_copy + 1].isdigit():
                anions += new_string[index_of_anion_copy + 1:]
            else:
                anions += new_string[index_of_anion_copy + 2:]

            #We have to reverse the metal string here because remember, back when we looped through
            #the metal string, we looped through it backwards. So if the metal string is
            #'Ag20Cl20', the metal ion count would come out to be '02' because it's backwards.
            #So we just reverse the string
            return_list.append(int(metals[::-1]))
            if anions == '':
                anions = '1'
            return_list.append(int(anions))
            return return_list

        def find_charge_of_metal(list_1):
            '''
            This function is made specifically for the function find_amount_of_metal_and_anions,
            It will only take a list of items in these order which find_amount_of_metal_and_anions
            returns: [anion name, how many metal ions there are, how many anion ions there are]
            '''

            anion_name = list_1[0]
            amount_of_metal = list_1[1]
            amount_of_anion = list_1[2]

            #get the position of the anion from the anion names list.
            position_of_anion = anion_list.index(anion_name.lower())
            total_charge = amount_of_anion * anion_charge[position_of_anion]
            metal_charge = total_charge / amount_of_metal
            return metal_charge


        #amount_of_materials = [compound file name, charge of metal, generic column name, anion file name, metal file name,
        #the anion name, the coefficient of compound for comparison, and the coefficient of anion for
        #comparison]

        amount_of_meterials = find_amount_of_metal_and_anions(test_string)

        charge_of_metal = find_charge_of_metal(amount_of_meterials)

        def find_file_name(string, list_1):
            '''
            takes in a string and a list that the function find_amount_of_metal_and_anions and
            finds the what the metal is for the file name.
            '''
            metal_name = ''
            index = string.find(list_1[0])
            metal_string = string[0:index]
            for char in metal_string:
                if char.isalpha():
                    metal_name += char
            return metal_name

        def split(word):
            return [char for char in word]

        def captalize_name(string):
            '''
            takes in a string and makes it captalized. If the string's length is more than 1,
            it captalizes the first letter of the name.
            '''
            return_string = ''
            list_of_string = split(string)
            list_of_string[0] = list_of_string[0].upper()
            for i in range(len(list_of_string)):
                return_string += list_of_string[i]
            return return_string

        name_of_metal = captalize_name(find_file_name(test_string, amount_of_meterials))

        name_of_anion = captalize_name(amount_of_meterials[0])

        #This block just takes account of the metal name, the amount of metal ions, the anion
        #name, and the amount of anion ions to make an accurate file name for the compound.

        if amount_of_meterials[1] == 1 and amount_of_meterials[2] == 1:
            data_file_name = name_of_metal + name_of_anion + '_' + 'ss.xlsx'
        elif amount_of_meterials[1] == 1:
            data_file_name = name_of_metal + name_of_anion + str(amount_of_meterials[2]) + '_ss.xlsx'
        elif amount_of_meterials[1] != 1 and amount_of_meterials[2] != 1:
            data_file_name = name_of_metal + str(amount_of_meterials[1]) + name_of_anion + str(
                amount_of_meterials[2]) + '_ss.xlsx'
        else:
            data_file_name = name_of_metal + str(amount_of_meterials[1]) + name_of_anion + '_ss.xlsx'


        #the return list contains these items [data file name, charge of metal, name of metal, the amount of
        # metal ions, the name of the anion, and the amount of anion ions]
        return_list = []
        return_list.append(data_file_name)
        return_list.append(charge_of_metal)
        return_list.append(name_of_metal)
        return_list.append(amount_of_meterials[1])
        return_list.append(name_of_anion)
        return_list.append(amount_of_meterials[2])

        #this block is trying to find the correct fraction for the delta G that we compare later
        #to see who is the N_B or N_A.

        #the coefficient for metal is always 1
        metal_counter = 1

        #The coefficient for compound is going to be the metal counter divided by the amount of metal
        # ions there are.
        fraction_for_compound = metal_counter / return_list[3]

        #The coefficient for anions is just the fraction for the compound / the amount of anion ions, and
        # divided by 2. We will worry about the special case for sulfur later.

        anion_counter = fraction_for_compound * return_list[5] / 2

        #This takes the list like the return list and find the anion file name with excel extension.
        def find_anion_file_name(list_1):

            if len(list_1[4]) == 2:
                name = ''
                list_2 = split(list_1[4])
                list_2[0] = list_2[0].upper()
                for item in list_2:
                    name += item
                return name + '_ss.xlsx'
            else:
                return list_1[4].upper() + '_ss.xlsx'

        #This takes the list like the return list and find the metal file name with the excel extension
        def find_metal_name(list_1):
            return list_1[2] + '_ss.xlsx'

        #This takes the list like return list and returns a generic column name for the compound file
        #so for example, for 'Ag2S', it will return 'a-Ag2S' because thats what the columns are written
        # as.

        def find_compound_name(list_1):

            metal_name = list_1[2]
            metal_count = list_1[3]
            anion_name = list_1[4]
            anion_count = list_1[5]
            if metal_count == 1 and anion_count == 1:
                return 'a-' + metal_name + anion_name
            elif anion_count == 1:
                return 'a-' + metal_name + str(metal_count) + anion_name
            elif metal_count == 1:
                return 'a-' + metal_name + anion_name + str(anion_count)
            else:
                return 'a-' + metal_name + str(metal_count) + anion_name + str(anion_count)


        #the return list 1 returns a list with items in this order: [data file name, charge of
        # metal, the generic compound name for file, the anion file, the metal file, the anion name
        # the coefficient for compound for comparing, the coefficient for anion for comparison, the metal name]
        return_list_1 = []
        return_list_1.append(data_file_name)
        return_list_1.append(charge_of_metal)
        return_list_1.append(find_compound_name(return_list))
        return_list_1.append(find_anion_file_name(return_list))
        return_list_1.append(find_metal_name(return_list))
        return_list_1.append(return_list[4])
        return_list_1.append(fraction_for_compound)
        return_list_1.append(anion_counter)
        return_list_1.append(return_list[2])
        return return_list_1

    try:
        #this just uses the function find file name and get the list of items.
        name_and_charge_compound_1 = find_file_name_and_charge(compound1_name)
        name_and_charge_compound_2 = find_file_name_and_charge(compound2_name)

        #get the anion file paths
        anion_1_file_name = path_of_python + '/Anodespecies_Standardstate/' + name_and_charge_compound_1[3]
        anion_2_file_name = path_of_python + '/Anodespecies_Standardstate/' + name_and_charge_compound_2[3]

        #transforms the excel sheet to lists for each anion
        anion_1_file_list = write_excel_to_list(rewrite_compound_name_for_file('anion_1.txt'), anion_1_file_name)
        anion_2_file_list = write_excel_to_list(rewrite_compound_name_for_file('anion_2.txt'),anion_2_file_name)

        #get the metal file name path
        metal_1_file_name = path_of_python + '/Metal_Standardstate/' + name_and_charge_compound_1[4]
        metal_2_file_name = path_of_python + '/Metal_Standardstate/' + name_and_charge_compound_2[4]

        #transforms the excel sheet to lists for each metal
        metal_1_file_list = write_excel_to_list(rewrite_compound_name_for_file('metal_1_data.txt'), metal_1_file_name)
        metal_2_file_list = write_excel_to_list(rewrite_compound_name_for_file('metal_2_data.txt'), metal_2_file_name)

        #get the compouond file path
        compound_1_file_name = path_of_python + '/Electrolyte_Standardstate/' + name_and_charge_compound_1[0]
        compound_2_file_name = path_of_python + '/Electrolyte_Standardstate/' + name_and_charge_compound_2[0]
        #try:

        #transforms the excel sheets to lists for each compound
        compound_1_file_list = write_excel_to_list(rewrite_compound_name_for_file(compound1_name)+' Data',
                                                 compound_1_file_name)
        compound_2_file_list =  write_excel_to_list(rewrite_compound_name_for_file(compound2_name)+' Data',
                                                  compound_2_file_name)


        #get the liquid column name for the compound.
        compound_1_liquid_position = compound_1_file_list[0].index(name_and_charge_compound_1[2].lower() + '(liq)')
        compound_2_liquid_position = compound_2_file_list[0].index(name_and_charge_compound_2[2].lower() + '(liq)')

        #get the liquid column name for the metal.
        metal_1_liquid_position = metal_1_file_list[0].index('a-' + name_and_charge_compound_1[8].lower()+ '(liq)')
        metal_2_liquid_position = metal_2_file_list[0].index('a-' + name_and_charge_compound_2[8].lower()+'(liq)')

        # except:
        #     os.remove(compound1_name + " Data.txt")
        #     os.remove(compound2_name + " Data.txt")


        def comparable_delta_G(compound_data_list, anion_data_list, metal_data_list, returned_list, anion_name,
                               temperature):


            coef_for_compound = returned_list[6]
            coef_for_anion = returned_list[7]

            #just initialize the g_stables of everything to 0 first.
            anion_g_stable = 0
            metal_g_stable = 0
            compound_g_stable = 0

            for i in range (len(anion_data_list)):
                if anion_data_list[i][0] == temperature:
                    #checks to see if the anion name is 's', if it is, then we check to see if there is 1 in any other
                    # column than liquid. If it is, then we multiply the coefficient of the anion by 2.
                    if anion_name.lower() == 's':
                        index_of_1 = anion_data_list[i].index(1)
                        if index_of_1 == 3 or index_of_1 == 4 or index_of_1 == 5:
                            coef_for_anion = coef_for_anion*2

                    #if the anion is not 's', then we just take the g_stable from the first column
                    anion_g_stable = anion_data_list[i][1]



            for i in range (len(compound_data_list)):
                compound_1_liquid_position = compound_data_list[0].index(returned_list[2].lower()+ '(liq)')
                if compound_data_list[i][0] == temperature:

                    #if the 1 is at the liquid position for the compound, we just return the g stable from column 1.
                    # otherwise we just get the a value from the liquid position and just do g_stable from column 1 -
                    # RTln(a).
                    if compound_data_list[i][compound_1_liquid_position] ==1:
                        compound_g_stable = compound_data_list[i][1]
                    else:
                        compound_g_stable = compound_data_list[i][1] - 8.314*temperature*ln(compound_data_list[i][compound_1_liquid_position])

            for i in range (len(metal_data_list)):
                if metal_data_list[i][0] == temperature:

                    #the metal g stable is just the g stable from column 1
                    metal_g_stable = metal_data_list[i][1]


            returned_delta_g = coef_for_compound*compound_g_stable - coef_for_anion*anion_g_stable - metal_g_stable



            return returned_delta_g, coef_for_compound


        comparable_delta_G_1 = comparable_delta_G(compound_1_file_list, anion_1_file_list, metal_1_file_list,
                                                   name_and_charge_compound_1, name_and_charge_compound_1[5],
                                                   temperature_in_k)

        comparable_delta_G_2 = comparable_delta_G(compound_2_file_list, anion_2_file_list, metal_2_file_list,
                                                   name_and_charge_compound_2, name_and_charge_compound_2[5],
                                                   temperature_in_k)

        delta_g_for_compare_1 = comparable_delta_G_1[0]

        delta_g_for_compare_2 = comparable_delta_G_2[0]

        coef_1 = comparable_delta_G_1[1]

        coef_2 = comparable_delta_G_2[1]



        def compare_delta_g(charge_1, charge_2, delta_g_1, delta_g_2, metal_1, metal_2, coef_1, coef_2):
            na_nb_list = []
            compare_1 = float(delta_g_1/charge_1)
            compare_2 = float(delta_g_2/charge_2)
            if compare_1 < compare_2:
                na_nb_list.append(charge_1)
                na_nb_list.append(charge_2)
                na_nb_list.append(metal_1)
                na_nb_list.append(metal_2)
                na_nb_list.append(compare_1)
                na_nb_list.append(compare_2)
                na_nb_list.append(coef_1)
                na_nb_list.append(coef_2)
            else:
                na_nb_list.append(charge_2)
                na_nb_list.append(charge_1)
                na_nb_list.append(metal_2)
                na_nb_list.append(metal_1)
                na_nb_list.append(compare_2)
                na_nb_list.append(compare_1)
                na_nb_list.append(coef_2)
                na_nb_list.append(coef_1)

            return na_nb_list


        #the electron_list returns these items [N_b, N_a, metal name for G_b, metal name for G_a,  G_b/n_b, G_a/n_a,
        # coefficient for compound b, coefficient for compound a]
        electron_list = compare_delta_g(name_and_charge_compound_1[1], name_and_charge_compound_2[1],
                                        delta_g_for_compare_1, delta_g_for_compare_2, name_and_charge_compound_1[8],
                                        name_and_charge_compound_2[8], coef_1, coef_2)



        n_a = electron_list[1]
        n_b = electron_list[0]
        metal_a = electron_list[3]
        metal_b = electron_list[2]

        position_of_stable_G = 1

        #making the gui

        frame_2_1 = ttk.Frame(frame_2)
        frame_2_1.pack()

        frame_2_2 = ttk.Frame(frame_2)
        frame_2_2.pack()

        frame_2_3 = ttk.Frame(frame_2)
        frame_2_3.pack()

        frame_2_4 = ttk.Frame(frame_2)
        frame_2_4.pack()

        if additional_element:
            filename = askopenfilename()
            real_file_name = filename
        else:
            # get the file name of gamma data and turn it into a list.
            gamma_file_name = path_of_python + '/Cathode_mixing_activity/' + str(temperature_in_k) + metal_a + metal_b + '.xlsx'
            gamma_file_name_1 = path_of_python + '/Cathode_mixing_activity/' + str(temperature_in_k) + metal_b + metal_a + '.xlsx'
            #
            # # checks to see which one of the file list names appears in path, if one does not exist, then pick the other one
            if os.path.isfile(gamma_file_name_1):
                real_file_name = gamma_file_name_1
            else:
                real_file_name = gamma_file_name

        gamma_list = write_excel_to_list('gamma data.txt', real_file_name)

        def get_delta_G_a_or_b(element):
            delta_G_list = 0


            #finding if the which colume the liquid is in and doing the corresponding calculations
            if 'liqu' in gamma_list[0][1] and 'liqu' in gamma_list[0][2]:
                if element in name_and_charge_compound_1:

                    for i in range(1, len(metal_1_file_list)):
                        if metal_1_file_list[i][0] == temperature_in_k:
                            g_stable = metal_1_file_list[i][position_of_stable_G]
                            a_liquid = metal_1_file_list[i][metal_1_liquid_position]
                            delta_g = float(g_stable) - (8.314 * temperature_in_k) * ln(a_liquid)
                            delta_G_list = delta_g - float(g_stable)
                else:
                    for i in range(1, len(metal_2_file_list)):
                        if metal_2_file_list[i][0] == temperature_in_k:
                            g_stable = metal_2_file_list[i][position_of_stable_G]
                            a_liquid = metal_2_file_list[i][metal_2_liquid_position]

                            delta_g = float(g_stable) - (8.314 * temperature_in_k) * ln(a_liquid)
                            delta_G_list = delta_g - float(g_stable)
            return delta_G_list

        delta_G_a = get_delta_G_a_or_b(electron_list[3])
        delta_G_b = get_delta_G_a_or_b(electron_list[2])

        #Checked all good, should be behaving the way that its suppose to

        y = []
        x=[]
        x_metal_a = []

        #below are lists that are needed for exporting data
        delta_E_export = []
        rho_export = []
        conc_export = []
        activity_export = []
        aox_export = []
        z_export=[]
        ohm_export=[]
        compound_a_export = []

        #just finding the correct column that the metals are in the data excel sheet
        metal_a_position = 0
        metal_b_position = 0
        for i in range (3):
            if metal_a.lower() in gamma_list[0][i]:
                metal_a_position = i
            elif metal_b.lower() in gamma_list[0][i]:
                metal_b_position = i

        x_a_position = -1
        index_of_0 = 0


        for i in range (1, 3):
            if gamma_list[1][i] == 0:
                index_of_0 = i

        if index_of_0 == metal_a_position:
            x_a_position = 0

        y_1 = []

        axes_label_a = metal_a
        axes_label_b = metal_b

        x_counter= 0.001

        #looping through the numbers 0.001 to 0.999 and finding the correct alpha, gamma a, and gamma b data for each.
        while (x_counter<= 0.999):
            y_value = 0.0
            if not additional_element:
                for i in range (1, len(gamma_list)):
                    if gamma_list[i][0] == x_counter:

                        # checks to see if the alpha is corresponding to the N_a or N_b
                        if x_a_position != -1:
                            #inside of this loop, the alpha is related to N_a
                            gamma_b = float (gamma_list[i][metal_b_position]) / (1- x_counter)
                            gamma_a = float (gamma_list[i][metal_a_position]) / (x_counter)
                            x_value = (1-x_counter)
                            x.append(x_value)
                            y_value = (-n_a * delta_G_b + n_b * delta_G_a + n_b * (8.314 * temperature_in_k) * ln(
                                (1 - x_value - x_cat) * gamma_a) - (n_a*
                                               8.314 * temperature_in_k) * ln(x_value * gamma_b)) / (96485 * n_a * n_b)
                        else:
                            # inside of this loop, the alpha is related to N_b
                            gamma_b = float(gamma_list[i][metal_b_position]) / (x_counter)
                            gamma_a = float(gamma_list[i][metal_a_position]) / (1-x_counter)
                            x.append(x_counter)
                            y_value = (-n_a * delta_G_b + n_b * delta_G_a + n_b * (8.314 * temperature_in_k) * ln(
                                (1 - x_counter - x_cat) * gamma_a) - (n_a*
                                               8.314 * temperature_in_k) * ln(x_counter * gamma_b)) / (96485 * n_a * n_b)
            else:
                if x_cat == 0:
                    for i in range(1, len(gamma_list)):
                        if gamma_list[i][0] == x_counter:

                            # checks to see if the alpha is corresponding to the N_a or N_b
                            if x_a_position != -1:
                                # inside of this loop, the alpha is related to N_a
                                gamma_b = float(gamma_list[i][metal_b_position]) / (1 - x_counter)
                                gamma_a = float(gamma_list[i][metal_a_position]) / (x_counter)
                                x_value = (1 - x_counter)
                                x.append(x_value)
                                y_value = (-n_a * delta_G_b + n_b * delta_G_a + n_b * (8.314 * temperature_in_k) * ln(
                                    (1 - x_value - x_cat) * gamma_a) - (n_a *
                                                                      8.314 * temperature_in_k) * ln(x_value * gamma_b)) / (
                                                      96485 * n_a * n_b)
                            else:
                                # inside of this loop, the alpha is related to N_b
                                gamma_b = float(gamma_list[i][metal_b_position]) / (x_counter)
                                gamma_a = float(gamma_list[i][metal_a_position]) / (1 - x_counter)
                                x.append(x_counter)
                                y_value = (-n_a * delta_G_b + n_b * delta_G_a + n_b * (8.314 * temperature_in_k) * ln(
                                    (1 - x_counter - x_cat) * gamma_a) - (n_a *
                                                                        8.314 * temperature_in_k) * ln(
                                    x_counter * gamma_b)) / (96485 * n_a * n_b)
                else:

                    #only added to metal A
                    if fixed_element == metal_a.lower():
                        axes_label_a = metal_a + '+' + cathod_name
                        for i in range(1, len(gamma_list)):
                            if gamma_list[i][0] == x_counter:

                                #checks to see if the alpha is corresponding to the N_a or N_b
                                if x_a_position != -1:

                                    # inside of this loop, the alpha is related to N_a
                                    x_a = x_counter * (1-x_cat)
                                    x_b = 1-x_counter
                                    x_c = float((x_cat*x_a)/(1-x_cat))

                                    gamma_b = float(gamma_list[i][metal_b_position])/(x_b)
                                    gamma_a = float(gamma_list[i][metal_a_position])/(x_a)

                                    x_value = (1 - x_counter)
                                    x.append(x_value)
                                    y_value = (-n_a * delta_G_b + n_b * delta_G_a + n_b * (8.314 * temperature_in_k) * ln(
                                        (1 - x_value - x_c) * gamma_a) - (n_a * 8.314 * temperature_in_k) * ln(x_value * gamma_b)) / (96485 * n_a * n_b)
                                else:

                                    # inside of this loop, the alpha is related to N_b

                                    x_a = (1-x_counter)*(1-x_cat)
                                    x_b = x_counter
                                    x_c = float(x_cat*x_a)/(1-x_cat)

                                    gamma_b = float(gamma_list[i][metal_b_position])/(x_b)
                                    gamma_a = float(gamma_list[i][metal_a_position])/(x_a)

                                    x.append(x_counter)
                                    y_value = (-n_a * delta_G_b + n_b * delta_G_a + n_b * (8.314 * temperature_in_k) * ln(
                                        (1 - x_counter - x_c) * gamma_a) - (n_a *
                                                                            8.314 * temperature_in_k) * ln(
                                        x_counter * gamma_b)) / (96485 * n_a * n_b)


                    #only added to metal B
                    elif fixed_element == metal_b.lower():
                        axes_label_b = metal_b + '+' + cathod_name
                        for i in range(1, len(gamma_list)):
                            if gamma_list[i][0] == x_counter:

                                #checks to see if the alpha is corresponding to the N_a or N_b
                                if x_a_position != -1:

                                    # inside of this loop, the alpha is related to N_a
                                    x_a = x_counter
                                    x_b = (1-x_counter)*(1-x_cat)
                                    x_c = float((x_cat * x_b) / (1 - x_cat))

                                    gamma_b = float(gamma_list[i][metal_b_position]) / (x_b)
                                    gamma_a = float(gamma_list[i][metal_a_position]) / (x_a)

                                    x_value = (1 - x_counter)
                                    x.append(x_value)
                                    y_value = (-n_a * delta_G_b + n_b * delta_G_a + n_b * (8.314 * temperature_in_k) * ln(
                                        (1 - x_value - x_c) * gamma_a) - (n_a * 8.314 * temperature_in_k) * ln(
                                        x_value * gamma_b)) / (96485 * n_a * n_b)
                                else:

                                    # inside of this loop, the alpha is related to N_b

                                    x_a = (1-x_counter)
                                    x_b = x_counter*(1-x_cat)
                                    x_c = float(x_cat * x_b) / (1 - x_cat)

                                    gamma_b = float(gamma_list[i][metal_b_position]) / (x_b)
                                    gamma_a = float(gamma_list[i][metal_a_position]) / (x_a)

                                    x.append(x_counter)
                                    y_value = (-n_a * delta_G_b + n_b * delta_G_a + n_b * (8.314 * temperature_in_k) * ln(
                                        (1 - x_counter - x_c) * gamma_a) - (n_a *
                                                                            8.314 * temperature_in_k) * ln(
                                        x_counter * gamma_b)) / (96485 * n_a * n_b)
                    else:
                        #Not added to any metal
                        for i in range(1, len(gamma_list)):
                            if gamma_list[i][0] == x_counter:

                                #checks to see if the alpha is corresponding to the N_a or N_b
                                if x_a_position != -1:

                                    # inside of this loop, the alpha is related to N_a
                                    x_a = x_counter*(1-x_counter)
                                    x_b = (1-x_counter)*(1-x_cat)
                                    x_c = float(x_cat)

                                    gamma_b = float(gamma_list[i][metal_b_position]) / (x_b)
                                    gamma_a = float(gamma_list[i][metal_a_position]) / (x_a)

                                    x_value = (1 - x_counter)
                                    x.append(x_value)
                                    y_value = (-n_a * delta_G_b + n_b * delta_G_a + n_b * (8.314 * temperature_in_k) * ln(
                                        (1 - x_value - x_c) * gamma_a) - (n_a *
                                                                          8.314 * temperature_in_k) * ln(
                                        x_value * gamma_b)) / (
                                                      96485 * n_a * n_b)
                                else:

                                    # inside of this loop, the alpha is related to N_b

                                    x_a = x_counter*(1-x_cat)
                                    x_b = (1-x_counter)
                                    x_c = float(x_cat)

                                    gamma_b = float(gamma_list[i][metal_b_position]) / (x_b)
                                    gamma_a = float(gamma_list[i][metal_a_position]) / (x_a)

                                    x.append(x_counter)
                                    y_value = (-n_a * delta_G_b + n_b * delta_G_a + n_b * (8.314 * temperature_in_k) * ln(
                                        (1 - x_counter - x_c) * gamma_a) - (n_a *
                                                                            8.314 * temperature_in_k) * ln(
                                        x_counter * gamma_b)) / (96485 * n_a * n_b)
            y.append(round(y_value,3))


            x_counter  = round((x_counter + 0.001), 3)


        for i in range (len(x)):
            x_metal_a.append(1-x[i])

        #getting the mid point value for the mid line
        index_of_mid = x.index(0.5)
        mid_y_value = y[index_of_mid]

        for i in range (len(x)):
            y_1.append(mid_y_value)

        #plot the graph using x, y, and mid y data


        fig = Figure(figsize=(6, 6))
        a = fig.add_subplot(111)
        params = {'mathtext.default': 'regular',  'font.size'   : 10}
        plt.rcParams.update(params)

        #set the max y value and the min y value of the graph
        y_max = round (mid_y_value + 0.6, 1)
        y_min = -(y_max)
        a.set_ylim([y_min, y_max])

        #set the max x value and min x value of the graph
        a.set_xlim([0.001, 0.999])


        #plot the x and y points
        a.plot(x,y, 'k', linewidth = 5)
        a.plot(x, y_1, 'k')

        plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)

        #a.set_title("Graph of -ΔEb vs Concentration", fontsize=14)
        a.set_ylabel("$E_{" + metal_a + "}- E_{" + metal_b + "}(V)$", fontsize=14)

        conc_str = '                                  $x_{' + metal_b + '}$                                 '


        a.set_xlabel(axes_label_a + conc_str + axes_label_b,
                     fontsize=14)

        canvas = FigureCanvasTkAgg(fig, master=frame_2_2)
        canvas.get_tk_widget().pack()
        tool_bar = NavigationToolbar2Tk(canvas, frame_2_2)
        tool_bar.update()

        def takeClosest(num, collection):
            return min(collection, key=lambda x: abs(x - num))

        SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")
        SUP = str.maketrans("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹")

        def change_compound_name(compound):
            # returns the compound name written in the proper way. So orginally it's 'fes', after using this function
            # the name would become 'FeS'.

            anions = 'sfocl'

            compound_lower = compound.lower()
            index_of_anion = 0
            for i in range(len(compound) - 1, -1, -1):
                if compound_lower[i] == 'l':
                    if compound_lower[i - 1] == 'c':
                        index_of_anion = i - 1
                        break
                elif compound_lower[i] in anions:
                    index_of_anion = i
                    break

            anion = compound[index_of_anion:]
            metal = compound[0:index_of_anion]

            def count_ions(string):
                count = ''
                for i in range(len(string) - 1, -1, -1):
                    if string[i].isdigit():
                        count += string[i]

                if count == '':
                    return 0
                else:
                    return int(count[::-1])

            def get_name(string):
                name = []
                for i in range(len(string)):
                    if string[i].isalpha():
                        name.append(string[i])

                name[0] = name[0].upper()
                return_name = ''.join(name)

                return return_name

            metal_count = count_ions(metal)
            anion_count = count_ions(anion)

            metal_name = get_name(metal)
            anion_name = get_name(anion)

            if metal_count == 0 and anion_count == 0:
                compound_name = metal_name + anion_name
            elif metal_count == 0:
                compound_name = metal_name + anion_name + str(anion_count)
            elif anion_count == 0:
                compound_name = metal_name + str(metal_count) + anion_name
            else:
                compound_name = metal_name + str(metal_count) + anion_name + str(anion_count)

            return compound_name.translate(SUB), metal_name

        new_compound_name_1 = change_compound_name(compound1_name)[0]
        new_compound_name_2 = change_compound_name(compound2_name)[0]

        if metal_a in new_compound_name_1:
            compound_a = new_compound_name_1
            compound_b = new_compound_name_2
        else:
            compound_a = new_compound_name_2
            compound_b = new_compound_name_1

        if analyze == 'Analyze Experiment Data':

            # just making the frames and gui
            A_metal_label = ttk.Label(frame_2_1, text=str(metal_a) + ' (Mole Fraction)', font=('Helvetica', 14))
            A_metal_label.grid(row=0, column=0)
            A_metal_entry = ttk.Entry(frame_2_1, font=('Helvetica', 14))
            A_metal_entry.grid(row=0, column=1)

            if metal_a.lower() in compound1_name:
                compound_name = compound1_name
                compound_b_name = compound2_name
            else:
                compound_name = compound2_name
                compound_b_name = compound1_name

            A_compound_label = ttk.Label(frame_2_1, text=change_compound_name(compound_name)[0] + ' (Mole Fraction)',
                                                                                          font=('Helvetica', 14))
            A_compound_label.grid(row=1, column=0)
            A_compound_entry = ttk.Entry(frame_2_1, font=('Helvetica', 14))
            A_compound_entry.grid(row=1, column=1)

            plot_button = ttk.Button(frame_2_1, text='Plot Point', width=9, command=lambda:
            command_button())
            plot_button.grid(row=2, column=1)

            remove_button = ttk.Button(frame_2_1, text="Remove all Points", width=9, command=lambda: remove_scatter())
            remove_button.grid(row=2, column=2)

            def command_button():

                #get the B_metal and B-compound value

                A_metal = float(A_metal_entry.get())
                A_comp = float(A_compound_entry.get())

                compound_a_export.append(A_comp)

                B_metal = 1 - A_metal
                B_comp = 1 - A_comp
                #get the closest x value that we have already calculated and its corresponding y value.
                x_coord = takeClosest(B_metal, x)
                x_index = x.index(x_coord)
                delta_E = y[x_index]

                nox_b = electron_list[6]
                nox_a = electron_list[7]
                E_a = electron_list[5] / 96485
                E_b = electron_list[4] / 96485
                N_b = electron_list[0]
                N_a = electron_list[1]
                T = temperature_in_k
                F = 96485
                R = 8.314

                A_comp_exp = (N_b*nox_a)/(N_a*nox_b)

                e_exp = (E_a-E_b-delta_E)*N_b*F/(nox_b*R*T)

                a_bcomp = A_comp**A_comp_exp * math.exp(e_exp)

                rho_comp = a_bcomp/B_comp

                label_x = ttk.Label(frame_2_3, text='Concentration Value: ' + str(x_coord) + ', ΔE: ' + str(round(delta_E,2))
                                                    + ', a_'+compound_b_name + ': ' + str(round(a_bcomp,2)) + ', '
                                                                                                     'ρ_' + compound_b_name + ':' + str(round(rho_comp,2)))
                label_x.pack()

                #plots the point
                plot_point(B_metal, delta_E)

                conc_export.append(1-A_metal)
                delta_E_export.append(delta_E)
                activity_export.append(a_bcomp)
                rho_export.append(rho_comp)

        #plots the big red circle on the graph
        list_of_points = []
        def plot_point(x, y):
            point = a.scatter(x, y, color="none", edgecolor="red", s=250, linewidths=3)
            canvas.draw()
            list_of_points.append(point)


        def remove_scatter():
            for item in list_of_points:
                item.remove()
            canvas.draw()

            del list_of_points[:]

        if analyze == 'Use Solution model (Standard State)':

            #electron_list[4] and electron_list[5] is the G_a/n_a value, then we divide it by the Faraday constant
            E_a = electron_list[5]/96485
            E_b = electron_list[4]/96485

            delta_E = E_a-E_b

            #get the closest y value that we have found and then find the corresponding x value.
            y_value = takeClosest(delta_E, y)
            y_index = y.index(y_value)
            x_coord = x[y_index]
            label_x = ttk.Label(frame_2_3, text='Concentration Value: ' + str(x_coord) + ' ΔE: ' + str(y_value))
            label_x.pack()
            plot_point(x_coord, delta_E)

            conc_export.append(x_coord)
            delta_E_export.append(y_value)


        elif analyze == 'Use Solution model (Ideal Solution)':

            #just making the frames and gui

            nox_b = electron_list[6]
            nox_a = electron_list[7]
            E_a = electron_list[5] / 96485
            E_b = electron_list[4] / 96485
            N_b = electron_list[0]
            N_a = electron_list[1]

            if metal_a.lower() in compound1_name:
                compound_name = compound1_name
            else:
                compound_name = compound2_name

            a_label = ttk.Label(frame_2_1, text=change_compound_name(compound_name)[0] + '(Mole Fraction): ',
                              font=('Helvetica',14))
            a_label.grid(row=0, column=0)

            a_entry = ttk.Entry(frame_2_1, font=('Helvetica', 14))
            a_entry.grid(row=0, column=1)

            plot_button = ttk.Button(frame_2_1, text = 'Plot Point', command= lambda:command())
            plot_button.grid(row=1)

            remove_button = ttk.Button(frame_2_1, text="Remove all Points", width=9, command=lambda: remove_scatter())
            remove_button.grid(row=2, column=2)

            # set all the variables to its value
            R = 8.314
            F = 96485
            T = temperature_in_k

            def command():
                a_aox = float(a_entry.get())
                a_box = 1-a_aox

                compound_a_export.append(a_aox)
                delta_E = E_a - (R*T/(N_a*F))*ln(1/((a_aox)**(nox_a))) - (E_b - R*T/(N_b*F)*ln(1/((a_box)**(nox_b))))
                # get the closest y value that we have found and then find the corresponding x value.
                y_value = takeClosest(delta_E, y)
                y_index = y.index(y_value)
                x_coord = x[y_index]
                label_x = ttk.Label(frame_2_3, text='Concentration Value: ' + str(x_coord) + ' ΔE: ' + str(delta_E))
                label_x.pack()
                plot_point(x_coord, delta_E)

                conc_export.append(x_coord)
                delta_E_export.append(delta_E)
                aox_export.append(a_aox)


        elif analyze == 'Use Solution model (Regular solution)':

            #just making the frames and gui

            if metal_a.lower() in compound1_name:
                compound_name = compound1_name
            else:
                compound_name = compound2_name

            a_label = ttk.Label(frame_2_1, text=change_compound_name(compound_name)[0] + '(Mole Fraction):',
                            font=('Helvetica', 14))
            a_label.grid(row=0, column=0)

            a_entry = ttk.Entry(frame_2_1, font=('Helvetica', 14))
            a_entry.grid(row=0, column=1)

            omega_label = ttk.Label(frame_2_1, text = 'ω:', font=('Helvetica', 14))
            omega_label.grid(row=1, column=0)

            omega_entry = ttk.Entry(frame_2_1, font=('Helvetica', 14))
            omega_entry.grid(row=1, column=1)

            z_label = ttk.Label(frame_2_1, text= 'z:', font=('Helvetica', 14))
            z_label.grid(row=2, column=0)

            z_entry = ttk.Entry(frame_2_1, font=('Helvetica', 14))
            z_entry.grid(row=2, column=1)

            plot_button = ttk.Button(frame_2_1, text="Plot Point", command = lambda: plot_command())
            plot_button.grid(row=3)

            remove_button = ttk.Button(frame_2_1, text="Remove all Points", width=9, command=lambda: remove_scatter())
            remove_button.grid(row=2, column=2)

            #set all the variables to its value
            R = 8.314
            F = 96485
            T = temperature_in_k

            nox_b = electron_list[6]
            nox_a = electron_list[7]
            E_a = electron_list[5] / 96485
            E_b = electron_list[4] / 96485
            N_b = electron_list[0]
            N_a = electron_list[1]

            def plot_command():
                z = float(z_entry.get())
                omega = float(omega_entry.get())
                x_aox = float(a_entry.get())

                compound_a_export.append(x_aox)

                a_aox = x_aox * math.exp((z*omega*(1-x_aox)**2)/(R*T))
                a_box = (1-x_aox) * math.exp((z*omega*(x_aox)**2)/(R*T))

                delta_E = E_a - (R * T / (N_a * F)) * ln(1 / ((a_aox) ** (nox_a))) - (
                            E_b - R * T / (N_b * F) * ln(1 / ((a_box) ** (nox_b))))

                # get the closest y value that we have found and then find the corresponding x value.
                y_value = takeClosest(delta_E, y)
                y_index = y.index(y_value)
                x_coord = x[y_index]
                label_x = ttk.Label(frame_2_3, text='Concentration Value: ' + str(x_coord) + ' ΔE: ' + str(delta_E))
                label_x.pack()
                plot_point(x_coord, delta_E)

                conc_export.append(x_coord)
                delta_E_export.append(delta_E)
                z_export.append(z)
                ohm_export.append(omega)


        canvas.draw()
        label_status.config(text='Done!')
        os.remove(compound1_name + " Data.txt")
        os.remove(compound2_name + " Data.txt")

        #this is the export button section.
        export_button = ttk.Button(frame_2_4, width=10,text = 'Export Data', command = lambda:
        ask_for_file_name())
        export_button.pack()

        #ask what name the user wants to save the file as
        def ask_for_file_name():
            file_name = tkinter.filedialog.asksaveasfilename(confirmoverwrite = False)
            export(file_name)

        #export the x_b values and the delta E values into excel format.
        def export(name):

            column_1 = 'Conc of ' + metal_a
            column_2 = 'Conc of ' + metal_b
            column_3 = 'ΔE'
            column_4 = "Analyzed ΔE"
            column_5 = 'Activity of Comp.' + compound_b
            column_10 = 'ρ of ' + compound_b
            column_6 = 'z'
            column_7 = 'ω'
            column_8 = 'Conc. of ' + compound_b
            column_9 = 'Conc. of ' + compound_a
            column_11 = 'Analyzed Conc. of ' + metal_b

            conc_compound_b = []
            for i in range(len(compound_a_export)):
                conc_compound_b.append(1-compound_a_export[i])

            if len(z_export) == 0 and len(ohm_export) == 0:
                df = {column_1: x_metal_a, column_2: x, column_3: y, column_11: conc_export,column_8:conc_compound_b ,column_9:
                compound_a_export,
                      column_4:delta_E_export,column_5: activity_export, column_10: rho_export}
            else:
                df = {column_1:x_metal_a,column_2: x, column_3: y, column_11: conc_export, column_8:conc_compound_b ,column_9:compound_a_export ,
                      column_4:
                delta_E_export,column_5: activity_export, column_10: rho_export,column_6: z_export, column_7: ohm_export}


            a = pd.DataFrame.from_dict(df, orient='index')
            a = a.transpose()

            a.to_excel( name + '.xlsx', header=True, index=False)
    except:
        messagebox.showinfo(title='Error', message='User Input Error (check your input and your data excel sheets)')


    #clears up some files that the user does not have to use
    direct_path_name  = os.path.dirname(os.path.abspath(__file__))
    folder = os.listdir(direct_path_name)
    for item in folder:
        if item.endswith(".txt"):
            os.remove(os.path.join(direct_path_name, item))

#initialize the window for gui
window = tk.ThemedTk()
window.get_themes()
window.set_theme('breeze')
window.title('Electrochemical Synthesis Diagram Calculator')
window.geometry('1280x900')

#making the pop up message box that confirms if the user wanted to quit the application.
def on_closing():
    if messagebox.askokcancel("Quit", "Quit the Application?"):
        window.destroy()
window.protocol("WM_DELETE_WINDOW", on_closing)

#making frames for gui
frame_1 = ttk.Frame(window)
frame_1.grid(row=0, column=0)
frame_2 = ttk.Frame(window)
frame_2.grid(row=0, column=1)
frame_3 = ttk.Frame(window)
frame_3.grid(row=0, column=2)
frame_4 = ttk.Frame(window)
frame_4.grid(row=1, column=0)

production_label = ttk.Label(frame_4, text="A Sheng Huang. Production", font=('Helvetica', 7))
production_label.grid(row=1, column=0)

supervisor_label = ttk.Label(frame_4, text="Methods and Equations developed by Mary Elizabeth Wagner",
                          font=('Helvetica',7))
supervisor_label.grid(row=0, column=0)

#making the image for gui
img = ImageTk.PhotoImage(Image.open("MIT LOGO.png"))
mit_label = ttk.Label(frame_1, image = img)
mit_label.grid(row=0)

#making user entry and label for compound 1
compound_1_label = ttk.Label(frame_1, text='Compound 1:', font=('Helvetica', 14))
compound_1_label.grid(row=1, column=0)
compound_1_entry = ttk.Entry(frame_1, width=10, font=('Helvetica', 14))
compound_1_entry.grid(row=1, column=1)

#making user entry and label for compound 2
compound_2_label = ttk.Label(frame_1, text='Compound 2:', font=('Helvetica', 14))
compound_2_label.grid(row=2, column=0)
compound_2_entry = ttk.Entry(frame_1, width=10, font=('Helvetica', 14))
compound_2_entry.grid(row=2, column=1)

#making user entry and label for temperature
temperature_label = ttk.Label(frame_1, text='Temperature (K):', font=('Helvetica', 14))
temperature_label.grid(row=5, column=0)
temperature_entry = ttk.Entry(frame_1, width=10, font=('Helvetica', 14))
temperature_entry.grid(row=5, column=1)

additional_element_label = ttk.Label(frame_1, text="Additional element?", font=('Helvetica', 14))
additional_element_label.grid(row=6, column=0)


def no_command():
    plot()

def yes_command(analyze = 'None'):
    new_window = tk.ThemedTk()
    new_window.get_themes()
    new_window.set_theme('arc')
    new_window.title('With Alloy')
    anion = 'fsocl'

    def find_metal_name(string):
        '''
        returns the metal name inside of the user input. So for example, 'Pr2O3" would return 'Pr'
        '''
        metal = ''
        index = 0
        new_string = string.lower()
        for i in range(len(new_string) - 1, -1, -1):
            char = new_string[i]

            if char == 'l' and new_string[i - 1] == 'c':
                index = i - 1
                break
            if char in anion:
                index = i
                break

        metal_string = new_string[0:index]
        for i in range(len(metal_string) - 1, -1, -1):
            char = metal_string[i]
            if char.isdigit() == False:
                metal += char

        list_1 = []
        for char in metal[::-1]:
            list_1.append(char)

        list_1[0] = list_1[0].upper()

        metal_name = ''

        for item in list_1:
            metal_name += item
        return metal_name

    def get_rid_of_white_spaces(string):
        return string.replace(' ', '')


    #making the frames and the gui
    compound1_name = str(get_rid_of_white_spaces(compound_1_entry.get()).lower())
    compound2_name = str(get_rid_of_white_spaces(compound_2_entry.get()).lower())

    metal_1_name = find_metal_name(compound1_name)
    metal_2_name = find_metal_name(compound2_name)

    new_frame = ttk.Frame(new_window)
    new_frame.pack(expand=True)

    new_frame_1 = ttk.Frame(new_window)
    new_frame_1.pack(expand=True)

    alloy_name_label = ttk.Label(new_frame, text="What is your cathode alloy: ", font=('Helvetica',14))
    alloy_name_label.grid(row=0, column=0)
    alloy_entry = ttk.Entry(new_frame, font=('Helvetica', 14))
    alloy_entry.grid(row=0, column=1)

    x_cathod_label = ttk.Label(new_frame, text="Mole fraction of additional species:",
                           font=('Helvetica',
                                                                                                               14))
    x_cathod_label.grid(row=1, column=0)
    x_cathod_entry = ttk.Entry(new_frame, font=('Helvetica',14))
    x_cathod_entry.grid(row=1, column=1)


    fixed_metal_label = ttk.Label(new_frame, text="Concentration fixed along pseudobinary with: ", font=('Helvetica',14))
    fixed_metal_label.grid(row=2, column=0)

    metal_1_button= ttk.Button(new_frame_1, text=metal_1_name, width=9, command= lambda:
    metal_1_command())


    metal_1_button.grid(row=0, column=0)

    metal_2_button = ttk.Button(new_frame_1, text=metal_2_name, width=9, command=lambda:
    metal_2_command())
    metal_2_button.grid(row=0, column=1)

    no_metal_button = ttk.Button(new_frame_1, text="Neither", width=9, command= lambda :
    no_metal_command())

    no_metal_button.grid(row=0, column=2)


    #plots the data and destroy the window so that the user don't have to manually close the window
    def metal_1_command():
        if analyze == '':
            plot(additional_element=True, cathod_name=str(get_rid_of_white_spaces((alloy_entry.get()).lower())),
                x_cat=float(get_rid_of_white_spaces(x_cathod_entry.get())), fixed_element=metal_1_name.lower())
            new_window.destroy()
            window.after(1, lambda: window.focus_force())
        else:
            plot(additional_element=True, cathod_name=str(get_rid_of_white_spaces((alloy_entry.get()).lower())),
                 x_cat=float(get_rid_of_white_spaces(x_cathod_entry.get())), fixed_element=metal_1_name.lower(),
                 analyze= analyze)
            new_window.destroy()
            window.after(1, lambda: window.focus_force())

    def metal_2_command():
        if analyze == '':
            plot(additional_element=True, cathod_name=str(get_rid_of_white_spaces((alloy_entry.get()).lower())),
                 x_cat=float(get_rid_of_white_spaces(x_cathod_entry.get())), fixed_element=metal_2_name.lower())
            new_window.destroy()
            window.after(1, lambda: window.focus_force())
        else:
            plot(additional_element=True, cathod_name=str(get_rid_of_white_spaces((alloy_entry.get()).lower())),
                 x_cat=float(get_rid_of_white_spaces(x_cathod_entry.get())), fixed_element=metal_2_name.lower(),
                 analyze= analyze)
            new_window.destroy()
            window.after(1, lambda: window.focus_force())

    def no_metal_command():
        if analyze == '':
            plot(additional_element=True, cathod_name=str(get_rid_of_white_spaces((alloy_entry.get()).lower())),
                x_cat=float(get_rid_of_white_spaces(x_cathod_entry.get())), fixed_element='None')
            new_window.destroy()
            window.after(1, lambda: window.focus_force())
        else:
            plot(additional_element=True, cathod_name=str(get_rid_of_white_spaces((alloy_entry.get()).lower())),
                 x_cat=float(get_rid_of_white_spaces(x_cathod_entry.get())), fixed_element='None', analyze=analyze)
            new_window.destroy()
            window.after(1, lambda: window.focus_force())


    new_window.mainloop()

additional_element_drop = ['','No', 'Yes']
options_1 = StringVar()
options_1.set(additional_element_drop[0])

font = tkFont.Font(family='Helvetica', size=12)
drop_down_1 = ttk.OptionMenu(frame_1, options_1, *additional_element_drop)
drop_down_1.grid(row=6, column=1)
drop_down_1.configure(width=15)

analyze_label = ttk.Label(frame_1, text="How would you like to analyze:", font=('Helvetica',14))
analyze_label.grid(row=7, column=0)

analyze_options = ['','None','Analyze Experiment Data', 'Use Solution model (Standard State)', 'Use Solution model ('
                                                                                             'Ideal '
                                                                                        'Solution)', 'Use Solution '
                                                                                                   'model (Regular solution)']
options_2 = StringVar()
options_2.set(analyze_options[0])

drop_down_2 = ttk.OptionMenu(frame_1, options_2, *analyze_options)
drop_down_2.grid(row=7, column=1)
drop_down_2.configure(width=35)

next_button = ttk.Button(frame_1, text = 'Next', width=9, command = lambda:
next_button_command())
next_button.grid(row=8, column=2)

def next_button_command():
    additional_element_option = options_1.get()
    analyze_option = options_2.get()
    if additional_element_option == 'No' and analyze_option == 'None':
        no_command()
    elif additional_element_option == 'Yes' and analyze_option == 'None':
        yes_command()
    elif additional_element_option == 'No' and analyze_option == 'Analyze Experiment Data':
        plot(analyze= 'Analyze Experiment Data')
    elif additional_element_option == 'No' and analyze_option == 'Use Solution model (Standard State)':
        plot(analyze='Use Solution model (Standard State)')
    elif additional_element_option == 'Yes' and analyze_option == 'Analyze Experiment Data':
        yes_command(analyze='Analyze Experiment Data')
    elif additional_element_option == 'Yes' and analyze_option == 'Use Solution model (Standard State)':
        yes_command(analyze='Use Solution model (Standard State)')
    elif additional_element_option == 'No' and analyze_option == 'Use Solution model (Ideal Solution)':
        plot(analyze='Use Solution model (Ideal Solution)')
    elif additional_element_option == 'Yes' and analyze_option == 'Use Solution model (Ideal Solution)':
        yes_command(analyze='Use Solution model (Ideal Solution)')
    elif additional_element_option == 'No' and analyze_option == 'Use Solution model (Regular solution)':
        plot(analyze='Use Solution model (Regular solution)')
    elif additional_element_option == 'Yes' and analyze_option == 'Use Solution model (Regular solution)':
        yes_command(analyze='Use Solution model (Regular solution)')

# #making the label status so that the user can have feedback from gui
label_status = ttk.Label(frame_1, font=('Helvetica', 10))
label_status.grid(row=9)

#getting the direct path of the python code file
path_of_python = os.path.dirname(__file__)

def turn_list_data_into_numbers(list_1):

    for i in range(len(list_1)):
        if list_1[i].find('e') != -1:
            index_of_e = list_1[i].find('e')
            number = float(list_1[i][0:index_of_e])
            power_number = int(list_1[i][index_of_e + 1:])
            new_number = number * 10 ** power_number
            list_1[i] = new_number
        else:
            number = list_1[i]
            new_number = float(number)
            list_1[i] = new_number


def write_excel_to_list(name_of_txt, path_to_file):
    with open(name_of_txt+'.txt', 'w') as file:
        pd.read_excel(path_to_file).to_string(file, index=False)
    lines = []
    with open(name_of_txt+'.txt') as file_in:
        for line in file_in:
            new_line = line.split()
            lines.append(new_line)
    for i in range(len(lines[0])):
        lines[0][i] = lines[0][i].lower()
    for i in range(1,len(lines)):
        turn_list_data_into_numbers(lines[i])
    return lines

window.mainloop()