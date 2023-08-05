class ExperimentDecision:
    def __init__(self, variation, reason):
        self.variation = variation
        self.reason = reason

    def __eq__(self, o):
        return self.variation == o.variation and self.reason == o.reason

    def __ne__(self, o):
        return not self.__eq__(o)

    def __str__(self):
        return '(variation={}, reason={})'.format(self.variation, self.reason)

    def __repr__(self):
        return self.__str__()


class FeatureFlagDecision:
    def __init__(self, is_on, reason):
        self.is_on = is_on
        self.reason = reason

    def __eq__(self, o):
        return self.is_on == o.is_on and self.reason == o.reason

    def __ne__(self, o):
        return not self.__eq__(o)

    def __str__(self):
        return '(is_on={}, reason={})'.format(self.is_on, self.reason)

    def __repr__(self):
        return self.__str__()


class DecisionReason(object):
    SDK_NOK_READY = 'SDK_NOK_READY'
    EXCEPTION = 'EXCEPTION'
    INVALID_INPUT = 'INVALID_INPUT'

    EXPERIMENT_NOT_FOUND = 'EXPERIMENT_NOT_FOUND'
    EXPERIMENT_DRAFT = 'EXPERIMENT_DRAFT'
    EXPERIMENT_PAUSED = 'EXPERIMENT_PAUSED'
    EXPERIMENT_COMPLETED = 'EXPERIMENT_COMPLETED'
    OVERRIDDEN = 'OVERRIDDEN'
    TRAFFIC_NOT_ALLOCATED = 'TRAFFIC_NOT_ALLOCATED'
    TRAFFIC_ALLOCATED = 'TRAFFIC_ALLOCATED'
    VARIATION_DROPPED = 'VARIATION_DROPPED'
    NOT_IN_EXPERIMENT_TARGET = 'NOT_IN_EXPERIMENT_TARGET'

    FEATURE_FLAG_NOT_FOUND = 'FEATURE_FLAG_NOT_FOUND'
    FEATURE_FLAG_INACTIVE = 'FEATURE_FLAG_INACTIVE'
    INDIVIDUAL_TARGET_MATCH = 'INDIVIDUAL_TARGET_MATCH'
    TARGET_RULE_MATCH = 'TARGET_RULE_MATCH'
    DEFAULT_RULE = 'DEFAULT_RULE'
