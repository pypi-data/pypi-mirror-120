def split_data(df, train_pct=.7, dv=None, dv_threshold=.00, random_state = 5435):
    """This function will split your data into training and testing datasets, separating the outcome from the rest of the file. 
    The resultant datasets will be named x_train,y_train, x_test, and y_test.
    df: name of your dataframe to split. Original dataframe will be retained
    train_pct: adjust the number of rows that are randomdly assigned to the training dataset.
    dv: Name of your outcome column. 
    dv_threshold: For logistic modeling. If positive instances (aka '1') of your outcome measure are below this value (defaults to 5%) then when splitting the data, 
    SMOTENC will be used to upsample positive instances until this value is reached. Can be turned off by setting to 0. Accepts values 0 to 0.5"""
    
    import pandas as pd
    import numpy as np
    from sklearn.model_selection import train_test_split
    from imblearn.over_sampling import SMOTENC
    from sklearn.utils import resample
    
    #Determine positive instances of the outcome percentage
    if dv != None:
        #Split Outcome From Other Fields
        x = df.drop(dv, axis = 1).copy(deep=True)
        y = df[dv].copy(deep=True)
        
        #Split Dataset
        x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=train_pct, test_size=1-train_pct,random_state = random_state, shuffle = True)
        
        #Get DV Occurance
        dv_pct = len(df[df[dv] != 0]) / len(df)
        
        #Up-sample if needed
        if dv_pct < dv_threshold:
            
            print(f'Outcome variable "{dv}" pct: {dv_pct}. Below the dv_threshold value of {dv_threshold}. Will up-sample with SMOTE-NC...')
            
            #Get list of binary variables (mostly categorical dummy codes)
            cats = pd.DataFrame(x_train.select_dtypes(include=['number']).nunique(dropna = False, axis=0))
            cats = np.where(cats[0] == 2, True, False)
            
            #SMOTENC
            sm = SMOTENC(random_state=None, categorical_features=cats, sampling_strategy=dv_threshold/(1-dv_threshold))
            x_train, y_train = sm.fit_resample(x_train, y_train)
                        
            #Assign Model Weights (Non-Instance, Positive Instance)
            model_weights = [1 / ((1 - dv_threshold) / (1 - dv_pct))
                            ,1 / (dv_threshold / dv_pct)]
        
        else:
            model_weights = [1,1]
            
    else:
        print('You must enter a DV value')

    return x_train, y_train, x_test, y_test, model_weights