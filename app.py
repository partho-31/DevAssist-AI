import streamlit as st
from branch import router


st.set_page_config(
    page_title="DevAssist AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.markdown(
    """
    <style>

    /* Global typography */
    html, body, [class*="css"] {
        font-family: Inter, "Segoe UI", sans-serif;
    }

    .block-container {
        padding-top: 2rem;
    }

    /* Header */
    .app-title {
        text-align: left;
        font-size: 2rem;
        font-weight: 650;
        margin-bottom: 1.2rem;
    }

    /* Sidebar */
    .sidebar-title {
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    /* Make selectbox full width */
    div[data-testid="stSelectbox"] {
        width: 100%;
        max-width: 100%;
        margin: 0 0 1.5rem 0;
    }

    div[data-baseweb="select"] {
        width: 100%;
        max-width: 100%;
    }

    /* Chat message alignment */
    div[data-testid="stChatMessage"] {
        padding-top: 0.6rem;
        padding-bottom: 0.6rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)



if "messages" not in st.session_state:
    st.session_state.messages = []

# sidebar
with st.sidebar:

    st.markdown(
        '<div class="sidebar-title">Review History</div>',
        unsafe_allow_html=True
    )

    for message in st.session_state.messages:
        if message["role"] == "user":
            preview = message["content"][:40]
            if len(message["content"]) > 40:
                preview += "..."
            st.markdown(
                f"**{preview}**"
            )


# web header
st.markdown(
    '<div class="app-title">DevAssist AI</div>',
    unsafe_allow_html=True
)

# Option selector
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


# previous chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            st.markdown(message["content"])
        else:
            st.markdown(message["content"])



user_input = st.chat_input(
    "Paste your code or describe what you want to build..."
)

if user_input:
    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    with st.chat_message("user"):
        st.markdown(user_input)

    task_input = f"""
    Selected Mode: {selected_mode}

    User Request:
    {user_input}
    """
    router_input = {
        "mode": selected_mode,
        "task_input": task_input
    }

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = router.invoke(router_input)

                if hasattr(response,"model_dump"):
                    response_data = response.model_dump()
                    output_parts = []

                    for field, value in response_data.items():
                        if value is None:
                            continue
                        title = field.replace( "_"," ").title()

                        if isinstance(value,list):
                            if len(value) == 0:
                                continue

                            items = "\n".join(
                                f"- {item}"
                                for item in value
                            )

                            output_parts.append(f"### {title}\n\n{items}")

                        elif "code" in field.lower():
                            output_parts.append(
                                f"### {title}\n\n"
                                f"```python\n{value}\n```"
                            )

                        else:
                            output_parts.append(f"### {title}\n\n{value}")

                    assistant_response = "\n\n".join(output_parts)

                else:
                    assistant_response = str(response)

                st.markdown(assistant_response)
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": assistant_response
                    }
                )
                st.rerun()

            except Exception as error:
                st.error(
                    f"Error: {error}"
                )