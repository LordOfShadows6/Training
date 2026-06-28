import time
import winsound




def select_option(prompt, options):
    print(prompt)
    for key, label in options.items():
        print(f"{key}: {label}")
    choice = input("Choose: ").strip()
    while choice not in options:
        choice = input("Invalid choice. Choose again: ").strip()
    return choice


def play_beep(frequency, duration_ms):
    winsound.Beep(frequency, duration_ms)


def get_positive_number(prompt, cast=float):
    while True:
        try:
            value = cast(input(prompt).strip())
            if value > 0:
                return value
        except ValueError:
            pass
        print("Invalid value. Please enter a positive number.")


def main():
    levels = {
        "1": ("quarter", 410),
        "2": ("half", 410),
        "3": ("three quarters", 410),
        "4": ("full", 410),
    }

    beep_length_options = {
        "1": 0.5,
        "2": 1,
        "3": 2,
        "4": 3,
        "5": 5,
        "6": 10,
        "7": 15,
    }

    modes = {
        "1": {
            "TOTAL_DURATION": 5 * 60,
            "INTERVAL_SECONDS": 1,
            "PAUSE_INTERVAL": 30,
            "PAUSE_DURATION": 10,
        },
        "2": {
            "TOTAL_DURATION": 10 * 60,
            "INTERVAL_SECONDS": 2,
            "PAUSE_INTERVAL": 60,
            "PAUSE_DURATION": 15,
        },
        "3": {
            "TOTAL_DURATION": 15 * 60,
            "INTERVAL_SECONDS": 3,
            "PAUSE_INTERVAL": 90,
            "PAUSE_DURATION": 20,
        },
        "4": {
            "TOTAL_DURATION": 20 * 60,
            "INTERVAL_SECONDS": 4,
            "PAUSE_INTERVAL": 120,
            "PAUSE_DURATION": 30,
        },
        "5": {
            "TOTAL_DURATION": 30 * 60,
            "INTERVAL_SECONDS": 5,
            "PAUSE_INTERVAL": 180,
            "PAUSE_DURATION": 60,
        },
        "6": {
            "CUSTOM": True,
        },
    }

    level_choice = select_option("Choose a level:", {k: v[0] for k, v in levels.items()})
    level_name, BEEP_FREQUENCY = levels[level_choice]

    beep_choice = select_option("Choose beep length:", {k: f"{v}s" for k, v in beep_length_options.items()})
    beep_seconds = beep_length_options[beep_choice]
    BEEP_DURATION_MS = beep_seconds * 1000

    print("Choose a mode:")
    for key, cfg in modes.items():
        if key == "6":
            print("6: custom settings")
        else:
            print(
                f"{key}: interval {cfg['INTERVAL_SECONDS']}s, total {cfg['TOTAL_DURATION'] // 60}m, pause every {cfg['PAUSE_INTERVAL']}s for {cfg['PAUSE_DURATION']}s"
            )

    choice = input("Mode (1-6): ").strip()
    while choice not in modes:
        choice = input("Invalid mode. Enter 1-6: ").strip()

    if choice == "6":
        TOTAL_DURATION = int(get_positive_number("Total duration in seconds: ", int))
        INTERVAL_SECONDS = get_positive_number("Beep interval in seconds: ")
        PAUSE_INTERVAL = get_positive_number("Pause interval in seconds: ")
        PAUSE_DURATION = get_positive_number("Pause duration in seconds: ")
        beep_seconds = get_positive_number("Beep length in seconds: ")
        BEEP_DURATION_MS = int(beep_seconds * 1000)
    else:
        config = modes[choice]
        TOTAL_DURATION = config["TOTAL_DURATION"]
        INTERVAL_SECONDS = config["INTERVAL_SECONDS"]
        PAUSE_INTERVAL = config["PAUSE_INTERVAL"]
        PAUSE_DURATION = config["PAUSE_DURATION"]
    PAUSE_FREQUENCY = 1000

    next_pause = PAUSE_INTERVAL
    elapsed = 0
    try:
        while elapsed < TOTAL_DURATION:
            while elapsed >= next_pause:
                print(f"Pause at {time.strftime('%H:%M:%S')} for {PAUSE_DURATION} seconds")
                winsound.Beep(PAUSE_FREQUENCY, 500)
                time.sleep(PAUSE_DURATION)
                elapsed += PAUSE_DURATION
                next_pause += PAUSE_INTERVAL
                if elapsed >= TOTAL_DURATION:
                    break
            if elapsed >= TOTAL_DURATION:
                break

            print(
                f"Beep at {time.strftime('%H:%M:%S')} ({elapsed}/{TOTAL_DURATION}s), "
                f"level {level_name}, {beep_seconds}s"
            )
            play_beep(BEEP_FREQUENCY, BEEP_DURATION_MS)

            time.sleep(INTERVAL_SECONDS)
            elapsed += beep_seconds + INTERVAL_SECONDS
    except KeyboardInterrupt:
        print("Timer stopped.")


if __name__ == "__main__":
    main()





