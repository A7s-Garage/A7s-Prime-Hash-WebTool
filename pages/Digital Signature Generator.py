import streamlit as st
from cryptography.hazmat.primitives.asymmetric import rsa, padding, ec, ed25519
from cryptography.hazmat.primitives import hashes
import base64

st.title("Digital Signature Generator")
st.subheader("Sign messages using RSA-PSS, RSA-PKCS1v1_5, ECDSA, or Ed25519 algorithms")


# Main page columns: left (2 parts), right (3 parts)
col1, col2 = st.columns([2, 3])

with col1:
    # Top row inside left column: split into two halves
    left_half, right_half = st.columns(2)
    with left_half:
        algo = st.selectbox("Choose a Signature Algorithm", ["RSA-PSS", "RSA-PKCS1v1_5", "ECDSA", "Ed25519"])
    # right_half is left empty (or add something later if you want)

    # Below the dropdown, full width inputs:
    message = st.text_area("✉️ Message to Sign", value="On His Majesty’s Secret Service.", height=180)

    params = {}

    if algo.startswith("RSA"):
        st.subheader("🔧 Parameters")
        key_col, hash_col = st.columns(2)
        with key_col:
            rsa_key_size = st.selectbox("Key Size (bits)", [1024, 2048, 3072, 4096], index=1)
        with hash_col:
            hash_func = st.selectbox("Hash Function", ["SHA256", "SHA384", "SHA512"], index=0)
        rsa_private_key = rsa.generate_private_key(public_exponent=65537, key_size=rsa_key_size)
        hash_algo = getattr(hashes, hash_func)()
        params['key'] = rsa_private_key

        if algo == "RSA-PSS":
            salt_col, mgf_col = st.columns(2)
            with salt_col:
                salt_length = st.slider("Salt Length (bytes)", min_value=0, max_value=hash_algo.digest_size, value=hash_algo.digest_size)
            with mgf_col:
                mgf1_hash = st.selectbox("MGF1 Hash Function", ["SHA256", "SHA384", "SHA512"], index=0)
            mgf1_algo = getattr(hashes, mgf1_hash)()
            params.update({
                'padding': padding.PSS(
                    mgf=padding.MGF1(mgf1_algo),
                    salt_length=salt_length
                ),
                'hash': hash_algo
            })
        elif algo == "RSA-PKCS1v1_5":
            params.update({
                'padding': padding.PKCS1v15(),
                'hash': hash_algo
            })

    elif algo == "ECDSA":
        st.subheader("🔧 Parameters")
        curve_col, hash_col = st.columns(2)
        with curve_col:
            curve = st.selectbox("ECC Curve", ["SECP256R1", "SECP384R1", "SECP521R1"])
            curve_obj = getattr(ec, curve)()
            ecdsa_key = ec.generate_private_key(curve_obj)
        with hash_col:
            hash_func = st.selectbox("Hash Function", ["SHA256", "SHA384", "SHA512"], index=0)
        params = {
            'key': ecdsa_key,
            'hash': getattr(hashes, hash_func)()
        }

    elif algo == "Ed25519":
        st.info("Ed25519 has no configurable parameters (RFC 8032).")
        ed_key = ed25519.Ed25519PrivateKey.generate()
        params = {'key': ed_key}

    compute_clicked = st.button("🔐 Compute Signature")  # full width of col1

with col2:
    st.subheader("Signature Output")

    if compute_clicked:
        if not message.strip():
            st.error("Please enter a message to sign.")
        elif not params:
            st.error("Parameters are incomplete.")
        else:
            try:
                def sign_message(algo, msg, params):
                    data = msg.encode()
                    key = params['key']

                    if algo == "RSA-PSS":
                        return key.sign(data, params['padding'], params['hash'])
                    elif algo == "RSA-PKCS1v1_5":
                        return key.sign(data, params['padding'], params['hash'])
                    elif algo == "ECDSA":
                        return key.sign(data, ec.ECDSA(params['hash']))
                    elif algo == "Ed25519":
                        return key.sign(data)
                
                signature = sign_message(algo, message, params)
                signature_b64 = base64.b64encode(signature).decode()

                st.success("Signature Generated ✅")
                st.text_area("Base64 Signature", value=signature_b64, height=150)
                st.write(f"📏 Signature Size: `{len(signature)} bytes`")
            except Exception as e:
                st.error(f"❌ Error: {e}")


st.markdown("""
---
### Supported Signature Algorithms

- **RSA-PSS**  
  Probabilistic Signature Scheme with mask generation function (MGF1).  
  Configurable key sizes (1024–4096 bits), hash functions, salt length, and MGF1 hash.

- **RSA-PKCS1v1_5**  
  Older RSA signature standard with fixed padding.  
  Configurable key sizes and hash functions.

- **ECDSA (Elliptic Curve Digital Signature Algorithm)**  
  Uses elliptic curve cryptography.  
  Choose between curves SECP256R1, SECP384R1, and SECP521R1 and hash function.

- **Ed25519**  
  Modern, fast elliptic curve signature scheme (Edwards curve).  
  No configurable parameters; fixed scheme per RFC 8032.

---

**Note:**  
- Keys are generated fresh each run with specified parameters.  
- Signature outputs are base64 encoded for easy copy/paste and transmission.  
- Make sure to keep your private keys secure — this demo generates keys on the fly and does not save them.
""")

