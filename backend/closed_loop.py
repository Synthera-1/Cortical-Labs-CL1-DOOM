import numpy as np
import cv2
from vizdoom_env import VizDoomEnv
import yaml

class ClosedLoopAgent:
    def __init__(self, cfg_path):
        self.env = VizDoomEnv(cfg_path)
        self.env.initialize()
        # Load encoding & decoding templates
        with open("encoding.yaml") as f:
            self.encoding = yaml.safe_load(f)
        with open("decoding.yaml") as f:
            self.decoding = yaml.safe_load(f)

    def encode_state(self, features):
        """Turn game state into stimulation pattern."""
        stim_pattern = np.zeros(59)
        for key, val in self.encoding.items():
            if features.get(key):
                stim_pattern[val['electrodes']] = val['frequency']
        return stim_pattern

    def decode_spikes(self, spikes):
        """Convert spike output to game action."""
        template_scores = {}
        for action, tmpl in self.decoding['templates'].items():
            electrodes = tmpl['electrodes']
            template_scores[action] = spikes[electrodes].sum()
        return max(template_scores, key=template_scores.get)

    def step(self):
        # 1. Get feature state
        features = self.env.get_feature_state()
        # 2. Encode -> stimulate neurons
        stim = self.encode_state(features)
        spikes = self.env.send_stim(stim)
        # 3. Decode spikes -> action
        action = self.decode_spikes(spikes)
        # 4. Execute action
        frame = self.env.make_action(action)
        return frame, spikes, action
