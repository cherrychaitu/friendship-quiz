import json
import urllib.request
import pandas as pd
import streamlit as st

# Replace this with the Web App URL you copied from Google Apps Script!
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbzSHELMdv7pjOgaYfeLK_Cp6dyHrrJcckIZuNqHohwEUHAp4l9Sxlu0q0sobdN-CbCKfQ/exec"


def save_score(name, score):
  payload = {"name": name, "score": score}
  data = json.dumps(payload).encode("utf-8")
  req = urllib.request.Request(
      WEB_APP_URL, data=data, headers={"Content-Type": "application/json"}
  )
  try:
    urllib.request.urlopen(req)
  except Exception as e:
    st.error(f"Could not save score: {e}")


def get_scores():
  try:
    with urllib.request.urlopen(WEB_APP_URL) as response:
      data = json.loads(response.read().decode())
      return data
  except Exception as e:
    return []





st.title("🌟 Bestie Compatibility Quiz: How Well Do You Know Me? 🌟")
st.write("Answer the questions below to test your friendship score!")
name=st.text_input("Enter your name to take the quiz:")
if name:
    st.write(f"welcome {name}, let's see how much you know about Charitha")
    score=0

# Initialize score

    total_questions = 5

# --- Question 1 ---
    st.subheader("1. What is the first kdrama charitha watched?")
    q1_options = ["W-Two worlds", "Strong Women Do-Bong-Soon", "While you were sleeping", "Lovely Runner", "F4"]
    q1_answer = st.radio("Select an option:", q1_options, key="q1")

# --- Question 2 ---
    st.subheader("2. What is my go-to comfort food?")
    q2_options = ["Pizza", "Biryani", "Ice Cream", "Noodles", "Burger"]
    q2_answer = st.radio("Select an option:", q2_options, key="q2")

# --- Question 3 ---
    st.subheader("3. What does charitha likes to drink the most?")
    q3_options = ["Tea", "Coffee", "Cooldrinks", "Milkshakes", "Fruit Juice"]
    q3_answer = st.radio("Select an option:", q3_options, key="q3")

# --- Question 4 ---
    st.subheader("4. What genre of books or movies do I love the most?")
    q4_options = ["Romance", "Thriller", "Sci-Fi", "Fantasy", "Mystery"]
    q4_answer = st.radio("Select an option:", q4_options, key="q4")

# --- Question 5 ---
    st.subheader("5. What is my preferred way to spend a free weekend?")
    q5_options = ["Crocheting", "Sleeping / Relaxing", "Shopping", "Reading novels", "Watching Tv with chips"]
    q5_answer = st.radio("Select an option:", q5_options, key="q5")

# Submit button to calculate score
    if st.button("Calculate Friendship Score"):
    # Define correct answers (you can customize these to your actual preferences!)
        correct_answers = {
        "q1": "Strong Women Do-Bong-Soon",
        "q2": "Noodles",
        "q3": "Cooldrinks",
        "q4": "Romance",
        "q5": "Watching Tv with chips"}

    # Evaluate answers
        score = 0
        if q1_answer == correct_answers["q1"]:
            score += 1
        if q2_answer == correct_answers["q2"]:
            score += 1
        if q3_answer == correct_answers["q3"]:
            score += 1
        if q4_answer == correct_answers["q4"]:
            score += 1
        if q5_answer == correct_answers["q5"]:
            score += 1

    # Calculate percentage
        percentage = (score / total_questions) * 100

        st.divider()
        st.metric(label="Your Friendship Score", value=f"{int(percentage)}%")
        st.write(f"You got **{score}** out of **{total_questions}** questions right!")
    # Example of where to put it when the quiz is submitted:
        if st.button("Submit Quiz"):
        # Calculate score here...
            #score = 4  # (example score)

        # Save score to Google Sheet (runs only once per submission)
            save_score(name, score)

            st.success(f"Thanks {name}! Your score has been recorded.")
            st.balloons()

    # Feedback messages based on score
        if percentage == 100:
            st.balloons()
            st.success("True Besties! You know everything about each other! 💖✨")
        elif percentage >= 60:
            st.info("Good friends! You know each other quite well, but there's a bit more to learn! 👍")
        else:
            st.warning("Acquaintance zone! Time to sit down and chat to catch up on favorites! 😅")

        #st.button("Submit Quiz")
        # Calculate score here...
            #score = 4  # (example score)

        # Save score to Google Sheet (runs only once per submission)
        #save_score(name, percentage)

        #st.success(f"Thanks {name}! Your score has been recorded.")


        #save_score(name, percentage)
        #st.caption("Your score has been recorded! Thanks for playing! ❤️")
else:
    st.info("👆 Please enter your name above to unlock the quiz.")

# --- ADMIN PANEL AT THE BOTTOM ---
st.divider()
st.subheader("🔐 Creator Admin Panel")

# Create a password-protected input box
admin_password = st.text_input(
        "Enter admin password to view submission", type="password")


# Set your own secret password here (e.g., change 'mysecret123' to whatever you like)
if admin_password == "besti2026":
    st.success("Access Granted! Here are your quiz participants:")

  # Fetch data from Google Sheet
    sheet_data = get_scores()

    if len(sheet_data) > 1:
    # Convert the Google Sheet rows into a clean DataFrame table
        df = pd.DataFrame(sheet_data[1:], columns=sheet_data[0])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No submissions yet! Share your link with friends.")

elif admin_password:
    st.error("Incorrect password! Nice try though. 😉")

