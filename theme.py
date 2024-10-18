import streamlit as st

# Set Streamlit theme
def set_theme():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #f5f5f5;
            color: #333333;
        }
        .stApp header {
            background-color: #336699;
            color: #ffffff;
            padding: 0.5rem;
            border-radius: 0.5rem;
            margin-bottom: 1rem;
        }
        .stApp button {
            background-color: #336699;
            color: #ffffff;
            border-radius: 0.25rem;
            padding: 0.5rem 1rem;
            border: none;
            cursor: pointer;
        }
        .stApp button:hover {
            background-color: #23527c;
        }
        .stApp .css-1l02zno {
            background-color: #ffffff;
            border-radius: 0.25rem;
            padding: 0.5rem;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .stApp .css-1l02zno:hover {
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .stApp .css-1l02zno:focus {
            outline: none;
            box-shadow: 0 0 0 2px #336699;
        }
        .stApp .css-1l02zno:disabled {
            background-color: #cccccc;
            color: #666666;
            cursor: not-allowed;
        }
        .stApp .css-1l02zno:disabled:hover {
            box-shadow: none;
        }
        .stApp .css-1l02zno .st-bq {
            color: #333333;
        }
        .stApp .css-1l02zno .st-bq:hover {
            color: #23527c;
        }
        .stApp .css-1l02zno .st-bq:focus {
            color: #23527c;
        }
        .stApp .css-1l02zno .st-bq:disabled {
            color: #666666;
        }
        .stApp .css-1l02zno .st-bq:disabled:hover {
            color: #666666;
        }
        .stApp .css-1l02zno .st-bq:disabled:focus {
            color: #666666;
        }
        .stApp .css-1l02zno .st-bq.st-bp {
            color: #ffffff;
        }
        .stApp .css-1l02zno .st-bq.st-bp:hover {
            color: #ffffff;
        }
        .stApp .css-1l02zno .st-bq.st-bp:focus {
            color: #ffffff;
        }
        .stApp .css-1l02zno .st-bq.st-bp:disabled {
            color: #ffffff;
        }
        .stApp .css-1l02zno .st-bq.st-bp:disabled:hover {
            color: #ffffff;
        }
        .stApp .css-1l02zno .st-bq.st-bp:disabled:focus {
            color: #ffffff;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn {
            background-color: #336699;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn:hover {
            background-color: #23527c;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn:focus {
            background-color: #23527c;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn:disabled {
            background-color: #cccccc;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn:disabled:hover {
            background-color: #cccccc;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn:disabled:focus {
            background-color: #cccccc;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bo {
            background-color: #23527c;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bo:hover {
            background-color: #1a4160;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bo:focus {
            background-color: #1a4160;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bo:disabled {
            background-color: #23527c;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bo:disabled:hover {
            background-color: #23527c;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bo:disabled:focus {
            background-color: #23527c;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bm {
            background-color: #1a4160;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bm:hover {
            background-color: #13304b;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bm:focus {
            background-color: #13304b;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bm:disabled {
            background-color: #1a4160;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bm:disabled:hover {
            background-color: #1a4160;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bm:disabled:focus {
            background-color: #1a4160;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bl {
            background-color: #13304b;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bl:hover {
            background-color: #0d2030;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bl:focus {
            background-color: #0d2030;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bl:disabled {
            background-color: #13304b;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bl:disabled:hover {
            background-color: #13304b;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bl:disabled:focus {
            background-color: #13304b;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bk {
            background-color: #0d2030;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bk:hover {
            background-color: #081520;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bk:focus {
            background-color: #081520;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bk:disabled {
            background-color: #0d2030;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bk:disabled:hover {
            background-color: #0d2030;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bk:disabled:focus {
            background-color: #0d2030;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bj {
            background-color: #081520;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bj:hover {
            background-color: #040c10;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bj:focus {
            background-color: #040c10;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bj:disabled {
            background-color: #081520;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bj:disabled:hover {
            background-color: #081520;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bj:disabled:focus {
            background-color: #081520;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bi {
            background-color: #040c10;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bi:hover {
            background-color: #000000;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bi:focus {
            background-color: #000000;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bi:disabled {
            background-color: #040c10;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bi:disabled:hover {
            background-color: #040c10;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bi:disabled:focus {
            background-color: #040c10;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bh {
            background-color: #000000;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bh:hover {
            background-color: #000000;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bh:focus {
            background-color: #000000;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bh:disabled {
            background-color: #000000;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bh:disabled:hover {
            background-color: #000000;
        }
        .stApp .css-1l02zno .st-bq.st-bp.st-bn.st-bh:disabled:focus {
            background-color: #000000;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
