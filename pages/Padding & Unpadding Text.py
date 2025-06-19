import streamlit as st
import os


st.title("🔐 Padding & Unpadding Tool")
st.subheader("Apply and remove various padding schemes on UTF-8 text")


# --- Padding functions ---
def pkcs7_pad(data: bytes, block_size: int) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([pad_len] * pad_len)

def pkcs7_unpad(data: bytes) -> bytes:
    pad_len = data[-1]
    if pad_len < 1 or pad_len > len(data):
        raise ValueError("Invalid padding length")
    if data[-pad_len:] != bytes([pad_len] * pad_len):
        raise ValueError("Invalid PKCS7 padding bytes")
    return data[:-pad_len]

def zero_pad(data: bytes, block_size: int) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([0] * pad_len)

def zero_unpad(data: bytes) -> bytes:
    return data.rstrip(b'\x00')

def ansi_x923_pad(data: bytes, block_size: int) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    return data + bytes([0] * (pad_len - 1)) + bytes([pad_len])

def ansi_x923_unpad(data: bytes) -> bytes:
    pad_len = data[-1]
    if pad_len < 1 or pad_len > len(data):
        raise ValueError("Invalid padding length")
    if data[-pad_len:-1] != bytes([0] * (pad_len - 1)):
        raise ValueError("Invalid ANSI X.923 padding")
    return data[:-pad_len]

def iso_10126_pad(data: bytes, block_size: int) -> bytes:
    pad_len = block_size - (len(data) % block_size)
    return data + os.urandom(pad_len - 1) + bytes([pad_len])

def iso_10126_unpad(data: bytes) -> bytes:
    pad_len = data[-1]
    if pad_len < 1 or pad_len > len(data):
        raise ValueError("Invalid padding length")
    return data[:-pad_len]

# --- Padding registry ---
paddings = {
    "PKCS7": (pkcs7_pad, pkcs7_unpad),
    "Zero": (zero_pad, zero_unpad),
    "ANSI X.923": (ansi_x923_pad, ansi_x923_unpad),
    "ISO 10126": (iso_10126_pad, iso_10126_unpad),
}


if "action" not in st.session_state:
    st.session_state.action = "Pad"

col1, col2 = st.columns(2)

with col1:
    st.header("Input")


    block_size = st.number_input("Block size (bytes)", min_value=1, max_value=256, value=16, step=1)

    #st.info(f"📦 Selected Block Size: `{block_size}` bytes")

    if block_size not in [8, 16, 32, 64]:
        st.warning("⚠️ Non-standard block size. Recommended: 8, 16, 32, or 64 bytes (used by most ciphers).")

    padding_type = st.selectbox("Padding Algorithm", list(paddings.keys()), key="padding_type")

    input_placeholder = (
        "Enter text to pad (UTF-8):"
        if st.session_state.action == "Pad"
        else "Enter padded data as hex string (e.g. 48656c6c6f030303):"
    )
    input_text = st.text_area(input_placeholder, key="input_text", height=150)

    radio_col, button_col = st.columns([1, 1])
    with radio_col:
        action_choice = st.radio(
            "Action", ("Pad", "Unpad"),
            index=0 if st.session_state.action == "Pad" else 1,
            key="action_radio",
            horizontal=True,
            on_change=lambda: st.session_state.update({"action": st.session_state.action_radio})
        )

    with button_col:
        st.markdown("<br>", unsafe_allow_html=True)
        compute = st.button("🔄 Compute", use_container_width=True)

    if compute:
        try:
            pad_func, unpad_func = paddings[st.session_state.padding_type]
            action = st.session_state.action

            if action == "Pad":
                input_bytes = input_text.encode("utf-8")
                output_bytes = pad_func(input_bytes, block_size)
            else:
                hex_clean = ''.join(input_text.split())
                if len(hex_clean) == 0 or len(hex_clean) % 2 != 0:
                    raise ValueError("Input hex string must be even-length and not empty")
                try:
                    input_bytes = bytes.fromhex(hex_clean)
                except ValueError as e:
                    raise ValueError(f"Invalid hex input: {e}")
                output_bytes = unpad_func(input_bytes)

            st.session_state["output_hex"] = output_bytes.hex()
            st.session_state["output_text"] = (
                output_bytes.decode("utf-8") if action == "Unpad" else ""
            )
            st.session_state["error"] = None
        except Exception as e:
            st.session_state["output_hex"] = ""
            st.session_state["output_text"] = ""
            st.session_state["error"] = str(e)

with col2:
    st.header("Output")

    if st.session_state.get("error"):
        st.error(f"❌ Error: {st.session_state['error']}")

    st.text_area("📦 Output (Hex)", value=st.session_state.get("output_hex", ""), height=150)

    if st.session_state.get("output_text"):
        st.text_area("📝 Decoded Output (UTF-8)", value=st.session_state["output_text"], height=100)


st.write("---")
st.markdown("""
<h2>About Padding Schemes</h2>
<p>Padding schemes are used to extend plaintext data so it fits block size requirements of block ciphers or cryptographic algorithms.</p>

<h3>PKCS7</h3>
<ul>
<li>Common padding for block ciphers like AES.</li>
<li>Pad bytes all have the same value equal to the number of padding bytes.</li>
<li>Can unambiguously detect and remove padding.</li>
</ul>

<h3>Zero Padding</h3>
<ul>
<li>Pads with zero (null) bytes.</li>
<li>Simple but ambiguous if plaintext ends with zero bytes.</li>
<li>Mostly used in fixed-length or binary data.</li>
</ul>

<h3>ANSI X.923</h3>
<ul>
<li>Pads with zeros except last byte indicates padding length.</li>
<li>Useful for binary data; easy to unpad.</li>
</ul>

<h3>ISO 10126</h3>
<ul>
<li>Pads with random bytes except last byte indicates padding length.</li>
<li>More secure padding; harder to guess padding bytes.</li>
<li>Mostly deprecated and replaced by other schemes.</li>
</ul>

<p><b>Note:</b> Always ensure the block size matches your cipher or algorithm requirement. Incorrect padding or block sizes can cause decryption errors or security issues.</p>
""", unsafe_allow_html=True)
