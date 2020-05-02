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
        self.df_assessments = pd.DataFrame()
        self.all_duration_list = []
        self.users_categories_list = []
        self.all_dur_mean_list = []
        self.all_cat_comp_dur_dict = {}
        self.all_users_answers_list = []
        self.all_users_accAnswers_percentage_list = []
        self.all_cat_comp_acc_dict = {}
        self.all_cat_comp_input_dict = {} # data for y-axis of linear plot
        self.all_cat_comp_assess_dict = {} #for user_assessment_plot
        self.dataframe = pd.DataFrame
        self.all_cat_comp_assess_list = []

    def assessment_reader(self):
        cnx = sqlite3.connect('database/final_db/QA2.db')
        self.df_assessment = pd.read_sql_query("SELECT * FROM Assessment", cnx)
        # assessment_column_1 = self.df_assessment["assessment_question_1"]
        # assessment_column_2 = self.df_assessment["assessment_question_1"]
        cnx.commit()
        cnx.close()


    def comp_duration_data(self):
        # fetching "complexity" of the questions from the primary database
        cnx = sqlite3.connect('database/QA2.db')
        self.df_questions = pd.read_sql_query("SELECT * FROM questions", cnx)
        complexity_column = self.df_questions["complexity"]
        cnx.commit()
        cnx.close()

        # adding "complexity" of the questions to the main database
        cnx = sqlite3.connect('database/final_db/QA2.db')
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
        # for every user, we calculate the mean of 'the time durations of all questions with a specific complexity(complexity 1, 2, or 3)'
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
                my_dict_1[j+1] = statistics.mean(my_dict[j + 1])

        for i in range(0, len(self.all_dur_mean_list)):
            for j in range(0, len(self.all_dur_mean_list[0])):
                if j == 0:
                    self.complexity_1_data.append(self.all_dur_mean_list[i][1])
                elif j == 1:
                    self.complexity_2_data.append(self.all_dur_mean_list[i][2])
                elif j == 2:
                    self.complexity_3_data.append(self.all_dur_mean_list[i][3])


    def accuracy_comp_data(self):
        self.complexity_1_data = []
        self.complexity_2_data = []
        self.complexity_3_data = []
        # all_users_answers_list = []
        counter = 1
        while counter != 21:
            selected_rows = self.df_interactions[self.df_interactions["question_id"] == counter]
            self.all_users_answers_list.append(selected_rows["user_answer"].tolist())
            print(len(self.all_users_answers_list[counter - 1]))
            counter = counter + 1

        all_accurate_answer_dict = {}
        for i in range(1, 21):
            all_accurate_answer_dict[i] = 0
        for i in range(0, len(self.all_users_answers_list)):
            for j in range(0, len(self.all_users_answers_list[0])):
                if self.all_users_answers_list[i][j] == "yes":
                    all_accurate_answer_dict[i+1] = all_accurate_answer_dict[i+1] + 1

        # assigning each duration_list in all_duration_list to its corresponding complexity
        for i in range(0, len(self.df_questions["complexity"])-1 ):
            if self.df_questions["complexity"][i] == 1:
                self.complexity_1_data.append(all_accurate_answer_dict[i+1])
            elif self.df_questions["complexity"][i] == 2:
                self.complexity_2_data.append(all_accurate_answer_dict[i+1])
            elif self.df_questions["complexity"][i] == 3:
                self.complexity_3_data.append(all_accurate_answer_dict[i+1])

        # calculating the percentage of people who have answered a question accurately
        self.assessment_reader()
        participants_quantity = len(self.df_assessment.index)
        self.complexity_1_data = [(comp_1/participants_quantity)*100 for comp_1 in self.complexity_1_data ]
        self.complexity_2_data = [(comp_2/participants_quantity)*100 for comp_2 in self.complexity_2_data ]
        self.complexity_3_data = [(comp_3/participants_quantity)*100 for comp_3 in self.complexity_3_data ]



    def question_category_recognizer(self, dbTable_name):
        if dbTable_name == "interaction":
            self.dataframe = self.df_interactions
        elif dbTable_name == "assessment":
            self.dataframe = self.df_assessment

        self.users_categories_list = []
        user_ids = OrderedSet(self.dataframe["user_id"])
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
            comp_dur_dict[1] = []
            comp_dur_dict[2] = []
            comp_dur_dict[3] = []
            self.all_cat_comp_dur_dict[i] = comp_dur_dict
        for i in range (0, len(self.users_categories_list)):
            if self.users_categories_list[i] == "controlledLanguage":
                self.all_cat_comp_dur_dict[0][1].append(self.all_dur_mean_list[i][1])
                self.all_cat_comp_dur_dict[0][2].append(self.all_dur_mean_list[i][2])
                self.all_cat_comp_dur_dict[0][3].append(self.all_dur_mean_list[i][3])
            elif self.users_categories_list[i] == "sparqlQuery":
                self.all_cat_comp_dur_dict[1][1].append(self.all_dur_mean_list[i][1])
                self.all_cat_comp_dur_dict[1][2].append(self.all_dur_mean_list[i][2])
                self.all_cat_comp_dur_dict[1][3].append(self.all_dur_mean_list[i][3])
            elif self.users_categories_list[i] == "knowledge_graph":
                self.all_cat_comp_dur_dict[2][1].append(self.all_dur_mean_list[i][1])
                self.all_cat_comp_dur_dict[2][2].append(self.all_dur_mean_list[i][2])
                self.all_cat_comp_dur_dict[2][3].append(self.all_dur_mean_list[i][3])
            elif self.users_categories_list[i] == "verbalized_answer":
                self.all_cat_comp_dur_dict[3][1].append(self.all_dur_mean_list[i][1])
                self.all_cat_comp_dur_dict[3][2].append(self.all_dur_mean_list[i][2])
                self.all_cat_comp_dur_dict[3][3].append(self.all_dur_mean_list[i][3])

        for i in range(0, len(self.all_cat_comp_dur_dict)):
            for j in range(0, len(self.all_cat_comp_dur_dict[i])):
                self.all_cat_comp_dur_dict[i][j+1] = statistics.mean(self.all_cat_comp_dur_dict[i][j+1])

        self.all_cat_comp_input_dict = self.all_cat_comp_dur_dict



    def comp_perc_accuracy_data(self):
        # for every user, we calculate the mean of 'the accuracy of all questions with a specific complexity(complexity 1, 2, or 3)'
        self.complexity_1_data = []
        self.complexity_2_data = []
        self.complexity_3_data = []
        all_comp_answer_list = []  # it includes all the dictionaries we are creating right below
        # for every user we create a dictionary which includes 3 lists, for answers for questions with complexity 1, 2, 3
        for i in range(0, len(self.all_users_answers_list[0])):
            user_comp_acc_dict = {}
            user_comp_acc_dict[1] = []
            user_comp_acc_dict[2] = []
            user_comp_acc_dict[3] = []
            all_comp_answer_list.append(user_comp_acc_dict)
        for i in range(0, len(self.df_questions["complexity"]) - 1):
            if self.df_questions["complexity"][i] == 1:
                for j in range(0, len(self.all_users_answers_list[0])):
                    my_dict = all_comp_answer_list[j]
                    my_dict[1].append(self.all_users_answers_list[i][j])
            elif self.df_questions["complexity"][i] == 2:
                for j in range(0, len(self.all_users_answers_list[0])):
                    my_dict = all_comp_answer_list[j]
                    my_dict[2].append(self.all_users_answers_list[i][j])
            elif self.df_questions["complexity"][i] == 3:
                for j in range(0, len(self.all_users_answers_list[0])):
                    my_dict = all_comp_answer_list[j]
                    my_dict[3].append(self.all_users_answers_list[i][j])

        for i in range(0, len(self.all_users_answers_list[0])):
            user_acc_perc_dict = {}
            self.all_users_accAnswers_percentage_list.append(user_acc_perc_dict)
        for i in range(0, len(all_comp_answer_list)):
            for j in range(0, len(all_comp_answer_list[i])):
                my_dict_1 = self.all_users_accAnswers_percentage_list[i]
                accurate_counter = 0
                for k in range(0, len(all_comp_answer_list[i][j+1])):  # j+1 because we have complexity 1, 2, or 3. Not 0, 1, or 2.
                    if (all_comp_answer_list[i][j+1][k]) == "yes":
                        accurate_counter = accurate_counter + 1
                my_dict_1[j+1] = (accurate_counter/len(all_comp_answer_list[i][j+1])) * 100
                my_dict_1[j+1] = round(my_dict_1[j+1], 2)  #rounding the float numbers


    def category_accuracy_data(self):
        self.all_cat_comp_acc_dict = {}
        for i in range(0, 4):
            comp_dur_dict = {}
            comp_dur_dict[1] = []
            comp_dur_dict[2] = []
            comp_dur_dict[3] = []
            self.all_cat_comp_acc_dict[i] = comp_dur_dict
        for i in range (0, len(self.users_categories_list)):
            if self.users_categories_list[i] == "controlledLanguage":
                self.all_cat_comp_acc_dict[0][1].append(self.all_users_accAnswers_percentage_list[i][1])
                self.all_cat_comp_acc_dict[0][2].append(self.all_users_accAnswers_percentage_list[i][2])
                self.all_cat_comp_acc_dict[0][3].append(self.all_users_accAnswers_percentage_list[i][3])
            elif self.users_categories_list[i] == "sparqlQuery":
                self.all_cat_comp_acc_dict[1][1].append(self.all_users_accAnswers_percentage_list[i][1])
                self.all_cat_comp_acc_dict[1][2].append(self.all_users_accAnswers_percentage_list[i][2])
                self.all_cat_comp_acc_dict[1][3].append(self.all_users_accAnswers_percentage_list[i][3])
            elif self.users_categories_list[i] == "knowledge_graph":
                self.all_cat_comp_acc_dict[2][1].append(self.all_users_accAnswers_percentage_list[i][1])
                self.all_cat_comp_acc_dict[2][2].append(self.all_users_accAnswers_percentage_list[i][2])
                self.all_cat_comp_acc_dict[2][3].append(self.all_users_accAnswers_percentage_list[i][3])
            elif self.users_categories_list[i] == "verbalized_answer":
                self.all_cat_comp_acc_dict[3][1].append(self.all_users_accAnswers_percentage_list[i][1])
                self.all_cat_comp_acc_dict[3][2].append(self.all_users_accAnswers_percentage_list[i][2])
                self.all_cat_comp_acc_dict[3][3].append(self.all_users_accAnswers_percentage_list[i][3])
        q = 1

        for i in range(0, len(self.all_cat_comp_acc_dict)):
            for j in range(0, len(self.all_cat_comp_acc_dict[i])):
                self.all_cat_comp_acc_dict[i][j+1] = statistics.mean(self.all_cat_comp_acc_dict[i][j+1])

        self.all_cat_comp_input_dict = self.all_cat_comp_acc_dict


    def categoty_user_assessment(self):
        assessment_column_1 = self.df_assessment["assessment_question_1"]
        assessment_column_2 = self.df_assessment["assessment_question_2"]
        self.all_cat_comp_assess_dict = {}
        for i in range(0, 4):
            comp_dur_dict = {}
            comp_dur_dict[1] = []
            comp_dur_dict[2] = []
            self.all_cat_comp_assess_dict[i] = comp_dur_dict
        for i in range(0, len(self.users_categories_list)):
            if self.users_categories_list[i] == "controlledLanguage":
                self.all_cat_comp_assess_dict[0][1].append(int(assessment_column_1[i]))
                self.all_cat_comp_assess_dict[0][2].append(int(assessment_column_2[i]))
            elif self.users_categories_list[i] == "sparqlQuery":
                self.all_cat_comp_assess_dict[1][1].append(int(assessment_column_1[i]))
                self.all_cat_comp_assess_dict[1][2].append(int(assessment_column_2[i]))
            elif self.users_categories_list[i] == "knowledge_graph":
                self.all_cat_comp_assess_dict[2][1].append(int(assessment_column_1[i]))
                self.all_cat_comp_assess_dict[2][2].append(int(assessment_column_2[i]))
            elif self.users_categories_list[i] == "verbalized_answer":
                self.all_cat_comp_assess_dict[3][1].append(int(assessment_column_1[i]))
                self.all_cat_comp_assess_dict[3][2].append(int(assessment_column_2[i]))

        # convert the dictionary to a list which is compatible with input of box plots
        for j in range(1, 3):
            sublist = []
            for i in range(0, 4):
                sublist.append(list(self.all_cat_comp_assess_dict.values())[i][j])
            self.all_cat_comp_assess_list.append(sublist)



    def line_plotter(self, image_number, x_label, y_label):
        X=[]
        Y=[]
        X.extend(self.all_cat_comp_input_dict[0].keys()) # complexities are the same for all 4 types of interpretations
        # X = [x + 1 for x in list(X)]  # because complexities are 1,2,3 not 0,1,2
        for i in range(0, len(self.all_cat_comp_input_dict)):
            Y.append(self.all_cat_comp_input_dict[i].values())

        # 1 is the initial value, 4 is the final value  (last value is not taken) and 1 is the difference of values between two consecutive ticks
        plt.xticks(np.arange(1, 4, 1))
        # plt.figure(1, figsize=(30, 20))
        plt.plot(X,list(Y[0]), label="controlled language", linewidth=3)
        plt.plot(X,list(Y[1]), label="sparql query", linewidth=3)
        plt.plot(X,list(Y[2]), label="knowledge graph", linewidth=3)
        plt.plot(X,list(Y[3]), label="verbalized answer", linewidth=3)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend(loc='best')
        plt.savefig('fig'+ str(image_number) + '.png', bbox_inches='tight' )

        # enabling pyplot to properly clean up the memory.
        plt.close()


    def box_plotter(self, image_number, x_label, y_label):
        ## agg backend is used to create plot as a .png file
        mpl.use('agg')
        ## combine these different collections into a list
        data_to_plot = [self.complexity_1_data, self.complexity_2_data, self.complexity_3_data]

        # Create a figure instance
        fig = plt.figure(1, figsize=(9, 6))
        # Create an axes instance
        ax = fig.add_subplot(111)
        # fig.colorbar(cm.ScalarMappable(norm=norm, cmap=cmap), ax=ax)

        # Create the boxplot
        bp = ax.boxplot(data_to_plot, showfliers=False, patch_artist=True)
        for box in bp['boxes']:
            box.set(color="palevioletred", linewidth=2)
            box.set(facecolor="lightskyblue")

        plt.xlabel(x_label)
        plt.ylabel(y_label)

        # Save the figure
        fig.savefig('fig'+ str(image_number) + '.png', bbox_inches='tight')

        #enabling pyplot to properly clean up the memory.
        plt.close()


    def set_box_color(self, bp, color):
        plt.setp(bp['boxes'], color=color)
        plt.setp(bp['whiskers'], color=color)
        plt.setp(bp['caps'], color=color)
        plt.setp(bp['medians'], color="#31a354", linewidth=2)

    def box_plotter_grouped(self, image_number):
        # data_a = [[1, 2, 5], [5, 7, 2, 2, 5], [7, 2, 5]]
        # data_b = [[6, 4, 2], [1, 2, 5, 3, 2], [2, 3, 5, 1]]
        data_a = [self.all_cat_comp_assess_list[0][i] for i in range(0,4)]
        data_b = [self.all_cat_comp_assess_list[1][i] for i in range(0,4)]

        ticks = ['contLan', 'sparql', 'KG', 'verbalAn' ]
        plt.figure(1, figsize=(9, 6))

        bpl = plt.boxplot(data_a, positions=np.array(np.arange(len(data_a))) * 2.0 - 0.4, sym='', widths=0.6, showfliers=False)
        bpr = plt.boxplot(data_b, positions=np.array(np.arange(len(data_b))) * 2.0 + 0.4, sym='', widths=0.6, showfliers=False)
        self.set_box_color(bpl, '#D7191C')  # colors are from http://colorbrewer2.org/
        self.set_box_color(bpr, '#2C7BB6')

        # draw temporary red and blue lines and use them to create a legend
        plt.plot([], c='#D7191C', label='ease of following the structure of the survey')
        plt.plot([], c='#2C7BB6', label='ease of understanding the relationship between different parts of a question')
        plt.legend()

        plt.xticks(np.arange(0, len(ticks) * 2, 2), ticks)
        plt.xlim(-2, len(ticks) * 2)
        plt.ylim(1, 6)
        plt.tight_layout()
        plt.savefig('fig'+ str(image_number) + '.png', bbox_inches='tight')
        plt.close()



if __name__ == '__main__':
    dbex = DatabaseExploration()
    dbex.comp_duration_data()
    dbex.box_plotter(1, "Complexity(The number of triples a sparql query is made of)", "Time Duration(seconds)")
    dbex.comp_mean_duration_data()
    dbex.box_plotter(2, "Complexity(The number of triples a sparql query is made of)", "Mean Time Duration(seconds)")
    dbex.accuracy_comp_data()
    dbex.box_plotter(3, "Complexity(The number of triples a sparql query is made of)", "Accurate Answers(percentage of people who have answered a question accurately)")
    dbex.question_category_recognizer("interaction")
    dbex.category_dur_data()
    dbex.line_plotter(4, 'Complexity(the number of triples a sparql query is made of)', 'Time Duration(second)')

    dbex.comp_perc_accuracy_data()
    dbex.category_accuracy_data()
    dbex.line_plotter(5, 'Complexity(the number of triples a sparql query is made of)', 'Accurate Answers(percentage of people who have answered a question accurately)')

    dbex.question_category_recognizer("assessment")
    dbex.categoty_user_assessment()
    # dbex.box_plotter(6, "Complexity(The number of triples a sparql query is made of)", "User assessment" )
    dbex.box_plotter_grouped(6)