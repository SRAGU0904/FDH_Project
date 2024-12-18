import openai
import pandas as pd
import numpy as np

def PerformTranslation(df, col):

    # Set the translation type, which will be nested into the system content.
    translation_type = col

    # Collect all data in the type of str, delete the int data
    df_totran = df[df[col].apply(lambda x: isinstance(x, str))]

    # Select the data without '|'
    df_NotCon = df_totran[~df_totran[col].str.contains('|', na=False, regex=False)]
    NotCon_list = df_NotCon[col].dropna().unique().tolist()

    # Divide the data with '|'
    df_Con = df_totran[df_totran[col].str.contains('|', na=False, regex=False)]
    if df_Con.shape[0] > 0:
        df_Con['divided'+col] = df_Con[col].apply(lambda x: x.split(' | '))
        Con_list = df_Con['divided'+col].sum()
        Con_list = list(set(Con_list))
    else:
        Con_list = []

    # Delete '-'
    Con_list = list(filter(lambda x: x != '-', Con_list))

    # Merge NotCon_list and Con_list
    unique_list = NotCon_list + Con_list
    unique_list = list(set(unique_list))
    print("The unique data need to be translated is: {}".format(len(unique_list)))

    # Set the system content
    system_content = "You are a helpful translator. I am currently translating {} related to ancient Venetian land and leases. \
                    I will send you text in Italian, and I would like you to translate it into English. \
                    Please make sure to only return the translated content, with no additional information.\
                    The translation should be output in lowercase.".format(translation_type)

    # Set the response list
    responses = []

    # Set the input list
    user_inputs = unique_list

    # Translate each input with gpt-4 model
    for user_input in user_inputs:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_input}
            ]
        )
        responses.append(response)

    # Save translated values
    translated_values = []
    for i in range(len(responses)):
        translated_values.append(responses[i]['choices'][0]['message']['content'])

    translated_dict = dict(zip(unique_list, translated_values))
    translated_df = pd.DataFrame(list(translated_dict.items()), columns=['Key', 'Value'])
    translated_df.columns = ['origin','translation']
    return translated_df


if __name__ == "__main__":

    # Load the original dataset
    df = pd.read_json("Data//1740_Catastici//catastici_text_data_20240924.json",encoding="utf-8", orient='records')
    # Fill all 'nan' and '' with np.null
    df.replace(['nan', ''], np.nan, inplace=True)

    # Select all the columns need to be translated
    column_list = ['owner_entity_group','owner_title_std','owner_mestiere_std','function','quality_income','combine_quanlity_quantity_income']
    df_totran = df[column_list]

    # Set api key
    openai.api_key = ""
    # Perform translation for each column
    for col in column_list:
        translated_df = PerformTranslation(df, col)
        saved_path = "..//C_translation//C_{}.csv".format(col)
        translated_df.to_csv(saved_path,index=False,encoding='utf-8-sig')