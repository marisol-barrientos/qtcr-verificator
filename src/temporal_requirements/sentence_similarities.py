import numpy as np

# It returns the similarity measured by F1
from bert_score import BERTScorer
from src.helpers import load_transformers, clean_text

'''
def remove_temporal_labels(text):
    text = text.replace('wait 7 days','')
    text = text.replace('wait 1 days', '')
    text = text.replace('wait 4 days', '')
    text = text.replace('wait one week or less', '')
    text = text.replace('wait until 1 week before meeting', '')
    return text.replace('wait 23 days', '')
    '''

def get_sentence_similarities(activities, sentence_with_time):
    load_transformers()
    sentence_with_time = clean_text(sentence_with_time)
    clean_sentence_with_time = len(activities) * [sentence_with_time]
    clean_activities = []
    for activity in activities:
        clean_activities.append(clean_text(activity))
    scorer = BERTScorer(lang="en", rescale_with_baseline=True)
    P, R, F1 = scorer.score(clean_activities, clean_sentence_with_time)
    activities_sorted_by_similarity = np.vstack((activities, F1)).T
    activities_sorted_by_similarity = sorted(activities_sorted_by_similarity, key=lambda x: float(x[1]), reverse=True)
    return activities_sorted_by_similarity


def main():
    print()


if __name__ == '__main__':
    main()
