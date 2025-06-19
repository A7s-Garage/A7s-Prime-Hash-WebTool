import streamlit as st
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Hash import HMAC, SHA1, SHA256, SHA512  # For PBKDF2 PRF

from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

st.title("🔐 Key Derivation Function (KDF)")
st.markdown(
    """
    Derive cryptographic keys from passwords using **PBKDF2**, **scrypt**, or **HKDF**.
    Customize parameters and generate salts to securely generate keys for encryption or authentication.
    """
)

def derive_key_pbkdf2(password, salt, dkLen, count, hashmod):
    return PBKDF2(password, salt, dkLen, count, lambda p, s: HMAC.new(p, s, hashmod).digest())

# --- scrypt Derivation ---
def derive_key_scrypt(password, salt, key_len, N, r, p):
    scrypt_kdf = Scrypt(salt=salt, length=key_len, n=N, r=r, p=p, backend=default_backend())
    return scrypt_kdf.derive(password)

# --- HKDF Derivation ---
def derive_key_hkdf(input_key_material, salt, info, length, hash_algorithm):
    hkdf = HKDF(
        algorithm=hash_algorithm,
        length=length,
        salt=salt,
        info=info,
        backend=default_backend()
    )
    return hkdf.derive(input_key_material)


# Input password
password = st.text_area("Enter your password:", "")

# Salt input or generation
custom_salt_hex = st.text_input("Enter salt (hex) or leave blank to auto-generate:")
if custom_salt_hex:
    try:
        salt = bytes.fromhex(custom_salt_hex.strip())
    except ValueError:
        st.error("❌ Invalid salt hex. Please enter a valid hex string.")
        st.stop()
else:
    salt = get_random_bytes(16)

# Show salt
st.code(f"Salt (hex): {salt.hex()}")

# Select algorithm
algorithm = st.selectbox("Choose KDF Algorithm", ["PBKDF2", "scrypt", "HKDF"])

# --- PBKDF2 ---
if algorithm == "PBKDF2":
    st.subheader("PBKDF2 Parameters")
    with st.expander("Mandatory Parameters"):
        dkLen = st.number_input("Derived Key Length (bytes):", min_value=8, max_value=64, value=16)
        count = st.number_input("Iterations (count):", min_value=1000, max_value=100000, value=1000)

    with st.expander("Non-Mandatory Parameters"):
        prf_choice = st.selectbox("Pseudorandom Function (PRF):", ["HMAC-SHA1", "HMAC-SHA256", "HMAC-SHA512"])
        prf_dict = {
            "HMAC-SHA1": SHA1,
            "HMAC-SHA256": SHA256,
            "HMAC-SHA512": SHA512
        }
        prf = prf_dict[prf_choice]

    if st.button("🔑 Generate Key (PBKDF2)"):
        try:
            key = derive_key_pbkdf2(password.encode(), salt, dkLen, count, prf)
            st.success("Derived Key (PBKDF2):")
            st.code(key.hex())
        except Exception as e:
            st.error(f"Error: {e}")

# --- scrypt ---
elif algorithm == "scrypt":
    st.subheader("scrypt Parameters")
    with st.expander("Mandatory Parameters"):
        key_len = st.number_input("Derived Key Length (bytes):", min_value=8, max_value=64, value=16)
        N = st.number_input("CPU/memory cost (N):", min_value=2**8, max_value=2**20, value=2**14, step=2**8)
        r = st.number_input("Block size (r):", min_value=1, max_value=256, value=8)
        p = st.number_input("Parallelization (p):", min_value=1, max_value=16, value=1)

    if st.button("🔑 Generate Key (scrypt)"):
        try:
            key = derive_key_scrypt(password.encode(), salt, key_len, int(N), int(r), int(p))
            st.success("Derived Key (scrypt):")
            st.code(key.hex())
        except Exception as e:
            st.error(f"Error: {e}")

# --- HKDF ---
elif algorithm == "HKDF":
    st.subheader("HKDF Parameters")
    with st.expander("Mandatory Parameters"):
        info = st.text_input("Info (optional):", "")
        length = st.number_input("Derived Key Length (bytes):", min_value=8, max_value=64, value=16)
        hash_algo = st.selectbox("Hash Algorithm:", ["SHA256", "SHA512"])
        hash_algorithm = hashes.SHA256() if hash_algo == "SHA256" else hashes.SHA512()

    with st.expander("Non-Mandatory Parameters"):
        pass  # required for indentation

    if st.button("🔑 Generate Key (HKDF)"):
        try:
            key = derive_key_hkdf(password.encode(), salt, info.encode(), length, hash_algorithm)
            st.success("Derived Key (HKDF):")
            st.code(key.hex())
        except Exception as e:
            st.error(f"Error: {e}")

st.write("---")

st.markdown("""
<h2>About Key Derivation Functions (KDFs)</h2>

<p>KDFs convert a password or initial key material into a fixed-length cryptographic key, suitable for encryption, authentication, or other cryptographic uses.</p>

<h3>PBKDF2</h3>
<ul>
  <li>Uses a pseudorandom function (HMAC with SHA1, SHA256, or SHA512) iteratively to slow down brute-force attacks.</li>
  <li>Iterations count controls the work factor (higher = slower but more secure).</li>
  <li>Output is a derived key of specified length.</li>
</ul>

<h3>scrypt</h3>
<ul>
  <li>Designed to be CPU- and memory-hard to resist hardware attacks (like GPUs or ASICs).</li>
  <li>Parameters N, r, p control cost and parallelism.</li>
  <li>Great for password hashing and key derivation where strong resistance against brute force is required.</li>
</ul>

<h3>HKDF</h3>
<ul>
  <li>Extracts and expands keys from high-entropy input key material.</li>
  <li>Often used in key management protocols.</li>
  <li>Requires salt and optional context info string.</li>
</ul>

<h3>Output</h3>
<ul>
  <li>All algorithms output a binary key (displayed as hex string).</li>
  <li>Length depends on your choice but typically 16-64 bytes.</li>
</ul>

<p>Always use a unique and sufficiently random <strong>salt</strong> to prevent precomputed dictionary attacks.</p>
""", unsafe_allow_html=True)
