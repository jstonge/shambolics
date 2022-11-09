import argparse
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd


def add_other_as_choice(df, main_col, other_col):
    """If other col, add response as main col choice"""
    new_col = re.findall("^.+?\?", main_col)[0]
    df[new_col] = np.where((df[main_col] == 'Other') | (df[main_col] == 'Fill in the blank:'), df[other_col], df[main_col])
    df = df.drop([main_col, other_col], axis=1)
    return df

def add_other_as_choice_all(df):
    selected_cols = df.loc[:, df.columns.str.contains(' - Selected Choice', case=True, regex=True)].columns
    other_cols = df.loc[:, df.columns.map(lambda x: bool(re.search(' - (Other|Fill in the blank:) - Text', x)))].columns
    for cs,co in zip(selected_cols, other_cols):
        df = add_other_as_choice(df, cs, co)
    return df

def clean_time_expectation_cols(df):
    df["What is your first advisor's main department?"] = np.where(
            df["What is your first advisor's main department?"].isna(),
            df["What is your advisor's main department?"],
            df["What is your first advisor's main department?"]
    )

    df["What is your first advisor's main department?"] = np.where(
        df["What is your first advisor's main department?"].isna(),
        df["What is your advisor's first main department?"],
        df["What is your first advisor's main department?"]
    )

    df['For any of your current projects,, do you think you spend more time than your supervisor expect on programming?'] = np.where(
        df["For any of your current projects,, do you think you spend more time than your supervisor expect on programming?"].isna(),
        df["For any of your current projects,, do you think you spend more time than your first supervisor expect on programming?"],
        df["For any of your current projects,, do you think you spend more time than your supervisor expect on programming?"]
    )

    df['For any of your current projects,, do you think you spend more time than your supervisor expect on programming?'] = np.where(
        df["For any of your current projects,, do you think you spend more time than your supervisor expect on programming?"].isna(),
        df["For any of your current projects,, do you think you spend more time than your first supervisor expect on programming?.1"],
        df["For any of your current projects,, do you think you spend more time than your supervisor expect on programming?"]
    )

    df["What is your second advisor's main department?"] = np.where(
            df["What is your second advisor's main department?"].isna(),
            df["What is your second advisor's main department?.1"],
            df["What is your second advisor's main department?"]
    )

    df['For any of your current projects,, do you think you spend more time than your second supervisor expect on programming?'] = np.where(
        df["For any of your current projects,, do you think you spend more time than your second supervisor expect on programming?"].isna(),
        df["For any of your current projects,, do you think you spend more time than your second supervisor expect on programming?.1"],
        df["For any of your current projects,, do you think you spend more time than your second supervisor expect on programming?"]
    )
    
    df = df.rename(columns={ 
        "What is your first advisor's main department?": "first_adv_dept",
        "For any of your current projects,, do you think you spend more time than your supervisor expect on programming?": "first_adv_expect_time_coding",
        "What is your second advisor's main department?":"second_adv_dept",
        "For any of your current projects,, do you think you spend more time than your second supervisor expect on programming?":"second_adv_expect_time_coding",
        "What is your third advisor's main department?": "third_adv_dept",
        "For any of your current projects,, do you think you spend more time than your third supervisor expect on programming?": "third_adv_expect_time_coding"
    })

    df = df.drop(
        ["What is your second advisor's main department?.1",
         "What is your advisor's main department?", "What is your advisor's first main department?",
         "For any of your current projects,, do you think you spend more time than your first supervisor expect on programming?",
         "For any of your current projects,, do you think you spend more time than your first supervisor expect on programming?.1",
         "For any of your current projects,, do you think you spend more time than your second supervisor expect on programming?.1"
        ], axis=1)

    return df

def clean_colnames(df):
    # deal with duplicated cols (selected vs other choices)
    df = add_other_as_choice_all(df)
    
    # We asked the same question for students and post-docs.
    df['How many advisors do you have?'] = np.where(
        df['How many advisors do you have?.1'].isna(),
         df['How many advisors do you have?'],
         df['How many advisors do you have?.1']
        )
    df = df.drop('How many advisors do you have?.1', axis=1)

    # clean expectation cols
    df = clean_time_expectation_cols(df)

    # clean all other cols
    old_colnames = df.columns.to_list()
    new_colnames = ['start_survey', 'end_survey', 'response_type', 'progress', 'duration_sec', 'is_finished',
                    'record_date', 'response_id', 'distribution_channel', 'user_lang', 'captcha_score',
                    'agree_term', 'academia_status', 'nb_advisors', 'dept_prof', 'dept_students', 
                    'first_line_code', 'years_coding', 'self_id_as_coder', 'read_prog_book', 'freq_oss_proj',
                    'what_os', 'time_cleaning_code', 'time_data_clean_prog', 
                    'time_data_clean_gui', 'time_exp_manip',
                    'time_field_data_coll', 'time_grant_writing', 'time_lit_review', 'time_meeting', 'time_read_doc',
                    'time_digital_data_coll', 'time_paper_writing', 'self_expect_time_coding', 
                    'value_comp_skills_wrt_domain','more_time_learning_to_code', 
                    'first_adv_expect_time_coding', 'first_adv_dept', 'second_adv_dept', 'second_adv_expect_time_coding', 'third_adv_dept', 'third_adv_expect_time_coding',
                    'pct_social_contacts_coding', 'comp_skills_factors_pursue_academia', 'comp_skills_pro_benefits_s',
                    'comp_skills_pro_benefits_p', 'comp_skills_recruiting', 'comp_skills_recruiting_undergrad', 'comp_skills_recruiting_grad',
                    'comp_skills_recruiting_postdoc', 'cite_code', 'cite_data', 'value_oss_license', 
                    'value_coc', 'value_contrib_guide', 'value_cla', 'value_active', 'value_responsive_maintainers',
                    'value_welcoming_community', 'value_widespread_use', 'disadv_not_coding', 'coding_on_future_opportunities', 'value_share_code',
                    'value_accessibility_paper_code', 'value_paper_code_citability', 'value_learn_code_in_field', 'year_born',
                    'country_origin', 'us_state', 'do_del', 'comments', 'score', 'email', 'name_research_group', 'reason_coding',
                    'how_did_you_learn_code', 'position_industry', 'freq_coding_proj', 'use_lang', 'enough_instit_support', 'friends_help',
                    'perceived_benefits_coding', 'do_share_code_online', 'qualities_oss', 'why_not_coding', 'pref_pronouns', 
                    'underrep_group', 'ethnicity']
    
    lookup_cols = {oc: nc for oc, nc in zip(old_colnames, new_colnames)}

    # keep track of renaming
    with open('lookup_col.json', 'w') as f: json.dump(lookup_cols, f)
    
    df = df.rename(columns = lookup_cols)

    return df

def coding(df):
    coding1 = {'Always':1, 'Most of the software': 2, 'Some of the software':3, 'Almost none of the software':4, 'None of the software':5}
    coding2 = {'On every project': 1, 'Most projects': 2, 'Few projects': 3}
    coding3 = {'25 - 34 years': 1, '18 - 24 years':2, '11 - 17 years': 3, '5 - 10 years': 4, 'Prefer not to say': 5}
    coding4 = {'Less than 1 year': 1, '1 to 2 years': 2, '2 to 4 years': 3, '5 to 9 years': 4, '10 to 14 years': 5, 'Prefer not to say': 6}
        
    df['freq_oss_proj_c']    = df.freq_oss_proj.replace(coding1)
    df['freq_coding_proj_c'] = df.freq_coding_proj.replace(coding2)
    df['first_line_code_c']  = df.first_line_code.replace(coding3)
    df['years_coding_c']     = df.years_coding.replace(coding4)
    
    return df

def main():
    ROOT_DIR = Path("..")
    DIR_DAT = ROOT_DIR / 'dat'
    DIR_OUTPUT = ROOT_DIR / 'posts' / 'survey-programming'

    # fname = DIR_DAT / 'survey_2022_10_09.csv'
    fname = DIR_DAT / args.filename

    df = pd.read_csv(fname, skiprows = [0,2])
    
    orig_count = len(df)

    df = clean_colnames(df)

    # rm my incomplete response
    df = df.query('response_id != "R_WCJBP94BGyoMzhn"')

    # cleaning values
    df['is_coder'] = np.where(df['reason_coding'] != 'I  do not know how to code', 'coder', 'non_coder')
    df['year_born'] = pd.to_datetime(df['year_born'], format="%Y").dt.year
    df['dept_students'] = df['dept_students'].str.replace("Complex Systems and Data Science Certificate of Graduate Study, M.S., Ph.D.", "Complex Systems", regex=True)
    df['dept_students'] = df['dept_students'].str.replace("Community Resilience and Planning Certificate of Graduate Study", "Com. Resilience", regex=True)
    df['dept_students'] = df['dept_students'].str.replace("Community Development and Applied Economic", "CDAE", regex=True)
    df['dept_students'] = df['dept_students'].str.replace("Sustainable Development Policy, Economics and Governance Ph.D.", "Sustainable Dev", regex=True)
    df['ethnicity'].str.replace("Southeast Asian,White", "CDAE", regex=True)
    df['academia_status'] = df['academia_status'].str.replace(" student", "", regex=False)
    df['academia_status'] = df['academia_status'].str.replace(" researcher", "", regex=False)
    
    df = coding(df)

    # removing my incomplete response
    df = df.query('progress >= 80')

    # cutoff at 20_000
    new_cut_off = df.query("duration_sec <= 20_000").duration_sec.max()
    df['duration_sec'] = np.where(df.duration_sec >= 20_000, new_cut_off, df.duration_sec)

    with open('comments.txt', 'w') as f:
        [f.write(f'{email} ({id}): {comment}\n') for id, email, comment in zip(df['response_id'], df['email'], df['comments'])]


    df = df.drop(["name_research_group", "email", "comments"], axis=1)

    print(f"We dropped {orig_count - len(df)} respondents.")

    df.to_csv(DIR_OUTPUT / 'data_clean.csv', index=False)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--filename", 
        help="Data should be in dat/."
    )
    args = parser.parse_args()
    main()
