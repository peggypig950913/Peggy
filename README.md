# Posture MVP (Streamlit snapshot 版)

簡介
- 使用 MediaPipe 偵測姿勢，Streamlit 作為簡易 UI（拍照分析、儲存紀錄、畫歷史趨勢）。
- 適合期末 demo：穩定、可展示偵測、角度、規則式判定與歷史視覺化。

快速說明
1. 部署 (Streamlit Cloud)
   - Push 到 GitHub，然後到 https://streamlit.io/cloud 新增 app（選擇此 repo 與 app.py）。
2. 本機測試
   - 建 virtualenv，安裝 requirements.txt，執行 streamlit run app.py

重要公式（報告可引用）
$$
\theta = \arccos\left(\frac{(A-B)\cdot(C-B)}{\|A-B\|\ \|C-B\|}\right)
$$
