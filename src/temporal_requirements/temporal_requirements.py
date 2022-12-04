from src.enums import ProcessElementScope, Conditional, Signal, ReferenceTime, TimeType, ActivityType
from src.event_logs.Log import Log
from src.helpers import get_unique_values, get_all_sentences
from src.temporal_expressions import temporal_expressions

from src.temporal_requirements.Activity import Activity
from src.temporal_requirements.TemporalRequirement import TemporalRequirement
from src.temporal_requirements.sentence_similarities import get_sentence_similarities

IN_KEYWORDS = [' in ', ' on ', ' by ', ' at ']
BEFORE_KEYWORDS = [' until ', ' before ', ' not later than ', ' prior to ']
AFTER_KEYWORDS = [' after ', ' from ']
ALL_KEYWORDS = IN_KEYWORDS + BEFORE_KEYWORDS + AFTER_KEYWORDS


def has_conditional_clause(original_sentence):
    if 'if' in original_sentence:
        return Conditional.Conditional.IF
    if 'otherwise' in original_sentence:
        return Conditional.Conditional.OTHERWISE
    return Conditional.Conditional.NONE


def get_process_element_scope(original_sentence, process_description_name, is_conditional, reference_time):
    process_description_name = process_description_name.lower().replace('_', ' ') + ' process'
    if process_description_name in original_sentence:
        return ProcessElementScope.ProcessElementScope.WHOLE_PROCESS
    if reference_time is ReferenceTime.ReferenceTime.ACTIVITY:
        return ProcessElementScope.ProcessElementScope.ACTIVITY_SET
    if is_conditional is not Conditional.Conditional.NONE or ' and ' in original_sentence or reference_time is ReferenceTime.ReferenceTime.ACTIVITY:
        return ProcessElementScope.ProcessElementScope.ACTIVITY_SET
    return ProcessElementScope.ProcessElementScope.SINGLE_ACTIVITY


def get_signals_in_range(original_sentence, annotated_time, time_type):
    if time_type is TimeType.TimeType.SET:
        return Signal.Signal.EACH
    signal_from = get_signals_range(original_sentence, annotated_time)[0]
    signal_to = get_signals_range(original_sentence, annotated_time)[1]
    if any(s in original_sentence[signal_from:signal_to] for s in IN_KEYWORDS):
        return Signal.Signal.IN
    if any(s in original_sentence[signal_from:signal_to] for s in BEFORE_KEYWORDS):
        return Signal.Signal.BEFORE
    if any(s in original_sentence[signal_from:signal_to] for s in AFTER_KEYWORDS):
        return Signal.Signal.AFTER
    return Signal.Signal.IN


def get_signals(original_sentence, time_type):
    if time_type is TimeType.TimeType.SET:
        return Signal.Signal.EACH
    if any(s in original_sentence for s in IN_KEYWORDS):
        return Signal.Signal.IN
    if any(s in original_sentence for s in BEFORE_KEYWORDS):
        return Signal.Signal.BEFORE
    if any(s in original_sentence for s in AFTER_KEYWORDS):
        return Signal.Signal.AFTER
    return Signal.Signal.IN


def get_position_first_character_after_time(original_sentence, annotated_time):
    annotated_time_position = original_sentence.find(annotated_time) + len(annotated_time)
    return annotated_time_position


def get_signals_range(original_sentence, annotated_time):
    first_character_after_time = get_position_first_character_after_time(original_sentence, annotated_time)
    signal_from = first_character_after_time - len(annotated_time) - 20
    if signal_from < 0:
        signal_from = 0
    signal_to = first_character_after_time + 20
    if signal_to < 0:
        signal_to = len(original_sentence)
    return [signal_from, signal_to]


def get_reference_activity(original_sentence, annotated_time):
    reference_time_activity = original_sentence[
                              get_position_first_character_after_time(original_sentence, annotated_time):len(
                                  original_sentence)]
    reference_time_activity = ' '.join(word for word in reference_time_activity.split() if word not in ALL_KEYWORDS)
    if 'each' in reference_time_activity:
        reference_time_activity = reference_time_activity.replace('each', '')
        reference_time_activity = reference_time_activity.split('to')[0]
    return reference_time_activity.split(',')[0]


def get_reference_time(original_sentence, time_type, annotated_time):
    if get_time_type(time_type) is TimeType.TimeType.DURATION:
        if ',' not in original_sentence[get_position_first_character_after_time(original_sentence, annotated_time)]:
            len(original_sentence) - 1
            return ReferenceTime.ReferenceTime.ACTIVITY
    return ReferenceTime.ReferenceTime.STARTING_FIRST_ACTIVITY


def remove_signal(original_sentence):
    if any(s in original_sentence for s in ('in', 'on', 'by', 'at')):
        return Signal.Signal.IN
    if any(s in original_sentence for s in ('until', 'before', 'not later than', 'prior to')):
        return Signal.Signal.BEFORE
    if any(s in original_sentence for s in ('after', 'from')):
        return Signal.Signal.AFTER
    return Signal.Signal.NONE


def get_time_type(time_type):
    if 'DATE' in time_type:
        return TimeType.TimeType.DATE
    if 'TIME' in time_type:
        return TimeType.TimeType.TIME
    if 'DURATION' in time_type:
        return TimeType.TimeType.DURATION
    if 'SET' in time_type:
        return TimeType.TimeType.SET



def get_temporal_requirements(log_path, process_description_path, process_description_name):
    candidate_activites_sorted_by_similarity = []
    requirements_found = []
    log = Log('', log_path)
    log.set_traces_and_events()
    event_concept_name = []
    for event in log.events:
        event_concept_name.append(event.get_concept_name())

    f = open(process_description_path, 'r')

    unique_event_concept_name = get_unique_values(event_concept_name)
    expressions = temporal_expressions.get_temporal_expressions(get_all_sentences(f), process_description_name)

    for temporal_expression in expressions:
        temporal_requirement = TemporalRequirement(temporal_expression)
        temporal_requirement.has_conditional_clause = has_conditional_clause(temporal_expression.original_sentence)
        temporal_requirement.reference_time = get_reference_time(temporal_expression.original_sentence,
                                                                 temporal_expression.time_type,
                                                                 temporal_expression.annotated_time)
        temporal_requirement.scope = get_process_element_scope(temporal_expression.original_sentence,
                                                               temporal_expression.process_description_name,
                                                               temporal_requirement.has_conditional_clause,
                                                               temporal_requirement.reference_time)

        if temporal_requirement.scope is not ProcessElementScope.ProcessElementScope.WHOLE_PROCESS:
            if temporal_requirement.scope is ProcessElementScope.ProcessElementScope.SINGLE_ACTIVITY:

                found_activities = get_sentence_similarities(unique_event_concept_name,
                                                             temporal_expression.original_sentence.replace(temporal_expression.annotated_time, ''),)
                candidate_activites_sorted_by_similarity.append([found_activities, temporal_expression.original_sentence])
                found_activity = Activity(found_activities[0][0],
                                          found_activities[0][1],
                                          ActivityType.ActivityType.DECLARATIVE,
                                          get_signals_in_range(temporal_expression.original_sentence,
                                                               temporal_expression.annotated_time,
                                                               temporal_expression.time_type))
                temporal_requirement.activities.append(found_activity)
            else:
                if temporal_requirement.reference_time is ReferenceTime.ReferenceTime.ACTIVITY:
                    reference_activity = get_reference_activity(temporal_expression.original_sentence,
                                                                temporal_expression.annotated_time)
                    found_activities = get_sentence_similarities(unique_event_concept_name,
                                                                 reference_activity.replace(temporal_expression.annotated_time, ''),)
                    candidate_activites_sorted_by_similarity.append([found_activities, temporal_expression.original_sentence])
                    found_activity = Activity(found_activities[0][0],
                                              found_activities[0][1],
                                              ActivityType.ActivityType.STARTING_REFERENCE,
                                              get_signals(reference_activity,
                                                          temporal_expression.time_type))
                    temporal_requirement.activities.append(found_activity)
                    referenced_activity = temporal_expression.original_sentence.replace(reference_activity, '')
                    found_activities = get_sentence_similarities(unique_event_concept_name,
                                                                 referenced_activity.replace(temporal_expression.annotated_time, ''),)
                    candidate_activites_sorted_by_similarity.append([found_activities, temporal_expression.original_sentence])
                    found_activity = Activity(found_activities[0][0],
                                              found_activities[0][1],
                                              ActivityType.ActivityType.DECLARATIVE,
                                              get_signals_in_range(referenced_activity,
                                                                   temporal_expression.annotated_time,
                                                                   temporal_expression.time_type))
                    temporal_requirement.activities.append(found_activity)
                    if ' and ' in referenced_activity:
                        found_activity = Activity(found_activities[1][0],
                                                  found_activities[1][1],
                                                  ActivityType.ActivityType.DECLARATIVE,
                                                  get_signals_in_range(referenced_activity,
                                                                       temporal_expression.annotated_time,
                                                                       temporal_expression.time_type))
                        temporal_requirement.activities.append(found_activity)
                elif temporal_requirement.has_conditional_clause is not Conditional.Conditional.NONE:
                    split_by = 'otherwise'
                    if temporal_requirement.has_conditional_clause is Conditional.Conditional.IF:
                        split_by = ','
                    condition_activity = str(temporal_expression.original_sentence.split(split_by)[0])
                    found_activities = get_sentence_similarities(unique_event_concept_name,
                                                                 condition_activity.replace(temporal_expression.annotated_time, ''),)
                    candidate_activites_sorted_by_similarity.append([found_activities, temporal_expression.original_sentence])
                    found_activity = Activity(found_activities[0][0],
                                              found_activities[0][1],
                                              ActivityType.ActivityType.CONDITION,
                                              get_signals_in_range(condition_activity,
                                                                   temporal_expression.annotated_time,
                                                                   temporal_expression.time_type))
                    temporal_requirement.activities.append(found_activity)
                    consequence_activity = str(temporal_expression.original_sentence.split(split_by)[1])

                    found_activities = get_sentence_similarities(unique_event_concept_name,
                                                                 consequence_activity.replace(temporal_expression.annotated_time, ''),)
                    candidate_activites_sorted_by_similarity.append([found_activities, temporal_expression.original_sentence])
                    found_activity = Activity(found_activities[0][0],
                                              found_activities[0][1],
                                              ActivityType.ActivityType.CONSEQUENCE,
                                              get_signals_in_range(consequence_activity,
                                                                   temporal_expression.annotated_time,
                                                                   temporal_expression.time_type))
                    temporal_requirement.activities.append(found_activity)
                    if ' and ' in consequence_activity:
                        found_activity = Activity(found_activities[1][0],
                                                  found_activities[1][1],
                                                  ActivityType.ActivityType.CONSEQUENCE,
                                                  get_signals_in_range(consequence_activity,
                                                                       temporal_expression.annotated_time,
                                                                       temporal_expression.time_type))
                        temporal_requirement.activities.append(found_activity)
                else:
                    found_activities = get_sentence_similarities(unique_event_concept_name,
                                                                 temporal_expression.original_sentence)
                    found_activity = Activity(found_activities[0][0],
                                              found_activities[0][1],
                                              ActivityType.ActivityType.DECLARATIVE,
                                              get_signals_in_range(temporal_expression.original_sentence,
                                                                   temporal_expression.annotated_time,
                                                                   temporal_expression.time_type))
                    candidate_activites_sorted_by_similarity.append([found_activities, temporal_expression.original_sentence])
                    temporal_requirement.activities.append(found_activity)
                    if ' and ' in temporal_expression.original_sentence:
                        found_activity = Activity(found_activities[1][0],
                                                  found_activities[1][1],
                                                  ActivityType.ActivityType.DECLARATIVE,
                                                  get_signals_in_range(temporal_expression.original_sentence,
                                                                       temporal_expression.annotated_time,
                                                                       temporal_expression.time_type))
                        temporal_requirement.activities.append(found_activity)

        else:
            temporal_requirement.process_signal = get_signals_in_range(temporal_expression.original_sentence,
                                                                       temporal_expression.annotated_time,
                                                                       temporal_expression.time_type)
        requirements_found.append(temporal_requirement)

    return candidate_activites_sorted_by_similarity


def main():
    print()


if __name__ == '__main__':
    main()
