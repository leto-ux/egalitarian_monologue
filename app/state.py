import colorsys
import threading
import time


class SpeakerState:
    def __init__(self, num_speakers: int):
        self.num_speakers = num_speakers
        self.colors = self._generate_colors(num_speakers)
        self.speaker_map = {}
        self.smoothed_scores = {}
        self.lock = threading.Lock()
        self.alpha = 0.1
        
    def _generate_colors(self, n):
        colors = []
        for i in range(n):
            hue = i / n
            rgb = colorsys.hsv_to_rgb(hue, 0.7, 0.95)
            colors.append([int(c * 255) for c in rgb])
        return colors

    def update(self, prediction):
        with self.lock:
            current_chunk_activity = {}
            
            for segment, _, label in prediction.itertracks(yield_label=True):
                current_chunk_activity[label] = current_chunk_activity.get(label, 0.0) + segment.duration
            
            for label in current_chunk_activity:
                if label not in self.speaker_map:
                    self.speaker_map[label] = len(self.speaker_map) % self.num_speakers

            all_known_labels = set(self.smoothed_scores.keys()) | set(current_chunk_activity.keys())
            
            for label in all_known_labels:
                current_val = current_chunk_activity.get(label, 0.0)
                prev_val = self.smoothed_scores.get(label, 0.0)
                
                new_val = prev_val * (1 - self.alpha) + current_val * self.alpha
                
                if new_val < 0.001:
                    if label in self.smoothed_scores:
                        del self.smoothed_scores[label]
                else:
                    self.smoothed_scores[label] = new_val

    def get_visualization_data(self):
        with self.lock:
            total_weight = sum(self.smoothed_scores.values())
            data = []
            
            if total_weight < 0.01:
                return []

            for label, score in self.smoothed_scores.items():
                color_idx = self.speaker_map.get(label, 0)
                color = self.colors[color_idx]
                percentage = score / total_weight
                data.append({
                    "color": color, 
                    "weight": percentage,
                    "label": label
                })
            
            return data
