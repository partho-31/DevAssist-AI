
import os
import tempfile
import streamlit as st

from core.branch import router
from core.responses import format_response

from rag.ingestion import ingest_pdf
from rag.rag_chain import ask as ask_rag


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="DevAssist AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-family: Inter, "Segoe UI", sans-serif;
    }

    .block-container {
        padding-top: 2rem;
    }

    .app-title {
        font-size: 2rem;
        font-weight: 650;
        margin-bottom: 1rem;
    }

    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
    }

    div[data-testid="stChatMessage"] {
        padding-top: 0.6rem;
        padding-bottom: 0.6rem;
    }

    div[data-testid="stSelectbox"] {
        width: 100%;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "app_mode" not in st.session_state:
    st.session_state.app_mode = "DevAssist AI"

# Reset structured report after one response
if st.session_state.pop("reset_report_format", False):
    st.session_state.structured_report = False


# --------------------------------------------------
# LEFT SIDEBAR: CONVERSATION HISTORY
# --------------------------------------------------

with st.sidebar:

    st.markdown("### 💬 Conversation History")

    if st.button("＋ New conversation", use_container_width=True):
        st.session_state.messages = []
        st.session_state.structured_report = False
        st.rerun()

    st.divider()

    for message in st.session_state.messages:

        if message["role"] == "user":

            preview = message["content"][:40]

            if len(message["content"]) > 40:
                preview += "..."

            st.markdown(f"**{preview}**")


# --------------------------------------------------
# MAIN LAYOUT
# --------------------------------------------------

chat_col, ingest_col = st.columns(
    [3, 1],
    gap="large"
)


# --------------------------------------------------
# RIGHT SIDE: WORKSPACE SELECTOR + PDF INGESTION
# --------------------------------------------------

with ingest_col:

    st.markdown("### ⚙️ Workspace")

    app_mode = st.radio(
        "Select application",
        ["DevAssist AI", "PDF RAG"],
        key="app_mode"
    )

    st.divider()

    st.markdown("### 📄 Document Ingestion")

    uploaded_file = st.file_uploader(
        "Upload a PDF document",
        type=["pdf"],
        disabled=(app_mode != "PDF RAG")
    )

    collection_name = st.text_input(
        "Collection Name",
        value="pdf_docs",
        key="collection_name",
        disabled=(app_mode != "PDF RAG")
    )

    if st.button(
        "Process PDF",
        use_container_width=True,
        disabled=(app_mode != "PDF RAG")
    ):

        if uploaded_file is not None:

            with st.spinner("Ingesting document..."):

                save_path = None

                try:
                    with tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".pdf"
                    ) as tmp:

                        tmp.write(uploaded_file.getvalue())
                        save_path = tmp.name

                    stats = ingest_pdf(
                        save_path,
                        collection_name
                    )

                    st.success(
                        f"Successfully processed "
                        f"{stats['pages']} pages and "
                        f"{stats['chunks']} chunks."
                    )

                except ValueError as exc:
                    st.error(f"Error: {exc}")

                finally:
                    if save_path and os.path.exists(save_path):
                        try:
                            os.remove(save_path)
                        except OSError:
                            pass

        else:
            st.warning("Please upload a PDF first.")


# --------------------------------------------------
# MAIN CHAT INTERFACE
# --------------------------------------------------

with chat_col:

    st.markdown(
        '<div class="app-title">🤖 DevAssist AI</div>',
        unsafe_allow_html=True
    )

    # ----------------------------------------------
    # DEVASSIST AI MODE
    # ----------------------------------------------

    if app_mode == "DevAssist AI":

        st.markdown("### AI Developer Assistant")

        selected_mode = st.selectbox(
            "Mode",
            [
                "Code Review",
                "Bug Fix",
                "Code Generation",
                "Code Explanation",
                "Code Optimization",
            ],
            label_visibility="collapsed"
        )

        structured_report = st.toggle(
            "Structured report for the next message",
            key="structured_report",
            help=(
                "Generate a full report in the selected mode. "
                "Follow-up messages return to chat automatically."
            )
        )

    # ----------------------------------------------
    # PDF RAG MODE
    # ----------------------------------------------

    else:

        st.markdown("### PDF Question Answering")

        st.info(
            "Ask questions about your ingested PDF documents."
        )


    # ----------------------------------------------
    # DISPLAY CONVERSATION HISTORY
    # ----------------------------------------------

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])

            # Display RAG sources when available
            if message.get("sources"):

                with st.expander("Sources"):

                    for src in message["sources"]:

                        st.write(
                            f"- **Page {src['page']}**: "
                            f"{src['snippet']}..."
                        )


    # ----------------------------------------------
    # CHAT INPUT
    # ----------------------------------------------

    if app_mode == "DevAssist AI":

        placeholder = (
            "Paste your code or describe what you want to build..."
        )

    else:

        placeholder = "Ask a question about your uploaded PDF..."


    user_input = st.chat_input(placeholder)


    # ----------------------------------------------
    # HANDLE USER INPUT
    # ----------------------------------------------

    if user_input:

        # Save user message
        st.session_state.messages.append(
            {
                "role": "user",
                "content": user_input,
                "app": app_mode
            }
        )

        with st.chat_message("user"):
            st.markdown(user_input)


        # ------------------------------------------
        # DEVASSIST AI CHAIN
        # ------------------------------------------

        if app_mode == "DevAssist AI":

            router_input = {
                "mode": selected_mode,
                "task_input": user_input,
                "response_format": (
                    "structured"
                    if structured_report
                    else "chat"
                ),
                "history": [
                    (message["role"], message["content"])
                    for message in st.session_state.messages[:-1]
                    if message.get("app", "DevAssist AI") == "DevAssist AI"
                ],
            }

            with st.chat_message("assistant"):

                with st.spinner("Thinking..."):

                    try:

                        assistant_response = format_response(
                            router.invoke(router_input)
                        )

                        st.markdown(assistant_response)

                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "content": assistant_response,
                                "app": app_mode
                            }
                        )

                        if structured_report:
                            st.session_state.reset_report_format = True

                        st.rerun()

                    except Exception as error:

                        st.error(f"Error: {error}")


        # ------------------------------------------
        # PDF RAG CHAIN
        # ------------------------------------------

        else:

            with st.chat_message("assistant"):

                with st.spinner("Searching your documents..."):

                    try:

                        result = ask_rag(
                            collection=collection_name,
                            question=user_input,
                            k=4
                        )

                        answer = result["answer"]
                        sources = result.get("sources", [])

                        st.markdown(answer)

                        if sources:

                            with st.expander("Sources"):

                                for src in sources:

                                    st.write(
                                        f"- **Page {src['page']}**: "
                                        f"{src['snippet']}..."
                                    )

                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "content": answer,
                                "sources": sources,
                                "app": app_mode
                            }
                        )

                        st.rerun()

                    except ValueError as exc:

                        st.error(
                            f"System Error: {exc}. "
                            "Please ingest a PDF first."
                        )

                    except Exception as error:

                        st.error(f"Error: {error}")
