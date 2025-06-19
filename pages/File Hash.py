import streamlit as st
import hashlib
import os
import mimetypes
import tempfile
from pathlib import Path


def human_readable_size(size, decimal_places=2):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.{decimal_places}f} {unit}"
        size /= 1024
    return f"{size:.{decimal_places}f} PB"

def save_uploaded_file_to_tempdir(uploaded_file, temp_dir):
    temp_file_path = Path(temp_dir) / uploaded_file.name
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return temp_file_path

def calculate_all_hashes_with_progress(file_path, progress_bar, status_text):
    results = {}
    file_size = os.path.getsize(file_path)
    chunk_size = 8192  # 8KB chunks
    read_bytes = 0
    
    # Initialize hashers
    hashers = {}
    for algo in hashlib.algorithms_guaranteed:
        hashers[algo] = hashlib.new(algo)
    
    with open(file_path, "rb") as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            read_bytes += len(chunk)
            for hasher in hashers.values():
                hasher.update(chunk)
            
            # Update progress bar and status text
            progress = min(read_bytes / file_size, 1.0)
            progress_bar.progress(progress)
            status_text.text(f"Hashing progress: {progress*100:.2f}%")
    
    # Finalize hash results
    for algo, hasher in hashers.items():
        if algo.startswith("shake_"):
            results[algo] = hasher.hexdigest(32)  # 32 bytes output
        else:
            results[algo] = hasher.hexdigest()
    
    progress_bar.empty()
    status_text.empty()
    
    return results

def get_mime_type(filename):
    mime_type, _ = mimetypes.guess_type(filename)
    return mime_type if mime_type else None

st.title("Multi-File Hash Calculator")

st.markdown(
    """
    Upload or Drag and Drop your files here to display their hashes.
    This site supports a number of hashes: Blake2b, Blake2s, MD5, SHA-1, SHA-2, SHA-3, and SHAKE128/256.
    """
)

uploaded_files = st.file_uploader("Drag and drop files here or click to select", accept_multiple_files=True)

if uploaded_files:
    st.write(f"### Selected Files ({len(uploaded_files)})")

    # Use TemporaryDirectory context to store files safely
    with tempfile.TemporaryDirectory() as temp_dir:
        for idx, uploaded_file in enumerate(uploaded_files, 1):
            temp_path = save_uploaded_file_to_tempdir(uploaded_file, temp_dir)

            # Get accurate info
            file_name = temp_path.name
            file_location = str(temp_path.resolve())
            file_size_bytes = os.path.getsize(temp_path)
            file_size = human_readable_size(file_size_bytes)
            file_format = temp_path.suffix[1:] or "N/A"
            mime_type = get_mime_type(file_name)

            with st.expander(f"File {idx}: {file_name}", expanded=True):
                col1, col2 = st.columns([2, 3])
                with col1:
                    st.markdown(f"**File Name:** {file_name}")
                    st.markdown(f"**Size:** {file_size}")
                with col2:
                    st.markdown(f"**Format:** {file_format}")
                    st.markdown(f"**Type (MIME):** {mime_type}")

                progress_bar = st.progress(0)
                status_text = st.empty()

                # Calculate hashes with progress bar
                all_hashes = calculate_all_hashes_with_progress(temp_path, progress_bar, status_text)

                st.markdown("**Hashes:**")
                for algo, hash_val in sorted(all_hashes.items()):
                    st.markdown(f"- **{algo.upper()}:** `{hash_val}`")
else:
    st.info("No files uploaded yet. Please upload files using drag & drop or file dialog above.")


st.markdown("""
---
### About This Multi-File Hash Calculator

- Supports a wide range of hashing algorithms, including:
  - **Blake2b / Blake2s**: modern, fast, and secure hashes.
  - **MD5**: legacy hash, fast but cryptographically broken, mainly for checksums.
  - **SHA-1**: deprecated for security, but still used in some legacy systems.
  - **SHA-2 family** (SHA-224, SHA-256, SHA-384, SHA-512): widely used secure hash functions.
  - **SHA-3 family**: newer alternative hashes with different construction.
  - **SHAKE128 / SHAKE256**: extendable-output functions from SHA-3 family, allowing variable-length hashes.

- Files are read in chunks to handle large files without consuming too much memory.

- Progress bars and status updates provide real-time feedback during hashing.

- Output hashes are displayed in hexadecimal format.

---
""")
