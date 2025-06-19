import streamlit as st
import pycipher
import ast
import inspect


st.title("Classical Cipher Toolbox")
st.subheader("Encipher and decipher text using a variety of classical ciphers with customizable parameters")



cipher_params = {
    "Atbash": {},
    "SimpleSubstitution": {"key": "AJPCZWRLFBDKOTYUQGENHXMIVS"},
    "Caesar": {"key": 13},
    "Affine": {"a": 5, "b": 9},
    "Autokey": {"key": "FORTIFICATION"},
    "Beaufort": {"key": "FORTIFICATION"},
    "Bifid": {"key": "phqgmeaylnofdxkrcvszwbuti", "period": 5},
    "ColTrans": {"keyword": "GERMAN"},
    "Gronsfeld": {"key": "[5, 4, 7, 9]"},
    "Foursquare": {"key1": "zgptfoihmuwdrcnykeqaxvsbl", "key2": "mfnbdcrhsaxyogvituewlqzkp"},
    "PolybiusSquare": {"key": "phqgiumeaylnofdxkrcvstzwb", "size": 5},
    "Playfair": {"key": "ABCDEFGHIKLMNOPQRSTUVWXYZ"},
    "Vigenere": {"key": "fortification"},
    "Rot13": {},
    "Railfence": {"key": 5},
}

def parse_param(val):
    if val in ["None", None, ""]:
        return None
    try:
        return ast.literal_eval(val)
    except:
        return val

def build_param_ui(cipher_name, section_prefix):
    params = cipher_params[cipher_name]
    user_inputs = {}

    st.markdown(f"**{section_prefix.capitalize()} Parameters – {cipher_name}**")
    if params:
        for p, default_val in params.items():
            parsed_default = parse_param(default_val)
            use_param = st.checkbox(f"Use '{p}'?", value=True, key=f"{section_prefix}_chk_{cipher_name}_{p}")
            if use_param:
                default_str = str(parsed_default) if parsed_default is not None else ""
                user_input = st.text_input(f"{p}", value=default_str, key=f"{section_prefix}_inp_{cipher_name}_{p}")
                user_inputs[p] = parse_param(user_input)
    else:
        st.info("This cipher has no parameters.")

    return user_inputs

def safe_cipher_instance(cipher_name, user_inputs):
    try:
        cipher_class = getattr(pycipher, cipher_name)
        accepted_params = inspect.signature(cipher_class.__init__).parameters
        valid_inputs = {k: v for k, v in user_inputs.items() if k in accepted_params}
        return cipher_class(**valid_inputs)
    except Exception as e:
        st.error(f"Error creating cipher instance: {e}")
        return None

def main():
    enc_col_text, enc_col_param, separator_col, dec_col_text, dec_col_param = st.columns([2, 2, 0.1, 2, 2])


    # === ENCIPHER SECTION ===
    with enc_col_text:
        st.subheader("📝 Encipher Text")
        enc_text = st.text_area("Input", value="HELLO", height=375, key="enc_text")

    with enc_col_param:
        st.subheader("🔐 Encipher Settings")
        enc_cipher = st.selectbox("Select Cipher", sorted(cipher_params.keys()), key="enc_cipher")
        enc_inputs = build_param_ui(enc_cipher, "enc")

    with separator_col:
        st.markdown(
            "<div style='height: 500px; border-left: 2px solid #bbb;'></div>",
            unsafe_allow_html=True
        )


    # === DECIPHER SECTION ===
    with dec_col_text:
        st.subheader("📝 Decipher Text")
        dec_text = st.text_area("Input", value="", height=375, key="dec_text")

    with dec_col_param:
        st.subheader("🔓 Decipher Settings")
        dec_cipher = st.selectbox("Select Cipher", sorted(cipher_params.keys()), key="dec_cipher")
        dec_inputs = build_param_ui(dec_cipher, "dec")

    # === BUTTONS SECTION ===
    btn_col1, _, btn_col2, _ = st.columns([2, 2, 2, 2])

    with btn_col1:
        if st.button("Encipher", key="enc_btn"):
            cipher_obj = safe_cipher_instance(enc_cipher, enc_inputs)
            if cipher_obj:
                try:
                    result = cipher_obj.encipher(enc_text.strip())
                    st.success(f"🔐 Result:\n{result}")
                except Exception as e:
                    st.error(f"Encipher Failed: {e}")

    with btn_col2:
        if st.button("Decipher", key="dec_btn"):
            cipher_obj = safe_cipher_instance(dec_cipher, dec_inputs)
            if cipher_obj:
                try:
                    result = cipher_obj.decipher(dec_text.strip())
                    st.success(f"🔓 Result:\n{result}")
                except Exception as e:
                    st.error(f"Decipher Failed: {e}")


    st.markdown("""
    ---
    ### Default Cipher Parameters Explained

    - **Atbash**: No parameters. A simple substitution cipher reversing the alphabet.

    - **SimpleSubstitution**:  
      - `key`: A 26-letter key representing the substitution alphabet.

    - **Caesar**:  
      - `key`: Integer shift value (default 13).

    - **Affine**:  
      - `a`: Multiplier in the affine formula (must be coprime to 26, default 5).  
      - `b`: Additive shift in the affine formula (default 9).

    - **Autokey**:  
      - `key`: Initial keyword for the Autokey cipher.

    - **Beaufort**:  
      - `key`: Keyword used in the Beaufort cipher.

    - **Bifid**:  
      - `key`: Polybius square alphabet key.  
      - `period`: Period length for the transposition step.

    - **ColTrans** (Columnar Transposition):  
      - `keyword`: Keyword determining column order.

    - **Gronsfeld**:  
      - `key`: List of digits as a key, e.g., `[5, 4, 7, 9]`.

    - **Foursquare**:  
      - `key1`: Key for the first square.  
      - `key2`: Key for the second square.

    - **PolybiusSquare**:  
      - `key`: Alphabet key for the square.  
      - `size`: Dimension of the square (usually 5).

    - **Playfair**:  
      - `key`: Keyword used to generate the Playfair matrix.

    - **Vigenere**:  
      - `key`: Keyword for Vigenère cipher.

    - **Rot13**: No parameters. Fixed Caesar cipher with shift 13.

    - **Railfence**:  
      - `key`: Number of rails used for the fence.

    ---
    """)

if __name__ == "__main__":
    main()

