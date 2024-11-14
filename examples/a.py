import streamlit as st

animal = st.form('my_animal')

# これはメインボディに直接書き込まれます。フォームコンテナが
# 上で定義されているので、フォーム内に書かれたすべての下に表示されます。
sound = st.selectbox('Sounds like', ['meow','woof','squeak','tweet'])

# これらのメソッドはフォームコンテナに対して呼び出されるため、フォーム内に表示されます。
submit = animal.form_submit_button(f'{sound}で言う!')
sentence = animal.text_input('あなたの文:', 'Where\'s the tuna?')
say_it = sentence.rstrip('.,!?') + f', {sound}!'
if submit:
    animal.subheader(say_it)
else:
    animal.subheader('&nbsp;')
    
