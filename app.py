import streamlit as st
from nj_search import search_nj_unclaimed  # Replace with actual filename

st.set_page_config(page_title="Refund Finder AI", layout="centered")
st.title("🔍 Find Your Unclaimed Money (New Jersey Only)")

with st.form("search_form"):
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    zip_code = st.text_input("Zip Code (optional)")
    email = st.text_input("Email (optional)")
    submitted = st.form_submit_button("Search Now")

if submitted:
    st.info("Searching NJ unclaimed property database... please wait.")
    results = search_nj_unclaimed(first_name, last_name)
    
    if results:
        st.success(f"🎉 We found {len(results)} potential matches!")
        for r in results:
            st.write(f"**Name:** {r['name']}")
            st.write(f"**Address:** {r['address']}")
            st.write(f"**Source:** {r['source']}")
            st.markdown("---")
    else:
        st.warning("Sorry, we didn’t find anything under that name.")
