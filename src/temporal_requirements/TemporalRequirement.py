import uuid


class TemporalRequirement:
    def __init__(self, temporal_expression):
        self.id = uuid.uuid4()
        self.temporal_expression = temporal_expression
        self._scope = None
        self._activities = []
        self._has_conditional_clause = None
        self._reference_time = None
        self._process_signal = None
        self._is_negation_clause = None

    def __repr__(self):
        content = str(self.temporal_expression)
        if self._scope:
            content = content + "\n" + "Scope: " + str(self._scope)

        if self._activities:
            content = content + "\n" + "Activities: " + str(self._activities)

        if self._has_conditional_clause:
            content = content + "\n" + "Conditional Clause: " + str(self._has_conditional_clause)

        if self._reference_time:
            content = content + "\n" + "Reference Time: " + str(self._reference_time)

        if self._process_signal:
            content = content + "\n" + "Process Signals: " + str(self._process_signal)

        if self._is_negation_clause:
            content = content + "\n" + "Is Negation Clause: " + str(self._is_negation_clause)
        return content

    @property
    def scope(self):
        return self._scope

    @scope.setter
    def scope(self, scope):
        self._scope = scope

    @property
    def activities(self):
        return self._activities

    @activities.setter
    def activities(self, activities):
        self._activities = activities

    @property
    def has_conditional_clause(self):
        return self._has_conditional_clause

    @has_conditional_clause.setter
    def has_conditional_clause(self, has_conditional_clause):
        self._has_conditional_clause = has_conditional_clause

    @property
    def reference_time(self):
        return self._reference_time

    @reference_time.setter
    def reference_time(self, reference_time):
        self._reference_time = reference_time

    @property
    def process_signal(self):
        return self._process_signal

    @process_signal.setter
    def process_signal(self, process_signal):
        self._process_signal = process_signal
