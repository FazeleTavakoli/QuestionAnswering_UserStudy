import sqlite3
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from datetime import timedelta
import statistics
from collections import OrderedDict
from ordered_set import OrderedSet


class DatabaseExploration:

    def __init__(self):
        self.complexity_1_data = []
        self.complexity_2_data = []
        self.complexity_3_data = []
        self.df_questions = pd.DataFrame()
        self.df_interactions = pd.DataFrame()
        self.all_duration_list = []
        self.users_categories_list = []
        self.all_dur_mean_list = []
        self.all_cat_comp_dur_dict = {}

    def comp_duration_data(self):
        # fetching "complexity" of the questions from the primary database
        cnx = sqlite3.connect('database/QA2.db')
        self.df_questions = pd.read_sql_query("SELECT * FROM questions", cnx)
        complexity_column = self.df_questions["complexity"]
        cnx.commit()
        cnx.close()

        # adding "complexity" of the questions to the main database
        cnx = sqlite3.connect('database/final_db/QA2_test.db')
        self.df_questions = pd.read_sql_query("SELECT * FROM questions", cnx)
        self.df_questions.insert(6,"complexity", complexity_column, True)
        self.df_interactions = pd.read_sql_query("SELECT * FROM interactions", cnx)
        cnx.commit()
        cnx.close()
        # user_id_colomn = df_interactions["user_id"]
        # question_id_column = df_interactions["question_id"]
        # time_column = pd.to_datetime(df_interactions["time"])

        self.df_interactions['time']= pd.to_datetime(self.df_interactions['time'])

        all_time_list = []
        counter = 1
        while counter != 21 :
            selected_rows = self.df_interactions[self.df_interactions["question_id"] == counter]
            all_time_list.append(selected_rows["time"].tolist())
            print(len(all_time_list[counter-1]))
            counter = counter + 1

        counter = 0
        for i in range(0, len(all_time_list)-1):
            duration_list = []
            answers_list_0 = all_time_list[i]
            answers_list_1 = all_time_list[i+1]
            for j in range(0, len(answers_list_0)):
                duration = (answers_list_1[j] - answers_list_0[j])
                duration_sec_microsec = duration.seconds + duration.microseconds/1000000
                duration_list.append(duration_sec_microsec)
            self.all_duration_list.append(duration_list)

        #assigning each duration_list in all_duration_list to its corresponding complexity
        #note that we don't have the duration when users answered to the first question
        for i in range(0, len(self.df_questions["complexity"])-2):
            if self.df_questions["complexity"][i+1] == 1:
                self.complexity_1_data.extend(self.all_duration_list[i])
            elif self.df_questions["complexity"][i+1] == 2:
                self.complexity_2_data.extend(self.all_duration_list[i])
            elif self.df_questions["complexity"][i+1] == 3:
                self.complexity_3_data.extend(self.all_duration_list[i])


    def comp_mean_duration_data(self):
        # for every user, we calculate the mean of the durations of all questions with a specific complexity(complexity 1, 2, or 3)
        self.complexity_1_data = []
        self.complexity_2_data = []
        self.complexity_3_data = []
        all_comp_dur_list = [] #it includes all the dictionaries we are creating right below
        #for every user we create a dictionary which includes 3 lists, for duration for questions with complexity 1, 2, 3
        for i in range(0, len(self.all_duration_list[0])):
            user_comp_dur_dict = {}
            user_comp_dur_dict[1] = []
            user_comp_dur_dict[2] = []
            user_comp_dur_dict[3] = []
            all_comp_dur_list.append(user_comp_dur_dict)
        for i in range(0, len(self.df_questions["complexity"]) - 2):
            if self.df_questions["complexity"][i + 1] == 1:
                for j in range(0, len(self.all_duration_list[0])):
                    my_dict = all_comp_dur_list[j]
                    my_dict[1].append(self.all_duration_list[i][j])
                    # complexity_1_data.extend(self.all_duration_list[i])
            elif self.df_questions["complexity"][i + 1] == 2:
                for j in range(0, len(self.all_duration_list[0])):
                    my_dict = all_comp_dur_list[j]
                    my_dict[2].append(self.all_duration_list[i][j])
                # complexity_2_data.extend(self.all_duration_list[i])
            elif self.df_questions["complexity"][i + 1] == 3:
                for j in range(0, len(self.all_duration_list[0])):
                    my_dict = all_comp_dur_list[j]
                    my_dict[3].append(self.all_duration_list[i][j])
                # complexity_3_data.extend(self.all_duration_list[i])

        # all_dur_mean_list = []
        for i in range(0, len(self.all_duration_list[0])):
            user_dur_mean_dict = {}
            self.all_dur_mean_list.append(user_dur_mean_dict)
        for i in range(0, len(all_comp_dur_list)):
            my_dict = all_comp_dur_list[i]
            for j in range(0, len(my_dict)):
                my_dict_1 = self.all_dur_mean_list[i]
                my_dict_1[j] = statistics.mean(my_dict[j + 1])

        for i in range(0, len(self.all_dur_mean_list)):
            for j in range(0, len(self.all_dur_mean_list[0])):
                if j == 0:
                    self.complexity_1_data.append(self.all_dur_mean_list[i][0])
                elif j == 1:
                    self.complexity_2_data.append(self.all_dur_mean_list[i][1])
                elif j == 2:
                    self.complexity_3_data.append(self.all_dur_mean_list[i][2])

    def accuracy_comp_data(self):
        self.complexity_1_data = []
        self.complexity_2_data = []
        self.complexity_3_data = []
        all_users_answers_list = []
        counter = 1
        while counter != 21:
            selected_rows = self.df_interactions[self.df_interactions["question_id"] == counter]
            all_users_answers_list.append(selected_rows["user_answer"].tolist())
            print(len(all_users_answers_list[counter - 1]))
            counter = counter + 1

        all_accurate_answer_dict = {}
        for i in range(1, 21):
            all_accurate_answer_dict[i] = 0
        for i in range(0, len(all_users_answers_list)):
            for j in range(0, len(all_users_answers_list[0])):
                if all_users_answers_list[i][j] == "yes":
                    all_accurate_answer_dict[i+1] = all_accurate_answer_dict[i+1] + 1

        # assigning each duration_list in all_duration_list to its corresponding complexity
        for i in range(0, len(self.df_questions["complexity"])-1 ):
            if self.df_questions["complexity"][i] == 1:
                self.complexity_1_data.append(all_accurate_answer_dict[i+1])
            elif self.df_questions["complexity"][i] == 2:
                self.complexity_2_data.append(all_accurate_answer_dict[i+1])
            elif self.df_questions["complexity"][i] == 3:
                self.complexity_3_data.append(all_accurate_answer_dict[i+1])


    def question_category_recognizer(self):
        user_ids = OrderedSet(self.df_interactions["user_id"])
        for i in range(0, len(user_ids)):
            if user_ids[i]%4 == 0:
                self.users_categories_list.append("controlledLanguage")
            elif user_ids[i]%4 == 1:
                self.users_categories_list.append("sparqlQuery")
            elif user_ids[i]%4 == 2:
                self.users_categories_list.append("knowledge_graph")
            elif user_ids[i]%4 == 3:
                self.users_categories_list.append("verbalized_answer")

    def category_dur_data(self):
        self.all_cat_comp_dur_dict = {}
        for i in range(0, 4):
            comp_dur_dict = {}
            comp_dur_dict[0] = []
            comp_dur_dict[1] = []
            comp_dur_dict[2] = []
            self.all_cat_comp_dur_dict[i] = comp_dur_dict
        for i in range (0, len(self.users_categories_list)):
            if self.users_categories_list[i] == "controlledLanguage":
                self.all_cat_comp_dur_dict[0][0].append(self.all_dur_mean_list[i][0])
                self.all_cat_comp_dur_dict[0][1].append(self.all_dur_mean_list[i][1])
                self.all_cat_comp_dur_dict[0][2].append(self.all_dur_mean_list[i][2])
            elif self.users_categories_list[i] == "sparqlQuery":
                self.all_cat_comp_dur_dict[1][0].append(self.all_dur_mean_list[i][0])
                self.all_cat_comp_dur_dict[1][1].append(self.all_dur_mean_list[i][1])
                self.all_cat_comp_dur_dict[1][2].append(self.all_dur_mean_list[i][2])
            elif self.users_categories_list[i] == "knowledge_graph":
                self.all_cat_comp_dur_dict[2][0].append(self.all_dur_mean_list[i][0])
                self.all_cat_comp_dur_dict[2][1].append(self.all_dur_mean_list[i][1])
                self.all_cat_comp_dur_dict[2][2].append(self.all_dur_mean_list[i][2])
            elif self.users_categories_list[i] == "verbalized_answer":
                self.all_cat_comp_dur_dict[3][0].append(self.all_dur_mean_list[i][0])
                self.all_cat_comp_dur_dict[3][1].append(self.all_dur_mean_list[i][1])
                self.all_cat_comp_dur_dict[3][2].append(self.all_dur_mean_list[i][2])

        for i in range(0, len(self.all_cat_comp_dur_dict)):
            for j in range(0, len(self.all_cat_comp_dur_dict[i])):
                self.all_cat_comp_dur_dict[i][j] = statistics.mean(self.all_cat_comp_dur_dict[i][j])
        a = 1

    def line_plotter(self, image_number):
        X=[]
        Y=[]
        X.extend(self.all_cat_comp_dur_dict[0].keys()) # complexities are the same for all 4 types of interpretations
        X = [x + 1 for x in list(X)]  # because complexities are 1,2,3 not 0,1,2
        for i in range(0, len(self.all_cat_comp_dur_dict)):
            Y.append(self.all_cat_comp_dur_dict[i].values())
        plt.plot(X,list(Y[0]), label="controlledLanguage")
        plt.plot(X,list(Y[1]), label="sparqlQuery")
        plt.plot(X,list(Y[2]), label="knowledge_graph")
        plt.plot(X,list(Y[3]), label="verbalized_answer")
        plt.xlabel('Complexity(the number of triples)')
        plt.ylabel('Time Duration(second)')
        plt.legend(loc='best')
        plt.savefig('fig'+ str(image_number) + '.png')

    def box_plotter(self, image_number, x_label, y_label):
        ## agg backend is used to create plot as a .png file
        mpl.use('agg')
        ## combine these different collections into a list
        data_to_plot = [self.complexity_1_data, self.complexity_2_data, self.complexity_3_data]

        # Create a figure instance
        fig = plt.figure(1, figsize=(9, 6))

        # Create an axes instance
        ax = fig.add_subplot(111)

        # Create the boxplot
        bp = ax.boxplot(data_to_plot, showfliers=False)
        plt.xlabel(x_label)
        plt.ylabel(y_label)

        # Save the figure
        fig.savefig('fig'+ str(image_number) + '.png', bbox_inches='tight')

        #enabling pyplot to properly clean up the memory.
        plt.close()



if __name__ == '__main__':
    dbex = DatabaseExploration()
    dbex.comp_duration_data()
    dbex.box_plotter(1, "Complexity", "Time Duration")
    dbex.comp_mean_duration_data()
    dbex.box_plotter(2, "Complexity", "Mean-Time Duration")
    dbex.accuracy_comp_data()
    dbex.box_plotter(3, "Complexity", "Accurate Answers")
    dbex.question_category_recognizer()
    dbex.category_dur_data()
    dbex.line_plotter(4)