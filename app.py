import streamlit as st
import pandas as pd

from utils.video import extract_video_id
from youtube_api import fetch_comments
from classifier import classify_comments


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="YouTube Comment Intelligence",
    page_icon="▶️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# YOUTUBE-STYLE CSS
# ============================================================

st.markdown("""
<style>

    /* Main page */
    .stApp {
        background-color: #ffffff;
    }

    /* Hide Streamlit default elements */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        visibility: hidden;
    }

    /* Main container */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1200px;
    }

    /* Header */
    .yt-header {
        display: flex;
        align-items: center;
        gap: 14px;
        margin-bottom: 5px;
    }

    .yt-logo {
        background-color: #ff0000;
        color: white;
        border-radius: 10px;
        padding: 7px 13px;
        font-size: 22px;
        font-weight: 800;
        line-height: 1;
    }

    .yt-title {
        font-size: 30px;
        font-weight: 700;
        color: #0f0f0f;
    }

    .yt-subtitle {
        color: #606060;
        font-size: 15px;
        margin-bottom: 25px;
    }

    /* URL box */
    .url-title {
        font-size: 18px;
        font-weight: 600;
        color: #0f0f0f;
        margin-bottom: 5px;
    }

    /* Analyze button */
    .stButton > button {
        background-color: #ff0000;
        color: white;
        border: none;
        border-radius: 22px;
        padding: 10px 24px;
        font-weight: 600;
        font-size: 15px;
        width: 100%;
        transition: 0.2s;
    }

    .stButton > button:hover {
        background-color: #cc0000;
        color: white;
        border: none;
    }

    /* Metrics */
    .metric-card {
        background: #f8f8f8;
        border: 1px solid #e5e5e5;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        margin-bottom: 10px;
    }

    .metric-number {
        font-size: 30px;
        font-weight: 700;
        color: #0f0f0f;
    }

    .metric-label {
        color: #606060;
        font-size: 14px;
        margin-top: 4px;
    }

    /* Section headings */
    .section-title {
        font-size: 22px;
        font-weight: 700;
        color: #0f0f0f;
        margin-top: 30px;
        margin-bottom: 15px;
    }

    /* Category cards */
    .category-card {
        background: #f9f9f9;
        border: 1px solid #e5e5e5;
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 10px;
    }

    .category-name {
        font-weight: 600;
        color: #0f0f0f;
    }

    .category-value {
        font-size: 20px;
        font-weight: 700;
        color: #ff0000;
    }

    /* Comment card */
    .comment-card {
        background: #f9f9f9;
        border-radius: 10px;
        padding: 13px 16px;
        margin: 8px 0;
        border: 1px solid #eeeeee;
        color: #0f0f0f;
        font-size: 15px;
        line-height: 1.5;
    }

    /* Video ID */
    .video-id {
        background: #f2f2f2;
        padding: 10px 14px;
        border-radius: 8px;
        font-family: monospace;
        color: #606060;
        margin: 10px 0 15px 0;
    }

    /* Divider */
    .red-line {
        height: 3px;
        background: #ff0000;
        border-radius: 5px;
        margin: 15px 0 25px 0;
    }

    /* Footer */
    .footer {
        text-align: center;
        color: #606060;
        font-size: 13px;
        margin-top: 40px;
        padding-top: 20px;
        border-top: 1px solid #eeeeee;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# SESSION STATE
# ============================================================

if "df" not in st.session_state:
    st.session_state.df = None

if "video_id" not in st.session_state:
    st.session_state.video_id = None


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="yt-header">
    <div class="yt-logo">▶</div>
    <div class="yt-title">YouTube Comment Intelligence</div>
</div>

<div class="yt-subtitle">
    Analyze, classify and explore YouTube comments using machine learning.
</div>

<div class="red-line"></div>
""", unsafe_allow_html=True)


# ============================================================
# URL INPUT
# ============================================================

st.markdown(
    '<div class="url-title">🔗 YouTube Video URL</div>',
    unsafe_allow_html=True
)

video_url = st.text_input(
    "YouTube URL",
    placeholder="Paste your YouTube video URL here...",
    label_visibility="collapsed"
)


# ============================================================
# VIDEO ANALYSIS
# ============================================================

if video_url:

    video_id = extract_video_id(video_url)

    if video_id:

        st.markdown(
            f"""
            <div class="video-id">
                Video ID: {video_id}
            </div>
            """,
            unsafe_allow_html=True
        )

        analyze = st.button(
            "▶ Analyze Video"
        )

        if analyze:

            try:

                # -------------------------------
                # Fetch comments
                # -------------------------------

                with st.spinner(
                    "Fetching YouTube comments..."
                ):

                    comments_df = fetch_comments(
                        video_id
                    )

                if comments_df.empty:

                    st.warning(
                        "No comments were found for this video."
                    )

                    st.session_state.df = None

                else:

                    st.success(
                        f"✅ Fetched {len(comments_df):,} comments"
                    )

                    # -------------------------------
                    # Classify comments
                    # -------------------------------

                    with st.spinner(
                        "Classifying comments..."
                    ):

                        classified_df = classify_comments(
                            comments_df
                        )

                    st.session_state.df = classified_df
                    st.session_state.video_id = video_id

                    st.success(
                        "✅ Comment analysis completed!"
                    )

            except Exception as e:

                st.error(
                    "❌ An error occurred while analyzing the video."
                )

                st.exception(e)

    else:

        st.error(
            "❌ Invalid YouTube URL. Please check the link."
        )


# ============================================================
# DISPLAY RESULTS
# ============================================================

if st.session_state.df is not None:

    df = st.session_state.df

    st.markdown(
        '<div class="section-title">📊 Overview</div>',
        unsafe_allow_html=True
    )


    # ========================================================
    # METRICS
    # ========================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-number">
                    {len(df):,}
                </div>
                <div class="metric-label">
                    💬 Total Comments
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with col2:

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-number">
                    {df["Category"].nunique()}
                </div>
                <div class="metric-label">
                    🏷️ Categories Found
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    with col3:

        if len(df) > 0:

            most_common = (
                df["Category"]
                .value_counts()
                .idxmax()
            )

        else:

            most_common = "None"

        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-number">
                    {most_common}
                </div>
                <div class="metric-label">
                    ⭐ Most Common Category
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # CATEGORY DISTRIBUTION
    # ========================================================

    st.markdown(
        '<div class="section-title">📈 Comment Distribution</div>',
        unsafe_allow_html=True
    )

    counts = df["Category"].value_counts()

    st.bar_chart(
        counts,
        height=350
    )


    # ========================================================
    # CATEGORY PERCENTAGES
    # ========================================================

    st.markdown(
        '<div class="section-title">📊 Category Breakdown</div>',
        unsafe_allow_html=True
    )

    total = len(df)

    categories = [
        "Positive",
        "Negative",
        "Neutral",
        "Question",
        "Suggestion",
        "Spam",
        "Toxic"
    ]

    available_categories = [
        category
        for category in categories
        if category in df["Category"].unique()
    ]

    # Display category cards in columns

    for i in range(
        0,
        len(available_categories),
        3
    ):

        cols = st.columns(3)

        for j, category in enumerate(
            available_categories[i:i + 3]
        ):

            count = int(
                counts.get(
                    category,
                    0
                )
            )

            percentage = round(
                (count / total) * 100,
                2
            )

            with cols[j]:

                st.markdown(
                    f"""
                    <div class="category-card">
                        <div class="category-name">
                            {category}
                        </div>
                        <div class="category-value">
                            {percentage}%
                        </div>
                        <div style="color:#606060;">
                            {count:,} comments
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


    # ========================================================
    # COMMENTS BY CATEGORY
    # ========================================================

    st.markdown(
        '<div class="section-title">💬 Comments by Category</div>',
        unsafe_allow_html=True
    )

    # IMPORTANT:
    # Only categories actually present in the dataframe

    selected = st.selectbox(
        "Choose a category",
        available_categories,
        label_visibility="collapsed"
    )

    filtered = df[
        df["Category"] == selected
    ].copy()

    # Show the most-liked comments first when like data is available
    if "Likes" in filtered.columns:
        filtered["Likes"] = pd.to_numeric(
            filtered["Likes"], errors="coerce"
        ).fillna(0).astype(int)
        filtered = filtered.sort_values(
            by="Likes", ascending=False, kind="stable"
        )

    st.markdown(
        f"""
        <div style="
            font-size:18px;
            font-weight:600;
            margin:15px 0;
        ">
            {selected} Comments:
            <span style="color:#ff0000;">
                {len(filtered):,}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # DISPLAY COMMENTS
    # ========================================================

    if filtered.empty:

        st.info(
            "No comments found in this category."
        )

    else:

        # Show comments
        # Use a scrollable container for many comments

        with st.container(
            height=500
        ):

            for _, row in filtered.iterrows():

                comment = row["Comment"]
                likes = int(row.get("Likes", 0))

                st.markdown(
                    f"""
                    <div class="comment-card" style="
                        display:flex;
                        align-items:center;
                        justify-content:space-between;
                        gap:20px;
                    ">
                        <div style="flex:1; min-width:0;">
                            💬 {comment}
                        </div>
                        <div style="
                            flex-shrink:0;
                            font-weight:600;
                            font-size:15px;
                            color:#0f0f0f;
                            white-space:nowrap;
                        ">
                            👍 {likes:,}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )


    # ========================================================
    # DOWNLOAD
    # ========================================================

    st.markdown(
        '<div class="section-title">⬇️ Download Results</div>',
        unsafe_allow_html=True
    )

    csv = df.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="⬇️ Download Classified Comments",
        data=csv,
        file_name="classified_comments.csv",
        mime="text/csv"
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        🎥 YouTube Comment Intelligence
        <br>
        Analyze • Classify • Understand
    </div>
    """,
    unsafe_allow_html=True
)
