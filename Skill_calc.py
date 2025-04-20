import streamlit as st

# ページ番号の初期化
if "page" not in st.session_state:
    st.session_state.page = 1

# 敏活レベル対応辞書
levels = {
    "ないよ": 1.00,
    "敏活I": 1.02,
    "敏活II": 1.04,
    "敏活III": 1.07,
    "敏活IV": 1.10,
    "敏活V": 1.15,
}

# 再計算ボタンで初期化
def reset():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state.page = 1

st.title("戦法発動時間チェッカー")

# ①ページ：基本の戦法発動時間
if st.session_state.page == 1:
    st.markdown("### ① 基本の戦法発動時間は何秒ですか？")
    selected_time = st.radio("選択してください", [10, 15, 20, 25, 30], key="X1")  # ここで自動的に st.session_state["X1"] に入る
    if selected_time:
        st.write(X1)
        if st.button("次へ"):
            st.session_state.page += 1
    else:
        st.warning("選択してください。")

# ②ページ：戦法ゲージ増加量（X2）
if st.session_state.page == 2:
    st.markdown("### ② 戦法ゲージ増加量（%）はありますか？（小数OK）")
    cols = st.columns(5)
    for i in range(10):
        with cols[i % 5]:
            st.number_input(f"{i+1}個目", min_value=0.0, step=0.1, key=f"X2_{i}")
    if st.button("次へ"):
        st.session_state.page += 1

# ③ページ：敏活レベル（X3）
elif st.session_state.page == 3:
    st.markdown("### ③ 敏活レベルはいかほどで？")
    st.radio("選んでください", list(levels.keys()), key="X3")
    if "X3" in st.session_state:
        if st.button("次へ"):
            st.session_state.page += 1
    else:
        st.warning("選択してください。")

# ④ページ：戦法速度アップ（X4）
elif st.session_state.page == 4:
    st.markdown("### ④ 戦法速度アップ技能やアイテム（%）はありますか？（小数OK）")
    cols = st.columns(5)
    for i in range(10):
        with cols[i % 5]:
            st.number_input(f"{i+1}個目", min_value=0.0, step=0.1, key=f"X4_{i}")
    if st.button("次へ"):
        st.session_state.page += 1

# ⑤ページ：結果表示
elif st.session_state.page == 5:
    # 値の取得
    X1 = int(st.session_state.get("X1", 0))
    X2 = sum([st.session_state.get(f"X2_{i}", 0.0) for i in range(10)])
    X3 = levels.get(st.session_state.get("X3"), 1.0)
    X4 = sum([st.session_state.get(f"X4_{i}", 0.0) for i in range(10)])

    # 計算
    X5 = (X1 - X1 * X2 / 100) / (X3 + X4 / 100)
    X6 = int(X5 // 2) * 2

    # 結果表示
    st.markdown("## 🧮 結果")
    st.markdown(f"""
    基本発動時間は **{X1}秒**、短縮割合は **{X2:.2f}%**、  
    敏活効果は **{X3:.2f}**、その他の効果は **{X4:.2f}%** なので、  
    戦法発動時間は **{X5:.2f}秒** の見込みです！

    ちなみにエフェクトは **{X6}秒** で発現します。  
    **知らんけど。**
    """)

    if st.button("🔄 再計算する", on_click=reset):
        pass
