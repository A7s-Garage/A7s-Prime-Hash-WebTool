import streamlit as st

st.set_page_config(page_title="A7's Prime Hash WebTool", layout="wide", page_icon="#️⃣")

st.title("A7's Prime Hash WebTool")

st.markdown(
    """
    <style>
    /* More generic selector to limit width */
    .stApp > main > div {
        max-width: 90% !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <style>
    .stApp {
        height: 100vh;
        margin: 0;
        background: linear-gradient(-45deg, #a1c4fd, #c2e9fb, #fbc687, #f5c06f);
        background-size: 400% 400%;
        animation: gradientBG 25s ease infinite;
        color: #000;
    }

    @keyframes gradientBG {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }

    .marquee-wrapper {
        overflow: hidden;
        width: 100%;
        box-sizing: border-box;
        padding: 10px 0;
    }

    .marquee-content {
        display: inline-flex;
        gap: 20px;
        padding-left: 100%;
        animation: marquee 25s linear infinite;
        white-space: nowrap;
    }

    .marquee-box {
        background: rgba(255, 255, 255, 0.7);
        border-radius: 15px;
        padding: 8px 16px;
        font-weight: 600;
        font-size: 1.1rem;
        color: #000;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        user-select: none;
        white-space: nowrap;
    }

    @keyframes marquee {
        0% {
            transform: translateX(0%);
        }
        100% {
            transform: translateX(-100%);
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="marquee-wrapper">
      <div class="marquee-content">
        <div class="marquee-box">🔐 Classical Cipher</div>
        <div class="marquee-box">📦 Padding & Unpadding</div>
        <div class="marquee-box">🔄 Encoding Converter</div>
        <div class="marquee-box">🎯 CMAC Calculator</div>
        <div class="marquee-box">🔑 HMAC Generator</div>
        <div class="marquee-box">🧬 Key Derivation Functions</div>
        <div class="marquee-box">✍️ Digital Signature Generator</div>
        <div class="marquee-box">🗂️ File Hash</div>
        <div class="marquee-box">📝 Text Hash</div>
        <div class="marquee-box">🖼️ Image Hash</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    """
    <style>
    .sticky-sidebar {
        position: sticky;
        bottom: 0;
        background: white;
        padding: 10px;
        font-size: 14px;
        color: #555;
        font-weight: 500;
        border-top: 1px solid #ddd;
        margin-top: 20px;
        z-index: 100;
    }
    </style>
    <div class="sticky-sidebar">
        By <strong>Patnam Kannabhiram</strong><br>
        From <em>A7's Garage</em>
    </div>
    """,
    unsafe_allow_html=True,
)


# Welcome paragraph (full width)
st.markdown(
    """
    <br>
    <p style="font-size:20px; font-weight: 500;">
    Welcome, folks! This tool helps you with various cryptography tasks like hashing text and files, converting encodings, and working with classical ciphers. It’s easy to use and designed for anyone interested in exploring or using basic cryptographic functions quickly and reliably. Have a nice day!
    </p>
    """,
    unsafe_allow_html=True,
)

# Columns for line below paragraph
col1, col2 = st.columns([4, 1])
with col1:
    st.markdown(
        """
        <p style="font-size:20px; color: #333; margin-top: 10px;">
        You’re using the online version — try our system software too, it’s free!<br>
        The software contains <b>File</b>, <b>Folder</b>, <b>Image</b>, <b>Disk hash</b>, and comparisons only.
        </p>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <a href="https://archive.org/details/a7s-prime-hash-calculator" target="_blank" style="
            display: inline-block;
            padding: 8px 16px;
            background-color: #4CAF50;
            color: white;
            text-align: center;
            text-decoration: none;
            font-weight: 600;
            border-radius: 5px;
            cursor: pointer;
        ">
            Download Now
        </a>
        """,
        unsafe_allow_html=True,
    )


st.markdown(
    """
    <br><br><br>
    <p style="font-size:18px; font-weight: 500; margin-top: 20px;">
    Programmed by <strong>Patnam Kannabhiram</strong><br>
    For Suggestions or Bugs, contact: 
    <a href="mailto:a7sgarage@gmail.com">a7sgarage@gmail.com</a>, 
    <a href="mailto:patnamkannabhiram@gmail.com">patnamkannabhiram@gmail.com</a>
    </p>
    """,
    unsafe_allow_html=True,
)

