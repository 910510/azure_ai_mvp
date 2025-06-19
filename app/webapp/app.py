import streamlit as st
import random

# Generate a random number between 1 and 100
if 'random_number' not in st.session_state:
    st.session_state.random_number = random.randint(1, 100)

st.title("숫자 맞추기 게임")
st.write("1부터 100 사이의 숫자를 맞춰보세요!")

# Input for user's guess
guess = st.number_input("숫자를 입력하세요:", min_value=1, max_value=100, step=1)

if st.button("확인"):
    if guess < st.session_state.random_number:
        st.write("더 큰 숫자입니다!")
    elif guess > st.session_state.random_number:
        st.write("더 작은 숫자입니다!")
    else:
        st.write("정답입니다! 🎉")
        # Reset the game
        st.session_state.random_number = random.randint(1, 100)
        st.write("새로운 숫자가 설정되었습니다. 다시 맞춰보세요!")