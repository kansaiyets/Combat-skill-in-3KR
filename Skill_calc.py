import streamlit as st

# ページ構成
st.set_page_config(page_title="戦法発動計算時間推定", layout="centered")

# セッションステート初期化
if "page" not in st.session_state:
    st.session_state.page = 1

# 再計算ボタンでリセット
def reset():
    st.session_state.page = 1
    for key in list(st.session_state.keys()):
        if key != "page":
            del st.session_state[key]

# ステップ 1: 基本発動時間の選択
if st.session_state.page == 1:
    st.markdown("### ① 基本の戦法発動時間は何秒ですか？")
    st.session_state.X1 = st.radio(
        "選択してください",
        [10, 15, 20, 25, 30],
        index=0,
        horizontal=True
    )
    st.session_state.page = 2

# ステップ 2: 戦法ゲージ増加量の入力
elif st.session_state.page == 2:
    st.markdown("### ② 戦法ゲージ増加量（%）はありますか？")
    st.write("10個まで入力できます。空欄は0として扱われます。")
    cols = st.columns(5)
    X2_values = []
    for i in range(10):
        col = cols[i % 5]
        val = col.number_input(
            f"{i+1}個目", value=0.0, min_value=0.0, max_value=100.0,
            step=0.1, key=f"X2_{i}"
        )
        X2_values.append(val)
    X2 = sum(X2_values)
    st.write(f"合計: {X2:.2f}%")
    if st.button("次へ"):
        st.session_state.page = 3

# ステップ 3: 敏活レベルの選択
elif st.session_state.page == 3:
    st.markdown("### ③ 敏活レベルはいかほどで？")
    levels = {
        "ないよ": 1.00,
        "敏活I": 1.02,
        "敏活II": 1.04,
        "敏活III": 1.07,
        "敏活IV": 1.10,
        "敏活V": 1.15,
    }
    level_label = st.radio("敏活レベルを選んでください。", list(levels.keys()), key="X3", horizontal=True)
    X3 = levels[level_label]
    if st.button("次へ"):
        st.session_state.page = 4

# ステップ 4: その他の速度アップ入力
elif st.session_state.page == 4:
    st.markdown("### ④ 戦法速度アップ技能やアイテム（%）はありますか？")
    st.write("10個まで入力できます。空欄は0として扱われます。")
    cols = st.columns(5)
    X4_values = []
    for i in range(10):
        col = cols[i % 5]
        val = col.number_input(
            f"{i+1}個目", value=0.0, min_value=0.0, max_value=100.0,
            step=0.1, key=f"X4_{i}"
        )
        X4_values.append(val)
    X4 = sum(X4_values)
    st.write(f"合計: {X4:.2f}%")
    if st.button("次へ"):
        st.session_state.page = 5

# ステップ 5: 結果表示
elif st.session_state.page == 5:
    X1 = st.session_state.X1
    X2 = sum([st.session_state.get(f"X2_{i}", 0.0) for i in range(10)])
    X3 = levels[st.session_state.X3]
    X4 = sum([st.session_state.get(f"X4_{i}", 0.0) for i in range(10)])
    X5 = (X1 - X1 * X2 / 100) / (X3 + X4 / 100)
    X6 = int(X5 // 2) * 2

    st.markdown("##✨ 結果発表 ✨")
    st.markdown(f"""
    基本発動時間は **{X1}秒**、短縮割合は **{X2:.2f}%**、  
    敏活効果は **{X3:.2f}**、その他の効果は **{X4:.2f}%** なので、  
    戦法発動時間は **{X5:.2f}秒** の見込みです！

    ちなみにエフェクトは **{X6}秒** で発現します。  
    **知らんけど。**
    """)
    if st.button("🔄 再計算する", on_click=reset):
        pass
