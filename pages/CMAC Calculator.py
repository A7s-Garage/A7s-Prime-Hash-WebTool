import streamlit as st
import binascii
from cryptography.hazmat.primitives.cmac import CMAC
from cryptography.hazmat.primitives.ciphers import algorithms
from cryptography.hazmat.backends import default_backend

st.title("CMAC Generator")
st.subheader("Compute CMAC values using AES, 3DES, or Camellia with a user-provided hex key and message.")


# Valid key lengths (in bytes) for each algorithm
VALID_KEY_LENGTHS = {
    'AES - CMAC': [16, 24, 32],
    '3DES - CMAC': [16, 24],
    'Camellia - CMAC': [16, 24, 32],
}

def closest_valid_length(length, valid_lengths):
    """Return the closest valid key length to the given length."""
    return min(valid_lengths, key=lambda x: abs(x - length))

def compute_cmac(data: str, key: str, algorithm: str) -> str:
    """Compute the CMAC for the given data, key, and algorithm."""
    try:
        byte_data = data.encode('utf-8')
        byte_key = bytes.fromhex(key.strip())  # Key must be hex string

        valid_lengths = VALID_KEY_LENGTHS.get(algorithm, [])
        if len(byte_key) not in valid_lengths:
            return f"Error: {algorithm} key must be one of {valid_lengths} bytes. You provided {len(byte_key)} bytes."

        if algorithm == 'AES - CMAC':
            algo = algorithms.AES(byte_key)
        elif algorithm == '3DES - CMAC':
            algo = algorithms.TripleDES(byte_key)
        elif algorithm == 'Camellia - CMAC':
            algo = algorithms.Camellia(byte_key)
        else:
            return f"Error: Unsupported algorithm '{algorithm}'."

        c = CMAC(algo, backend=default_backend())
        c.update(byte_data)
        cmac_result = c.finalize()
        return binascii.hexlify(cmac_result).decode()

    except ValueError:
        return "Error: Invalid hex key or input data."
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit UI
col1, col2 = st.columns(2)

with col1:
    key_input = st.text_area(
        "Enter Key (hex)",
        height=150,
        help="Hex string, e.g. 2b7e151628aed2a6abf7158809cf4f3c"
    )
with col2:
    message_input = st.text_area(
        "Enter Message (text)",
        height=150,
        help="Plain text message to calculate CMAC for"
    )

algorithm = st.selectbox(
    "Select Algorithm",
    list(VALID_KEY_LENGTHS.keys())
)

# Validate and show key length info
try:
    key_bytes_len = len(bytes.fromhex(key_input.strip())) if key_input.strip() else 0
except Exception:
    key_bytes_len = 0

valid_lengths = VALID_KEY_LENGTHS[algorithm]
closest_len = closest_valid_length(key_bytes_len, valid_lengths)

#st.markdown(f"**Key length:** {key_bytes_len} bytes")
st.markdown(f"**Expected lengths for {algorithm}:** {valid_lengths} bytes")

if key_bytes_len != 0 and key_bytes_len not in valid_lengths:
    st.warning(f"Your key length is {key_bytes_len} bytes. Closest valid length is {closest_len} bytes.")

if st.button("Calculate CMAC"):
    if not key_input or not message_input:
        st.error("Please provide both key and message.")
    else:
        result = compute_cmac(message_input, key_input, algorithm)
        if result.startswith("Error"):
            st.error(result)
        else:
            st.success("✅ CMAC successfully calculated!")
            st.code(result, language='text')


st.markdown("""
---
### Supported Algorithms and Key Requirements

**AES (Advanced Encryption Standard)**  
- Symmetric block cipher widely used across industries.  
- Key sizes supported: **128, 192, or 256 bits** (16, 24, or 32 bytes).  
- Used here to generate CMAC (Cipher-based Message Authentication Code) for message integrity.

**3DES (Triple Data Encryption Standard)**  
- Legacy symmetric cipher applying DES encryption three times for increased security.  
- Key sizes supported: **128 or 192 bits** (16 or 24 bytes).  
- Used for CMAC generation on legacy systems or compatibility scenarios.

**Camellia**  
- Modern symmetric cipher comparable to AES in security and efficiency.  
- Key sizes supported: **128, 192, or 256 bits** (16, 24, or 32 bytes).  
- Used here to compute CMAC with a cipher alternative to AES.

---

**Note:**  
- Keys must be provided as hexadecimal strings of the correct length.  
- CMAC provides a way to verify message authenticity and integrity using the chosen block cipher.  
- Selecting an algorithm with an invalid key size will result in an error.

""")

