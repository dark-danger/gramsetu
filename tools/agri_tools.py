"""
GramSetu AI - Agriculture Math & Seed/Fertilizer Calculators
Provides exact scientific measurements per acre/bigha.
"""
import re

def calculate_agri_requirements(prompt: str, user_land_str: str = None) -> dict:
    lower = prompt.lower()

    # Extract acres from prompt or fallback to user_land_str
    acre_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:acre|acres|एकड़)', prompt, re.IGNORECASE)
    acres = None
    if acre_match:
        acres = float(acre_match.group(1))
    elif user_land_str:
        m_saved = re.search(r'(\d+(?:\.\d+)?)\s*(?:acre|acres|एकड़)', user_land_str, re.IGNORECASE)
        if m_saved:
            acres = float(m_saved.group(1))

    # Detect crop
    crop = "wheat"
    crop_name = "Wheat (गेहूं)"
    if re.search(r'\b(mustard|sarson)\b', lower):
        crop = "mustard"
        crop_name = "Mustard (सरसों)"
    elif re.search(r'\b(rice|dhan|paddy)\b', lower):
        crop = "rice"
        crop_name = "Paddy/Rice (धान)"

    if acres is None:
        acres = 1.0  # Default standard 1 acre calculation

    # Calculations
    res = {}
    if crop == "wheat":
        min_seed = round(acres * 40, 1)
        max_seed = round(acres * 45, 1)
        dap_bags = round(acres * 1, 1)
        urea_bags = round(acres * 2, 1)
        potash_bags = round(acres * 0.5, 1)
        zinc_kg = round(acres * 10, 1)

        res["tool_name"] = "Agri Calculator (Seed & Fertilizer)"
        res["badge"] = f"🌾 Calculated for {acres} Acre(s) of {crop_name}"
        res["text"] = (
            f"🌾 **{crop_name} Seed & Fertilizer Calculation for {acres} Acre(s):**\n\n"
            f"1. **Seed Requirement (बीज मात्रा):**\n"
            f"   • समय पर बुवाई: **{min_seed} से {max_seed} किलोग्राम** ({min_seed/100:.2f} से {max_seed/100:.2f} क्विंटल) बीज।\n"
            f"   • पछेती बुवाई (दिसंबर): **{round(acres*50, 1)} से {round(acres*55, 1)} किलोग्राम** बीज।\n\n"
            f"2. **Fertilizer Requirement (खाद की मात्रा):**\n"
            f"   • **DAP (50kg बैग):** **{dap_bags} बैग** (बुवाई के समय Basal).\n"
            f"   • **Urea (45kg बैग):** **{urea_bags} बैग** (21 दिन और 45 दिन की सिंचाई पर 2 बार में).\n"
            f"   • **MOP पोटाश (50kg बैग):** **{potash_bags} बैग**.\n"
            f"   • **जिंक सल्फेट (33%):** **{zinc_kg} kg**."
        )

    elif crop == "mustard":
        min_seed = round(acres * 1.5, 2)
        max_seed = round(acres * 2.0, 2)
        ssp_bags = round(acres * 1, 1)
        urea_bags = round(acres * 0.8, 1)
        sulphur_kg = round(acres * 10, 1)

        res["tool_name"] = "Agri Calculator (Mustard)"
        res["badge"] = f"🌼 Calculated for {acres} Acre(s) of {crop_name}"
        res["text"] = (
            f"🌼 **{crop_name} Seed & Fertilizer Calculation for {acres} Acre(s):**\n\n"
            f"1. **Seed Requirement (बीज मात्रा):** **{min_seed} से {max_seed} किलोग्राम**।\n"
            f"2. **Fertilizer Requirement:** **{ssp_bags} बैग SSP (50kg)** + **{urea_bags} बैग यूरिया** + **{sulphur_kg} kg सल्फर 90%**."
        )

    elif crop == "rice":
        hybrid_seed = round(acres * 6, 1)
        basmati_seed = round(acres * 10, 1)
        res["tool_name"] = "Agri Calculator (Rice)"
        res["badge"] = f"🌾 Calculated for {acres} Acre(s) of {crop_name}"
        res["text"] = (
            f"🌾 **{crop_name} Seed Requirement for {acres} Acre(s):**\n\n"
            f"• **Hybrid धान:** **{hybrid_seed} किलोग्राम**।\n"
            f"• **बासमती / देसी किस्में:** **{basmati_seed} किलोग्राम**।"
        )

    return res

def convert_land_area(acres: float) -> dict:
    pucca_bigha = round(acres * 1.6, 2)
    kaccha_bigha = round(acres * 4.8, 2)
    sq_yards = f"{int(acres * 4840):,}"
    sq_feet = f"{int(acres * 43560):,}"
    hectares = round(acres * 0.404686, 3)

    return {
        "acres": acres,
        "pucca_bigha": pucca_bigha,
        "kaccha_bigha": kaccha_bigha,
        "sq_yards": sq_yards,
        "sq_feet": sq_feet,
        "hectares": hectares,
        "text": (
            f"📐 **Land Area Calculation for {acres} Acre(s):**\n\n"
            f"• **Pucca Bigha (पक्का बीघा):** **{pucca_bigha} Bigha** (Standard: 1 Acre = 1.6 Pucca Bigha)\n"
            f"• **Kaccha Bigha (कच्चा बीघा):** **{kaccha_bigha} Bigha** (1 Pucca Bigha = 3 Kaccha Bigha)\n"
            f"• **Square Yards (वर्ग गज / Gaj):** **{sq_yards} sq. yards**\n"
            f"• **Square Feet (वर्ग फुट):** **{sq_feet} sq. ft**\n"
            f"• **Hectares (हेक्टेयर):** **{hectares} Ha**"
        )
    }
