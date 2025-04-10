import streamlit as st
from dotenv import load_dotenv
import os
import pandas as pd
from Uploadfile.upload import *
from openai import OpenAI, AsyncOpenAI
from Models.model import SentimentItem, SentimentTrue, OutputOptions, Item, system_prompt, system_prompt_2, ClassifyItem, ClassifyTrue
from io import BytesIO
import asyncio
import openai
import random


msg= upload_file()
# โหลดค่าจาก .env
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# st.write(openai_api_key)

# if not openai_api_key:
#     st.error("API Key is missing. Please check your .env file.")
# else:
#     st.success("API Key loaded successfully!")


# if msg:
#     col1 = [row[0] for row in msg]  # ดึงค่า col1 เก็บเป็น list
#     col2 = [row[1] for row in msg]  # ดึงค่า col2 เก็บเป็น list
#     col3 = [row[2] for row in msg]

sentiment_exp = []
sentiment_val = []
IS_TRUE_exp = []
IS_TRUE_val = []
classify_exp = []

classify_val = []
classify_new = []

    
# หากกรอก API Key ให้ทำการตั้งค่า

if openai_api_key:
    openai.api_key = openai_api_key
    model = "gpt-4o-mini" #เปลี่ยน model ได้

    client = AsyncOpenAI(api_key=openai.api_key)

    async def function_llm(qa_test):
        # แปลงข้อความเดี่ยวเป็นลิสต์
        qa_list = qa_test.strip().split("\n")
        qa_cleaned = [line.split(". ", 1)[1] for line in qa_list if ". " in line]
        classy_final = []  # ลิสต์สำหรับเก็บผลลัพธ์
        sentiment_final = []

        # วนลูปผ่านข้อความแต่ละรายการใน qa_cleaned
        for qa in qa_cleaned:
            completion = await client.beta.chat.completions.parse(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt.format(phase=len(qa.split("\n")))},
                    {"role": "user", "content": qa},
                ],
                response_format=ClassifyTrue,
            )
            classy = completion.choices[0].message.parsed  # ดึงผลลัพธ์จาก API
            classy_final.append(classy)

            completion = await client.beta.chat.completions.parse(
                model=model,
                messages=[
                    {"role": "system", "content": system_prompt_2.format(phase=len(qa.split("\n")))},
                    {"role": "user", "content": qa},
                ],
                response_format=SentimentTrue,
            )
            sentiment = completion.choices[0].message.parsed
            sentiment_final.append(sentiment)

        output = {
        "Sentiment": sentiment_final,
        "Classify": classy_final
        }

        return output

    async def main():
        batch_size = 10
        ql = []
        for i in range(0, len(msg), batch_size):
            info = msg[i:i+batch_size]
            info = [f"{j+1}. {info[j]}" for j in range(len(info))]
            ql.append("\n".join(info))

        tasks = [function_llm(ql[i]) for i in range(len(ql))]
        result = await asyncio.gather(*tasks)
        
        return result

    if st.button("Run Analysis"):
        with st.spinner("Loading... Please wait"):
            final_result = asyncio.run(main())  # รอผลจาก main()

        # เตรียม list สำหรับเก็บข้อมูล
        sentiment_exp = []
        sentiment_val = []
        IS_TRUE_exp = []
        IS_TRUE_val = []
        ADS_exp = []
        ADS_val = []

        classify_val = []
        classify_new = []
        # วนลูปผ่านข้อมูลแต่ละ event
        for event in final_result:
            for i in range(len(event['Sentiment'])):
                sentiment_exp.append(event['Sentiment'][i].Sentiment[0].explanation)
                sentiment_val.append(event['Sentiment'][i].Sentiment[0].output)
                IS_TRUE_exp.append(event['Sentiment'][i].IS_TRUE[0].explanation)
                IS_TRUE_val.append(event['Sentiment'][i].IS_TRUE[0].output)
            for i in range(len(event['Classify'])):
                classify_exp.append(event['Classify'][i].Classify.explanation)
                classify_val.append(event['Classify'][i].Classify_output.output.value)

        # แสดงผลข้อมูลในแต่ละ list
        min_length = len(msg)
        sentiment_exp = sentiment_exp[:min_length]
        sentiment_val = sentiment_val[:min_length]
        # ans = my_classify[:min_length]
        # human_ans = human_ans[:min_length]
        IS_TRUE_exp = IS_TRUE_exp[:min_length]
        IS_TRUE_val = IS_TRUE_val[:min_length]
        classify_exp = classify_exp[:min_length]
        classify_val = classify_val[:min_length]

        # st.write(
        #     len(sentiment_exp), len(sentiment_val), len(IS_TRUE_exp), len(IS_TRUE_val),
        #     len(classify_exp), len(classify_val)
        # )


        if len(sentiment_exp) == len(sentiment_val) == len(IS_TRUE_exp) == len(IS_TRUE_val) == len(classify_exp) == len(classify_val):
            # ใช้ st.columns เพื่อแยกพื้นที่ออกเป็นสองคอลัมน์
            col1, col2 = st.columns(2)

            # ส่วนของคอลัมน์ซ้าย (col1)
            with col1:
                st.subheader("Sentiment Analysis Summary")
                
                # นับจำนวน Sentiment
                sentiment_counts = {
                    "Positive": sentiment_val.count("Positive"),
                    "Neutral": sentiment_val.count("Neutral"),
                    "Negative": sentiment_val.count("Negative")
                }

                # แสดงจำนวน Sentiment
                st.write(f"Positive: {sentiment_counts['Positive']}")
                st.write(f"Neutral: {sentiment_counts['Neutral']}")
                st.write(f"Negative: {sentiment_counts['Negative']}")
                total_sentiment = sum(sentiment_counts.values())
                st.write(f"**TOTAL SENTIMENT: {total_sentiment}**")

                # นับจำนวน classify ที่ไม่ใช่ NaN และแสดงจำนวน
                classify_counts = {
                    "Nan": classify_val.count("Nan"),
                    "True": classify_val.count("True"),
                    "True 5G": classify_val.count("True 5G"),
                    "True Visions": classify_val.count("True Visions"),
                    "True Visions NOW": classify_val.count("True Visions NOW"),
                    "True Online": classify_val.count("True Online"),
                    "True You": classify_val.count("True You"),
                    "True ID": classify_val.count("True ID"),
                    "True iService": classify_val.count("True iService"),
                    "True Corp": classify_val.count("True Corp"),
                    "Dtac": classify_val.count("Dtac")
                }
                total_classify = sum(classify_counts.values())
                # แสดงจำนวน Classify
                for key, value in classify_counts.items():
                    st.write(f"{key}: {value}")
                st.write(f"**TOTAL CLASSIFY: {total_classify}**")

            # ส่วนของคอลัมน์ขวา (col2)
            with col2:
                st.subheader("Preview:")
                gpt_4o_mini = pd.DataFrame({
                    "Message": msg,
                    "LLM_Reason": sentiment_exp,
                    "LLM": sentiment_val,
                    # "Answer": ans,
                    # "Human_Answer": human_ans,
                    "IS_TRUE_explain": IS_TRUE_exp,
                    "IS_TRUE_value": IS_TRUE_val,
                    "Classify_explain": classify_exp,
                    "classify_value": classify_val,
                    # "true_classify": true_classify,
                    # "my_classify": cleaned_ans
                })
                st.write(gpt_4o_mini.head())  # แสดง preview

                # สร้างไฟล์ Excel ให้ดาวน์โหลด
                output = BytesIO()
                with pd.ExcelWriter(output, engine="xlsxwriter") as writer:
                    gpt_4o_mini.to_excel(writer, index=False, sheet_name="Results")
                output.seek(0)

                # ปุ่มดาวน์โหลด
                st.download_button(
                    label="Download as Excel",
                    data=output,
                    file_name="output_results.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
        else:
            st.write("Data mismatch, re-running data extraction.")
            # คุณสามารถเพิ่มโค้ดที่นี่เพื่อรันข้อมูลใหม่หากไม่ตรงกัน
else:
    st.info("Please enter your OpenAI API Key to proceed.")

