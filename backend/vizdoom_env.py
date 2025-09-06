import vizdoom as vzd
import numpy as np

class VizDoomEnv:
    def __init__(self, cfg_path):
        self.game = vzd.DoomGame()
        self.game.load_config(cfg_path)
        self.game.init()

    def initialize(self):
        # Give pistol by default
        self.game.send_game_command("give weapon pistol")
        self.game.send_game_command("use pistol")

    def get_feature_state(self):
        """Extract enemy/obstacle info for stimulation."""
        # Simplified: vision-based placeholders
        state = {}
        state['enemy_left'] = np.random.choice([True, False], p=[0.5,0.5])
        state['enemy_right'] = np.random.choice([True, False], p=[0.5,0.5])
        state['enemy_center'] = np.random.choice([True, False], p=[0.5,0.5])
        state['wall_ahead'] = np.random.choice([True, False], p=[0.3,0.7])
        return state

    def send_stim(self, stim_pattern):
        """Send stim to neurons and read spike output (simulated)."""
        # In real use: CL1 API call
        spikes = np.random.randint(0,5,59)
        return spikes

    def make_action(self, action):
        """Send action to ViZDoom and get frame."""
        buttons = {
            'MOVE_FORWARD': [1,0,0,0],
            'TURN_LEFT': [0,1,0,0],
            'TURN_RIGHT':[0,0,1,0],
            'SHOOT':[0,0,0,1]
        }
        self.game.make_action(buttons.get(action, [0,0,0,0]))
        frame = self.game.get_state().screen_buffer
        frame = np.transpose(frame, (1,2,0)) # HWC
        return frame
