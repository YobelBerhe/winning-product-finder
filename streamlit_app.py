# Set the page config FIRST
import streamlit as st
from PIL import Image
import pandas as pd
import openai

# Set the page config for streamlit
st.set_page_config(page_title="Winning Product Toolkit", layout="wide")

# Display Logo
image = Image.open('A_2D_digital_graphic_design_presentation_features_.png')  # Path to your logo file
st.image(image, width=300)  # Adjust the width as needed

# Set up OpenAI API key
openai.api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")
mode = st.radio("Choose Scoring Mode:", ["Beginner Mode", "Pro Mode"])
uploaded_file = st.file_uploader("📁 Upload your Product Score Excel or CSV", type=["xlsx", "csv"])

# Display Table for Product Evaluation Parameters
st.markdown("""
### 30 Product Evaluation Parameters

| **Parameter**               | **What It Means**                                                              | **Why It Matters**                                                       | **What It Tells You**                                 | **Score 1-2 (Low)**                            | **Score 4-6 (Medium)**                          | **Score 7-10 (High)**                           |
|-----------------------------|--------------------------------------------------------------------------------|------------------------------------------------------------------------|------------------------------------------------------|-------------------------------------------------|-------------------------------------------------|--------------------------------------------------|
| **Wow Factor**               | How unique and visually appealing the product is.                              | Determines the initial attraction and interest it generates.            | Attractiveness to users, first impressions.           | The product is generic or lacks appeal.       | Moderately appealing with some visual impact.   | Highly eye-catching, unique, and visually stunning.|
| **Newness Score**            | How new or innovative the product is in the market.                           | New products tend to attract more attention and higher demand.          | Market interest and trend potential.                  | Very old product with no novelty.             | Moderately new product with some uniqueness.    | Fresh and innovative product with high appeal.  |
| **Trend Alignment**          | How well the product fits with current trends.                               | Products in line with trends have higher viral potential.               | Market demand and current relevance.                  | Product is outdated or irrelevant.            | Fits some current trends, but not very strong.  | Perfectly aligned with current hot trends.      |
| **Hobby Niche Fit**          | How well the product fits into specific hobbies or interests.                | Niche products often have high conversion rates and passionate buyers.  | Potential target audience and loyalty.                | No connection to hobbies or interests.        | Fits some hobbies, but niche appeal is moderate.| Strong fit for a passionate hobbyist market.    |
| **Audience Understanding**   | How well the product matches the needs of its target audience.              | Crucial for conversion as it meets customer desires.                    | Alignment with customer pain points or desires.       | Doesn't meet the needs of the target audience.| Addresses some customer needs but with gaps.   | Fully meets the target audience's needs.        |
""")

# Define the 33 Parameters for GPT
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

# When the file is uploaded and the API key is entered
if uploaded_file and openai.api_key:
    try:
        df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith("xlsx") else pd.read_csv(uploaded_file)
        st.success("✅ File loaded successfully!")

        # Show the button for analysis
        if st.button("🔍 Analyze Products with GPT"):
            with st.spinner("Working GPT magic..."):
                # Apply GPT scoring and commentary
                df["GPT Feedback"] = df.apply(lambda row: get_gpt_response(generate_prompt(row)), axis=1)
                st.success("🎯 GPT Analysis Complete!")
                st.dataframe(df)

                # Prepare the output Excel file
                output_file = "GPT_Verified_Product_Scores.xlsx"
                df.to_excel(output_file, index=False)
                with open(output_file, "rb") as f:
                    st.download_button("⬇️ Download Verified Excel", f, output_file, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        st.error(f"Error loading file: {e}")
else:
    st.info("Upload your product score file and enter your OpenAI key to begin.")


# Generate Excel File for Download
# Define the 33 Product Evaluation Parameters for download
data = {
    "Title": ["Product 1", "Product 2"],  # Add titles of your products
    "Category": ["Category A", "Category B"],  # Add categories of your products
    "Wow Factor": [8, 7],  # Add scores for each parameter
    "Newness Score": [7, 6],  # Continue for each parameter
    "Trend Alignment": [9, 8],
    "Hobby Niche Fit": [6, 7],
    "Audience Understanding Score": [8, 6],
    "Cross-Platform Trend": [7, 8],
    "Google Trends Trajectory": [9, 7],
    "Amazon Sales Rank": [8, 6],
    "Customer Review Insights": [7, 6],
    "Seasonal Demand Insight": [9, 8],
    "Engagement": [8, 7],
    "Demonstrability Score": [9, 7],
    "Creative Versatility": [8, 7],
    "Marketing Hook Strength": [7, 8],
    "Organic Sentiment Score": [9, 7],
    "Hashtag Popularity": [8, 7],
    "Influencer Potential (IG)": [9, 8],
    "YouTube Review Presence": [8, 7],
    "Perceived Value": [9, 8],
    "Impulse Price Match": [7, 6],
    "Profit Margin Room": [8, 9],
    "Shipping Efficiency": [7, 8],
    "Reliable Fulfillment": [9, 7],
    "Repeatability Score": [8, 7],
    "Scarcity Advantage Score": [9, 8],
    "USP (Uniqueness)": [8, 7],
    "Testing Simplicity": [7, 9],
    "Video Link": ["https://tiktok.com/xyz", "https://instagram.com/xyz"]  # Add video links
}

# Convert data into DataFrame
filtered_df = pd.DataFrame(data)

# Save the DataFrame to an Excel file
output_file_filtered = "Filtered_Product_Evaluation_Parameters.xlsx"
filtered_df.to_excel(output_file_filtered, index=False)

# Display download button for the new Excel sheet in Streamlit
with open(output_file_filtered, "rb") as f:
    st.download_button("⬇️ Download Filtered Product Evaluation Parameters", f, output_file_filtered, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
