import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pandas as pd

from src.pose_detector import PoseDetector, draw_landmarks
from src.posture_analyzer import PostureAnalyzer
from src.data_manager import DataManager

st.set_page_config(page_title="Posture MVP", layout="centered")
st.title("AI 姿勢矯正 MVP（Snapshot 版）")

detector = PoseDetector()
analyzer = PostureAnalyzer()
dm = DataManager()

st.write("操作：按「拍照」取一張相片，系統會計算角度並給出建議。")

img_file = st.camera_input("請對準全身，按下拍照")

if img_file is not None:
    image = Image.open(img_file)
    img_np = np.array(image.convert("RGB"))
    img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

    landmarks, pose_landmarks = detector.detect(img_bgr)
    annotated = draw_landmarks(img_bgr.copy(), pose_landmarks)

    res = analyzer.analyze(landmarks)

    st.subheader("分析結果")
    st.write(f"分數： {res['score']}")
    for k,v in res["angles"].items():
        st.write(f"{k}: {v:.1f}°")
    if res["messages"]:
        st.warning("\n".join(res["messages"]))
    else:
        st.success("姿勢良好！")

    annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
    st.image(annotated_rgb, caption="偵測結果（骨架 overlay）", use_column_width=True)

    if st.button("儲存紀錄"):
        dm.save_record(res["score"], res["angles"], res["messages"])
        st.success("已儲存")

st.markdown("---")
st.subheader("歷史紀錄")
df = dm.load_records()
if not df.empty:
    st.write(df[["timestamp","score","messages"]].tail(10))
    import plotly.express as px
    df["timestamp_parsed"] = pd.to_datetime(df["timestamp"])
    fig = px.line(df, x="timestamp_parsed", y="score", title="分數走勢")
    st.plotly_chart(fig)
else:
    st.info("尚無紀錄，拍張照並儲存一次來建立歷史資料。")
