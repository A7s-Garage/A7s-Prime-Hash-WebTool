import streamlit as st
import codecs
import encodings
import pkgutil


st.title("Text Encoding Converter")
st.subheader("Encode your text into various Encodings.")


# --- Utils ---
def get_all_encodings():
    """Get a list of all available text encodings in Python."""
    encodings_list = set()
    for _, modname, _ in pkgutil.iter_modules(encodings.__path__):
        encodings_list.add(modname)
    return sorted(encodings_list)

def encode_text(text, encoding):
    """Encode text using the selected encoding. Handles both standard and codec-based encodings."""
    try:
        if encoding.endswith('_codec') or encoding in {'base64', 'hex', 'bz2', 'quopri', 'uu', 'zlib'}:
            byte_input = text.encode('utf-8')
            encoded_bytes = codecs.encode(byte_input, encoding)
            return encoded_bytes.decode('utf-8', errors='replace')
        else:
            return text.encode(encoding).decode(encoding)
    except Exception as e:
        return f"[Encoding Error]: {e}"


# Initialize session state once
if "encoded_output" not in st.session_state:
    st.session_state["encoded_output"] = ""

# Layout: Two text boxes side by side
col1, col2 = st.columns(2)

with col1:
    raw_text = st.text_area("✏️ Raw Text Input", height=300, key="raw_input")

with col2:
    st.text_area("🧪 Encoded Output", value=st.session_state["encoded_output"], height=300, disabled=True)

# Dropdown and Convert Button
col_dropdown, col_button = st.columns([3, 1])

with col_dropdown:
    all_encodings = get_all_encodings()
    selected_encoding = st.selectbox("Select Encoding", all_encodings, key="encoding_selectbox")

with col_button:
    st.markdown("<div style='margin-top: 28px'></div>", unsafe_allow_html=True)
    if st.button("🔁 Convert", key="convert_button"):
        st.session_state["encoded_output"] = encode_text(raw_text, selected_encoding)



st.write("---")
st.markdown("""
<h2>About Text Encodings</h2>
<p>Text encoding is the process of converting text into bytes using various character encodings. Different encodings represent characters differently, which affects how text is stored, transmitted, and displayed.</p>

<h3>Common Text Encodings</h3>
<ul>
<li><b>UTF-8:</b> Most popular encoding for Unicode, supports all characters, variable length (1-4 bytes).</li>
<li><b>ASCII:</b> Basic encoding for English characters (0-127), single byte per character.</li>
<li><b>ISO-8859-1 (Latin-1):</b> Extends ASCII for Western European languages.</li>
<li><b>UTF-16 & UTF-32:</b> Fixed-length Unicode encodings, larger than UTF-8 but easier for some languages.</li>
</ul>

<h3>Special Codecs</h3>
<ul>
<li><b>base64:</b> Encodes binary data into ASCII characters, commonly used in email and web data transfer.</li>
<li><b>hex:</b> Represents binary data as hexadecimal characters.</li>
<li><b>bz2, zlib:</b> Compression codecs that encode data into compressed formats.</li>
</ul>

<p><b>Note:</b> Always choose the right encoding for your use case to avoid data corruption or loss. This tool helps you convert text between many encodings to test compatibility and correctness.</p>
""", unsafe_allow_html=True)

