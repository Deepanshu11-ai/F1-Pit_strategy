from simulator import RaceSimulator

sim = RaceSimulator(10, "soft")

print("\n🏎️ Race Start!\n")

while True:
    # simple strategy: pit on lap 5
    if sim.current_lap == 5:
        action = 3   # pit to hard
        print(f"👉 Lap {sim.current_lap}: PIT STOP → HARD")
    else:
        action = 0   # continue

    state, reward, done = sim.step(action)

    print(f"Lap: {state[0]-1} | Tire: {state[1]} | Age: {state[2]} | LapTime: {-reward:.2f} | TotalTime: {sim.total_time:.2f}")

    if done:
        break

print("\n🏁 Race Finished!")
print(f"Total Race Time: {sim.total_time:.2f}")