import streamlit as st
from am2json.diff import extract_opcodes_v2
import json
def visualize_text_difference(original_text, amended_text):
    original_words = original_text.split()
    amended_words = amended_text.split()

    opcodes = extract_opcodes_v2(original_words, amended_words)

    for opcode in opcodes:
        tag, i1, i2, j1, j2 = opcode

        if tag == 'replace':
            st.markdown(f"**Replace:** Original: {' '.join(original_words[i1:i2])}, Amended: {' '.join(amended_words[j1:j2])}")
        elif tag == 'delete':
            st.markdown(f"**Delete:** {' '.join(original_words[i1:i2])}")
        elif tag == 'insert':
            st.markdown(f"**Insert:** {' '.join(amended_words[j1:j2])}")
        elif tag == 'equal':
            st.markdown(f"**Equal:** {' '.join(original_words[i1:i2])}")


def main():
    st.title("Text Difference Visualizer")

    file_path = "./data/war-of-words-2-ep8.txt"
    exclude_index = st.text_input("Exclude Index", "18")
    exclude_index = int(exclude_index)

    with open(file_path, "r") as f:
        for i, line in enumerate(f.readlines()):
            a = json.loads(line.rstrip())[0]
            found = False

            for j, (tag, i1, i2, j1, j2) in enumerate(extract_opcodes_v2(a['text_original'], a['text_amended'])):

                if a['edit_type'] == tag and a['edit_indices'] == {"i1": i1, "i2": i2, "j1": j1, "j2": j2}:
                    found = True
                    break

            if not found and i != exclude_index:
                st.write(f"Not found: {a['edit_type']}, {a['edit_indices']}")

                original = a['text_original']
                amended = a['text_amended']

                original_html = []
                amended_html = []
                missing_tag = a["edit_type"]

                for tag, i1, i2, j1, j2 in extract_opcodes_v2(a['text_original'], a['text_amended']):
                    if tag == 'delete':
                        original_html.append(
                            f"<span style='background-color:rgba(255, 0, 0, 0.5)'>{' '.join(original[i1:i2])}</span>")
                    elif tag == 'replace':
                        original_html.append(
                            f"<span style='background-color:rgba(255, 165, 0, 0.5)'>{' '.join(original[i1:i2])}</span>")
                        amended_html.append(
                            f"<span style='background-color:rgba(255, 165, 0, 0.5)'>{' '.join(amended[j1:j2])}</span>")
                    elif tag == 'equal':
                        original_html.append(
                            f"<span style='background-color:rgba(0, 128, 0, 0.5)'>{' '.join(original[i1:i2])}</span>")
                        amended_html.append(
                            f"<span style='background-color:rgba(0, 128, 0, 0.5)'>{' '.join(amended[j1:j2])}</span>")
                    elif tag == 'insert':
                        amended_html.append(
                            f"<span style='background-color:rgba(128, 0, 128, 0.5)'>{' '.join(amended[j1:j2])}</span>")

                # Default value
                missing_color = "rgba(255,255,255, 0.9)"

                if missing_tag == 'delete':
                    missing_color = "rgba(255, 0, 0, 0.5)"
                elif missing_tag == 'replace':
                    missing_color = "rgba(255, 165, 0, 0.5)"
                elif missing_tag == 'equal':
                    missing_color = "rgba(0, 128, 0, 0.5)"
                elif missing_tag == 'insert':
                    missing_color = "rgba(128, 0, 128, 0.5)"

                missing_original_html = f"<span style='background-color:{missing_color}'>{' '.join(original[a['edit_indices']['i1']:a['edit_indices']['i2']])}</span>"
                missing_amended_html = f"<span style='background-color:{missing_color}'>{' '.join(amended[a['edit_indices']['j1']:a['edit_indices']['j2']])}</span>"
                original_html = ' '.join(original_html)
                amended_html = ' '.join(amended_html)
                col1, col2 = st.columns(2)
                col3, col4 = st.columns(2)

                with col1:
                    st.write("Original:")
                    st.markdown(original_html, unsafe_allow_html=True)

                with col2:
                    st.write("Amended:")
                    st.markdown(amended_html, unsafe_allow_html=True)

                with col3:
                    st.write(f"Missing {a['edit_type']} in Original:")
                    st.markdown(missing_original_html, unsafe_allow_html=True)

                with col4:
                    st.write(f"Missing {a['edit_type']} in Amended:")
                    st.markdown(missing_amended_html, unsafe_allow_html=True)

                st.write('-----')

                st.sidebar.title("Key")
                st.sidebar.markdown("- <span style='background-color:rgba(255, 0, 0, 0.5)'>Deleted Text</span>", unsafe_allow_html=True)
                st.sidebar.markdown("- <span style='background-color:rgba(255, 165, 0, 0.5)'>Replaced Text</span>", unsafe_allow_html=True)
                st.sidebar.markdown("- <span style='background-color:rgba(0, 128, 0, 0.5)'>Equal Text</span>", unsafe_allow_html=True)
                st.sidebar.markdown("- <span style='background-color:rgba(128, 0, 128, 0.5)'>Inserted Text</span>", unsafe_allow_html=True)


                break

            if i > 150:
                break

if __name__ == "__main__":
    main()