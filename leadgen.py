import streamlit as st
import pandas as pd
import ml


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)


def icon(icon_name):
    st.markdown(f'<i class="material-icons">{icon_name}</i>', unsafe_allow_html=True)


@st.cache
def get_df(v):
    ml.start_tor()
    return (gig_scraper.craigslist_gig_scrape(v))


def next(df):
    if st.checkbox("Remove Duplicate Titles"):
        df = df.drop_duplicates(subset=['titles'], keep="first")
        df = df.reset_index()
        # df=df.drop(['timestamp'], axis = 1)
        st.write(df)
        icon("search")
        selected = st.text_input("", "Search...")
        if st.button("OK"):
            df = df[df['titles'].str.contains(selected)]
            L = df.to_html(escape=False)
            st.write(L, unsafe_allow_html=True)


@st.cache
def count():
    m = ml.get_countries()
    return (m)

def scrape_by_category():
    cou = count()
    values = cou['link']
    options = cou['pais']
    value = st.sidebar.selectbox("Pais", options)
    if st.sidebar.checkbox("Next"):
        v = cou[cou['pais'] == value]
        p = v['link']
        cate = ml.get_cat(p.iloc[0])
        value2 = st.sidebar.selectbox("Categorias", cate["sub-title"])
        if value2:
            v2 = cate[cate["sub-title"] == value2]
            v2 = v2["link"]
            if st.sidebar.checkbox("Empezar"):
                df = ml.get_the_loot(str(v2.iloc[0]))
                st.write('Hola, *Encontre:* ')
                st.write(df)
                st.write('*Paginas de Resultados!* :sunglasses:')
                age = st.slider('Cuantas paginas quieres analizar?', 0, df,1)
                st.write("Tiempo de espera es: ", (age * 20) / 60, 'minutos')

                if st.checkbox("Comenzar"):
                    d=ml.single_scrape(str(v2.iloc[0]),age)
                    d

def make_link(search):
    search=search.split()
    l = "https://listado.mercadolibre.com.mx/"
    #x = "#D[A:"
    c = 0
    for s in search:
        c = c + 1
        if c == len(search):
            l = l + s
        else:
            l = l + s + "-"

    #for s in search:
     #   x = x + "%20" + s
    #x = x + "]"
    return(l)


def get_results(busqueda):
    l=make_link(busqueda)
    if st.sidebar.checkbox("Empezar"):
        df = ml.get_the_loot(l)
        return(df)

def scrape_by_search(busqueda):
    df=get_results(busqueda)
    l = make_link(busqueda)
    if df!="Intenta de Nuevo":
        st.write('Hola, *Encontre:* ')
        st.write(df)
        st.write('*Paginas de Resultados!* :sunglasses:')
        age = st.slider('Cuantas paginas quieres analizar?', 0, df, 1)
        st.write("Tiempo de espera es: ", (age * 20) / 60, 'minutos')
        if st.checkbox("Comenzar"):
            d = ml.single_scrape2(str(l), age)
            d
    else:
        st.write("Intenta de nuevo")


def main():
    st.sidebar.header('Analizador Mercadolibre')
    st.sidebar.subheader('Escoge el tipo de busqueda')
    # local_css("style.css")
    ml.start_tor()
    task = st.sidebar.selectbox("Tipo de Busqueda", ["Por Categoria", "Por Busqueda"])


    st.title('Analizador Mercadolibre')
    ml.start_tor()
    if st.sidebar.checkbox("Siguente"):
        if task == "Por Categoria":
            scrape_by_category()
        if task == "Por Busqueda":
            busqueda = st.sidebar.text_input("Busqueda")
            if busqueda:
                st.write(busqueda)
                scrape_by_search(busqueda)
    remote_css('https://fonts.googleapis.com/icon?family=Material+Icons')



if __name__ == '__main__':
    main()
