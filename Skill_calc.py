import streamlit as st

# ページのステートを初期化
if "page" not in st.session_state:
    st.session_state.page = 1
if "X1" not in st.session_state:
    st.session_state.X1 = None
if "X2_list" not in st.session_state:
    st.session_state.X2_list = [0]*10
if "X3" not in st.session_state:
    st.session_state.X3 = None

# 「次へ」ボタン押下で次ページに進む
def next_page():
    st.session_state.page += 1

# 「再計算する」ボタンで初期化
def reset():
    st.session_state.page = 1
    st.session_state.X1 = None
    st.session_state.X2_list = [0]*10
    st.session_state.X3 = None

# ステップ1
if st.session_state.page == 1:
    st.write("### ① 基本の戦法発動時間は？")
    st.session_state.X1 = st.radio(
        "選択してください",
        [10, 15, 20, 25, 30],
        index=0,
        horizontal=True
    )
    st.button("次へ", on_click=next_page)

# ステップ2
elif st.session_state.page == 2:
    st.write("### ② 戦法短縮時間割合(%)は？（10個まで入れて自動で合計）")
    cols = st.columns(5)
    for i in range(10):
        col = cols[i % 5]
        st.session_state.X2_list[i] = col.number_input(
            f"{i+1}個目", value=0, min_value=0, max_value=100, step=1, key=f"X2_{i}"
        )
    st.button("次へ", on_click=next_page)

# ステップ3
elif st.session_state.page == 3:
    st.write("### ③ 敏活レベルは？")
    options = {
        "ないよ": 1.00,
        "敏活I": 1.02,
        "敏活II": 1.04,
        "敏活III": 1.07,
        "敏活IV": 1.10,
        "敏活V": 1.15
    }
    selected = st.radio("選んでね", list(options.keys()), horizontal=True)
    st.session_state.X3 = options[selected]
    st.button("次へ", on_click=next_page)

# ステップ4：計算と表示
elif st.session_state.page == 4:
    X1 = st.session_state.X1
    X2 = sum(st.session_state.X2_list)
    X3 = st.session_state.X3

    X4 = (X1 - (X1 * X2 / 100)) / X3
    X5 = int(X4 // 2) * 2

    st.write("### ✨ 結果発表 ✨")
    st.markdown(f"""
    - 基本発動時間は **{X1}秒**
    - 短縮割合は **{X2}%**
    - 敏活効果は **{X3}**
    - ➤ 戦法発動時間は **{X4:.2f}秒** の見込み！
    - ➤ エフェクトは **{X5}秒** で発現します。知らんけど。
    """)

    st.button("🔁 再計算する", on_click=reset)