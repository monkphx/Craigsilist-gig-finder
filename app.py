import streamlit as st
import pandas as pd
import gig_scraper
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)    

def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)
@st.cache
def get_df(v):
    try:
	    tor_process=gig_scraper.start_tor()
    except OSError:
	    pass
    return(gig_scraper.craigslist_gig_scrape(v))

def next(df):
    if st.checkbox("Remove Duplicate Titles"):
            df=df.drop_duplicates(subset=['titles'],keep="first")
            df=df.reset_index()
            #df=df.drop(['timestamp'], axis = 1)
            st.write(df)
            icon("search")
            selected = st.text_input("", "Search...")
            if st.button("OK"):
                df=df[df['titles'].str.contains(selected)]
                L=df.to_html(escape=False)
                st.write(L, unsafe_allow_html=True)
def main():
    #local_css("style.css")
    st.title('Craigslist Gig Scraper')

    remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')
    values=("/d/computer-gigs/search/cpg","/d/creative-gigs/search/crg","/d/crew-gigs/search/cwg","/d/domestic-gigs/search/dmg","/d/event-gigs/search/evg","/d/labor-gigs/search/lbg","/d/talent-gigs/search/tlg","/d/writing-gigs/search/wrg")
    options=("Computer","Creative","Crew","Domestic","Event","Labor","Talent","Writing")
    value=st.sidebar.selectbox("Gig Type",options) 
    if st.sidebar.checkbox("Start"):
	    v=values[options.index(value)]
	    df=get_df(v)
	    df
	    next(df)
if __name__ == '__main__':
	main()
