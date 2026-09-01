import streamlit as st
import requests
from PIL import Image

# Configurare pagină stilizată ca o aplicație de mobil
st.set_page_config(page_title="Eco AI System", page_icon="🌳", layout="centered")

# --- BAZA DE DATE GLOBALĂ BILINGVĂ ---
plant_database = {
    "Stejar (Oak Tree)": {
        "RO": {
            "title": "🌳 Stejarul - Regele Pădurii",
            "kids": {
                "growth": "🌱 Crește dintr-o ghindă mică! Îi ia mulți ani să devină uriaș și puternic.",
                "components": "🍁 Are frunze crestate, ghinde rotunde și o scoarță groasă ca o armură.",
                "protection": "💧 Nu îi scrijeli scoarța și nu îi rupe crengile! Lasă pământul curat în jur.",
                "saving_nature": "🐿️ Este o adevărată fabrică de oxigen și oferă căsuță gratuită veverițelor.",
                "destruction_downside": "😢 Dacă mă tai, animăluțele își pierd casa, iar aerul devine mai greu de respirat."
            },
            "adulti": {
                "growth": "📈 Ritm de creștere lent, longevitate de peste 500 de ani. Preferă soluri adânci și fertile.",
                "components": "🧪 Scoarța bogată în taninuri are uz medicinal. Lemnul este dens și foarte rezistent.",
                "protection": "🛡️ Necesită protecție împotriva dăunătorilor și evitarea compactării solului.",
                "saving_nature": "🌍 Absoarbe până la 150 kg de CO2 pe an și previne eroziunea solului.",
                "destruction_downside": "⚠️ Defrișarea elimină un ecosistem matur și destabilizează pânza freatică."
            }
        },
        "EN": {
            "title": "🌳 The Oak Tree - King of the Forest",
            "kids": {
                "growth": "🌱 I grow from a tiny little acorn! It takes many years to become a giant, strong tree.",
                "components": "🍁 I have lobed leaves, round acorns, and a thick bark that acts like armor.",
                "protection": "💧 Do not carve into my bark or break my branches! Keep the soil around me clean.",
                "saving_nature": "🐿️ I am a real oxygen factory and I provide a free home for squirrels and birds.",
                "destruction_downside": "😢 If you cut me down, little animals lose their homes, and the air becomes dirty."
            },
            "adulti": {
                "growth": "📈 Slow growth rate in the early years, longevity exceeding 500 years. Prefers deep soils.",
                "components": "🧪 The bark is rich in tannins used in medicine. The wood is extremely dense and durable.",
                "protection": "🛡️ Requires protection against pests (caterpillars, powdery mildew) and avoiding soil compaction.",
                "saving_nature": "🌍 Absorbs up to 150 kg of CO2 per year, stabilizes the soil, and supports local biodiversity.",
                "destruction_downside": "⚠️ Deforestation eliminates a mature ecosystem, increases carbon footprint, and degrades soil."
            }
        }
    }
}

# --- TEXTE INTERFAȚĂ BILINGVĂ ---
texte_interfata = {
    "RO": {
        "subtitle": "### *Ghidul tău inteligent pentru protecția naturii*",
        "label_lang": "🌐 Selectează Limba",
        "label_age": "👶 Grupa de vârstă",
        "kids_option": "Kids (Copii)",
        "adults_option": "Adults (Adulți)",
        "scan_title": "#### 📸 Scanează un Copac sau o Floare",
        "upload_btn": "Fă o poză sau încarcă o imagine...",
        "success_upload": "Imagine încărcată cu succes",
        "ai_detected": "🤖 AI-ul a identificat specia: **Stejar (Oak Tree)**!",
        "label_growth": "🔄 **Cum se dezvoltă:**",
        "label_comp": "🔬 **Ce conține / Structură:**",
        "label_prot": "💚 **Cum trebuie protejat:**",
        "label_save": "🌍 **Cum salvează natura:**",
        "label_danger": "❌ **Dezavantajele distrugerii/tăierii:**",
        "chat_title": "### 💬 Vorbește mai departe cu Eco AI!",
        "chat_sub": "Pune orice întrebare suplimentară despre această specie:",
        "chat_input": "Întreabă-mă ceva (ex: Ce animale trăiesc în stejar?)",
        "ans_animals": "🐿️ Pe lângă veverițe, în stejar trăiesc bufnițe, cerbi care îi mănâncă ghindele și sute de specii de insecte mici!",
        "ans_water": "💧 Stejarii tineri au nevoie de apă în perioadele secetoase, dar cei bătrâni își iau singuri apa din adâncul pământului.",
        "ans_default": "🤖 Aceasta este o întrebare excelentă! În versiunea finală, aici vei primi un răspuns IA complet personalizat."
    },
    "EN": {
        "subtitle": "### *Your Smart Guide to Nature Conservation*",
        "label_lang": "🌐 Select Language",
        "label_age": "👶 Age Group",
        "kids_option": "Kids",
        "adults_option": "Adults",
        "scan_title": "#### 📸 Scan a Tree or a Flower",
        "upload_btn": "Take a photo or upload an image...",
        "success_upload": "Image uploaded successfully",
        "ai_detected": "🤖 AI identified the species: **Oak Tree (Stejar)**!",
        "label_growth": "🔄 **How it grows:**",
        "label_comp": "🔬 **Composition / Structure:**",
        "label_prot": "💚 **How to protect it:**",
        "label_save": "🌍 **How it saves nature:**",
        "label_danger": "❌ **Consequences of destruction/cutting:**",
        "chat_title": "### 💬 Keep talking to Eco AI!",
        "chat_sub": "Ask any follow-up questions about this species:",
        "chat_input": "Ask me anything (e.g., What animals live in the oak tree?)",
        "ans_animals": "🐿️ Besides squirrels, oaks host owls, deer that eat their acorns, and hundreds of tiny insect species!",
        "ans_water": "💧 Young oaks need water during droughts, but old ones fetch water from deep underground via massive roots.",
        "ans_default": "🤖 That is an excellent question! In the final version, you will receive a fully customized AI response here."
    }
}

# --- RENDERING INTERFAȚĂ ---
st.title("🌳 Eco AI System")

# Resetare chat dacă se schimbă limba (pentru a evita amestecarea limbilor în istoric)
if "limba_precedenta" not in st.session_state:
    st.session_state.limba_precedenta = "RO"

col1, col2 = st.columns(2)
with col1:
    limba = st.selectbox("🌐 Language", ["RO", "EN"])
with col2:
    txt = texte_interfata[limba]
    varsta = st.selectbox(txt["label_age"], [txt["kids_option"], txt["adults_option"]])

if limba != st.session_state.limba_precedenta:
    st.session_state.messages = []
    st.session_state.limba_precedenta = limba

st.markdown(txt["subtitle"])
mod_cheie = "kids" if ("Kids" in varsta or "Copii" in varsta) else "adulti"

st.write("---")
st.markdown(txt["scan_title"])
fisier_imagine = st.file_uploader(txt["upload_btn"], type=["jpg", "jpeg", "png"])

if fisier_imagine is not None:
    imagine = Image.open(fisier_imagine)
    st.image(imagine, caption=txt["success_upload"], use_container_width=True)
    st.success(txt["ai_detected"])
    st.write("---")
    
    # Date botanice din DB
    date_planta = plant_database["Stejar (Oak Tree)"][limba]
    st.subheader(date_planta["title"])
    info = date_planta[mod_cheie]
    
    st.info(f"{txt['label_growth']} {info['growth']}")
    st.info(f"{txt['label_comp']} {info['components']}")
    st.success(f"{txt['label_prot']} {info['protection']}")
    st.success(f"{txt['label_save']} {info['saving_nature']}")
    st.error(f"{txt['label_danger']} {info['destruction_downside']}")
    
    # === CHAT INTERACTIV BILINGV ===
    st.write("---")
    st.markdown(txt["chat_title"])
    st.write(txt["chat_sub"])
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input(txt["chat_input"]):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            p_low = prompt.lower()
            if "animal" in p_low or "veveri" in p_low or "squirrel" in p_low or "bird" in p_low:
                raspuns_ai = txt["ans_animals"]
            elif "apă" in p_low or "ud" in p_low or "water" in p_low or "care" in p_low or "îngrij" in p_low:
                raspuns_ai = txt["ans_water"]
            else:
                raspuns_ai = txt["ans_default"]
            
            st.markdown(raspuns_ai)
        st.session_state.messages.append({"role": "assistant", "content": raspuns_ai})
