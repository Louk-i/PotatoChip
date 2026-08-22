from typing import Dict, Tuple
from config.data.emotions import (
    INITIAL_GAUGE_VALUE,
    OVERFLOW_THRESHOLD,
    CASCADE_DISTRIBUTION_VALUE,
    STAGE_2_THRESHOLD,
    STAGE_3_THRESHOLD,
)

EMOTION_STAGES = {
    "happy": {
        1: "Happy",
        2: "Ecstatic",
        3: "Manic"
    },
    "sad": {
        1: "Sad",
        2: "Miserable",
        3: "Depressed"
    },
    "angry": {
        1: "Angry",
        2: "Frustrated",
        3: "Furious"
    },
    "fear": {
        1: "Fear",
        2: "Dreadful",
        3: "Petrified"
    },
    "quiet": {
        1: "Quiet",
        2: "Reserved",
        3: "Silent"
    },
    "loud": {
        1: "Loud",
        2: "Brash",
        3: "Obstreperous"
    },
}

TIE_BREAKER_PRIORITY = ["happy", "sad", "angry", "quiet", "loud", "fear"]

class EmotionEngine:
    def __init__(self):
        # init
        self.gauges: Dict[str, int] = {
            "happy": INITIAL_GAUGE_VALUE,
            "sad": INITIAL_GAUGE_VALUE,
            "angry": INITIAL_GAUGE_VALUE,
            "fear": INITIAL_GAUGE_VALUE,
            "quiet": INITIAL_GAUGE_VALUE,
            "loud": INITIAL_GAUGE_VALUE,
        }

    def _resolve_overflows(self):
        """continuous loops recursion to handle chain reactions"""
        while True:
            overflowing = [emo for emo, val in self.gauges.items() if val > 100]
            
            if not overflowing:
                break
            for emo in overflowing:
                if self.gauges[emo] > OVERFLOW_THRESHOLD:
                    self.gauges[emo] = INITIAL_GAUGE_VALUE
                    
                    for other_emo in self.gauges:
                        if other_emo != emo:
                            self.gauges[other_emo] += 15

    def set_gauge(self, emotion: str, value: int):
        if emotion in self.gauges:
            self.gauges[emotion] = max(0, value)
            self._resolve_overflows()

    def adjust_gauge(self, emotion: str, delta: int):
        if emotion in self.gauges:
            self.set_gauge(emotion, self.gauges[emotion] + delta)

    def _get_stage_level(self, gauge_val: int) -> int:
        if gauge_val >= STAGE_3_THRESHOLD:
            return 3
        elif gauge_val >= STAGE_2_THRESHOLD:
            return 2
        return 1

    def get_dominant_emotion(self) -> Tuple[str, str, int]:
        dominant_category = min(
            self.gauges.keys(), 
            key=lambda k: (-self.gauges[k], TIE_BREAKER_PRIORITY.index(k))
        )
        
        gauge_val = self.gauges[dominant_category]
        stage_level = self._get_stage_level(gauge_val)
        stage_name = EMOTION_STAGES[dominant_category][stage_level]
        
        return dominant_category, stage_name, stage_level

emotion_engine = EmotionEngine()