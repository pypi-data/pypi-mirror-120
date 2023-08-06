def drop_categorical(df, inplace=False):
    
    import pandas as pd
    import numpy as np
    
    
    cats = list(df.select_dtypes(exclude='number'))
    print(f'Dropping {len(cats)} categorical columns: {cats}')
          
    if inplace==True:
        df.drop(columns=cats, inplace=True)
        
        return
    
    else:
        new_df = df.drop(columns=cats, inplace=False)

        return new_df

def remove_low_variation(df=None, dv=None, columns='all', threshold=.98, inplace=True, verbose=True):
    """
    For each column, determine the maximum threshold for s single variable. 
    For example, if threshold is set to .97 and your `gender` column contains 97.8% values = 1, then that field will be dropped from the df
    """
    
    import pandas as pd
    import numpy as np
    
    print("\nRemoval of Low Variance Fields\n")
        
    if columns =='all':
        var_list = df.columns.tolist()
        print('\nWill examine all variables as candidate for removal')
        
    else:
        var_list = columns
        print('\nWill examine the following variables as candidates for removal: {var_list}')
        
    #Do not remove dv outcome
    if dv != None:
        var_list.remove(dv)
        
    removal_list = []

    #Loop through each column. This is slower than all at once but processing the entire df at once is very memory intensive
    for v in var_list:
        #Get levels of variable
        lvls = pd.DataFrame(df[v].value_counts(normalize=True, sort=True, ascending=False, dropna=False))
        
        #print('here')
        #print(lvls)
        #print(lvls.iloc[0][0])
        #Select highest freq and drop if exceeds threshold
        if lvls.iloc[0][0] > threshold:
            
            if verbose == True:
                print(f'In field {v}, the value {lvls.index[0]} accounts for {lvls.iloc[0][0]*100}% of the values and the column will be dropped.')
            removal_list.append(v)
    
    print(f'{len(removal_list)} fields removed due to low variance')
    
    if removal_list:
        if inplace==True:

            df.drop(columns=removal_list, inplace=True)

            return

        else:
            new_df = df.drop(columns=removal_list, inplace=False)

            return new_df    
    
    
def dv_proxies(df, dv, threshold=.8, inplace=False):
    
    import pandas as pd
    import numpy as np
    
    
    corrs = df.corr(method='pearson')[dv]
    corrs = pd.DataFrame(corrs.dropna().drop([dv], axis=0))
    corrs = corrs[corrs[dv] > threshold].index.to_list()
    
    print(corrs)
    
    if inplace==True:
        df.drop(columns=corrs, inplace=True)
        
        return
    
    else:
        new_df = df.drop(columns=corrs, inplace=False)
    
        return new_df
    
def correlation_reduction(df=None, dv=None, threshold = 0.90, inplace=True, verbose=True):
    
    import pandas as pd
    import numpy as np
    
    corrs = df.drop([dv], axis = 1).corr()
    
    #Drop repeats by just selecting the upperhalf of the matrix
    upper = pd.DataFrame(np.triu(np.ones(corrs.shape)).astype('bool').reshape(corrs.size), columns=['to_keep'])
    corrs = corrs.stack().reset_index()
    corrs = pd.concat([corrs, upper], axis=1)
    corrs = corrs[corrs['to_keep'] == True]
    corrs.drop(columns=['to_keep'], inplace=True)
    corrs.columns = ['var1', 'var2', 'corr']
    
    #Drop self-correlations 
    corrs = corrs[corrs['var1'] != corrs['var2']]
    
    #Sort by highest correlations
    corrs['abs_corr'] = np.abs(corrs['corr'])
    corrs.sort_values(by = ['abs_corr'], ascending = False, inplace = True)
    corrs = corrs[corrs['abs_corr'] > threshold]
    
    #Drop Var2
    if verbose == True:
        print(f'Variables to be dropped:\n{corrs.var2.unique()}')
    else:
        print(f'{corrs.var2.nunique()} variables will be dropped')
    
    if inplace==True:
        df.drop(columns=corrs.var2.unique(), inplace=True)
        
        return
    
    else:
        new_df = df.drop(columns=corrs.var2.unique(), inplace=False)

        return new_df
