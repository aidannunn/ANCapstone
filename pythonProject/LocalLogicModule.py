"""
This file contains the class which stores algorithms that will be run locally.
It will have one class, LocalLogic, which holds the algorithm for testing the accuracy of a machine learning model and running the model against experiment data to make predictions on the data.
"""
import sklearn.metrics
from sklearn.linear_model import Lasso, LassoCV
from sklearn.metrics import accuracy_score, r2_score
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from Load_Data import *
from matplotlib import pyplot as plt

class LocalLogicModule:

    def __init__(self, lambda_val):
        self.lambda_val = lambda_val
        self.model = 0

    def fit(self, x_train, y_train):
        self.model.fit(x_train, y_train)

    def calculate_mse(self, y_pred, y_test):
        return mean_squared_error(y_pred, y_test)

    def predict(self, x_test):
        return self.model.predict(x_test)

    def test_accuracy(self, y_true, y_pred):
        return accuracy_score(y_true, y_pred)



    def train_binary_model_vapor_room_air(self, dataframe):
        """Method which builds a model for predicting on if a rodent is exposed to room air or alcohol vapor"""
        print("Building Room Air vs Vapor Model")

        # set the target condition
        target = 'Condition'

        # create model
        # max_iter is the maximum number of iterations we run to try to converge the model
        self.model = Lasso(alpha=self.lambda_val, max_iter=100_000, warm_start=True, positive=True)

        #self.model = LassoCV(n_alphas=1, alphas=[0.1], max_iter=100_000, verbose=1, n_jobs=-1)

        # retrieve data from dataframe
        y = dataframe[target].values
        features = list(dataframe.columns.values)
        features.remove('Condition')
        features.remove('Unnamed: 0')
        x = dataframe[features].values

        # Split data
        print("Splitting Data")
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.1, shuffle=True)

        # fit data to the model
        print("Fitting Data")
        self.model.fit(x_train, y_train)

        # print model parameters
        print("\nPrinting Model Coefficients")
        print(self.model.coef_)

        # predict on the training data
        prediction = self.model.predict(x_train)
        train_accuracy = sklearn.metrics.r2_score(y_train, prediction)

        # predict on the testing data
        prediction = self.model.predict(x_test)
        test_accuracy = sklearn.metrics.r2_score(y_test, prediction)

        return train_accuracy, test_accuracy

    def train_continuous_model_vapor_room_air(self, dataframe):
        """Method which builds a model for predicting how much alcohol ing g\kg a rodent has consumed"""
        print("Building Alcohol Consumption Model")

        # set the target condition
        target = 'g/kg'

        # create model
        # max_iter is the maximum number of iterations we run to try to converge the model
        self.model = Lasso(alpha=self.lambda_val, max_iter=10000000)

        # retrieve data from dataframe
        y = dataframe[target]
        features = list(dataframe.columns.values)
        features.remove('g/kg')
        features.remove('Unnamed: 0')
        x = dataframe[features]

        # Split data
        print("Splitting Data")
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, shuffle=True)

        # fit data to the model
        print("Fitting Data")
        self.fit(x_train, y_train)

        return self.model.score(x_test, y_test)

    def graph_binary_lasso_accuracy(self, dataframe, epochs):
        """This method fits data to a model a number of times equal to the epochs value,
        and then graphs the accuracy over a series of models"""

        test_accuracy_arr = []
        training_accuracy_arr = []
        for epoch in range(epochs):
            print("\nBuilding Model {} of {}".format(epoch+1, epochs))
            # train the model
            train_accuracy, test_accuracy = self.train_binary_model_vapor_room_air(dataframe)
            training_accuracy_arr.append(train_accuracy)
            test_accuracy_arr.append(test_accuracy)
            print("Training Accuracy: {}".format(train_accuracy))
            print("Testing Accuracy: {}".format(test_accuracy))

        average_training_accuracy = sum(training_accuracy_arr)/len(training_accuracy_arr)
        print("Average Training Accuracy: {}".format(average_training_accuracy))

        average_test_accuracy = sum(test_accuracy_arr)/len(test_accuracy_arr)
        print("Average Testing Accuracy: {}".format(average_test_accuracy))

        best_training_accuracy = max(training_accuracy_arr)
        index_training = training_accuracy_arr.index(best_training_accuracy)
        print("Best Training Accuracy: {} for model number {}".format(best_training_accuracy, index_training+1))

        best_testing_accuracy = max(test_accuracy_arr)
        index_testing = test_accuracy_arr.index(best_testing_accuracy)
        print("Best Testing Accuracy: {} for model number {}".format(best_testing_accuracy, index_testing + 1))

        plt.plot(range(1, epochs+1), test_accuracy_arr, label="Test Accuracy")
        plt.plot(range(1, epochs+1), training_accuracy_arr, label="Training Accuracy")
        plt.legend()
        plt.xlabel("Fit Epoch")
        plt.ylabel("R2 Score")
        plt.show()  # open window displaying graph

    def graph_continuous_lasso_accuracy(self, dataframe, epochs):
        """This method fits data to a model a number of times equal to the epochs value,
        and then graphs the accuracy over a series of models"""


        accuracy_arr = []
        for epoch in range(epochs):
            print("On Epoch {} of {}".format(epoch, epochs))
            # train the model
            accuracy = self.train_continuous_model_vapor_room_air(dataframe)
            accuracy_arr.append(accuracy)
            print("Accuracy: {}".format(accuracy))

        plt.plot(range(1, epochs+1), accuracy_arr)
        plt.xlabel("Fit Epoch")
        plt.ylabel("Lasso Score")
        plt.show()  # open window displaying graph

    def graph_lambda_accuracy(self, dataframe):
        lambda_vals = [0.000001, 0.0001, 0.005, 0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.5, 1]  # set lambda.
        x = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        accuracy_arr = []
        for val in lambda_vals:
            self.lambda_val = val
            accuracy = self.train_continuous_model_vapor_room_air(dataframe)
            accuracy_arr.append(accuracy)
            print(("\nLasso RSqaured Score with Lambda={} is {}").format(val, accuracy))

        plt.plot(x, accuracy_arr)
        plt.xlabel("Lambda Values")
        plt.ylabel("Lasso Score")
        plt.xticks(x, lambda_vals)
        plt.show()



if __name__ == "__main__":
    # loader = LoadData(r'D:\CS 421\Binary_Predictor_Data\dataframe_binary_females.xlsx')
    # learning_rate = 0.01
    # model_object = LocalLogicModule(learning_rate)
    # #model_object.train_binary_model_vapor_room_air(loader.df)
    #
    # model_object.graph_lasso_accuracy(loader.df, 100)

    # print("\n\nDone\n\n")

    loader = LoadData(r'C:\Users\charl\Desktop\dataframe_continuous_females.xlsx')
    model_object = LocalLogicModule(0.01)
    model_object.graph_lambda_accuracy(loader.df)


    print("\n\nDone\n\n")

