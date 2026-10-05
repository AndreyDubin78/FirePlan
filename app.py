import streamlit as st
import fitz
from streamlit_image_coordinates import streamlit_image_coordinates
from PIL import Image
import io

st.set_page_config(
    page_title="FirePlan",
    layout="wide"
)

st.title("FirePlan")
st.subheader("План этажа")

uploaded_file = st.file_uploader(
    "Загрузить план проекта",
    type=["pdf", "png", "jpg", "jpeg"]
)

if uploaded_file is not None:

    st.success(f"Файл загружен: {uploaded_file.name}")

    if uploaded_file.name.lower().endswith(".pdf"):

        pdf = fitz.open(
            stream=uploaded_file.read(),
            filetype="pdf"
        )

        st.write(f"Страниц в PDF: {len(pdf)}")

        page_number = st.selectbox(
            "Выберите страницу",
            range(len(pdf)),
            format_func=lambda x: f"Страница {x + 1}"
        )

        page = pdf[page_number]

        pix = page.get_pixmap(
            matrix=fitz.Matrix(1.5, 1.5)
        )

        image_bytes = pix.tobytes("png")

        image = Image.open(io.BytesIO(image_bytes))

    else:

        image = Image.open(uploaded_file)

    st.write("Кликните внутри помещения на плане.")

    value = streamlit_image_coordinates(
        image,
        key="floor_plan"
    )

    if value is not None:

        x = value["x"]
        y = value["y"]

        st.success(
            f"Точка выбрана: X = {x}, Y = {y}"
        )

    st.info(
        "Следующий этап — определение границ помещения."
    )
