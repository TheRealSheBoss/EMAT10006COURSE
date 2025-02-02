

#!/usr/bin/env python

'''

AI REGRESSION MODELLING: 

Our dataset contains numeric variables relevant to the Covid pandemic across all regions in the UK. 
This data includes information about deaths, population vaccinated 1st, 2nd and 3rd doses, and many more data points.
Our team decided to apply AI/Machine Learnining regression algorithms to give us an understanding of the data. 

Thus, in this code, we have a main function called regresssion(). To split our data into test and training data, we use the traintestsplit function. 
Depending on the type of regression algorithms the user wants to fit to the data, we created subfunctions for Linear Regression, Polynomial Regression, and Decision Tree Regression.
Lastly, we have a function to compare all these models to see which ones performed best. 

The other sub-functions are SelectTargetVariable(), and traintestsplit(). These help the user compare peformance of each model and select a target variable as well as split data before 
running the regression algorithms through the data. 

PERFORMANCE METRICS: 

The performance metrics used are the Mean Squared Error(MSE) and R-squared. 
A model with a lower MSE is a better performning data and the closer R-squared value is to 1, the better the model's fit to the data. 
Hence, better performing. However, to prevent our model from over-fitting to the data and ensure model generalizability to new unseen data, we 
had to optimize for parameters, specifically in our polynomial model, so you will see parameter testing happening within the polynomial algorithm. 
A polynomial degree value more than 5 is likely to produce overfitting or crash the program, so in order to prevent this, we introduced a While loop to 
operate the code only if the conditional that poly_degree_test has to be less than or equal to 5 is met. 

WHILE TRUE LOOPS: 
    
In order to prevent our program from crashing, we implemented a while true loop with if, else statements that will only run the functions within Regression_models.py if the user enter the 
correct input value. 

We set conditions for the value of the input parameter a user enters to run the linear regression function. If user enters L in response to the regression_type input variable, the program is 
instructed to run a linear regression model denoted with the linear() function. Once the linear regression algorithm runs, the user is then asked if they wish to continue in regression models 
and run other models. If the answer is no, the program breaks. If yes, the program continues. If user enters something else, the program prints ‘Invalid input’. 

We also apply a While True loop to the train_test_split() function for the purpose of ensuring our test size input values are between 0.1 and 0.5, and to make sure the input value entered to 
represent random state is actually an integer. The program minimizes the possibility of crashing by only running when the right input has been entered. 

THIS SCRIPT CAN BE USED TO: 
    
    1. Fit 3 AI regression models imported from the scikit-learn library to the data. 
    2. Evaluate each model's performance(fit to data) using metrics such as Mean Squared Error(MSE) and R-squared. Produce line graphs, scatters plots and box plots
    that give us a visual representation of performance of each model.
    3. Use the CompareAllModels function to compare the performance of each model to each other using box plot files as the visualization method.
    
'''

def regression(file_location):
    """Asks users to select the target variable for prediction (using 
    Variable_Finder() from variable_finder module). 
    Calls traintestsplit() to split parameters and response into training 
    and testing samples.
    Subsequently, asks users to select which regression model they wish to 
    apply and calls the appropriate corresponding function. See each function 
    for description of functionality.
    Once the regression model has been implemented, the user can either stay 
    in this module to apply an alternative model or return to covid_project 
    to implement another program functionality. """
    import matplotlib
    #matplotlib.use('TkAgg') #comment out if using Jupyter notebook.
    #%matplotlib inline  #(comment out if not using Jupyter NB)
    import matplotlib.pyplot as plt
    import pandas as pd
    from sklearn.metrics import mean_squared_error, r2_score  #from sklearn.metrics import mean_squared_error, r2_score
    from sklearn import linear_model  #from sklearn import linear_model
    from sklearn.preprocessing import PolynomialFeatures
    from sklearn.model_selection import KFold
    from sklearn.tree import DecisionTreeRegressor
    from scipy.stats import ttest_rel
    from sklearn.model_selection import train_test_split
    import numpy as np
    import variable_finder as VF
    import graphs as Gph
    from matplotlib.backends.backend_pdf import PdfPages
    
    master_data = pd.read_csv(f'{file_location}/Master Data.csv')

    def traintestsplit(X_data, Y_data):
        """Function splits the dataset into training and test sets. The user is 
        asked to input the required test size and random state for splitting 
        the data.
        Function returns the training and test sets for the pre-determined X 
        and Y variables."""
        while True:
            try:
                size_test = float(input("What test size do you want? This has to take the form of a float between 0.1 - 0.5:"))
                if size_test > 0.5 or size_test < 0.1:
                    print("Test size must be less than 0.5 and greater than 0.1")
                    continue
                else:
                    break
            except ValueError:
                print("Test size must be a float value between 0 and 1")
                continue
        
        while True:
            try:
                state_random = int(input("What random state do you want? Enter any integer number:"))
                break
            except ValueError:
                print("Test size must be an integer value")
                continue
       
        
        Xtr, Xtest, Ytr, Ytest = train_test_split(X_data, Y_data, test_size = float(size_test), random_state = int(state_random))
        
        return Xtr, Xtest, Ytr, Ytest 
    
    def linear(Xtr, Xtest, Ytr, Ytest):
        """
        Function takes the training and test split data of predefined X and Y 
        variables.
        Function uses LinearRegression function from sklearn and is trained on 
        the training data sets.
        The fitted linear regression model (regr) then predicts the Y variable 
        of interest from the Xtest dataset. 
        The function prints the mean squared error and R-squared scores for the 
        models prediction from both the training and test sets. 
        The function then calls the class Data_Viz from module graphs.py to display 
        a scatterplot of the predicted vs actual values for the Y test set.

        Parameters
        ----------
        Xtr : training dataset of predefined X variables.
        Xtest : test dataset of predefined X variables.
        Ytr : training dataset of predefined Y variable.
        Ytest : test dataset of predefined Y variable.

        Returns
        -------
        None.

        """
        regr = linear_model.LinearRegression()
        regr_model = regr.fit(Xtr, Ytr)
    
        print(f'Coefficent is {regr.coef_}')
    
        print(f'Intercept is {regr.intercept_}')
        
        ypred_test = regr_model.predict(Xtest)
        print("\n" f'Testing MSE is {mean_squared_error(ypred_test, Ytest)}')
        print("\n" f'Testing R2 score is {r2_score(ypred_test, Ytest)}')
        
        ypred_train = regr_model.predict(Xtr)
        print("\n" f'Training MSE is {mean_squared_error(ypred_train, Ytr)}')
        print("\n" f'Training R2 score is {r2_score(ypred_train, Ytr)}')
        
        
        xlabel = 'Predicted values'
        ylabel = 'True values'
        title = 'Linear Regression model, predicted vs. true values'
        Plots = Gph.Data_Viz(ypred_test, Ytest, None, xlabel, ylabel, title)
        Plots.scatter()
        
        

    def Polynomial(Xtr, Xtest, Ytr, Ytest): #cross validation happening inside this function too
        """
        Function takes the training and test split data of predefined X and Y 
        variables.
        The user is asked the number of degrees over which to transform the data.
        Function uses PolynomialFeatures function from sklearn to perform 
        cross-validation across each of the degrees by iteratively 
        transforming the data sets across the range of degrees 
        selected by the user.
        For each iteration, the function then uses the LinearRegression from sklearn 
        and is fit to the transformed training data sets.
        The fitted linear regression model (regr) then predicts the Y variable 
        of interest from the transformed Xtest dataset. 
        The function plots the mean squared error for the training and test predictions
        as a multi-line plot over each iteraction of the  data transformations. 

        Parameters
        ----------
        Xtr : training dataset of predefined X variables.
        Xtest : test dataset of predefined X variables.
        Ytr : training dataset of predefined Y variable.
        Ytest : test dataset of predefined Y variable.

        Returns
        -------
        None.

        """
        while True:
            try:
                poly_degree_test = int(input("Please enter an integer as the maximum number of polynomial degree values you wish to test in this model (maximum number is 5) : "))
                if poly_degree_test > 5 or poly_degree_test < 1:
                    print("Degree must be between 1 and 5") 
                    continue
                else:
                    break
            except ValueError:
                print("Degree must be an integer betweeen 1 and 5")
                continue

        MSE_test_data = []
        MSE_train_data = []
        
        for i in range(poly_degree_test):
            poly = PolynomialFeatures(degree=i+1)
            
            Xtr_new = poly.fit_transform(Xtr)
            Xtest_new = poly.fit_transform(Xtest)
            
            regr = linear_model.LinearRegression()
            regr.fit(Xtr_new, Ytr) #fit transformed data and target to regression model 
            
            pred_tr = regr.predict(Xtr_new) #performing predictions on transformed data 
            pred_tst = regr.predict(Xtest_new)
            
            MSE_train_data.append(mean_squared_error(Ytr, pred_tr))
            MSE_test_data.append(mean_squared_error(Ytest, pred_tst))

        AllXVars = [MSE_train_data, MSE_test_data]
        y_var = list(range(1, poly_degree_test+1))
        labels = ['Training', 'Validation']
        xlabel = 'Degree'
        ylabel = 'MSE'
        title = 'Parameter optimisation and cross validation for Polynomial Regression'
        Plots = Gph.Data_Viz(AllXVars, y_var, labels, xlabel, ylabel, title)

        print('1. The ideal polynomial degree for this model is the point where our MSE is lowest for both training') 
        print('and test data. Please identify it in figure produced.')
        Plots.multi_line()
        
    
    def DecisionTree(Xtr, Xtest, Ytr, Ytest):
        """
        Function takes the training and test split data of predefined X and Y 
        variables.
        Function uses DecisionTreeRegressor() function from sklearn and is 
        fit to the training data sets.
        The fitted decision tree regression model (DTR_model) then predicts 
        the Y variable of interest from the Xtest dataset. 
        The function prints the mean squared error and R-squared scores for the 
        models prediction from both the training and test sets in the terminal.
        The function also saves a simple table of the training and test mean 
        squared errors.

        Parameters
        ----------
        Xtr : training dataset of predefined X variables.
        Xtest : test dataset of predefined X variables.
        Ytr : training dataset of predefined Y variable.
        Ytest : test dataset of predefined Y variable.

        Returns
        -------
        None.
        """
        
        DTR = DecisionTreeRegressor()
        DTR_model = DTR.fit(Xtr, Ytr)
        ypred_train = DTR_model.predict(Xtr)
        print("\n" f'Training MSE is {mean_squared_error(ypred_train, Ytr)}')
        print("\n" f'Training R2 score is {r2_score(ypred_train, Ytr)}')
        
        ypred_test = DTR_model.predict(Xtest)
        print("\n" f'Testing MSE is {mean_squared_error(ypred_test, Ytest)}')
        print("\n" f'Testing R2 score is {r2_score(ypred_test, Ytest)}')
        
        fig, axs = plt.subplots()
        axs.xaxis.set_visible(False) 
        axs.yaxis.set_visible(False)
        prediction_data = [[mean_squared_error(ypred_train, Ytr), r2_score(ypred_train, Ytr)], 
                           [mean_squared_error(ypred_test, Ytest), r2_score(ypred_test, Ytest)]]
        columns = ('MSE', 'R squared')
        rows = ['Training', 'Test']
        axs.axis('tight')
        axs.axis('off')
        the_table = axs.table(cellText=prediction_data,rowLabels = rows, colLabels=columns,loc='center')
        the_table.auto_set_font_size(False)
        the_table.set_fontsize(8)
        pp = PdfPages("DTR_Errors.pdf")
        pp.savefig(fig, bbox_inches='tight')
        pp.close()
        plt.show()
    
    
    def CompareAllModels(Xtr, Xtest, Ytr, Ytest):
        """
        Function takes the training and test split data of predefined X and Y 
        variables.
        Function compares LinearRegression(), PolynomialFeatures (degree 2) and 
        DecisionTreeRegressor() functions from sklearn by cross validation. 
        The training and test data sets are split randomly into 10 cross-
        validation samples using KFold() from sklearn. 
        For each iteraction of the cross-validation samples:
        LinearRegression() (regr) and DecisionTreeRegressor() (DTR) are fit to 
        the training data sets (Xtrain, Ytrain). The fitted models 
        PolynomialFeatures transforms the training and test validation samples
        by degree 2. Subsequently, LinearRegression is fit to the transformed 
        training data sets.
        All three trained models (model_LR, model_FTR, model_poly), are then 
        used to predict repsonse (Y) values on the Xtst validation sample.
        For each cross validation sample, the mean squared error and R squared 
        scores of the predicted vs actual values for the cross-valudation Ytst
        set are then calculated and appended to the corresponding list for 
        each model.
        
        The function then calls multi_boxplot() from the class Data_Viz from 
        module graphs.py to display the boxplots of cross-validation mean 
        squared error scores for each model on the same plot.
        The function prints the mean of the mean squared error and R-squared 
        scores for each model in the terminal.  

        Parameters
        ----------
        Xtr : training dataset of predefined X variables.
        Xtest : test dataset of predefined X variables.
        Ytr : training dataset of predefined Y variable.
        Ytest : test dataset of predefined Y variable.

        Returns
        -------
        None.
        """
        mse_LR = []
        r2_LR = []
        mse_DTR = []
        r2_DTR = []
        mse_poly = []
        r2_poly = []
        
        regr = linear_model.LinearRegression()
        DTR = DecisionTreeRegressor()
        poly = PolynomialFeatures()
        cv = KFold(n_splits=10, shuffle=True)
        for train_index, test_index in cv.split(Xtr):
            Xtrain, Xtst = Xtr[train_index], Xtr[test_index]
            Ytrain, Ytst = Ytr[train_index], Ytr[test_index]
            
            model_LR = regr.fit(Xtrain, Ytrain)
            LR_pred = model_LR.predict(Xtst)
            mse_LR.append(mean_squared_error(Ytst, LR_pred))
            r2_LR.append(r2_score(Ytst, LR_pred))
            
            model_DTR = DTR.fit(Xtrain, Ytrain)
            DTR_pred = model_DTR.predict(Xtst)
            mse_DTR.append(mean_squared_error(Ytst, DTR_pred))
            r2_DTR.append(r2_score(Ytst, DTR_pred))
            
            Xtrain_new = poly.fit_transform(Xtrain)
            Xtst_new = poly.fit_transform(Xtst)
            model_poly = regr.fit(Xtrain_new, Ytrain) #fit transformed data and target to regression model 
            poly_pred = model_poly.predict(Xtst_new)
            mse_poly.append(mean_squared_error(Ytst, poly_pred))
            r2_poly.append(r2_score(Ytst, poly_pred))
        
        AllMSE = []
        AllMSE.append(mse_LR)
        AllMSE.append(mse_DTR)
        AllMSE.append(mse_poly)
        labels = ['Linear \nRegression', 'Decision Tree \nRegression', 'Polynomial \nRegression']
        xlabel = 'AI models'
        ylabel = 'Mean Squared Error'
        title = 'Comparison of AI model performances'
        Plots = Gph.Data_Viz(AllMSE, None, labels, xlabel, ylabel, title)
        Plots.multi_boxplot()

        
        print("\n" f'LR mse: mean={np.mean(mse_LR)}, sd={np.std(mse_LR)}')
        print("\n" f'LR r2: mean={np.mean(r2_LR)}, sd={np.std(r2_LR)}')
        print("\n" f'DTR mse: mean={np.mean(mse_DTR)}, sd={np.std(mse_DTR)}')
        print("\n" f' DTR r2: mean={np.mean(r2_DTR)}, sd={np.std(r2_DTR)}') 
        print("\n" f'LR vs. DTR: {ttest_rel(mse_LR,mse_DTR)}'"\n")
    
    def SelectTargetVariable():
        """Asks user to select the appropriate response variable for prediction
        and returns a DataFrame of the parameters and an array of the response."""
        while True:
            var_choice = VF.Variable_Finder("target", master_data)
            Y_var = var_choice.variable_finder()
            if Y_var.dtype != float:
                print("Invalid input, please select a numeric variable")
                continue
            else:
                master_data_copy = master_data.copy()
                X = master_data_copy.drop(columns=[Y_var.name, 'Local Authority', 'Region name'])
                return X, Y_var
                break


    Parameters, Target = SelectTargetVariable()
    
    Xtraining, Xtesting, Ytraining, Ytesting = traintestsplit(Parameters, Target)
    Xtraining = Xtraining.to_numpy()
    Xtesting = Xtesting.to_numpy()
    Ytraining = Ytraining.to_numpy()
    Ytesting = Ytesting.to_numpy()
    
    
 
    while True:

        regression_type = input("Do you want to use a linear regression model (L), Polynomial regression (P), Decision Tree Regression (D), compare all (C) or return to covid_project.py (main)? ")
        if regression_type == "L":
            linear(Xtraining, Xtesting, Ytraining, Ytesting)
            info_stay = input("Do you want to stay in regression models? (Y or N) ")
            if info_stay == "Y":
                continue
            elif info_stay == "N":
                break
            else:
                print("Invalid input")
                continue
        elif regression_type == "P":
            Polynomial(Xtraining, Xtesting, Ytraining, Ytesting)
            info_stay = input("Do you want to stay in regression models? (Y or N) ")
            if info_stay == "Y":
                continue
            elif info_stay == "N":
                break
            else:
                print("Invalid input")
                continue
        elif regression_type == "D":
            DecisionTree(Xtraining, Xtesting, Ytraining, Ytesting)
            info_stay = input("Do you want to stay in regression models? (Y or N) ")
            if info_stay == "Y":
                continue
            elif info_stay == "N":
                break
            else:
                print("Invalid input")
                continue
        elif regression_type == "C":
            CompareAllModels(Xtraining, Xtesting, Ytraining, Ytesting)
            info_stay = input("Do you want to stay in regression models? (Y or N) ")
            if info_stay == "Y":
                continue
            elif info_stay == "N":
                break
            else:
                print("Invalid input")
                continue
        elif regression_type == "main":
            break
        else:
            print("Invalid input")
            continue
    
    
    
