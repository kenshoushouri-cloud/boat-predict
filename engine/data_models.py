class Boat:
    def __init__(
        self,
        number,
        name,
        st,
        win_rate,
        motor,
        boat,
        local_win_rate,
        course_stats,
        accident_rate
    ):
        self.number = number
        self.name = name

        # 元データ
        self.st = st
        self.win_rate = win_rate
        self.motor = motor
        self.boat = boat
        self.local_win_rate = local_win_rate
        self.course_stats = course_stats
        self.accident_rate = accident_rate

        # scoring.py が要求する属性
        self.motor_score = 0
        self.boat_score = 0
        self.local_score = 0
        self.course_score = 0

        # scoring.py が参照する属性
        self.avg_st = st
        self.player_id = number
        self.pair_stats = {}

    def __repr__(self):
        return f"Boat({self.number}, {self.name})"


class Race:
    def __init__(self, race_id, boats, metadata=None):
        """
        race_id: レースID（例: '20240324_尼崎_1R'）
        boats: Boat オブジェクトのリスト（6艇）
        metadata: 開催場、天候、風、波などの追加情報（任意）
        """
        self.race_id = race_id
        self.boats = boats  # list[Boat]
        self.metadata = metadata or {}

        # scoring.py が参照する可能性のある属性
        self.course_stats = {}     # コース別統計（任意）
        self.race_info = {}        # レース情報（任意）

    def __repr__(self):
        return f"Race({self.race_id}, boats={len(self.boats)})"
