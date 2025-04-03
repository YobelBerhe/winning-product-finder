
from PIL import Image
import streamlit as st
import pandas as pd
import openai

# Display Logo
image = Image.open('A_2D_digital_graphic_design_presentation_features_.png')  # Path to your logo file
st.image(image, width=300)  # Adjust the width as needed

# Your existing code continues here...

import streamlit as st
import pandas as pd
import openai

st.set_page_config(page_title="Winning Product Toolkit", layout="wide")
st.title("📦 Ultimate Product Scoring & GPT Analysis Tool")

openai.api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")
mode = st.radio("Choose Scoring Mode:", ["Beginner Mode", "Pro Mode"])
uploaded_file = st.file_uploader("📁 Upload your Product Score Excel or CSV", type=["xlsx", "csv"])

def generate_prompt(row):
    return f"""
You're a dropshipping expert. This product has been evaluated across 33 different criteria.

Product: {row['Title']} | Category: {row['Category']}
Scores:
- Wow Factor: {row['Wow Factor']}
- Newness Score: {row['Newness Score']}
- Trend Alignment: {row['Trend Alignment']}
- Hobby Niche Fit: {row['Hobby Niche Fit']}
- Audience Understanding Score: {row['Audience Understanding Score']}
- Cross-Platform Trend: {row['Cross-Platform Trend']}
- Google Trends Trajectory: {row['Google Trends Trajectory']}
- Amazon Sales Rank: {row['Amazon Sales Rank']}
- Customer Review Insights: {row['Customer Review Insights']}
- Seasonal Demand Insight: {row['Seasonal Demand Insight']}
- Engagement: {row['Engagement']}
- Demonstrability Score: {row['Demonstrability Score']}
- Creative Versatility: {row['Creative Versatility']}
- Marketing Hook Strength: {row['Marketing Hook Strength']}
- Organic Sentiment Score: {row['Organic Sentiment Score']}
- Hashtag Popularity: {row['Hashtag Popularity']}
- Influencer Potential (IG): {row['Influencer Potential (IG)']}
- YouTube Review Presence: {row['YouTube Review Presence']}
- Perceived Value: {row['Perceived Value']}
- Impulse Price Match: {row['Impulse Price Match']}
- Profit Margin Room: {row['Profit Margin Room']}
- Shipping Efficiency: {row['Shipping Efficiency']}
- Reliable Fulfillment: {row['Reliable Fulfillment']}
- Repeatability Score: {row['Repeatability Score']}
- Scarcity Advantage Score: {row['Scarcity Advantage Score']}
- USP (Uniqueness): {row['USP (Uniqueness)']}
- Testing Simplicity: {row['Testing Simplicity']}

Please:
1. Analyze strengths and weaknesses
2. Suggest a TikTok hook idea
3. Give a Smart Recommendation

Respond clearly in 3 sections: Strengths & Weaknesses, Hook Idea, Recommendation.
"""

def get_gpt_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a senior dropshipping product analyst."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {e}"

if uploaded_file and openai.api_key:
    try:
        df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith("xlsx") else pd.read_csv(uploaded_file)
        st.success("✅ File loaded successfully!")

        if st.button("🔍 Analyze Products with GPT"):
            with st.spinner("Working GPT magic..."):
                df["GPT Feedback"] = df.apply(lambda row: get_gpt_response(generate_prompt(row)), axis=1)
                st.success("🎯 GPT Analysis Complete!")
                st.dataframe(df)

                output_file = "GPT_Verified_Product_Scores.xlsx"
                df.to_excel(output_file, index=False)
                with open(output_file, "rb") as f:
                    st.download_button("⬇️ Download Verified Excel", f, output_file, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        st.error(f"Error loading file: {e}")
else:
    st.info("Upload your product score file and enter your OpenAI key to begin.")
