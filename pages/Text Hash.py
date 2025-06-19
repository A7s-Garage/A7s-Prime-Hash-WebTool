import streamlit as st
import hashlib

st.title("Text Hash Generator")
st.subheader("Encode your input text and compute its hash using various algorithms and encodings")

col1, col2 = st.columns(2)

with col1:
    input_text = st.text_area("Input Text", height=150)

with col2:
    output_hash = ""

# Common encodings and hash functions
encodings = [
    "utf-8", "ascii", "latin-1", "utf-16", "utf-32", 
    "cp1252", "iso-8859-1", "mac_roman", "utf-7", "big5", "gb2312"
]
hash_algos = sorted(hashlib.algorithms_guaranteed)

# Row with encoding and hash function selectors
ec1, ec2 = st.columns(2)
with ec1:
    selected_encoding = st.selectbox("Encoding", encodings, key="enc")
with ec2:
    selected_hash = st.selectbox("Hash Function", hash_algos, key="hash")

# Compute button
compute = st.button("Compute")

# Hashing logic
if compute:
    if not input_text.strip():
        st.warning("Please enter some input text to hash.")
    else:
        try:
            encoded_text = input_text.encode(selected_encoding)
            h = hashlib.new(selected_hash)
            h.update(encoded_text)

            if selected_hash.startswith("shake_"):
                output_hash = h.hexdigest(64)
            else:
                output_hash = h.hexdigest()

            st.session_state.output_hash = output_hash

        except LookupError:
            st.warning(f"Encoding '{selected_encoding}' is not supported.")
        except UnicodeEncodeError as e:
            st.warning(f"Encoding error: {e}")
        except Exception as e:
            st.warning(f"Unexpected issue: {e}")

# Use stored hash if no new hash computed
if "output_hash" in st.session_state and not output_hash:
    output_hash = st.session_state.output_hash

# Show the result
col2.text_area("Output Hash", height=150, value=output_hash, disabled=True, key="output_hash_display")


st.write("---")

st.markdown("""
<h3>Hash Functions</h3>
<ul>
<li><b>MD5:</b> One of the earliest widely-used cryptographic hash functions producing a 128-bit hash. It is fast but considered cryptographically broken and unsuitable for security purposes due to vulnerabilities to collision attacks.</li>

<li><b>SHA-1:</b> Produces a 160-bit hash and was once widely used for digital signatures and certificates. However, SHA-1 is now considered weak because practical collision attacks have been demonstrated, so its use is discouraged in favor of stronger algorithms.</li>

<li><b>SHA-2 Family (SHA-224, SHA-256, SHA-384, SHA-512):</b> These are currently the most popular secure hash functions. They produce hashes of different lengths (e.g., SHA-256 produces 256-bit hashes) and are widely used for data integrity, password hashing (with salt), and digital signatures.</li>

<li><b>SHA-3 Family and SHAKE:</b> SHA-3 is the latest standard hash function family based on the Keccak algorithm, designed to be resistant to various attacks and to offer an alternative to SHA-2. SHAKE (SHA-3 Extendable-Output Functions) produces hashes of arbitrary length, which is useful for applications requiring variable-length digests like key derivation.</li>
</ul>

<h3>Important Cryptographic Properties of Hash Functions</h3>
<ul>
<li><b>Deterministic:</b> The same input always produces the same hash output.</li>

<li><b>Fixed Output Size:</b> Regardless of the input size, hash functions produce a fixed-length digest (e.g., 256 bits for SHA-256).</li>

<li><b>Preimage Resistance:</b> Given a hash output, it should be computationally infeasible to find any input that hashes to that output.</li>

<li><b>Collision Resistance:</b> It should be computationally infeasible to find two different inputs that produce the same hash output.</li>

<li><b>Avalanche Effect:</b> A small change in input drastically changes the output hash, making it appear random.</li>
</ul>

<p><b>Summary:</b> While MD5 and SHA-1 are mostly obsolete for security-sensitive tasks, SHA-2 and SHA-3 (including SHAKE) provide strong cryptographic guarantees and are recommended for most modern applications.</p>
""", unsafe_allow_html=True)
