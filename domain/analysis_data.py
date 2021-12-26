class AnalysisData:

    def __init__(self, count, count_positive: int, count_negative: int, count_neutral: int, count_mixed: int,
                 positive_pc: int, negative_pc: int, neutral_pc: int):
        self.count = count
        self.count_positive = count_positive
        self.count_negative = count_negative
        self.count_neutral = count_neutral
        self.count_mixed = count_mixed
        self.positive_pc = positive_pc
        self.negative_pc = negative_pc
        self.neutral_pc = neutral_pc
