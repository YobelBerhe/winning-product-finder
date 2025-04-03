# Set the page config FIRST
import streamlit as st
from PIL import Image
import pandas as pd
import openai

st.set_page_config(page_title="Winning Product Toolkit", layout="wide")

# Display Logo
image = Image.open('A_2D_digital_graphic_design_presentation_features_.png')  # Path to your logo file
st.image(image, width=300)  # Adjust the width as needed

# Set up OpenAI API key
openai.api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")
mode = st.radio("Choose Scoring Mode:", ["Beginner Mode", "Pro Mode"])
uploaded_file = st.file_uploader("📁 Upload your Product Score Excel or CSV", type=["xlsx", "csv"])

# Define the 33 Parameters
def generate_prompt(row):
    video_link = row['Video Link']
    
    # Build prompt for GPT
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

    Video Link: {video_link}

    Please:
    1. Analyze the video link and provide a sentiment/engagement analysis.
    2. Analyze the product's strengths and weaknesses based on the provided data.
    3. Suggest a TikTok/Instagram marketing hook idea.
    4. Give a Smart Recommendation on the product.

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
                # Apply GPT scoring and commentary
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
