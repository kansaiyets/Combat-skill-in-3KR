import streamlit as st

# ステート初期化
if "page" not in st.session_state:
    st.session_state.page = 1
if "X1" not in st.session_state:
    st.session_state.X1 = None
if "X2_list" not in st.session_state:
    st.session_state.X2_list = [0.0] * 10
if "X3" not in st.session_state:
    st.session_state.X3 = None
if "X4" not in st.session_state:
    st.session_state.X3 = None
if "X5_list" not in st.session_state:
    st.session_state.X4_list = [0.0] * 10

# ページ操作
def next_page():
    st.session_state.page += 1

def reset():
    st.session_state.page = 1
    st.session_state.X1 = None
    st.session_state.X2_list = [0.0] * 10
    st.session_state.X3 = None
    st.session_state.X4 = None
    st.session_state.X5_list = [0.0] * 10

# ページ1：基本の戦法発動時間
if st.session_state.page == 1:
    st.title("戦法発動時間の推定ツール")
    st.write("### ① 基本の戦法発動時間は？")
    st.session_state.X1 = st.radio(
        "秒数を選択してください。",
        [10, 15, 20, 25, 30],
        index=0,
        horizontal=True
    )
    st.button("次へ", on_click=next_page)

# ページ2：戦法ゲージ増加量（X2）
elif st.session_state.page == 2:
    st.write("### ② 戦法ゲージ増加量（%）はありますか？（最大10個まで、小数OK）")
    cols = st.columns(5)
    for i in range(10):
        col = cols[i % 5]
        st.session_state.X2_list[i] = col.number_input(
            f"{i+1}個目", value=0.0, min_value=0.0, step=0.1, key=f"X2_{i}"
        )
    st.button("次へ", on_click=next_page)

# ページ3：敏活レベル（X3）
elif st.session_state.page == 3:
    st.write("### ③ 敏活レベルは？")
    options = {
        "ないです。": 1.00,
        "敏活I": 1.02,
        "敏活II": 1.04,
        "敏活III": 1.07,
        "敏活IV": 1.10,
        "敏活V": 1.15
    }
    selected = st.radio("下から1つ選んでください。", list(options.keys()), horizontal=True)
    st.session_state.X3 = options[selected]
    st.button("次へ", on_click=next_page)

# ページ3：羌敏活レベル（X4）
elif st.session_state.page == 4:
    st.write("### ③ 羌敏活レベルは？")
    options = {
        "今頑張って研究しています。": 1.00,
        "羌敏活I": 1.02,
        "羌敏活II": 1.04,
        "羌敏活III": 1.07,
        "羌敏活IV": 1.10,
        "堂々の羌敏活V": 1.15
    }
    selected = st.radio("また1つ選んでください。", list(options.keys()), horizontal=True)
    st.session_state.X4 = options[selected]
    st.button("次へ", on_click=next_page)

# ページ5：戦法速度アップ（X5）
elif st.session_state.page == 5:
    st.write("### ④ 戦法速度アップ技能やアイテム（%）はありますか？（最大10個まで、小数OK）")
    cols = st.columns(5)
    for i in range(10):
        col = cols[i % 5]
        st.session_state.X4_list[i] = col.number_input(
            f"{i+1}個目", value=0.0, min_value=0.0, step=0.1, key=f"X4_{i}"
        )
    st.button("次へ", on_click=next_page)

# ページ6：結果表示
elif st.session_state.page == 6:
    X1 = st.session_state.X1
    X2 = sum(st.session_state.X2_list)
    X3 = st.session_state.X3
    X4 = st.session_state.X4
    X5 = sum(st.session_state.X5_list)

    X6 = (X1 - (X1 * X2 / 100)) / (X3 + X4 + X5 / 100)
    X7 = int(X6 // 2) * 2

    st.write("### ✨ 結果発表 ✨")
    st.markdown(f"""
    - 基本発動時間：**{X1}秒**  
    - 戦法ゲージ短縮割合：**{X2:.2f}%**  
    - 敏活効果（係数）：**{X3:.2f}**  
    - 羌敏活効果（係数）：**{X4:.2f}**  
    - その他の加速効果：**{X5:.2f}%**

    🧮 **吾輩のがばがば計算だと戦法発動時間は {X6:.2f}秒 の見込み！**  
    🌟 **エフェクトは {X7}秒 で発現するんとちゃうかな。（たぶん。知らんけど。）**
    """)

    st.button("🔁 再計算する", on_click=reset)
