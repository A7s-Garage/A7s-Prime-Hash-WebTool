import streamlit as st
from PIL import Image
import imagehash
import hashlib
import io
import time

SUPPORTED_FORMATS = ["png", "jpg", "jpeg", "webp", "bmp", "tiff", "gif"]


st.title("🖼️ Image Hashing Tool")
st.subheader("Compute cryptographic and perceptual hashes for uploaded images")

st.markdown("Upload multiple images to compute **cryptographic** and **perceptual** hashes for each one.")
st.markdown("View your image instantly — **A7's Image Viewer** supports 25+ image formats! [Open Image Viewer ! ](https://a7s-image-viewer.streamlit.app/)")



# Upload multiple files
uploaded_files = st.file_uploader(
    "Upload one or more images",
    type=SUPPORTED_FORMATS,
    accept_multiple_files=True,
    label_visibility="collapsed"
)

if uploaded_files:
    progress_bar = st.progress(0)
    total_files = len(uploaded_files)

    for idx, uploaded_file in enumerate(uploaded_files):
        file_bytes = uploaded_file.read()
        image = Image.open(io.BytesIO(file_bytes))
        file_size_kb = len(file_bytes) / 1024
        file_name = uploaded_file.name

        st.markdown("---")
        st.subheader(f"🖼️ Image {idx+1}: `{file_name}`")

        # Layout: Two Columns
        col1, col2 = st.columns([1, 2])

        with col1:
            st.image(image, caption="Preview", use_container_width=True)
            st.markdown(f"**File Name:** `{file_name}`")
            st.markdown(f"**Size:** `{file_size_kb:.2f} KB`")

        with col2:
            st.markdown("#### 🔐 General Hashes")
            sha1 = hashlib.sha1(file_bytes).hexdigest()
            sha256 = hashlib.sha256(file_bytes).hexdigest()
            sha512 = hashlib.sha512(file_bytes).hexdigest()
            md5 = hashlib.md5(file_bytes).hexdigest()

            st.code(f"SHA-1   : {sha1}")
            st.code(f"SHA-256 : {sha256}")
            st.code(f"SHA-512 : {sha512}")
            st.code(f"MD5     : {md5}")

            st.markdown("#### 🧠 Image Hashes")
            ahash = str(imagehash.average_hash(image))
            phash = str(imagehash.phash(image))
            dhash = str(imagehash.dhash(image))
            whash = str(imagehash.whash(image))

            st.code(f"aHash : {ahash}")
            st.code(f"pHash : {phash}")
            st.code(f"dHash : {dhash}")
            st.code(f"wHash : {whash}")

        # Progress update
        progress = (idx + 1) / total_files
        progress_bar.progress(progress)
        time.sleep(0.1)  # Optional small delay for smooth UI update

    progress_bar.empty()  # Remove progress bar when done
else:
    st.info("📂 Drag and drop or select one or more image files to begin.")


st.write("---")
st.markdown("""
<h2>About Image Hashing</h2>
<p>This tool computes two types of hashes for your images: <strong>cryptographic hashes</strong> and <strong>perceptual hashes</strong>.</p>

<h3>Cryptographic Hashes</h3>
<ul>
  <li>These are fixed-length digests (e.g., SHA-1, SHA-256, SHA-512, MD5) that uniquely represent the image file's binary data.</li>
  <li>Any change to the image file—even a single bit—will result in a completely different cryptographic hash.</li>
  <li>Common algorithms used here are:</li>
  <ul>
    <li><strong>MD5:</strong> Fast but not collision-resistant; not recommended for security.</li>
    <li><strong>SHA-1:</strong> Better than MD5 but has known vulnerabilities.</li>
    <li><strong>SHA-256 and SHA-512:</strong> Secure and widely used.</li>
  </ul>
  <li>These hashes are useful for verifying file integrity and detecting exact duplicates.</li>
</ul>

<h3>Perceptual Hashes (Image Hashes)</h3>
<ul>
  <li>Perceptual hashes generate a fingerprint of the image's visual content rather than its raw bytes.</li>
  <li>They allow detection of visually similar images even if they differ in file format, size, or minor edits.</li>
  <li>Common algorithms implemented here:</li>
  <ul>
    <li><strong>aHash (Average Hash):</strong> Computes average pixel values.</li>
    <li><strong>pHash (Perceptual Hash):</strong> Uses discrete cosine transform for robust similarity detection.</li>
    <li><strong>dHash (Difference Hash):</strong> Focuses on gradients between adjacent pixels.</li>
    <li><strong>wHash (Wavelet Hash):</strong> Applies wavelet transform for capturing texture.</li>
  </ul>
  <li>These hashes produce short strings (e.g., 64-bit hashes) representing the image's essence.</li>
  <li>Comparing these hashes can identify near-duplicates or similar images.</li>
</ul>

<h3>Output Format</h3>
<ul>
  <li><strong>Cryptographic hashes</strong> are displayed as long hexadecimal strings representing byte sequences.</li>
  <li><strong>Perceptual hashes</strong> are typically shorter hexadecimal strings (e.g., 16 characters) summarizing visual content.</li>
  <li>Both types can be truncated for quick reference, but full hashes are required for precise matching.</li>
</ul>

<h3>Summary</h3>
<p>
Use cryptographic hashes to verify exact file integrity and detect identical files.<br>
Use perceptual hashes to find visually similar images, even if they have been resized, compressed, or slightly altered.
</p>
""", unsafe_allow_html=True)
