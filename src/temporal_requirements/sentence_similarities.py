#
# This file is part of QTCR-VERIFICATOR.
#
# QTCR-VERIFICATOR is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your
# option) any later version.
#
# QTCR-VERIFICATOR is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with QTCR-VERIFICATOR (file COPYING in the main directory). If not, see
# http://www.gnu.org/licenses/.

import numpy as np

# It returns the similarity measured by F1
from bert_score import BERTScorer
from src.helpers import load_transformers, clean_text

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
