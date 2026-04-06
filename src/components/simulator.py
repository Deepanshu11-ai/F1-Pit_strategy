class RaceSimulator:
    def __init__(self, total_laps, initial_tire):
        self.total_laps = total_laps
        self.default_tire = initial_tire
        
        self.reset()

        self.tire_profiles = {
        "soft":   {"base_offset": -2, "deg_rate": 0.5},
        "medium": {"base_offset": 0,  "deg_rate": 0.3},
        "hard":   {"base_offset": +1, "deg_rate": 0.1}
}

    def reset(self):
        self.current_lap = 1
        self.tire_type = self.default_tire
        self.tire_age = 0
        self.total_time = 0
    
    def calculate_lap_time(self):

        base_time = 90

        profile = self.tire_profiles[self.tire_type]

        base_offset = profile["base_offset"]
        deg_rate = profile["deg_rate"]

        penalty = self.tire_age * deg_rate

        lap_time = base_time + base_offset + penalty

        return lap_time
    
    def step(self, action):

        # 1. Handle pit stop
        if action == 1:
            self.tire_type = "soft"
            self.tire_age = 0
            self.total_time += 22

        elif action == 2:
            self.tire_type = "medium"
            self.tire_age = 0
            self.total_time += 22

        elif action == 3:
            self.tire_type = "hard"
            self.tire_age = 0
            self.total_time += 22

        # 2. Calculate lap time
        lap_time = self.calculate_lap_time()

        # 3. Update race state
        self.total_time += lap_time
        self.current_lap += 1
        self.tire_age += 1

        # 4. Check if race finished
        done = self.current_lap > self.total_laps

        # 5. Reward (minimize lap time)
        reward = -lap_time

        # 6. State (what RL sees)
        state = (self.current_lap, self.tire_type, self.tire_age)

        return state, reward, done
    
    def get_state(self):
        return (self.current_lap, self.tire_type, self.tire_age)

sim = RaceSimulator(10, "soft")

for i in range(10):
    action = 3 if i == 4 else 0  # pit on lap 5

    state, reward, done = sim.step(action)
    print(state, reward, sim.total_time)

    if done:
        break