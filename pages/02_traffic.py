st.title("교통량 예측 프로그램")

# 1. 시, 구, 동, 번지 선택
selected_city = st.selectbox("시 선택", city_list)
selected_gu = st.selectbox("구 선택", get_gu_list(selected_city))
selected_dong = st.selectbox("동 선택", get_dong_list(selected_city, selected_gu))
selected_address = st.text_input("번지 입력")

# 2. 도로명 선택
if selected_address:
    road_list = get_road_list(selected_city, selected_gu, selected_dong, selected_address)
    selected_road = st.selectbox("도로 선택", road_list)

# 3. 시간 선택
current_time = datetime.now().time()
selected_time = st.time_input("예측할 시간", value=current_time)

# 4. 예측 실행
if st.button("예측 시작"):
    prediction = predict_traffic(selected_city, selected_gu, selected_dong, selected_road, selected_time)
    st.success(f"예측된 교통량: {prediction['volume']}대 / 시간")
    st.metric("혼잡도 등급", prediction['level'])
