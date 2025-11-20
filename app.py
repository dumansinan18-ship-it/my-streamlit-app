import streamlit as st
import geopandas as gpd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Türkiye Haritası", layout="wide")
st.title("Türkiye Haritası – İl ve Komşu İl Görüntüleyici")
# Tanıtıcı açıklama
st.markdown("""
**Sinan Duman tarafından Sosyal Bilgiler dersi için hazırlanmıştır.**  

Bu uygulama, Türkiye’nin coğrafi ve idari yapısını görselleştirmenizi sağlar.  
Haritalar üzerinde etkileşimli olarak bölgeleri inceleyebilir ve eğitim amaçlı bilgiler edinebilirsiniz.
""")
# GeoJSON dosyasını oku
geojson_path = "turkiye.geojson"

try:
    gdf = gpd.read_file(geojson_path)
except Exception as e:
    st.error(f"GeoJSON dosyası okunamadı: {e}")
    st.stop()

# İl isim kolonunu bul
name_col = None
for col in gdf.columns:
    if "name" in col.lower() or "il" in col.lower() or "province" in col.lower():
        name_col = col
        break

if not name_col:
    st.error("İl ismi kolonu bulunamadı!")
    st.stop()

# İl seçimi
secili_il = st.selectbox("Bir il seçin:", sorted(gdf[name_col].unique()))

# Seçili ilin geometrisi
geom_il = gdf[gdf[name_col] == secili_il].geometry.iloc[0]

# Komşu illeri bul (geometrik olarak temas edenler)
komsular = gdf[gdf.geometry.touches(geom_il)][name_col].tolist()

st.subheader(f"📍 Seçili il: {secili_il}")
st.write(f"**Komşu iller:** {', '.join(komsular) if komsular else 'Yok'}")

# Harita çizimi
fig, ax = plt.subplots(figsize=(8, 8))
gdf.plot(ax=ax, color="#dddddd", edgecolor="black")

# Seçilen ili renklendir
gdf[gdf[name_col] == secili_il].plot(ax=ax, color="yellow", edgecolor="black")

# Komşuları renklendir
gdf[gdf[name_col].isin(komsular)].plot(ax=ax, color="orange", edgecolor="black")

ax.set_axis_off()
st.pyplot(fig)

