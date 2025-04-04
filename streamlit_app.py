import streamlit as st
from PIL import Image
import pandas as pd
import openai

# Set the page config FIRST
st.set_page_config(page_title="Winning Product Toolkit", layout="wide")

# Display Logo
image = Image.open('A_2D_digital_graphic_design_presentation_features_.png')  # Path to your logo file
st.image(image, width=300)  # Adjust the width as needed

# Set up OpenAI API key
openai.api_key = st.text_input("🔑 Enter your OpenAI API Key", type="password")

# Upload file
uploaded_file = st.file_uploader("📁 Upload your Product Score Excel or CSV", type=["xlsx", "csv"])

if uploaded_file:
    try:
        # Load the uploaded file based on its extension (CSV or Excel)
        if uploaded_file.name.endswith('csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith('xlsx'):
            df = pd.read_excel(uploaded_file)

        st.success("✅ File loaded successfully!")

        # List of required columns for processing
        required_columns = [
            'Title', 'Category', 'Wow Factor', 'Newness Score', 'Trend Alignment', 
            'Hobby Niche Fit', 'Audience Understanding Score', 'Cross-Platform Trend', 
            'Google Trends Trajectory', 'Amazon Sales Rank', 'Customer Review Insights', 
            'Seasonal Demand Insight', 'Engagement', 'Demonstrability Score', 'Creative Versatility', 
            'Marketing Hook Strength', 'Organic Sentiment Score', 'Hashtag Popularity', 
            'Influencer Potential (IG)', 'YouTube Review Presence', 'Perceived Value', 
            'Impulse Price Match', 'Profit Margin Room', 'Shipping Efficiency', 
            'Reliable Fulfillment', 'Repeatability Score', 'Scarcity Advantage Score', 
            'USP (Uniqueness)', 'Testing Simplicity', 'Video Link'
        ]

        # Check if all required columns are present
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.error(f"The uploaded file is missing the following columns: {', '.join(missing_columns)}")
        else:
            # If columns are correct, filter the DataFrame to include only the relevant columns
            filtered_df = df[['Title', 'Category', 'Wow Factor', 'Newness Score', 'Trend Alignment', 
                              'Hobby Niche Fit', 'Audience Understanding Score', 'Cross-Platform Trend', 
                              'Google Trends Trajectory', 'Amazon Sales Rank', 'Customer Review Insights', 
                              'Seasonal Demand Insight', 'Engagement', 'Demonstrability Score', 'Creative Versatility', 
                              'Marketing Hook Strength', 'Organic Sentiment Score', 'Hashtag Popularity', 
                              'Influencer Potential (IG)', 'YouTube Review Presence', 'Perceived Value', 
                              'Impulse Price Match', 'Profit Margin Room', 'Shipping Efficiency', 
                              'Reliable Fulfillment', 'Repeatability Score', 'Scarcity Advantage Score', 
                              'USP (Uniqueness)', 'Testing Simplicity', 'Video Link']]

            # Save the filtered DataFrame to an Excel file
            output_file_filtered = "Filtered_Product_Evaluation_Parameters.xlsx"
            filtered_df.to_excel(output_file_filtered, index=False)

            # Display download button for the new Excel sheet in Streamlit
            with open(output_file_filtered, "rb") as f:
                st.download_button("⬇️ Download Filtered Product Evaluation Parameters", f, output_file_filtered, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    except Exception as e:
        st.error(f"Error loading file: {e}")
else:
    st.info("Upload your product score file and enter your OpenAI key to begin.")
