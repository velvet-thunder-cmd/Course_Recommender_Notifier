import boto3
import time 
import json
import pandas as pd
import neattext.functions as nfx
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity,linear_kernel
def lambda_handler(event, context):
    mm=event.pop(0)
    data=pd.DataFrame.from_dict(event, orient='columns') 
    data['CourseName'] = data['Name'].apply(nfx.remove_stopwords)
    data['sections_new'] = data['sections'].apply(nfx.remove_special_characters)
        # Vectorize our Text
    count_vect = CountVectorizer()
    cv_mat = count_vect.fit_transform(data['sections_new'])
        # Dense
    cv_mat.todense()
        
    words = pd.DataFrame(cv_mat.todense(),columns=count_vect.get_feature_names())
    cosine_sim_mat = cosine_similarity(words)
    course_indices = pd.Series(data.index,index=data['Name']).drop_duplicates()
    def recommend_course(title,num_of_rec=10):
            # ID for title
        idx = course_indices[title]
            # Course Indice
            # Search inside cosine_sim_mat
        scores = list(enumerate(cosine_sim_mat[idx]))
            # Scores
            # Sort Scores
        sorted_scores = sorted(scores,key=lambda x:x[1],reverse=True)
            # Recomm
        selected_course_indices = [i[0] for i in sorted_scores[1:]]
        selected_course_scores = [i[1] for i in sorted_scores[1:]]
        result = data['Name'].iloc[selected_course_indices]
        rec_df = pd.DataFrame(result)
        rec_df['similarity_scores'] = selected_course_scores
        return rec_df.head(num_of_rec)
    b=recommend_course(mm["names"],2)
    return json.dumps(json.loads(b.to_json(orient="records")))
