import cv2

# Load Haar cascade files for face and smile detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')

# Function for calculator (returns result and emoji)
def calculator():
    try:
        num1 = float(input("Enter first number: "))
        op = input("Enter operation (+, -, *, /): ")
        num2 = float(input("Enter second number: "))
        
        emoji = ""
        result = None

        if op == '+':
            result = num1 + num2
            emoji = "😀"  # happy
        elif op == '-':
            result = num1 - num2
            emoji = "😢"  # sad
        elif op == '*':
            result = num1 * num2
            emoji = "😡"  # angry
        elif op == '/':
            if num2 != 0:
                result = num1 / num2
                emoji = "🤣"  # funny
            else:
                print("Error: Division by zero")
                return None, ""
        else:
            print("Invalid operation")
            return None, ""

        print(f"Result: {result} {emoji}")
        return result, emoji

    except:
        print("Invalid input")
        return None, ""

# Open camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        roi_gray = gray[y:y+h, x:x+w]

        # Draw face rectangle
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Detect smiles
        smiles = smile_cascade.detectMultiScale(roi_gray, 1.8, 20)

        if len(smiles) > 0:
            cv2.putText(frame, "Smile Detected! Running Calculator...", (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.imshow('Webcam', frame)
            cv2.waitKey(500)

            # Get result & emoji
            result, emoji = calculator()

            # Show result + emoji in webcam
            if result is not None:
                text = f"Result: {result} {emoji}"
                cv2.putText(frame, text, (50, 100),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2)
                cv2.imshow('Webcam', frame)
                cv2.waitKey(3000)  # Show for 3 seconds

            cap.release()
            cv2.destroyAllWindows()
            exit()

    cv2.imshow('Webcam', frame)

cap.release()
cv2.destroyAllWindows()



