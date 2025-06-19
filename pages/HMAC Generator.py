import streamlit as st
import hmac
import hashlib

st.title("HMAC Generator")
st.subheader("Calculate HMAC digests using various hash algorithms securely with your secret key")


hash_algorithms = {
    f"HMAC-{algo.upper()}": getattr(hashlib, algo)
    for algo in sorted(hashlib.algorithms_guaranteed)
    if callable(getattr(hashlib, algo, None)) and "shake" not in algo
}

# UI Layout
col1, col2 = st.columns(2)

# Left column: Inputs
with col1:
    st.subheader("🔤 Message & Key Input")
    message = st.text_area("Message", height=200)
    key = st.text_input("Key (secret)", type="password")

    st.subheader("🔧️ HMAC Settings")

    # Side-by-side dropdown and button with equal width
    col_algo, col_button = st.columns([1, 1])
    with col_algo:
        algo_selected = st.selectbox(
            "🔽 Select HMAC Algorithm",
            list(hash_algorithms.keys()),
            label_visibility="collapsed"
        )
    with col_button:
        calculate = st.button("Calculate HMAC", use_container_width=True)

    # HMAC calculation
    hmac_result = ""
    if calculate:
        if not message or not key:
            st.warning("⚠️ Please enter both a message and a key.")
        else:
            try:
                digestmod = hash_algorithms[algo_selected]
                h = hmac.new(key.encode(), message.encode(), digestmod)
                if "shake" in algo_selected.lower():
                    # shake algorithms require output length for hexdigest
                    hmac_result = h.hexdigest(64)  # 64 hex digits (32 bytes)
                else:
                    hmac_result = h.hexdigest()
                st.success("✅ HMAC calculated successfully!")
            except Exception as e:
                st.error(f"❌ Error: {e}")

# Right column: Output
with col2:
    st.subheader("HMAC Output")
    st.text_area("HMAC (Hex Digest)", value=hmac_result, height=400, key="hmac_result")

st.write('---')
st.markdown("""
<h2>About HMAC and Its Output</h2>
<p>
  <strong>HMAC</strong> (Hash-based Message Authentication Code) is a cryptographic technique that combines a secret key with a hash function to produce a unique digest.
  This digest ensures message integrity and authenticity.
</p>

<h3>Output Characteristics</h3>
<ul>
  <li>The <em>HMAC digest</em> is a fixed-length hexadecimal string, whose length depends on the underlying hash algorithm.</li>
  <li>For example, <strong>HMAC-SHA256</strong> outputs a 64-character hex string (32 bytes).</li>
  <li>Displaying the first <strong>5 characters</strong> of the digest can provide a quick fingerprint, but for security, always use the full digest.</li>
</ul>

<h3>Security Properties</h3>
<ul>
  <li><strong>Collision resistance:</strong> It is practically impossible to find two different inputs producing the same HMAC.</li>
  <li><strong>Preimage resistance:</strong> Given an HMAC digest, it is infeasible to recover the original message or the secret key.</li>
  <li><strong>Key-dependent:</strong> The HMAC value changes if either the message or secret key changes, protecting against tampering and impersonation.</li>
</ul>

<h3>Algorithms Supported</h3>
<p>
  This tool supports HMAC using various cryptographic hash algorithms provided by Python’s <code>hashlib</code>, such as:
</p>
<ul>
  <li>MD5 (not recommended for security-sensitive use)</li>
  <li>SHA-1 (legacy, less secure)</li>
  <li>SHA-224, SHA-256, SHA-384, SHA-512 (recommended)</li>
  <li>SHA-3 variants (modern secure options)</li>
</ul>

<p>
  You can select the desired algorithm from the dropdown to generate the HMAC digest based on your message and secret key.
</p>
""", unsafe_allow_html=True)
