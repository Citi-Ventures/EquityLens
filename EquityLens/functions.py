#############################      Equity Lens     #############################
#                                                                              #
# This file includes the functions that use in Equity Lens                     #
#                                                                              #
################################################################################

import numpy as np
import pandas as pd
import re
import warnings
import statistics
from prettytable import PrettyTable
from IPython.display import display_markdown
warnings.filterwarnings("ignore", category=FutureWarning)


def custom_formatwarning(msg, *args, **kwargs):
    # ignore everything except the message
    return str(msg) + '\n'

def read_data(data_name, token):
    import pandas as pd
    if data_name == 'dii':
       return pd.read_csv('https://raw.githubusercontent.com/Citi-Ventures/EquityLens/main/EquityLens/datasets/dii_2020.csv?token={token}'.format(token=token))
    elif data_name == 'german':
      return pd.read_csv('https://raw.githubusercontent.com/Citi-Ventures/EquityLens/main/EquityLens/datasets/dii_2020.csv?token={token}'.format(token=token))
    else:
      print('Data not found!')



# color the score, lower than 50: red, otherwise green
def color_it(sta):
    if sta > 50: return "\033[1;32m%s\033[0m" %sta
    else: return "\033[1;31m%s\033[0m" %sta 

def compute_hhi(var_list):
    total = sum(var_list)
    hhi_elements = [(i/total)**2 for i in var_list]
    return sum(hhi_elements)


# Evaluate company's (company name or stock code) DEI efforts in three dimensions
def company_dei_score(company_name, token):
  dii = read_data('dii', token)
  dii['company_name_lower'] = dii['company_name'].str.lower()
  company_name = company_name.lower()
  count_com = dii['company_name_lower'].str.contains(company_name).sum()
  if count_com > 0:
    if count_com == 1:
      company_index = (dii.loc[dii['company_name_lower'].str.contains(company_name)].index).tolist()[0]
      

      display_markdown('''## {} 
      Diversity and Inclusion Index, 1-100:'''.format(dii.loc[company_index, 'company_name']),  raw=True)

      t = PrettyTable(['', 'Score'])
      t.align[""] = "l"
      t.add_row(['DEI', color_it(int(dii['p_DII'][company_index]*100)) ])
      t.add_row(['Gender Diversity', color_it(int(dii['p_hhi_count_gender'][company_index]*100))])
      t.add_row(['Racial Diversity', color_it(int(dii['p_hhi_count_race'][company_index]*100))])
      t.add_row(['Gender Attrition Inclusion', color_it(int(dii['p_std_attrition_gender'][company_index]*100))])
      t.add_row(['Racial Attrition Inclusion', color_it(int(dii['p_std_attrition_race'][company_index]*100))])
      t.add_row(['Gender Resource Disparity', color_it(int(dii['p_cv_salary_gender'][company_index]*100))])
      t.add_row(['Racial Resource Disparity', color_it(int(dii['p_cv_salary_race'][company_index]*100))])
      print(t)
    else:
      display_markdown('''## Choose the exact name of the company and try again:\n''',  raw=True)
      display(dii[dii['company_name_lower'].str.contains(company_name)]['company_name'].to_list())
  else:
      #display_markdown('''## Company not found!''',  raw=True)
      warnings.formatwarning = custom_formatwarning
      warnings.warn("Company not found!")

# Evaluate data sample representation
def sample_dei_score(company_list, token):
  dii = read_data('dii', token)
  # inner merge company_list to dii master dataset
  new_list = pd.DataFrame({'stock_code': company_list})
  master = dii.merge(new_list, how='inner', on='stock_code')
  median_scores = master.median()


  display_markdown('''### Diversity and Inclusion Median Scores, 1-100:''',  raw=True)

  t = PrettyTable(['', 'Score'])
  t.align[''] = "l"
  #t.add_row(['DEI', color_it(int(median_scores[0]*100))])
  t.add_row(['Gender Diversity', color_it(int(median_scores[1]*100))])
  t.add_row(['Racial Diversity', color_it(int(median_scores[4]*100))])
  t.add_row(['Gender Attrition Inclusion', color_it(int(median_scores[2]*100))])
  t.add_row(['Racial Attrition Inclusion', color_it(int(median_scores[5]*100))])
  t.add_row(['Gender Resource Disparity', color_it(int(median_scores[3]*100))])
  t.add_row(['Racial Resource Disparity', color_it(int(median_scores[6]*100))])
  print(t)


# Compute DEI scores - variety
# dataset: representations
# input: numeric columns contains the counts between groups (gender or racial)
# variety: hhi;  separation: std; disparity: cv
def compute_score(var_list, dii_type, industry, token):
  dii = read_data('dii', token)

  # lower HHI, more diversity!
  if dii_type == 'variety':
    return compute_hhi(var_list) 
  # lower std, less difference
  elif dii_type == 'separation':
    return statistics.stdev(var_list) 
  # Coefficient of Variation
  elif dii_type == 'disparity':
    return statistics.stdev(var_list)/ (sum(var_list)/len(var_list))
  else:
    warnings.formatwarning = custom_formatwarning
    warnings.warn("DII type incorrect!")


def counterfactual_transformation(feature, favor, premuium_swap,df):
  # calculate the diff
  diff = df[df['sex'] == favor][feature].mean() - df[df['sex'] != favor][feature].mean()
  new_feature = []
  
  for i in range(len(df)):
    # if unfavor group and lower than favor group's median, change to median
    if premuium_swap == 'premuium':
      if df['sex'][i] != favor:
          new_feature.append(df[feature][i]+diff)
      else:
        new_feature.append(df[feature][i])
  return new_feature

def top_10(protected,features,df):
    from sklearn.preprocessing import StandardScaler
    import math
    import numpy as np
    from scipy import stats

    # protected:sex
    #protected = 'sex'

    # standardization 
    df_new = df[[protected]+ features]
    df_new[features] = StandardScaler().fit_transform(df_new[features])
    results = np.zeros(len(features))
    i = 0

    for feature in features:
      _, p_val = stats.ttest_ind(df_new[df_new[protected] == 1][feature],df_new[df_new[protected] == 0][feature], equal_var=False)
      if p_val <= 0.05: 
        results[i] = abs(df_new[df_new[protected] == 0][feature].mean() - df_new[df_new[protected] == 1][feature].mean())
      else:
        results[i] = 0
      i = i + 1

    d = {'feature': features, 'mean': results}
    result_df = pd.DataFrame(data=d)
    result_df.sort_values('mean', ascending=False,ignore_index=True, inplace=True)
    n = math.ceil(len(features)*0.1)
    print('Most differences in {}'.format(protected),'come from:\n\n', 
          result_df['feature'][:n].to_string(index=False))
    return result_df.head(n)

# favor group: the one with favor outcome: good credit
# label: 2 is bad , 1 is good
def Equity_Lens(protected, features,df):
  import warnings
  from scipy import stats
  warnings.filterwarnings("ignore", category=FutureWarning)
  _, p_val = stats.ttest_ind(df[df[protected] == 1]['label'],df[df[protected] == 0]['label'], equal_var=False)
  if df[df[protected] == 0]['label'].mean() < df[df[protected] == 0]['label'].mean(): favor = 0
  else: favor = 1

  new_features = {}
  if p_val <= 0.05:
    print('The differences in {} are significant'.format(protected))
  
    # 1. predict 10% variable list
    result_df = top_10(protected,features, df)
    
    # 2. counterfactual_transformation
    for i in range(len(result_df)):
              feature = result_df['feature'][i]
              new_features[feature+'_new'] = counterfactual_transformation(feature, favor, 'premuium', df)
            
  return new_features

def ttest_var(group_var, feature,df):
      from scipy import stats
      _, p_val = stats.ttest_ind(df[df[group_var] == 1][feature],df[df[group_var] == 0][feature], equal_var=False)
      diff = df[df[group_var] == 1][feature].mean() - df[df[group_var] == 0][feature].mean()
      #print("ttest_ind_from_stats:  p-value = %g" % ( round(p_val,2)),  '\nDiff:', round(diff))
      return p_val, diff
