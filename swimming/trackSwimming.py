# This script helps swimmers track their performance and provides motivational feedback based on their pace.
# It can be expanded with more features like storing past records or visualizing progress.

distance = float(input("Enter the distance you swam in meters: "))
time_str = input("Enter the time you took (mm:ss): ")
minutes, seconds = map(int, time_str.split(":"))
time = minutes + seconds / 60

pace = (time / distance) * 100  # pace in minutes per 100 meters

if pace < 1:
    feedback = "Excellent pace! You're swimming like a champion!"
elif pace < 1.5:
    feedback = "Great job! Keep up the good work!"
elif pace < 2:
    feedback = "Good effort! You can improve your pace with more practice."
else:
    feedback = "Don't be discouraged! Every swimmer has their own pace. Keep training!"

print(f"You swam {distance} meters in {time:.2f} minutes.")
print(f"Your pace is {pace:.2f} minutes per 100 meters.")
print(feedback)
# End of the script
