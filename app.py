import streamlit as st
import random
import time

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="CarryMe Store - Product Description Generator",
    page_icon="🏠",
    layout="centered"
)

# ---------- CUSTOM CSS FOR BETTER UI ----------
st.markdown("""
    <style>
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-size: 18px;
        padding: 10px 24px;
        border-radius: 8px;
        border: none;
    }
    .stButton > button:hover {
        background-color: #45a049;
    }
    .generated-text {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        font-family: monospace;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------- TITLE & HEADER ----------
st.title("🏠 CarryMe Store")
st.subheader("AI-Powered Product Description Generator")
st.markdown("*Create compelling product descriptions for home decor, appliance covers, towels, and table covers*")
st.divider()

# ---------- SIDEBAR: TONE PRESETS ----------
st.sidebar.header("⚙️ Settings")
st.sidebar.markdown("Choose your writing style:")

# Tone options with descriptions
tone_options = {
    "Professional": "Formal, feature-focused, suitable for Amazon/Flipkart",
    "Casual": "Friendly, conversational, great for social media",
    "Luxury": "Elegant, premium-sounding, high-end positioning",
    "Eco-friendly": "Natural, sustainable, organic-focused",
    "Urgent/Buy Now": "Action-oriented, limited time feel",
    "Storytelling": "Narrative style, emotional connection"
}

# Tone selection dropdown
selected_tone = st.sidebar.selectbox(
    "Select Tone",
    options=list(tone_options.keys()),
    index=0,
    help=tone_options["Professional"]
)

# Display tone description
st.sidebar.caption(tone_options[selected_tone])

# ---------- PRODUCT CATEGORY (Optional) ----------
st.sidebar.markdown("---")
st.sidebar.markdown("### Product Category (Optional)")
category = st.sidebar.selectbox(
    "Helps generate better descriptions",
    ["Auto-detect", "Appliance Cover", "Table Cover", "Towels", "Home Decor"],
    index=0
)

# ---------- MAIN INPUT AREA ----------
st.markdown("### 📝 Enter Product Features")
st.markdown("*Separate features with commas or write in paragraphs*")

# Text input for product features
product_features = st.text_area(
    "Product features",
    placeholder="Example: 100% cotton, absorbent, quick-dry, machine washable, 20x30 inches, available in 5 colors",
    height=150,
    help="Include materials, size, colors, special features, etc."
)

# Character counter
if product_features:
    st.caption(f"📊 {len(product_features)} characters | ~{len(product_features.split())} words")

# Optional: Additional keywords
with st.expander("➕ Add specific keywords (optional)"):
    keywords = st.text_input(
        "Keywords to include",
        placeholder="e.g., soft, durable, eco-friendly, premium"
    )

# ---------- GENERATE BUTTON ----------
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    generate_button = st.button("🚀 Generate Description", use_container_width=True)

# ---------- GENERATION FUNCTION ----------
def generate_description(features, tone, category_hint="", keywords=""):
    """Generate product description based on inputs"""
    
    # Parse features into a list
    if "," in features:
        feature_list = [f.strip() for f in features.split(",")]
    else:
        feature_list = [features]
    
    # Category-specific opening lines
    category_openers = {
        "Appliance Cover": "Protect your appliances in style with",
        "Table Cover": "Transform your dining experience with",
        "Towels": "Experience ultimate comfort with",
        "Home Decor": "Elevate your living space with"
    }
    
    opener = category_openers.get(category_hint, "Introducing")
    if category_hint == "Auto-detect":
        # Simple detection logic
        if "cover" in features.lower():
            opener = "Protect and enhance with"
        elif "towel" in features.lower():
            opener = "Indulge in luxury with"
        else:
            opener = "Upgrade your home with"
    
    # Tone-specific templates
    templates = {
        "Professional": [
            f"{opener} this premium-quality product. Key features include: {', '.join(feature_list[:3])}. Designed for durability and performance, it meets the highest standards of home textile excellence. Perfect for everyday use.",
            f"This product offers exceptional value with {feature_list[0] if feature_list else 'superior quality'}. {', '.join(feature_list[:2])} ensures long-lasting satisfaction. An ideal choice for discerning customers.",
        ],
        "Casual": [
            f"Hey there! Meet your new favorite {category_hint.lower() if category_hint not in ['Auto-detect', 'Home Decor'] else 'product'}! 🎉 {feature_list[0] if feature_list else 'Super comfy'} and {feature_list[1] if len(feature_list) > 1 else 'super stylish'}. Trust me, you're going to love this one!",
            f"Ready to level up your home game? Check this out! {feature_list[0]} - sounds good, right? It's perfect for {feature_list[1] if len(feature_list) > 1 else 'everyday use'}. Grab yours today!",
        ],
        "Luxury": [
            f"Experience unparalleled elegance with this exquisite {category_hint.lower() if category_hint not in ['Auto-detect', 'Home Decor'] else 'creation'}. Crafted with {feature_list[0] if feature_list else 'premium materials'}, {feature_list[1] if len(feature_list) > 1 else 'exceptional craftsmanship'} elevates everyday moments into extraordinary experiences.",
            f"Indulge in the finest {category_hint.lower() if category_hint not in ['Auto-detect', 'Home Decor'] else 'home textile'}. {feature_list[0]} meets sophisticated design. Where luxury meets functionality.",
        ],
        "Eco-friendly": [
            f"Made with love for your home and our planet. {feature_list[0] if feature_list else 'Sustainably sourced'} materials, {feature_list[1] if len(feature_list) > 1 else 'eco-friendly production'}. Choose comfort that doesn't cost the Earth. 🌍",
            f"Nature-friendly and people-friendly! {feature_list[0] if feature_list else '100% natural'}. Biodegradable, sustainable, and absolutely beautiful for your home.",
        ],
        "Urgent/Buy Now": [
            f"🔥 LIMITED TIME! Get this {category_hint.lower()} NOW. {feature_list[0] if feature_list else 'Premium quality'} + {feature_list[1] if len(feature_list) > 1 else 'amazing value'}. Stock is flying! Click ADD TO CART before it's gone!",
            f"⚡ FLASH SALE! Don't miss out on {feature_list[0]}. {len(feature_list) if len(feature_list) > 1 else 2}+ reasons to buy: {', '.join(feature_list[:3])}. Order in the next 24 hours!",
        ],
        "Storytelling": [
            f"Picture this: You wake up, and your home feels {feature_list[0] if feature_list else 'cozy and inviting'}. That's exactly what this {category_hint.lower() if category_hint not in ['Auto-detect', 'Home Decor'] else 'piece'} brings. {feature_list[1] if len(feature_list) > 1 else 'Every detail'} tells a story of comfort and care.",
            f"There was a time when {feature_list[0] if feature_list else 'ordinary products'} were enough. Then came this {category_hint.lower() if category_hint not in ['Auto-detect', 'Home Decor'] else 'product'}. Now, your home feels complete.",
        ]
    }
    
    # Get random template for selected tone
    tone_templates = templates.get(tone, templates["Professional"])
    description = random.choice(tone_templates)
    
    # Add keywords if provided
    if keywords:
        description += f"\n\n✨ {keywords} ✨"
    
    # Add call to action based on tone
    if tone == "Urgent/Buy Now":
        description += "\n\n📦 Free shipping on orders above ₹499!"
    elif tone == "Luxury":
        description += "\n\n🌟 Limited edition - Only a few pieces available"
    else:
        description += "\n\n🏷️ Shop now at CarryMe Store"
    
    return description

# ---------- DISPLAY GENERATED DESCRIPTION ----------
if generate_button:
    if not product_features or product_features.strip() == "":
        st.error("⚠️ Please enter product features before generating!")
    else:
        with st.spinner("✨ Crafting your perfect description..."):
            time.sleep(1)  # Simulate processing (remove in production)
            description = generate_description(
                product_features, 
                selected_tone, 
                category,
                keywords if keywords else ""
            )
        
        st.success("✅ Description generated successfully!")
        st.markdown("### 📄 Generated Description")
        st.markdown(f'<div class="generated-text">{description}</div>', unsafe_allow_html=True)
        
        # Copy button workaround (users can select text)
        st.info("💡 Tip: Select the text above and press Ctrl+C to copy")
        
        # Optional: Add to session state for history
        if 'history' not in st.session_state:
            st.session_state.history = []
        st.session_state.history.append({
            "features": product_features,
            "tone": selected_tone,
            "description": description
        })
        
        # Show quick actions
        with st.expander("🔧 Quick Actions"):
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("📋 Clear & New"):
                    st.rerun()
            with col_b:
                if st.button("👍 This works! Use similar tone"):
                    st.info("Great! Keep using the same settings for your product batch")

# ---------- TIPS SECTION (Always visible) ----------
with st.expander("💡 Pro Tips for Better Descriptions"):
    st.markdown("""
    **For best results:**
    1. **Be specific** - Include material, size, color, weight
    2. **Add benefits** - Not just "cotton" but "soft 100% cotton that absorbs 2x faster"
    3. **Include numbers** - Dimensions, quantity, price points
    4. **Mention use cases** - "Perfect for kitchen", "Ideal for gift giving"
    
    **Example for CarryMe Store:**
    > 100% cotton, 20x30 inches, absorbent, quick-dry, machine washable, 5 colors available, includes matching hanger, ideal for guest bathroom
    """)

# ---------- HISTORY SECTION (Optional) ----------
if 'history' in st.session_state and len(st.session_state.history) > 0:
    with st.expander("📜 Recent Descriptions"):
        for i, item in enumerate(reversed(st.session_state.history[-3:])):
            st.markdown(f"**{i+1}. Tone: {item['tone']}**")
            st.caption(f"Features: {item['features'][:100]}...")
            st.text(item['description'][:150] + "...")
            st.divider()

# ---------- FOOTER ----------
st.divider()
st.markdown(
    "<center>🚀 CarryMe Store - AI Description Generator | Powered by Streamlit</center>",
    unsafe_allow_html=True
)
