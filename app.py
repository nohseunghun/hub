import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(
    page_title="오성고 매점 재고 관리",
    page_icon="🏪",
    layout="wide"
)

# 초기 데이터
if 'inventory' not in st.session_state:
    st.session_state.inventory = pd.DataFrame([
        ["삼각김밥", 1200, 15],
        ["컵라면", 1800, 10],
        ["콜라", 2000, 20],
        ["초코우유", 1500, 8],
        ["과자", 1700, 12]
    ], columns=["상품명", "가격", "재고"])

# 제목
st.title("🏪 오성고 매점 재고 관리 앱")
st.markdown("학생회/매점용 실시간 재고 관리 시스템")

# 사이드바
st.sidebar.header("📋 메뉴")
menu = st.sidebar.radio(
    "기능 선택",
    ["재고 현황", "상품 추가", "판매 처리", "재고 수정", "통계"]
)

inventory = st.session_state.inventory

# 재고 현황
if menu == "재고 현황":
    st.subheader("📦 현재 재고 현황")

    total_items = inventory["재고"].sum()
    total_products = len(inventory)
    low_stock = len(inventory[inventory["재고"] <= 5])

    col1, col2, col3 = st.columns(3)

    col1.metric("총 상품 종류", total_products)
    col2.metric("전체 재고 수량", total_items)
    col3.metric("재고 부족 상품", low_stock)

    st.dataframe(inventory, use_container_width=True)

    st.subheader("⚠️ 재고 부족 상품")
    low_stock_df = inventory[inventory["재고"] <= 5]

    if len(low_stock_df) > 0:
        st.warning("재고가 부족한 상품이 있습니다!")
        st.dataframe(low_stock_df, use_container_width=True)
    else:
        st.success("모든 상품 재고가 충분합니다.")

# 상품 추가
elif menu == "상품 추가":
    st.subheader("➕ 새 상품 추가")

    with st.form("add_product"):
        product_name = st.text_input("상품명")
        product_price = st.number_input("가격", min_value=0, step=100)
        product_stock = st.number_input("초기 재고", min_value=0, step=1)

        submit = st.form_submit_button("상품 추가")

        if submit:
            if product_name:
                new_row = pd.DataFrame([
                    [product_name, product_price, product_stock]
                ], columns=["상품명", "가격", "재고"])

                st.session_state.inventory = pd.concat(
                    [st.session_state.inventory, new_row],
                    ignore_index=True
                )

                st.success(f"'{product_name}' 상품이 추가되었습니다!")
            else:
                st.error("상품명을 입력해주세요.")

# 판매 처리
elif menu == "판매 처리":
    st.subheader("🛒 판매 처리")

    product_list = inventory["상품명"].tolist()

    selected_product = st.selectbox("판매 상품 선택", product_list)

    selected_row = inventory[inventory["상품명"] == selected_product].iloc[0]

    st.info(
        f"현재 재고: {selected_row['재고']}개 | 가격: {selected_row['가격']}원"
    )

    sell_quantity = st.number_input(
        "판매 수량",
        min_value=1,
        max_value=int(selected_row['재고']) if selected_row['재고'] > 0 else 1,
        step=1
    )

    if st.button("판매 완료"):
        if selected_row['재고'] >= sell_quantity:
            idx = inventory[inventory["상품명"] == selected_product].index[0]
            st.session_state.inventory.at[idx, "재고"] -= sell_quantity

            total_price = selected_row['가격'] * sell_quantity

            st.success(
                f"{selected_product} {sell_quantity}개 판매 완료!\n총 금액: {total_price:,}원"
            )
        else:
            st.error("재고가 부족합니다!")

# 재고 수정
elif menu == "재고 수정":
    st.subheader("✏️ 재고 수정")
