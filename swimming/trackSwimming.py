# This script helps swimmers track their performance and provides motivational feedback based on their pace.
# It can be expanded with more features like storing past records or visualizing progress.

distance = float(input("Enter the distance you swam in meters: "))
time = float(input("Enter the time you took in minutes: "))
pace = (time / distance) * 100  # pace in minutes per meter

if pace < 0.5:
    feedback = "Excellent pace! You're swimming like a champion!"
elif pace < 1:
    feedback = "Great job! Keep up the good work!"
elif pace < 1.5:
    feedback = "Good effort! You can improve your pace with more practice."
else:
    feedback = "Don't be discouraged! Every swimmer has their own pace. Keep training!"

print(f"You swam {distance} meters in {time} minutes.")
print(f"Your pace is {pace:.2f} minutes per meter.")
print(feedback)
# End of the script
