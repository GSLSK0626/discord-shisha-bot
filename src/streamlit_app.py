import streamlit as st
from db import get_user, create_user, add_shisha_log, get_shisha_logs, delete_shisha_log, update_shisha_log, init_db

# データベース初期化
init_db()

# セッション管理
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = None

st.title("シーシャ記録Webアプリ")

# ユーザー登録
with st.sidebar:
    st.header("ユーザー登録・ログイン")
    register = st.checkbox("新規登録")
    if register:
        username = st.text_input("ユーザー名")
        password = st.text_input("パスワード", type="password")
        if st.button("登録"):
            if get_user(username):
                st.warning("そのユーザー名は既に使われています。")
            else:
                from werkzeug.security import generate_password_hash
                user_id = create_user(username, generate_password_hash(password))
                st.success("登録しました。ログインしてください。")
    else:
        username = st.text_input("ユーザー名")
        password = st.text_input("パスワード", type="password")
        if st.button("ログイン"):
            user = get_user(username)
            from werkzeug.security import check_password_hash
            if user and check_password_hash(user[2], password):
                st.session_state['user_id'] = user[0]
                st.success(f"{username}でログインしました。")
            else:
                st.error("ユーザー名またはパスワードが違います。")
        if st.button("ログアウト"):
            st.session_state['user_id'] = None
            st.success("ログアウトしました。")

# ログイン後の機能
if st.session_state['user_id']:
    st.header("シーシャログ追加")
    date = st.text_input("日付（例: 2025-07-21）")
    shop_name = st.text_input("店名")
    main_flavor = st.text_input("メインフレーバー")
    sub_flavor = st.text_input("サブフレーバー（最大4つ、カンマ区切り）")
    comment = st.text_area("感想")
    if st.button("ログ追加"):
        add_shisha_log(st.session_state['user_id'], date, shop_name, main_flavor, sub_flavor, comment)
        st.success("ログを追加しました。")

    if 'edit_idx' not in st.session_state:
        st.session_state['edit_idx'] = None

    st.header("シーシャログ一覧")
    logs = get_shisha_logs(st.session_state['user_id'])
    for idx, log in enumerate(sorted(logs, key=lambda x: x[2]), start=1):
        st.write(f"番号: {idx} | 日付: {log[2]} | 店名: {log[3]}")
        st.write(f"メイン: {log[4]} / サブ: {log[5]}")
        st.write(f"感想: {log[6]}")
        col1, col2 = st.columns(2)
        if col1.button(f"編集 {idx}"):
            st.session_state['edit_idx'] = idx
            st.experimental_rerun()
        if col2.button(f"削除 {idx}"):
            delete_shisha_log(log[0])
            st.warning("削除しました。")
            st.experimental_rerun()

        # 編集フォームの表示
        if st.session_state['edit_idx'] == idx:
            new_date = st.text_input(f"新しい日付（現在: {log[2]}）", value=log[2], key=f"edit_date_{idx}")
            new_shop = st.text_input(f"新しい店名（現在: {log[3]}）", value=log[3], key=f"edit_shop_{idx}")
            new_main = st.text_input(f"新しいメイン（現在: {log[4]}）", value=log[4], key=f"edit_main_{idx}")
            new_sub = st.text_input(f"新しいサブ（現在: {log[5]}）", value=log[5], key=f"edit_sub_{idx}")
            new_comment = st.text_area(f"新しい感想（現在: {log[6]}）", value=log[6], key=f"edit_comment_{idx}")
            if st.button(f"保存 {idx}"):
                update_shisha_log(log[0], new_date, new_shop, new_main, new_sub, new_comment)
                st.success("修正しました。")
                st.session_state['edit_idx'] = None
                st.experimental_rerun()  # 最新版で有効

            if st.button(f"キャンセル {idx}"):
                st.session_state['edit_idx'] = None
                st.experimental_rerun()  # 最新版で有効

    st.header("フレーバー検索")
    search = st.text_input("検索したいフレーバー名")
    if st.button("検索"):
        results = [log for log in logs if search.lower() in log[4].lower() or search.lower() in log[5].lower()]
        if results:
            for log in results:
                st.write(f"日付: {log[2]} | 店名: {log[3]} | メイン: {log[4]} | サブ: {log[5]} | 感想: {log[6]}")
        else:
            st.info("該当するログはありません。")
else:
    st.info("ログインしてください。")