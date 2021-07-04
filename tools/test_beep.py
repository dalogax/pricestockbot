import winsound

def beep():
    frequency = 2500
    duration = 100
    winsound.Beep(frequency, duration)
    time.sleep(0.05)
    winsound.Beep(frequency, duration)
    time.sleep(0.05)
    winsound.Beep(frequency, duration)

beep()