import openai
import streamlit as st
from PIL import Image
import pandas as pd

# Set the page config for Streamlit
st.set_page_config(page_title="Winning Product Toolkit", layout="wide")

# Display Logo
image = Image.open('A_2D_digital_graphic_design_presentation_features_.png')  # Path to your logo file
st.image(image, width=300)  # Adjust the width as needed

# Set up OpenAI API key
openai.api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")

# Mode selection for product scoring
mode = st.radio("Choose Scoring Mode:", ["Beginner Mode", "Pro Mode"])

# File upload for product score data
uploaded_file = st.file_uploader("📁 Upload your Product Score Excel or CSV", type=["xlsx", "csv"])

# Function to interact with OpenAI API
def get_gpt_response(prompt):
    try:
        response = openai.Completion.create(
            model="gpt-4",  # Using GPT-4 model
            prompt=prompt,  # The prompt you send to GPT
            temperature=0.4,  # Controls the randomness of the response
            max_tokens=1000  # Limits the length of the generated text
        )
        return response['choices'][0]['text'].strip()  # Extract and return the response text
    except Exception as e:
        return f"Error: {e}"

# Check if file is uploaded and analyze
if uploaded_file and openai.api_key:
    try:
        # Load the uploaded CSV or Excel file
        if uploaded_file.name.endswith("xlsx"):
            df = pd.read_excel(uploaded_file)
        else:
            df = pd.read_csv(uploaded_file)

        st.success("✅ File loaded successfully!")

        # Ensure columns have the same number of rows (no missing data)
        if df.isnull().values.any():
            st.error("⚠️ Your file contains missing values. Please fix and try again.")
        else:
            st.write(df)  # Display the uploaded data

            # Add a button to analyze the products using GPT after the file upload
            if st.button("🔍 Analyze Products with GPT"):
                with st.spinner("Analyzing products..."):
                    # Apply GPT analysis for each row in the file
                    df['GPT Feedback'] = df.apply(lambda row: get_gpt_response(generate_prompt(row)), axis=1)
                    st.success("🎯 Analysis Complete!")
                    st.dataframe(df)  # Display results
    except Exception as e:
        st.error(f"Error: {e}")

# Function to create the prompt for GPT
def generate_prompt(row):
    video_link = row['Video Link']
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
