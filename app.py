import streamlit as st
import requests
from PIL import Image

# --- HYBRID WEB/MOBILE APP CONFIGURATION ---
st.set_page_config(page_title="Eco AI System", page_icon="🌳", layout="centered")

# --- BOTANICAL DATA STRUCTURE (ENGLISH ONLY) ---
BOTANICAL_DB = {
    "Oak Tree": {
        "display_name": "Oak Tree",
        "kids": {
            "growth": "It grows from a tiny little acorn! It takes many years to become a giant king of the forest.",
            "components": "It has lobed leaves, round acorns, and a thick bark that acts like winter armor.",
            "protection": "Do not scratch its bark or break its branches! Keep the ground clean around it.",
            "saving_nature": "It is a huge oxygen factory and provides a completely free home for squirrels and birds.",
            "destruction": "If you cut it down, animals lose their homes, and the air becomes dirty and hard to breathe."
        },
        "adults": {
            "growth": "Slow initial growth rate with a lifespan exceeding 500 years. Prefers deep, fertile soils.",
            "components": "Bark rich in tannins is used in medicine. The wood is extremely dense, heavy, and rot-resistant.",
            "protection": "Requires protection against powdery mildew and prevention of soil compaction around roots.",
            "saving_nature": "Absorbs up to 150 kg of CO2 per year and helps prevent severe soil erosion.",
            "destruction": "Deforestation eliminates a mature ecosystem, destabilizes local water tables, and increases carbon footprint."
        }
    },
    "Snowdrop": {
        "display_name": "Snowdrop",
        "kids": {
            "growth": "It wakes up from a small bulb hidden under the snow, being the very first flower of spring.",
            "components": "It has white petals shaped like little bells and thin, bright green leaves.",
            "protection": "Do not pull it out by the roots! Leave it in the ground so it can bloom again next year.",
            "saving_nature": "It provides the very first warm meal for bees waking up early in the year.",
            "destruction": "If you pick them all, bees won't find food early, and the forest loses its magic."
        },
        "adults": {
            "growth": "Bulbous perennial plant. Blooms in low temperatures, often before the snow completely melts.",
            "components": "Contains galantamine, an active compound extracted and studied for treating nervous system disorders.",
            "protection": "Protected by international conventions. Massive harvesting from the wild is illegal.",
            "saving_nature": "Serves as a crucial indicator of early biodiversity and supports early spring entomofauna.",
            "destruction": "Abusive harvesting degrades forest habitats and jeopardizes the species' natural reproduction."
        }
    }
}

# --- RESPONSIVE GRAPHICAL INTERFACE RENDERING ---
st.title("🌳 Eco AI System")
st.markdown("### *Your Smart Guide to Nature Conservation*")

# Age Selector for Adaptive Content
st.write("---")
selected_age = st.selectbox("👶 Select Age Group / Experience Mode", ["Kids Mode 👶", "Adults Mode 🧔"])
age_key = "kids" if "Kids" in selected_age else "adulti"

# Camera Upload Simulation Container
st.markdown("#### 📸 Scan a Tree, Flower, or Plant")
uploaded_file = st.file_uploader("Take a photo or upload an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    img = Image.open(uploaded_file)
    st.image(img, caption="Image uploaded successfully!", use_container_width=True)
    
    # Mock computer vision processing file naming convention
    file_name_lc = uploaded_file.name.lower()
    detected_species = "Snowdrop" if any(x in file_name_lc for x in ["ghiocel", "flower", "snowdrop"]) else "Oak Tree"
    
    plant_data = BOTANICAL_DB[detected_species]
    st.success(f"🤖 AI Engine identified the species as: **{plant_data['display_name']}**!")
    st.write("---")
    
    # Render Dynamic Data Panels
    info = plant_data[age_key]
    st.info(f"🔄 **How it develops:** {info['growth']}")
    st.info(f"🔬 **What it contains / Structure:** {info['components']}")
    st.success(f"💚 **How to protect it:** {info['protection']}")
    st.success(f"🌍 **How it saves nature:** {info['saving_nature']}")
    st.error(f"❌ **Downsides of cutting/destruction:** {info['destruction']}")
    
    # --- 💬 CONVERSATIONAL AI COMPONENT ---
    st.write("---")
    st.markdown("### 💬 Continuous Chat with Eco AI!")
    st.write(f"Ask any follow-up questions adapted for {selected_age}:")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask something (e.g., What animals live in this tree?)"):
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            prompt_lc = prompt.lower()
            # Intelligent Keyword-based NLP routing in English
            if any(x in prompt_lc for x in ["animal", "insect", "bird", "squirrel", "nest"]):
                ai_response = "🐿️ Beside squirrels, this tree provides a home for owls, woodpeckers, and hundreds of insect species!" if detected_species == "Oak Tree" else "🐛 Tiny soil insects and early spring beetles find shelter around this flower as the snow melts."
            elif any(x in prompt_lc for x in ["water", "bulb", "soil", "care", "grow"]):
                ai_response = "💧 Young trees need watering during dry seasons, but mature oaks draw water deep from the underground with huge roots." if detected_species == "Oak Tree" else "🌱 These flowers love damp forest soil. Their bulbs store energy during winter to bloom early."
            elif any(x in prompt_lc for x in ["bee", "honey", "nectar"]):
                ai_response = "🐝 Yes! These early flowers are vital for bees, providing the first nectar when temperatures rise just above 0°C."
            else:
                ai_response = f"🤖 Excellent question! In the final version, the connected LLM will generate real-time answers for {selected_age}."
            
            st.markdown(ai_response)
        st.session_state.messages.append({"role": "assistant", "content": ai_response})
